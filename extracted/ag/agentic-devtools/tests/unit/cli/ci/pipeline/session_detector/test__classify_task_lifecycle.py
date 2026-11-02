"""Tests for classifying task and session lifecycle ages."""

from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.pipeline.session_detector import (
    _classify_task_lifecycle,
)

NOW = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)


def test_task_at_exact_75_minute_boundary_remains_blocking() -> None:
    """Does not expire a lifecycle at exactly 75 minutes."""
    result = _classify_task_lifecycle(
        "idle",
        lifecycle_at=None,
        created_at=(NOW - timedelta(minutes=75)).isoformat(),
        first_observed_at=None,
        now=NOW,
    )
    assert result.blocking is True
    assert result.expired is False


def test_task_over_75_minutes_expires() -> None:
    """Expires a lifecycle only after the 75-minute limit."""
    result = _classify_task_lifecycle(
        "running",
        lifecycle_at=(NOW - timedelta(minutes=75, microseconds=1)).isoformat(),
        created_at=None,
        first_observed_at=None,
        now=NOW,
    )
    assert result.blocking is False
    assert result.expired is True


def test_terminal_task_does_not_block_without_timestamps() -> None:
    """A known terminal state does not require an age timestamp."""
    result = _classify_task_lifecycle(
        "completed",
        lifecycle_at=None,
        created_at=None,
        first_observed_at=None,
        now=NOW,
    )
    assert result.blocking is False
    assert result.expired is False


def test_unknown_status_is_unknown() -> None:
    """Does not treat an unknown state as active or terminal."""
    result = _classify_task_lifecycle(
        "paused",
        lifecycle_at=None,
        created_at=None,
        first_observed_at=None,
        now=NOW,
    )
    assert result.blocking is None


def test_missing_status_is_unknown() -> None:
    """Requires a string lifecycle state."""
    result = _classify_task_lifecycle(
        None,
        lifecycle_at=None,
        created_at=None,
        first_observed_at=None,
        now=NOW,
    )
    assert result.blocking is None


def test_uses_creation_time_when_lifecycle_time_is_invalid() -> None:
    """Falls back to creation time when the session timestamp is unusable."""
    result = _classify_task_lifecycle(
        "idle",
        lifecycle_at="invalid",
        created_at=(NOW - timedelta(minutes=5)).isoformat(),
        first_observed_at=None,
        now=NOW,
    )
    assert result.blocking is True
    assert result.since == NOW - timedelta(minutes=5)


def test_uses_first_observed_time_when_provider_times_are_missing() -> None:
    """Uses the persisted first-observed time as the final age source."""
    result = _classify_task_lifecycle(
        "in_progress",
        lifecycle_at=None,
        created_at=None,
        first_observed_at=(NOW - timedelta(minutes=80)).isoformat(),
        now=NOW,
    )
    assert result.blocking is False
    assert result.expired is True


def test_missing_all_time_sources_remains_unknown() -> None:
    """Does not infer expiry when no durable lifecycle clock exists."""
    result = _classify_task_lifecycle(
        "idle",
        lifecycle_at=None,
        created_at=None,
        first_observed_at=None,
        now=NOW,
    )
    assert result.blocking is None
    assert result.expired is False


def test_future_lifecycle_timestamp_remains_blocking() -> None:
    """Treats a future provider timestamp conservatively as active."""
    result = _classify_task_lifecycle(
        "waiting",
        lifecycle_at=(NOW + timedelta(minutes=1)).isoformat(),
        created_at=None,
        first_observed_at=None,
        now=NOW,
    )
    assert result.blocking is True


def test_future_lifecycle_timestamp_is_unknown_for_incomplete_inventory() -> None:
    result = _classify_task_lifecycle(
        "waiting",
        lifecycle_at=(NOW + timedelta(minutes=1)).isoformat(),
        created_at=None,
        first_observed_at=None,
        now=NOW,
        future_is_unknown=True,
    )

    assert result.blocking is None
    assert result.reason == "future-lifecycle-clock"


def test_incomplete_future_clock_keeps_terminal_state_unknown() -> None:
    result = _classify_task_lifecycle(
        "completed",
        lifecycle_at=(NOW + timedelta(minutes=1)).isoformat(),
        created_at=None,
        first_observed_at=None,
        now=NOW,
        future_is_unknown=True,
    )

    assert result.blocking is None
    assert result.reason == "future-lifecycle-clock"


def test_active_status_is_case_insensitive() -> None:
    """Recognizes provider lifecycle states without case sensitivity."""
    result = _classify_task_lifecycle(
        "IDLE",
        lifecycle_at=None,
        created_at=NOW.isoformat(),
        first_observed_at=None,
        now=NOW,
    )
    assert result.blocking is True
