"""Critique-specific data loaded into the AI PR loop snapshot."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TypedDict

from agentic_devtools.cli.ci.critique_adjudicator import (
    classify_critique_headline,
    parse_critique_adjudications,
    parse_critique_tasks,
)
from agentic_devtools.cli.ci.guards import find_repair_satisfied_review_id
from agentic_devtools.cli.ci.models import IssueCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.deferral import find_suppressed_deferral_state
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_CLEAN, REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict
from agentic_devtools.cli.ci.provider import CIPlatformProvider, trusted_loop_comment_logins
from agentic_devtools.cli.ci.retry import ProviderRateLimitError
from agentic_devtools.cli.github.ccr_headline import parse_ccr_overview_summary

logger = logging.getLogger(__name__)


class CritiqueSnapshotKwargs(TypedDict):
    critique_task_state_available: bool
    critique_adjudicated_review_id: int | None
    critique_adjudicated_head_sha: str
    critique_adjudicated_headline: str
    critique_adjudicated_verdict: str
    critique_followup_instruction: str
    critique_headline_classification: str


@dataclass(frozen=True, kw_only=True)
class CritiqueSnapshotFields:
    """Adjudication and headline state inherited by the PR snapshot."""

    critique_task_state_available: bool = True
    critique_adjudicated_review_id: int | None = None
    critique_adjudicated_head_sha: str = ""
    critique_adjudicated_headline: str = ""
    critique_adjudicated_verdict: str = ""
    critique_followup_instruction: str = ""
    critique_headline_classification: str = ""

    def as_kwargs(self) -> CritiqueSnapshotKwargs:
        return {
            "critique_task_state_available": self.critique_task_state_available,
            "critique_adjudicated_review_id": self.critique_adjudicated_review_id,
            "critique_adjudicated_head_sha": self.critique_adjudicated_head_sha,
            "critique_adjudicated_headline": self.critique_adjudicated_headline,
            "critique_adjudicated_verdict": self.critique_adjudicated_verdict,
            "critique_followup_instruction": self.critique_followup_instruction,
            "critique_headline_classification": self.critique_headline_classification,
        }


def should_load_issue_comment_critique_state(verdict: CopilotGateVerdict, current_overview_headline: str) -> bool:
    """Load trusted task state for a blocked review or any eligible current-head overview."""
    return not verdict.passed or bool(current_overview_headline)


def current_zero_findings_headline(
    verdict: CopilotGateVerdict | None,
    reviews: list[ReviewInfo],
    current_head_sha: str,
    head_changed_since_review: bool,
    effective_review_comment_count: int | None,
    effective_review_comment_count_review_id: int | None,
    effective_review_comment_filter_applied: bool | None,
) -> tuple[str, str]:
    """Return the eligible current-head headline and semantic classification."""
    if (
        verdict is None
        or (verdict.passed and verdict.reason != REASON_CLEAN)
        or (not verdict.passed and verdict.reason != REASON_NEW_CCR_NOT_APPROVED)
    ):
        return "", ""
    review = next((candidate for candidate in reviews if candidate.id == verdict.review_id), None)
    overview = parse_ccr_overview_summary(review.body) if review is not None else None
    if (
        verdict.body_comment_count not in (None, 0)
        or verdict.suppressed_count != 0
        or head_changed_since_review
        or not current_head_sha
        or review is None
        or review.commit_sha != current_head_sha
        or overview is None
        or not overview[0]
        or overview[1] is None
    ):
        return "", ""
    if (
        effective_review_comment_count_review_id == verdict.review_id
        and effective_review_comment_filter_applied is not None
        and effective_review_comment_count is not None
        and effective_review_comment_count != 0
    ):
        return "", ""
    return overview[1], classify_critique_headline(overview[1]).verdict


def initial_critique_snapshot_state(
    verdict: CopilotGateVerdict | None,
    reviews: list[ReviewInfo],
    current_head_sha: str,
    head_changed_since_review: bool,
    effective_review_comment_count: int | None,
    effective_review_comment_count_review_id: int | None,
    effective_review_comment_filter_applied: bool | None,
) -> tuple[int | None, str, CritiqueSnapshotFields]:
    """Return the current headline with its default classification fields."""
    headline, classification = current_zero_findings_headline(
        verdict,
        reviews,
        current_head_sha,
        head_changed_since_review,
        effective_review_comment_count,
        effective_review_comment_count_review_id,
        effective_review_comment_filter_applied,
    )
    return None, headline, CritiqueSnapshotFields(critique_headline_classification=classification)


def load_issue_comment_critique_state(
    provider: CIPlatformProvider,
    pr_number: int,
    issue_comments: list[IssueCommentInfo],
    reviews: list[ReviewInfo],
    current_head_sha: str,
    verdict: CopilotGateVerdict,
    headline: str,
    classification: str,
    extra_authors: frozenset[str] | None,
) -> tuple[int | None, int | None, int | None, CritiqueSnapshotFields]:
    """Load existing gate markers before best-effort critique task state."""
    repair_satisfied_review_id = find_repair_satisfied_review_id(issue_comments)
    deferral_review_id, deferral_issue_number = find_suppressed_deferral_state(issue_comments, extra_authors)
    try:
        fields = load_critique_snapshot_fields(
            provider,
            pr_number,
            issue_comments,
            reviews,
            current_head_sha,
            verdict,
            headline,
            classification,
        )
    except Exception as exc:
        if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
            raise
        logger.warning("PR #%d: Failed to load critique task state: %s", pr_number, str(exc)[:200])
        fields = CritiqueSnapshotFields(
            critique_headline_classification=classification,
            critique_task_state_available=False,
        )
    return repair_satisfied_review_id, deferral_review_id, deferral_issue_number, fields


def load_critique_snapshot_fields(
    provider: CIPlatformProvider,
    pr_number: int,
    issue_comments: list[IssueCommentInfo],
    reviews: list[ReviewInfo],
    current_head_sha: str,
    verdict: CopilotGateVerdict,
    headline: str,
    classification: str,
) -> CritiqueSnapshotFields:
    """Resolve trusted task and adjudication markers for the current HEAD."""
    trusted_logins = trusted_loop_comment_logins(provider)
    records = parse_critique_adjudications(
        issue_comments,
        trusted_logins=trusted_logins,
        pr_number=pr_number,
    )
    tasks = parse_critique_tasks(
        issue_comments,
        trusted_logins=trusted_logins,
        pr_number=pr_number,
        head_sha=current_head_sha,
    )
    if any(task.review_id == verdict.review_id for task in tasks):
        classification = "critique"
    attempts = {(task.review_id, task.attempt) for task in tasks if task.head_sha == current_head_sha}
    followup = next(
        (
            record.concrete_instruction
            for record in reversed(records)
            if record.verdict == "needs_repair"
            and record.head_sha == current_head_sha
            and record.review_id == verdict.review_id
            and record.attempt == 1
            and record.concrete_instruction
            and (record.review_id, 2) not in attempts
        ),
        "",
    )
    review_by_id = {review.id: review for review in reviews}
    adjudicated_review_id = None
    adjudicated_head_sha = ""
    adjudicated_headline = ""
    adjudicated_verdict = ""
    for record in reversed(records):
        review = review_by_id.get(record.review_id)
        overview = parse_ccr_overview_summary(review.body) if review is not None else None
        if (
            record.verdict == "rebutted"
            and record.head_sha == current_head_sha
            and record.review_id <= verdict.review_id
            and review is not None
            and review.commit_sha == current_head_sha
            and overview is not None
            and overview[0]
            and overview[1] == headline
        ):
            adjudicated_review_id = record.review_id
            adjudicated_head_sha = record.head_sha
            adjudicated_headline = headline
            adjudicated_verdict = record.verdict
            break
    return CritiqueSnapshotFields(
        critique_adjudicated_review_id=adjudicated_review_id,
        critique_adjudicated_head_sha=adjudicated_head_sha,
        critique_adjudicated_headline=adjudicated_headline,
        critique_adjudicated_verdict=adjudicated_verdict,
        critique_followup_instruction=followup or "",
        critique_headline_classification=classification,
    )
