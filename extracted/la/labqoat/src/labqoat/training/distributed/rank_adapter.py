"""Explicit distributed adapter boundary implemented by the retained workload."""

from typing import Protocol

from labqoat.json_document import JsonDocument
from labqoat.training.recovery.restore_adapter import RestoreAdapter


class RankAdapter(RestoreAdapter, Protocol):
    """Restore one rank completely before the coordinator permits its fit region."""

    def fit(self) -> JsonDocument:
        """Train only after all ranks restore and one root-owned fit supervisor is armed."""
        ...
