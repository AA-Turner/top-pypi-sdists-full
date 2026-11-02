from __future__ import annotations

import os

import pytest

from agentic_devtools.adapters.pull_request_approval import (
    GitHubPullRequestApprovalAdapter,
    PullRequestApprovalRequest,
)


def test_delegates_with_pinned_head_sha() -> None:
    calls: list[tuple[object, ...]] = []

    def approve(*args: object) -> dict[str, bool]:
        calls.append(args)
        return {"approved": True, "verified": True}

    adapter = GitHubPullRequestApprovalAdapter(approve)
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is True
    assert result.status == "approved"
    assert calls == [(1, "owner/repo", "LGTM", "a" * 40)]


def test_reports_unverified_result() -> None:
    adapter = GitHubPullRequestApprovalAdapter(lambda *args: {"approved": True, "verified": False})
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "submitted_unverified"


def test_reports_submission_failure() -> None:
    adapter = GitHubPullRequestApprovalAdapter(
        lambda *args: {"approved": False, "verified": False, "message": "approval failed"}
    )
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "approval_failed"
    assert result.error == "approval failed"


def test_reports_invalid_delegate_result() -> None:
    adapter = GitHubPullRequestApprovalAdapter(lambda *args: None)
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)

    result = adapter.approve(request)

    assert result.success is False
    assert result.status == "approval_failed"
    assert result.error == "GitHub approval returned an invalid result"


def test_reports_already_approved_result() -> None:
    adapter = GitHubPullRequestApprovalAdapter(
        lambda *args: {"approved": True, "verified": True, "status": "already_approved", "reviewId": 9}
    )
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is True
    assert result.status == "already_approved"
    assert result.external_id == 9


def test_dry_run_does_not_delegate() -> None:
    calls: list[tuple[object, ...]] = []
    adapter = GitHubPullRequestApprovalAdapter(lambda *args: calls.append(args))
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40, dry_run=True)
    result = adapter.approve(request)
    assert result.status == "dry_run"
    assert calls == []


def test_default_approval_function_is_loaded() -> None:
    assert GitHubPullRequestApprovalAdapter() is not None


def test_rejects_provider_mismatch() -> None:
    adapter = GitHubPullRequestApprovalAdapter(lambda *_: {})
    request = PullRequestApprovalRequest("azure_devops", "repo", 1, "LGTM")
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "provider_mismatch"


def test_converts_systemexit_to_result() -> None:
    def approve(*args: object) -> dict[str, bool]:
        raise SystemExit(1)

    adapter = GitHubPullRequestApprovalAdapter(approve)
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "readiness_failed"
    assert "exit code 1" in result.error


def test_missing_approver_token_fails_readiness_for_default_fn(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.delenv("AGDT_PR_APPROVER_PAT", raising=False)
    adapter = GitHubPullRequestApprovalAdapter()
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "missing_approver_identity"
    assert "AGDT_PR_APPROVER_PAT" in result.error


def test_passes_approver_token_to_default_fn_without_mutating_process_env(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    import agentic_devtools.cli.github.pr_approve as pr_approve

    monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "approver-token")
    monkeypatch.setenv("GH_TOKEN", "ambient-token")
    monkeypatch.setenv("GITHUB_TOKEN", "ambient-github-token")
    seen: dict[str, object] = {}

    def fake_approve_pr(*args: object, **kwargs: object) -> dict[str, bool]:
        seen["GH_TOKEN"] = os.environ.get("GH_TOKEN")
        seen["GITHUB_TOKEN"] = os.environ.get("GITHUB_TOKEN")
        seen["env"] = kwargs.get("env")
        seen["persist_state"] = kwargs.get("persist_state")
        return {"approved": True, "verified": True}

    monkeypatch.setattr(pr_approve, "approve_pr", fake_approve_pr)
    adapter = GitHubPullRequestApprovalAdapter()
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is True
    assert seen["GH_TOKEN"] == "ambient-token"
    assert seen["GITHUB_TOKEN"] == "ambient-github-token"
    approval_env = seen["env"]
    assert isinstance(approval_env, dict)
    assert approval_env["GH_TOKEN"] == "approver-token"
    assert "GITHUB_TOKEN" not in approval_env
    assert seen["persist_state"] is False
    assert os.environ.get("GH_TOKEN") == "ambient-token"
    assert os.environ.get("GITHUB_TOKEN") == "ambient-github-token"


def test_reports_already_approved_status() -> None:
    """An existing verified approval found by the delegate is reported without resubmission."""
    adapter = GitHubPullRequestApprovalAdapter(
        lambda *args: {"approved": True, "verified": True, "status": "already_approved", "reviewId": 42}
    )
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is True
    assert result.status == "already_approved"
    assert result.external_id == 42


@pytest.mark.parametrize("verified", ["false", 1, None])
def test_requires_boolean_true_for_verified_result(verified: object) -> None:
    adapter = GitHubPullRequestApprovalAdapter(lambda *args: {"approved": True, "verified": verified})
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)

    result = adapter.approve(request)

    assert result.success is False
    assert result.verified is False
    assert result.status == "submitted_unverified"


@pytest.mark.parametrize(
    ("review_id", "expected_external_id"),
    [(True, None), (0, None), (-1, None), (9, 9)],
)
def test_normalizes_only_positive_non_boolean_review_ids(review_id: object, expected_external_id: int | None) -> None:
    adapter = GitHubPullRequestApprovalAdapter(
        lambda *args: {"approved": True, "verified": True, "reviewId": review_id}
    )
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)

    result = adapter.approve(request)

    assert result.external_id == expected_external_id


def test_submission_failure_message_is_sanitized(monkeypatch) -> None:
    """A provider-raised failure message has secrets redacted before being surfaced."""
    monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "leaked-token-value")
    adapter = GitHubPullRequestApprovalAdapter(
        lambda *args: {"approved": False, "message": "auth failed using leaked-token-value"}
    )
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is False
    assert "leaked-token-value" not in result.error
    assert "[REDACTED]" in result.error


def test_generic_exception_is_caught_and_sanitized(monkeypatch) -> None:
    """A non-SystemExit exception from the delegate is caught and its message sanitized."""
    monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "another-secret")

    def approve(*args: object) -> dict[str, bool]:
        raise RuntimeError("network error: another-secret")

    adapter = GitHubPullRequestApprovalAdapter(approve)
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "approval_failed"
    assert "another-secret" not in result.error
    assert "[REDACTED]" in result.error


def test_sanitizes_provider_diagnostics(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "super-secret")
    adapter = GitHubPullRequestApprovalAdapter(
        lambda *args: {
            "approved": False,
            "verified": False,
            "message": "token=super-secret",
            "error": "approval_failed",
        }
    )
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is False
    assert "super-secret" not in result.error
    assert "[REDACTED]" in result.error


def test_sanitizes_raised_diagnostics(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "super-secret")

    def approve(*args: object) -> dict[str, bool]:
        raise RuntimeError("token=super-secret")

    adapter = GitHubPullRequestApprovalAdapter(approve)
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    result = adapter.approve(request)
    assert result.success is False
    assert result.status == "approval_failed"
    assert "super-secret" not in result.error
    assert "[REDACTED]" in result.error
