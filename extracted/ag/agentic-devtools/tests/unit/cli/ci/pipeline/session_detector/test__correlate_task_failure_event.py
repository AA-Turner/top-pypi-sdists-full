"""Tests for correlating failed tasks with their timeline event."""

from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.models import (
    COPILOT_SESSION_EVENT_FINISHED,
    COPILOT_SESSION_EVENT_FINISHED_FAILURE,
    COPILOT_SESSION_EVENT_STARTED,
)
from agentic_devtools.cli.ci.pipeline.session_detector import _correlate_task_failure_event


@pytest.mark.parametrize(
    ("task_created_at", "failure_created_at"),
    [
        (None, "2026-01-01T00:02:00Z"),
        ("invalid", "2026-01-01T00:02:00Z"),
        ("2026-01-01T00:00:00Z", "invalid"),
        ("2026-01-01T00:03:00Z", "2026-01-01T00:02:00Z"),
        ("2026-01-01T00:00:00Z", 42),
    ],
)
def test_returns_none_without_a_valid_task_lifetime(task_created_at, failure_created_at) -> None:
    events = [SimpleNamespace(id=42, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2026-01-01T00:01:00Z")]

    assert _correlate_task_failure_event(task_created_at, failure_created_at, events) is None


def test_returns_latest_failure_event_within_task_lifetime() -> None:
    events = [
        SimpleNamespace(id=42, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2026-01-01T00:01:00Z"),
        SimpleNamespace(id=43, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2026-01-01T00:02:00"),
        SimpleNamespace(id=44, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2026-01-01T00:03:00Z"),
        SimpleNamespace(id=45, event=COPILOT_SESSION_EVENT_FINISHED, created_at="2026-01-01T00:01:30Z"),
        SimpleNamespace(id=True, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2026-01-01T00:01:30Z"),
        SimpleNamespace(id=0, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2026-01-01T00:01:30Z"),
        SimpleNamespace(
            id=46,
            event=COPILOT_SESSION_EVENT_FINISHED_FAILURE,
            created_at="invalid",
        ),
        SimpleNamespace(
            id=47,
            event=COPILOT_SESSION_EVENT_FINISHED_FAILURE,
            created_at=None,
        ),
    ]

    assert _correlate_task_failure_event(
        "2026-01-01T00:00:00",
        "2026-01-01T00:02:00",
        events,
    ) == (43, "2026-01-01T00:02:00")


@pytest.mark.parametrize(
    "started_at",
    ["2026-01-01T00:00:00Z", "2026-01-01T00:00:00", "invalid"],
    ids=["aware-start", "naive-start", "malformed-start"],
)
def test_correlates_latest_timeline_failure_when_task_failure_time_is_missing(started_at: str) -> None:
    events = [
        SimpleNamespace(id=41, event=COPILOT_SESSION_EVENT_STARTED, created_at=started_at),
        SimpleNamespace(id=42, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2026-01-01T00:02:00"),
    ]

    assert _correlate_task_failure_event(
        "2026-01-01T00:01:00Z",
        None,
        events,
    ) == (42, "2026-01-01T00:02:00")


@pytest.mark.parametrize(
    "events",
    [
        [],
        [
            SimpleNamespace(id=42, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2026-01-01T00:02:00Z"),
            SimpleNamespace(id=43, event=COPILOT_SESSION_EVENT_STARTED, created_at="2026-01-01T00:03:00Z"),
        ],
        [
            SimpleNamespace(id=42, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="invalid"),
        ],
        [
            SimpleNamespace(id=42, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2025-12-31T23:59:00Z"),
        ],
        [SimpleNamespace(id=42, event=COPILOT_SESSION_EVENT_STARTED, created_at="2025-12-31T23:59:00Z")],
    ],
    ids=["empty", "later-start", "malformed-latest", "failure-before-task", "start-before-task"],
)
def test_does_not_infer_failure_from_incomplete_timeline(events) -> None:
    assert _correlate_task_failure_event("2026-01-01T00:00:00Z", None, events) is None


def test_returns_none_when_no_timeline_failure_occurs_during_task() -> None:
    events = [
        SimpleNamespace(id=42, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2025-12-31T23:59:00Z"),
        SimpleNamespace(id=43, event=COPILOT_SESSION_EVENT_FINISHED_FAILURE, created_at="2026-01-01T00:03:00Z"),
    ]

    assert (
        _correlate_task_failure_event(
            "2026-01-01T00:00:00Z",
            "2026-01-01T00:02:00Z",
            events,
        )
        is None
    )
