"""Tests for _get_temp_output_dir."""

from pathlib import Path

from agentic_devtools.cli.azure import app_insights_commands


def test_returns_state_directory(monkeypatch, tmp_path):
    monkeypatch.setattr(app_insights_commands, "get_state_dir", lambda: tmp_path)

    result = app_insights_commands._get_temp_output_dir()

    assert result == Path(tmp_path)
