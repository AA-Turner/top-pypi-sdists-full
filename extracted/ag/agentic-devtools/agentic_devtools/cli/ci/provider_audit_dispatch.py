"""Pull-request and audit-evaluation creation capabilities."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.agent_assignment import AgentAssignmentResult


class _ProviderAuditDispatchMixin(ABC):
    """Pull-request and audit-evaluation creation capabilities."""

    def create_pull_request(
        self,
        title: str,
        body: str,
        *,
        draft: bool = True,
    ) -> str:
        """Create a pull request on the current branch.

        Args:
            title: PR title.
            body: PR body/description (Markdown).
            draft: Whether to create the PR as a draft (default True).

        Returns:
            URL of the created PR, or empty string on failure.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: ``POST /pullRequests`` with ``isDraft=True``.
        The return value should be the PR web URL.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement create_pull_request")

    def create_audit_tracking_issue(self, *, batch_id: str, pr_numbers: list[int]) -> int:
        """Create a per-batch tracking issue for review-feedback audit.

        Args:
            batch_id: Audit batch identifier.
            pr_numbers: PR numbers included in the batch.

        Returns:
            Created issue number/ID.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Create a work item (for example a Task)
        containing the batch summary and return the work item ID.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement create_audit_tracking_issue")

    def dispatch_audit_evaluation(
        self,
        *,
        tracking_issue: int,
        batch_id: str,
        batch_branch: str,
        batch_dir: str,
        pr_numbers: list[int],
    ) -> AgentAssignmentResult:
        """Dispatch the review-feedback audit evaluation agent.

        Args:
            tracking_issue: Tracking issue ID/number used as dispatch surface.
            batch_id: Audit batch identifier.
            batch_branch: Branch containing the prepared batch files.
            batch_dir: Repo-relative batch directory path.
            pr_numbers: PR numbers included in the batch.

        Returns:
            Structured assignment result, including method/task metadata.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: Trigger the provider's coding-agent assignment
        flow and return equivalent assignment metadata.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement dispatch_audit_evaluation")
