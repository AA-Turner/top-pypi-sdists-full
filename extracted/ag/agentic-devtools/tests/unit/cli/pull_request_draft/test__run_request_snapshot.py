from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.adapters.pull_request_draft import PullRequestDraftResult
from agentic_devtools.cli import pull_request_draft as commands


def test_returns_zero_for_success(monkeypatch, capsys) -> None:
    request = MagicMock()
    monkeypatch.setattr(commands, "PullRequestDraftRequest", lambda **kwargs: request)
    monkeypatch.setattr(
        commands,
        "dispatch_draft",
        lambda value: PullRequestDraftResult(True, "github", "updated"),
    )

    result = commands._run_request_snapshot(
        provider="github", repository="owner/repo", pull_request_id=42, dry_run=False
    )

    assert result == 0
    assert '"success": true' in capsys.readouterr().out


def test_returns_one_for_failure(monkeypatch, capsys) -> None:
    request = MagicMock()
    monkeypatch.setattr(commands, "PullRequestDraftRequest", lambda **kwargs: request)
    monkeypatch.setattr(
        commands,
        "dispatch_draft",
        lambda value: PullRequestDraftResult(False, "github", "failed", "boom"),
    )

    result = commands._run_request_snapshot(
        provider="github", repository="owner/repo", pull_request_id=42, dry_run=False
    )

    assert result == 1
    assert '"success": false' in capsys.readouterr().out
