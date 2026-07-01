import typing as t
from datetime import UTC, datetime
from uuid import UUID, uuid4

import typing_extensions as te
from pydantic import BaseModel, ConfigDict, Field, computed_field

from dreadnode.tracing.constants import (
    EVALUATION_ATTRIBUTE_DATASET_SIZE,
    SAMPLE_ATTRIBUTE_INDEX,
)

if t.TYPE_CHECKING:
    from dreadnode.evaluations.result import EvalResult
    from dreadnode.tracing.span import TaskSpan

In = te.TypeVar("In", default=t.Any)
Out = te.TypeVar("Out", default=t.Any)


class EvalEvent(BaseModel, t.Generic[In, Out]):
    """Base class for all evaluation events."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    eval_id: UUID = Field(default_factory=uuid4)
    eval_name: str | None = None

    @computed_field
    @property
    def type(self) -> str:
        """Event type discriminator for serialization."""
        return self.__class__.__name__.lower()

    def as_dict(self) -> dict[str, t.Any]:
        """Serialize event to a dictionary."""
        return self.model_dump(mode="json")

    def _get_data(self) -> dict[str, t.Any]:
        """Override to provide event-specific data for serialization."""
        return self.model_dump(mode="json")

    def emit(self, span: "TaskSpan") -> None:
        """Emit telemetry to the span."""
        span.log_event(
            f"eval.{self.__class__.__name__}",
            {"event_type": self.__class__.__name__, "timestamp": self.timestamp.isoformat()},
        )


class EvalStart(EvalEvent[In, Out]):
    """Signals the beginning of an evaluation."""

    dataset_size: int = 0
    iterations: int = 1

    def emit(self, span: "TaskSpan") -> None:
        span.set_attribute(EVALUATION_ATTRIBUTE_DATASET_SIZE, self.dataset_size)
        span.log_param("dataset_size", self.dataset_size)
        span.log_param("scenario_count", 1)
        span.log_param("iterations", self.iterations)
        super().emit(span)


class EvalSample(EvalEvent[In, Out]):
    """A single sample in the evaluation."""

    sample_index: int = 0
    input: In | None = None
    output: Out | None = None
    scores: dict[str, float] = Field(default_factory=dict)
    passed: bool | None = None
    error: str | None = None

    def _get_data(self) -> dict[str, t.Any]:
        """Serialize event to a dictionary, with full serialization for input/output."""
        from dreadnode.core.serialization import serialize

        data = self.model_dump(mode="json", exclude={"input", "output"})

        if self.input is not None:
            data["input"] = serialize(self.input).data
        if self.output is not None:
            data["output"] = serialize(self.output).data

        return data

    def emit(self, span: "TaskSpan") -> None:
        span.set_attribute(SAMPLE_ATTRIBUTE_INDEX, self.sample_index)
        if self.input is not None:
            span.log_input("input", self.input)
        if self.output is not None:
            span.log_output("output", self.output)
        if self.scores:
            for name, score in self.scores.items():
                span.log_metric(f"sample/{name}", score, step=self.sample_index)
        if self.passed is not None:
            span.log_metric("sample/passed", 1 if self.passed else 0, step=self.sample_index)
        if self.error:
            span.log_output("error", self.error[:500])
        super().emit(span)


class EvalEnd(EvalEvent[In, Out]):
    """Signals the end of an evaluation."""

    result: "EvalResult[In, Out] | None" = Field(default=None, repr=False, exclude=True)
    total_samples: int = 0
    passed_count: int = 0
    failed_count: int = 0
    error_count: int = 0
    pass_rate: float = 0.0
    stop_reason: str | None = None
    mean_scores: dict[str, float] = Field(default_factory=dict)

    def emit(self, span: "TaskSpan") -> None:
        span.log_output(
            "eval_result",
            {
                "total_samples": self.total_samples,
                "passed_count": self.passed_count,
                "failed_count": self.failed_count,
                "error_count": self.error_count,
                "pass_rate": self.pass_rate,
                "stop_reason": self.stop_reason,
                "scenario_count": 1,
                "mean_scores": self.mean_scores,
            },
        )
        span.log_metric("eval/pass_rate", self.pass_rate)
        span.log_metric("eval/passed_count", self.passed_count)
        span.log_metric("eval/failed_count", self.failed_count)
        super().emit(span)
