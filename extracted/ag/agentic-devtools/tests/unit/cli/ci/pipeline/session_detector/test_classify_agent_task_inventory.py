from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
    FailureCategory,
)
from agentic_devtools.cli.ci.pipeline.session_detector import classify_agent_task_inventory

NOW = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)


@pytest.mark.parametrize("state", ["queued", "QUEUED", "QuEuEd"])
def test_queued_task_without_sessions_does_not_prove_activity(state: str) -> None:
    task = AgentTaskLifecycle(
        task_id="queued",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state=state,
        created_at=NOW.isoformat(),
    )
    result = classify_agent_task_inventory(AgentTaskInventory((task,)), now=NOW)
    assert result.blocking is None


def test_unknown_task_state_is_not_active() -> None:
    task = AgentTaskLifecycle(
        task_id="unknown",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="new-provider-state",
        created_at=NOW.isoformat(),
    )
    result = classify_agent_task_inventory(AgentTaskInventory((task,)), now=NOW)
    assert result.blocking is None
    assert result.failure_category is FailureCategory.UNKNOWN_TASK_STATE


def test_partial_inventory_preserves_verified_active_task() -> None:
    task = AgentTaskLifecycle(
        task_id="active",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=NOW.isoformat(),
    )
    result = classify_agent_task_inventory(
        AgentTaskInventory((task,), complete=False, incomplete_reasons=("task-detail:other",)), now=NOW
    )
    assert result.blocking is True


def test_incomplete_future_clock_is_unknown_without_losing_inventory_diagnostics() -> None:
    task = AgentTaskLifecycle(
        task_id="future",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=(NOW - timedelta(hours=2)).isoformat(),
        idle_at="9999-12-31T23:59:59Z",
    )
    inventory = AgentTaskInventory(
        (task,),
        complete=False,
        incomplete_reasons=("page-limit",),
        failure_category=FailureCategory.RETRIEVAL_EXHAUSTED,
        http_status=503,
    )

    result = classify_agent_task_inventory(inventory, now=NOW)

    assert result.blocking is None
    assert result.reason == "future-lifecycle-clock"
    assert result.inventory_availability.value == "partial"
    assert result.failure_category is FailureCategory.RETRIEVAL_EXHAUSTED
    assert result.http_status == 503
    assert inventory.incomplete_reasons == ("page-limit",)


@pytest.mark.parametrize(
    ("incomplete_reason", "parent_age", "expected"),
    [
        ("page-limit", timedelta(minutes=5), True),
        ("task-detail:task-1", timedelta(minutes=5), True),
        ("page-limit", timedelta(hours=2), None),
        ("page-limit", -timedelta(minutes=5), None),
    ],
)
def test_future_session_clock_uses_parent_activity_only_when_current(
    incomplete_reason: str, parent_age: timedelta, expected: bool | None
) -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=(NOW - timedelta(hours=2)).isoformat(),
        started_at=(NOW - parent_age).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="in_progress",
                idle_at="9999-12-31T23:59:59Z",
            ),
        ),
    )

    result = classify_agent_task_inventory(
        AgentTaskInventory((task,), complete=False, incomplete_reasons=(incomplete_reason,)),
        now=NOW,
    )

    assert result.blocking is expected
    assert result.reason == ("blocking-lifecycle" if expected else "future-lifecycle-clock")


@pytest.mark.parametrize(
    ("incomplete_reason", "fallback_source"),
    [
        ("page-limit", "created_at"),
        ("task-detail:task-1", "created_at"),
        ("page-limit", "first_observed_at"),
        ("task-detail:task-1", "first_observed_at"),
    ],
)
def test_incomplete_future_session_clock_does_not_use_bookkeeping_fallbacks(
    incomplete_reason: str, fallback_source: str
) -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=NOW.isoformat() if fallback_source == "created_at" else "",
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="in_progress",
                idle_at="9999-12-31T23:59:59Z",
            ),
        ),
    )
    inventory = AgentTaskInventory((task,), complete=False, incomplete_reasons=(incomplete_reason,))
    observed = {"task-1": {"task": NOW.isoformat()}} if fallback_source == "first_observed_at" else None

    result = classify_agent_task_inventory(inventory, now=NOW, first_observed_at=observed)

    assert result.blocking is None
    assert result.reason == "future-lifecycle-clock"
    assert result.inventory_availability.value == "partial"
    assert inventory.incomplete_reasons == (incomplete_reason,)


