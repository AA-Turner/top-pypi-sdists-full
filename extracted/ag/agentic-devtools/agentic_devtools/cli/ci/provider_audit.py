"""Review-feedback audit query and claim capabilities."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.models import ReviewCommentInfo

if TYPE_CHECKING:
    from agentic_devtools.cli.audit.models import (
        ClaimResult,
        ClosedPRInfo,
    )


class _ProviderAuditMixin(ABC):
    """Review-feedback audit query and claim capabilities."""

    def list_closed_prs(
        self,
        *,
        exclude_labels: list[str],
        limit: int,
        state: str = "closed",
    ) -> list[ClosedPRInfo]:
        """List closed PRs excluding those with specified labels.

        Returns newest-closed PRs first (sorted by ``closed_at`` descending).

        Args:
            exclude_labels: Labels to exclude from results.
            limit: Maximum number of PRs to return.
            state: PR state filter (default "closed").

        Returns:
            List of ``ClosedPRInfo`` dataclass instances.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Use ``GitPullRequestSearchCriteria`` with
        ``status=completed|abandoned`` and filter by tag absence. Sort by
        ``closedDate`` descending.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_closed_prs")

    def claim_pr_for_audit(self, pr_number: int, label: str) -> ClaimResult:
        """Attempt to claim a PR for audit by adding a label.

        Uses a GET-then-POST pattern: checks if the label is already
        present, then adds it if absent. Returns the claim result.

        This is best-effort, not atomic — concurrent runs may both observe
        the label absent and both proceed. Idempotency and deduplication
        are enforced downstream.

        Args:
            pr_number: PR number to claim.
            label: Label to add as the claim marker.

        Returns:
            ``ClaimResult.CLAIMED`` if newly added,
            ``ClaimResult.ALREADY_CLAIMED`` if already present.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Use PR tags (``GET /pullRequests/{id}/labels``
        then ``POST /pullRequests/{id}/labels``). Handle 409 Conflict as
        ALREADY_CLAIMED.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement claim_pr_for_audit")

    def add_label(self, pr_number: int, label: str) -> None:
        """Add a label to a PR (idempotent).

        If the label is already present, this is a no-op.

        Args:
            pr_number: PR number.
            label: Label name to add.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: ``POST /pullRequests/{id}/labels`` with the
        tag name. Handle 409 as success (already exists).
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement add_label")

    def remove_label(self, pr_number: int, label: str) -> None:
        """Remove a label from a PR (idempotent).

        If the label is not present, this is a no-op.

        Args:
            pr_number: PR number.
            label: Label name to remove.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: ``DELETE /pullRequests/{id}/labels/{labelId}``.
        Handle 404 as success (already absent).
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement remove_label")

    def count_prs_without_labels(
        self,
        *,
        exclude_labels: list[str],
        state: str = "closed",
    ) -> int:
        """Count closed PRs that do NOT have any of the specified labels.

        Used for threshold checks before triggering an audit batch.

        Args:
            exclude_labels: Labels whose absence qualifies a PR for counting.
            state: PR state filter (default "closed").

        Returns:
            Count of matching PRs.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Use search criteria with tag exclusion
        and count the results.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement count_prs_without_labels")

    def list_all_review_comments(self, pr_number: int) -> list[ReviewCommentInfo]:
        """List ALL review comments for a PR (across all reviews).

        Unlike ``list_review_comments()`` which requires a specific review ID,
        this method returns all inline review comments for the PR regardless
        of which review they belong to. Pagination is handled internally.

        Args:
            pr_number: PR number.

        Returns:
            List of ReviewCommentInfo for all review comments.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: ``GET /pullRequests/{id}/threads`` with
        ``threadContext`` filtering for inline comments.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_all_review_comments")
