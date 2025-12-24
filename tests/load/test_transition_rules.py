from app.load.service import LoadTransitionService
from app.load.models import LoadState
from app.load.exceptions import (
    IllegalTransitionError,
    TerminalStateError,
    LoadCancelledError,
    MissingReasonError,
)
from app.load.repository import LoadRepository


class FakeLoadRepository(LoadRepository):
    def __init__(self, load):
        self.load = load
        self.updated_state = None
        self.transition_logged = False

    def get_load_by_id(self, load_id: str):
        return self.load

    def get_load_state(self, load_id: str):
        return self.load["state"]

    def update_load_state(self, load_id: str, new_state: str):
        self.updated_state = new_state

    def insert_state_transition(
        self,
        load_id: str,
        from_state: str,
        to_state: str,
        actor: str,
        is_backward: bool,
        reason: str | None,
    ):
        self.transition_logged = True


def test_valid_forward_transition():
    repo = FakeLoadRepository(
        {"state": "NEW", "is_cancelled": False}
    )
    service = LoadTransitionService(repo)

    service.request_load_transition(
        load_id="1",
        to_state=LoadState.ACCEPTED,
        actor="dispatcher",
    )

    assert repo.updated_state == "ACCEPTED"
    assert repo.transition_logged is True


def test_backward_transition_requires_reason():
    repo = FakeLoadRepository(
        {"state": "ACCEPTED", "is_cancelled": False}
    )
    service = LoadTransitionService(repo)

    try:
        service.request_load_transition(
            load_id="1",
            to_state=LoadState.NEW,
            actor="dispatcher",
        )
        assert False, "Expected MissingReasonError"
    except MissingReasonError:
        pass


def test_illegal_transition_fails():
    repo = FakeLoadRepository(
        {"state": "NEW", "is_cancelled": False}
    )
    service = LoadTransitionService(repo)

    try:
        service.request_load_transition(
            load_id="1",
            to_state=LoadState.IN_TRANSIT,
            actor="dispatcher",
        )
        assert False, "Expected IllegalTransitionError"
    except IllegalTransitionError:
        pass


def test_terminal_state_fails():
    repo = FakeLoadRepository(
        {"state": "BILLED", "is_cancelled": False}
    )
    service = LoadTransitionService(repo)

    try:
        service.request_load_transition(
            load_id="1",
            to_state=LoadState.READY_TO_BILL,
            actor="dispatcher",
        )
        assert False, "Expected TerminalStateError"
    except TerminalStateError:
        pass


def test_cancelled_load_fails():
    repo = FakeLoadRepository(
        {"state": "ACCEPTED", "is_cancelled": True}
    )
    service = LoadTransitionService(repo)

    try:
        service.request_load_transition(
            load_id="1",
            to_state=LoadState.DISPATCHED,
            actor="dispatcher",
        )
        assert False, "Expected LoadCancelledError"
    except LoadCancelledError:
        pass
