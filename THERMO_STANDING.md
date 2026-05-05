# Thermo-Standing

Thermo-standing is not temperature.

It is whether the accelerator fabric has enough thermal, energy, memory, timing, and capacity support to carry the workload without forcing invalid state.

## Inputs

```text
temperature
thermal slope
power draw
energy debt
memory pressure
queue pressure
interconnect pressure
partition contention
clock throttling state
cooling degradation
```

## Outcomes

```text
THERMO_VALID
THERMO_DEGRADED
THERMO_CRITICAL
THERMO_UNKNOWN
```

## Rule

```text
THERMO_CRITICAL -> HALT
THERMO_DEGRADED -> THROTTLE or ESCALATE
THERMO_UNKNOWN -> ESCALATE or HALT based on corridor
```
