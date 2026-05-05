# Corridor Standing

Corridor standing resolves whether this workload may use this accelerator route.

Not merely:

```text
is GPU available?
```

But:

```text
is this tenant allowed to use this model, data class, action type, partition, runtime, and consequence path under current state?
```

## Corridor fields

```text
tenant_id
model_id
data_classification
action_class
gpu_partition
fabric_domain
policy_hash
authority_hash
replay_hash
capacity_window
thermal_window
revocation_stream
```
