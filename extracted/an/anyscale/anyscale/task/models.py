"""Models for `anyscale task aggregate` and `anyscale.task.aggregate`.

The groups come from the observability API on the cloud's system cluster, the same source
the console's Tasks tab reads. Field names and values are the API's.
"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, Type, Union

from anyscale._private.models import ModelBase, ModelEnum


class TaskAggregateBy(ModelEnum):
    """How tasks are grouped."""

    FUNCTION = "FUNCTION"
    JOB = "JOB"
    EXCEPTION = "EXCEPTION"

    __docstrings__: ClassVar[Dict[str, str]] = {
        FUNCTION: "One group per Ray function (and task type).",
        JOB: "One group per Ray job.",
        EXCEPTION: "One group per exception type that failed tasks.",
    }


class TaskType(ModelEnum):
    """The kind of Ray task a function group counts."""

    NORMAL_TASK = "NORMAL_TASK"
    ACTOR_TASK = "ACTOR_TASK"
    ACTOR_CREATION_TASK = "ACTOR_CREATION_TASK"
    DRIVER_TASK = "DRIVER_TASK"

    __docstrings__: ClassVar[Dict[str, str]] = {
        NORMAL_TASK: "A remote function call.",
        ACTOR_TASK: "A method call on an actor.",
        ACTOR_CREATION_TASK: "The task that creates an actor.",
        DRIVER_TASK: "The driver itself.",
    }


def _int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int.")


def _str(name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")


def _optional_str(name: str, value: Optional[str]) -> None:
    if value is not None and not isinstance(value, str):
        raise TypeError(f"{name} must be a string or None.")


def _optional_int(name: str, value: Optional[int]) -> None:
    if value is not None and (isinstance(value, bool) or not isinstance(value, int)):
        raise TypeError(f"{name} must be an int or None.")


@dataclass(frozen=True)
class TaskAggregateMetrics(ModelBase):
    """Counts and timings of the task attempts in one group."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.task.aggregate(by="function", job_id="prodjob_abc123")
for group in groups.results:
    print(group.function_name, group.metrics.count_failed, group.metrics.avg_execution_ns)
