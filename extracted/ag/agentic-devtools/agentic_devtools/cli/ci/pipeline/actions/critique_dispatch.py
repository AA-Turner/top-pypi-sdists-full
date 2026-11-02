"""Critique-specific dispatch decisions and task-marker operations."""

from __future__ import annotations

import logging
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypedDict

from agentic_devtools.cli.ci.critique_adjudicator import (
    build_critique_task_cancellation_comment,
    build_critique_task_comment,
)
from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_NEW_CCR_NOT_APPROVED,
    is_copilot_or_synthetic_review,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.repair_attempts import RepairAttemptTracker
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider, RepairDispatchNotAttemptedError
from agentic_devtools.cli.github.ccr_headline import parse_ccr_overview_summary

logger = logging.getLogger(__name__)


class CritiqueRepairParameters(TypedDict, total=False):
    agent_task_prompt: str


def dispatched_repair_result(
    name: str,
    repair_type: str,
    receipt: int | str,
    bookkeeping_audit: object,
    audit_start: int,
    binding_failure: ActionResult | None,
) -> ActionResult:
    """Build the final result after dispatch and critique task binding."""
    if binding_failure is not None:
        return binding_failure
    details = f"Repair dispatched (type={repair_type}, receipt={receipt})"
    if isinstance(bookkeeping_audit, list) and bookkeeping_audit[audit_start:]:
        details += f"; bookkeeping audit: {'; '.join(bookkeeping_audit[audit_start:])}"
    return ActionResult(name=name, decision=ActionDecision.EXECUTE, details=details)


def known_empty_zero_findings_overview(snapshot: PRStateSnapshot) -> tuple[ReviewInfo, str | None] | None:
    """Return a zero-findings overview with a known-empty comment inventory."""
    verdict = snapshot.copilot_gate_verdict
    if (
        verdict is None
        or (verdict.passed and verdict.reason != REASON_CLEAN)
        or (not verdict.passed and verdict.reason != REASON_NEW_CCR_NOT_APPROVED)
        or verdict.body_comment_count not in (None, 0)
        or verdict.suppressed_count != 0
        or verdict.review_id <= 0
        or snapshot.effective_review_comment_count != 0
        or snapshot.effective_review_comment_count_review_id != verdict.review_id
        or snapshot.effective_review_comment_filter_applied is None
    ):
        return None
    review = next(
        (
            candidate
            for candidate in snapshot.reviews
            if candidate.id == verdict.review_id and is_copilot_or_synthetic_review(candidate)
        ),
        None,
    )
    if review is None:
        return None
    overview = parse_ccr_overview_summary(review.body)
    if overview is None or not overview[0]:
        return None
    return review, overview[1]


def zero_findings_headline(snapshot: PRStateSnapshot) -> tuple[int, str] | None:
    """Return a parseable, known-empty overview only from the exact current HEAD review."""
    overview = known_empty_zero_findings_overview(snapshot)
    if overview is None:
        return None
    review, headline = overview
    if not snapshot.head_sha or review.commit_sha != snapshot.head_sha:
        return None
    if headline is None:
        logger.warning(
            "PR #%d: zero-open-findings CCR overview has no parseable headline — preserving existing gate behavior",
            snapshot.pr_number,
        )
        return None
    return review.id, headline


def critique_headline(snapshot: PRStateSnapshot) -> tuple[int, str] | None:
    """Return a headline classified as a critique unless a matching rebuttal exists."""
    parsed = zero_findings_headline(snapshot)
    if parsed is None or snapshot.critique_headline_classification != "critique":
        return None
    review_id, headline = parsed
    adjudicated_review_id = snapshot.critique_adjudicated_review_id
    if (
        snapshot.critique_adjudicated_verdict == "rebutted"
        and snapshot.critique_adjudicated_head_sha == snapshot.head_sha
        and snapshot.critique_adjudicated_headline == headline
        and isinstance(adjudicated_review_id, int)
        and 0 < adjudicated_review_id <= review_id
    ):
        return None
    return parsed


def approval_worthy_headline(snapshot: PRStateSnapshot) -> tuple[int, str] | None:
    """Return a zero-finding headline classified as approval-worthy."""
    parsed = zero_findings_headline(snapshot)
    if parsed is None or snapshot.critique_headline_classification != "approval_worthy":
        return None
    return parsed


def actionable_review_id(snapshot: PRStateSnapshot, review_id: int) -> int:
    """Exclude approval-worthy zero-findings headlines from repair actionability."""
    if (
        snapshot.copilot_gate_verdict is not None
        and snapshot.copilot_gate_verdict.reason == REASON_NEW_CCR_NOT_APPROVED
        and approval_worthy_headline(snapshot) is not None
    ):
        return 0
    return review_id


