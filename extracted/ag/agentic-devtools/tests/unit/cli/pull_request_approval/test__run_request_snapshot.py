from __future__ import annotations

from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalResult
from agentic_devtools.cli import pull_request_approval as commands


def test_returns_success_status(monkeypatch) -> None:
    monkeypatch.setattr(
        commands,
        "dispatch_pull_request_approval",
        lambda _: PullRequestApprovalResult(True, "github", "approved"),
    )
    assert (
        commands._run_request_snapshot(
            provider="github", repository="owner/repo", pull_request_id=1, content="x", expected_head="a" * 40
        )
        == 0
    )


def test_returns_failure_status(monkeypatch) -> None:
    monkeypatch.setattr(
        commands,
        "dispatch_pull_request_approval",
        lambda _: PullRequestApprovalResult(False, "github", "failed"),
    )
    assert (
        commands._run_request_snapshot(
            provider="github", repository="owner/repo", pull_request_id=1, content="x", expected_head="a" * 40
        )
        == 1
    )
