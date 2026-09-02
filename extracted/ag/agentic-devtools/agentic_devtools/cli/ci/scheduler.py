"""Round-robin PR scheduler for the AI PR loop.

Provides pure scheduling functions and orchestration logic for selecting
the next batch of eligible PRs to dispatch via workflow_dispatch events.
"""

from __future__ import annotations

import logging
import os
import sys
import time
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.cooldown import (
    active_cooldown,
    ai_pr_loop_credential_identities,
    format_resume_at,
    persist_cooldown,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)

DEFAULT_BATCH_SIZE = 1
MAX_BATCH_SIZE = 100
DEFAULT_POOL_SIZE = 1
MAX_POOL_SIZE = 100
VARIABLE_LAST_DISPATCHED = "AI_PR_LOOP_LAST_DISPATCHED_PR"
VARIABLE_BATCH_SIZE = "AI_PR_LOOP_DISPATCH_BATCH_SIZE"
VARIABLE_POOL_SIZE = "AI_PR_LOOP_ELIGIBLE_PR_LIMIT"

SKIP_LABEL = "ai-pr-loop-ignore"
AUTO_MERGE_LABEL = "ai-auto-merge-allowed"
SUPPRESSED_FOLLOW_UP_LABEL = "suppressed-comment-follow-up"
#: Fixed allowlist of labels carried from a PR's linked issues onto the PR itself.
#: This is an allowlist, not a mirror — no other label is ever copied.
PROPAGATED_ISSUE_LABELS: tuple[str, ...] = (AUTO_MERGE_LABEL, SUPPRESSED_FOLLOW_UP_LABEL)
AUDIT_EVAL_BRANCH_SUBSTR = "copilot"
AUDIT_AGENT_OUTPUT_PATH_PREFIX = "audit-batches/"
AUDIT_AGENT_OUTPUT_PATH_SUBSTR = "/agent-output/"


@dataclass(frozen=True)
class EligiblePR:
    """A PR eligible for AI loop processing."""

    number: int
    created_at: str
    labels_to_propagate: tuple[str, ...] = ()


@dataclass(frozen=True)
class DispatchEvent:
    """A dispatch event record for a PR."""

    pr_number: int
    created_at: str


@dataclass(frozen=True)
class SchedulerResult:
    """Result of a scheduler run."""

    run_mode: str
    batch_size: int
    pool_size: int
    eligible_count: int
    dispatched_count: int
    dispatched_prs: list[int] = field(default_factory=list)
    cursor_before: int | None = None
    cursor_after: int | None = None
    cursor_persisted: bool = False
    had_dispatch_error: bool = False
    status: str = "ok"
    cooldown_key: str = ""
    cooldown_source: str = ""
    cooldown_resume_at: str = ""
    cooldown_remaining_seconds: int = 0


