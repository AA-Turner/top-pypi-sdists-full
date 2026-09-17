from __future__ import annotations

from agentic_devtools.adapters.pull_request_draft import (
    AzureDevOpsPullRequestDraftAdapter,
    PullRequestDraftRequest,
)


def test_delegates_to_existing_toggle() -> None:
    calls: list[PullRequestDraftRequest] = []
    adapter = AzureDevOpsPullRequestDraftAdapter(lambda request: calls.append(request))
    request = PullRequestDraftRequest("azure_devops", "repo", 7)
    result = adapter.mark_draft(request)
    assert calls == [request]
    assert result.success is True
    assert result.status == "updated"


def test_delegates_captured_organization_and_project() -> None:
    calls: list[PullRequestDraftRequest] = []
    adapter = AzureDevOpsPullRequestDraftAdapter(lambda request: calls.append(request))
    request = PullRequestDraftRequest("azure_devops", "repo", 7, organization="org", project="proj")
    adapter.mark_draft(request)
    assert calls[0].organization == "org"
    assert calls[0].project == "proj"


def test_dry_run_does_not_delegate() -> None:
    calls: list[PullRequestDraftRequest] = []
    adapter = AzureDevOpsPullRequestDraftAdapter(lambda request: calls.append(request))
    result = adapter.mark_draft(PullRequestDraftRequest("azure_devops", "repo", 7, dry_run=True))
    assert calls == []
    assert result.status == "dry_run"


def test_returns_failure_when_toggle_raises() -> None:
    def toggle(_: PullRequestDraftRequest) -> None:
        raise RuntimeError("failed")

    result = AzureDevOpsPullRequestDraftAdapter(toggle).mark_draft(PullRequestDraftRequest("azure_devops", "repo", 7))
    assert result.success is False
    assert result.error == "failed"


def test_rejects_mismatched_provider_request() -> None:
    def toggle(_: PullRequestDraftRequest) -> None:
        raise AssertionError("toggle_fn must not be invoked for a mismatched provider")

    request = PullRequestDraftRequest("github", "o/r", 7)
    result = AzureDevOpsPullRequestDraftAdapter(toggle).mark_draft(request)
    assert result.success is False
    assert result.provider == "github"
    assert result.error == "provider mismatch"
