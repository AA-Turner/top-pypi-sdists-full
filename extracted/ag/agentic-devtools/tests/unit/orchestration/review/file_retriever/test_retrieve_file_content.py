"""Tests for retrieve_file_content function."""

from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.review.file_retriever import RetrievalResult, retrieve_file_content


class TestRetrieveFileContent:
    """Tests for retrieve_file_content with git-show and fallback."""

    def test_successful_git_show(self) -> None:
        """Git show success returns content."""
        cat_file_result = MagicMock()
        cat_file_result.returncode = 0
        cat_file_result.stdout = "17"  # len("file content here")

        git_show_result = MagicMock()
        git_show_result.returncode = 0
        git_show_result.stdout = "file content here"

        with patch(
            "agentic_devtools.orchestration.review.file_retriever.subprocess.run",
            side_effect=[cat_file_result, git_show_result],
        ) as mock_run:
            result = retrieve_file_content("/src/app.py", "abc123", {})

        assert result.content == "file content here"
        assert result.context_status == "success"
        assert mock_run.call_count == 2
        # Verify git show path is normalized (no leading slash)
        git_show_call_args = mock_run.call_args_list[1][0][0]
        assert git_show_call_args == ["git", "show", "abc123:src/app.py"]

    def test_git_show_failure_triggers_ado_fallback(self) -> None:
        """Git show failure triggers ADO API fallback."""
        mock_git_result = MagicMock()
        mock_git_result.returncode = 128

        state = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-123"}

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.subprocess.run", return_value=mock_git_result),
            patch("agentic_devtools.orchestration.review.file_retriever._retrieve_via_ado_api") as mock_ado,
        ):
            mock_ado.return_value = RetrievalResult(content="ado content", context_status="success")
            result = retrieve_file_content("/src/app.py", "abc123", state)

        assert result.content == "ado content"
        assert result.context_status == "success"

    def test_both_fail_returns_unavailable(self) -> None:
        """When both git-show and ADO fail, returns unavailable."""
        mock_git_result = MagicMock()
        mock_git_result.returncode = 128

        state = {"organization": "", "project": "", "repo_id": ""}

        with patch("agentic_devtools.orchestration.review.file_retriever.subprocess.run", return_value=mock_git_result):
            result = retrieve_file_content("/src/app.py", "abc123", state)

        assert result.context_status == "unavailable"

    def test_oversized_file_skipped(self) -> None:
        """Files exceeding size threshold are skipped."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "x" * 600_000

        with patch("agentic_devtools.orchestration.review.file_retriever.subprocess.run", return_value=mock_result):
            result = retrieve_file_content("/src/big.py", "abc123", {}, max_size_bytes=500_000)

        assert result.context_status == "skipped_too_large"

    def test_timeout_returns_unavailable(self) -> None:
        """Git show timeout returns unavailable from fallback (ADO also fails)."""
        with patch(
            "agentic_devtools.orchestration.review.file_retriever.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="git", timeout=30),
        ):
            # Empty state means ADO fallback also returns unavailable
            result = retrieve_file_content("/src/app.py", "abc123", {"organization": "", "project": "", "repo_id": ""})

        assert result.context_status == "unavailable"

    def test_max_size_bytes_passed_to_ado_fallback(self) -> None:
        """max_size_bytes is forwarded to the ADO fallback."""
        mock_git_result = MagicMock()
        mock_git_result.returncode = 128

        state = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-123"}

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.subprocess.run", return_value=mock_git_result),
            patch("agentic_devtools.orchestration.review.file_retriever._retrieve_via_ado_api") as mock_ado,
        ):
            mock_ado.return_value = RetrievalResult(content="ok", context_status="success")
            retrieve_file_content("/src/app.py", "abc123", state, max_size_bytes=1024)

        # Verify the custom size limit was forwarded
        mock_ado.assert_called_once_with("/src/app.py", "abc123", state, 1024)
