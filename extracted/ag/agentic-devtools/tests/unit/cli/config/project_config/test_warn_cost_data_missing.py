"""Tests for ``warn_cost_data_missing``."""

import pytest

from agentic_devtools.cli.config.project_config import warn_cost_data_missing


class TestWarnCostDataMissing:
    """Tests for the missing-data guard helper."""

    def test_valid_timestamp_is_accepted(self):
        warn_cost_data_missing("2026-08-22T00:00:00+00:00")

    def test_none_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            warn_cost_data_missing(None)

    def test_blank_string_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            warn_cost_data_missing("   ")

    def test_non_string_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_INVALID"):
            warn_cost_data_missing(123)
