"""Actual state inventory and progress reported by a workload-owned restoration adapter."""

from dataclasses import dataclass

from labqoat._generated.restore_acknowledgement import RestoreAcknowledgement
from labqoat.compute.checkpoint_progress import CheckpointProgress
from labqoat.compute.checkpoint_recovery_types import CheckpointState
from labqoat.json_document import JsonDocument
from labqoat.training.recovery.restore_envelope import RestoreEnvelope


@dataclass(frozen=True)
class RestoreState:
    """Describe state actually restored, never state merely advertised by a checkpoint manifest."""

    progress: CheckpointProgress
    state: tuple[CheckpointState, ...]

    def evidence(self, envelope: RestoreEnvelope) -> RestoreAcknowledgement:
        """Reject incomplete or rewound acknowledgements before asking the service to authorize fit."""
        plan = envelope.document
        requirements = JsonDocument.expect_dict(plan["requirements"])
        required = JsonDocument.expect_list(requirements["required_state"])
        if len(set(self.state)) != len(self.state) or any(item not in self.state for item in required):
            raise ValueError("Restore state inventory is incomplete or repeated")
        if self.progress.document() != plan["progress"]:
            raise ValueError("Restored progress does not match accepted checkpoint")
        checkpoint = JsonDocument.expect_dict(plan["checkpoint"])
        return RestoreAcknowledgement(
            checkpoint_id=JsonDocument.expect_scalar(checkpoint["id"], str),
            manifest_digest=JsonDocument.expect_scalar(checkpoint["manifest_digest"], str),
            plan_digest=envelope.manifest.digest,
            progress=self.progress.document(),
            state=list(self.state),
        )
