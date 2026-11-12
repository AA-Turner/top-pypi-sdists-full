"""Models for `anyscale actor aggregate` and `anyscale.actor.aggregate`.

The groups come from the observability API on the cloud's system cluster, the same source
the console's Actors tab reads. Field names and values are the API's.
"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, Type, Union

from anyscale._private.models import ModelBase, ModelEnum


class ActorAggregateBy(ModelEnum):
    """How actors are grouped."""

    NAME = "NAME"
    JOB = "JOB"
    EXIT_DETAIL = "EXIT_DETAIL"

    __docstrings__: ClassVar[Dict[str, str]] = {
        NAME: "One group per actor name and class.",
        JOB: "One group per Ray job.",
        EXIT_DETAIL: "One group per reason actors died, with its error message.",
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


@dataclass(frozen=True)
class ActorAggregateMetrics(ModelBase):
    """Counts of the actors in one group, by state."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.actor.aggregate(by="name", job_id="prodjob_abc123")
for group in groups.results:
    print(group.name, group.metrics.count_alive, group.metrics.count_dead)
"""

    total: int = field(metadata={"docstring": "How many actors are in the group."})
    count_dependencies_unready: int = field(
        metadata={"docstring": "Actors waiting for their constructor arguments."}
    )
    count_pending_creation: int = field(
        metadata={"docstring": "Actors waiting to be placed and created."}
    )
    count_alive: int = field(metadata={"docstring": "Actors alive right now."})
    count_restarting: int = field(metadata={"docstring": "Actors being restarted."})
    count_dead: int = field(metadata={"docstring": "Actors that died or exited."})

    def _validate_total(self, total: int):
        _int("total", total)

    def _validate_count_dependencies_unready(self, count_dependencies_unready: int):
        _int("count_dependencies_unready", count_dependencies_unready)

    def _validate_count_pending_creation(self, count_pending_creation: int):
        _int("count_pending_creation", count_pending_creation)

    def _validate_count_alive(self, count_alive: int):
        _int("count_alive", count_alive)

    def _validate_count_restarting(self, count_restarting: int):
        _int("count_restarting", count_restarting)

    def _validate_count_dead(self, count_dead: int):
        _int("count_dead", count_dead)


_METRICS_DOC = "Counts of the group's actors by state; see ActorAggregateMetrics."
_SESSION_DOC = "The Ray session the group belongs to."


def _metrics(
    name: str, value: Union[ActorAggregateMetrics, Dict[str, Any]]
) -> ActorAggregateMetrics:
    # A dict is what `to_dict`, json or yaml gives back; it is coerced so a saved page
    # loads again with `from_dict`.
    if isinstance(value, dict):
        value = ActorAggregateMetrics.from_dict(value)
    if not isinstance(value, ActorAggregateMetrics):
        raise TypeError(f"{name} must be an ActorAggregateMetrics or corresponding dict.")
    return value


@dataclass(frozen=True)
class ActorNameAggregate(ModelBase):
    """The actors of one name and class in one Ray session."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.actor.aggregate(by="name", cluster_id="ses_abc123")
for group in groups.results:
    print(group.name, group.class_name, group.metrics.total)
"""

    name: Optional[str] = field(
        metadata={"docstring": "The actor name, or None for actors without one."}
    )
    class_name: Optional[str] = field(
        metadata={"docstring": "The actor's class, or None when Ray did not report one."}
    )
    ray_session_name: str = field(metadata={"docstring": _SESSION_DOC})
    metrics: Union[ActorAggregateMetrics, Dict[str, Any]] = field(
        metadata={"docstring": _METRICS_DOC}
    )

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ActorNameAggregate":
        # `to_dict` (and so json or yaml) leaves out a None `name` or `class_name`. The
        # fields cannot take a default, as they come before fields without one, so they
        # are filled back in here.
        return cls(**{"name": None, "class_name": None, **d})

    def _validate_name(self, name: Optional[str]):
        _optional_str("name", name)

    def _validate_class_name(self, class_name: Optional[str]):
        _optional_str("class_name", class_name)

    def _validate_ray_session_name(self, ray_session_name: str):
        _str("ray_session_name", ray_session_name)

    def _validate_metrics(
        self, metrics: Union[ActorAggregateMetrics, Dict[str, Any]]
    ) -> ActorAggregateMetrics:
        return _metrics("metrics", metrics)


@dataclass(frozen=True)
class ActorJobAggregate(ModelBase):
    """The actors of one Ray job in one Ray session."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.actor.aggregate(by="job", cluster_id="ses_abc123")
