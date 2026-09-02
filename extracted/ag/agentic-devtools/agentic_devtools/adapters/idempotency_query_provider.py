"""IdempotencyQueryProvider protocol for adapter-level existence queries.

Separated from ``IssueProvider`` (which has exactly 8 methods) to avoid
a breaking change to the mutation protocol.  Used by the orchestrator
when ``dry_run=True`` and ``check_existing=True``.

All ``*_provider_id`` parameters accept provider-native string identifiers
(e.g., ``"42"`` for GitHub, ``"PROJ-123"`` for Jira).
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from agentic_devtools.adapters.issue_provider import ProviderIssueResult, ProviderLinkResult


@runtime_checkable
class IdempotencyQueryProvider(Protocol):
    """Companion protocol for adapter-level idempotency queries.

    Separated from IssueProvider (which has exactly 8 methods) to avoid
    a breaking change to the mutation protocol. Used by the orchestrator
    when dry_run=True and check_existing=True.

    All *_provider_id parameters accept provider-native string identifiers
    (e.g., "42" for GitHub, "PROJ-123" for Jira).
    """

    def find_existing_issue(
        self,
        orchestration_key: str,
    ) -> ProviderIssueResult | None:
        """Find an issue by its embedded orchestration key.

        Returns ProviderIssueResult with status="existing" if found,
        None if not found. Raises ValueError if multiple matches found
        (ambiguous state — FR-008).
        """
        ...  # pragma: no cover

    def find_existing_link(
        self,
        parent_provider_id: str,
        child_provider_id: str,
    ) -> ProviderLinkResult | None:
        """Check if a parent-child link already exists.

        Returns ProviderLinkResult with status="already-linked" if found,
        None if not found.
        """
        ...  # pragma: no cover

    def find_existing_dependency(
        self,
        issue_provider_id: str,
        blocked_by_provider_id: str,
    ) -> ProviderLinkResult | None:
        """Check if a blocking dependency already exists.

        Returns ProviderLinkResult with status="already-linked" if found,
        None if not found.
        """
        ...  # pragma: no cover
