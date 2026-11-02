"""Standard training scalar names shared by every authored training loop."""

from collections.abc import Mapping

from labqoat.training.labqoat_logger import LabqoatLogger


class TrainingMetrics:
    """Record training, validation and test scalars under stable names so runs from any codebase line up."""

    def __init__(self, logger: LabqoatLogger) -> None:
        """Share the invocation's ordered telemetry logger."""
        self._logger = logger

    def step(self, step: int, **scalars: float | None) -> None:
        """Record one optimizer or RL step: every named scalar becomes `train/<name>` (`loss`, `reward`, `lr`, ...).

        `None` values are skipped, so optional measurements need no branching. At least one value is required.
        """
        measured = {name: value for name, value in scalars.items() if value is not None}
        if not measured:
            raise ValueError("training().step(step, ...) needs at least one scalar, such as loss= or reward=")
        self._record("train", None, measured, step)

    def validation(self, step: int, scores: Mapping[str, float], *, group: str | None = None) -> None:
        """Record held-out scores as `val/<name>` or `val/<group>/<name>`; `val/loss` is the main validation score."""
        self._record("val", group, scores, step)

    def test(self, scores: Mapping[str, float], *, group: str | None = None, step: int = 0) -> None:
        """Record final benchmark scores as `test/<name>`, or `test/<group>/<name>` for one slice."""
        self._record("test", group, scores, step)

    def model(self, *, parameters: int) -> None:
        """Record the trainable parameter count as `model/parameters`."""
        self._logger.record_metrics({"model/parameters": float(parameters)}, step=0)

    def _record(self, section: str, group: str | None, scores: Mapping[str, float], step: int) -> None:
        """Prefix every score with its section and optional slice before the shared name validation."""
        prefix = section if group is None else f"{section}/{group}"
        self._logger.record_metrics({f"{prefix}/{name}": float(value) for name, value in scores.items()}, step=step)
