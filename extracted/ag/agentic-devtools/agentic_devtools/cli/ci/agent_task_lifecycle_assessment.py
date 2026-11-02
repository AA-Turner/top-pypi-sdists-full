"""Typed lifecycle assessment models and inventory diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.agent_task_inventory import FailureCategory
from agentic_devtools.cli.ci.agent_task_lifecycle import parse_lifecycle_timestamp
from agentic_devtools.cli.ci.models import AgentTaskInventory, AgentTaskInventoryAvailability, AgentTaskLifecycle


@dataclass(frozen=True)
class LifecycleAssessment:
    """Classification of one active task or session lifecycle."""

    blocking: bool | None
    expired: bool
    since: datetime | None
    reason: str
    inventory_availability: AgentTaskInventoryAvailability = AgentTaskInventoryAvailability.COMPLETE
    failure_category: FailureCategory | None = None
    http_status: int | None = None
    failure_source: str | None = None


def _parent_lifecycle_clock(task: AgentTaskLifecycle) -> datetime | None:
    """Select only actual parent start or idle activity."""
    return max(
        (
            timestamp
            for value in (task.started_at, task.idle_at)
            if (timestamp := parse_lifecycle_timestamp(value)) is not None
        ),
        default=None,
    )


def _inventory_lifecycle_assessment(
    blocking: bool | None,
    expired: bool,
    since: datetime | None,
    reason: str,
    *,
    inventory: AgentTaskInventory,
    failure_category: FailureCategory | None = None,
) -> LifecycleAssessment:
    """Carry inventory availability and failure details through lifecycle classification."""
    return LifecycleAssessment(
        blocking,
        expired,
        since,
        reason,
        inventory_availability=inventory.availability or AgentTaskInventoryAvailability.COMPLETE,
        failure_category=inventory.failure_category or failure_category,
        http_status=inventory.http_status,
        failure_source="agent-task-lifecycle" if not inventory.complete or failure_category else None,
    )


def _malformed_task_ids(inventory: AgentTaskInventory, *, now: datetime, max_age: timedelta) -> frozenset[str]:
    """Identify task-scoped incompleteness except for independently current parent activity."""
    now_utc = now.replace(tzinfo=UTC) if now.tzinfo is None else now.astimezone(UTC)
    malformed: set[str] = set()
    for reason in inventory.incomplete_reasons:
        if not reason.startswith(("task-detail:", "malformed-session:", "missing-session-id:")):
            continue
        task_id = reason.partition(":")[2]
        if reason.startswith("task-detail:"):
            task = next((item for item in inventory.tasks if item.task_id == task_id), None)
            if task is not None and any(
                (clock := parse_lifecycle_timestamp(value)) is not None and timedelta(0) <= now_utc - clock <= max_age
                for value in (task.started_at, task.idle_at)
            ):
                continue
        malformed.add(task_id)
    return frozenset(malformed)
