"""Tests for ``warn_cost_data_invalid``."""

import pytest

from agentic_devtools.cli.config.project_config import warn_cost_data_invalid


class TestWarnCostDataInvalid:
    """Tests for the invalid-data guard helper."""

    def test_valid_timestamp_is_accepted(self):
        warn_cost_data_invalid("2026-08-22T00:00:00+00:00")

    def test_none_raises_missing(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            warn_cost_data_invalid(None)

    def test_blank_string_raises_missing(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            warn_cost_data_invalid("   ")

    def test_non_string_raises_invalid(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_INVALID"):
            warn_cost_data_invalid(123)

    def test_malformed_date_raises_invalid(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_INVALID"):
            warn_cost_data_invalid("not-a-date")

    def test_timestamp_without_timezone_raises_invalid(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_INVALID"):
            warn_cost_data_invalid("2025-01-01T00:00:00")