def test_incomplete_future_clock_does_not_hide_an_independent_typed_blocker() -> None:
    future = AgentTaskLifecycle(
        task_id="future",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=(NOW - timedelta(hours=2)).isoformat(),
        idle_at="9999-12-31T23:59:59Z",
    )
    active = AgentTaskLifecycle(
        task_id="active",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=NOW.isoformat(),
    )

    result = classify_agent_task_inventory(
        AgentTaskInventory((future, active), complete=False, incomplete_reasons=("page-limit",)),
        now=NOW,
    )

    assert result.blocking is True
    assert result.reason == "blocking-lifecycle"


def test_malformed_active_task_is_unknown() -> None:
    task = AgentTaskLifecycle(
        task_id="malformed",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=NOW.isoformat(),
    )

    result = classify_agent_task_inventory(
        AgentTaskInventory((task,), complete=False, incomplete_reasons=("malformed-session:malformed",)),
        now=NOW,
    )

    assert result.blocking is None
    assert result.reason == "malformed-lifecycle"


def test_well_formed_active_task_blocks_alongside_malformed_task() -> None:
    malformed = AgentTaskLifecycle(
        task_id="malformed",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=NOW.isoformat(),
    )
    active = AgentTaskLifecycle(
        task_id="active",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=NOW.isoformat(),
    )

    result = classify_agent_task_inventory(
        AgentTaskInventory(
            (malformed, active),
            complete=False,
            incomplete_reasons=("malformed-session:malformed",),
        ),
        now=NOW,
    )

    assert result.blocking is True


def test_complete_empty_inventory_proves_no_activity() -> None:
    result = classify_agent_task_inventory(AgentTaskInventory(()), now=NOW)
    assert result.blocking is False
    assert result.expired is False


def test_failed_inventory_retains_http_failure_details() -> None:
    inventory = AgentTaskInventory(
        (),
        complete=False,
        failure_category=FailureCategory.PERMISSION,
        http_status=403,
    )
    result = classify_agent_task_inventory(inventory, now=NOW)
    assert result.blocking is None
    assert result.failure_category is FailureCategory.PERMISSION
    assert result.http_status == 403
    assert result.failure_source == "agent-task-lifecycle"


def test_classify_agent_task_inventory_expires_only_after_75_minutes() -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=(NOW - timedelta(minutes=75)).isoformat(),
    )
    boundary = classify_agent_task_inventory(AgentTaskInventory((task,)), now=NOW)
    expired = classify_agent_task_inventory(
        AgentTaskInventory(
            (
                AgentTaskLifecycle(
                    **{
                        **task.__dict__,
                        "created_at": (NOW - timedelta(minutes=75, seconds=1)).isoformat(),
                    }
                ),
            )
        ),
        now=NOW,
    )

    assert boundary.blocking is True
    assert boundary.expired is False
    assert expired.blocking is False
    assert expired.expired is True


def test_classify_agent_task_inventory_preserves_newer_session_after_task_expiry() -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=(NOW - timedelta(hours=3)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="in_progress",
                started_at=(NOW - timedelta(minutes=10)).isoformat(),
            ),
        ),
    )

    result = classify_agent_task_inventory(AgentTaskInventory((task,)), now=NOW)

    assert result.blocking is True
    assert result.expired is False
    assert result.since == NOW - timedelta(minutes=10)


def test_classify_agent_task_inventory_ignores_scoped_incomplete_expired_task() -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=(NOW - timedelta(hours=2)).isoformat(),
    )

    result = classify_agent_task_inventory(
        AgentTaskInventory((task,), complete=False, incomplete_reasons=("task-detail:task-1",)),
        now=NOW,
    )

    assert result.blocking is False
    assert result.expired is True
    assert result.reason == "expired-incomplete-task"


def test_classify_agent_task_inventory_keeps_unscoped_incomplete_unknown() -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="in_progress",
        created_at=(NOW - timedelta(hours=2)).isoformat(),
    )

    result = classify_agent_task_inventory(
        AgentTaskInventory((task,), complete=False, incomplete_reasons=("page-limit",)),
        now=NOW,
    )

    assert result.blocking is None
    assert result.expired is True
    assert result.reason == "incomplete-inventory"
