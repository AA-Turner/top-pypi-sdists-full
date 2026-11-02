"""An adapter-owned rank snapshot before coordinated publication."""

from dataclasses import dataclass
from pathlib import Path

from labqoat.compute.checkpoint_progress import CheckpointProgress
from labqoat.compute.checkpoint_rank import CheckpointRank
from labqoat.compute.checkpoint_recovery_types import CheckpointState
from labqoat.storage.verified_file import VerifiedFile


@dataclass(frozen=True, kw_only=True)
class RankSnapshot:
    """Retain each rank's independently serialized state and actual restored update boundary."""

    rank: int
    payload: Path
    progress: CheckpointProgress
    state: tuple[CheckpointState, ...]

    def inventory(self) -> CheckpointRank:
        """Capture exact bytes before constructing the complete group manifest."""
        return CheckpointRank(
            rank=self.rank,
            sha256=f"sha256:{VerifiedFile.digest(self.payload)}",
            byte_size=self.payload.stat().st_size,
            progress=self.progress,
            state=self.state,
        )
