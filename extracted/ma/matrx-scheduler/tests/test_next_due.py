"""Frozen-time tests for compute_next_due_at."""

from __future__ import annotations

from datetime import datetime, timezone

from matrx_scheduler.next_due import compute_next_due_at


NOW = datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)


def test_one_shot_returns_at():
    out = compute_next_due_at(
        "one-shot", {"at": "2026-05-12T15:00:00Z"}, now=NOW
    )
    assert out is not None
    assert out.isoformat().startswith("2026-05-12T15:00:00")


def test_one_shot_invalid_returns_none():
    assert compute_next_due_at("one-shot", {}, now=NOW) is None


def test_interval_adds_seconds():
    out = compute_next_due_at("interval", {"every_seconds": 3600}, now=NOW)
    assert out == datetime(2026, 5, 10, 13, 0, 0, tzinfo=timezone.utc)


def test_heartbeat_treats_same_as_interval():
    out = compute_next_due_at("heartbeat", {"every_seconds": 60}, now=NOW)
    assert out == datetime(2026, 5, 10, 12, 1, 0, tzinfo=timezone.utc)


def test_interval_under_minimum_returns_none():
    assert compute_next_due_at("interval", {"every_seconds": 0}, now=NOW) is None


def test_cron_5_field_la():
    out = compute_next_due_at(
        "cron",
        {"expression": "0 9 * * 1-5", "tz": "America/Los_Angeles"},
        now=NOW,
    )
    assert out is not None
    # NOW is Sunday 2026-05-10 noon UTC → 5am PDT.
    # Next weekday 9am PDT = Mon 2026-05-11 09:00 PDT = 16:00 UTC.
    assert out == datetime(2026, 5, 11, 16, 0, 0, tzinfo=timezone.utc)


def test_context_match_returns_none():
    assert (
        compute_next_due_at("context-match", {"hostname": "github.com"}, now=NOW)
        is None
    )


def test_event_driven_returns_none():
    for typ in ("event", "manual", "dependency"):
        assert compute_next_due_at(typ, {}, now=NOW) is None
