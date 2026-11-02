"""Narrow approval-gate exception for adjudicated zero-findings CCR headlines."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.critique_adjudicator import classify_critique_headline
from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.github.ccr_headline import parse_ccr_overview_summary

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.pipeline.gate_verdict import CopilotGateVerdict
    from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def critique_gate_exception_passed(snapshot: PRStateSnapshot, unresolved_threads: int) -> bool | None:
    """Return the critique-specific gate result, or ``None`` when not applicable."""
    from agentic_devtools.cli.ci.pipeline.gate_verdict import (
        REASON_CLEAN,
        REASON_NEW_CCR_NOT_APPROVED,
        is_copilot_or_synthetic_review,
    )

    verdict = snapshot.copilot_gate_verdict
    if not snapshot.critique_task_state_available:
        return False
    if (
        verdict is None
        or (verdict.passed and verdict.reason != REASON_CLEAN)
        or (not verdict.passed and verdict.reason != REASON_NEW_CCR_NOT_APPROVED)
        or verdict.body_comment_count not in (None, 0)
        or verdict.suppressed_count != 0
        or snapshot.head_changed_since_review
        or not snapshot.head_sha
    ):
        return None
    review = next(
        (
            candidate
            for candidate in snapshot.reviews
            if candidate.id == verdict.review_id
            and candidate.commit_sha == snapshot.head_sha
            and is_copilot_or_synthetic_review(candidate)
        ),
        None,
    )
    if review is None:
        return None
    overview = parse_ccr_overview_summary(review.body)
    if overview is None or not overview[0] or overview[1] is None:
        return None
    if (
        snapshot.effective_review_comment_count != 0
        or snapshot.effective_review_comment_count_review_id != verdict.review_id
        or snapshot.effective_review_comment_filter_applied is None
    ):
        return False
    if verdict.reason == REASON_NEW_CCR_NOT_APPROVED and snapshot.critique_headline_classification == "UNKNOWN":
        return False
    if snapshot.critique_headline_classification == "approval_worthy":
        return unresolved_threads == 0 if verdict.reason == REASON_NEW_CCR_NOT_APPROVED else None
    if verdict.passed and snapshot.critique_headline_classification != "critique":
        return None
    adjudicated_review_id = snapshot.critique_adjudicated_review_id
    if (
        snapshot.critique_adjudicated_verdict == "rebutted"
        and snapshot.critique_adjudicated_head_sha == snapshot.head_sha
        and snapshot.critique_adjudicated_headline == overview[1]
        and isinstance(adjudicated_review_id, int)
        and 0 < adjudicated_review_id <= review.id
    ):
        return unresolved_threads == 0
    return False


def _block_prior_critique_carryover(verdict: CopilotGateVerdict, review: ReviewInfo) -> CopilotGateVerdict:
    """Require a fresh review when a diff-preserved prior review has a critique headline."""
    if not verdict.passed:
        return verdict
    overview = parse_ccr_overview_summary(review.body)
    if overview is None or not overview[0] or overview[1] is None:
        return verdict
    if classify_critique_headline(overview[1]).verdict != "critique":
        return verdict
    from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_AWAITING_FRESH

    return replace(
        verdict,
        passed=False,
        reason=REASON_AWAITING_FRESH,
        details="Prior-commit critique review requires a fresh review on HEAD",
    )
