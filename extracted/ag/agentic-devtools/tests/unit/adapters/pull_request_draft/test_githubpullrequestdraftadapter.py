from __future__ import annotations

from types import SimpleNamespace
from typing import cast

import pytest

from agentic_devtools.adapters.pull_request_draft import (
    GitHubPullRequestDraftAdapter,
    PullRequestDraftRequest,
)


def test_marks_draft_with_gh(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "secret-token")
    calls: list[tuple[list[str], bool, object, dict[str, object]]] = []

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        env = cast(dict[str, object], kwargs["env"])
        calls.append((command, kwargs["shell"] is False, kwargs.get("timeout"), dict(env)))
        return SimpleNamespace(returncode=0, stderr="")

    result = GitHubPullRequestDraftAdapter(run).mark_draft(PullRequestDraftRequest("github", "o/r", 8))
    assert result.success is True
    assert result.status == "updated"
    assert calls[0][0] == ["gh", "pr", "ready", "--undo", "8", "--repo", "o/r"]
    assert calls[0][1] is True
    assert calls[0][2] == 30
    assert calls[0][3]["GH_TOKEN"] == "secret-token"


def test_reports_no_op_when_already_draft(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "secret-token")

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(returncode=0, stderr='! pull request #8 is already "in draft"\n')

    result = GitHubPullRequestDraftAdapter(run).mark_draft(PullRequestDraftRequest("github", "o/r", 8))
    assert result.success is True
    assert result.status == "no-op"


def test_reports_gh_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "secret-token")

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(returncode=1, stderr="permission denied")

    result = GitHubPullRequestDraftAdapter(run).mark_draft(PullRequestDraftRequest("github", "o/r", 8))
    assert result.success is False
    assert result.status == "failed"
    assert result.error == "permission denied"


def test_reports_gh_failure_with_empty_stderr(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "secret-token")

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(returncode=1, stderr="")

    result = GitHubPullRequestDraftAdapter(run).mark_draft(PullRequestDraftRequest("github", "o/r", 8))
    assert result.success is False
    assert result.status == "failed"
    assert result.error == "gh pr ready exited with status 1"


def test_dry_run_does_not_run_gh() -> None:
    result = GitHubPullRequestDraftAdapter(lambda *_args, **_kwargs: None).mark_draft(
        PullRequestDraftRequest("github", "o/r", 8, dry_run=True)
    )
    assert result.status == "dry_run"


def test_returns_failure_when_gh_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "secret-token")

    def run(*_args, **_kwargs):
        raise RuntimeError("not installed")

    result = GitHubPullRequestDraftAdapter(run).mark_draft(PullRequestDraftRequest("github", "o/r", 8))
    assert result.success is False
    assert result.error == "not installed"


def test_rejects_mismatched_provider_request() -> None:
    def run(*_args, **_kwargs):
        raise AssertionError("gh must not be invoked for a mismatched provider")

    request = PullRequestDraftRequest("azure_devops", "org/proj/repo", 8)
    result = GitHubPullRequestDraftAdapter(run).mark_draft(request)
    assert result.success is False
    assert result.provider == "azure_devops"
    assert result.error == "provider mismatch"


def test_fails_when_no_workflow_token_available(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", raising=False)

    def run(*_args, **_kwargs):
        raise AssertionError("gh must not be invoked without a resolved token")

    result = GitHubPullRequestDraftAdapter(run).mark_draft(PullRequestDraftRequest("github", "o/r", 8))
    assert result.success is False
    assert result.status == "failed"
    assert "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT" in result.error
