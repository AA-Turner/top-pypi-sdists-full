"""Workload-specific restoration requirements retained independently of the runtime protocol."""

from dataclasses import dataclass
from typing import Literal

from labqoat.compute.checkpoint_compatibility import CheckpointCompatibility
from labqoat.compute.checkpoint_recovery_types import CheckpointGuarantee, CheckpointState
from labqoat.json_document import JsonDocument
from labqoat.manifests import Manifest
from labqoat.training.budgets.fit_allowance import FitAllowance


@dataclass(frozen=True, kw_only=True)
class RecoveryCapability:
    """Advertise only restoration implemented by the retained entrypoint's explicit adapter."""

    adapter_id: str
    adapter_version: str
    compatibility: CheckpointCompatibility
    required_state: tuple[CheckpointState, ...]
    guarantees: tuple[CheckpointGuarantee, ...]
    modes: tuple[Literal["resume", "finalize"], ...] = ("resume",)

    def capture(self, workers: object, allowance: FitAllowance | None) -> JsonDocument:
        """Require isolated execution with enforceable cumulative allowance before publication."""
        if workers is not None or allowance is None:
            raise ValueError("Recovery requires isolated execution and a cumulative fit allowance")
        if not self.modes or len(set(self.modes)) != len(self.modes):
            raise ValueError("Recovery modes must be nonempty and unique")
        document = JsonDocument(
            adapter={"id": self.adapter_id, "version": self.adapter_version},
            compatibility=self.compatibility.document(),
            required_state=list(self.required_state),
            guarantees=list(self.guarantees),
        )
        for mode in self.modes:
            Manifest.capture("checkpoint_restore", JsonDocument(document, mode=mode))
        return JsonDocument(document, modes=list(self.modes))
