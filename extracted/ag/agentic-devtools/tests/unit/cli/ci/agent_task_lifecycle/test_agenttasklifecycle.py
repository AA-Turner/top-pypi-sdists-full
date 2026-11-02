"""Tests for the AgentTaskLifecycle dataclass."""

from agentic_devtools.cli.ci.agent_task_lifecycle import AgentTaskLifecycle


def test_task_activity_fields_default_empty_without_changing_positional_arguments() -> None:
    task = AgentTaskLifecycle("task", "owner/repo", 42, "branch", "running", "created", (), "sha", "run")

    assert task.created_at == "created"
    assert task.sessions == ()
    assert task.head_sha == "sha"
    assert task.workflow_run_id == "run"
    assert task.started_at == ""
    assert task.idle_at == ""


def test_task_activity_fields_accept_typed_clock_values() -> None:
    task = AgentTaskLifecycle(
        "task",
        "owner/repo",
        42,
        "branch",
        "running",
        "created",
        started_at="2026-10-16T09:55:00Z",
        idle_at="2026-10-16T09:58:00Z",
    )

    assert task.started_at == "2026-10-16T09:55:00Z"
    assert task.idle_at == "2026-10-16T09:58:00Z"
