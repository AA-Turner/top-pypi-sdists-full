"""Tests for _reply_to_pull_request_thread_task."""

from unittest.mock import patch

import pytest

from agentic_devtools.adapters.base import PullRequestThreadReplyResult
from agentic_devtools.cli.pull_request_thread import (
    _reply_to_pull_request_thread_task,
)

_DRY_RUN_REQUEST = {
    "provider": "github",
    "repository": "owner/repo",
    "pull_request_number": 12,
    "discussion_id": 34,
    "body": "preview",
    "dry_run": True,
}

_FAILED_RESULT = PullRequestThreadReplyResult(
    provider="github",
    repository="owner/repo",
    pull_request_number=12,
    discussion_id=34,
    resolution_requested=False,
    mutation_status="failed",
    resolution_status="not_attempted",
    diagnostics=("authentication failed",),
)


class TestHelper:
    def test_task_wrapper_persists_structured_result(self, capsys: pytest.CaptureFixture[str]) -> None:
        _reply_to_pull_request_thread_task(_DRY_RUN_REQUEST)
        assert '"mutationStatus": "dry_run"' in capsys.readouterr().out

    def test_task_wrapper_raises_on_failed_status(self, capsys: pytest.CaptureFixture[str]) -> None:
        with patch(
            "agentic_devtools.cli.pull_request_thread.reply_to_pull_request_thread",
            return_value=_FAILED_RESULT,
        ):
            with pytest.raises(RuntimeError, match="authentication failed"):
                _reply_to_pull_request_thread_task(_DRY_RUN_REQUEST)
        assert '"mutationStatus": "failed"' in capsys.readouterr().out

    def test_task_wrapper_raises_uses_diagnostics_as_message(self) -> None:
        result = PullRequestThreadReplyResult(
            provider="github",
            repository="owner/repo",
            pull_request_number=12,
            discussion_id=34,
            resolution_requested=False,
            mutation_status="failed",
            resolution_status="not_attempted",
            diagnostics=(),
        )
        with patch(
            "agentic_devtools.cli.pull_request_thread.reply_to_pull_request_thread",
            return_value=result,
        ):
            with pytest.raises(RuntimeError, match="provider mutation failed"):
                _reply_to_pull_request_thread_task(_DRY_RUN_REQUEST)
