"""Tests for TrustedControlPlaneClock implementations."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.ci.reconciliation.clock import (
    ClockSnapshot,
    DeterministicTrustedControlPlaneClock,
    ElapsedReference,
    SystemTrustedControlPlaneClock,
    parse_utc_z,
    remaining_seconds,
    serialize_utc_z,
)


def test_serialize_and_parse_roundtrip() -> None:
    value = datetime(2026, 9, 15, 12, 0, tzinfo=UTC)
    serialized = serialize_utc_z(value)
    assert serialized.endswith("Z")
    assert parse_utc_z(serialized) == value


def test_serialize_rejects_naive_datetime() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        serialize_utc_z(datetime(2026, 9, 15, 12, 0))


def test_parse_requires_trailing_z() -> None:
    with pytest.raises(ValueError, match="end with 'Z'"):
        parse_utc_z("2026-09-15T12:00:00+00:00")


def test_deterministic_clock_advance_and_remaining_seconds() -> None:
    clock = DeterministicTrustedControlPlaneClock(utc_now=datetime(2026, 9, 15, 12, 0, tzinfo=UTC), monotonic_now=10.0)
    anchor = ElapsedReference(anchor_utc_z=clock.now_utc_z(), anchor_monotonic_seconds=10.0)
    clock.advance(seconds=30)
    remaining = remaining_seconds(
        deadline_utc_z="2026-09-15T12:01:00Z",
        now=clock.snapshot(),
        anchor=anchor,
    )
    assert remaining == pytest.approx(30.0)


def test_remaining_seconds_returns_none_for_clock_discontinuity() -> None:
    now = ClockSnapshot(utc_now=datetime(2026, 9, 15, 11, 59, tzinfo=UTC), monotonic_now=5.0)
    anchor = ElapsedReference(anchor_utc_z="2026-09-15T12:00:00Z", anchor_monotonic_seconds=10.0)
    assert remaining_seconds(deadline_utc_z="2026-09-15T12:30:00Z", now=now, anchor=anchor) is None


def test_remaining_seconds_returns_none_for_negative_elapsed_monotonic() -> None:
    now = ClockSnapshot(utc_now=datetime(2026, 9, 15, 12, 1, tzinfo=UTC), monotonic_now=5.0)
    anchor = ElapsedReference(anchor_utc_z="2026-09-15T12:00:00Z", anchor_monotonic_seconds=10.0)
    assert remaining_seconds(deadline_utc_z="2026-09-15T12:30:00Z", now=now, anchor=anchor) is None


def test_system_clock_snapshot_is_timezone_aware() -> None:
    clock = SystemTrustedControlPlaneClock()
    snapshot = clock.snapshot()
    assert snapshot.utc_now.tzinfo is not None
    assert clock.now_utc_z().endswith("Z")


def test_deterministic_clock_validates_inputs() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        DeterministicTrustedControlPlaneClock(utc_now=datetime(2026, 9, 15, 12, 0))

    clock = DeterministicTrustedControlPlaneClock(utc_now=datetime(2026, 9, 15, 12, 0, tzinfo=UTC))
    with pytest.raises(ValueError, match=">= 0"):
        clock.advance(seconds=-1)
