"""Data models for cross-cluster migration jobs (platform contract 0.2.0).

The platform exposes a *job-level status projection*: a 5-value status enum
plus item counters, and — for single-job lookups — a per-item breakdown. The
internal per-stage phases (planning / streaming / registering...) deliberately
do not cross the platform boundary, so no model here tries to carry them.

Wire rules this module encodes:

* Response bodies are camelCase protojson (``jobId``, ``nextCursor``,
  ``resourceType``).
* ``EmitUnpopulated`` is on, so unset fields arrive as **0 / empty string**
  rather than being omitted. A counter of ``0`` is a real value and must be
  preserved, not normalized away.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

#: Resource types a migration job can operate on. Kept internal: no public
#: v2 signature needs it (``resource_type`` is implied by which method you call).
RESOURCE_TYPE_SANDBOX = "sandbox"
RESOURCE_TYPE_TEMPLATE = "template"


class JobStatus(str, Enum):
    """Overall, externally visible status of a migration job.

    Internal per-stage detail is intentionally not exposed by the platform.
    """

    MIGRATING = "migrating"
    COMPLETED = "completed"
    #: Cancel accepted; the runner is rolling back what it had already moved.
    #: Replaced the pre-0.2.0 ``cancelling`` value, which only marked work for
    #: cancellation instead of undoing it.
    REVERTING = "reverting"
    CANCELLED = "cancelled"
    FAILED = "failed"


class JobType(str, Enum):
    """Job type, derived from ``resource_type`` by the platform.

    ``CUSTOMER`` (whole-account migration) is only ever created by operators
    talking to migration-api directly; SDK-created jobs never have it. It stays
    a member because it is a valid ``list(type=...)`` filter value.
    """

    SANDBOX_BATCH = "sandbox_batch"
    TEMPLATE = "template"
    CUSTOMER = "customer"


TERMINAL_JOB_STATUSES = frozenset(
    {JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED}
)
"""Statuses after which a job never changes again.

``reverting`` is deliberately absent: cancel is cooperative, so a job can stay
in ``reverting`` until the runner finishes rolling the already-moved items
back.
"""


@dataclass(frozen=True)
class MigrationItemStatus:
    """One item of a migration job.

    ``resource_type`` is ``sandbox``, ``template`` or ``base`` — the base
    template a sandbox migration drags along — and unknown values are passed
    through unchanged.
    """

    item_id: str
    resource_type: str
    resource_id: str
    # A known member of :class:`JobStatus`, or the unknown wire string as-is.
    status: Union[JobStatus, str]


@dataclass(frozen=True)
class MigrationStatus:
    """Job-level status projection: the 5-value status plus item counters.

    :attr:`items` is only populated by the single-job lookups (``get``,
    ``cancel`` and therefore every ``wait`` poll); list responses carry an
    empty list and are described by the counters alone.

    ``total`` counts the job's requested items only: the base template a
    sandbox migration drags along appears in :attr:`items` with
    ``resource_type == "base"`` but is not counted, and
    ``completed + failed + cancelled`` may therefore be smaller than ``total``
    — items still in flight, or being reverted by a cancel, are counted in
    ``total`` only.
    """

    job_id: str
    # A known member of :class:`JobStatus`, or — because the platform may add
    # statuses and parsing must never crash — the unknown wire string as-is.
    status: Union[JobStatus, str]
    completed: int
    failed: int
    cancelled: int
    total: int
    #: Per-item breakdown. Defaulted so a hand-built status compares equal to
    #: a list projection, which carries no items.
    items: List[MigrationItemStatus] = field(default_factory=list)

    @property
    def is_terminal(self) -> bool:
        return self.status in TERMINAL_JOB_STATUSES


@dataclass(frozen=True)
class JobPage:
    """One page of migration statuses. Single and list queries share the shape."""

    items: List[MigrationStatus]
    next_cursor: Optional[str]


def _optional_str(value: Any) -> Optional[str]:
    """Normalize the empty string protojson uses for "unset" to ``None``."""
    if not isinstance(value, str) or value == "":
        return None
    return value


def _parse_status(value: Any) -> Any:
    """Parse the status enum, passing unknown values through as plain strings.

    The platform may add statuses; an unknown one must not crash parsing, and
    ``wait()`` treats it as non-terminal so the caller keeps polling rather
    than silently succeeding on a state it cannot interpret.
    """
    if isinstance(value, JobStatus):
        return value
    try:
        return JobStatus(value)
    except ValueError:
        return value


def _parse_counter(value: Any) -> int:
    """Parse an int32 counter. ``0`` is a legal value (EmitUnpopulated)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0
    return int(value)


def status_wire_value(status: Any) -> str:
    """The wire string for a status, whether parsed enum or passed-through."""
    value = getattr(status, "value", status)
    return value if isinstance(value, str) else str(value)


def migration_item_status_from_json(
    data: Dict[str, Any],
) -> MigrationItemStatus:
    """Build a :class:`MigrationItemStatus` from a camelCase response object."""
    return MigrationItemStatus(
        item_id=data.get("itemId") or "",
        resource_type=data.get("resourceType") or "",
        resource_id=data.get("resourceId") or "",
        status=_parse_status(data.get("status")),
    )


def migration_status_from_json(data: Dict[str, Any]) -> MigrationStatus:
    """Build a :class:`MigrationStatus` from a camelCase response object."""
    return MigrationStatus(
        job_id=data.get("jobId") or "",
        status=_parse_status(data.get("status")),
        completed=_parse_counter(data.get("completed")),
        failed=_parse_counter(data.get("failed")),
        cancelled=_parse_counter(data.get("cancelled")),
        total=_parse_counter(data.get("total")),
        items=[
            migration_item_status_from_json(item)
            for item in data.get("items") or []
        ],
    )


def job_page_from_json(data: Dict[str, Any]) -> JobPage:
    """Build a :class:`JobPage` from a camelCase response object."""
    return JobPage(
        items=[
            migration_status_from_json(item) for item in data.get("items") or []
        ],
        next_cursor=_optional_str(data.get("nextCursor")),
    )
