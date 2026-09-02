"""Pipeline command entry point — replaces the event-branching orchestrator."""

from __future__ import annotations

import logging
import sys
import time

from agentic_devtools.cli.ci.cooldown import format_resume_at, persist_cooldown
from agentic_devtools.cli.ci.evaluator.lock import acquire_lock, release_lock
from agentic_devtools.cli.ci.models import EventPayload
from agentic_devtools.cli.ci.pipeline.actions import (
    ApplySuggestionsAction,
    ApproveAction,
    DeferSuppressedAction,
    DispatchConflictResolutionAction,
    DispatchRepairAction,
    GuardsAction,
    MergeAction,
    PublishAction,
    RebaseAction,
    RequestReviewAction,
    ResolveThreadsAction,
    SquashAction,
    TakeOverAutomationCommitAction,
)
from agentic_devtools.cli.ci.pipeline.base import Action
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.runner import run_pipeline
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot, build_pr_state_snapshot
from agentic_devtools.cli.ci.pipeline.summary import post_summary_comment
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, calculate_rate_limit_delay

logger = logging.getLogger(__name__)

# Exit codes (same as orchestrator.py for compatibility)
EXIT_SUCCESS = 0
EXIT_GUARD_BLOCKED = 1
EXIT_MERGE_BLOCKED = 3
EXIT_METADATA_FAILED = 4
EXIT_REPAIR_DISPATCHED = 5
EXIT_RATE_LIMIT_PAUSED = 6


def run_ai_pr_loop_v2(
    provider: CIPlatformProvider,
    event_payload: EventPayload,
    *,
    actionable_check_names: frozenset[str] | None = None,
) -> int:
    """Run the idempotent AI PR loop pipeline.

    Replaces the event-branching orchestrator with a sequential pipeline
    of 12 action evaluators. Every run evaluates all actions regardless of
    trigger type.

    Pipeline ordering:
        Guards → Publish → TakeOver → ApplySuggestions → DeferSuppressed
        → DispatchRepair → ResolveThreads → Squash → Rebase
        → DispatchConflictResolution → RequestReview → Approve → Merge

    TakeOver runs immediately after Publish so that a Copilot-authored HEAD is
    reclaimed under the human CI identity (re-emitting a synchronize event that
    triggers the required checks) before any downstream action evaluates it.

    ApplySuggestions runs before DispatchRepair so that autofixable suggestions
    are committed first, potentially eliminating the need for repair dispatch.

    DeferSuppressed runs between the two so a specs-only suppressed-only round is
    handed to a follow-up triage issue — and its deferral marker read by
    DispatchRepair — instead of manufacturing another repair round.

    ResolveThreads runs before RequestReview so that resolved threads are reflected in
    derived state before the review-request guard evaluates unresolved_threads.

    DispatchConflictResolution runs immediately after Rebase so that a rebase whose
    conflicts could not be auto-resolved is handed to the cloud agent in the same run
    instead of stalling the loop until a human intervenes.

    Args:
        provider: CI platform provider for API interactions.
        event_payload: Normalized event payload from the trigger.
        actionable_check_names: Optional set of check run names to evaluate.

    Returns:
        Exit code (0 = success, non-zero = blocked/error).
    """
    pr_number = event_payload.pr_number
    if pr_number == 0:
        logger.warning("No PR number in event payload, skipping")
        return EXIT_SUCCESS

    # Acquire evaluator lock first so that races resolve without burning snapshot
    # API quota on runs that will be discarded.
    lock_token: str | None = None
    try:
        lock_token = acquire_lock(provider, pr_number)
    except ProviderRateLimitError as exc:
        if exc.is_rate_limit:
            return _handle_rate_limit(provider, exc)
        logger.warning("PR #%d: Failed to acquire lock: %s", pr_number, exc)
        return EXIT_METADATA_FAILED
    except Exception as exc:
        logger.warning("PR #%d: Failed to acquire lock: %s", pr_number, exc)
        return EXIT_METADATA_FAILED

    if lock_token is None:
        logger.info("PR #%d: Lock already held — skipping pipeline run", pr_number)
        return EXIT_SUCCESS

    try:
        # Build PR state snapshot (after the lock so only the winner pays the cost)
        try:
            snapshot = build_pr_state_snapshot(
                provider,
                pr_number,
                actionable_check_names=actionable_check_names,
            )
        except ProviderRateLimitError as exc:
            if exc.is_rate_limit:
                return _handle_rate_limit(provider, exc)
            logger.error("Failed to build PR state snapshot for #%d: %s", pr_number, exc)
            return EXIT_METADATA_FAILED
        except Exception as exc:
            logger.error("Failed to build PR state snapshot for #%d: %s", pr_number, exc)
            return EXIT_METADATA_FAILED

        # Build action pipeline
        actions: list[Action] = [
            GuardsAction(),
            PublishAction(),
            TakeOverAutomationCommitAction(),
            ApplySuggestionsAction(),
            DeferSuppressedAction(),
            DispatchRepairAction(),
            ResolveThreadsAction(),
            SquashAction(),
            RebaseAction(),
            DispatchConflictResolutionAction(),
            RequestReviewAction(),
            ApproveAction(),
            MergeAction(),
        ]

        # Run pipeline
        try:
            summary = run_pipeline(
                provider,
                snapshot,
                actions,
                actionable_check_names=actionable_check_names,
            )
        except ProviderRateLimitError as exc:
            if exc.is_rate_limit:
                return _handle_rate_limit(provider, exc)
            raise

        # Post summary comment
        try:
            post_summary_comment(provider, pr_number, summary)
        except ProviderRateLimitError as exc:
            if exc.is_rate_limit:
                return _handle_rate_limit(provider, exc)
            raise

        # Determine exit code from results
        return _determine_exit_code(summary.results, snapshot=summary.snapshot)

    finally:
        # Release lock — distinguish rate-limit errors from ordinary failures so that
        # a RATE_LIMITED response during lock release is converted to the paused outcome
        # rather than being swallowed and claiming successful processing.
        # Only override the caller's return value; never suppress an already-propagating
        # primary exception (sys.exc_info captures any active exception before the inner
        # try/except replaces it with the lock-release error).
        _exc_in_flight = sys.exc_info()[1]
        try:
            release_lock(provider, pr_number, lock_token)
        except ProviderRateLimitError as exc:
            if exc.is_rate_limit and _exc_in_flight is None:
                return _handle_rate_limit(provider, exc)  # noqa: B012
            logger.warning("PR #%d: Failed to release lock: %s", pr_number, exc)
        except Exception as exc:
            logger.warning("PR #%d: Failed to release lock: %s", pr_number, exc)


