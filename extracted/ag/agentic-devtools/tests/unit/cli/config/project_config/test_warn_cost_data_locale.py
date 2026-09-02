"""Tests for ``warn_cost_data_locale``."""

from datetime import datetime, timedelta, timezone

import pytest

from agentic_devtools.cli.config.project_config import warn_cost_data_locale

_FRESH_TIMESTAMP = (datetime.now(timezone.utc) - timedelta(days=1)).replace(microsecond=0).isoformat()


class TestWarnCostDataLocale:
    """Tests for the locale-aware staleness warning helper."""

    def test_recent_timestamp_does_not_warn(self, capsys):
        warn_cost_data_locale(_FRESH_TIMESTAMP)
        assert capsys.readouterr().err == ""

    def test_old_timestamp_warns(self, capsys):
        warn_cost_data_locale("2024-01-01T00:00:00+00:00")
        assert "WARN_COST_DATA_STALE" in capsys.readouterr().err

    def test_missing_value_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            warn_cost_data_locale(None)

    def test_blank_string_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            warn_cost_data_locale("   ")

    def test_invalid_timestamp_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_INVALID"):
            warn_cost_data_locale("not-a-date")

    def test_timestamp_without_timezone_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_INVALID"):
            warn_cost_data_locale("2025-01-01T00:00:00")
