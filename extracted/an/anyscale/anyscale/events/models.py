"""Models for `anyscale <resource> events` and `anyscale.events.list()`."""

from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import Dict, List, Optional

from anyscale._private.models import ModelBase


# The resources events can be listed for. Two of them have a different name on the
# wire (job -> production_job, cluster -> session); the private SDK owns that mapping.
ENTITY_TYPES: List[str] = ["job", "service", "workspace", "cluster"]

# Which `source` values the backend accepts for each resource. It returns 500 on any
# other value, so both the CLI (click.Choice) and this model check against this table.
# `CLUSTER` is deliberately absent for clusters: the API advertises it, but cluster events
# are stored with the finer-grained sources below and never with `CLUSTER`, so filtering
# on it would always return nothing. For the other three it selects the cluster's events.
SOURCES_BY_ENTITY: Dict[str, List[str]] = {
    "job": ["JOB", "CLUSTER"],
    "workspace": ["WORKSPACE", "CLUSTER"],
    "service": ["SERVICE", "SERVICE_VERSION", "ALB", "SERVE_DEPLOYMENT", "CLUSTER"],
    "cluster": [
        "AUTOSCALER",
        "CLUSTER_LIFECYCLE",
        "IDLE_TERMINATION",
        "JOBS",
        "WORKSPACE_SNAPSHOT",
        "OS",
    ],
}

# Every value of the backend's EventLevel, most severe first. Events are stored with all of
# them (the journal proto emits TRACE and CRITICAL too), so each must be filterable.
LEVELS: List[str] = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "UNKNOWN"]


@dataclass(frozen=True)
class EventsFilter(ModelBase):
    """Which resource to read events for, and which of its events to keep."""

    __doc_py_example__ = """\
import anyscale
from anyscale.events.models import EventsFilter

events_filter = EventsFilter(
    # One of: job, service, workspace, cluster.
    entity_type="job",
    # ID of that resource.
    entity_id="prodjob_abc123",
    # Optional: only events emitted by these subsystems. Valid values depend on entity_type.
    source=["JOB"],
    # Optional: only events at these levels.
    level=["ERROR", "WARNING"],
    # Optional: only events whose message contains this text (case-sensitive).
    message_contains="OOM",
    # Optional: exclusive time window, as timezone-aware datetimes.
    start_time=None,
    end_time=None,
    # Oldest first when True. Newest first by default.
    ascending=False,
    # Stop after this many events, across pages.
    max_items=100,
)
"""

    entity_type: str = field(
        metadata={"docstring": "The kind of resource: job, service, workspace or cluster."}
    )
    entity_id: str = field(metadata={"docstring": "ID of the resource, e.g. prodjob_abc123."})
    source: Optional[List[str]] = field(
        default=None,
        metadata={
            "docstring": "Only events emitted by these subsystems. Valid values depend on "
            "entity_type; None means all."
        },
    )
    level: Optional[List[str]] = field(
        default=None,
        metadata={
            "docstring": "Only events at these levels: CRITICAL, ERROR, WARNING, INFO, DEBUG, "
            "TRACE or UNKNOWN. None means all."
        },
    )
    message_contains: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Only events whose message contains this text (case-sensitive substring)."
        },
    )
    start_time: Optional[datetime] = field(
        default=None,
        metadata={
            "docstring": "Only events after this time (exclusive). None means from the beginning."
        },
    )
    end_time: Optional[datetime] = field(
        default=None,
        metadata={"docstring": "Only events before this time (exclusive). None means up to now."},
    )
    ascending: bool = field(
        default=False,
        metadata={"docstring": "Return the oldest events first. Newest first by default."},
    )
    max_items: int = field(
        default=100,
        metadata={
            "docstring": "Stop after this many events. Fetched in pages where the backend "
            "supports it."
        },
    )
    verbose: bool = field(
        default=False,
        metadata={
            "docstring": "Service only: return full event bodies instead of truncated ones."
        },
    )
    instance_id: Optional[str] = field(
        default=None,
        metadata={"docstring": "Cluster only: only events from this instance."},
    )
    node_ip: Optional[str] = field(
        default=None,
        metadata={"docstring": "Cluster only: only events from the node with this IP."},
    )
    resource_bundles: Optional[List[str]] = field(
        default=None,
        metadata={
            "docstring": "Cluster only: autoscaler events relevant to these resource bundles, "
            "each a JSON object such as '{\"GPU\": 1}'."
        },
    )

    def _validate_entity_type(self, entity_type: str):
        if entity_type not in ENTITY_TYPES:
            raise ValueError(f"entity_type must be one of {ENTITY_TYPES}, got {entity_type!r}.")

    def _validate_entity_id(self, entity_id: str):
        if not isinstance(entity_id, str) or not entity_id:
            raise ValueError("entity_id must be a non-empty string.")

    def _validate_source(self, source: Optional[List[str]]):
        if source is None:
            return
        allowed = SOURCES_BY_ENTITY.get(self.entity_type, [])
        unknown = [s for s in source if s not in allowed]
        if unknown:
            raise ValueError(
                f"source {unknown} is not valid for {self.entity_type}; choose from {allowed}."
            )

    def _validate_level(self, level: Optional[List[str]]):
        if level is None:
            return
        unknown = [lvl for lvl in level if lvl not in LEVELS]
        if unknown:
            raise ValueError(f"level {unknown} is not valid; choose from {LEVELS}.")

    def _validate_message_contains(self, message_contains: Optional[str]):
        if message_contains is not None and not isinstance(message_contains, str):
            raise TypeError("message_contains must be a string.")

    def _validate_start_time(self, start_time: Optional[datetime]):
        if start_time is not None and not isinstance(start_time, datetime):
            raise TypeError("start_time must be a datetime.")

    def _validate_end_time(self, end_time: Optional[datetime]):
        if end_time is not None and not isinstance(end_time, datetime):
            raise TypeError("end_time must be a datetime.")
        if end_time is not None and self.start_time is not None and end_time <= self.start_time:
            raise ValueError("end_time must be after start_time.")

    def _validate_ascending(self, ascending: bool):
        if not isinstance(ascending, bool):
            raise TypeError("ascending must be a boolean.")

    def _validate_max_items(self, max_items: int):
        if not isinstance(max_items, int) or isinstance(max_items, bool) or max_items < 1:
            raise ValueError("max_items must be a positive integer.")

    def _validate_verbose(self, verbose: bool):
        if not isinstance(verbose, bool):
            raise TypeError("verbose must be a boolean.")

    def _validate_instance_id(self, instance_id: Optional[str]):
        if instance_id is not None and not isinstance(instance_id, str):
            raise TypeError("instance_id must be a string.")

    def _validate_node_ip(self, node_ip: Optional[str]):
        if node_ip is not None and not isinstance(node_ip, str):
            raise TypeError("node_ip must be a string.")

    def _validate_resource_bundles(self, resource_bundles: Optional[List[str]]):
        if resource_bundles is None:
            return
        for bundle in resource_bundles:
            try:
                parsed = json.loads(bundle)
            except (TypeError, ValueError):
                parsed = None
            if not isinstance(parsed, dict):
                raise ValueError(
                    f"resource_bundles entries must be JSON objects such as '{{\"GPU\": 1}}', "
                    f"got {bundle!r}."
                )


