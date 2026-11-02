"""Pull-request lifecycle and file/check capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.models import ClosingIssue

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.initial_delivery_claims import InitialDeliveryClaims


class _ProviderPrLifecycleMixin(ABC):
    """Pull-request lifecycle and file/check capabilities."""

    def _get_initial_delivery_claims(self) -> InitialDeliveryClaims:
        """Return durable, cross-worker claims when supported; never a local lock."""
        raise NotImplementedError("Provider does not support durable initial-delivery claims")

    @abstractmethod
    def approve_pr(self, pr_number: int, head_sha: str, body: str) -> bool:
        """Approve a pull request.

        Args:
            pr_number: Pull request number.
            head_sha: Expected HEAD SHA (for safety check).
            body: Approval comment body.

        Returns:
            ``True`` when approval was posted, ``False`` when intentionally skipped.
        """

    def get_pr_body(self, pr_number: int) -> str:
        """Return the pull request description when the provider supports it."""
        return ""

    def update_pr_title(self, pr_number: int, title: str) -> None:
        """Update a pull request title when supported by the provider."""
        raise NotImplementedError(f"{type(self).__name__} does not implement update_pr_title")

    def list_closing_issues(self, pr_number: int) -> list[ClosingIssue]:
        """List linked issues configured to be closed by the pull request."""
        return []

    @abstractmethod
    def merge_pr(self, pr_number: int, head_sha: str, method: str, *, commit_title: str | None = None) -> None:
        """Merge a pull request.

        Args:
            pr_number: Pull request number.
            head_sha: Expected HEAD SHA (for safety check).
            method: Merge method (e.g., "squash", "merge", "rebase").
            commit_title: Optional squash commit title (subject line only).
        """

    @abstractmethod
    def delete_branch(self, branch: str) -> None:
        """Delete a remote branch.

        Args:
            branch: Branch name to delete (e.g., "feature/my-branch").

        Raises:
            RuntimeError: If the branch could not be deleted.
        """

    @abstractmethod
    def publish_pr(self, pr_number: int) -> None:
        """Mark a draft pull request as ready for review.

        Args:
            pr_number: Pull request number.
        """

    @abstractmethod
    def squash_before_publish(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> None:
        """Squash or otherwise normalize a draft branch before publish.

        Implementations may perform provider-specific history normalization
        before publish and force-push the prepared branch when needed.
        Single-commit branches should remain a safe no-op for the squash phase
        while still ensuring the branch is pushed.
        """

    @abstractmethod
    def list_pr_files(self, pr_number: int) -> list[str]:
        """List files changed in a pull request.

        Args:
            pr_number: Pull request number.

        Returns:
            List of file paths changed in the PR.
        """

    @abstractmethod
    def get_check_annotations(self, check_run_id: int, limit: int) -> list[str]:
        """Get annotations from a check run.

        Args:
            check_run_id: ID of the check run.
            limit: Maximum number of annotations to return.

        Returns:
            List of annotation messages.
        """
