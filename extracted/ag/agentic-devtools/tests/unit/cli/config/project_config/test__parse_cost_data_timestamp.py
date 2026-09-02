"""Tests for ``_parse_cost_data_timestamp``."""

from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.config.project_config import (
    WARN_COST_DATA_INVALID,
    WARN_COST_DATA_MISSING,
    _parse_cost_data_timestamp,
)


class TestParseCostDataTimestamp:
    """Tests for the cost-data timestamp parser."""

    def test_none_raises_missing(self):
        with pytest.raises(ValueError, match=WARN_COST_DATA_MISSING):
            _parse_cost_data_timestamp(None)

    def test_non_string_raises_invalid(self):
        with pytest.raises(ValueError, match=WARN_COST_DATA_INVALID):
            _parse_cost_data_timestamp(12345)

    def test_empty_string_raises_missing(self):
        with pytest.raises(ValueError, match=WARN_COST_DATA_MISSING):
            _parse_cost_data_timestamp("")

    def test_blank_string_raises_missing(self):
        with pytest.raises(ValueError, match=WARN_COST_DATA_MISSING):
            _parse_cost_data_timestamp("   ")

    def test_invalid_iso_string_raises_invalid(self):
        with pytest.raises(ValueError, match=WARN_COST_DATA_INVALID):
            _parse_cost_data_timestamp("not-a-date")

    def test_naive_datetime_raises_invalid(self):
        with pytest.raises(ValueError, match=WARN_COST_DATA_INVALID):
            _parse_cost_data_timestamp("2024-06-01T12:00:00")

    def test_z_suffix_is_accepted_and_normalized_to_utc(self):
        result = _parse_cost_data_timestamp("2024-06-01T12:00:00Z")
        assert result == datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC)

    def test_plus_offset_is_accepted_and_normalized_to_utc(self):
        result = _parse_cost_data_timestamp("2024-06-01T14:00:00+02:00")
        assert result == datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC)

    def test_overflow_error_during_timezone_normalization_raises_invalid(self, monkeypatch):
        import agentic_devtools.cli.config.project_config as project_config

        class _OverflowingDatetime:
            tzinfo = object()

            def astimezone(self, _tz):
                raise OverflowError

        monkeypatch.setattr(
            project_config,
            "datetime",
            type(
                "FakeDatetime",
                (),
                {"fromisoformat": staticmethod(lambda _v: _OverflowingDatetime())},
            ),
        )
        with pytest.raises(ValueError, match=WARN_COST_DATA_INVALID):
            _parse_cost_data_timestamp("2026-08-27T00:00:00+00:00")

    def test_os_error_during_timezone_normalization_raises_invalid(self, monkeypatch):
        import agentic_devtools.cli.config.project_config as project_config

        class _OSErrorDatetime:
            tzinfo = object()

            def astimezone(self, _tz):
                raise OSError

        monkeypatch.setattr(
            project_config,
            "datetime",
            type(
                "FakeDatetime",
                (),
                {"fromisoformat": staticmethod(lambda _v: _OSErrorDatetime())},
            ),
        )
        with pytest.raises(ValueError, match=WARN_COST_DATA_INVALID):
            _parse_cost_data_timestamp("2026-08-27T00:00:00+00:00")

    def test_utc_offset_is_preserved(self):
        result = _parse_cost_data_timestamp("2024-06-01T12:00:00+00:00")
        assert result.tzinfo == UTC
