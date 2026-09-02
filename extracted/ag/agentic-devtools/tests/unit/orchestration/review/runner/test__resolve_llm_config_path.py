"""Tests for _resolve_llm_config_path()."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.orchestration.review.runner import _resolve_llm_config_path


class TestResolveLlmConfigPath:
    """Tests for the repo-root config path resolver."""

    def test_returns_repo_root_relative_path(self) -> None:
        """Returns .agdt/config/llm-providers.yml under the detected repo root."""
        fake_root = Path("/repo/root")
        with patch("agentic_devtools.state.get_repo_root", return_value=fake_root):
            result = _resolve_llm_config_path()

        assert result == fake_root / ".agdt/config/llm-providers.yml"

    def test_returns_none_when_repo_root_is_none(self) -> None:
        """Returns None when not inside a git repository."""
        with patch("agentic_devtools.state.get_repo_root", return_value=None):
            result = _resolve_llm_config_path()

        assert result is None

    def test_returns_none_when_get_repo_root_raises(self) -> None:
        """Returns None when get_repo_root raises an unexpected exception."""
        with patch(
            "agentic_devtools.state.get_repo_root",
            side_effect=RuntimeError("git not found"),
        ):
            result = _resolve_llm_config_path()

        assert result is None
