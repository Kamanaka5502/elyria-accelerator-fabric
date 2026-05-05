# Governed Workload Envelope

The envelope is not a log.

It is the decision substrate used by the boundary.

## Minimum public-safe fields

```json
{
  "workload_id": "WL-0001",
  "tenant_id": "tenant_hash",
  "actor_id": "actor_hash",
  "model_id": "model_ref",
  "model_risk_class": "standard | restricted | high",
  "requested_action": "inference | training | fine_tune | embedding | batch_run",
  "data_classification": "public | internal | confidential | restricted",
  "authority_state": "VALID | EXPIRED | REVOKED | OUT_OF_SCOPE",
  "custody_state": "INTACT | DEGRADED | BROKEN",
  "policy_state": "CURRENT | STALE | MISMATCH",
  "revocation_status": "CLEAR | REVOKED",
  "corridor_id": "ACCELERATOR_WORKLOAD_V0",
  "gpu_partition": "MIG_or_partition_ref",
  "fabric_domain": "pod_or_island_ref",
  "capacity_state": "SUPPORTED | DEGRADED | OVERBURDENED | UNKNOWN",
  "thermal_state": "NORMAL | DEGRADED | CRITICAL",
  "energy_debt_state": "WITHIN_BUDGET | NEAR_LIMIT | EXCEEDED",
  "scheduler_integrity": "VALID | DEGRADED | UNKNOWN",
  "standing_decay_state": "CLEAR | ACTIVE",
  "replay_reference": "replay_ref_hash",
  "receipt_parent": "prior_receipt_hash",
  "issued_at": "ISO-8601"
}
```