@dataclass(frozen=True)
class Event(ModelBase):
    """One event of a job, service, workspace or cluster."""

    __doc_py_example__ = """\
import anyscale
from anyscale.events.models import EventsFilter

events = anyscale.events.list(EventsFilter(entity_type="job", entity_id="prodjob_abc123"))
for event in events:
    print(event.created_at, event.level, event.source, event.message)
"""

    id: str = field(metadata={"docstring": "Unique ID of the event."})
    created_at: datetime = field(metadata={"docstring": "When the event happened."})
    level: str = field(
        metadata={
            "docstring": "Severity, e.g. ERROR, WARNING, INFO or DEBUG. UNKNOWN when the event "
            "carries no level."
        }
    )
    source: str = field(metadata={"docstring": "Subsystem that emitted the event, e.g. CLUSTER."})
    message: Optional[str] = field(
        metadata={"docstring": "Human-readable description of the event. None when it has none."}
    )
    cluster_id: Optional[str] = field(
        default=None,
        metadata={"docstring": "ID of the cluster the event relates to, if any."},
    )

    def _validate_id(self, id: str):  # noqa: A002
        if not isinstance(id, str):
            raise TypeError("id must be a string.")

    def _validate_created_at(self, created_at: datetime):
        if not isinstance(created_at, datetime):
            raise TypeError("created_at must be a datetime.")

    def _validate_level(self, level: str):
        if not isinstance(level, str):
            raise TypeError("level must be a string.")

    def _validate_source(self, source: str):
        if not isinstance(source, str):
            raise TypeError("source must be a string.")

    def _validate_message(self, message: Optional[str]):
        if message is not None and not isinstance(message, str):
            raise TypeError("message must be a string or None.")

    def _validate_cluster_id(self, cluster_id: Optional[str]):
        if cluster_id is not None and not isinstance(cluster_id, str):
            raise TypeError("cluster_id must be a string.")
