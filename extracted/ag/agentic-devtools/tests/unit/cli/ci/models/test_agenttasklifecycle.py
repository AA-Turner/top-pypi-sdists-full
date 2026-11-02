"""Tests for AgentTaskLifecycle."""

from agentic_devtools.cli.ci.models import AgentTaskLifecycle, AgentTaskSessionLifecycle


def test_agent_task_lifecycle_preserves_task_and_session_evidence() -> None:
    """Stores repository, PR, branch, task, and nested session lifecycle fields."""
    session = AgentTaskSessionLifecycle(
        session_id="session-1",
        state="idle",
        started_at="2026-10-16T08:00:00Z",
        idle_at="2026-10-16T08:30:00Z",
    )
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/fix",
        state="idle",
        created_at="2026-10-16T07:00:00Z",
        sessions=(session,),
    )

    assert task.repository == "owner/repo"
    assert task.pr_number == 42
    assert task.head_branch == "copilot/fix"
    assert task.sessions == (session,)
