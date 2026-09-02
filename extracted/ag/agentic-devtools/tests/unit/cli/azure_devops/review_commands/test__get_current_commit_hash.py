"""Tests for the current Git commit hash helper."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.review_commands import _get_current_commit_hash


class TestGetCurrentCommitHash:
    """Tests for _get_current_commit_hash."""

    def test_returns_normalized_full_sha(self):
        """A valid HEAD SHA is returned in lowercase without surrounding whitespace."""
        result = MagicMock(returncode=0, stdout="ABCDEF1234567890ABCDEF1234567890ABCDEF12\n")

        with patch("agentic_devtools.cli.azure_devops.review_commands.run_safe", return_value=result) as mock_run:
            assert _get_current_commit_hash() == "abcdef1234567890abcdef1234567890abcdef12"

        mock_run.assert_called_once_with(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            shell=False,
        )

    def test_returns_none_for_failed_git_command(self):
        """A failed Git command does not produce a commit hash."""
        result = MagicMock(returncode=128, stdout="")

        with patch("agentic_devtools.cli.azure_devops.review_commands.run_safe", return_value=result):
            assert _get_current_commit_hash() is None

    def test_returns_none_for_invalid_git_output(self):
        """Non-SHA output is rejected."""
        result = MagicMock(returncode=0, stdout="not-a-commit\n")

        with patch("agentic_devtools.cli.azure_devops.review_commands.run_safe", return_value=result):
            assert _get_current_commit_hash() is None

    def test_returns_none_when_git_cannot_start(self):
        """An OS error from Git is converted to an absent hash."""
        with patch(
            "agentic_devtools.cli.azure_devops.review_commands.run_safe",
            side_effect=OSError("git unavailable"),
        ):
            assert _get_current_commit_hash() is None
