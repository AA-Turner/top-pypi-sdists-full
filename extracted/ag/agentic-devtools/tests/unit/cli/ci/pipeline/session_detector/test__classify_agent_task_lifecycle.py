"""Tests for ordering task and session lifecycle evidence."""

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.models import AgentTaskLifecycle, AgentTaskSessionLifecycle
from agentic_devtools.cli.ci.pipeline.session_detector import _classify_agent_task_lifecycle

NOW = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)


def test_newer_active_session_blocks_even_when_task_is_terminal() -> None:
    """A newer session remains visible when the terminal task has no updatedAt."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="failed",
        created_at=(NOW - timedelta(minutes=90)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="failed",
                started_at=(NOW - timedelta(minutes=85)).isoformat(),
            ),
            AgentTaskSessionLifecycle(
                session_id="session-2",
                state="in_progress",
                started_at=(NOW - timedelta(minutes=5)).isoformat(),
            ),
        ),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is True
    assert result.since == NOW - timedelta(minutes=5)


def test_failed_session_and_later_new_start_are_not_collapsed_by_task_id() -> None:
    """Distinct session identities are classified independently under one task."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="completed",
        created_at=(NOW - timedelta(minutes=90)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="failed",
                started_at=(NOW - timedelta(minutes=85)).isoformat(),
            ),
            AgentTaskSessionLifecycle(
                session_id="session-2",
                state="running",
                started_at=(NOW - timedelta(minutes=10)).isoformat(),
            ),
        ),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is True
    assert result.since == NOW - timedelta(minutes=10)


def test_idle_transition_restarts_the_75_minute_clock() -> None:
    """Uses the newest real idle-transition timestamp rather than task heartbeat time."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="idle",
        created_at=(NOW - timedelta(minutes=100)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="idle",
                started_at=(NOW - timedelta(minutes=90)).isoformat(),
                idle_at=(NOW - timedelta(minutes=20)).isoformat(),
            ),
        ),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is True
    assert result.since == NOW - timedelta(minutes=20)


def test_task_creation_does_not_override_an_available_session_clock() -> None:
    """Task creation is not allowed to override an available session clock."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="running",
        created_at=(NOW - timedelta(minutes=5)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-old",
                state="idle",
                started_at=(NOW - timedelta(minutes=90)).isoformat(),
            ),
        ),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is False
    assert result.expired is True


def test_unusable_clock_for_active_session_remains_unknown() -> None:
    """Does not expire a session when all durable clocks are absent."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="completed",
        created_at="",
        sessions=(AgentTaskSessionLifecycle(session_id="session-1", state="in_progress"),),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is None
    assert result.expired is False


def test_terminal_session_idle_clock_takes_precedence_for_active_parent() -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="idle",
        created_at=(NOW - timedelta(minutes=90)).isoformat(),
        started_at=(NOW - timedelta(minutes=90)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="completed",
                started_at=(NOW - timedelta(minutes=85)).isoformat(),
                idle_at=(NOW - timedelta(minutes=5)).isoformat(),
            ),
        ),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is True
    assert result.expired is False
    assert result.since == NOW - timedelta(minutes=5)


def test_recent_creation_only_session_prevents_expiring_an_old_task() -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="in_progress",
        created_at=(NOW - timedelta(minutes=90)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="in_progress",
                created_at=(NOW - timedelta(minutes=5)).isoformat(),
            ),
        ),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is True
    assert result.expired is False
    assert result.since == NOW - timedelta(minutes=5)


def test_newest_creation_only_session_wins_over_an_older_start() -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="in_progress",
        created_at=(NOW - timedelta(minutes=100)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-old",
                state="idle",
                started_at=(NOW - timedelta(minutes=90)).isoformat(),
                created_at=(NOW - timedelta(minutes=1)).isoformat(),
            ),
            AgentTaskSessionLifecycle(
                session_id="session-new",
                state="in_progress",
                created_at=(NOW - timedelta(minutes=5)).isoformat(),
            ),
        ),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is True
    assert result.since == NOW - timedelta(minutes=5)


@pytest.mark.parametrize("clock_field", ["started_at", "idle_at"])
def test_newer_task_activity_wins_over_older_session_activity(clock_field: str) -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="running",
        created_at=(NOW - timedelta(minutes=100)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="running",
                started_at=(NOW - timedelta(minutes=90)).isoformat(),
            ),
        ),
        **{clock_field: (NOW - timedelta(minutes=5)).isoformat()},
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is True
    assert result.since == NOW - timedelta(minutes=5)


def test_far_future_task_activity_remains_valid_and_defers_expiry() -> None:
    future = datetime(9999, 1, 1, tzinfo=UTC)
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="running",
        created_at=(NOW - timedelta(minutes=100)).isoformat(),
        started_at=future.isoformat(),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is True
    assert result.expired is False
    assert result.since == future


def test_task_creation_remains_final_fallback_without_lifecycle_clocks() -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="running",
        created_at=(NOW - timedelta(minutes=5)).isoformat(),
    )

    result = _classify_agent_task_lifecycle(task, first_observed_at={}, now=NOW)

    assert result.blocking is True
    assert result.since == NOW - timedelta(minutes=5)
