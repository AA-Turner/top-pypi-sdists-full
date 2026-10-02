"""Tests for cron_helpers."""

from __future__ import annotations

from datetime import datetime, timezone

from matrx_scheduler.cron_helpers import (
    fire_count_in_window,
    next_n_fires,
    validate_cron,
)


def test_validate_cron_ok():
    assert validate_cron("0 9 * * 1-5", "America/Los_Angeles") is None
    assert validate_cron("*/15 * * * *", "UTC") is None


def test_validate_cron_bad_expression():
    out = validate_cron("not a cron", "UTC")
    assert out is not None
    assert "invalid" in out.lower()


def test_validate_cron_bad_tz():
    assert validate_cron("0 9 * * *", "Not/A/Zone") is not None


def test_next_n_returns_n_distinct():
    fires = next_n_fires(
        "0 9 * * 1-5",
        "UTC",
        n=5,
        start=datetime(2026, 5, 10, 0, 0, 0, tzinfo=timezone.utc),
    )
    assert len(fires) == 5
    assert all(f.tzinfo is not None for f in fires)
    # Monday May 11 → next Monday.
    assert fires[0].weekday() == 0
    # Must be strictly increasing.
    for a, b in zip(fires, fires[1:]):
        assert a < b


def test_fire_count_in_window():
    start = datetime(2026, 5, 11, 0, 0, 0, tzinfo=timezone.utc)  # Monday
    end = datetime(2026, 5, 18, 0, 0, 0, tzinfo=timezone.utc)  # next Monday
    # Mon–Fri at 09:00 UTC → 5 fires in the week.
    assert fire_count_in_window("0 9 * * 1-5", "UTC", start, end) == 5
