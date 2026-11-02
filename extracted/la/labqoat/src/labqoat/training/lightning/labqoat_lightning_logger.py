"""PyTorch Lightning-compatible logger without a framework dependency."""

from __future__ import annotations

from collections.abc import Mapping

from labqoat.references import ResourceId
from labqoat.training.labqoat_logger import LabqoatLogger
from labqoat.training.lightning_scalars import LightningScalars


class LabqoatLightningLogger:
    """Adapt Lightning telemetry to an explicitly injected experiment sink."""

    def __init__(self, logger: LabqoatLogger, *, run_id: ResourceId) -> None:
        """Store the run identity and telemetry adapter."""
        self._logger = logger
        self._run_id = run_id
        self._parameters: dict[str, str] = {}
        self._parameters_logged = False

    @property
    def name(self) -> str:
        """Return the stable Lightning logger name."""
        return "labqoat"

    @property
    def version(self) -> str:
        """Return the immutable run identity."""
        return str(self._run_id)

    @property
    def experiment(self) -> LabqoatLightningLogger:
        """Expose this adapter as Lightning's experiment handle."""
        return self

    @property
    def save_dir(self) -> None:
        """Indicate that telemetry has no Lightning log directory."""
        return None

    @property
    def root_dir(self) -> None:
        """Indicate that telemetry has no local root directory."""
        return None

    @property
    def log_dir(self) -> None:
        """Indicate that telemetry has no local version directory."""
        return None

    @property
    def group_separator(self) -> str:
        """Preserve hierarchical metric names."""
        return "/"

    def log_hyperparams(self, params: object) -> None:
        """Collect hyperparameters before the first metric batch."""
        if not self._parameters_logged:
            self._parameters.update(LightningScalars.parameters(params))

    def log_metrics(self, metrics: Mapping[str, object], step: int | None = None) -> None:
        """Send one finite scalar metric batch."""
        self._flush_parameters()
        converted = {}
        for name, value in metrics.items():
            scalar = LightningScalars.metric(value)
            if scalar is not None:
                key = LightningScalars.name(name)
                if key in converted:
                    raise ValueError("Normalized training metric names must be unique")
                converted[key] = scalar
        if not converted:
            return
        self._logger.record_metrics(converted, step=step)

    def save(self) -> None:
        """Flush hyperparameters and the bounded metric queue."""
        self._flush_parameters()
        self._logger.flush()

    def finalize(self, status: str) -> None:
        """Flush telemetry without changing authoritative run state."""
        self.save()
        self._logger.finalize(status)

    def log_graph(self, model: object, input_array: object | None = None) -> None:
        """Accept Lightning's optional graph notification."""
        del model, input_array

    def after_save_checkpoint(self, checkpoint_callback: object) -> None:
        """Accept Lightning's checkpoint notification."""
        del checkpoint_callback

    def _flush_parameters(self) -> None:
        """Queue hyperparameters exactly once after successful sink acceptance."""
        if self._parameters_logged or not self._parameters:
            return
        self._logger.log_hyperparameters(tuple(sorted(self._parameters.items())))
        self._parameters_logged = True
