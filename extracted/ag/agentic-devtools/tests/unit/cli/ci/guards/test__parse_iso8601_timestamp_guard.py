"""Tests for _parse_iso8601_timestamp_guard() in guards."""

from datetime import timezone

from agentic_devtools.cli.ci.guards import _parse_iso8601_timestamp_guard


class TestParseIso8601TimestampGuard:
    """Tests for _parse_iso8601_timestamp_guard()."""

    def test_empty_string_returns_none(self) -> None:
        """An empty timestamp string returns None (fail-open)."""
        result = _parse_iso8601_timestamp_guard("")
        assert result is None

    def test_invalid_string_returns_none(self) -> None:
        """An unparseable string returns None."""
        result = _parse_iso8601_timestamp_guard("not-a-timestamp")
        assert result is None

    def test_timezone_aware_string_parses(self) -> None:
        """A valid UTC ISO 8601 string parses to a UTC-aware datetime."""
        result = _parse_iso8601_timestamp_guard("2024-06-01T12:00:00+00:00")
        assert result is not None
        assert result.tzinfo == timezone.utc

    def test_timezone_naive_string_is_normalised_to_utc(self) -> None:
        """A timezone-naive ISO 8601 string is treated as UTC."""
        result = _parse_iso8601_timestamp_guard("2024-06-01T12:00:00")
        assert result is not None
        assert result.tzinfo == timezone.utc
