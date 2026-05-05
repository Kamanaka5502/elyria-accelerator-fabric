#!/usr/bin/env python3
from pathlib import Path

from accelerator_fabric_validator import (
    EXECUTE,
    REFUSE,
    HALT,
    THROTTLE,
    REVOKE_DISPATCH,
    evaluate,
    load_json,
)

EX = Path("examples")


def test_valid_executes():
    decision = evaluate(load_json(EX / "valid_inference_workload.json"))
    assert decision.boundary_outcome == EXECUTE
    assert decision.dispatch_allowed is True
    assert decision.fabric_action == "ALLOW_DISPATCH"
    assert decision.input_hash.startswith("sha256:")
    assert decision.receipt_hash.startswith("sha256:")
    assert decision.replay_token.startswith("sha256:")


def test_revoked_refuses():
    decision = evaluate(load_json(EX / "revoked_authority_workload.json"))
    assert decision.boundary_outcome == REFUSE
    assert decision.dispatch_allowed is False
    assert decision.reason_code == "AUTHORITY_NOT_VALID"


def test_thermal_halts():
    decision = evaluate(load_json(EX / "thermal_halt_workload.json"))
    assert decision.boundary_outcome == HALT
    assert decision.dispatch_allowed is False
    assert decision.reason_code == "THERMAL_CRITICAL"


def test_replay_missing_halts():
    decision = evaluate(load_json(EX / "replay_missing_workload.json"))
    assert decision.boundary_outcome == HALT
    assert decision.dispatch_allowed is False
    assert decision.reason_code == "REPLAY_REFERENCE_MISSING"


def test_standing_decay_revokes():
    decision = evaluate(load_json(EX / "standing_decay_workload.json"))
    assert decision.boundary_outcome == REVOKE_DISPATCH
    assert decision.dispatch_allowed is False
    assert decision.fabric_action == "REVOKE_OR_REBOUND"


def test_capacity_degraded_throttles():
    decision = evaluate(load_json(EX / "capacity_degraded_workload.json"))
    assert decision.boundary_outcome == THROTTLE
    assert decision.dispatch_allowed is False
    assert decision.fabric_action == "NARROW_OR_REVIEW"


def test_same_input_replays_same_receipt():
    a = evaluate(load_json(EX / "valid_inference_workload.json"))
    b = evaluate(load_json(EX / "valid_inference_workload.json"))
    assert a.input_hash == b.input_hash
    assert a.receipt_hash == b.receipt_hash
    assert a.replay_token == b.replay_token


def run_all_tests():
    tests = [
        test_valid_executes,
        test_revoked_refuses,
        test_thermal_halts,
        test_replay_missing_halts,
        test_standing_decay_revokes,
        test_capacity_degraded_throttles,
        test_same_input_replays_same_receipt,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print("ALL ACCELERATOR FABRIC PROOFS PASSED")


if __name__ == "__main__":
    run_all_tests()
