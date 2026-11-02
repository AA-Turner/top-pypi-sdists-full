"""Explicit adapter recovery declarations, separate from arbitrary user checkpoint metadata."""

from dataclasses import dataclass

from labqoat.compute.checkpoint_compatibility import CheckpointCompatibility
from labqoat.compute.checkpoint_group import CheckpointGroup
from labqoat.compute.checkpoint_progress import CheckpointProgress
from labqoat.compute.checkpoint_recovery_types import (
    CheckpointBoundary,
    CheckpointGuarantee,
    CheckpointRole,
    CheckpointState,
)
from labqoat.json_document import JsonDocument
from labqoat.manifests import Manifest


@dataclass(frozen=True, kw_only=True)
class CheckpointRecovery:
    """Advertise only the state and continuation boundary actually serialized by an adapter."""

    role: CheckpointRole
    adapter_id: str
    adapter_version: str
    compatibility: CheckpointCompatibility
    state: tuple[CheckpointState, ...]
    boundary: CheckpointBoundary
    guarantee: CheckpointGuarantee
    progress: CheckpointProgress
    group: CheckpointGroup | None = None

    def document(self, step: int) -> JsonDocument:
        """Validate portable shape and complete continuation state before any upload begins."""
        self._validate(step)
        document = JsonDocument(
            {
                "protocol_version": 1,
                "role": self.role,
                "adapter": {"id": self.adapter_id, "version": self.adapter_version},
                "compatibility": self.compatibility.document(),
                "state": list(self.state),
                "boundary": self.boundary,
                "guarantee": self.guarantee,
                "progress": self.progress.document(),
            }
        )
        if self.group is not None:
            document["group"] = self.group.document()
        return Manifest.capture("checkpoint_recovery", document).document

    def _validate(self, step: int) -> None:
        """Reject inconsistent cursors, incomplete continuation and misleading final-state roles."""
        if step != self.progress.update:
            raise ValueError("Checkpoint step must match the restored update cursor")
        if self.role in ("resumable-last", "final-training-state"):
            required = {"model", "optimizer", "rng_python", "data_cursor", "callbacks", "fit_clock"}
            if self.role == "final-training-state":
                required.add("completed_training")
            if not required.issubset(self.state):
                raise ValueError("Checkpoint does not contain complete continuation state")
        self._validate_boundary()
        self._validate_group()

    def _validate_group(self) -> None:
        """Weights from incomplete distributed groups never become resume candidates."""
        if self.group is None:
            if self.compatibility.world_size != 1 and self.role in ("resumable-last", "final-training-state"):
                raise ValueError("Distributed checkpoints require a coordinated rank inventory")
        else:
            self.group.validate(self.compatibility.world_size, self.progress, self.state)

    def _validate_boundary(self) -> None:
        """Constrain finalization-only and epoch-only checkpoints to their declared boundary."""
        if self.role == "final-training-state":
            valid = self.boundary == "training-complete"
        elif self.guarantee == "epoch-boundary":
            valid = self.boundary == "epoch"
        else:
            valid = self.boundary in ("optimizer-update", "epoch")
        if not valid:
            raise ValueError("Checkpoint boundary does not support its declared recovery guarantee")
