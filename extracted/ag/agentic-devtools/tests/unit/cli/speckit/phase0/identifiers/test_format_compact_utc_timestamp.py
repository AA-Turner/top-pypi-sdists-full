"""Tests for format_compact_utc_timestamp in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

from datetime import UTC, datetime

from agentic_devtools.cli.speckit.phase0.identifiers import format_compact_utc_timestamp


class TestFormatCompactUtcTimestamp:
    """Tests for the format_compact_utc_timestamp function."""

    def test_produces_16_character_token(self) -> None:
        dt = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
        result = format_compact_utc_timestamp(dt)
        assert result == "20260102T030405Z"
        assert len(result) == 16

    def test_only_contains_permitted_operation_id_characters(self) -> None:
        dt = datetime(2026, 12, 31, 23, 59, 59, tzinfo=UTC)
        result = format_compact_utc_timestamp(dt)
        assert all(char.isdigit() or char in ("T", "Z") for char in result)
