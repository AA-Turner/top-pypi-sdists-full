"""Tests for ``get_current_branch``."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.speckit.scaffold_common import get_current_branch


class TestGetCurrentBranch:
    """get_current_branch returns the current branch name, or None if unavailable."""

    def test_returns_branch_name(self, tmp_path: Path) -> None:
        completed = MagicMock(returncode=0, stdout="042-my-feature\n")
        with patch("subprocess.run", return_value=completed) as mock_run:
            result = get_current_branch(tmp_path)

        assert result == "042-my-feature"
        mock_run.assert_called_once_with(
            ["git", "-C", str(tmp_path), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_returns_none_when_git_returns_nonzero(self, tmp_path: Path) -> None:
        completed = MagicMock(returncode=128, stdout="")
        with patch("subprocess.run", return_value=completed):
            result = get_current_branch(tmp_path)

        assert result is None

    def test_returns_none_when_stdout_empty(self, tmp_path: Path) -> None:
        completed = MagicMock(returncode=0, stdout="   \n")
        with patch("subprocess.run", return_value=completed):
            result = get_current_branch(tmp_path)

        assert result is None

    def test_returns_none_when_git_missing(self, tmp_path: Path) -> None:
        with patch("subprocess.run", side_effect=OSError("git not found")):
            result = get_current_branch(tmp_path)

        assert result is None