def filter_eligible_prs(
    prs: list[dict],
    skip_label: str = SKIP_LABEL,
    *,
    exclude_human_blocked: bool = True,
    exclude_audit_handoff: bool = True,
) -> list[EligiblePR]:
    """Filter raw PR dicts to eligible PRs.

    Pure function that applies exclusion rules:
    - Excludes fork PRs (isCrossRepository)
    - Excludes PRs with the skip label (default: ai-pr-loop-ignore)
    - Excludes human-blocked PRs (is_human_blocked flag) when requested
    - Excludes audit evaluation handoff PRs as a scheduler backstop when BOTH:
      - head branch contains ``copilot`` and
      - provider enrichment says PR touches ``audit-batches/**/agent-output/**``
      and ``exclude_audit_handoff`` is enabled
    - Preserves creation order (assumes input is sorted oldest-first)

    Args:
        prs: List of PR dicts with keys: number, createdAt, isCrossRepository,
            labels (list of dicts with 'name'), is_human_blocked (bool),
            head_ref/headRefName (str), touches_audit_agent_output (bool),
            labels_to_propagate (list of str — allowlisted labels carried from
            the PR's linked issues; see :func:`select_labels_to_propagate`).
        skip_label: Label name that excludes a PR from processing.
        exclude_human_blocked: When True, remove PRs marked human-blocked.
        exclude_audit_handoff: When True, remove audit-evaluation handoff PRs.

    Returns:
        Sorted list (oldest-first) of EligiblePR dataclasses.
    """
    eligible: list[EligiblePR] = []
    for pr in prs:
        raw_number = pr.get("number")
        if isinstance(raw_number, int) and not isinstance(raw_number, bool):
            number = raw_number
        elif isinstance(raw_number, str):
            try:
                number = int(raw_number.strip())
            except ValueError:
                continue
        else:
            continue

        if number <= 0:
            continue

        raw_created_at = pr.get("createdAt", "")
        if isinstance(raw_created_at, str):
            created_at = raw_created_at
        elif raw_created_at is None:
            created_at = ""
        else:
            created_at = str(raw_created_at)

        # Skip forks
        if pr.get("isCrossRepository", False):
            continue

        # Skip PRs with exclusion label
        labels = pr.get("labels", [])
        if not isinstance(labels, list):
            labels = []
        label_names = [lbl.get("name", "") if isinstance(lbl, dict) else str(lbl) for lbl in labels]
        if skip_label in label_names:
            continue

        # Skip human-blocked PRs
        if exclude_human_blocked and pr.get("is_human_blocked", False):
            continue

        # Scheduler backstop for audit evaluation handoff PRs.
        raw_head_ref = pr.get("head_ref", pr.get("headRefName", ""))
        head_ref = str(raw_head_ref) if raw_head_ref is not None else ""
        touches_audit_agent_output = bool(pr.get("touches_audit_agent_output", False))
        if exclude_audit_handoff and AUDIT_EVAL_BRANCH_SUBSTR in head_ref.lower() and touches_audit_agent_output:
            continue

        raw_propagate = pr.get("labels_to_propagate", ())
        if isinstance(raw_propagate, (list, tuple)):
            labels_to_propagate = tuple(name for name in raw_propagate if isinstance(name, str) and name)
        else:
            labels_to_propagate = ()

        eligible.append(EligiblePR(number=number, created_at=created_at, labels_to_propagate=labels_to_propagate))

    return eligible


def select_labels_to_propagate(
    pr_labels: Iterable[object],
    linked_issue_labels: Iterable[object],
    allowlist: Sequence[str] = PROPAGATED_ISSUE_LABELS,
) -> list[str]:
    """Select the allowlisted labels that must be copied from linked issues to a PR.

    Pure function. Only labels on ``allowlist`` are ever considered — arbitrary
    issue labels are never mirrored onto the PR. Labels the PR already carries are
    omitted so callers make no redundant API calls.

    Args:
        pr_labels: Label names currently on the PR (non-string entries ignored).
        linked_issue_labels: Label names present on any of the PR's linked issues
            (non-string entries ignored).
        allowlist: Ordered allowlist of label names eligible for propagation.

    Returns:
        Allowlisted label names present on a linked issue but missing from the PR,
        in allowlist order and without duplicates.
    """
    existing = {name for name in pr_labels if isinstance(name, str) and name}
    from_issues = {name for name in linked_issue_labels if isinstance(name, str) and name}
    return [label for label in allowlist if label in from_issues and label not in existing]


def propagate_linked_issue_labels(
    provider: CIPlatformProvider,
    eligible_prs: Iterable[EligiblePR],
    *,
    dry_run: bool = False,
) -> dict[int, list[str]]:
    """Apply the allowlisted labels each PR inherits from its linked issues.

    PRs with nothing to propagate (no linked issue, no allowlisted issue label, or
    the label already present) trigger no provider call at all. Failures are
    non-fatal: each failed label is logged and the pass continues.

    Args:
        provider: CI platform provider instance.
        eligible_prs: PRs enriched with ``labels_to_propagate``.
        dry_run: When True, log the intended labels without calling the provider.

    Returns:
        Mapping of PR number to the labels applied (or, in dry-run mode, the
        labels that would have been applied). PRs with no changes are omitted.
    """
    propagated: dict[int, list[str]] = {}
    for pr in eligible_prs:
        # Re-enforce the fixed allowlist at the mutation boundary: even if upstream
        # enrichment placed an unexpected value into labels_to_propagate, only labels
        # explicitly present in PROPAGATED_ISSUE_LABELS are passed to the provider.
        pending = [lbl for lbl in pr.labels_to_propagate if lbl in PROPAGATED_ISSUE_LABELS]
        if not pending:
            continue

        if dry_run:
            logger.info("DRY RUN — would propagate labels %s to PR #%d", pending, pr.number)
            propagated[pr.number] = pending
            continue

        applied: list[str] = []
        for label in pending:
            try:
                provider.add_label(pr.number, label)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.warning(
                    "Failed to propagate label %r from linked issue to PR #%d: %s — continuing",
                    label,
                    pr.number,
                    exc,
                )
                continue
            applied.append(label)
            logger.info("Propagated label %r from linked issue to PR #%d", label, pr.number)

        if applied:
            propagated[pr.number] = applied

    return propagated


