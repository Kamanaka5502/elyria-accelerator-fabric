# Safety Debt Model

Safety debt is accumulated burden against standing capacity.

It is not generic risk.

## Public-safe formulation

```text
Phi_accel = C_support - B_burden
```

Where:

```text
C_support = authority, capacity, thermal headroom, custody integrity, replay basis, policy support

B_burden = workload demand, risk exposure, memory pressure, energy pressure, tenant conflict, drift, standing decay
```

Rule:

```text
If Phi_accel < 0, the workload cannot continue as admitted.
```

Hardware-adjacent expression:

```text
fixed-point accumulator
saturating overflow
parallel threshold comparators
yellow / orange / red / hard halt levels
```
