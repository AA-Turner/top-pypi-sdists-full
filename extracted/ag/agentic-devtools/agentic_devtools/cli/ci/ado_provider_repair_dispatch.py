"""Azure DevOps repair dispatch stub."""

from __future__ import annotations

from agentic_devtools.cli.ci.models import CheckRunStatus, ReviewCommentInfo


class _AdoRepairDispatchMixin:
    """Provide the ADO-specific repair dispatch stub."""

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
    ) -> int:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.dispatch_repair() not yet implemented")
