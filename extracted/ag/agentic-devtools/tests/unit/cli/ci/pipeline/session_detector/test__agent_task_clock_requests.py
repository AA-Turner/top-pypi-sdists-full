"""Tests for selecting usable lifecycle clock fallbacks."""

from agentic_devtools.cli.ci.models import AgentTaskLifecycle, AgentTaskSessionLifecycle
from agentic_devtools.cli.ci.pipeline.session_detector import _agent_task_clock_requests


def test_missing_creation_with_valid_session_clock_only_requests_unclocked_session():
    task = AgentTaskLifecycle(
        task_id="task",
        repository="owner/repo",
        pr_number=42,
        head_branch="branch",
        state="running",
        created_at="invalid",
        sessions=(
            AgentTaskSessionLifecycle(session_id="valid", state="running", started_at="2026-10-16T10:00:00Z"),
            AgentTaskSessionLifecycle(session_id="invalid", state="running", started_at="bad", idle_at="bad"),
        ),
    )

    assert _agent_task_clock_requests(task) == [("invalid", "invalid")]


def test_creation_only_session_does_not_request_first_observed_clock() -> None:
    task = AgentTaskLifecycle(
        task_id="task",
        repository="owner/repo",
        pr_number=42,
        head_branch="branch",
        state="running",
        created_at="invalid",
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="created",
                state="running",
                created_at="2026-10-16T10:00:00Z",
            ),
        ),
    )

    assert _agent_task_clock_requests(task) == []


def test_invalid_start_uses_valid_session_creation_without_fallback_request() -> None:
    task = AgentTaskLifecycle(
        task_id="task",
        repository="owner/repo",
        pr_number=42,
        head_branch="branch",
        state="running",
        created_at="invalid",
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="created",
                state="running",
                started_at="invalid",
                created_at="2026-10-16T10:00:00Z",
            ),
        ),
    )

    assert _agent_task_clock_requests(task) == []


def test_valid_task_activity_does_not_request_a_task_first_observed_clock() -> None:
    task = AgentTaskLifecycle(
        task_id="task",
        repository="owner/repo",
        pr_number=42,
        head_branch="branch",
        state="running",
        created_at="invalid",
        started_at="2026-10-16T10:00:00Z",
    )

    assert _agent_task_clock_requests(task) == []
