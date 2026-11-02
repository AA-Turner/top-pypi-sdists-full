"""Tests for agentic_devtools.cli.git.operations.resolve_branch_diff_ref."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git import operations


class TestResolveBranchDiffRef:
    """Tests for resolve_branch_diff_ref."""

    def test_returns_origin_ref_when_available(self):
        """Return origin/<branch>...HEAD when ``git diff --quiet`` finds differences (returncode 1)."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.return_value = MagicMock(returncode=1, stdout="", stderr="")

            result = operations.resolve_branch_diff_ref()

            assert result == "origin/main...HEAD"
            mock_run_git.assert_called_once_with(
                "diff",
                "--quiet",
                "--find-renames",
                "origin/main...HEAD",
                check=False,
            )

    def test_falls_back_to_local_branch_ref(self):
        """Fall back to <branch>...HEAD when origin ref check fails."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=128, stdout="", stderr="error"),
                MagicMock(returncode=1, stdout="", stderr=""),
            ]

            result = operations.resolve_branch_diff_ref(main_branch="develop")

            assert result == "develop...HEAD"

    def test_returns_none_when_no_ref_is_valid(self):
        """Return None when neither origin nor local branch refs are valid."""
        with patch.object(operations, "run_git") as mock_run_git:
            mock_run_git.side_effect = [
                MagicMock(returncode=128, stdout="", stderr="error"),
                MagicMock(returncode=128, stdout="", stderr="error"),
            ]

            result = operations.resolve_branch_diff_ref()

            assert result is None
