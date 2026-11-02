"""Tests for get_copilot_config_path."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.copilot.trust import get_copilot_config_path


class TestGetCopilotConfigPath:
    """Tests for get_copilot_config_path."""

    def test_honors_copilot_home(self, monkeypatch, tmp_path):
        """Uses COPILOT_HOME when set."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        assert get_copilot_config_path() == tmp_path / "config.json"

    def test_defaults_to_home_dot_copilot(self, monkeypatch, tmp_path):
        """Falls back to ~/.copilot when COPILOT_HOME is unset."""
        monkeypatch.delenv("COPILOT_HOME", raising=False)
        with patch.object(Path, "home", return_value=tmp_path):
            assert get_copilot_config_path() == tmp_path / ".copilot" / "config.json"

    def test_empty_copilot_home_falls_back(self, monkeypatch, tmp_path):
        """Treats an empty COPILOT_HOME as unset."""
        monkeypatch.setenv("COPILOT_HOME", "")
        with patch.object(Path, "home", return_value=tmp_path):
            assert get_copilot_config_path() == tmp_path / ".copilot" / "config.json"
