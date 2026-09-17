from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.adapters.pull_request_draft import PullRequestDraftRequest, PullRequestDraftResult
from agentic_devtools.cli import pull_request_draft as commands


def test_dispatches_github(monkeypatch) -> None:
    adapter = MagicMock()
    adapter.mark_draft.return_value = PullRequestDraftResult(True, "github", "updated")
    monkeypatch.setattr(commands, "GitHubPullRequestDraftAdapter", lambda: adapter)
    result = commands.dispatch_draft(PullRequestDraftRequest("github", "o/r", 1))
    assert result.success is True


def test_dispatches_azure(monkeypatch) -> None:
    calls: list[tuple[int, bool, str | None, str | None, bool]] = []

    def mark_pull_request_draft(
        *,
        pull_request_id: int,
        exit_on_error: bool,
        organization: str | None = None,
        project: str | None = None,
        dry_run: bool = False,
    ) -> None:
        calls.append((pull_request_id, exit_on_error, organization, project, dry_run))

    monkeypatch.setattr(commands, "_mark_azure_draft", mark_pull_request_draft)
    result = commands.dispatch_draft(
        PullRequestDraftRequest("azure_devops", "repo", 7, organization="org", project="proj")
    )
    assert result.success is True
    assert calls == [(7, False, "org", "proj", False)]
