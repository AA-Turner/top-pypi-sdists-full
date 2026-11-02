"""Tests for normalizing provider Agent Task detail and session records."""

from agentic_devtools.cli.ci.agent_task_lifecycle import (
    AgentTaskLifecycle,
    _map_agent_task_lifecycle_detail,
)


def _map(task: dict, detail: dict) -> tuple[AgentTaskLifecycle, tuple[str, ...]]:
    return _map_agent_task_lifecycle_detail(
        task,
        detail,
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        task_pr_number=42,
        head_branch="copilot/pr-42",
    )


def test_maps_task_aliases_and_nested_session_clocks() -> None:
    lifecycle, reasons = _map(
        {},
        {
            "started_at": "malformed",
            "startedAt": "2026-10-16T09:00:00Z",
            "idle_at": "2026-10-16T09:05:00Z",
            "idleAt": "2026-10-16T09:10:00Z",
            "idle_since": "2026-10-16T09:15:00Z",
            "idleSince": "2099-10-16T09:20:00Z",
            "sessions": [{"id": "session-1", "startedAt": "2026-10-16T08:00:00Z"}],
        },
    )

    assert lifecycle.started_at == "2026-10-16T09:00:00Z"
    assert lifecycle.idle_at == "2099-10-16T09:20:00Z"
    assert lifecycle.sessions[0].started_at == "2026-10-16T08:00:00Z"
    assert reasons == ()


def test_maps_task_clock_aliases_from_metadata_and_summary_fallback() -> None:
    lifecycle, reasons = _map(
        {"idleSince": "2026-10-16T09:30:00Z"},
        {"metadata": {"state": "running", "startedAt": "2026-10-16T09:00:00Z"}, "sessions": []},
    )

    assert lifecycle.state == "running"
    assert lifecycle.started_at == "2026-10-16T09:00:00Z"
    assert lifecycle.idle_at == "2026-10-16T09:30:00Z"
    assert reasons == ()


def test_does_not_promote_update_or_completion_clocks_to_activity() -> None:
    lifecycle, reasons = _map(
        {},
        {
            "updatedAt": "2026-10-16T09:30:00Z",
            "completedAt": "2026-10-16T09:45:00Z",
        },
    )

    assert lifecycle.started_at == ""
    assert lifecycle.idle_at == ""
    assert reasons == ()


def test_preserves_top_level_singleton_session_and_creation_fallback() -> None:
    lifecycle, reasons = _map(
        {"createdAt": "2026-10-16T08:00:00Z"},
        {"sessionId": "session-1", "startedAt": "2026-10-16T09:00:00Z"},
    )

    assert lifecycle.created_at == "2026-10-16T08:00:00Z"
    assert lifecycle.started_at == "2026-10-16T09:00:00Z"
    assert len(lifecycle.sessions) == 1
    assert lifecycle.sessions[0].session_id == "session-1"
    assert lifecycle.sessions[0].created_at == ""
    assert reasons == ()


def test_preserves_task_scoped_malformed_and_missing_session_diagnostics() -> None:
    lifecycle, reasons = _map({}, {"sessions": [None, {}, {"state": "running"}]})

    assert len(lifecycle.sessions) == 1
    assert lifecycle.sessions[0].session_id == ""
    assert lifecycle.sessions[0].state == "running"
    assert reasons == ("malformed-session:task-1", "missing-session-id:task-1", "missing-session-id:task-1")
    malformed, malformed_reasons = _map({}, {"sessions": {"bad": "shape"}})

    assert malformed.sessions == ()
    assert malformed_reasons == ("malformed-session:task-1",)
