"""Workload-owned Lightning checkpoint relocation and post-restoration verification."""

from pathlib import Path
from typing import Protocol

from labqoat.training.recovery.restore_adapter import RestoreAdapter
from labqoat.training.recovery.restore_snapshot import RestoreSnapshot


class LightningRestoreAdapter(RestoreAdapter, Protocol):
    """Bind an existing model, Trainer and data cursor to an explicit certified workload adapter."""

    def prepare(self, snapshot: RestoreSnapshot) -> Path:
        """Validate archive contents and return the exact local Lightning checkpoint for Trainer.fit.

        The inherited restore hook runs after Lightning restores optimizer and loop state. It must
        verify that actual state, restore remaining RNG/data/callback state in its certified order,
        and report actual progress and inventory. Merely returning manifest claims is insufficient.
        """
        ...