"""

    total: int = field(metadata={"docstring": "How many task attempts are in the group."})
    count_finished: int = field(metadata={"docstring": "Attempts that finished."})
    count_failed: int = field(metadata={"docstring": "Attempts that failed."})
    count_running: int = field(metadata={"docstring": "Attempts running right now."})
    count_pending_schedule: int = field(
        metadata={"docstring": "Attempts waiting to be scheduled."}
    )
    count_pending_dep: int = field(metadata={"docstring": "Attempts waiting for their arguments."})
    max_duration_ts_ns: Optional[int] = field(
        default=None,
        metadata={
            "docstring": "Longest attempt from submission to end, in nanoseconds, "
            "or None when no attempt has finished or failed."
        },
    )
    min_duration_ts_ns: Optional[int] = field(
        default=None,
        metadata={
            "docstring": "Shortest attempt from submission to end, in nanoseconds, "
            "or None when no attempt has finished or failed."
        },
    )
    avg_duration_ts_ns: Optional[int] = field(
        default=None,
        metadata={
            "docstring": "Mean attempt from submission to end, in nanoseconds, "
            "or None when no attempt has finished or failed."
        },
    )
    max_execution_ns: Optional[int] = field(
        default=None,
        metadata={
            "docstring": "Longest attempt execution time, in nanoseconds, "
            "or None when no attempt has finished or failed."
        },
    )
    min_execution_ns: Optional[int] = field(
        default=None,
        metadata={
            "docstring": "Shortest attempt execution time, in nanoseconds, "
            "or None when no attempt has finished or failed."
        },
    )
    avg_execution_ns: Optional[int] = field(
        default=None,
        metadata={
            "docstring": "Mean attempt execution time, in nanoseconds, "
            "or None when no attempt has finished or failed."
        },
    )

    def _validate_total(self, total: int):
        _int("total", total)

    def _validate_count_finished(self, count_finished: int):
        _int("count_finished", count_finished)

    def _validate_count_failed(self, count_failed: int):
        _int("count_failed", count_failed)

    def _validate_count_running(self, count_running: int):
        _int("count_running", count_running)

    def _validate_count_pending_schedule(self, count_pending_schedule: int):
        _int("count_pending_schedule", count_pending_schedule)

    def _validate_count_pending_dep(self, count_pending_dep: int):
        _int("count_pending_dep", count_pending_dep)

    def _validate_max_duration_ts_ns(self, max_duration_ts_ns: Optional[int]):
        _optional_int("max_duration_ts_ns", max_duration_ts_ns)

    def _validate_min_duration_ts_ns(self, min_duration_ts_ns: Optional[int]):
        _optional_int("min_duration_ts_ns", min_duration_ts_ns)

    def _validate_avg_duration_ts_ns(self, avg_duration_ts_ns: Optional[int]):
        _optional_int("avg_duration_ts_ns", avg_duration_ts_ns)

    def _validate_max_execution_ns(self, max_execution_ns: Optional[int]):
        _optional_int("max_execution_ns", max_execution_ns)

    def _validate_min_execution_ns(self, min_execution_ns: Optional[int]):
        _optional_int("min_execution_ns", min_execution_ns)

    def _validate_avg_execution_ns(self, avg_execution_ns: Optional[int]):
        _optional_int("avg_execution_ns", avg_execution_ns)


_METRICS_DOC = "Counts and timings of the group's task attempts; see TaskAggregateMetrics."
_SESSION_DOC = "The Ray session the group belongs to."


def _metrics(
    name: str, value: Union[TaskAggregateMetrics, Dict[str, Any]]
) -> TaskAggregateMetrics:
    # A dict is what `to_dict`, json or yaml gives back; it is coerced so a saved page
    # loads again with `from_dict`.
    if isinstance(value, dict):
        value = TaskAggregateMetrics.from_dict(value)
    if not isinstance(value, TaskAggregateMetrics):
        raise TypeError(f"{name} must be a TaskAggregateMetrics or corresponding dict.")
    return value


@dataclass(frozen=True)
class TaskFunctionAggregate(ModelBase):
    """The tasks of one Ray function, by task type, in one Ray session."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.task.aggregate(by="function", cluster_id="ses_abc123")
for group in groups.results:
    print(group.function_name, group.task_type, group.metrics.total)
"""

    function_name: Optional[str] = field(
        metadata={"docstring": "Name of the function, or None when Ray did not report one."}
    )
    task_type: TaskType = field(metadata={"docstring": "Kind of task; see TaskType."})
    ray_session_name: str = field(metadata={"docstring": _SESSION_DOC})
    metrics: Union[TaskAggregateMetrics, Dict[str, Any]] = field(
        metadata={"docstring": _METRICS_DOC}
    )

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TaskFunctionAggregate":
        # `to_dict` (and so json or yaml) leaves out a None `function_name`. The field
        # cannot take a default, as it comes before fields without one, so it is filled
        # back in here.
        return cls(**{"function_name": None, **d})

    def _validate_function_name(self, function_name: Optional[str]):
        _optional_str("function_name", function_name)

    def _validate_task_type(self, task_type: TaskType) -> TaskType:
        return TaskType.validate(task_type)

    def _validate_ray_session_name(self, ray_session_name: str):
        _str("ray_session_name", ray_session_name)

    def _validate_metrics(
        self, metrics: Union[TaskAggregateMetrics, Dict[str, Any]]
    ) -> TaskAggregateMetrics:
        return _metrics("metrics", metrics)


@dataclass(frozen=True)
class TaskJobAggregate(ModelBase):
    """The tasks of one Ray job in one Ray session."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.task.aggregate(by="job", cluster_id="ses_abc123")
for group in groups.results:
    print(group.job_id, group.metrics.count_running, group.metrics.count_failed)
"""

    job_id: str = field(metadata={"docstring": "The Ray job ID (hex)."})
    ray_session_name: str = field(metadata={"docstring": _SESSION_DOC})
    metrics: Union[TaskAggregateMetrics, Dict[str, Any]] = field(
        metadata={"docstring": _METRICS_DOC}
    )

    def _validate_job_id(self, job_id: str):
        _str("job_id", job_id)

    def _validate_ray_session_name(self, ray_session_name: str):
        _str("ray_session_name", ray_session_name)

    def _validate_metrics(
        self, metrics: Union[TaskAggregateMetrics, Dict[str, Any]]
    ) -> TaskAggregateMetrics:
        return _metrics("metrics", metrics)


@dataclass(frozen=True)
class TaskExceptionAggregate(ModelBase):
    """The failed tasks that raised one exception type in one Ray session."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.task.aggregate(by="exception", cluster_id="ses_abc123")
