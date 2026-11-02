"""Construct rank-local framework state only inside fresh spawned processes."""

from pathlib import Path
from typing import Literal, Protocol

from labqoat.training.distributed.rank_adapter import RankAdapter


class RankFactory(Protocol):
    """Bind an importable workload adapter to fixed topology and a private rendezvous."""

    adapter_id: str
    adapter_version: str

    def create(self, rank: int, world_size: int, backend: Literal["gloo", "nccl"], rendezvous: Path) -> RankAdapter:
        """Initialize collectives and model state for one rank without starting any fit updates."""
        ...
