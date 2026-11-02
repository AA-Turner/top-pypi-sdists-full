"""Provider-side Agent Tasks dispatch helpers for critique repairs."""

from __future__ import annotations

from collections.abc import Callable

from agentic_devtools.cli.ci import critique_adjudicator
from agentic_devtools.cli.ci.comment_format import AI_PR_LOOP_COMMENT_LABEL
from agentic_devtools.cli.ci.models import CheckRunStatus, FailedCheckContext, ReviewCommentInfo
from agentic_devtools.cli.ci.provider import (
    CIPlatformProvider,
    RepairDispatchNotAttemptedError,
)
from agentic_devtools.cli.ci.repair_accounting import RepairDispatchLedger, repair_work_key
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


class CritiqueProviderDispatch:
    """Build and guard Agent Tasks requests for critique repairs."""

    @staticmethod
    def build_repair_body(
        provider: CIPlatformProvider,
        standard_builder: Callable[..., str],
        comment_size_enforcer: Callable[..., str],
        max_comment_body_chars: int,
        *,
        agent_task_prompt: str | None,
        head_sha: str,
        repair_type: str,
        failed_checks: list[CheckRunStatus],
        review_comments: list[ReviewCommentInfo],
        repository_full_name: str,
        pr_number: int,
        review_id: int,
        check_contexts: dict[int, FailedCheckContext],
        declared_author_comment_count: int,
        declared_author_comment_counts_by_review: dict[int, int] | None,
    ) -> str:
        """Build a contract-bound critique prompt or a standard repair comment."""
        if agent_task_prompt is not None:
            return critique_adjudicator.build_critique_repair_prompt(agent_task_prompt)
        body = standard_builder(
            head_sha=head_sha,
            repair_type=repair_type,
            failed_checks=failed_checks,
            review_comments=review_comments,
            repository_full_name=repository_full_name,
            pr_number=pr_number,
            review_id=review_id,
            check_contexts=check_contexts,
            declared_author_comment_count=declared_author_comment_count,
            declared_author_comment_counts_by_review=declared_author_comment_counts_by_review,
        )
        work_key = repair_work_key(
            review_id,
            review_comments,
            failed_checks if repair_type in ("ci", "both") else [],
            declared_author_comment_counts_by_review,
        )
        evidence = RepairDispatchLedger(provider, pr_number, head_sha, review_id, work_key).evidence_marker
        label_suffix_length = len(f"\n\n{AI_PR_LOOP_COMMENT_LABEL}")
        body = comment_size_enforcer(
            body,
            hard_limit=max_comment_body_chars - len(evidence) - 2 - label_suffix_length,
        )
        return body + f"\n\n{evidence}"

    @staticmethod
    def validate_task_dispatch(
        agent_task_prompt: str | None,
        use_agent_tasks: bool,
        repository_full_name: str,
    ) -> None:
        """Require Agent Tasks for critique prompts."""
        if agent_task_prompt is not None and (
            not use_agent_tasks or not repository_full_name or "/" not in repository_full_name
        ):
            raise RepairDispatchNotAttemptedError("Critique repair requires the Agent Tasks API and repository")

    @staticmethod
    def must_not_fallback(agent_task_prompt: str | None, exc: Exception) -> bool:
        """Prevent critique and rate-limit errors from falling back to comments."""
        return agent_task_prompt is not None or (isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit)
