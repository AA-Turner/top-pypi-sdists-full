"""Tests for ``warn_cost_data_stale``."""

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.config.project_config import MODEL_COST_FRESHNESS_DAYS, warn_cost_data_stale

_FRESH_TIMESTAMP = (datetime.now(UTC) - timedelta(days=1)).replace(microsecond=0).isoformat()


class TestWarnCostDataStale:
    """Tests for the stale-only cost-data warning helper."""

    def test_freshness_window_constant(self):
        assert MODEL_COST_FRESHNESS_DAYS == 90

    def test_recent_timestamp_does_not_warn(self, capsys):
        warn_cost_data_stale(_FRESH_TIMESTAMP)
        assert capsys.readouterr().err == ""

    def test_old_timestamp_warns(self, capsys):
        warn_cost_data_stale("2024-01-01T00:00:00+00:00")
        assert "WARN_COST_DATA_STALE" in capsys.readouterr().err

    def test_old_timestamp_warns_with_model_and_provenance_context(self, capsys):
        warn_cost_data_stale(
            "2024-01-01T00:00:00+00:00",
            model_id="claude-opus-4.8",
            provenance="curated-catalog",
        )
        warning = capsys.readouterr().err
        assert "WARN_COST_DATA_STALE" in warning
        assert "model 'claude-opus-4.8'" in warning
        assert "source=curated-catalog" in warning

    def test_z_suffix_is_accepted(self, capsys):
        warn_cost_data_stale("2024-01-01T00:00:00Z")
        assert "WARN_COST_DATA_STALE" in capsys.readouterr().err

    def test_missing_value_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            warn_cost_data_stale(None)

    def test_blank_string_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            warn_cost_data_stale("   ")

    def test_non_string_raises(self):
        with pytest.raises(ValueError, match="WARN_COST_DATA_INVALID"):
            warn_cost_data_stale(123)

    def test_future_timestamp_raises(self):
        future = (datetime.now(UTC) + timedelta(days=365)).replace(microsecond=0).isoformat()
        with pytest.raises(ValueError, match="WARN_COST_DATA_INVALID"):
            warn_cost_data_stale(future)

    def test_future_timestamp_emits_invalid_to_stderr(self, capsys):
        future = (datetime.now(UTC) + timedelta(days=1)).replace(microsecond=0).isoformat()
        with pytest.raises(ValueError):
            warn_cost_data_stale(future)
        assert "WARN_COST_DATA_INVALID" in capsys.readouterr().err

    def test_emit_warnings_false_suppresses_parse_error_stderr(self, capsys):
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            warn_cost_data_stale(None, emit_warnings=False)
        assert capsys.readouterr().err == ""

    def test_emit_warnings_false_suppresses_future_timestamp_stderr(self, capsys):
        future = (datetime.now(UTC) + timedelta(days=1)).replace(microsecond=0).isoformat()
        with pytest.raises(ValueError, match="WARN_COST_DATA_INVALID"):
            warn_cost_data_stale(future, emit_warnings=False)
        assert capsys.readouterr().err == ""

    def test_emit_warnings_false_suppresses_stale_stderr(self, capsys):
        warn_cost_data_stale("2024-01-01T00:00:00+00:00", emit_warnings=False)
        assert capsys.readouterr().err == ""
