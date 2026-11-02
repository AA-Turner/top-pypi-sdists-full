"""Shared assignment-owned metrics and Lightning logging with a strict completion barrier."""

from typing import TYPE_CHECKING

from labqoat.references import ResourceId
from labqoat.training.labqoat_logger import LabqoatLogger
from labqoat.training.worker_experiment_sink import WorkerExperimentSink
from labqoat.worker.worker_api import WorkerApi
from labqoat.compute.output_buffer import OutputBuffer

if TYPE_CHECKING:
    from labqoat.training.lightning.labqoat_lightning_logger import LabqoatLightningLogger


class RunTelemetry:
    """Keep a single ordered telemetry buffer and step sequence for one invocation."""

    def __init__(self, api: WorkerApi, run_id: str) -> None:
        """Bind an explicit worker transport without opening a connection."""
        sink = WorkerExperimentSink(api)
        self.logs = sink
        self.output = OutputBuffer(sink)
        self.error_output = OutputBuffer(sink, "stderr")
        self.logger = LabqoatLogger(sink)
        self._run_id = ResourceId.parse(run_id)
        self._lightning: LabqoatLightningLogger | None = None

    @property
    def lightning(self) -> "LabqoatLightningLogger":
        """Create the optional framework adapter only when the authored function requests it."""
        from labqoat.training.lightning.labqoat_lightning_logger import LabqoatLightningLogger

        if self._lightning is None:
            self._lightning = LabqoatLightningLogger(self.logger, run_id=self._run_id)
        return self._lightning

    def finish(self) -> None:
        """Require all buffered framework evidence to reach the transport before publishing a result."""
        if self._lightning is not None:
            self._lightning.save()
        self.flush_output()
        self.logger.flush(require_delivery=True)

    def flush_output(self) -> None:
        """Flush independent stdout and stderr fragments without mixing their content."""
        self.output.flush()
        self.error_output.flush()
