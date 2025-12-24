CREATE TABLE loads (
    id UUID PRIMARY KEY,

    -- lifecycle
    state TEXT NOT NULL,
    state_updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- cancellation (terminal, not a state)
    is_cancelled BOOLEAN NOT NULL DEFAULT FALSE,
    cancelled_at TIMESTAMPTZ,
    cancellation_reason TEXT,

    -- audit
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- future financial anchor (no logic yet)
    billable_at TIMESTAMPTZ,

    CONSTRAINT loads_state_valid
        CHECK (state IN (
            'NEW',
            'ACCEPTED',
            'DISPATCHED',
            'IN_TRANSIT',
            'DOCS_PENDING',
            'COMPLETE_UNVERIFIED',
            'READY_TO_BILL',
            'BILLED'
        )),

    CONSTRAINT loads_cancel_terminal
        CHECK (
            (is_cancelled = FALSE)
            OR
            (is_cancelled = TRUE AND cancelled_at IS NOT NULL)
        )
);

CREATE TABLE load_state_transitions (
    id UUID PRIMARY KEY,
    load_id UUID NOT NULL REFERENCES loads(id) ON DELETE RESTRICT

    from_state TEXT NOT NULL,
    to_state TEXT NOT NULL,

    moved_by TEXT NOT NULL, -- dispatcher identifier
    moved_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    is_backward BOOLEAN NOT NULL,
    reason TEXT,

    CONSTRAINT transition_states_valid
        CHECK (
            from_state IN (
                'NEW','ACCEPTED','DISPATCHED','IN_TRANSIT',
                'DOCS_PENDING','COMPLETE_UNVERIFIED',
                'READY_TO_BILL','BILLED'
            )
            AND
            to_state IN (
                'NEW','ACCEPTED','DISPATCHED','IN_TRANSIT',
                'DOCS_PENDING','COMPLETE_UNVERIFIED',
                'READY_TO_BILL','BILLED'
            )
        ),

    CONSTRAINT backward_requires_reason
        CHECK (
            is_backward = FALSE
            OR
            (is_backward = TRUE AND reason IS NOT NULL)
        )
);
