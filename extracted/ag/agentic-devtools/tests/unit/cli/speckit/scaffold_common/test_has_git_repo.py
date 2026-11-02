"""Tests for ``has_git_repo``."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.speckit.scaffold_common import has_git_repo


class TestHasGitRepo:
    """has_git_repo reports whether *repo_root* is inside a git working tree."""

    def test_true_when_git_succeeds(self, tmp_path: Path) -> None:
        completed = MagicMock(returncode=0, stdout=str(tmp_path) + "\n")
        with patch("subprocess.run", return_value=completed) as mock_run:
            result = has_git_repo(tmp_path)

        assert result is True
        mock_run.assert_called_once_with(
            ["git", "-C", str(tmp_path), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_false_when_git_returns_nonzero(self, tmp_path: Path) -> None:
        completed = MagicMock(returncode=128, stdout="")
        with patch("subprocess.run", return_value=completed):
            result = has_git_repo(tmp_path)

        assert result is False

    def test_false_when_stdout_empty(self, tmp_path: Path) -> None:
        completed = MagicMock(returncode=0, stdout="")
        with patch("subprocess.run", return_value=completed):
            result = has_git_repo(tmp_path)

        assert result is False

    def test_false_when_git_missing(self, tmp_path: Path) -> None:
        with patch("subprocess.run", side_effect=OSError("git not found")):
            result = has_git_repo(tmp_path)

        assert result is False
