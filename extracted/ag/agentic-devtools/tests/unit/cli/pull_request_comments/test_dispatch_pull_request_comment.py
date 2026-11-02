"""Tests for provider-neutral pull-request comment command."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.pull_request_comments import PullRequestCommentRequest, PullRequestCommentResult
from agentic_devtools.cli import pull_request_comments as commands


def test_dispatch_and_sync_command(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    request = PullRequestCommentRequest("github", "owner/repo", 7, "comment")
    result = PullRequestCommentResult(True, "github", "dry_run")
    monkeypatch.setattr(commands, "_adapter_for", lambda _: MagicMock(add_comment=lambda _: result))
    assert commands.dispatch_pull_request_comment(request) == result


def test_dispatch_catches_adapter_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    request = PullRequestCommentRequest("github", "owner/repo", 7, "comment")
    monkeypatch.setattr(commands, "_adapter_for", MagicMock(side_effect=RuntimeError("failed")))
    result = commands.dispatch_pull_request_comment(request)
    assert result.success is False
    assert result.error == "failed"
