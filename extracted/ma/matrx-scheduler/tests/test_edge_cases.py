"""Edge-case tests for cron + next_due."""

from __future__ import annotations

from datetime import datetime, timezone

from matrx_scheduler.cron_helpers import next_n_fires, validate_cron
from matrx_scheduler.next_due import compute_next_due_at


# ── Malformed inputs ───────────────────────────────────────────────────────


def test_interval_non_numeric_returns_none():
    assert (
        compute_next_due_at(
            "interval",
            {"every_seconds": "abc"},
            now=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        is None
    )


def test_interval_zero_returns_none():
    assert compute_next_due_at("interval", {"every_seconds": 0}) is None


def test_interval_negative_returns_none():
    assert compute_next_due_at("interval", {"every_seconds": -10}) is None


def test_one_shot_naive_datetime_treated_as_utc():
    """A bare ISO string without tz suffix is parsed as naive then forced to UTC."""
    out = compute_next_due_at("one-shot", {"at": "2030-01-01T12:00:00"})
    assert out is not None
    assert out.tzinfo is not None


def test_one_shot_malformed_returns_none():
    assert compute_next_due_at("one-shot", {"at": "not a date"}) is None


# ── Cron edge cases ────────────────────────────────────────────────────────


def test_cron_dst_spring_forward_la():
    """
    2026-03-08 02:00 → 03:00 LA. A cron at '0 2 * * *' has no 02:00 that day
    in LA; croniter should fire at the next valid time.
    """
    # Just before spring-forward.
    fires = next_n_fires(
        "0 2 * * *",
        "America/Los_Angeles",
        3,
        datetime(2026, 3, 7, 12, 0, 0, tzinfo=timezone.utc),
    )
    assert len(fires) == 3
    # Each fire must be unique and in order.
    for a, b in zip(fires, fires[1:]):
        assert a < b


def test_cron_dst_fall_back_la():
    """
    2026-11-01 02:00 → 01:00 LA. Should fire once at 02:00, not duplicate.
    """
    fires = next_n_fires(
        "0 2 * * *",
        "America/Los_Angeles",
        3,
        datetime(2026, 10, 31, 0, 0, 0, tzinfo=timezone.utc),
    )
    assert len(fires) == 3
    for a, b in zip(fires, fires[1:]):
        assert a < b


def test_cron_every_minute():
    fires = next_n_fires(
        "* * * * *",
        "UTC",
        5,
        datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc),
    )
    assert len(fires) == 5
    for a, b in zip(fires, fires[1:]):
        delta = (b - a).total_seconds()
        assert 30 < delta <= 120  # roughly one minute apart


def test_validate_cron_empty_string():
    assert validate_cron("", "UTC") is not None


def test_validate_cron_too_many_fields():
    # croniter typically rejects 7-field cron
    out = validate_cron("0 0 0 0 0 0 0", "UTC")
    assert out is not None


# ── Heartbeat ──────────────────────────────────────────────────────────────


def test_heartbeat_advances_by_seconds():
    now = datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)
    out = compute_next_due_at("heartbeat", {"every_seconds": 90}, now=now)
    assert out is not None
    assert (out - now).total_seconds() == 90


# ── Future trigger types ───────────────────────────────────────────────────


def test_future_trigger_types_event_driven():
    for typ in ("event", "manual", "dependency", "context-match"):
        assert compute_next_due_at(typ, {}) is None
