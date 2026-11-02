"""Tests for timeline outcomes newer than a terminal Agent Task."""

from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState, _newer_timeline_state


@pytest.mark.parametrize(
    ("events", "terminal_at"),
    [
        (None, "2026-01-01T00:00:00Z"),
        ([], None),
        ([], object()),
    ],
    ids=["missing-events", "missing-terminal-time", "invalid-terminal-time-type"],
)
def test_returns_none_when_events_or_terminal_time_are_unusable(events: object, terminal_at: object) -> None:
    assert _newer_timeline_state(events, terminal_at) is None  # type: ignore[arg-type]


def test_returns_none_for_invalid_terminal_timestamp() -> None:
    assert _newer_timeline_state([], "not-a-timestamp") is None


@pytest.mark.parametrize(
    ("event_id", "event_type", "created_at"),
    [
        (None, "copilot_work_started", "2026-01-01T00:02:00Z"),
        (True, "copilot_work_started", "2026-01-01T00:02:00Z"),
        (0, "copilot_work_started", "2026-01-01T00:02:00Z"),
        (1, "other", "2026-01-01T00:02:00Z"),
        (1, "copilot_work_started", None),
        (1, "copilot_work_started", "not-a-timestamp"),
    ],
    ids=["missing-id", "boolean-id", "nonpositive-id", "unknown-event", "missing-time", "invalid-time"],
)
def test_ignores_malformed_timeline_events(event_id: object, event_type: str, created_at: object) -> None:
    event = SimpleNamespace(id=event_id, event=event_type, created_at=created_at)

    assert _newer_timeline_state([event], "2026-01-01T00:00:00Z") is None  # type: ignore[list-item]


def test_ignores_timeline_events_not_newer_than_terminal_task() -> None:
    event = SimpleNamespace(
        id=10,
        event="copilot_work_started",
        created_at="2026-01-01T00:00:00Z",
    )

    assert _newer_timeline_state([event], "2026-01-01T00:00:00Z") is None


@pytest.mark.parametrize(
    ("event_type", "expected"),
    [
        ("copilot_work_started", SessionState(SessionOutcome.ACTIVE)),
        ("copilot_work_finished", SessionState(SessionOutcome.FINISHED)),
        (
            "copilot_work_finished_failure",
            SessionState(SessionOutcome.FAILED, 10, None, "2026-01-01T00:02:00"),
        ),
    ],
    ids=["active", "finished", "failed"],
)
def test_maps_newer_timeline_event(
    event_type: str,
    expected: SessionState,
) -> None:
    event = SimpleNamespace(
        id=10,
        event=event_type,
        created_at="2026-01-01T00:02:00",
    )

    assert _newer_timeline_state([event], "2026-01-01T00:01:00") == expected
