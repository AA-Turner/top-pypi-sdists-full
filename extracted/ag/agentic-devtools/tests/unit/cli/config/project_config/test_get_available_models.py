"""Tests for get_available_models function."""

from unittest.mock import patch

from agentic_devtools.cli.config.project_config import get_available_models

_LOAD = "agentic_devtools.cli.config.project_config.load_project_config"


class TestGetAvailableModels:
    """Tests for get_available_models."""

    def test_returns_list_when_present(self):
        """Returns the cached availableModels list."""
        with patch(_LOAD, return_value={"availableModels": ["gpt-5.3-codex", "claude-opus-4.6"]}):
            assert get_available_models() == ["gpt-5.3-codex", "claude-opus-4.6"]

    def test_returns_empty_when_missing(self):
        """Returns [] when the key is absent."""
        with patch(_LOAD, return_value={}):
            assert get_available_models() == []

    def test_returns_empty_when_not_a_list(self):
        """Returns [] when availableModels is not a list."""
        with patch(_LOAD, return_value={"availableModels": "gpt-5.3-codex"}):
            assert get_available_models() == []

    def test_filters_non_string_entries(self):
        """Filters out non-string entries from the list."""
        with patch(_LOAD, return_value={"availableModels": ["gpt-5.3-codex", 42, None, "claude-opus-4.6"]}):
            assert get_available_models() == ["gpt-5.3-codex", "claude-opus-4.6"]

    def test_strips_and_drops_blank_strings(self):
        """Strips whitespace and drops blank string entries."""
        with patch(_LOAD, return_value={"availableModels": ["  gpt-5.3-codex  ", "   ", "claude-opus-4.6"]}):
            assert get_available_models() == ["gpt-5.3-codex", "claude-opus-4.6"]
