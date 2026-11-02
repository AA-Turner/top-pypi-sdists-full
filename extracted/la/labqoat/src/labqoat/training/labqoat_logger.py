"""Bounded experiment telemetry buffering."""

from collections import deque
from collections.abc import Mapping

from labqoat.training.experiment_sink import ExperimentSink
from labqoat.training.metric_batch import MetricBatch
from labqoat.training.telemetry_unavailable_error import TelemetryUnavailableError


class LabqoatLogger:
    """Retry transient telemetry failures without unbounded worker memory."""

    def __init__(self, sink: ExperimentSink, *, maximum_buffered_batches: int = 1000) -> None:
        """Store the explicit sink and a positive retry-buffer bound."""
        if maximum_buffered_batches <= 0:
            raise ValueError("Metric buffer capacity must be positive")
        self._sink = sink
        self._maximum = maximum_buffered_batches
        self._buffer: deque[MetricBatch] = deque()
        self._next_step = 0

    def log_hyperparameters(self, parameters: tuple[tuple[str, str], ...]) -> None:
        """Forward immutable parameters through the explicit sink."""
        self._sink.log_hyperparameters(parameters)

    def log_metrics(self, batch: MetricBatch) -> None:
        """Queue metrics in arrival order, failing rather than discarding evidence on overflow."""
        if len(self._buffer) == self._maximum:
            self.flush(require_delivery=True)
        self._buffer.append(batch)
        self._next_step = max(self._next_step, batch.step + 1)
        self.flush()

    def record_metrics(self, metrics: Mapping[str, float], *, step: int | None = None) -> None:
        """Validate scalar measurements and select an invocation-wide step independently of any framework."""
        selected = self._next_step if step is None else step
        batch = MetricBatch(step=selected, metrics=tuple(sorted(metrics.items())))
        if batch.metrics:
            self.log_metrics(batch)

    def flush(self, *, require_delivery: bool = False) -> None:
        """Retry queued batches and require the sink's durable acknowledgement when explicitly requested."""
        while self._buffer:
            try:
                self._sink.log_metrics(self._buffer[0])
            except TelemetryUnavailableError:
                if require_delivery:
                    raise
                return
            self._buffer.popleft()
        if require_delivery:
            self._sink.flush()

    def finalize(self, status: str) -> None:
        """Flush queued metrics before closing telemetry."""
        self.flush(require_delivery=True)
        self._sink.finalize(status)
