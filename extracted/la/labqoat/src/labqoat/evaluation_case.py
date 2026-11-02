"""Typed evidence linking an evaluated case to ordinary inference and scoring Runs."""

from dataclasses import dataclass

from labqoat.references import ResourceId
from labqoat.training.metric_batch import MetricBatch


@dataclass(frozen=True)
class EvaluationCase:
    """Record successful result handles and finite named scores without a remote evaluation lifecycle."""

    key: str
    inference_run_id: str
    scorer_run_id: str
    metrics: dict[str, float]

    def __post_init__(self) -> None:
        """Require explicit attribution, a bounded case key and nonempty finite measurements."""
        if not 1 <= len(self.key.encode()) <= 200 or not self.metrics:
            raise ValueError("Evaluation cases require a bounded key and nonempty metrics")
        ResourceId.parse(self.inference_run_id)
        ResourceId.parse(self.scorer_run_id)
        MetricBatch(step=0, metrics=tuple(self.metrics.items()))
