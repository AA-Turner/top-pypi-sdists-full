"""Tests for selecting task and session lifecycle clocks."""

from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.agent_task_lifecycle import (
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
    select_task_lifecycle_timestamp,
)

NOW = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)


def _task(
    *,
    started_at: str = "",
    idle_at: str = "",
    sessions: tuple[AgentTaskSessionLifecycle, ...] = (),
) -> AgentTaskLifecycle:
    return AgentTaskLifecycle(
        "task",
        "owner/repo",
        42,
        "branch",
        "running",
        "",
        sessions=sessions,
        started_at=started_at,
        idle_at=idle_at,
    )


def test_newer_task_start_wins_over_older_session_activity() -> None:
    task = _task(
        started_at=(NOW - timedelta(minutes=5)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                "session",
                "running",
                started_at=(NOW - timedelta(minutes=90)).isoformat(),
            ),
        ),
    )

    assert select_task_lifecycle_timestamp(task) == NOW - timedelta(minutes=5)


def test_newer_task_idle_wins_over_older_session_activity() -> None:
    task = _task(
        idle_at=(NOW - timedelta(minutes=5)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                "session",
                "running",
                idle_at=(NOW - timedelta(minutes=90)).isoformat(),
            ),
        ),
    )

    assert select_task_lifecycle_timestamp(task) == NOW - timedelta(minutes=5)


def test_newer_session_clock_wins_over_task_activity() -> None:
    task = _task(
        started_at=(NOW - timedelta(minutes=90)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                "session",
                "running",
                created_at=(NOW - timedelta(minutes=5)).isoformat(),
            ),
        ),
    )

    assert select_task_lifecycle_timestamp(task) == NOW - timedelta(minutes=5)


def test_session_creation_is_fallback_only_for_session_without_activity() -> None:
    task = _task(
        sessions=(
            AgentTaskSessionLifecycle(
                "session",
                "running",
                started_at="invalid",
                created_at=(NOW - timedelta(minutes=5)).isoformat(),
            ),
        ),
    )

    assert select_task_lifecycle_timestamp(task) == NOW - timedelta(minutes=5)


def test_invalid_task_and_session_clocks_have_no_selected_clock() -> None:
    task = _task(
        started_at="invalid",
        idle_at="",
        sessions=(AgentTaskSessionLifecycle("session", "running"),),
    )

    assert select_task_lifecycle_timestamp(task) is None


def test_task_creation_is_not_promoted_to_activity() -> None:
    task = AgentTaskLifecycle("task", "owner/repo", 42, "branch", "running", NOW.isoformat())

    assert select_task_lifecycle_timestamp(task) is None
