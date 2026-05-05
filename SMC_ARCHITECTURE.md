# Safety Monitoring Co-Processor Architecture

## Role

The Safety Monitoring Co-Processor (SMC) is the hardware-adjacent enforcement witness for accelerator-bound workloads.

It does not merely observe GPU safety.

It participates in whether accelerator-bound consequence was admissible before it ran.

## Public-safe components

```text
Fabric Standing Monitor
Deterministic Metric Engine
Halt / Throttle / Fence Plane
Hash-chain audit path
Fixed-point safety debt accumulator
Standing-decay monitor
```

## Placement

Candidate placements:

```text
on-package beside compute/tensor cores
sidecar ASIC on accelerator board
fabric-island controller per GPU pod/rack/partition
software-adjacent simulator in v0.1
```

## Interfaces

```text
memory telemetry path
scheduler path
work distributor
fabric interconnect
partition control plane
host MMIO / control registers
audit log path
```

## Claim discipline

This repository does not claim fabricated SMC hardware, CUDA integration, kernel-level enforcement, or NVIDIA certification.
