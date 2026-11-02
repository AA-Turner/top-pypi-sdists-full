"""Own the verified file leases of one ready-to-consume dataset batch."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path

from labqoat.dataset_access.dataset_provider import DatasetProvider, DatasetReference


@dataclass(frozen=True, slots=True)
class PrefetchedBatch:
    """Transfer a batch's lease ownership from the acquisition thread to its consumer."""

    files: Mapping[str, Path]
    leases: ExitStack

    @classmethod
    def acquire(cls, provider: DatasetProvider, reference: DatasetReference, paths: Sequence[str]) -> PrefetchedBatch:
        """Acquire only this sampler-selected batch, releasing partial failures."""
        with ExitStack() as leases:
            files = leases.enter_context(provider.local_files(reference, paths))
            return cls(files, leases.pop_all())

    def close(self) -> None:
        """Release every file as soon as its batch is consumed or abandoned."""
        self.leases.close()
