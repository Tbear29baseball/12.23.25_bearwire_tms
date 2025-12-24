# Load Transition Guard Rules

This document defines which load state transitions are LEGAL.
The database enforces validity and audit.
This file enforces policy.

No transition may occur unless it is defined here.

---

## Forward Transitions

### NEW → ACCEPTED
Who:
- Dispatcher

Must be true:
- Core load fields completed
- RateCon attached
- Dispatcher has reviewed OCR or manual entry

---

### ACCEPTED → DISPATCHED
Who:
- Dispatcher

Must be true:
- Carrier has acknowledged the load
- Driver is confirmed

---

### DISPATCHED → IN_TRANSIT
Who:
- Dispatcher

Must be true:
- Pickup confirmed OR dispatcher manually advances

---

### IN_TRANSIT → DOCS_PENDING
Who:
- Dispatcher

Must be true:
- Delivery confirmed

---

### DOCS_PENDING → COMPLETE_UNVERIFIED
Who:
- Dispatcher

Must be true:
- All required documents uploaded

---

### COMPLETE_UNVERIFIED → READY_TO_BILL
Who:
- Dispatcher

Must be true:
- Documents reviewed
- No rejected or missing paperwork

---

### READY_TO_BILL → BILLED
Who:
- Dispatcher or Accounting (future)

Must be true:
- Invoice sent OR factoring submitted

---

## Backward Transitions (Corrective Only)

Backward transitions are allowed to correct reality.
They must never hide mistakes.

Rules:
- Dispatcher only
- Reason required
- Transition is logged immutably

Allowed backward paths:

- ACCEPTED → NEW
- DISPATCHED → ACCEPTED
- IN_TRANSIT → DISPATCHED
- DOCS_PENDING → IN_TRANSIT
- COMPLETE_UNVERIFIED → DOCS_PENDING
- READY_TO_BILL → COMPLETE_UNVERIFIED

No other backward transitions are allowed.

---

## Forbidden Transitions

The following are always illegal:

- BILLED → any state
- NEW → DISPATCHED
- NEW → IN_TRANSIT
- ACCEPTED → DOCS_PENDING
- ACCEPTED → READY_TO_BILL
- DISPATCHED → READY_TO_BILL

If it is not explicitly allowed above, it is forbidden.

---

## Enforcement Contract

- Application services MUST validate transitions against this document
- Database audit tables MUST record all attempts
- UI may not bypass these rules

This document is authoritative.
