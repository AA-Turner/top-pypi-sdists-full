from __future__ import annotations

from agentic_devtools.adapters.pull_request_approval import (
    AzureDevOpsPullRequestApprovalAdapter,
    PullRequestApprovalRequest,
)


def test_delegates_to_existing_azure_approval() -> None:
    calls: list[PullRequestApprovalRequest] = []
    adapter = AzureDevOpsPullRequestApprovalAdapter(calls.append)
    request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        1,
        "LGTM",
        organization="https://dev.azure.com/example",
        project="project",
    )
    result = adapter.approve(request)
    assert result.success is True
    assert result.status == "approved"
    assert calls == [request]


def test_dry_run_does_not_delegate() -> None:
    calls: list[PullRequestApprovalRequest] = []
    adapter = AzureDevOpsPullRequestApprovalAdapter(calls.append)
    request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        1,
        "LGTM",
        dry_run=True,
        organization="https://dev.azure.com/example",
        project="project",
    )
    result = adapter.approve(request)
    assert result.status == "dry_run"
    assert calls == []


def test_rejects_provider_mismatch() -> None:
    adapter = AzureDevOpsPullRequestApprovalAdapter(lambda: None)
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "provider_mismatch"


def test_unresolved_fallback_thread_is_reported_as_failure() -> None:
    """An outcome with resolved=False must not be reported as a successful task."""
    from agentic_devtools.cli.azure_devops.commands import AzureApprovalOutcome

    adapter = AzureDevOpsPullRequestApprovalAdapter(lambda _request: AzureApprovalOutcome(resolved=False, thread_id=7))
    request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        1,
        "LGTM",
        organization="https://dev.azure.com/example",
        project="project",
    )
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "approved_unresolved_thread"
    assert result.external_id == 7
    assert "could not be resolved" in result.error


def test_resolved_outcome_carries_thread_id() -> None:
    """A resolved fallback outcome reports success with the thread ID."""
    from agentic_devtools.cli.azure_devops.commands import AzureApprovalOutcome

    adapter = AzureDevOpsPullRequestApprovalAdapter(
        lambda _request: AzureApprovalOutcome(resolved=True, thread_id=9, operation_kind="fallback_comment")
    )
    request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        1,
        "LGTM",
        organization="https://dev.azure.com/example",
        project="project",
    )
    result = adapter.approve(request)
    assert result.success is True
    assert result.status == "approved"
    assert result.external_id == 9
    assert result.verified is True
    assert result.operation_kind == "fallback_comment"


def test_narrative_outcome_identifies_operation_kind() -> None:
    """A narrative update is explicitly distinguishable from a fallback comment."""
    from agentic_devtools.cli.azure_devops.commands import AzureApprovalOutcome

    adapter = AzureDevOpsPullRequestApprovalAdapter(
        lambda _request: AzureApprovalOutcome(resolved=True, operation_kind="narrative_update")
    )
    request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        1,
        "LGTM",
        organization="https://dev.azure.com/example",
        project="project",
    )

    result = adapter.approve(request)

    assert result.status == "approved"
    assert result.external_id is None
    assert result.operation_kind == "narrative_update"


def test_calls_zero_argument_legacy_delegate_without_request() -> None:
    """A delegate whose signature accepts no positional parameters is called with no arguments."""
    calls: list[tuple[object, ...]] = []

    def _legacy_approve_fn() -> None:
        calls.append(())

    adapter = AzureDevOpsPullRequestApprovalAdapter(_legacy_approve_fn)
    request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        1,
        "LGTM",
        organization="https://dev.azure.com/example",
        project="project",
    )
    result = adapter.approve(request)
    assert result.success is True
    assert result.status == "approved"
    assert calls == [()]


def test_signature_inspection_failure_is_reported_as_approval_failure() -> None:
    """A delegate whose signature cannot be inspected is reported as a failure, not called."""

    class _Uninspectable:
        def __call__(self, *args: object, **kwargs: object) -> None:  # pragma: no cover - must not run
            raise AssertionError("delegate must not be invoked when its signature can't be inspected")

        def __signature__(self) -> None:
            raise ValueError("no signature found")

    adapter = AzureDevOpsPullRequestApprovalAdapter(_Uninspectable())
    request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        1,
        "LGTM",
        organization="https://dev.azure.com/example",
        project="project",
    )
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "approval_failed"


def test_approve_fn_exception_is_sanitized(monkeypatch) -> None:
    """An exception raised by the delegate is caught and its message sanitized."""

    monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "super-secret-token")

    def _boom(_request: PullRequestApprovalRequest) -> None:
        raise RuntimeError("failed with token super-secret-token")

    adapter = AzureDevOpsPullRequestApprovalAdapter(_boom)
    request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        1,
        "LGTM",
        organization="https://dev.azure.com/example",
        project="project",
    )
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "approval_failed"
    assert "super-secret-token" not in result.error
    assert "[REDACTED]" in result.error
