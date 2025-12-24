# BearWire Load Lifecycle 
## states
STATE: New (Unreviewed)
Can dispatch?        no
Can notify anyone?  no
Can edit fields?    yes
Can OCR run?        yes
Can billing happen? no

> Human meaning:
> The load exists, but nothing is trusted yet.
> OCR and manual entry are allowed, but no commitments, notifications,
> or dispatch actions may occur in this state.

STATE: Accepted
Can dispatch?        yes
Can notify anyone?  yes
Can edit fields?    yes (restricted)
Can OCR run?        no
Can billing happen? no

> Human meaning:
> The dispatcher has reviewed the load and trusts the core details.
> The load is now real and can be dispatched and communicated externally.

STATE: Dispatched
Can dispatch?        no
Can notify anyone?  yes
Can edit fields?    yes (highly restricted)
Can OCR run?        no
Can billing happen? no

> Human meaning:
> The load has been committed to a carrier and driver.
> Changes now affect real people and must be tightly controlled.

STATE: In Transit
Can dispatch?        no
Can notify anyone?  yes
Can edit fields?    yes (status-only)
Can OCR run?        no
Can billing happen? no

> Human meaning:
> The truck has the load (or is actively moving).
> This state is for tracking and communication, not editing fundamentals.

STATE: Docs Pending
Can dispatch?        no
Can notify anyone?  yes
Can edit fields?    yes (docs + notes only)
Can OCR run?        yes (docs only)
Can billing happen? no

> Human meaning:
> The load has been delivered, but required paperwork is missing.
> Billing and factoring are blocked until POD/BOL are received.

STATE: Complete (Unverified)
Can dispatch?        no
Can notify anyone?  yes
Can edit fields?    yes (docs review + notes only)
Can OCR run?        yes (verification only)
Can billing happen? no

> Human meaning:
> All required documents are present, but have not been reviewed.
> This is the quality-check buffer before money is allowed to move.

STATE: Ready to Bill
Can dispatch?        no
Can notify anyone?  yes
Can edit fields?    no (read-only except internal notes)
Can OCR run?        no
Can billing happen? yes

> Human meaning:
> Documents have been reviewed and verified.
> The load is clean, approved, and safe to invoice or submit for factoring.

STATE: Billed
Can dispatch?        no
Can notify anyone?  yes
Can edit fields?    no
Can OCR run?        no
Can billing happen? no

> Human meaning:
> The invoice has been sent or factoring submitted.
> The load is financially committed and permanently read-only.

## states transitions
Transition rules (this is the real wiring)
1️⃣ New (Unreviewed) → Accepted

Who: Dispatcher
Must be true:

Core load fields are filled

RateCon is attached

Dispatcher has reviewed OCR or manual entry

In human terms:

“I’ve looked at this and trust it.”

This is human authority, not automation.

2️⃣ Accepted → Dispatched

Who: Dispatcher
Must be true:

Carrier has acknowledged the load
(ratecon accepted / driver confirmed)

In human terms:

“Someone outside our system has committed.”

This prevents fake or premature dispatch.

3️⃣ Dispatched → In Transit

Who: Dispatcher (or driver action that dispatcher trusts)
Must be true:

Pickup confirmed OR dispatcher manually advances

In human terms:

“The truck has the freight (or is rolling).”

You allow flexibility here on purpose.

4️⃣ In Transit → Docs Pending

Who: Dispatcher
Must be true:

Delivery occurred

In human terms:

“The load is done moving.”

Docs may still be missing — that’s the point.

5️⃣ Docs Pending → Complete (Unverified)

Who: Dispatcher
Must be true:

All required documents are uploaded

In human terms:

“We have paperwork — now we need to check it.”

No quality judgment yet. Just presence.

6️⃣ Complete (Unverified) → Ready to Bill

Who: Dispatcher
Must be true:

Human has reviewed docs

Nothing missing or rejected

In human terms:

“This won’t blow up accounting.”

This is the money safety gate.

7️⃣ Ready to Bill → Billed

Who: Dispatcher (or accounting role later)
Must be true:

Invoice sent OR factoring submitted

In human terms:

“Money process has started.”

After this, the load is frozen forever.

About moving loads backward

Backward moves are allowed, but never silent.

Rule (simple, don’t code yet):

Any backward transition requires:

Dispatcher action

Reason / note

Examples:

Complete (Unverified) → Docs Pending (bad POD)

Ready to Bill → Complete (Unverified) (doc issue caught)

Accepted → New (entered wrong load)

This protects you during audits and “what happened?” moments.

## Backward Transitions

Backward state transitions are allowed but restricted.

Rules:
- Only dispatchers (or admins) may move a load backward
- A reason/note is required for every backward move
- Backward moves do not erase history

Examples:
- Complete (Unverified) → Docs Pending (bad POD)
- Ready to Bill → Complete (Unverified) (doc issue found)
- Accepted → New (entered incorrectly)

Backward transitions exist to correct reality, not to hide mistakes.