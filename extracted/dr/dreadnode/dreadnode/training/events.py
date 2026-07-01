"""Training lifecycle events following the emit(span) pattern."""

from __future__ import annotations

import typing as t
from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from dreadnode.tracing.constants import (
    TRAINING_ATTRIBUTE_CHECKPOINT_PATH,
    TRAINING_ATTRIBUTE_STEP,
)

if t.TYPE_CHECKING:
    from dreadnode.tracing.span import TaskSpan


class TrainingEvent(BaseModel):
    """Base class for training lifecycle events."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    training_id: UUID = Field(default_factory=uuid4)
    training_name: str | None = None

    def as_dict(self) -> dict[str, t.Any]:
        """Serialize event for MCP transport. Override in subclasses for custom data."""
        return {
            "type": self.__class__.__name__.lower(),
            "timestamp": self.timestamp.isoformat(),
            "training_id": str(self.training_id),
            "training_name": self.training_name,
            "data": self._get_data(),
        }

    def _get_data(self) -> dict[str, t.Any]:
        """Override to provide event-specific data for serialization."""
        return {}

    def emit(self, span: TaskSpan) -> None:
        """Emit this event's telemetry to the span."""
        span.log_event(
            f"training.{self.__class__.__name__}",
            {"event_type": self.__class__.__name__, "timestamp": self.timestamp.isoformat()},
        )


class TrainingStarted(TrainingEvent):
    """Emitted at training start with hyperparameters and dataset info."""

    params: dict[str, t.Any] = Field(default_factory=dict)
    dataset_stats: dict[str, t.Any] = Field(default_factory=dict)

    def _get_data(self) -> dict[str, t.Any]:
        return {"params": self.params, "dataset_stats": self.dataset_stats}

    def emit(self, span: TaskSpan) -> None:
        for key, value in self.params.items():
            span.log_param(key, value)
        for key, value in self.dataset_stats.items():
            span.log_metric(key, value, prefix="dataset")
        super().emit(span)


class TrainingStepCompleted(TrainingEvent):
    """Emitted per training step with loss/token metrics."""

    step: int = 0
    metrics: dict[str, float] = Field(default_factory=dict)

    def _get_data(self) -> dict[str, t.Any]:
        return {"step": self.step, "metrics": self.metrics}

    def emit(self, span: TaskSpan) -> None:
        span.set_attribute(TRAINING_ATTRIBUTE_STEP, self.step)
        for key, value in self.metrics.items():
            span.log_metric(key, value, step=self.step)
        super().emit(span)


class EvaluationCompleted(TrainingEvent):
    """Emitted after an evaluation pass during training."""

    step: int = 0
    metrics: dict[str, float] = Field(default_factory=dict)

    def _get_data(self) -> dict[str, t.Any]:
        return {"step": self.step, "metrics": self.metrics}

    def emit(self, span: TaskSpan) -> None:
        span.set_attribute(TRAINING_ATTRIBUTE_STEP, self.step)
        for key, value in self.metrics.items():
            span.log_metric(key, value, step=self.step, prefix="eval")
        super().emit(span)


class CheckpointSaved(TrainingEvent):
    """Emitted when a checkpoint is saved."""

    step: int = 0
    path: str = ""
    samples: list[dict[str, t.Any]] | None = None

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {"step": self.step, "path": self.path}
        if self.samples:
            data["sample_count"] = len(self.samples)
        return data

    def emit(self, span: TaskSpan) -> None:
        span.set_attribute(TRAINING_ATTRIBUTE_STEP, self.step)
        span.set_attribute(TRAINING_ATTRIBUTE_CHECKPOINT_PATH, self.path)
        span.log_artifact(self.path)
        if self.samples:
            for idx, sample in enumerate(self.samples):
                span.log_output(f"sample_{idx}", sample)
        super().emit(span)


class TrainingCompleted(TrainingEvent):
    """Emitted at training end with summary metrics."""

    total_steps: int = 0
    metrics: dict[str, float] = Field(default_factory=dict)

    def _get_data(self) -> dict[str, t.Any]:
        return {"total_steps": self.total_steps, "metrics": self.metrics}

    def emit(self, span: TaskSpan) -> None:
        span.set_attribute(TRAINING_ATTRIBUTE_STEP, self.total_steps)
        span.log_output(
            "training_result",
            {
                "total_steps": self.total_steps,
                "metrics": self.metrics,
            },
        )
        for key, value in self.metrics.items():
            span.log_metric(key, value)
        super().emit(span)
