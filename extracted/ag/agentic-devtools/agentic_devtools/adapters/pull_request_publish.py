"""Provider-neutral pull-request publishing contracts and transports."""

from __future__ import annotations

import os
from dataclasses import dataclass

from agentic_devtools.cli.ci.credential_roles import require_default_repo_workflow_token
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


@dataclass(frozen=True)
class PullRequestPublishRequest:
    """Validated request to make a pull request ready for review."""

    provider: str
    pull_request_id: int
    repository: str = ""
    dry_run: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.provider, str) or self.provider not in {"azure_devops", "github"}:
            raise ValueError("provider must be 'azure_devops' or 'github'")
        if not isinstance(self.repository, str):
            raise ValueError("repository is required")
        if self.provider == "github" and not self.repository.strip():
            raise ValueError("repository is required")
        if not isinstance(self.pull_request_id, int) or isinstance(self.pull_request_id, bool):
            raise ValueError("pull_request_id must be a positive integer")
        if self.pull_request_id <= 0:
            raise ValueError("pull_request_id must be a positive integer")
        if self.provider == "github" and (
            self.repository.count("/") != 1
            or any(not part.strip() or any(char.isspace() for char in part) for part in self.repository.split("/"))
        ):
            raise ValueError("GitHub repository must be in owner/repo form")
        if not isinstance(self.dry_run, bool):
            raise ValueError("dry_run must be a boolean")


@dataclass(frozen=True)
class PullRequestPublishResult:
    """Result of a provider-neutral publish operation."""

    success: bool
    provider: str
    status: str
    error: str = ""


class GitHubPullRequestPublishAdapter:
    """Mark a GitHub pull request ready for review."""

    def publish(self, request: PullRequestPublishRequest) -> PullRequestPublishResult:
        """Run ``gh pr ready`` for a validated GitHub request."""
        if request.provider != "github":
            return PullRequestPublishResult(False, request.provider, "provider_mismatch", "provider must be 'github'")
        if request.dry_run:
            return PullRequestPublishResult(True, request.provider, "dry_run")
        try:
            token = require_default_repo_workflow_token("publish the GitHub pull request")
            GitHubActionsProvider(request.repository).publish_pr(
                request.pull_request_id,
                env={**os.environ, "GH_TOKEN": token},
            )
        except ProviderRateLimitError as exc:
            return PullRequestPublishResult(False, request.provider, "rate_limited", str(exc))
        except RetryableError as exc:
            return PullRequestPublishResult(False, request.provider, "retryable_failure", str(exc))
        except (OSError, RuntimeError) as exc:
            return PullRequestPublishResult(False, request.provider, "failed", str(exc))
        return PullRequestPublishResult(True, request.provider, "published")
