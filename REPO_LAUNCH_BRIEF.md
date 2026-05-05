# Elyria Accelerator Fabric — Launch Brief

## Public position

```text
GPU availability is not execution admissibility.

Nothing reaches accelerator execution unless standing resolves first.
```

Elyria Accelerator Fabric defines a pre-dispatch admissibility boundary for accelerator-bound AI workloads.

It does not ask whether compute is available.

It asks whether the proposed workload has standing to consume accelerator execution under current authority, custody, policy, corridor, capacity, thermo-standing, standing-decay, and replay conditions.

## Why this matters

Modern AI infrastructure can schedule, route, and execute workloads before consequence standing is resolved.

That creates a gap:

```text
a workload may be technically executable
and still be inadmissible
```

This repository demonstrates a public proof corridor for closing that gap before dispatch.

## Proof corridor

```text
valid workload        -> EXECUTE / ALLOW_DISPATCH
revoked authority     -> REFUSE / BLOCK_DISPATCH
thermal critical      -> HALT / STOP_EXECUTION
capacity degraded     -> THROTTLE / NARROW_OR_REVIEW
replay missing        -> HALT / BLOCK_CERTIFICATION
standing decay active -> REVOKE_DISPATCH / REVOKE_OR_REBOUND
```

## Determinism requirement

For identical input and identical boundary state, the validator must reproduce:

```text
same input hash
same receipt hash
same replay token
same dispatch decision
```

## What the visual represents

The hero image represents the repo as a governed accelerator fabric:

```text
workload envelope
  -> 15D+ standing / SMC witness gate
  -> accelerator fabric mesh
  -> dispatch, halt, throttle, fence, revoke
```

The right-side mesh represents accelerator fabric nodes, tenant/partition paths, fabric-switch routing, and sideband SMC control.

## Claim discipline

This repository does not claim:

```text
NVIDIA partnership
NVIDIA certification
CUDA-level integration
kernel-level enforcement
fabricated SMC hardware
production deployment
```

It is a protected public proof surface for controlled review and pilot corridor discussion.

## Reviewer read

A reviewer should be able to verify three things quickly:

```text
1. only EXECUTE dispatches
2. every decision emits receipt/replay material
3. accelerator availability never bypasses standing resolution
```

That is the repository's load-bearing claim.