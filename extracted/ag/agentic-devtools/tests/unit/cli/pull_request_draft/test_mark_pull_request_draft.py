from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.adapters.pull_request_draft import PullRequestDraftResult
from agentic_devtools.cli import pull_request_draft as commands


def test_dispatches_request(monkeypatch) -> None:
    request = MagicMock()
    result = PullRequestDraftResult(True, "github", "updated")
    monkeypatch.setattr(commands, "build_draft_request", lambda **kwargs: request)
    monkeypatch.setattr(commands, "dispatch_draft", lambda value: result)
    assert commands.mark_pull_request_draft() == result


def test_invalid_request_returns_failure(monkeypatch) -> None:
    monkeypatch.setattr(commands, "build_draft_request", MagicMock(side_effect=ValueError("bad request")))
    result = commands.mark_pull_request_draft()
    assert result.success is False
    assert result.status == "invalid"
