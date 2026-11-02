"""Suppressed-review deferral capabilities."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult


class _ProviderDeferralsMixin(ABC):
    """Suppressed-review deferral capabilities."""

    def find_deferral_issue(self, *, pr_number: int, review_id: int) -> int | None:
        """Return the open deferral issue already filed for ``(pr_number, review_id)``.

        Makes :meth:`create_deferral_issue` recoverable: when a previous run created
        the issue but failed before its PR marker was posted, the next run must reuse
        that issue instead of filing a duplicate.

        Args:
            pr_number: PR whose suppressed comments are being deferred.
            review_id: Copilot review the suppressed comments were raised by.

        Returns:
            Issue number/ID of the matching open deferral issue, or ``None`` when no
            such issue exists.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: query work items carrying the deferral tag and match
        the same marker payload.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement find_deferral_issue")

    def create_deferral_issue(
        self,
        *,
        pr_number: int,
        review_id: int,
        base_sha: str,
        findings: list[tuple[str, str]],
        labels: list[str],
    ) -> int:
        """Create the follow-up triage issue for a deferred suppressed-only review.

        The issue body is the input contract consumed by the
        ``agdt.suppressed-comment-triage.evaluate`` agent (see
        ``docs/suppressed-comment-triage-contract.md``).

        Args:
            pr_number: PR whose suppressed comments are being deferred.
            review_id: Copilot review the suppressed comments were raised by.
            base_sha: Commit SHA the findings were raised against.
            findings: ``(path, comment_body)`` pairs, in review-body order.
            labels: Labels to apply at creation.

        Returns:
            Created issue number/ID.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: create a work item carrying the same body and tags.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement create_deferral_issue")

    def dispatch_suppressed_triage(
        self,
        *,
        issue_number: int,
        pr_number: int,
        review_id: int,
    ) -> AgentAssignmentResult:
        """Dispatch the suppressed-comment triage agent onto a deferral issue.

        Args:
            issue_number: Deferral issue used as the dispatch surface.
            pr_number: PR the deferred findings came from.
            review_id: Copilot review the deferred findings came from.

        Returns:
            Structured assignment result, including method/task metadata.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: trigger the provider's coding-agent assignment flow.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement dispatch_suppressed_triage")

    def count_open_issues_with_label(self, label: str) -> int:
        """Return the number of open issues carrying *label*.

        Used as the deferral circuit breaker: the loop refuses to create another
        deferral issue while the open backlog is at its ceiling.

        Args:
            label: Label name to filter on.

        Returns:
            Count of open issues carrying the label.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: query open work items by tag and return the count.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement count_open_issues_with_label")
