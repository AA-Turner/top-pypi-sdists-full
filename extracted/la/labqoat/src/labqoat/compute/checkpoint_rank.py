"""One content-addressed rank payload at a coordinated continuation boundary."""

from dataclasses import dataclass

from labqoat.compute.checkpoint_progress import CheckpointProgress
from labqoat.compute.checkpoint_recovery_types import CheckpointState
from labqoat.json_document import JsonDocument


@dataclass(frozen=True, kw_only=True)
class CheckpointRank:
    """Bind one rank's bytes, actual serialized state and next-update cursor."""

    rank: int
    sha256: str
    byte_size: int
    progress: CheckpointProgress
    state: tuple[CheckpointState, ...]

    @property
    def path(self) -> str:
        """Use a canonical archive entry independent of user-controlled filesystem paths."""
        return f"ranks/{self.rank}.bin"

    def document(self) -> JsonDocument:
        """Return the inventory entry validated by the complete recovery manifest."""
        return JsonDocument(
            rank=self.rank,
            path=self.path,
            sha256=self.sha256,
            byte_size=self.byte_size,
            progress=self.progress.document(),
            state=list(self.state),
        )
