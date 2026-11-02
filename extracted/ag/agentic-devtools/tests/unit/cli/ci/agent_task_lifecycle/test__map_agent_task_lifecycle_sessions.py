"""Tests for mapping Agent Task session collections and their diagnostics."""

from agentic_devtools.cli.ci.agent_task_lifecycle import (
    AgentTaskSessionLifecycle,
    _map_agent_task_lifecycle_sessions,
)


def test_maps_nested_sessions_and_preserves_collection_diagnostics() -> None:
    sessions, reasons = _map_agent_task_lifecycle_sessions(
        {},
        {"sessions": [None, {"id": "session-1", "state": "running"}]},
        task_id="task-1",
        task_state="queued",
    )

    assert sessions == (AgentTaskSessionLifecycle("session-1", "running"),)
    assert reasons == ("malformed-session:task-1",)


def test_preserves_top_level_singleton_session_and_malformed_collection() -> None:
    singleton, singleton_reasons = _map_agent_task_lifecycle_sessions(
        {},
        {"startedAt": "2026-10-16T09:00:00Z"},
        task_id="task-1",
        task_state="running",
    )
    malformed, malformed_reasons = _map_agent_task_lifecycle_sessions(
        {},
        {"sessions": {"bad": "shape"}},
        task_id="task-1",
        task_state="",
    )

    assert singleton == (AgentTaskSessionLifecycle("", "running", started_at="2026-10-16T09:00:00Z"),)
    assert singleton_reasons == ("missing-session-id:task-1",)
    assert malformed == ()
    assert malformed_reasons == ("malformed-session:task-1",)
