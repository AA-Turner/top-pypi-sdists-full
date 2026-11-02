"""Explicit immutable execution identity supplied by an assignment-owned worker."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from labqoat.authoring.resources import Resources
from labqoat.compute.run_assets import RunAssets
from labqoat.json_document import JsonValue
from labqoat.training.run_log_record import RunLogRecord

if TYPE_CHECKING:
    from labqoat.coordination.dict import Dict
    from labqoat.coordination.dicts_client import DictsClient
    from labqoat.coordination.queue import Queue
    from labqoat.coordination.queues_client import QueuesClient
    from labqoat.coordination.store_channel import StoreChannel
    from labqoat.compute.run_memory import RunMemory
    from labqoat.compute.run_group import RunGroup
    from labqoat.compute.run_submissions import RunSubmissions
    from labqoat.compute.run_datasets import RunDatasets
    from labqoat.compute.run_telemetry import RunTelemetry
    from labqoat.compute.run_checkpoints import RunCheckpoints
    from labqoat.compute.run_fit_budget import RunFitBudget
    from labqoat.compute.run_recovery import RunRecovery
    from labqoat.compute.run_services import RunServices
    from labqoat.compute.run_workflow import RunWorkflow
    from labqoat.service.served_service import ServedService
    from labqoat.service.service import Service
    from labqoat.training.lightning.labqoat_lightning_logger import LabqoatLightningLogger
    from labqoat.training.training_metrics import TrainingMetrics


@dataclass(frozen=True)
class RunContext:
    """Identify the current fenced execution without retaining host management credentials."""

    run_id: str
    attempt_id: str
    fence: int
    scratch: Path
    assets: RunAssets = field(default_factory=RunAssets, repr=False, compare=False)
    _datasets: "RunDatasets | None" = field(default=None, repr=False, compare=False)
    seed: int = 0
    resources: Resources = field(default_factory=Resources)
    _telemetry: "RunTelemetry | None" = field(default=None, repr=False, compare=False)
    _checkpoints: "RunCheckpoints | None" = field(default=None, repr=False, compare=False)
    _runs: "RunSubmissions | None" = field(default=None, repr=False, compare=False)

    _memory: "RunMemory | None" = field(default=None, repr=False, compare=False)
    _fit_budget: "RunFitBudget | None" = field(default=None, repr=False, compare=False)
    recovery: "RunRecovery | None" = field(default=None, repr=False, compare=False)
    _workflow: "RunWorkflow | None" = field(default=None, repr=False, compare=False)
    _services: "RunServices | None" = field(default=None, repr=False, compare=False)
    _channel: "StoreChannel | None" = field(default=None, repr=False, compare=False)

    def dict(self, name: str) -> "Dict":
        """A dict of this run's project, shared with its other runs and its people; the first write creates it."""
        from labqoat.coordination.dict import Dict

        return Dict(self._coordination(), name)

    def queue(self, name: str) -> "Queue":
        """A queue of this run's project, shared with its other runs and its people; the first put creates it."""
        from labqoat.coordination.queue import Queue

        return Queue(self._coordination(), name)

    @property
    def dicts(self) -> "DictsClient":
        """List and delete this project's dicts, or use a throwaway one."""
        from labqoat.coordination.dicts_client import DictsClient

        return DictsClient(self._coordination())

    @property
    def queues(self) -> "QueuesClient":
        """List and delete this project's queues, or use a throwaway one."""
        from labqoat.coordination.queues_client import QueuesClient

        return QueuesClient(self._coordination())

    def _coordination(self) -> "StoreChannel":
        """Dicts and queues belong to the project the run's own credentials name."""
        if self._channel is None:
            raise RuntimeError("Dicts and queues require an assignment-owned RunContext")
        return self._channel

    @property
    def workflow(self) -> "RunWorkflow":
        """Access retained decisions only when the authored function declared workflow replay."""
        if self._workflow is None:
            raise RuntimeError("Workflow decisions require an assignment-owned context with declared workflow replay")
        return self._workflow

    def require_restored(self) -> None:
        """Prevent a retained entrypoint from ignoring an accepted restore plan and publishing fresh output."""
        if self.recovery is not None:
            self.recovery.require_ready()

    @property
    def fit_budget(self) -> "RunFitBudget":
        """Enter an explicitly declared cumulative fit region only under invocation-owned authority."""
        if self._fit_budget is None:
            raise RuntimeError("Fit supervision requires an assignment-owned RunContext with a declared allowance")
        return self._fit_budget

    @property
    def memory(self) -> "RunMemory":
        """Read and publish the shared research memory of this run's project."""
        if self._memory is None:
            raise RuntimeError("Memory access requires an assignment-owned RunContext")
        return self._memory

    @property
    def runs(self) -> "RunSubmissions":
        """Submit and reattach durable owned children through the current assignment's scoped authority."""
        if self._runs is None:
            raise RuntimeError("Child submission requires an assignment-owned RunContext")
        return self._runs

    def serve(
        self, name: str, *, port: int | None = None, unix_socket: str | None = None, startup_timeout: float = 600.0
    ) -> "ServedService":
        """Serve a local HTTP server to this run's project under ``name`` for the length of a ``with`` block.

        Give the loopback ``port`` the server listens on, or the ``unix_socket`` it listens at. Entering the
        block waits up to ``startup_timeout`` seconds for the server to listen and for the platform to carry
        it; other runs of the project then reach it through ``context.service(name)``.
        """
        from labqoat.service.service_target import ServiceTarget

        return self._serving().serve(name, ServiceTarget(port, unix_socket), startup_timeout)

    def service(self, name: str) -> "Service":
        """Name a service another run of this project serves; ``.url`` and ``.headers`` are what a client needs."""
        return self._serving().lookup(name)

    def _serving(self) -> "RunServices":
        """Services exist only where a run's own credentials decide whose they are."""
        if self._services is None:
            raise RuntimeError("Services require an assignment-owned RunContext")
        return self._services

    def group(self, name: str, *, title: str | None = None) -> "RunGroup":
        """Open a named group of child work that needs no parent run of its own.

        Use it as ``async with context.group("model-1") as group:`` and submit through the group. The name is a
        permanent key within this run; ``title`` is only what people see.
        """
        from labqoat.compute.run_group import RunGroup

        return RunGroup(self.runs, name, title)

    @property
    def checkpoints(self) -> "RunCheckpoints":
        """Expose publication and restoration only through the invocation's scoped capability."""
        if self._checkpoints is None:
            raise RuntimeError("Checkpoint access requires an assignment-owned RunContext")
        return self._checkpoints

    def settle(self) -> None:
        """Finish background work the function started, such as checkpoints still uploading."""
        if self._checkpoints is not None:
            self._checkpoints.settle()

    def log_metrics(self, metrics: Mapping[str, float], *, step: int | None = None) -> None:
        """Retain finite step metrics directly through the invocation's core telemetry logger."""
        if self._telemetry is None:
            raise RuntimeError("Metric logging requires an assignment-owned RunContext")
        self._telemetry.logger.record_metrics(metrics, step=step)

    def training(self) -> "TrainingMetrics":
        """Return the stable-name recorder for training, validation and test scalars."""
        from labqoat.training.training_metrics import TrainingMetrics

        if self._telemetry is None:
            raise RuntimeError("Metric logging requires an assignment-owned RunContext")
        return TrainingMetrics(self._telemetry.logger)

    def lightning_logger(self) -> "LabqoatLightningLogger":
        """Return the invocation's shared Lightning adapter without importing the framework."""
        if self._telemetry is None:
            raise RuntimeError("Metric logging requires an assignment-owned RunContext")
        return self._telemetry.lightning

    def milestone(self, message: str, data: Mapping[str, JsonValue] | None = None) -> None:
        """Record a structured key moment independently of sampled training metrics."""
        if self._telemetry is None:
            raise RuntimeError("Milestones require an assignment-owned RunContext")
        self._telemetry.logs.log_record(
            RunLogRecord(message, level="progress", stream="milestone", data=dict(data or {}))
        )

    def progress(self, step: int, *, total: int | None = None) -> None:
        """Report a work counter, bounded by `total` when the amount of work is known."""
        if isinstance(step, bool) or isinstance(total, bool) or step < 0:
            raise ValueError("Progress requires a step of 0 or more")
        if total is not None and (total <= 0 or step > total):
            raise ValueError("Progress requires 0 <= step <= total and total > 0")
        if self._telemetry is None:
            raise RuntimeError("Progress requires an assignment-owned RunContext")
        data: dict[str, JsonValue] = {"step": step}
        message = f"step {step}"
        if total is not None:
            data["total"] = total
            message = f"step {step}/{total}"
        self._telemetry.logs.log_record(RunLogRecord(message, level="progress", stream="progress", data=data))

    @property
    def datasets(self) -> "RunDatasets":
        """Expose publication and reads only when the worker supplied assignment-scoped services."""
        if self._datasets is None:
            raise RuntimeError("Dataset access requires an assignment-owned RunContext")
        return self._datasets
