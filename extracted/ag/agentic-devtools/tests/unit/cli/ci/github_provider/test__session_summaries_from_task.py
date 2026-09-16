"""Tests for _session_summaries_from_task."""

from agentic_devtools.cli.ci.github_provider import _session_summaries_from_task


def test_returns_completed_session_summaries() -> None:
    """Builds summaries from nested completed sessions."""
    task = {
        "id": "task-1",
        "status": "completed",
        "sessions": [
            {
                "id": "session-1",
                "state": "completed",
                "startedAt": "2026-01-02T00:00:00Z",
                "completedAt": "2026-01-02T01:00:00Z",
                "summary": "Finished.",
            }
        ],
    }

    result = _session_summaries_from_task(task, 42)

    assert len(result) == 1
    assert result[0].task_id == "task-1"
    assert result[0].completed_at == "2026-01-02T01:00:00Z"


def test_uses_task_as_session_and_skips_invalid_tasks_or_sessions() -> None:
    """Handles task-level records and rejects incomplete or malformed records."""
    assert _session_summaries_from_task({"id": "task-1", "status": "running"}, 42) == []
    assert _session_summaries_from_task({"id": 1, "status": "completed"}, 42) == []
    assert (
        _session_summaries_from_task(
            {
                "id": "task-1",
                "state": "completed",
                "session_id": "session-1",
                "created_at": "2026-01-02T00:00:00Z",
                "output": "Finished.",
            },
            42,
        )[0].finishing_text
        == "Finished."
    )
    assert (
        _session_summaries_from_task(
            {"id": "task-1", "status": "completed", "sessions": [None, {}]},
            42,
        )
        == []
    )


def test_filters_sessions_by_their_own_status() -> None:
    """Includes only completed sessions and preserves each session's status."""
    task = {
        "id": "task-1",
        "status": "failed",
        "sessions": [
            {"id": "session-1", "state": "completed", "startedAt": "2026-01-02T00:00:00Z"},
            {"id": "session-2", "status": "failed", "startedAt": "2026-01-02T02:00:00Z"},
        ],
    }

    result = _session_summaries_from_task(task, 42)

    assert len(result) == 1
    assert result[0].session_id == "session-1"
    assert result[0].status == "completed"


def test_skips_completed_sessions_without_start_time() -> None:
    """Skips completed sessions that do not provide a start timestamp."""
    task = {
        "id": "task-1",
        "sessions": [{"id": "session-1", "state": "completed"}],
    }

    assert _session_summaries_from_task(task, 42) == []
