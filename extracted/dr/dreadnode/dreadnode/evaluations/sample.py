import typing as t
from datetime import UTC, datetime
from uuid import UUID, uuid4

import typing_extensions as te
from pydantic import BaseModel, ConfigDict, Field

from dreadnode.core.exceptions import AssertionFailedError
from dreadnode.core.metric import MetricSeries
from dreadnode.core.types.common import UNSET, ErrorField
from dreadnode.tracing.span import TaskSpan

if t.TYPE_CHECKING:
    from dreadnode.core.task import Task
    from dreadnode.core.types.common import AnyDict


def _now_utc() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(tz=UTC)


In = te.TypeVar("In", default=t.Any)
Out = te.TypeVar("Out", default=t.Any)

FileFormat = t.Literal["jsonl", "csv", "json", "yaml", "yml"]

InputDataset = list[In]
InputDatasetProcessor = t.Callable[[InputDataset], InputDataset]


class Sample(BaseModel, t.Generic[In, Out]):
    """
    Represents a single input-output sample processed by a task.

    Attributes:
        id: Unique identifier for the sample.
        input: The sample input value.
        output: The sample output value.
        index: The index of the sample in the dataset.
        metrics: Metrics from scorers and execution.
        assertions: Pass/fail status for asserted scorers.
        context: Contextual information about the sample.
        error: Any error that occurred.
        task: Associated task span.
        created_at: The creation timestamp of the sample.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, use_attribute_docstrings=True)

    id: UUID = Field(default_factory=uuid4)
    input: In
    output: Out | None = None
    index: int = 0
    metrics: dict[str, MetricSeries] = Field(default_factory=dict)
    assertions: dict[str, bool] = Field(default_factory=dict)
    context: dict[str, t.Any] | None = Field(default=None, repr=False)
    error: ErrorField | None = Field(default=None, repr=False)
    task: TaskSpan[Out] | None = Field(default=None, repr=False)
    created_at: datetime = Field(default_factory=_now_utc)

    @property
    def passed(self) -> bool:
        """Whether all assertions have passed."""
        return all(self.assertions.values()) if self.assertions else True

    @property
    def failed(self) -> bool:
        """Whether the underlying task failed for reasons other than score assertions."""
        return self.error is not None and not isinstance(self.error, AssertionFailedError)

    def get_average_metric_value(self, key: str) -> float:
        """Compute the average value of the specified metric."""
        series = self.metrics.get(key)
        if series:
            mean = series.mean()
            if mean is not None:
                return mean
        return 0.0

    @classmethod
    def from_task(
        cls,
        task: "Task[..., t.Any]",
        span: TaskSpan[Out],
        input: t.Any,
        *,
        index: int = 0,
        context: dict[str, t.Any] | None = None,
    ) -> "Sample[In, Out]":
        # Assume false for all
        assert_scores: t.Any = getattr(task, "assert_scores", [])
        assertions = dict.fromkeys(assert_scores, False)

        # If a score was reported, assume true
        for name in set(span.metrics.keys()) & set(assertions.keys()):
            assertions[name] = True

        # Reset to false for any that triggered a failure
        if isinstance(span.exception, AssertionFailedError):
            for name in span.exception.failures:
                assertions[name] = False

        output: Out | None = None
        if span._output is not UNSET:
            output = t.cast("Out", span._output)

        return cls(
            input=t.cast("In", input),
            output=output,
            index=index,
            metrics=span.metrics,
            assertions=assertions,
            context=context,
            error=span.exception,
            task=span,
        )

    def to_dict(self) -> dict[str, t.Any]:
        """Flatten the sample's data for DataFrame conversion."""
        record: AnyDict = self.model_dump(
            exclude={"metrics", "assertions", "task"},
            mode="json",
        )

        record["passed"] = self.passed
        record["failed"] = self.failed
        record["task"] = self.task.name if self.task else None

        for assertion_name, passed in self.assertions.items():
            record[f"assertion_{assertion_name}"] = passed

        record_inputs = record.get("input", {})
        if isinstance(record_inputs, dict):
            for name, value in record_inputs.items():
                record[f"input_{name}"] = value

        for name, series in self.metrics.items():
            if series.value is not None:
                record[f"metric_{name}"] = series.mean()

        return record