def select_next_batch(
    eligible_prs: list[EligiblePR],
    last_dispatched_pr: int | None,
    batch_size: int,
) -> list[int]:
    """Select the next batch of PRs using round-robin scheduling.

    Pure function — given the list of eligible PRs (sorted oldest-first),
    the last-dispatched cursor, and batch size, returns the next N PRs
    in cycle order, wrapping around to the beginning.

    Args:
        eligible_prs: EligiblePR instances sorted by creation date (oldest first).
        last_dispatched_pr: Last PR number in the previous dispatch batch.
            If None or not in the eligible list, starts from the oldest.
        batch_size: Maximum number of PRs to select.

    Returns:
        List of PR numbers to dispatch (up to batch_size), in cycle order.
        Never exceeds len(eligible_prs).
    """
    if not eligible_prs:
        return []

    pr_numbers = [pr.number for pr in eligible_prs]
    effective_batch = max(1, min(batch_size, MAX_BATCH_SIZE, len(pr_numbers)))

    # Determine starting position
    if last_dispatched_pr is None or last_dispatched_pr not in pr_numbers:
        start_idx = 0
    else:
        last_idx = pr_numbers.index(last_dispatched_pr)
        start_idx = (last_idx + 1) % len(pr_numbers)

    # Collect batch, wrapping around
    batch: list[int] = []
    for i in range(effective_batch):
        idx = (start_idx + i) % len(pr_numbers)
        batch.append(pr_numbers[idx])

    return batch


def resolve_batch_size(
    env_value: str | None,
    repo_value: str | None,
    default: int = DEFAULT_BATCH_SIZE,
) -> int:
    """Resolve batch size from environment variable and repo variable.

    Priority: env_value > repo_value > default.
    Values outside [1, 100] are clamped with a warning.

    Args:
        env_value: Value from AI_PR_LOOP_DISPATCH_BATCH_SIZE env var (or None).
        repo_value: Value from repository variable (or None).
        default: Default batch size if both sources are unavailable.

    Returns:
        Resolved batch size (1–100).
    """
    for source_name, raw in [("env", env_value), ("repo_variable", repo_value)]:
        if raw is not None and raw.strip():
            try:
                parsed = int(raw.strip())
            except ValueError:
                print(
                    f"WARNING: Invalid {VARIABLE_BATCH_SIZE} from {source_name}={raw!r} — falling through",
                    file=sys.stderr,
                )
                continue

            if parsed < 1 or parsed > MAX_BATCH_SIZE:
                print(
                    f"WARNING: {VARIABLE_BATCH_SIZE} from {source_name}={parsed} "
                    f"outside [1, {MAX_BATCH_SIZE}] — clamping",
                    file=sys.stderr,
                )
            return max(1, min(parsed, MAX_BATCH_SIZE))

    return default


