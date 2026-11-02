"""Tests for normalizing an individual Agent Task session record."""

from agentic_devtools.cli.ci.agent_task_lifecycle import (
    AgentTaskSessionLifecycle,
    _map_agent_task_lifecycle_session,
)


def test_maps_nested_session_identity_and_state() -> None:
    session, reasons = _map_agent_task_lifecycle_session(
        {},
        {"sessionId": "session-1", "state": "running", "runId": 42},
        task_id="task-1",
        task_state="queued",
        top_level_session_record=False,
    )

    assert session == AgentTaskSessionLifecycle("session-1", "running", workflow_run_id="42")
    assert reasons == ()


def test_maps_top_level_session_fallback_and_reports_missing_identity() -> None:
    session, reasons = _map_agent_task_lifecycle_session(
        {},
        {"startedAt": "2026-10-16T09:00:00Z"},
        task_id="task-1",
        task_state="running",
        top_level_session_record=True,
    )

    assert session == AgentTaskSessionLifecycle("", "running", started_at="2026-10-16T09:00:00Z")
    assert reasons == ("missing-session-id:task-1",)


def test_skips_empty_session_values_and_reports_malformed_record() -> None:
    empty, empty_reasons = _map_agent_task_lifecycle_session(
        {},
        {},
        task_id="task-1",
        task_state="",
        top_level_session_record=False,
    )
    malformed, malformed_reasons = _map_agent_task_lifecycle_session(
        {},
        None,
        task_id="task-1",
        task_state="",
        top_level_session_record=False,
    )

    assert empty is None
    assert empty_reasons == ("missing-session-id:task-1",)
    assert malformed is None
    assert malformed_reasons == ("malformed-session:task-1",)