for group in groups.results:
    print(group.exception_type, group.metrics.count_failed)
"""

    exception_type: str = field(
        metadata={
            "docstring": "The Ray error type the tasks failed with, e.g. "
            "TASK_EXECUTION_EXCEPTION, TASK_UNSCHEDULABLE_ERROR or ACTOR_DIED."
        }
    )
    ray_session_name: str = field(metadata={"docstring": _SESSION_DOC})
    metrics: Union[TaskAggregateMetrics, Dict[str, Any]] = field(
        metadata={"docstring": _METRICS_DOC}
    )

    def _validate_exception_type(self, exception_type: str):
        _str("exception_type", exception_type)

    def _validate_ray_session_name(self, ray_session_name: str):
        _str("ray_session_name", ray_session_name)

    def _validate_metrics(
        self, metrics: Union[TaskAggregateMetrics, Dict[str, Any]]
    ) -> TaskAggregateMetrics:
        return _metrics("metrics", metrics)


TaskAggregate = Union[TaskFunctionAggregate, TaskJobAggregate, TaskExceptionAggregate]
_GROUP_TYPES = (TaskFunctionAggregate, TaskJobAggregate, TaskExceptionAggregate)
_GROUP_TYPE_BY: Dict[str, Type[ModelBase]] = {
    TaskAggregateBy.FUNCTION: TaskFunctionAggregate,
    TaskAggregateBy.JOB: TaskJobAggregate,
    TaskAggregateBy.EXCEPTION: TaskExceptionAggregate,
}
_RESULTS_ERROR = (
    "results must be a list of TaskFunctionAggregate, TaskJobAggregate or "
    "TaskExceptionAggregate, or their dicts."
)


@dataclass(frozen=True)
class TaskAggregates(ModelBase):
    """The task groups of a cluster, and how many groups there are in all."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.task.aggregate(by="exception", job_id="prodjob_abc123", max_items=50)
print(f"{len(groups.results)} of {groups.total} groups")
for group in groups.results:
    print(group.exception_type, group.metrics.count_failed)
"""

    by: TaskAggregateBy = field(
        metadata={"docstring": "How the tasks are grouped; see TaskAggregateBy."}
    )
    results: List[Union[TaskAggregate, Dict[str, Any]]] = field(
        metadata={
            "docstring": "The groups, as the API orders them: TaskFunctionAggregate, "
            "TaskJobAggregate or TaskExceptionAggregate, matching `by`."
        }
    )
    total: int = field(
        metadata={
            "docstring": "How many groups there are in all, which can be more than "
            "len(results) when max_items cut the list short."
        }
    )
    warning: Optional[str] = field(
        default=None,
        metadata={"docstring": "A note from the API when its data may be stale, else None."},
    )

    def _validate_by(self, by: TaskAggregateBy) -> TaskAggregateBy:
        return TaskAggregateBy.validate(by)

    def _validate_results(
        self, results: List[Union[TaskAggregate, Dict[str, Any]]]
    ) -> List[TaskAggregate]:
        # `by` is validated first, so a dict (from `to_dict`, json or yaml) is coerced into
        # the group type of this page's grouping; that is how a saved page loads again.
        if not isinstance(results, list):
            raise TypeError(_RESULTS_ERROR)
        group_type = _GROUP_TYPE_BY[self.by]
        groups: List[TaskAggregate] = []
        for item in results:
            group = group_type.from_dict(item) if isinstance(item, dict) else item
            if not isinstance(group, _GROUP_TYPES):
                raise TypeError(_RESULTS_ERROR)
            groups.append(group)
        return groups

    def _validate_total(self, total: int):
        if isinstance(total, bool) or not isinstance(total, int) or total < 0:
            raise ValueError("total must be a non-negative int.")

    def _validate_warning(self, warning: Optional[str]):
        _optional_str("warning", warning)
