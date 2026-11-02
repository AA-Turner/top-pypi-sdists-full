"""Tests for agentic_devtools.cli.issue_template.commands._find_repo_root."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.issue_template.commands import _find_repo_root


class TestFindRepoRoot:
    """Tests for the _find_repo_root helper function."""

    def test_finds_git_repo(self, tmp_path: Path) -> None:
        """Returns repo root when .git directory exists."""
        (tmp_path / ".git").mkdir()
        subdir = tmp_path / "sub" / "dir"
        subdir.mkdir(parents=True)

        with patch("agentic_devtools.cli.issue_template.commands.Path.cwd", return_value=subdir):
            result = _find_repo_root()

        assert result == tmp_path

    def test_returns_none_when_no_git(self, tmp_path: Path) -> None:
        """Returns None when not in a git repository."""
        subdir = tmp_path / "not-a-repo"
        subdir.mkdir()

        with patch("agentic_devtools.cli.issue_template.commands.Path.cwd", return_value=subdir):
            result = _find_repo_root()

        assert result is None

    def test_finds_root_level_git(self, tmp_path: Path) -> None:
        """Finds .git at the root of the path."""
        (tmp_path / ".git").mkdir()

        with patch("agentic_devtools.cli.issue_template.commands.Path.cwd", return_value=tmp_path):
            result = _find_repo_root()

        assert result == tmp_path
