"""Tests for format_rfc3339_utc in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone

from agentic_devtools.cli.speckit.phase0.identifiers import format_rfc3339_utc


class TestFormatRfc3339Utc:
    """Tests for the format_rfc3339_utc function."""

    def test_utc_datetime(self) -> None:
        dt = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
        assert format_rfc3339_utc(dt) == "2026-01-02T03:04:05Z"

    def test_naive_datetime_is_treated_as_utc(self) -> None:
        dt = datetime(2026, 1, 2, 3, 4, 5)
        assert format_rfc3339_utc(dt) == "2026-01-02T03:04:05Z"

    def test_non_utc_timezone_is_converted(self) -> None:
        tz = timezone(timedelta(hours=-5))
        dt = datetime(2026, 1, 2, 3, 4, 5, tzinfo=tz)
        assert format_rfc3339_utc(dt) == "2026-01-02T08:04:05Z"

    def test_drops_sub_second_precision(self) -> None:
        dt = datetime(2026, 1, 2, 3, 4, 5, 999999, tzinfo=UTC)
        assert format_rfc3339_utc(dt) == "2026-01-02T03:04:05Z"
