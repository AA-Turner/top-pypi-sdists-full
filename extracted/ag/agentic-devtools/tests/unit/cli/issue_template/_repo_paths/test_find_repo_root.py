"""Tests for agentic_devtools.cli.issue_template._repo_paths._find_repo_root."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.issue_template._repo_paths import _find_repo_root


class TestFindRepoRoot:
    """Tests for _find_repo_root."""

    def test_finds_git_root(self, tmp_path: Path) -> None:
        """Returns path when .git directory exists."""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        sub = tmp_path / "sub" / "deep"
        sub.mkdir(parents=True)
        with patch("agentic_devtools.cli.issue_template._repo_paths.Path.cwd", return_value=sub):
            result = _find_repo_root()
        assert result == tmp_path

    def test_returns_none_when_no_git(self, tmp_path: Path) -> None:
        """Returns None when no .git directory found up to filesystem root."""
        sub = tmp_path / "sub" / "deep"
        sub.mkdir(parents=True)
        with (
            patch("agentic_devtools.cli.issue_template._repo_paths.Path.cwd", return_value=sub),
            patch("agentic_devtools.cli.issue_template._repo_paths.Path.exists", return_value=False),
        ):
            result = _find_repo_root()
        assert result is None