def log_noncritique_overview(snapshot: PRStateSnapshot) -> None:
    """Log why a zero-findings overview was not dispatched as a critique."""
    verdict = snapshot.copilot_gate_verdict
    if verdict is None or verdict.reason != REASON_NEW_CCR_NOT_APPROVED:
        return
    review = next((candidate for candidate in snapshot.reviews if candidate.id == verdict.review_id), None)
    overview = parse_ccr_overview_summary(review.body) if review is not None else None
    if overview is not None and overview[0] and critique_headline(snapshot) is None:
        logger.info(
            "PR #%d: zero-open-findings CCR overview is approval-worthy or not eligible for critique dispatch",
            snapshot.pr_number,
        )


def should_skip_zero_findings_repair(snapshot: PRStateSnapshot, stuck_prior_threads: bool) -> bool:
    """Return whether an ineligible or non-critique overview should skip repair."""
    if snapshot.ci_status == "failing" or stuck_prior_threads or known_empty_zero_findings_overview(snapshot) is None:
        return False
    if zero_findings_headline(snapshot) is None:
        return True
    if snapshot.critique_headline_classification == "approval_worthy":
        return True
    return snapshot.critique_headline_classification == "critique" and critique_headline(snapshot) is None


def zero_findings_repair_skip(
    name: str,
    snapshot: PRStateSnapshot,
    stuck_prior_threads: bool,
) -> ActionResult | None:
    """Return the skip result when a zero-findings overview is not repairable."""
    if should_skip_zero_findings_repair(snapshot, stuck_prior_threads):
        return ActionResult(
            name=name,
            decision=ActionDecision.SKIP,
            details="Zero-findings CCR overview is approval-worthy, unparseable, stale, or already rebutted",
        )
    return None


@dataclass(frozen=True)
class CritiqueAttemptPlan:
    key: str
    already_attempted: bool
    cap_reached: bool


def plan_critique_attempt(snapshot: PRStateSnapshot, review_id: int, attempted: set[str]) -> CritiqueAttemptPlan:
    """Select the initial critique task or authorized follow-up attempt."""
    critique_attempts = [
        (int(match[1]), int(match[2]))
        for attempted_key in attempted
        if (match := re.fullmatch(r"critique:([1-9]\d*):([12])", attempted_key)) is not None
    ]
    attempts_for_review = {
        attempt for attempted_review_id, attempt in critique_attempts if attempted_review_id == review_id
    }
    next_attempt = max((attempt for _, attempt in critique_attempts), default=0) + 1
    if next_attempt > 2:
        logger.info(
            "PR #%d: critique repair task cap reached for HEAD %s — awaiting adjudication or human action",
            snapshot.pr_number,
            snapshot.head_sha[:12],
        )
        return CritiqueAttemptPlan("", False, True)
    current_critique = critique_headline(snapshot)
    needs_repair_adjudication = (
        snapshot.critique_adjudicated_verdict == "needs_repair"
        and snapshot.critique_adjudicated_review_id == review_id
        and snapshot.critique_adjudicated_head_sha == snapshot.head_sha
        and current_critique is not None
        and snapshot.critique_adjudicated_headline == current_critique[1]
        and bool(snapshot.critique_followup_instruction.strip())
    )
    if attempts_for_review:
        if attempts_for_review == {1} and next_attempt == 2 and needs_repair_adjudication:
            return CritiqueAttemptPlan(f"critique:{review_id}:2", False, False)
        logger.info(
            "PR #%d: critique task for review %d was already attempted on HEAD %s — "
            "waiting for task completion and adjudication",
            snapshot.pr_number,
            review_id,
            snapshot.head_sha[:12],
        )
        return CritiqueAttemptPlan("", True, False)
    return CritiqueAttemptPlan(f"critique:{review_id}:{next_attempt}", False, False)


def plan_review_attempt(
    name: str,
    snapshot: PRStateSnapshot,
    review_id: int,
    body_only_work: bool,
    stuck_prior_threads: bool,
    attempted: set[str],
) -> CritiqueAttemptPlan | ActionResult | None:
    """Plan a critique-specific attempt only for its review's opaque body work."""
    critique = critique_headline(snapshot)
    if (
        snapshot.ci_status != "passing"
        or stuck_prior_threads
        or not body_only_work
        or critique is None
        or critique[0] != review_id
    ):
        return None
    plan = plan_critique_attempt(snapshot, review_id, attempted)
    if plan.cap_reached:
        return ActionResult(
            name=name,
            decision=ActionDecision.SKIP,
            details="Critique repair task cap reached for this HEAD",
        )
    return plan