for group in groups.results:
    print(group.job_id, group.metrics.count_alive)
"""

    job_id: str = field(metadata={"docstring": "The Ray job ID (hex)."})
    ray_session_name: str = field(metadata={"docstring": _SESSION_DOC})
    metrics: Union[ActorAggregateMetrics, Dict[str, Any]] = field(
        metadata={"docstring": _METRICS_DOC}
    )

    def _validate_job_id(self, job_id: str):
        _str("job_id", job_id)

    def _validate_ray_session_name(self, ray_session_name: str):
        _str("ray_session_name", ray_session_name)

    def _validate_metrics(
        self, metrics: Union[ActorAggregateMetrics, Dict[str, Any]]
    ) -> ActorAggregateMetrics:
        return _metrics("metrics", metrics)


@dataclass(frozen=True)
class ActorExitDetailAggregate(ModelBase):
    """The actors that died for one reason, with one error message, in one Ray session."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.actor.aggregate(by="exit_detail", cluster_id="ses_abc123")
for group in groups.results:
    print(group.death_reason, group.metrics.count_dead, group.error_message)
"""

    death_reason: str = field(metadata={"docstring": "Why the actors died, as Ray reports it."})
    error_message: str = field(
        metadata={"docstring": "The error message Ray attached, or an empty string."}
    )
    ray_session_name: str = field(metadata={"docstring": _SESSION_DOC})
    metrics: Union[ActorAggregateMetrics, Dict[str, Any]] = field(
        metadata={"docstring": _METRICS_DOC}
    )

    def _validate_death_reason(self, death_reason: str):
        _str("death_reason", death_reason)

    def _validate_error_message(self, error_message: str):
        _str("error_message", error_message)

    def _validate_ray_session_name(self, ray_session_name: str):
        _str("ray_session_name", ray_session_name)

    def _validate_metrics(
        self, metrics: Union[ActorAggregateMetrics, Dict[str, Any]]
    ) -> ActorAggregateMetrics:
        return _metrics("metrics", metrics)


ActorAggregate = Union[ActorNameAggregate, ActorJobAggregate, ActorExitDetailAggregate]
_GROUP_TYPES = (ActorNameAggregate, ActorJobAggregate, ActorExitDetailAggregate)
_GROUP_TYPE_BY: Dict[str, Type[ModelBase]] = {
    ActorAggregateBy.NAME: ActorNameAggregate,
    ActorAggregateBy.JOB: ActorJobAggregate,
    ActorAggregateBy.EXIT_DETAIL: ActorExitDetailAggregate,
}
_RESULTS_ERROR = (
    "results must be a list of ActorNameAggregate, ActorJobAggregate or "
    "ActorExitDetailAggregate, or their dicts."
)


@dataclass(frozen=True)
class ActorAggregates(ModelBase):
    """The actor groups of a cluster, and how many groups there are in all."""

    __doc_py_example__ = """\
import anyscale

groups = anyscale.actor.aggregate(by="exit_detail", job_id="prodjob_abc123", max_items=50)
print(f"{len(groups.results)} of {groups.total} groups")
for group in groups.results:
    print(group.death_reason, group.metrics.count_dead)
"""

    by: ActorAggregateBy = field(
        metadata={"docstring": "How the actors are grouped; see ActorAggregateBy."}
    )
    results: List[Union[ActorAggregate, Dict[str, Any]]] = field(
        metadata={
            "docstring": "The groups, as the API orders them: ActorNameAggregate, "
            "ActorJobAggregate or ActorExitDetailAggregate, matching `by`."
        }
    )
    total: int = field(
        metadata={
            "docstring": "How many groups the API returned in all. The API does not page "
            "actors, so this can be more than len(results) only when max_items cut the "
            "list short."
        }
    )
    warning: Optional[str] = field(
        default=None,
        metadata={"docstring": "A note from the API when its data may be stale, else None."},
    )

    def _validate_by(self, by: ActorAggregateBy) -> ActorAggregateBy:
        return ActorAggregateBy.validate(by)

    def _validate_results(
        self, results: List[Union[ActorAggregate, Dict[str, Any]]]
    ) -> List[ActorAggregate]:
        # `by` is validated first, so a dict (from `to_dict`, json or yaml) is coerced into
        # the group type of this page's grouping; that is how a saved page loads again.
        if not isinstance(results, list):
            raise TypeError(_RESULTS_ERROR)
        group_type = _GROUP_TYPE_BY[self.by]
        groups: List[ActorAggregate] = []
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
