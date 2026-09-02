"""Tests for provider-neutral pull-request comment command."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.pull_request_comments import PullRequestCommentRequest
from agentic_devtools.cli import pull_request_comments as commands


def test_async_snapshots_request(monkeypatch: pytest.MonkeyPatch) -> None:
    request = PullRequestCommentRequest("github", "owner/repo", 7, "comment")
    monkeypatch.setattr(commands, "_build_request", lambda **kwargs: request)
    task = MagicMock(id="task")
    runner = MagicMock(return_value=task)
    monkeypatch.setattr(commands, "run_function_in_background", runner)
    monkeypatch.setattr(commands, "print_task_tracking_info", MagicMock())
    monkeypatch.setattr(
        commands.sys, "argv", ["agdt-add-pull-request-comment", "--pull-request-id", "7", "--content", "x"]
    )
    commands.add_pull_request_comment_async()
    assert runner.call_args.kwargs["func_kwargs"] == request.__dict__


def test_async_accepts_explicit_arguments(monkeypatch: pytest.MonkeyPatch) -> None:
    request = PullRequestCommentRequest("github", "owner/repo", 7, "comment")
    builder = MagicMock(return_value=request)
    monkeypatch.setattr(commands, "_build_request", builder)
    monkeypatch.setattr(commands, "run_function_in_background", MagicMock())
    monkeypatch.setattr(commands, "print_task_tracking_info", MagicMock())
    monkeypatch.setattr(commands.sys, "argv", ["other"])
    commands.add_pull_request_comment_async("7", "comment", "github", "owner/repo")
    builder.assert_called_once_with(
        provider="github",
        repository="owner/repo",
        pull_request_id="7",
        content="comment",
    )


def test_async_reports_invalid_request(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(commands, "_build_request", MagicMock(side_effect=ValueError("content is required")))
    monkeypatch.setattr(commands.sys, "argv", ["agdt-add-pull-request-comment"])
    with pytest.raises(SystemExit) as exc_info:
        commands.add_pull_request_comment_async(provider="github")
    assert exc_info.value.code == 1
    result = json.loads(capsys.readouterr().out)
    assert result["success"] is False
    assert result["status"] == "invalid"
