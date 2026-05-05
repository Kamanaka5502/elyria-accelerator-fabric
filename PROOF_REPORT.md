# Elyria Accelerator Fabric Proof Report

## Proof objective

This public proof corridor demonstrates that accelerator dispatch is not granted by GPU availability alone.

```text
GPU availability is not execution admissibility.
```

Only a workload that resolves `EXECUTE` at the accelerator boundary may dispatch.

## Public proof corridor

| Case | Input condition | Expected boundary outcome | Expected fabric action | Dispatch allowed |
|---|---|---:|---:|---:|
| Valid inference | Standing holds | `EXECUTE` | `ALLOW_DISPATCH` | `true` |
| Revoked authority | Authority revoked | `REFUSE` | `BLOCK_DISPATCH` | `false` |
| Thermal halt | Thermal state critical | `HALT` | `STOP_EXECUTION` | `false` |
| Capacity degraded | Capacity degraded | `THROTTLE` | `NARROW_OR_REVIEW` | `false` |
| Replay missing | No replay basis | `HALT` | `BLOCK_CERTIFICATION` | `false` |
| Standing decay | Standing decay active | `REVOKE_DISPATCH` | `REVOKE_OR_REBOUND` | `false` |

## Determinism claim

For identical input:

```text
same workload envelope
+ same authority state
+ same policy state
+ same custody state
+ same fabric state
+ same corridor
= same input hash, receipt hash, and replay token
```

## Run locally

```bash
python accelerator_fabric_validator.py examples/valid_inference_workload.json
python accelerator_fabric_validator.py examples/revoked_authority_workload.json
python accelerator_fabric_validator.py examples/thermal_halt_workload.json
python accelerator_fabric_validator.py examples/replay_missing_workload.json
python accelerator_fabric_validator.py examples/standing_decay_workload.json
python accelerator_fabric_validator.py examples/capacity_degraded_workload.json
python test_accelerator_fabric_validator.py
```

## Expected final test line

```text
ALL ACCELERATOR FABRIC PROOFS PASSED
```

## Protected boundary

This proof report does not expose private runtime law, protected SMC implementation, production thresholds, customer corridors, private schemas, production adapters, or deployment-sensitive architecture.
