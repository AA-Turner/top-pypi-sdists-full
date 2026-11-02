"""Repair task and conflict dispatch capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod

from agentic_devtools.cli.ci.models import (
    CheckRunStatus,
    ReviewCommentInfo,
)


class _ProviderRepairDispatchMixin(ABC):
    """Repair task and conflict dispatch capabilities."""

    @abstractmethod
    def dispatch_repair(
        self,
        pr_number: int,
        head_sha: str,
        repair_type: str,
        failed_checks: list[CheckRunStatus],
        review_comments: list[ReviewCommentInfo],
        review_id: int = 0,
        declared_author_comment_count: int = 0,
        declared_author_comment_counts_by_review: dict[int, int] | None = None,
        agent_task_prompt: str | None = None,
    ) -> int | str:
        """Create a repair task or authenticated @copilot trigger comment.

        Posts an authenticated ``@copilot`` comment with CI and/or review context.
        A leading ``@copilot`` reliably triggers an AI agent session.

        Args:
            pr_number: Pull request number.
            head_sha: Current HEAD SHA for the PR.
            repair_type: Type of repair (``"review"``, ``"ci"``, or ``"both"``).
            failed_checks: List of failed check runs with details.
            review_comments: Rich review comment metadata to include in the
                trigger comment.
            review_id: ID of the Copilot review that triggered the repair
                (used for the dedup marker and review URL in the comment body).
            declared_author_comment_count: Suppressed-comment count declared by the
                review body. When it exceeds the number of author comments that could
                be recovered, the dispatched comment names the shortfall so the repair
                agent can fetch the remainder from the review body.
            declared_author_comment_counts_by_review: Optional per-review declared
                suppressed-comment counts. When several prior reviews contribute to a
                repair dispatch, each affected review body gets its own shortfall
                notice and recovery fetch.
            agent_task_prompt: Optional exact prompt dispatched only through Agent Tasks.

        Returns:
            Confirmed comment ID, or a stable ``task:...`` creation receipt.
        """

    def dispatch_conflict_repair(
        self,
        pr_number: int,
        head_sha: str,
        base_sha: str,
        base_branch: str,
        head_branch: str,
    ) -> int:
        """Post a @copilot-tagged comment to resolve base-branch merge conflicts.

        The comment MUST begin with ``@copilot`` for reliable agent triggering.
        Uses ``AGDT_PR_APPROVER_PAT`` for authentication to ensure
        ``issues:write`` access.

        The dispatched instructions direct the cloud agent to merge
        ``origin/<base_branch>`` (not rebase), resolve conflicts using
        file-type-appropriate strategies, and push a normal commit —
        explicitly prohibiting ``git rebase``, ``git commit --amend``,
        ``git push --force``, and ``git push --force-with-lease``.

        Args:
            pr_number: Pull request number.
            head_sha: Current HEAD SHA of the PR branch.
            base_sha: Current tip SHA of the base branch (used in the
                idempotency marker).
            base_branch: Name of the base/target branch.
            head_branch: Name of the PR head/source branch.

        Returns:
            The ID of the posted comment.

        Raises:
            NotImplementedError: If the provider does not implement this method.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement dispatch_conflict_repair")