def _determine_exit_code(results: list[ActionResult], *, snapshot: PRStateSnapshot | None = None) -> int:
    """Determine the exit code from pipeline results."""
    repair_dispatched = False
    failed_side_effect_action = False
    side_effect_actions = {
        "apply_suggestions",
        "defer_suppressed",
        "publish",
        "takeover",
        "request_review",
        "resolve_threads",
        "dispatch_repair",
        "dispatch_conflict_resolution",
        "squash",
        "rebase",
        "approve",
        "merge",
    }

    conflict_repair_result = next(
        (result for result in results if result.name == "dispatch_conflict_resolution"),
        None,
    )
    for result in results:
        if result.decision == ActionDecision.BLOCKED and not (
            result.name == "rebase"
            and conflict_repair_result is not None
            and conflict_repair_result.decision in {ActionDecision.EXECUTE, ActionDecision.FAILED}
        ):
            return EXIT_GUARD_BLOCKED
        if result.name == "dispatch_conflict_resolution" and result.decision == ActionDecision.EXECUTE:
            # A conflict-repair dispatch is a repair dispatch: the PR is now
            # waiting on the cloud agent, not on this run.
            repair_dispatched = True
        if result.name == "dispatch_repair":
            if result.decision == ActionDecision.EXECUTE:
                repair_dispatched = True
            elif result.limit_reached:
                # Dedup or cycle limit reached — treat as guard-blocked (same as legacy orchestrator)
                return EXIT_GUARD_BLOCKED
        if (
            result.name == "approve"
            and result.decision == ActionDecision.SKIP
            and not result.preconditions.get("approver_token_available", True)
        ):
            # Provider could not submit approval (missing approver token).  Block merge so
            # the workflow retries rather than silently exiting 0 with the PR unmerged.
            return EXIT_MERGE_BLOCKED
        if result.decision == ActionDecision.FAILED and result.name in side_effect_actions:
            failed_side_effect_action = True

    if repair_dispatched:
        return EXIT_REPAIR_DISPATCHED
    if failed_side_effect_action:
        return EXIT_MERGE_BLOCKED
    if snapshot is not None and snapshot.ci_status == "unknown":
        return EXIT_MERGE_BLOCKED
    return EXIT_SUCCESS


def _handle_rate_limit(provider: CIPlatformProvider, error: ProviderRateLimitError) -> int:
    """Persist and report a provider pause without claiming the PR succeeded."""
    now = time.time()
    persisted = persist_cooldown(provider, error, now=now)
    delay = calculate_rate_limit_delay(
        retry_after_seconds=error.retry_after_seconds,
        reset_timestamp=error.reset_timestamp,
        now=now,
    )
    key = (
        persisted[0]
        if persisted is not None
        else f"{error.provider or 'github'}:{error.credential_identity or 'GH_TOKEN'}"
    )
    provider_name, _, credential_identity = key.partition(":")
    resume_at = persisted[1].resume_at if persisted is not None else delay.resume_at
    source = persisted[1].source if persisted is not None else (error.source or delay.source)
    message = (
        f"AI PR Loop paused for rate limit: provider={provider_name} "
        f"credential={credential_identity} reason=rate_limit source={source} "
        f"resume_at={format_resume_at(resume_at)} remaining_delay={max(0, int(resume_at - now))}s"
    )
    logger.warning(message)
    print(f"::notice::{message}")
    return EXIT_RATE_LIMIT_PAUSED
