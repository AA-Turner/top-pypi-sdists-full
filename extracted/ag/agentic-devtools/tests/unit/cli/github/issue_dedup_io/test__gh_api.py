"""Tests for _gh_api internal helper."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.shared.retry import RetryableError

_MOD = "agentic_devtools.cli.github.issue_dedup_io"


class TestGhApi:
    """Tests for the _gh_api function."""

    @patch(f"{_MOD}.run_safe")
    def test_passes_body_via_stdin(self, mock_run) -> None:
        """Body is serialized as JSON and passed via --input -."""
        from agentic_devtools.cli.github.issue_dedup_io import _gh_api

        mock_run.return_value = MagicMock(returncode=0, stdout='{"ok": true}')
        result = _gh_api("/endpoint", method="POST", body={"key": "value"})
        assert result == '{"ok": true}'
        call_args = mock_run.call_args
        cmd = call_args.args[0]
        assert "--input" in cmd
        assert "-" in cmd
        assert call_args.kwargs["input"] == json.dumps({"key": "value"})

    @patch(f"{_MOD}.run_safe")
    def test_passes_headers(self, mock_run) -> None:
        """Headers are passed as repeated -H arguments."""
        from agentic_devtools.cli.github.issue_dedup_io import _gh_api

        mock_run.return_value = MagicMock(returncode=0, stdout="ok")
        _gh_api("/endpoint", headers={"Accept": "application/json", "X-Custom": "val"})
        cmd = mock_run.call_args.args[0]
        assert "-H" in cmd
        assert "Accept: application/json" in cmd
        assert "X-Custom: val" in cmd

    @patch(f"{_MOD}.run_safe")
    def test_rate_limit_raises_retryable(self, mock_run) -> None:
        """Rate limit error in stderr raises RetryableError with is_rate_limit=True."""
        from agentic_devtools.cli.github.issue_dedup_io import _gh_api

        mock_run.return_value = MagicMock(returncode=1, stderr="secondary rate limit exceeded", stdout="")
        with pytest.raises(RetryableError, match="Rate limited") as exc_info:
            _gh_api("/endpoint")
        assert exc_info.value.is_rate_limit is True
        assert exc_info.value.provider == "github"

    @patch(f"{_MOD}.run_safe")
    def test_http_4xx_raises_runtime_error(self, mock_run) -> None:
        """Exit code 4 (HTTP 4xx) raises RuntimeError."""
        from agentic_devtools.cli.github.issue_dedup_io import _gh_api

        mock_run.return_value = MagicMock(returncode=4, stderr="Not Found", stdout="")
        with pytest.raises(RuntimeError, match="GitHub API error"):
            _gh_api("/endpoint")

    @patch(f"{_MOD}.run_safe")
    def test_other_failure_raises_runtime_error(self, mock_run) -> None:
        """Other non-zero exit codes raise RuntimeError with exit code."""
        from agentic_devtools.cli.github.issue_dedup_io import _gh_api

        mock_run.return_value = MagicMock(returncode=2, stderr="something went wrong", stdout="")
        with pytest.raises(RuntimeError, match="exit 2"):
            _gh_api("/endpoint")

    @patch(f"{_MOD}.run_safe")
    def test_no_body_no_input_flag(self, mock_run) -> None:
        """Without body, no --input flag is passed."""
        from agentic_devtools.cli.github.issue_dedup_io import _gh_api

        mock_run.return_value = MagicMock(returncode=0, stdout="")
        _gh_api("/endpoint")
        cmd = mock_run.call_args.args[0]
        assert "--input" not in cmd
        assert mock_run.call_args.kwargs.get("input") is None

    @patch(f"{_MOD}.run_safe")
    def test_empty_dict_body_sends_input_flag(self, mock_run) -> None:
        """Empty dict body still sends --input - with serialized JSON."""
        from agentic_devtools.cli.github.issue_dedup_io import _gh_api

        mock_run.return_value = MagicMock(returncode=0, stdout="")
        _gh_api("/endpoint", method="POST", body={})
        cmd = mock_run.call_args.args[0]
        assert "--input" in cmd
        assert "-" in cmd
        assert mock_run.call_args.kwargs["input"] == "{}"
