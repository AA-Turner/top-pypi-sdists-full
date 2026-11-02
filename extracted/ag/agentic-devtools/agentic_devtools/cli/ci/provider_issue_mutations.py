"""Issue-comment and issue/pull-request close capabilities."""

from __future__ import annotations

from abc import ABC


class _ProviderIssueMutationsMixin(ABC):
    """Issue-comment and issue/pull-request close capabilities."""

    def post_issue_comment(self, issue_number: int, body: str) -> int:
        """Post a comment on an issue.

        Args:
            issue_number: Issue number to comment on.
            body: Comment body.

        Returns:
            The created comment ID.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: add a work item comment.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement post_issue_comment")

    def post_issue_comment_as_bookkeeping_token(self, issue_number: int, body: str) -> int:
        """Post an issue comment with the verified AI PR Loop bookkeeping identity."""
        raise NotImplementedError(f"{type(self).__name__} does not implement post_issue_comment_as_bookkeeping_token")

    def close_issue(self, issue_number: int, *, reason: str = "completed") -> None:
        """Close an issue.

        Args:
            issue_number: Issue number to close.
            reason: Platform close reason (``"completed"`` or ``"not_planned"``).

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: transition the work item to a closed state.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement close_issue")

    def close_pr(self, pr_number: int, *, comment: str | None = None) -> None:
        """Close a pull request without merging it.

        Args:
            pr_number: PR number to close.
            comment: Optional comment posted before closing.

        Raises:
            NotImplementedError: If the provider does not support this operation.

        Azure DevOps equivalent: abandon the pull request.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement close_pr")
