"""GitHub IssueProvider implementation.

Uses the ``gh`` CLI for REST API calls.  All mutating calls pass
``shell=False`` to prevent ``%VAR%`` expansion on Windows when user-controlled
text is present in arguments.
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from typing import Any

from agentic_devtools.adapters.dry_run_manifest import build_dry_run_manifest
from agentic_devtools.adapters.github_provider_common import _GitHubProviderCommonMixin
from agentic_devtools.adapters.github_provider_creation import GitHubProviderCreationMixin
from agentic_devtools.adapters.github_provider_creation_lookup import GitHubProviderCreationLookupMixin
from agentic_devtools.adapters.github_provider_creation_recovery import GitHubProviderCreationRecoveryMixin
from agentic_devtools.adapters.github_provider_dependencies import GitHubProviderDependenciesMixin
from agentic_devtools.adapters.github_provider_hierarchy import (
    GitHubProviderCreationHierarchyMixin,
    GitHubProviderHierarchyMixin,
)
from agentic_devtools.adapters.github_provider_idempotency import GitHubProviderIdempotencyMixin
from agentic_devtools.adapters.github_provider_issue_types import GitHubProviderIssueTypesMixin
from agentic_devtools.adapters.github_provider_labels import GitHubProviderLabelsMixin
from agentic_devtools.adapters.github_provider_resolution import GitHubProviderResolutionMixin
from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.cli.subprocess_utils import run_safe


class GitHubProvider(
    GitHubProviderCreationMixin,
    GitHubProviderCreationLookupMixin,
    GitHubProviderCreationRecoveryMixin,
    GitHubProviderCreationHierarchyMixin,
    GitHubProviderIssueTypesMixin,
    GitHubProviderResolutionMixin,
    GitHubProviderHierarchyMixin,
    GitHubProviderDependenciesMixin,
    GitHubProviderLabelsMixin,
    GitHubProviderIdempotencyMixin,
    _GitHubProviderCommonMixin,
):
    """GitHub IssueProvider using the ``gh`` CLI for API calls.

    Args:
        owner_repo: Repository slug in ``owner/repo`` format.
        run_command: Optional callable for executing subprocess commands
            (for testing injection).
    """

    def __init__(
        self,
        owner_repo: str,
        run_command: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        normalized_owner_repo = owner_repo.strip()
        owner, sep, repo = normalized_owner_repo.partition("/")
        if not sep or not owner or not repo or "/" in repo:
            raise ValueError("owner_repo must be in 'owner/repo' format")

        self._owner_repo = normalized_owner_repo
        self._run: Callable[..., subprocess.CompletedProcess[str]] = run_command or run_safe
        self._dry_run_issues: list[dict[str, Any]] = []
        self._dry_run_deps: list[dict[str, Any]] = []
        # Per-instance cache for idempotency key → result: avoids duplicate
        # creation when GitHub search indexing lags after a fresh POST.
        self._idempotency_cache: dict[str, ProviderIssueResult] = {}

    def get_dry_run_manifest(self) -> dict[str, Any]:
        """Return the accumulated dry-run manifest."""
        return build_dry_run_manifest(
            issues=self._dry_run_issues,
            dependencies=self._dry_run_deps,
        )