def resolve_pool_size(
    env_value: str | None,
    repo_value: str | None,
    default: int = DEFAULT_POOL_SIZE,
) -> int:
    """Resolve pool size (eligible PR limit) from environment variable and repo variable.

    The pool size restricts the round-robin rotation to the N oldest eligible PRs.
    PRs beyond this limit are excluded from scheduling until older PRs are merged/closed.

    Priority: env_value > repo_value > default.
    Values outside [1, 100] are clamped with a warning.

    Args:
        env_value: Value from AI_PR_LOOP_ELIGIBLE_PR_LIMIT env var (or None).
        repo_value: Value from repository variable (or None).
        default: Default pool size if both sources are unavailable.

    Returns:
        Resolved pool size (1–100).
    """
    for source_name, raw in [("env", env_value), ("repo_variable", repo_value)]:
        if raw is not None and raw.strip():
            try:
                parsed = int(raw.strip())
            except ValueError:
                print(
                    f"WARNING: Invalid {VARIABLE_POOL_SIZE} from {source_name}={raw!r} — falling through",
                    file=sys.stderr,
                )
                continue

            if parsed < 1 or parsed > MAX_POOL_SIZE:
                print(
                    f"WARNING: {VARIABLE_POOL_SIZE} from {source_name}={parsed} "
                    f"outside [1, {MAX_POOL_SIZE}] — clamping",
                    file=sys.stderr,
                )
            return max(1, min(parsed, MAX_POOL_SIZE))

    return default


def resolve_cursor(provider: CIPlatformProvider) -> int | None:
    """Resolve the round-robin cursor using two-tier strategy.

    Tier 1: Read AI_PR_LOOP_LAST_DISPATCHED_PR variable (fast, no API pagination).
    Tier 2: Query recent ai-pr-loop.yml runs to infer the last dispatched PR (fallback).

    Args:
        provider: CI platform provider instance.

    Returns:
        Last dispatched PR number, or None if no cursor can be resolved.
    """
    # Tier 1: Try repository variable
    try:
        raw_last = provider.get_variable(VARIABLE_LAST_DISPATCHED)
    except ProviderRateLimitError as exc:
        if exc.is_rate_limit:
            raise
        logger.warning("Failed to read cursor variable %s: %s", VARIABLE_LAST_DISPATCHED, exc)
        raw_last = None
    except Exception as exc:
        logger.warning("Failed to read cursor variable %s: %s", VARIABLE_LAST_DISPATCHED, exc)
        raw_last = None
    if raw_last is not None:
        raw_last = raw_last.strip()
    if raw_last:
        try:
            pr_number = int(raw_last)
            if pr_number > 0:
                logger.info("Cursor resolved from variable: PR #%d", pr_number)
                return pr_number
        except ValueError:
            pass

    # Tier 2: Fallback — query recent workflow runs
    logger.info("Variable cursor unavailable — falling back to workflow run history")
    try:
        events = provider.get_recent_dispatch_history("ai-pr-loop.yml")
        if events:
            # Events should be sorted most-recent-first by the provider
            latest = events[0]
            if latest.pr_number > 0:
                logger.info(
                    "Cursor resolved from run history: PR #%d",
                    latest.pr_number,
                )
                return latest.pr_number
    except ProviderRateLimitError as exc:
        if exc.is_rate_limit:
            raise
        logger.warning("Failed to query workflow run history for cursor: %s", exc)
    except Exception as exc:
        logger.warning("Failed to query workflow run history for cursor: %s", exc)

    logger.info("No cursor found — will start from oldest eligible PR")
    return None


def _pause_scheduler_for_rate_limit(
    provider: CIPlatformProvider,
    exc: ProviderRateLimitError,
    *,
    run_mode: str,
    batch_size: int,
    pool_size: int,
    eligible_count: int,
    phase: str,
    dispatched_prs: list[int] | None = None,
    cursor_before: int | None = None,
    cursor_after: int | None = None,
    cursor_persisted: bool = False,
) -> SchedulerResult:
    """Persist cooldown state and return the standard paused scheduler result."""
    paused = persist_cooldown(provider, exc)
    key = ""
    source = exc.source
    resume_at = ""
    remaining = 0
    if paused is not None:
        key, record = paused
        source = record.source
        resume_at = format_resume_at(record.resume_at)
        remaining = max(0, int(record.resume_at - time.time()))
    logger.warning(
        "Scheduler paused after provider rate-limit during %s: "
        "provider=%s credential=%s source=%s resume_at=%s remaining_delay=%ss",
        phase,
        exc.provider or "github",
        exc.credential_identity or "unknown",
        source or "unknown",
        resume_at or "unknown",
        remaining,
    )
    return SchedulerResult(
        run_mode=run_mode,
        batch_size=batch_size,
        pool_size=pool_size,
        eligible_count=eligible_count,
        dispatched_count=len(dispatched_prs or []),
        dispatched_prs=dispatched_prs or [],
        cursor_before=cursor_before,
        cursor_after=cursor_after if cursor_after is not None else cursor_before,
        cursor_persisted=cursor_persisted,
        status="rate_limit_paused",
        cooldown_key=key,
        cooldown_source=source,
        cooldown_resume_at=resume_at,
        cooldown_remaining_seconds=remaining,
    )


