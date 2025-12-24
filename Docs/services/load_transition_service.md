# Load Transition Service Contract

This document defines the ONLY legal way a load may change state.
All UI, API, automation, and future agents MUST use this contract.

Direct database updates to `loads.state` are forbidden.

---

## Service Entry Point

request_load_transition(
    load_id,
    to_state,
    actor,
    reason = null
)

---

## Required Inputs

### load_id
- Must exist
- Must not be cancelled

### to_state
- Must be a valid lifecycle state
- Must be different from current state

### actor
- Dispatcher (required for all transitions)
- Accounting (allowed only for READY_TO_BILL → BILLED)

### reason
- Required ONLY for backward transitions
- Stored immutably in audit log

---

## Validation Order (Strict)

1. Load exists
2. Load is not cancelled
3. Load is not in terminal state (`BILLED`)
4. Transition is allowed by:
   - Docs/db/load_transition_rules.md
5. Actor is permitted for this transition
6. If backward:
   - reason MUST be present

Failure at any step aborts the transition.

---

## Guaranteed Side Effects (Atomic)

On success, the service MUST:

1. Update:
   - loads.state
   - loads.state_updated_at
2. Insert a row into:
   - load_state_transitions
     - from_state
     - to_state
     - actor
     - is_backward
     - reason

All actions MUST occur in a single transaction.

---

## Forbidden Behavior

- Skipping guard validation
- Modifying historical transition rows
- Deleting transition history
- Updating loads.state without logging
- Allowing any transition out of BILLED

---

## Failure Modes (Explicit)

- Load not found
- Load cancelled
- Illegal transition
- Unauthorized actor
- Missing backward reason
- Terminal state violation

Failures produce NO side effects.

---

## Enforcement Contract

- All future code MUST call this service
- No UI or automation may bypass it
- Tests must validate against this contract

This document is authoritative.
