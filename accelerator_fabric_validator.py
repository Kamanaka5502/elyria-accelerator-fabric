#!/usr/bin/env python3
"""
Elyria Accelerator Fabric Validator

Protected public proof surface.
This file is a software-adjacent public validator for the proof corridor.
It is not the protected production runtime, not CUDA integration, and not SMC hardware.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

EXECUTE = "EXECUTE"
REFUSE = "REFUSE"
ESCALATE = "ESCALATE"
HALT = "HALT"
THROTTLE = "THROTTLE"
REVOKE_DISPATCH = "REVOKE_DISPATCH"

REQUIRED_FIELDS = [
    "workload_id",
    "tenant_id",
    "actor_id",
    "model_id",
    "model_risk_class",
    "requested_action",
    "data_classification",
    "authority_state",
    "custody_state",
    "policy_state",
    "revocation_status",
    "corridor_id",
    "gpu_partition",
    "fabric_domain",
    "capacity_state",
    "thermal_state",
    "energy_debt_state",
    "scheduler_integrity",
    "standing_decay_state",
    "replay_reference",
    "receipt_parent",
    "issued_at",
]


@dataclass(frozen=True)
class FabricDecision:
    workload_id: str
    boundary_outcome: str
    dispatch_allowed: bool
    reason_code: str
    fabric_action: str
    missing_fields: List[str]
    standing_summary: Dict[str, str]
    input_hash: str
    receipt_hash: str
    replay_token: str


def canonical_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def canonical_hash(payload: Dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _standing_summary(payload: Dict[str, Any]) -> Dict[str, str]:
    return {
        "authority": str(payload.get("authority_state", "MISSING")),
        "custody": str(payload.get("custody_state", "MISSING")),
        "policy": str(payload.get("policy_state", "MISSING")),
        "revocation": str(payload.get("revocation_status", "MISSING")),
        "capacity": str(payload.get("capacity_state", "MISSING")),
        "thermal": str(payload.get("thermal_state", "MISSING")),
        "energy_debt": str(payload.get("energy_debt_state", "MISSING")),
        "scheduler": str(payload.get("scheduler_integrity", "MISSING")),
        "standing_decay": str(payload.get("standing_decay_state", "MISSING")),
        "replay": "PRESENT" if payload.get("replay_reference") else "MISSING",
    }


def evaluate(payload: Dict[str, Any]) -> FabricDecision:
    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    workload_id = str(payload.get("workload_id", "UNKNOWN"))

    outcome = EXECUTE
    reason = "ACCELERATOR_STANDING_ADMISSIBLE"
    action = "ALLOW_DISPATCH"
    dispatch = True

    if missing:
        outcome, reason, action, dispatch = ESCALATE, "MISSING_REQUIRED_FIELDS", "REVIEW_REQUIRED", False
    elif payload["authority_state"] != "VALID":
        outcome, reason, action, dispatch = REFUSE, "AUTHORITY_NOT_VALID", "BLOCK_DISPATCH", False
    elif payload["revocation_status"] != "CLEAR":
        outcome, reason, action, dispatch = REFUSE, "REVOCATION_NOT_CLEAR", "BLOCK_DISPATCH", False
    elif payload["custody_state"] == "BROKEN":
        outcome, reason, action, dispatch = HALT, "CUSTODY_BROKEN", "STOP_EXECUTION", False
    elif payload["policy_state"] != "CURRENT":
        outcome, reason, action, dispatch = REFUSE, "POLICY_NOT_CURRENT", "BLOCK_DISPATCH", False
    elif payload["thermal_state"] == "CRITICAL":
        outcome, reason, action, dispatch = HALT, "THERMAL_CRITICAL", "STOP_EXECUTION", False
    elif payload["thermal_state"] == "DEGRADED":
        outcome, reason, action, dispatch = THROTTLE, "THERMO_STANDING_DEGRADED", "NARROW_OR_REVIEW", False
    elif payload["capacity_state"] == "OVERBURDENED":
        outcome, reason, action, dispatch = HALT, "CAPACITY_OVERBURDENED", "STOP_EXECUTION", False
    elif payload["capacity_state"] == "DEGRADED":
        outcome, reason, action, dispatch = THROTTLE, "CAPACITY_DEGRADED", "NARROW_OR_REVIEW", False
    elif payload["energy_debt_state"] == "EXCEEDED":
        outcome, reason, action, dispatch = HALT, "ENERGY_DEBT_EXCEEDED", "STOP_EXECUTION", False
    elif payload["scheduler_integrity"] != "VALID":
        outcome, reason, action, dispatch = ESCALATE, "SCHEDULER_INTEGRITY_NOT_VALID", "REVIEW_REQUIRED", False
    elif payload["standing_decay_state"] == "ACTIVE":
        outcome, reason, action, dispatch = REVOKE_DISPATCH, "STANDING_DECAY_ACTIVE", "REVOKE_OR_REBOUND", False
    elif not payload.get("replay_reference"):
        outcome, reason, action, dispatch = HALT, "REPLAY_REFERENCE_MISSING", "BLOCK_CERTIFICATION", False

    input_hash = canonical_hash(payload)
    receipt_payload = {
        "workload_id": workload_id,
        "boundary_outcome": outcome,
        "dispatch_allowed": dispatch,
        "reason_code": reason,
        "fabric_action": action,
        "input_hash": input_hash,
    }
    receipt_hash = canonical_hash(receipt_payload)
    replay_token = canonical_hash({
        "receipt_hash": receipt_hash,
        "receipt_parent": payload.get("receipt_parent"),
        "corridor_id": payload.get("corridor_id"),
    })

    return FabricDecision(
        workload_id=workload_id,
        boundary_outcome=outcome,
        dispatch_allowed=dispatch,
        reason_code=reason,
        fabric_action=action,
        missing_fields=missing,
        standing_summary=_standing_summary(payload),
        input_hash=input_hash,
        receipt_hash=receipt_hash,
        replay_token=replay_token,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Elyria Accelerator Fabric workload envelope.")
    parser.add_argument("path", type=Path, help="Path to workload envelope JSON")
    parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    args = parser.parse_args()

    decision = evaluate(load_json(args.path))
    output = asdict(decision)
    if args.compact:
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
