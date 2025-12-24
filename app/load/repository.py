from abc import ABC, abstractmethod
from typing import Optional


class LoadRepository(ABC):
    @abstractmethod
    def get_load_by_id(self, load_id: str) -> dict:
        """
        Returns load record.
        Raises if not found.
        """
        pass

    @abstractmethod
    def get_load_state(self, load_id: str) -> str:
        """
        Returns current load state.
        Raises if not found.
        """
        pass

    @abstractmethod
    def update_load_state(self, load_id: str, new_state: str) -> None:
        """
        Updates loads.state and loads.state_updated_at.
        Does NOT validate legality.
        """
        pass

    @abstractmethod
    def insert_state_transition(
        self,
        load_id: str,
        from_state: str,
        to_state: str,
        actor: str,
        is_backward: bool,
        reason: Optional[str],
    ) -> None:
        """
        Inserts immutable audit record.
        """
        pass