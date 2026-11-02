"""Tests for _retrieve_via_git_show."""

from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch


class TestRetrieveViaGitShow:
    """Tests for _retrieve_via_git_show."""

    def test_timeout_returns_unavailable(self) -> None:
        """Git show timeout produces unavailable result."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_git_show

        with patch("agentic_devtools.orchestration.review.file_retriever.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="git show", timeout=30)
            result = _retrieve_via_git_show("abc123", "/src/app.py")

        assert result.context_status == "unavailable"
        assert "timeout" in result.context_status_reason

    def test_cat_file_os_error_returns_unavailable(self) -> None:
        """OSError during git cat-file -s returns unavailable without reaching git show."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_git_show

        with patch("agentic_devtools.orchestration.review.file_retriever.subprocess.run") as mock_run:
            mock_run.side_effect = OSError("git not found")
            result = _retrieve_via_git_show("abc123", "/src/app.py")

        assert result.context_status == "unavailable"
        assert "git_cat_file_error" in result.context_status_reason

    def test_cat_file_size_exceeds_limit_skips_without_git_show(self) -> None:
        """When cat-file reports size > max_size_bytes, git show is not called."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_git_show

        cat_file_result = MagicMock()
        cat_file_result.returncode = 0
        cat_file_result.stdout = "600001"

        with patch("agentic_devtools.orchestration.review.file_retriever.subprocess.run") as mock_run:
            mock_run.return_value = cat_file_result
            result = _retrieve_via_git_show("abc123", "/src/app.py")

        assert result.context_status == "skipped_too_large"
        mock_run.assert_called_once()
        assert result.file_size == 600001

    def test_git_show_timeout_when_cat_file_succeeds(self) -> None:
        """TimeoutExpired from git show (after successful cat-file) returns unavailable."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_git_show

        cat_file_result = MagicMock()
        cat_file_result.returncode = 0
        cat_file_result.stdout = "100"

        with patch("agentic_devtools.orchestration.review.file_retriever.subprocess.run") as mock_run:
            mock_run.side_effect = [cat_file_result, subprocess.TimeoutExpired(cmd="git show", timeout=30)]
            result = _retrieve_via_git_show("abc123", "/src/app.py")

        assert result.context_status == "unavailable"
        assert "git_show_timeout" in result.context_status_reason

    def test_os_error_returns_unavailable(self) -> None:
        """OSError during git show returns unavailable."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_git_show

        cat_file_fail = MagicMock()
        cat_file_fail.returncode = 128

        with patch("agentic_devtools.orchestration.review.file_retriever.subprocess.run") as mock_run:
            mock_run.side_effect = [cat_file_fail, OSError("No such file")]
            result = _retrieve_via_git_show("abc123", "/src/app.py")

        assert result.context_status == "unavailable"
        assert "git_show_error" in result.context_status_reason
