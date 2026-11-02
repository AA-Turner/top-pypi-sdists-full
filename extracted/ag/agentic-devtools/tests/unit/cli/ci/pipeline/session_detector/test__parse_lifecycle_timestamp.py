"""Tests for parsing provider lifecycle timestamps."""

from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.pipeline.session_detector import _parse_lifecycle_timestamp


def test_parses_zulu_timestamp_as_utc() -> None:
    """Parses a Z-suffixed lifecycle timestamp as UTC."""
    assert _parse_lifecycle_timestamp("2026-10-16T08:00:00Z") == datetime(2026, 10, 16, 8, tzinfo=UTC)


def test_normalizes_offset_timestamp_to_utc() -> None:
    """Normalizes an offset timestamp to UTC."""
    assert _parse_lifecycle_timestamp("2026-10-16T10:00:00+02:00") == datetime(2026, 10, 16, 8, tzinfo=UTC)


def test_assumes_utc_for_naive_timestamp() -> None:
    """Treats a timestamp without a timezone as UTC."""
    assert _parse_lifecycle_timestamp("2026-10-16T08:00:00") == datetime(2026, 10, 16, 8, tzinfo=UTC)


def test_rejects_invalid_or_non_string_timestamps() -> None:
    """Returns None for absent, malformed, or non-string timestamp values."""
    assert _parse_lifecycle_timestamp("") is None
    assert _parse_lifecycle_timestamp("not-a-date") is None
    assert _parse_lifecycle_timestamp(None) is None
    assert _parse_lifecycle_timestamp(123) is None


def test_normalizes_subminute_offset() -> None:
    """Supports timezone offsets with minute precision."""
    parsed = _parse_lifecycle_timestamp("2026-10-16T08:45:00+00:30")
    assert parsed == datetime(2026, 10, 16, 8, 15, tzinfo=UTC)
    assert parsed is not None
    assert parsed.utcoffset() == timedelta(0)
