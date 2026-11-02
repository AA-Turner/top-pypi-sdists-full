"""Invocation-owned restore execution and exact fenced acknowledgement before fit or publication."""

from pathlib import Path

from labqoat._generated.restore_receipt import RestoreReceipt
from labqoat.compute.run_checkpoints import RunCheckpoints
from labqoat.json_document import JsonDocument
from labqoat.schemas.identity import Identity
from labqoat.training.recovery.restore_adapter import RestoreAdapter
from labqoat.training.recovery.restore_envelope import RestoreEnvelope
from labqoat.training.recovery.restore_snapshot import RestoreSnapshot
from labqoat.training.recovery.restore_state import RestoreState
from labqoat.worker.replay_request import ReplayRequest
from labqoat.worker.worker_api import WorkerApi


class RunRecovery:
    """Keep restoration separate from authored arguments and never reinterpret resume as fresh execution."""

    def __init__(self, api: WorkerApi, checkpoints: RunCheckpoints, envelope: RestoreEnvelope, scratch: Path) -> None:
        """Bind only assignment-owned byte access and the exact retained immutable recovery plan."""
        self.api = api
        self.checkpoints = checkpoints
        self.envelope = envelope
        self.scratch = scratch
        self._state: RestoreState | None = None
        self._receipt: RestoreReceipt | None = None
        self._snapshot: RestoreSnapshot | None = None

    def restore(self, adapter: RestoreAdapter) -> RestoreState:
        """Restore once and exactly replay lost acknowledgements without invoking the adapter again."""
        snapshot = self.prepare(adapter)
        if self._state is None:
            restored = adapter.restore(snapshot)
            restored.evidence(self.envelope)
            self._state = restored
        self.acknowledge(self._state)
        return self._state

    def prepare(self, adapter: RestoreAdapter) -> RestoreSnapshot:
        """Stage verified bytes without acknowledging restoration or granting execution authority."""
        return self.stage(adapter.adapter_id, adapter.adapter_version)

    def stage(self, adapter_id: str, adapter_version: str) -> RestoreSnapshot:
        """Verify an explicit adapter binding before downloading one immutable aggregate snapshot."""
        requirements = JsonDocument.expect_dict(self.envelope.document["requirements"])
        if requirements["adapter"] != {"id": adapter_id, "version": adapter_version}:
            raise ValueError("Restore adapter does not match accepted workload capability")
        if self._snapshot is None:
            destination = self.scratch / "recovery" / "checkpoint"
            manifest = self.checkpoints.download(self.envelope.checkpoint, destination=destination)
            self.envelope.verify_snapshot(manifest)
            self._snapshot = RestoreSnapshot(destination, manifest, self.envelope)
        return self._snapshot

    def acknowledge(self, state: RestoreState) -> None:
        """Acknowledge actual restoration; distributed plans additionally require every persisted rank vote."""
        state.evidence(self.envelope)
        if self._state is not None and self._state != state:
            raise ValueError("Restore state cannot change after acknowledgement was requested")
        self._state = state
        if self._receipt is None:
            self._acknowledge(state)

    def _acknowledge(self, state: RestoreState) -> None:
        """Verify that the server's immutable receipt acknowledges this attempt and exact actual restored state."""
        evidence = state.evidence(self.envelope).to_dict()
        response = ReplayRequest(self.api).send("/api/v1/worker/restore/acknowledgements", evidence)
        receipt = RestoreReceipt.from_dict(response)
        if (
            receipt.attempt_id != self.envelope.document["attempt_id"]
            or receipt.fingerprint != Identity.digest(evidence)
            or receipt.evidence.to_dict() != evidence
        ):
            raise ValueError("Restore receipt does not match acknowledged state")
        self._receipt = receipt

    def require_ready(self) -> None:
        """Reject ignored plans before outputs or local training entry rather than silently starting fresh."""
        if self._receipt is None:
            raise ValueError("Recovery requires acknowledged restoration before execution can finish or fit")

    def require_fit(self) -> None:
        """Finalization-only restoration cannot receive another scientific fit interval."""
        self.require_ready()
        if self.envelope.document["mode"] == "finalize":
            raise ValueError("Finalization-only recovery cannot train")
