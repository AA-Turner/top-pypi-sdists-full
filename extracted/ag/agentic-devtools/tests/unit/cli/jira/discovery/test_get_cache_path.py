"""Tests for agentic_devtools.cli.jira.discovery._get_cache_path."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.jira.discovery import _get_cache_path


class TestGetCachePath:
    """Tests for _get_cache_path."""

    def test_returns_cache_path_when_repo_root_exists(self, tmp_path: Path) -> None:
        """Returns .agdt/cache/jira-discovery.json under the git root."""
        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            result = _get_cache_path()

        assert result == tmp_path / ".agdt" / "cache" / "jira-discovery.json"

    def test_returns_none_when_no_repo_root(self) -> None:
        """Returns None when git repo root cannot be determined."""
        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=None,
        ):
            result = _get_cache_path()

        assert result is None
