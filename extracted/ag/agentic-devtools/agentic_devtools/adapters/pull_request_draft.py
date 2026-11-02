"""Provider-neutral pull-request draft-state adapters."""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from agentic_devtools.cli.ci.credential_roles import require_default_repo_workflow_token
from agentic_devtools.cli.subprocess_utils import run_safe

_GITHUB_CLI_TIMEOUT_SECONDS = 30


@dataclass(frozen=True)
class PullRequestDraftRequest:
    """Validated request to mark a pull request as draft."""

    provider: str
    repository: str
    pull_request_id: int
    dry_run: bool = False
    organization: str | None = None
    project: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.provider, str) or self.provider not in {"azure_devops", "github"}:
            raise ValueError("provider must be 'azure_devops' or 'github'")
        if not isinstance(self.repository, str) or not self.repository.strip():
            raise ValueError("repository is required")
        if self.provider == "github" and (
            self.repository.count("/") != 1
            or any(not part.strip() or any(char.isspace() for char in part) for part in self.repository.split("/"))
        ):
            raise ValueError("GitHub repository must be in owner/repo form")
        if not isinstance(self.pull_request_id, int) or isinstance(self.pull_request_id, bool):
            raise ValueError("pull_request_id must be a positive integer")
        if self.pull_request_id <= 0:
            raise ValueError("pull_request_id must be a positive integer")
        if not isinstance(self.dry_run, bool):
            raise ValueError("dry_run must be a boolean")
        if self.organization is not None and (not isinstance(self.organization, str) or not self.organization.strip()):
            raise ValueError("organization must be a non-empty string")
        if self.project is not None and (not isinstance(self.project, str) or not self.project.strip()):
            raise ValueError("project must be a non-empty string")


@dataclass(frozen=True)
class PullRequestDraftResult:
    """Result of marking a pull request as draft."""

    success: bool
    provider: str
    status: str
    error: str = ""


class AzureDevOpsPullRequestDraftAdapter:
    """Delegate Azure DevOps draft changes to the existing command."""

    provider = "azure_devops"

    def __init__(self, toggle_fn: Callable[[PullRequestDraftRequest], Any]) -> None:
        self._toggle_fn = toggle_fn

    def mark_draft(self, request: PullRequestDraftRequest) -> PullRequestDraftResult:
        """Mark an Azure DevOps pull request as draft."""
        if request.provider != self.provider:
            return PullRequestDraftResult(False, request.provider, "failed", "provider mismatch")
        if request.dry_run:
            return PullRequestDraftResult(True, request.provider, "dry_run")
        try:
            self._toggle_fn(request)
        except Exception as exc:
            return PullRequestDraftResult(False, request.provider, "failed", str(exc)[:1000])
        return PullRequestDraftResult(True, request.provider, "updated")


class GitHubPullRequestDraftAdapter:
    """Mark a GitHub pull request as draft using the GitHub CLI."""

    provider = "github"

    def __init__(self, run_fn: Callable[..., Any] = run_safe) -> None:
        self._run_fn = run_fn

    def mark_draft(self, request: PullRequestDraftRequest) -> PullRequestDraftResult:
        """Convert a GitHub pull request to draft."""
        if request.provider != self.provider:
            return PullRequestDraftResult(False, request.provider, "failed", "provider mismatch")
        if request.dry_run:
            return PullRequestDraftResult(True, request.provider, "dry_run")
        try:
            token = require_default_repo_workflow_token("mark the GitHub pull request as draft")
        except RuntimeError as exc:
            return PullRequestDraftResult(False, request.provider, "failed", str(exc)[:1000])
        command = [
            "gh",
            "pr",
            "ready",
            "--undo",
            str(request.pull_request_id),
            "--repo",
            request.repository,
        ]
        try:
            result = self._run_fn(
                command,
                capture_output=True,
                text=True,
                shell=False,
                timeout=_GITHUB_CLI_TIMEOUT_SECONDS,
                env={**os.environ, "GH_TOKEN": token},
            )
        except Exception as exc:
            return PullRequestDraftResult(False, request.provider, "failed", str(exc)[:1000])
        if result.returncode != 0:
            error = (result.stderr or "").strip() or f"gh pr ready exited with status {result.returncode}"
            return PullRequestDraftResult(False, request.provider, "failed", error[:1000])
        if "already" in (result.stderr or "").lower():
            return PullRequestDraftResult(True, request.provider, "no-op")
        return PullRequestDraftResult(True, request.provider, "updated")
