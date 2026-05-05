#!/usr/bin/env python3
"""
Elyria Accelerator Fabric — Admission Proof Demo

This file demonstrates pre-execution admission for accelerator-bound workloads.

Execution is not assumed.
It is admitted only when authority, state, capacity, and replay conditions hold.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Dict, List, Tuple


class Decision(str, Enum):
    EXECUTE = "EXECUTE"
    REDIRECT = "REDIRECT"
    ESCALATE = "ESCALATE"
    REFUSE = "REFUSE"
    HALT = "HALT"


@dataclass(frozen=True)
class WorkloadRequest:
    request_id: str
    actor: str
    authority_scope: str
    corridor: str
    workload_type: str
    accelerator_target: str
    estimated_compute_units: int
    estimated_latency_ms: int
    risk_score: float
    state_hash: str
    policy_hash: str
    replay_nonce: str


@dataclass(frozen=True)
class AdmissionLaw:
    law_bundle_id: str
    allowed_authority_scopes: Tuple[str, ...]
    allowed_corridors: Tuple[str, ...]
    allowed_targets: Tuple[str, ...]
    max_compute_units: int
    max_latency_ms: int
    max_risk_score: float
    require_state_hash: bool = True
    require_policy_hash: bool = True
    require_replay_nonce: bool = True


@dataclass(frozen=True)
class GateResult:
    gate: str
    passed: bool
    reason: str


@dataclass(frozen=True)
class AdmissionReceipt:
    request_id: str
    decision: Decision
    law_bundle_id: str
    gate_results: Tuple[GateResult, ...]
    request_hash: str
    decision_hash: str
    receipt_hash: str


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_hex(value: Any) -> str:
    encoded = canonical_json(value).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evaluate_gates(request: WorkloadRequest, law: AdmissionLaw) -> Tuple[GateResult, ...]:
    gates: List[GateResult] = []

    gates.append(
        GateResult(
            gate="authority",
            passed=request.authority_scope in law.allowed_authority_scopes,
            reason="authority scope admitted"
            if request.authority_scope in law.allowed_authority_scopes
            else "authority scope not admitted",
        )
    )

    gates.append(
        GateResult(
            gate="corridor",
            passed=request.corridor in law.allowed_corridors,
            reason="corridor admitted"
            if request.corridor in law.allowed_corridors
            else "corridor not admitted",
        )
    )

    gates.append(
        GateResult(
            gate="target",
            passed=request.accelerator_target in law.allowed_targets,
            reason="accelerator target admitted"
            if request.accelerator_target in law.allowed_targets
            else "accelerator target not admitted",
        )
    )

    gates.append(
        GateResult(
            gate="capacity",
            passed=request.estimated_compute_units <= law.max_compute_units,
            reason="compute burden within limit"
            if request.estimated_compute_units <= law.max_compute_units
            else "compute burden exceeds limit",
        )
    )

    gates.append(
        GateResult(
            gate="latency",
            passed=request.estimated_latency_ms <= law.max_latency_ms,
            reason="latency within admission ceiling"
            if request.estimated_latency_ms <= law.max_latency_ms
            else "latency ceiling exceeded",
        )
    )

    gates.append(
        GateResult(
            gate="risk",
            passed=request.risk_score <= law.max_risk_score,
            reason="risk within governed threshold"
            if request.risk_score <= law.max_risk_score
            else "risk exceeds governed threshold",
        )
    )

    gates.append(
        GateResult(
            gate="state_hash",
            passed=(not law.require_state_hash) or bool(request.state_hash),
            reason="state hash present"
            if request.state_hash
            else "missing state hash",
        )
    )

    gates.append(
        GateResult(
            gate="policy_hash",
            passed=(not law.require_policy_hash) or bool(request.policy_hash),
            reason="policy hash present"
            if request.policy_hash
            else "missing policy hash",
        )
    )

    gates.append(
        GateResult(
            gate="replay_nonce",
            passed=(not law.require_replay_nonce) or bool(request.replay_nonce),
            reason="replay nonce present"
            if request.replay_nonce
            else "missing replay nonce",
        )
    )

    return tuple(gates)


def resolve_decision(gates: Tuple[GateResult, ...]) -> Decision:
    failed = [gate for gate in gates if not gate.passed]

    if not failed:
        return Decision.EXECUTE

    failed_names = {gate.gate for gate in failed}

    if "state_hash" in failed_names or "policy_hash" in failed_names:
        return Decision.HALT

    if "authority" in failed_names or "target" in failed_names:
        return Decision.REFUSE

    if "latency" in failed_names:
        return Decision.ESCALATE

    if "capacity" in failed_names or "risk" in failed_names or "corridor" in failed_names:
        return Decision.REDIRECT

    return Decision.REFUSE


def admit(request: WorkloadRequest, law: AdmissionLaw) -> AdmissionReceipt:
    gates = evaluate_gates(request, law)
    decision = resolve_decision(gates)

    request_hash = sha256_hex(asdict(request))
    decision_material: Dict[str, Any] = {
        "request_hash": request_hash,
        "law_bundle_id": law.law_bundle_id,
        "decision": decision.value,
        "gate_results": [asdict(gate) for gate in gates],
    }
    decision_hash = sha256_hex(decision_material)

    receipt_material: Dict[str, Any] = {
        "request_id": request.request_id,
        "law_bundle_id": law.law_bundle_id,
        "request_hash": request_hash,
        "decision_hash": decision_hash,
    }
    receipt_hash = sha256_hex(receipt_material)

    return AdmissionReceipt(
        request_id=request.request_id,
        decision=decision,
        law_bundle_id=law.law_bundle_id,
        gate_results=gates,
        request_hash=request_hash,
        decision_hash=decision_hash,
        receipt_hash=receipt_hash,
    )


def replay_verify(request: WorkloadRequest, law: AdmissionLaw, receipt: AdmissionReceipt) -> bool:
    replayed = admit(request, law)
    return replayed == receipt


def print_receipt(receipt: AdmissionReceipt, replay_passed: bool) -> None:
    print(f"REQUEST_ID: {receipt.request_id}")
    print(f"DECISION: {receipt.decision.value}")
    print(f"LAW_BUNDLE_ID: {receipt.law_bundle_id}")
    print(f"REQUEST_HASH: {receipt.request_hash}")
    print(f"DECISION_HASH: {receipt.decision_hash}")
    print(f"RECEIPT_HASH: {receipt.receipt_hash}")
    print(f"REPLAY_CHECK: {'PASS' if replay_passed else 'FAIL'}")
    print("GATE_TRACE:")
    for gate in receipt.gate_results:
        status = "PASS" if gate.passed else "FAIL"
        print(f"  - {gate.gate}: {status} — {gate.reason}")


def main() -> None:
    law = AdmissionLaw(
        law_bundle_id="ELYRIA_ACCELERATOR_FABRIC_LAW_v0.1",
        allowed_authority_scopes=("accelerator.submit", "accelerator.operator"),
        allowed_corridors=("bounded_inference", "governed_batch"),
        allowed_targets=("local_gpu", "managed_accelerator_pool"),
        max_compute_units=1000,
        max_latency_ms=200,
        max_risk_score=0.40,
    )

    scenarios = [
        WorkloadRequest(
            request_id="valid-execute-001",
            actor="sam-candidate",
            authority_scope="accelerator.submit",
            corridor="bounded_inference",
            workload_type="inference",
            accelerator_target="local_gpu",
            estimated_compute_units=420,
            estimated_latency_ms=84,
            risk_score=0.18,
            state_hash="state_9a7e",
            policy_hash="policy_2b11",
            replay_nonce="nonce_valid_001",
        ),
        WorkloadRequest(
            request_id="bad-authority-001",
            actor="unknown-actor",
            authority_scope="unscoped.execute",
            corridor="bounded_inference",
            workload_type="inference",
            accelerator_target="local_gpu",
            estimated_compute_units=420,
            estimated_latency_ms=84,
            risk_score=0.18,
            state_hash="state_9a7e",
            policy_hash="policy_2b11",
            replay_nonce="nonce_refuse_001",
        ),
        WorkloadRequest(
            request_id="latency-escalate-001",
            actor="sam-candidate",
            authority_scope="accelerator.submit",
            corridor="bounded_inference",
            workload_type="inference",
            accelerator_target="local_gpu",
            estimated_compute_units=420,
            estimated_latency_ms=250,
            risk_score=0.18,
            state_hash="state_9a7e",
            policy_hash="policy_2b11",
            replay_nonce="nonce_escalate_001",
        ),
        WorkloadRequest(
            request_id="capacity-redirect-001",
            actor="sam-candidate",
            authority_scope="accelerator.submit",
            corridor="bounded_inference",
            workload_type="batch",
            accelerator_target="managed_accelerator_pool",
            estimated_compute_units=1300,
            estimated_latency_ms=144,
            risk_score=0.22,
            state_hash="state_9a7e",
            policy_hash="policy_2b11",
            replay_nonce="nonce_redirect_001",
        ),
        WorkloadRequest(
            request_id="missing-policy-halt-001",
            actor="sam-candidate",
            authority_scope="accelerator.submit",
            corridor="bounded_inference",
            workload_type="inference",
            accelerator_target="local_gpu",
            estimated_compute_units=420,
            estimated_latency_ms=84,
            risk_score=0.18,
            state_hash="state_9a7e",
            policy_hash="",
            replay_nonce="nonce_halt_001",
        ),
    ]

    for index, request in enumerate(scenarios, start=1):
        print("=" * 72)
        print(f"SCENARIO {index}: {request.request_id}")
        receipt = admit(request, law)
        replay_passed = replay_verify(request, law, receipt)
        print_receipt(receipt, replay_passed)


if __name__ == "__main__":
    main()
