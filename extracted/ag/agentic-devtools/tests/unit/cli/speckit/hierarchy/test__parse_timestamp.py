"""Tests for the _parse_timestamp private helper in hierarchy.py."""

from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.speckit.hierarchy import HierarchyValidationError, _parse_timestamp


class TestParseTimestamp:
    """Direct tests for _parse_timestamp covering non-string input branches."""

    def test_none_returns_none(self):
        """None input returns None without error."""
        assert _parse_timestamp(None) is None

    def test_datetime_aware_returned_directly(self):
        """Timezone-aware datetime is returned as-is."""
        dt = datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC)
        result = _parse_timestamp(dt)
        assert result is dt

    def test_datetime_naive_normalized_to_utc(self):
        """Naive datetime is assumed UTC and tzinfo is attached."""
        dt = datetime(2024, 6, 1, 12, 0, 0)
        result = _parse_timestamp(dt)
        assert result == datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC)
        assert result is not None and result.tzinfo == UTC

    def test_non_string_non_datetime_raises_validation_error(self):
        """An integer (or any other unexpected type) raises HierarchyValidationError."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            _parse_timestamp(42)  # type: ignore[arg-type]

        assert exc_info.value.field_name == "processed_at"
        assert "int" in exc_info.value.detail

    def test_list_type_raises_validation_error_with_correct_type_name(self):
        """A list value raises HierarchyValidationError with the correct type name."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            _parse_timestamp(["2024-01-01"])  # type: ignore[arg-type]

        assert exc_info.value.field_name == "processed_at"
        assert "list" in exc_info.value.detail
