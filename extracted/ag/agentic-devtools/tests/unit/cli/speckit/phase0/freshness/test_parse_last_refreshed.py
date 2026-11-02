"""Tests for parse_last_refreshed in speckit/phase0/freshness.py (FR-007b)."""

from __future__ import annotations

from datetime import UTC, datetime

from agentic_devtools.cli.speckit.phase0.freshness import parse_last_refreshed


class TestParseLastRefreshed:
    """Tests for the parse_last_refreshed function."""

    def test_valid_past_timestamp(self) -> None:
        now = datetime(2026, 6, 1, tzinfo=UTC)
        result = parse_last_refreshed("2026-01-01T00:00:00Z", now=now)
        assert result == datetime(2026, 1, 1, tzinfo=UTC)

    def test_missing_value_is_none(self) -> None:
        now = datetime(2026, 6, 1, tzinfo=UTC)
        assert parse_last_refreshed(None, now=now) is None

    def test_non_string_value_is_none(self) -> None:
        now = datetime(2026, 6, 1, tzinfo=UTC)
        assert parse_last_refreshed(12345, now=now) is None

    def test_malformed_string_is_none(self) -> None:
        now = datetime(2026, 6, 1, tzinfo=UTC)
        assert parse_last_refreshed("not-a-timestamp", now=now) is None

    def test_future_timestamp_is_none(self) -> None:
        now = datetime(2026, 6, 1, tzinfo=UTC)
        assert parse_last_refreshed("2026-12-01T00:00:00Z", now=now) is None

    def test_date_only_value_is_none(self) -> None:
        now = datetime(2026, 6, 1, tzinfo=UTC)
        assert parse_last_refreshed("2026-01-01", now=now) is None

    def test_naive_timestamp_is_treated_as_utc(self) -> None:
        now = datetime(2026, 6, 1, tzinfo=UTC)
        result = parse_last_refreshed("2026-01-01T00:00:00", now=now)
        assert result == datetime(2026, 1, 1, tzinfo=UTC)

    def test_space_separated_timestamp_is_treated_as_utc(self) -> None:
        now = datetime(2026, 6, 1, tzinfo=UTC)
        result = parse_last_refreshed("2026-01-01 00:00:00", now=now)
        assert result == datetime(2026, 1, 1, tzinfo=UTC)

    def test_unusable_offset_that_overflows_utc_conversion_is_none(self) -> None:
        now = datetime(2026, 6, 1, tzinfo=UTC)
        assert parse_last_refreshed("0001-01-01T00:00:00+23:59", now=now) is None
