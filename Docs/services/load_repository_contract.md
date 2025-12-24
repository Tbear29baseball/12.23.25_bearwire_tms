# Load Repository Contract

This document defines the ONLY permitted database access methods
for Load data and Load state transitions.

No service, UI, automation, or agent may execute raw SQL against
the Load tables outside this repository.

---

## Repository Responsibilities

The Load Repository is responsible for:
- Fetching load records
- Updating load state
- Writing transition audit records

It is NOT responsible for:
- Validating transitions
- Enforcing business rules
- Determining legality
- Actor authorization

---

## Read Operations

### get_load_by_id(load_id)

Returns:
- load.id
- load.state
- load.is_cancelled
- load.state_updated_at

Errors:
- Load not found

---

### get_load_state(load_id)

Returns:
- current lifecycle state

Errors:
- Load not found

---

## Write Operations

### update_load_state(load_id, new_state)

Behavior:
- Updates `loads.state`
- Updates `loads.state_updated_at`

Rules:
- Must NOT validate transition legality
- Must NOT write audit records

Errors:
- Load not found

---

### insert_state_transition(
    load_id,
    from_state,
    to_state,
    actor,
    is_backward,
    reason
)

Behavior:
- Inserts row into `load_state_transitions`
- Never mutates existing rows

Rules:
- Reason may be null only if is_backward = false

---

## Transaction Contract

- The repository MUST support being called inside a transaction
- The repository MUST NOT start or commit transactions itself
- Atomicity is controlled by the service layer

---

## Forbidden Behavior

- Combining state updates and audit writes into one method
- Performing transition validation
- Deleting or modifying audit records
- Exposing raw SQL to callers

---

## Enforcement Contract

- All database access for loads MUST flow through this repository
- Services may not bypass it
- Tests must mock against this contract

This document is authoritative.
