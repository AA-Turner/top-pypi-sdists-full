"""Tests for _fetch_pr_head_sha."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.github.browser_apply_autofix import _fetch_pr_head_sha

_PATCH = "agentic_devtools.cli.github.browser_apply_autofix.run_safe"


class TestFetchPrHeadSha:
    """Tests for _fetch_pr_head_sha (best-effort gh CLI wrapper)."""

    def test_returns_sha_on_success(self) -> None:
        proc = MagicMock()
        proc.returncode = 0
        proc.stdout = "abc1234567890abc\n"
        with patch(_PATCH, return_value=proc) as mock_run:
            result = _fetch_pr_head_sha(42, "owner/repo")
        assert result == "abc1234567890abc"
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "gh" in cmd
        assert "--jq" in cmd

    def test_returns_none_on_nonzero_exit(self) -> None:
        proc = MagicMock()
        proc.returncode = 1
        proc.stderr = "not found"
        proc.stdout = ""
        with patch(_PATCH, return_value=proc):
            result = _fetch_pr_head_sha(42, "owner/repo")
        assert result is None

    def test_returns_none_on_empty_stdout(self) -> None:
        proc = MagicMock()
        proc.returncode = 0
        proc.stdout = "   \n"
        with patch(_PATCH, return_value=proc):
            result = _fetch_pr_head_sha(42, "owner/repo")
        assert result is None

    def test_returns_none_on_exception(self) -> None:
        with patch(_PATCH, side_effect=FileNotFoundError("gh not found")):
            result = _fetch_pr_head_sha(42, "owner/repo")
        assert result is None
