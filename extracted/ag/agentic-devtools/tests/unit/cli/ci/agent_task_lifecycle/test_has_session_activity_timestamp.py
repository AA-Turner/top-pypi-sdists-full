"""Tests for detecting parseable session activity timestamps."""

from agentic_devtools.cli.ci.agent_task_lifecycle import has_session_activity_timestamp


def test_requires_parseable_activity_but_keeps_valid_aliases() -> None:
    assert not has_session_activity_timestamp({"startedAt": "invalid"})
    assert has_session_activity_timestamp({"started_at": "invalid", "startedAt": "2026-10-16T09:55:00Z"})
    assert has_session_activity_timestamp({"idleSince": "2026-10-16T09:55:00Z"})
    assert has_session_activity_timestamp(
        {"startedAt": "invalid"},
        fallback={"idleSince": "2026-10-16T09:55:00Z"},
    )
    assert not has_session_activity_timestamp({"createdAt": "2026-10-16T09:55:00Z"})
