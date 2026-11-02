"""Tests for _fetch_current_head_sha helper."""

import subprocess
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.github import pr_approve


class TestFetchCurrentHeadSha:
    """Tests for _fetch_current_head_sha."""

    def test_returns_sha_on_success(self):
        """Successful gh api call returns the stripped head SHA and no error."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "  " + ("a" * 40) + "\n"

        with patch.object(pr_approve, "run_safe", return_value=mock_result) as mock_run:
            sha, error = pr_approve._fetch_current_head_sha(42, "owner/repo")

        assert sha == "a" * 40
        assert error == ""
        args = mock_run.call_args.args[0]
        assert args[:2] == ["gh", "api"]
        assert "repos/owner/repo/pulls/42" in args[2]
        assert mock_run.call_args.kwargs["timeout"] == 30

    def test_returns_none_and_stderr_on_nonzero_exit(self):
        """A non-zero exit code yields (None, stderr) without raising."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "authentication required"

        with patch.object(pr_approve, "run_safe", return_value=mock_result):
            sha, error = pr_approve._fetch_current_head_sha(42, "owner/repo")

        assert sha is None
        assert error == "authentication required"

    def test_falls_back_to_stdout_when_stderr_empty(self):
        """When stderr is empty, the error message falls back to stdout."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "not found"
        mock_result.stderr = ""

        with patch.object(pr_approve, "run_safe", return_value=mock_result):
            sha, error = pr_approve._fetch_current_head_sha(42, "owner/repo")

        assert sha is None
        assert error == "not found"

    def test_falls_back_to_exit_code_when_no_detail(self):
        """When both stdout and stderr are empty, error mentions the exit code."""
        mock_result = MagicMock()
        mock_result.returncode = 7
        mock_result.stdout = ""
        mock_result.stderr = ""

        with patch.object(pr_approve, "run_safe", return_value=mock_result):
            sha, error = pr_approve._fetch_current_head_sha(42, "owner/repo")

        assert sha is None
        assert error == "gh api exited with code 7"

    def test_returns_none_when_success_but_empty_sha(self):
        """A zero exit code with blank stdout is treated as a failure to resolve."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "   "
        mock_result.stderr = ""

        with patch.object(pr_approve, "run_safe", return_value=mock_result):
            sha, error = pr_approve._fetch_current_head_sha(42, "owner/repo")

        assert sha is None
        assert error == "gh api exited with code 0"

    def test_returns_timeout_error_when_head_lookup_times_out(self):
        """A stalled head lookup becomes a controlled failure result."""
        with patch.object(
            pr_approve,
            "run_safe",
            side_effect=subprocess.TimeoutExpired(cmd="gh api", timeout=30),
        ):
            sha, error = pr_approve._fetch_current_head_sha(42, "owner/repo")

        assert sha is None
        assert error == "gh api timed out after 30s"
