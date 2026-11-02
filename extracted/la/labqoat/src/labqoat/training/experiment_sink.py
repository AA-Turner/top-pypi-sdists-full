"""Explicit experiment telemetry boundary."""

from typing import Protocol

from labqoat.training.metric_batch import MetricBatch


class ExperimentSink(Protocol):
    """Accept telemetry without claiming authority over training run state."""

    def log_hyperparameters(self, parameters: tuple[tuple[str, str], ...]) -> None:
        """Record immutable training hyperparameters."""
        ...

    def log_metrics(self, batch: MetricBatch) -> None:
        """Record one finite step-aligned metric batch."""
        ...

    def finalize(self, status: str) -> None:
        """Flush observational telemetry at the end of execution."""
        ...

    def flush(self) -> None:
        """Require durable acknowledgement of all accepted observational telemetry."""
        ...
