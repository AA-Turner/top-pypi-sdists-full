"""Tests for provider-neutral pull-request comment command."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.pull_request_comments import PullRequestCommentRequest, PullRequestCommentResult
from agentic_devtools.cli import pull_request_comments as commands


def test_add_pull_request_comment(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    request = PullRequestCommentRequest("github", "owner/repo", 7, "comment")
    result = PullRequestCommentResult(True, "github", "dry_run")
    monkeypatch.setattr(commands, "_build_request", lambda **kwargs: request)
    monkeypatch.setattr(commands, "dispatch_pull_request_comment", lambda _: result)
    assert commands.add_pull_request_comment() == result
    assert json.loads(capsys.readouterr().out)["status"] == "dry_run"

    monkeypatch.setattr(commands, "_build_request", MagicMock(side_effect=ValueError("bad request")))
    invalid = commands.add_pull_request_comment(provider="github")
    assert invalid.success is False
    assert invalid.status == "invalid"
