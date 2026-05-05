# Replay for Accelerator Workloads

Replay reproduces the boundary decision, not the full model output.

## Replay rule

```text
same workload envelope
+ same authority state
+ same policy basis
+ same custody state
+ same fabric state
+ same SMC thresholds
+ same corridor
= same boundary decision
```

## Replay outcomes

```text
REPLAY_MATCH
REPLAY_MISMATCH
REPLAY_INCOMPLETE
REPLAY_BLOCKED
REPLAY_REQUIRES_REVIEW
```
