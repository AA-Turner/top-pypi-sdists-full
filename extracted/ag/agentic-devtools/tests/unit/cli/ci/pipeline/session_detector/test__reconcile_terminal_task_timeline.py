"""Tests for reconciling terminal Agent Tasks with timeline events."""

from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.models import (
    COPILOT_SESSION_EVENT_FINISHED,
    COPILOT_SESSION_EVENT_FINISHED_FAILURE,
    COPILOT_SESSION_EVENT_STARTED,
)
from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    _reconcile_terminal_task_timeline,
)


def test_uses_known_terminal_timestamp() -> None:
    event = SimpleNamespace(
        id=1,
        event=COPILOT_SESSION_EVENT_STARTED,
        created_at="2026-01-01T00:02:00Z",
    )

    assert _reconcile_terminal_task_timeline([event], None, "2026-01-01T00:01:00Z", "") == SessionState(
        SessionOutcome.ACTIVE
    )


@pytest.mark.parametrize(
    ("events", "created_at", "expected"),
    [
        (None, "2026-01-01T00:00:00Z", None),
        ([], "2026-01-01T00:00:00Z", None),
        ([], None, SessionState(SessionOutcome.UNKNOWN)),
        ([], "invalid", SessionState(SessionOutcome.UNKNOWN)),
    ],
    ids=["missing-events", "no-later-events", "missing-created-time", "invalid-created-time"],
)
def test_handles_missing_or_invalid_task_timeline_inputs(
    events: list[object] | None,
    created_at: object,
    expected: SessionState | None,
) -> None:
    assert _reconcile_terminal_task_timeline(events, created_at, None, COPILOT_SESSION_EVENT_FINISHED) == expected


@pytest.mark.parametrize(
    "event",
    [
        SimpleNamespace(id=None, event=COPILOT_SESSION_EVENT_FINISHED, created_at="2026-01-01T00:01:00Z"),
        SimpleNamespace(id=True, event=COPILOT_SESSION_EVENT_FINISHED, created_at="2026-01-01T00:01:00Z"),
        SimpleNamespace(id=0, event=COPILOT_SESSION_EVENT_FINISHED, created_at="2026-01-01T00:01:00Z"),
        SimpleNamespace(id=1, event="other", created_at="2026-01-01T00:01:00Z"),
        SimpleNamespace(id=1, event=COPILOT_SESSION_EVENT_FINISHED, created_at=None),
        SimpleNamespace(id=1, event=COPILOT_SESSION_EVENT_FINISHED, created_at="invalid"),
    ],
    ids=["missing-id", "boolean-id", "nonpositive-id", "unknown-event", "missing-time", "invalid-time"],
)
def test_ignores_malformed_or_unrelated_events(event: object) -> None:
    assert (
        _reconcile_terminal_task_timeline(
            [event],
            "2026-01-01T00:00:00Z",
            None,
            COPILOT_SESSION_EVENT_FINISHED,
        )
        is None
    )


def test_returns_unknown_when_event_order_is_ambiguous() -> None:
    event = SimpleNamespace(
        id=1,
        event=COPILOT_SESSION_EVENT_STARTED,
        created_at="2026-01-01T00:01:00Z",
    )

    assert _reconcile_terminal_task_timeline(
        [event],
        "2026-01-01T00:00:00Z",
        None,
        COPILOT_SESSION_EVENT_FINISHED,
    ) == SessionState(SessionOutcome.UNKNOWN)


def test_returns_unknown_when_task_terminal_conflicts_with_timeline() -> None:
    event = SimpleNamespace(
        id=1,
        event=COPILOT_SESSION_EVENT_FINISHED_FAILURE,
        created_at="2026-01-01T00:01:00Z",
    )

    assert _reconcile_terminal_task_timeline(
        [event],
        "2026-01-01T00:00:00Z",
        None,
        COPILOT_SESSION_EVENT_FINISHED,
    ) == SessionState(SessionOutcome.UNKNOWN)


def test_returns_newer_timeline_state_after_matching_terminal_event() -> None:
    events = [
        SimpleNamespace(
            id=1,
            event=COPILOT_SESSION_EVENT_FINISHED,
            created_at="2026-01-01T00:01:00",
        ),
        SimpleNamespace(
            id=2,
            event=COPILOT_SESSION_EVENT_STARTED,
            created_at="2026-01-01T00:02:00",
        ),
    ]

    assert _reconcile_terminal_task_timeline(
        events,
        "2026-01-01T00:00:00",
        None,
        COPILOT_SESSION_EVENT_FINISHED,
    ) == SessionState(SessionOutcome.ACTIVE)


@pytest.mark.parametrize(
    ("events", "created_at", "terminal_at"),
    [
        (None, "2026-01-01T00:00:00Z", "2026-01-01T00:02:00Z"),
        ([], None, "2026-01-01T00:02:00Z"),
        ([], "2026-01-01T00:00:00Z", None),
        ([], "invalid", "2026-01-01T00:02:00Z"),
        ([], "2026-01-01T00:03:00Z", "2026-01-01T00:02:00Z"),
    ],
    ids=["unavailable-timeline", "missing-created-time", "missing-terminal-time", "invalid-time", "reversed-time"],
)
def test_missing_outcome_fails_closed_when_task_timeline_cannot_be_correlated(
    events: list[object] | None,
    created_at: object,
    terminal_at: object,
) -> None:
    assert _reconcile_terminal_task_timeline(events, created_at, terminal_at, None) == SessionState(
        SessionOutcome.UNKNOWN
    )


def test_infers_missing_outcome_from_naive_timeline_timestamps() -> None:
    event = SimpleNamespace(
        id=42,
        event=COPILOT_SESSION_EVENT_FINISHED,
        created_at="2026-01-01T00:01:00",
    )

    assert _reconcile_terminal_task_timeline(
        [event],
        "2026-01-01T00:00:00",
        "2026-01-01T00:02:00",
        None,
        task_id="task-abc",
    ) == SessionState(SessionOutcome.FINISHED, task_id="task-abc")


def test_missing_outcome_ignores_malformed_terminal_event_timestamp() -> None:
    event = SimpleNamespace(
        id=42,
        event=COPILOT_SESSION_EVENT_FINISHED,
        created_at="invalid",
    )

    assert _reconcile_terminal_task_timeline(
        [event],
        "2026-01-01T00:00:00Z",
        "2026-01-01T00:02:00Z",
        None,
    ) == SessionState(SessionOutcome.UNKNOWN)
