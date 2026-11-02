"""Reconstruct one invocation's immutable accepted configuration and scoped capabilities."""

from dataclasses import dataclass
from pathlib import Path

from labqoat._generated.compute_publication import ComputePublication
from labqoat.authoring.resources import Resources
from labqoat.compute.run_assets import RunAssets
from labqoat.compute.run_memory import RunMemory
from labqoat.compute.run_checkpoints import RunCheckpoints
from labqoat.compute.run_datasets import RunDatasets
from labqoat.compute.run_telemetry import RunTelemetry
from labqoat.compute.run_submissions import RunSubmissions
from labqoat.compute.run_fit_budget import RunFitBudget
from labqoat.compute.run_recovery import RunRecovery
from labqoat.compute.run_services import RunServices
from labqoat.compute.run_workflow import RunWorkflow
from labqoat.coordination.worker_channel import WorkerChannel
from labqoat.json_document import JsonDocument
from labqoat.run_context import RunContext
from labqoat.storage.cache_settings import CacheSettings
from labqoat.storage.worker_file_access import WorkerFileAccess
from labqoat.training.assets.worker_asset_publisher import WorkerAssetPublisher
from labqoat.training.transfer_log import TransferLog
from labqoat.worker.worker_api import WorkerApi
from labqoat.training.recovery.restore_envelope import RestoreEnvelope


@dataclass(frozen=True)
class ContextFactory:
    """Give authored code only assignment-owned adapters and the service's effective resource selection."""

    api: WorkerApi
    scratch: Path

    def create(self, captured: JsonDocument) -> RunContext:
        """Bind capabilities to invocation scratch without reading ambient management configuration."""
        run_id = JsonDocument.expect_scalar(captured["run_id"], str)
        telemetry = RunTelemetry(self.api, run_id)
        log = TransferLog(telemetry.logs)
        assets = self._assets(log)
        digest = JsonDocument.expect_scalar(captured["execution_digest"], str)
        checkpoints = RunCheckpoints(self.api, assets, run_id, digest, self.scratch / "checkpoint-uploads", log)
        recovery = self._recovery(captured, checkpoints)
        return RunContext(
            run_id=run_id,
            attempt_id=JsonDocument.expect_scalar(captured["attempt_id"], str),
            fence=JsonDocument.expect_scalar(captured["fence"], int),
            scratch=self.scratch,
            assets=assets,
            _memory=RunMemory(self.api),
            _datasets=RunDatasets(self.api, self.scratch / "datasets", log),
            seed=JsonDocument.expect_scalar(captured["seed"], int),
            resources=Resources.from_value(captured["resources"]),
            _telemetry=telemetry,
            _checkpoints=checkpoints,
            _runs=RunSubmissions(self.api, ComputePublication.from_dict(JsonDocument.expect_dict(captured["compute"]))),
            _fit_budget=self._fit_budget(captured, recovery),
            recovery=recovery,
            _workflow=self._workflow(captured),
            _services=RunServices(self.api),
            _channel=WorkerChannel(self.api),
        )

    def _workflow(self, captured: JsonDocument) -> RunWorkflow | None:
        """Keep authored replay capability separate from runtime protocol support."""
        publication = ComputePublication.from_dict(JsonDocument.expect_dict(captured["compute"]))
        if publication.workflow_replay_protocol == 1 and publication.function.workflow_replay == 1:
            return RunWorkflow(self.api)
        return None

    def _recovery(self, captured: JsonDocument, checkpoints: RunCheckpoints) -> RunRecovery | None:
        """Validate the separate immutable recovery envelope before entering any workload code."""
        value = captured.get("recovery")
        if value is None:
            return None
        envelope = RestoreEnvelope.capture(JsonDocument.expect_dict(value), captured)
        return RunRecovery(self.api, checkpoints, envelope, self.scratch)

    def _fit_budget(self, captured: JsonDocument, recovery: RunRecovery | None) -> RunFitBudget | None:
        """Budgeted invocation code receives only its own fenced fit client, never a fresh allowance."""
        publication = ComputePublication.from_dict(JsonDocument.expect_dict(captured["compute"]))
        if publication.function.fit_budget_ms is None:
            return None
        return RunFitBudget(
            self.api,
            JsonDocument.expect_scalar(captured["run_id"], str),
            JsonDocument.expect_scalar(captured["attempt_id"], str),
            JsonDocument.expect_scalar(captured["fence"], int),
            recovery,
        )

    def _assets(self, log: TransferLog) -> RunAssets:
        """Share the same verified byte capabilities with authored asset and checkpoint operations."""
        return RunAssets(
            WorkerFileAccess(self.api, CacheSettings.worker(self.scratch / "assets")),
            WorkerAssetPublisher(self.api, purpose="compute", log=log),
        )
