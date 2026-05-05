# Fabric Decision Receipt

Every boundary decision emits a receipt.

## Receipt fields

```json
{
  "decision_id": "DECISION-0001",
  "workload_id": "WL-0001",
  "corridor_id": "ACCELERATOR_WORKLOAD_V0",
  "standing_geometry": "15D_PLUS_PUBLIC",
  "boundary_outcome": "EXECUTE",
  "dispatch_allowed": true,
  "reason_code": "ACCELERATOR_STANDING_ADMISSIBLE",
  "smc_state": "ARMED",
  "fabric_action": "ALLOW_DISPATCH",
  "input_hash": "sha256:...",
  "receipt_hash": "sha256:...",
  "replay_token": "sha256:...",
  "issued_at": "ISO-8601"
}
```

Receipt does not expose protected private machinery.
