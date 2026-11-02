"""Complete coordinated checkpoint inventories for fixed-topology distributed training."""

from dataclasses import dataclass
from typing import Literal

from labqoat.compute.checkpoint_progress import CheckpointProgress
from labqoat.compute.checkpoint_rank import CheckpointRank
from labqoat.compute.checkpoint_recovery_types import CheckpointState
from labqoat.json_document import JsonDocument


@dataclass(frozen=True, kw_only=True)
class CheckpointGroup:
    """Require every rank at one progress boundary in the same immutable aggregate payload."""

    backend: Literal["gloo", "nccl"]
    ranks: tuple[CheckpointRank, ...]

    def document(self) -> JsonDocument:
        """Record bounded rank diagnostics beneath the logical checkpoint."""
        return JsonDocument(
            topology="single-host", backend=self.backend, ranks=[rank.document() for rank in self.ranks]
        )

    def validate(self, world_size: int, progress: CheckpointProgress, state: tuple[CheckpointState, ...]) -> None:
        """Reject partial groups, duplicate ranks, topology changes and divergent update boundaries."""
        if not 2 <= world_size <= 256 or tuple(rank.rank for rank in self.ranks) != tuple(range(world_size)):
            raise ValueError("Coordinated checkpoint requires every rank in canonical order")
        for rank in self.ranks:
            if rank.progress != progress or not set(state).issubset(rank.state):
                raise ValueError("Checkpoint ranks must share complete state and the same progress boundary")