def register_review_attempt(
    name: str,
    snapshot: PRStateSnapshot,
    review_id: int,
    body_only_work: bool,
    stuck_prior_threads: bool,
    attempts: RepairAttemptTracker,
    review_keys: set[str],
    provider: CIPlatformProvider,
    finding_aware: bool,
    shortfall: int,
    duplicate_trigger: Callable[..., bool],
) -> tuple[ActionResult | None, int]:
    """Register opaque review work while preserving generic and critique attempt rules."""
    attempt_plan = plan_review_attempt(
        name, snapshot, review_id, body_only_work, stuck_prior_threads, attempts.attempted
    )
    if isinstance(attempt_plan, ActionResult):
        return attempt_plan, shortfall
    if attempt_plan is not None and attempt_plan.already_attempted:
        return None, shortfall

    key = attempt_plan.key if attempt_plan is not None else f"review:{review_id}"
    if key in attempts.attempted:
        attempts.escalate(key)
        return None, 0
    validated_followup = attempt_plan is not None and bool(snapshot.critique_followup_instruction)
    if (
        validated_followup
        or finding_aware
        or not duplicate_trigger(provider, snapshot.pr_number, review_id, ttl_minutes=None)
    ):
        review_keys.add(key)
        return None, shortfall

    # Legacy triggers cannot identify individual findings or HEAD.
    # Migrate only opaque body work, never attribute it to roots.
    attempts.reserve({key})
    attempts.escalate(key)
    return None, 0


def create_critique_task_marker(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    critique: tuple[int, str],
    attempt: int,
) -> tuple[tuple[int, int, int], str]:
    """Persist the attempt marker and return marker identity plus exact task prompt."""
    review_id, headline = critique
    marker_body = build_critique_task_comment(snapshot.pr_number, snapshot.head_sha, review_id, attempt)
    marker_id = provider.post_comment_as_pr_token(snapshot.pr_number, marker_body)
    if type(marker_id) is not int or marker_id <= 0:
        raise RuntimeError("Critique task marker was not persisted")
    text = snapshot.critique_followup_instruction or headline
    prompt = f"@copilot please address the following critique of this pr:\n\n{text}"
    return (marker_id, review_id, attempt), prompt


def create_critique_dispatch_marker(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    review_context_id: int,
    pending_attempts: set[str],
) -> tuple[tuple[int, int, int] | None, str | None]:
    """Create a marker only for the critique attempt reserved for this dispatch."""
    critique = critique_headline(snapshot)
    if critique is None or critique[0] != review_context_id:
        return None, None
    prefix = f"critique:{review_context_id}:"
    attempt_key = next((key for key in pending_attempts if key.startswith(prefix)), None)
    if attempt_key is None:
        return None, None
    attempt = int(attempt_key.rsplit(":", 1)[1])
    try:
        return create_critique_task_marker(provider, snapshot, critique, attempt)
    except Exception as exc:
        try:
            reconcile_critique_task_marker(provider, snapshot, pending_attempts)
        except Exception as reconciliation_error:
            raise RuntimeError(f"Critique task marker reconciliation failed: {reconciliation_error}") from exc
        raise RepairDispatchNotAttemptedError(f"Critique task marker write failed: {exc}") from exc


def critique_repair_parameters(prompt: str | None) -> CritiqueRepairParameters:
    """Return strict Agent Tasks dispatch options only for critique prompts."""
    if prompt is None:
        return {}
    return {"agent_task_prompt": prompt}


def cancel_critique_task_marker(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    marker: tuple[int, int, int],
) -> None:
    """Replace a pre-dispatch marker with a verified cancellation tombstone."""
    marker_id, review_id, attempt = marker
    cancelled_body = build_critique_task_cancellation_comment(
        snapshot.pr_number,
        snapshot.head_sha,
        review_id,
        attempt,
    )
    updated_id = provider.update_comment_as_pr_token(marker_id, cancelled_body)
    if updated_id is not None and updated_id != marker_id:
        raise RuntimeError("Critique task cancellation changed the comment identity")
    confirmed = provider.find_comment(snapshot.pr_number, cancelled_body.splitlines()[0])
    if confirmed != (marker_id, cancelled_body):
        raise RuntimeError("Critique task cancellation could not be confirmed")


def cancel_critique_task_marker_if_present(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    marker: tuple[int, int, int] | None,
) -> None:
    """Cancel the persisted task marker when one was created."""
    if marker is not None:
        cancel_critique_task_marker(provider, snapshot, marker)


def reconcile_critique_task_marker(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    pending_attempts: set[str],
) -> None:
    """Cancel any exact critique marker left by a failed pre-dispatch write."""
    critique = critique_headline(snapshot)
    if critique is None:
        return
    review_id, _headline = critique
    prefix = f"critique:{review_id}:"
    for key in pending_attempts:
        if not key.startswith(prefix):
            continue
        attempt = int(key.rsplit(":", 1)[1])
        marker_body = build_critique_task_comment(snapshot.pr_number, snapshot.head_sha, review_id, attempt)
        existing = provider.find_comment(snapshot.pr_number, marker_body.splitlines()[0])
        if existing is None:
            continue
        marker_id, existing_body = existing
        if existing_body != marker_body:
            raise RuntimeError("Critique task marker could not be safely reconciled")
        cancel_critique_task_marker(provider, snapshot, (marker_id, review_id, attempt))
