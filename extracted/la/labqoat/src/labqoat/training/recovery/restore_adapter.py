"""Explicit context-based workload hook for complete checkpoint restoration."""

from typing import Protocol

from labqoat.training.recovery.restore_snapshot import RestoreSnapshot
from labqoat.training.recovery.restore_state import RestoreState


class RestoreAdapter(Protocol):
    """Restore model, optimizer, data cursor and other declared state before returning evidence."""

    adapter_id: str
    adapter_version: str

    def restore(self, snapshot: RestoreSnapshot) -> RestoreState:
        """Load verified snapshot bytes and report actual completed restoration."""
        ...
