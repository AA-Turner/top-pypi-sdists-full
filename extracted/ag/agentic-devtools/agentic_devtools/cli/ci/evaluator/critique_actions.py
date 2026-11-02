"""Critique-specific post-agent evaluation actions."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import replace

from agentic_devtools.cli.shared.retry import ProviderRateLimitError

from ..critique_adjudicator import CritiqueAdjudication, build_adjudication_comment
from ..critique_adjudicator import adjudicate_critique as run_critique_adjudication
from ..guards import AGENT_FAILED_LABEL
from ..pipeline.actions import critique_dispatch
from ..pipeline.actions.dispatch_repair import DispatchRepairAction
from ..pipeline.models import ActionDecision
from ..pipeline.snapshot_builder import build_pr_state_snapshot
from ..pipeline.snapshot_models import DerivedState
from ..provider import CIPlatformProvider
from .models import EvaluationResult, PostAgentAction, PostAgentClassification, PostAgentSnapshot

logger = logging.getLogger(__name__)


def _result(
    snapshot: PostAgentSnapshot,
    unresolved_count: int,
    *,
    success: bool,
    dry_run: bool = False,
    error_details: str | None = None,
) -> EvaluationResult:
    return EvaluationResult(
        classification=PostAgentClassification.critique_adjudication,
        action_taken=PostAgentAction.adjudicate_critique,
        success=success,
        threads_unresolved=unresolved_count,
        error_details=error_details,
        dry_run=dry_run,
    )


def _lock_ownership_error(
    snapshot: PostAgentSnapshot,
    unresolved_count: int,
    ownership_guard: Callable[[], bool] | None,
) -> EvaluationResult | None:
    if ownership_guard is None:
        return None
    try:
        owns_lock = ownership_guard()
    except ProviderRateLimitError as exc:
        if exc.is_rate_limit:
            raise
        owns_lock = False
    except Exception:
        owns_lock = False
    if owns_lock:
        return None
    return _result(
        snapshot,
        unresolved_count,
        success=False,
        error_details="Evaluator lock ownership changed before critique mutation",
    )


def _existing_result(
    provider: CIPlatformProvider,
    snapshot: PostAgentSnapshot,
    unresolved_count: int,
    *,
    existing_needs_human: bool,
    dry_run: bool,
    ownership_guard: Callable[[], bool] | None,
) -> EvaluationResult:
    if existing_needs_human and not dry_run:
        lock_error = _lock_ownership_error(snapshot, unresolved_count, ownership_guard)
        if lock_error is not None:
            return lock_error
        try:
            provider.add_label(snapshot.pr_number, AGENT_FAILED_LABEL)
        except Exception as exc:
            logger.warning("PR #%d: Failed to restore %s label: %s", snapshot.pr_number, AGENT_FAILED_LABEL, exc)
            return _result(
                snapshot,
                unresolved_count,
                success=False,
                error_details=f"needs-human label could not be restored: {exc}",
            )
    return _result(snapshot, unresolved_count, success=True, dry_run=dry_run)


def _current_head_error(
    provider: CIPlatformProvider,
    snapshot: PostAgentSnapshot,
    head_sha: str,
    unresolved_count: int,
) -> EvaluationResult | None:
    try:
        current_metadata = provider.get_pr_metadata(snapshot.pr_number)
    except Exception as exc:
        logger.warning("PR #%d: Could not verify HEAD before critique adjudication: %s", snapshot.pr_number, exc)
        return _result(
            snapshot,
            unresolved_count,
            success=False,
            error_details="Current HEAD could not be verified before adjudication",
        )
    if current_metadata.head_sha != head_sha or snapshot.current_head_sha != head_sha:
        return _result(
            snapshot,
            unresolved_count,
            success=True,
            error_details="Critique task belongs to a stale HEAD; no adjudication was persisted",
        )
    return None


def _adjudicate_snapshot(
    snapshot: PostAgentSnapshot,
    head_sha: str,
    review_id: int,
    attempt: int,
) -> CritiqueAdjudication:
    try:
        decision = run_critique_adjudication(
            {
                "pr_number": snapshot.pr_number,
                "head_sha": head_sha,
                "review_id": review_id,
                "headline": snapshot.critique_headline,
                "review_body": snapshot.critique_review_body,
                "agent_reply": snapshot.latest_agent_comment.body if snapshot.latest_agent_comment else "",
                "diff_text": snapshot.diff_text,
                "threads": snapshot.threads,
                "prior_adjudications": snapshot.critique_adjudications,
            }
        )
    except Exception as exc:
        logger.warning("PR #%d: Critique adjudication failed closed to needs-human: %s", snapshot.pr_number, exc)
        return CritiqueAdjudication(
            verdict="needs_human",
            rationale=f"AI adjudication was unavailable or malformed after retries: {str(exc)[:500]}",
        )
    unique_head_tasks = {(item.review_id, item.attempt) for item in snapshot.critique_tasks}
    if decision.verdict == "needs_repair" and len(unique_head_tasks) >= 2:
        rationale_prefix = (
            "The adjudicator requested another repair, but the two-task per-HEAD limit has been reached. "
        )
        return CritiqueAdjudication(
            verdict="needs_human",
            rationale=(rationale_prefix + decision.rationale)[:2_000],
        )
    return decision


def _adjudicate_with_lock_guard(
    snapshot: PostAgentSnapshot,
    task_head_sha: str,
    review_id: int,
    attempt: int,
    unresolved_count: int,
    ownership_guard: Callable[[], bool] | None,
) -> CritiqueAdjudication | EvaluationResult:
    lock_error = _lock_ownership_error(snapshot, unresolved_count, ownership_guard)
    if lock_error is not None:
        return lock_error
    decision = _adjudicate_snapshot(snapshot, task_head_sha, review_id, attempt)
    return _lock_ownership_error(snapshot, unresolved_count, ownership_guard) or decision


def _dispatch_followup(
    provider: CIPlatformProvider,
    snapshot: PostAgentSnapshot,
    task_head_sha: str,
    review_id: int,
    headline: str,
    decision: CritiqueAdjudication,
    unresolved_count: int,
    ownership_guard: Callable[[], bool] | None,
) -> tuple[CritiqueAdjudication, EvaluationResult | None]:
    derived: DerivedState | None = None
    try:
        live_snapshot = build_pr_state_snapshot(provider, snapshot.pr_number, promote_findings=False)
        if live_snapshot.head_sha != task_head_sha:
            return decision, _result(
                snapshot,
                unresolved_count,
                success=True,
                error_details="HEAD changed before the follow-up repair could be dispatched",
            )
        if critique_dispatch.zero_findings_headline(live_snapshot) != (review_id, headline):
            return decision, _result(
                snapshot,
                unresolved_count,
                success=True,
                error_details="Critique review context changed before the follow-up repair could be dispatched",
            )
        live_snapshot = replace(
            live_snapshot,
            critique_adjudicated_review_id=review_id,
            critique_adjudicated_head_sha=task_head_sha,
            critique_adjudicated_headline=headline,
            critique_adjudicated_verdict=decision.verdict,
            critique_followup_instruction=decision.concrete_instruction or "",
        )
        derived = DerivedState(live_snapshot)
        derived.set("provider", provider)
        dispatch = DispatchRepairAction()
        preflight = dispatch.evaluate(live_snapshot, derived)
        if preflight.decision is not ActionDecision.EXECUTE:
            raise RuntimeError(f"Follow-up repair was not eligible: {preflight.details}")
        lock_error = _lock_ownership_error(snapshot, unresolved_count, ownership_guard)
        if lock_error is not None:
            return decision, lock_error
        dispatch_result = dispatch.execute(provider, live_snapshot, derived)
        if dispatch_result.decision is not ActionDecision.EXECUTE:
            raise RuntimeError(dispatch_result.error or dispatch_result.details)
    except Exception as exc:
        if derived is None or derived.get("repair_dispatched") is not True:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning(
                "PR #%d: Follow-up critique repair could not be dispatched; escalating to needs-human: %s",
                snapshot.pr_number,
                exc,
            )
            return (
                CritiqueAdjudication(
                    verdict="needs_human",
                    rationale=(
                        f"A concrete repair was requested but the protected follow-up dispatch failed: {str(exc)[:500]}"
                    ),
                ),
                None,
            )
        logger.warning(
            "PR #%d: Follow-up repair was created but bookkeeping was interrupted: %s", snapshot.pr_number, exc
        )
    return decision, None


def _persist_decision(
    provider: CIPlatformProvider,
    snapshot: PostAgentSnapshot,
    task_head_sha: str,
    review_id: int,
    attempt: int,
    unresolved_count: int,
    decision: CritiqueAdjudication,
    ownership_guard: Callable[[], bool] | None,
) -> EvaluationResult:
    try:
        latest_metadata = provider.get_pr_metadata(snapshot.pr_number)
    except Exception as exc:
        logger.warning(
            "PR #%d: Could not re-verify HEAD before persisting critique outcome: %s", snapshot.pr_number, exc
        )
        return _result(
            snapshot,
            unresolved_count,
            success=False,
            error_details="Current HEAD could not be verified before persisting the critique outcome",
        )
    if latest_metadata.head_sha != task_head_sha:
        return _result(
            snapshot,
            unresolved_count,
            success=True,
            error_details="HEAD changed before the critique outcome could be persisted",
        )

    body = build_adjudication_comment(
        pr_number=snapshot.pr_number,
        head_sha=task_head_sha,
        review_id=review_id,
        attempt=attempt,
        adjudication=decision,
    )
    lock_error = _lock_ownership_error(snapshot, unresolved_count, ownership_guard)
    if lock_error is not None:
        return lock_error
    try:
        comment_id = provider.post_comment_as_pr_token(snapshot.pr_number, body)
        if type(comment_id) is not int or comment_id <= 0:
            raise RuntimeError("Critique adjudication marker was not persisted")
    except Exception as exc:
        logger.warning("PR #%d: Failed to persist critique adjudication: %s", snapshot.pr_number, exc)
        return _result(
            snapshot,
            unresolved_count,
            success=False,
            error_details=f"Critique adjudication marker write failed: {exc}",
        )

    if decision.verdict == "needs_human":
        lock_error = _lock_ownership_error(snapshot, unresolved_count, ownership_guard)
        if lock_error is not None:
            return lock_error
        try:
            provider.add_label(snapshot.pr_number, AGENT_FAILED_LABEL)
        except Exception as exc:
            logger.warning("PR #%d: Failed to add %s label: %s", snapshot.pr_number, AGENT_FAILED_LABEL, exc)
            return _result(
                snapshot,
                unresolved_count,
                success=False,
                error_details=f"needs-human outcome persisted but label write failed: {exc}",
            )
    return _result(snapshot, unresolved_count, success=True)


def adjudicate_critique(
    provider: CIPlatformProvider,
    snapshot: PostAgentSnapshot,
    *,
    dry_run: bool = False,
    ownership_guard: Callable[[], bool] | None = None,
) -> EvaluationResult:
    """Adjudicate a no-commit critique task and persist one head-scoped outcome."""
    task = snapshot.critique_task
    unresolved_count = sum(not thread.is_resolved for thread in snapshot.threads)
    if task is None:
        return _result(
            snapshot,
            unresolved_count,
            success=False,
            dry_run=dry_run,
            error_details="Critique task identity is unavailable",
        )

    existing = next(
        (
            record
            for record in snapshot.critique_adjudications
            if record.head_sha == task.head_sha
            and record.review_id == task.review_id
            and record.attempt == task.attempt
        ),
        None,
    )
    if existing is not None:
        if existing.verdict == "needs_human" and not dry_run:
            head_error = _current_head_error(provider, snapshot, task.head_sha, unresolved_count)
            if head_error is not None:
                return head_error
        return _existing_result(
            provider,
            snapshot,
            unresolved_count,
            existing_needs_human=existing.verdict == "needs_human",
            dry_run=dry_run,
            ownership_guard=ownership_guard,
        )

    if dry_run:
        return _result(snapshot, unresolved_count, success=True, dry_run=True)

    head_error = _current_head_error(provider, snapshot, task.head_sha, unresolved_count)
    if head_error is not None:
        return head_error

    decision = _adjudicate_with_lock_guard(
        snapshot,
        task.head_sha,
        task.review_id,
        task.attempt,
        unresolved_count,
        ownership_guard,
    )
    if isinstance(decision, EvaluationResult):
        return decision
    if decision.verdict == "needs_repair":
        decision, early_result = _dispatch_followup(
            provider,
            snapshot,
            task.head_sha,
            task.review_id,
            snapshot.critique_headline,
            decision,
            unresolved_count,
            ownership_guard,
        )
        if early_result is not None:
            return early_result

    return _persist_decision(
        provider,
        snapshot,
        task.head_sha,
        task.review_id,
        task.attempt,
        unresolved_count,
        decision,
        ownership_guard,
    )
