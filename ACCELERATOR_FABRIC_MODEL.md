# Accelerator Fabric Model

## Core distinction

```text
Accelerator infrastructure asks: can the workload run?
Elyria Accelerator Fabric asks: may this workload bind accelerator-bound consequence before it runs?
```

A workload can be schedulable and still inadmissible.

## Layer model

```text
0 Workload Request
1 Governed Workload Envelope
2 Fabric Canonicalization
3 15D+ Standing Geometry Resolver
4 SMC / Accelerator Safety Fabric
5 Dispatch Decision
6 GPU / Fabric Execution
7 Receipt + Replay + Audit Chain
8 Standing Decay Monitor
9 Revoke / Halt / Quarantine / Rebound
```

## Dispatch law

```text
dispatch_allowed = true ONLY IF
  boundary_outcome = EXECUTE
  AND receipt_basis exists
  AND replay_basis exists
  AND standing_decay is not active
```

If standing cannot be proven, dispatch does not occur.
