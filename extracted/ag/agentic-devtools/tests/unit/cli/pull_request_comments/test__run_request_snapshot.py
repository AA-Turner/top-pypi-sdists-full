"""Tests for the immutable background request worker."""

from __future__ import annotations

from agentic_devtools.adapters.pull_request_comments import PullRequestCommentResult
from agentic_devtools.cli import pull_request_comments as commands


def test_returns_nonzero_for_failed_snapshot(monkeypatch) -> None:
    result = PullRequestCommentResult(False, "github", "failed", error="no")
    monkeypatch.setattr(commands, "dispatch_pull_request_comment", lambda _: result)
    assert (
        commands._run_request_snapshot(provider="github", repository="owner/repo", pull_request_id=1, content="x") == 1
    )