def run_scheduler(provider: CIPlatformProvider, *, dry_run: bool = False) -> SchedulerResult:
    """Execute the full scheduling cycle.

    1. Validate REPO_VARIABLE_WRITER_PAT (log warning if invalid)
    2. Load config from repo variables (with API fallback for cursor)
    3. List eligible PRs via provider
    4. Propagate allowlisted labels from each PR's linked issues (best-effort)
    5. Select next batch via round-robin
    6. Dispatch ai-pr-loop.yml for each selected PR
    7. Attempt to update cursor variable (graceful on failure)

    Args:
        provider: CI platform provider instance.
        dry_run: If True, skip dispatch and cursor writes.

    Returns:
        SchedulerResult with details of the scheduling cycle.
    """
    run_mode = "dry_run" if dry_run else "live"
    token_present = bool(os.environ.get("REPO_VARIABLE_WRITER_PAT", "").strip())

    try:
        paused = active_cooldown(
            provider,
            credential_identity=ai_pr_loop_credential_identities(),
            use_writer_token=token_present,
        )
    except ProviderRateLimitError as exc:
        if not exc.is_rate_limit:
            raise
        return _pause_scheduler_for_rate_limit(
            provider,
            exc,
            run_mode=run_mode,
            batch_size=DEFAULT_BATCH_SIZE,
            pool_size=DEFAULT_POOL_SIZE,
            eligible_count=0,
            phase="reading provider cooldown gate",
        )
    if paused is not None:
        key, record = paused
        remaining = max(0, int(record.resume_at - time.time()))
        logger.warning(
            "Scheduler paused by provider cooldown: key=%s source=%s resume_at=%s remaining_delay=%ss",
            key,
            record.source,
            format_resume_at(record.resume_at),
            remaining,
        )
        return SchedulerResult(
            run_mode=run_mode,
            batch_size=DEFAULT_BATCH_SIZE,
            pool_size=DEFAULT_POOL_SIZE,
            eligible_count=0,
            dispatched_count=0,
            cursor_persisted=False,
            status="rate_limit_paused",
            cooldown_key=key,
            cooldown_source=record.source,
            cooldown_resume_at=format_resume_at(record.resume_at),
            cooldown_remaining_seconds=remaining,
        )

    # Step 1: Validate token (informational only)
    try:
        token_valid = provider.validate_variable_token()
    except ProviderRateLimitError as exc:
        if exc.is_rate_limit:
            return _pause_scheduler_for_rate_limit(
                provider,
                exc,
                run_mode=run_mode,
                batch_size=DEFAULT_BATCH_SIZE,
                pool_size=DEFAULT_POOL_SIZE,
                eligible_count=0,
                phase="validating REPO_VARIABLE_WRITER_PAT",
            )
        logger.warning("REPO_VARIABLE_WRITER_PAT validation errored: %s", exc)
        token_valid = False
    except Exception as exc:
        logger.warning("REPO_VARIABLE_WRITER_PAT validation errored: %s", exc)
        token_valid = False
    if not token_valid:
        if token_present:
            logger.warning(
                "REPO_VARIABLE_WRITER_PAT validation failed — cursor will not persist. "
                "Falling back to workflow-run-history cursor resolution on next cycle."
            )
        else:
            logger.info(
                "REPO_VARIABLE_WRITER_PAT not configured — cursor persistence disabled. "
                "Falling back to workflow-run-history cursor resolution on next cycle."
            )

    # Step 2: Resolve batch size, pool size, and cursor
    env_batch = os.environ.get(VARIABLE_BATCH_SIZE)
    try:
        repo_batch = provider.get_variable(VARIABLE_BATCH_SIZE)
    except ProviderRateLimitError as exc:
        if not exc.is_rate_limit:
            raise
        return _pause_scheduler_for_rate_limit(
            provider,
            exc,
            run_mode=run_mode,
            batch_size=DEFAULT_BATCH_SIZE,
            pool_size=DEFAULT_POOL_SIZE,
            eligible_count=0,
            phase=f"reading {VARIABLE_BATCH_SIZE}",
        )
    except Exception as exc:
        logger.warning("Failed to read repo variable %s: %s", VARIABLE_BATCH_SIZE, exc)
        repo_batch = None
    batch_size = resolve_batch_size(env_batch, repo_batch)

    env_pool = os.environ.get(VARIABLE_POOL_SIZE)
    try:
        repo_pool = provider.get_variable(VARIABLE_POOL_SIZE)
    except ProviderRateLimitError as exc:
        if not exc.is_rate_limit:
            raise
        return _pause_scheduler_for_rate_limit(
            provider,
            exc,
            run_mode=run_mode,
            batch_size=batch_size,
            pool_size=DEFAULT_POOL_SIZE,
            eligible_count=0,
            phase=f"reading {VARIABLE_POOL_SIZE}",
        )
    except Exception as exc:
        logger.warning("Failed to read repo variable %s: %s", VARIABLE_POOL_SIZE, exc)
        repo_pool = None
    pool_size = resolve_pool_size(env_pool, repo_pool)

    try:
        cursor_before = resolve_cursor(provider)
    except ProviderRateLimitError as exc:
        if not exc.is_rate_limit:
            raise
        return _pause_scheduler_for_rate_limit(
            provider,
            exc,
            run_mode=run_mode,
            batch_size=batch_size,
            pool_size=pool_size,
            eligible_count=0,
            phase="resolving dispatch cursor",
        )
    logger.info("Config: batch_size=%d, pool_size=%d, cursor=%s", batch_size, pool_size, cursor_before)

    # Step 3: List eligible PRs (limited to pool size when supported by provider)
    try:
        eligible = provider.list_eligible_prs(max_prs=pool_size)
    except ProviderRateLimitError as exc:
        if not exc.is_rate_limit:
            raise
        return _pause_scheduler_for_rate_limit(
            provider,
            exc,
            run_mode=run_mode,
            batch_size=batch_size,
            pool_size=pool_size,
            eligible_count=0,
            phase="eligibility listing",
            cursor_before=cursor_before,
        )
    except TypeError as exc:
        message = str(exc)
        if "unexpected keyword argument" not in message or "max_prs" not in message:
            raise
        try:
            eligible = provider.list_eligible_prs()
        except ProviderRateLimitError as rate_limit_exc:
            if not rate_limit_exc.is_rate_limit:
                raise
            return _pause_scheduler_for_rate_limit(
                provider,
                rate_limit_exc,
                run_mode=run_mode,
                batch_size=batch_size,
                pool_size=pool_size,
                eligible_count=0,
                phase="eligibility listing fallback",
                cursor_before=cursor_before,
            )
    fetched_count = len(eligible)
    eligible = eligible[:pool_size]
    pr_numbers = [pr.number for pr in eligible]
    logger.info(
        "Eligible PRs fetched from provider: %d (pool size: %d), in pool: %s",
        fetched_count,
        pool_size,
        pr_numbers,
    )

    if not pr_numbers:
        logger.info("No eligible PRs — nothing to dispatch")
        return SchedulerResult(
            run_mode=run_mode,
            batch_size=batch_size,
            pool_size=pool_size,
            eligible_count=fetched_count,
            dispatched_count=0,
            dispatched_prs=[],
            cursor_before=cursor_before,
            cursor_after=cursor_before,
            cursor_persisted=False,
        )

    # Step 4: Propagate allowlisted labels from linked issues (best-effort — a
    # failure here must never abort scheduling).
    try:
        propagate_linked_issue_labels(provider, eligible, dry_run=dry_run)
    except ProviderRateLimitError as exc:
        if not exc.is_rate_limit:
            raise
        return _pause_scheduler_for_rate_limit(
            provider,
            exc,
            run_mode=run_mode,
            batch_size=batch_size,
            pool_size=pool_size,
            eligible_count=fetched_count,
            phase="label propagation",
            cursor_before=cursor_before,
        )
    except Exception as exc:
        logger.warning("Linked-issue label propagation failed: %s — continuing", exc)

    # Step 5: Select batch
    batch = select_next_batch(eligible, cursor_before, batch_size)
    logger.info("Selected batch (%d): %s", len(batch), batch)

    # Step 6: Dispatch
    dispatched: list[int] = []
    had_dispatch_error = False
    if dry_run:
        for pr_number in batch:
            logger.info("DRY RUN — would dispatch PR #%d", pr_number)
            dispatched.append(pr_number)
    else:
        for pr_number in batch:
            try:
                provider.dispatch_workflow(
                    workflow="ai-pr-loop.yml",
                    inputs={"pr_number": str(pr_number), "trigger_reason": "scheduler_round_robin"},
                )
                dispatched.append(pr_number)
                logger.info("Dispatched ai-pr-loop for PR #%d", pr_number)
            except ProviderRateLimitError as exc:
                if not exc.is_rate_limit:
                    raise
                rl_cursor_after = dispatched[-1] if dispatched else cursor_before
                rl_cursor_persisted = False
                if dispatched and not dry_run and token_valid:
                    try:
                        provider.set_variable(VARIABLE_LAST_DISPATCHED, str(dispatched[-1]))
                        rl_cursor_persisted = True
                        logger.info(
                            "Cursor persisted before rate-limit pause: %s=%d",
                            VARIABLE_LAST_DISPATCHED,
                            dispatched[-1],
                        )
                    except Exception as cursor_exc:
                        if isinstance(cursor_exc, ProviderRateLimitError) and cursor_exc.is_rate_limit:
                            logger.warning(
                                "Cursor persistence before rate-limit pause also hit a provider cooldown; "
                                "continuing with dispatch pause handling"
                            )
                        else:
                            logger.warning(
                                "Failed to persist cursor before rate-limit pause: %s — "
                                "next cycle will use workflow-run-history fallback",
                                cursor_exc,
                            )
                return _pause_scheduler_for_rate_limit(
                    provider,
                    exc,
                    run_mode=run_mode,
                    batch_size=batch_size,
                    pool_size=pool_size,
                    eligible_count=fetched_count,
                    phase="dispatch",
                    dispatched_prs=dispatched,
                    cursor_before=cursor_before,
                    cursor_after=rl_cursor_after,
                    cursor_persisted=rl_cursor_persisted,
                )
            except Exception as exc:
                logger.error("Failed to dispatch for PR #%d: %s — stopping batch", pr_number, exc)
                had_dispatch_error = True
                break

    # Step 7: Persist cursor (best-effort)
    cursor_after = dispatched[-1] if dispatched else cursor_before
    cursor_persisted = False
    should_persist_cursor = bool(dispatched) and not dry_run
    if should_persist_cursor:
        if token_valid:
            try:
                provider.set_variable(VARIABLE_LAST_DISPATCHED, str(dispatched[-1]))
                logger.info("Cursor persisted: %s=%d", VARIABLE_LAST_DISPATCHED, dispatched[-1])
                cursor_persisted = True
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    return _pause_scheduler_for_rate_limit(
                        provider,
                        exc,
                        run_mode=run_mode,
                        batch_size=batch_size,
                        pool_size=pool_size,
                        eligible_count=fetched_count,
                        phase="persisting dispatch cursor",
                        dispatched_prs=dispatched,
                        cursor_before=cursor_before,
                        cursor_after=cursor_after,
                        cursor_persisted=False,
                    )
                logger.warning(
                    "Failed to persist cursor (REPO_VARIABLE_WRITER_PAT may be missing): %s — "
                    "next cycle will use workflow-run-history fallback",
                    exc,
                )
        else:
            logger.info(
                "Skipping cursor persistence because variable writer token is unavailable or invalid; "
                "workflow-run-history fallback will be used on next cycle"
            )

    return SchedulerResult(
        run_mode=run_mode,
        batch_size=batch_size,
        pool_size=pool_size,
        eligible_count=fetched_count,
        dispatched_count=len(dispatched),
        dispatched_prs=dispatched,
        cursor_before=cursor_before,
        cursor_after=cursor_after,
        cursor_persisted=cursor_persisted,
        had_dispatch_error=had_dispatch_error,
    )
