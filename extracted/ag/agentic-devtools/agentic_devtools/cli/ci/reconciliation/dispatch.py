"""Due-work selection, eligibility evaluation, and atomic claim acquisition."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING
from uuid import uuid4

from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.models import (
    Claim,
    DispatchEligibility,
    Lease,
    QueueState,
    WorkItem,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import ConcurrentModificationError, QueueStore
from agentic_devtools.cli.ci.reconciliation.queue_transitions import (
    ClaimConflictError,
    acquire_lease,
    claim_work_item,
)

if TYPE_CHECKING:
    from agentic_devtools.orchestration.safety.operation_log import OperationLog

_DISPATCHABLE_STATUSES = frozenset({WorkItemStatus.QUEUED})
_INFLIGHT_STATUSES = frozenset({WorkItemStatus.CLAIMED, WorkItemStatus.LEASED})


@dataclass(frozen=True)
class DispatchResult:
    """Outcome of one dispatch attempt."""

    eligibility: DispatchEligibility
    operation_id: str = ""
    lease: Lease | None = None
    state: QueueState | None = None


EligibilityChecker = Callable[[WorkItem], bool | None]
PreflightChecker = Callable[[WorkItem], bool | None]


class DispatchConflictError(Exception):
    """Raised when dispatch is blocked by a conflicting claim or lease."""


def _defer_due_candidate(
    state: QueueState,
    item: WorkItem,
    now: datetime,
) -> QueueState:
    next_due_at = now + timedelta(minutes=config.RECONCILIATION_SCHEDULE_INTERVAL_MINUTES)
    updated = replace(
        item,
        due_at=next_due_at,
        last_observed_at=now,
    )
    return replace(state, items={**state.items, item.pr_number: updated})


def select_due_work(state: QueueState, now: datetime | None = None) -> list[WorkItem]:
    """Return work items that are currently due for dispatch."""
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    due: list[WorkItem] = []
    for item in state.items.values():
        if item.status in _INFLIGHT_STATUSES:
            continue
        if item.status not in _DISPATCHABLE_STATUSES:
            continue
        if item.eligibility != "eligible":
            continue
        if item.due_at is not None and item.due_at > current:
            continue
        due.append(item)
    due.sort(key=lambda item: (item.due_at or datetime.min.replace(tzinfo=UTC), item.pr_number))
    return due


def evaluate_dispatch_eligibility(item: WorkItem, now: datetime) -> DispatchEligibility:
    """Evaluate current dispatch eligibility for a work item."""
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    is_eligible = item.eligibility == "eligible"
    eligibility_reason = "" if is_eligible else f"eligibility={item.eligibility!r}"
    due_at = item.due_at
    is_due = due_at is None or due_at <= now
    due_reason = "" if is_due or due_at is None else f"due_at={due_at.isoformat()}"
    return DispatchEligibility(
        pr_number=item.pr_number,
        repo=item.repo,
        is_eligible=is_eligible,
        eligibility_reason=eligibility_reason,
        evaluated_at=now,
        is_due=is_due,
        due_reason=due_reason,
    )


def evaluate_eligibility(
    item: WorkItem,
    *,
    now: datetime | None = None,
    checker: EligibilityChecker | None = None,
) -> DispatchEligibility:
    """Evaluate due-ness and current eligibility; ``None`` is unknown."""
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    due = item.due_at is None or item.due_at <= current
    if not due:
        return DispatchEligibility(
            item.pr_number,
            item.repo,
            False,
            "not_due",
            current,
            False,
            "due_at_not_reached",
        )
    result = True if checker is None else checker(item)
    if result is not True:
        reason = "eligibility_unknown" if result is None else "not_eligible"
        return DispatchEligibility(item.pr_number, item.repo, False, reason, current, True, "due")
    return DispatchEligibility(item.pr_number, item.repo, True, "eligible", current, True, "due")


def acquire_dispatch_claim(
    state: QueueState,
    pr_number: int,
    operation_id: str,
    claim_ttl_seconds: int = 300,
) -> tuple[QueueState, Claim]:
    """Atomically acquire a dispatch claim on a work item."""
    item = state.items.get(pr_number)
    if item is None:
        raise KeyError(f"No work item for pr_number={pr_number}")
    if item.eligibility != "eligible":
        raise ValueError(f"pr_number={pr_number} is not eligible for dispatch: eligibility={item.eligibility!r}")
    if item.status != WorkItemStatus.QUEUED:
        raise DispatchConflictError(f"pr_number={pr_number} is not queued")
    if item.due_at is not None and item.due_at > datetime.now(UTC):
        raise DispatchConflictError(f"pr_number={pr_number} is not due")
    try:
        return claim_work_item(
            state,
            pr_number,
            operation_id,
            claim_ttl_seconds=claim_ttl_seconds,
        )
    except ClaimConflictError as exc:
        raise DispatchConflictError(str(exc)) from exc


def dispatch_due_work(
    state: QueueState,
    *,
    eligibility_checker: EligibilityChecker | None = None,
    preflight_checker: PreflightChecker | None = None,
    now: datetime | None = None,
    store: QueueStore | None = None,
    operation_log: OperationLog | None = None,
    operation_id: str | None = None,
) -> DispatchResult:
    """Claim and lease the oldest due item after live eligibility and preflight."""
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    due_candidates = select_due_work(state, current)
    if not due_candidates:
        return DispatchResult(
            DispatchEligibility(0, state.repo, False, "no_due_work", current, False, ""),
            state=state,
        )
    if eligibility_checker is None or preflight_checker is None:
        return DispatchResult(
            DispatchEligibility(0, state.repo, False, "live_checks_unavailable", current, False, ""),
            state=state,
        )

    current_state = state
    last_unknown: DispatchEligibility | None = None
    for candidate in due_candidates:
        item = current_state.items.get(candidate.pr_number)
        if item is None:
            continue
        eligibility = evaluate_dispatch_eligibility(item, current)
        if not eligibility.is_eligible:
            continue
        live_eligibility = eligibility_checker(item)
        if live_eligibility is None:
            last_unknown = DispatchEligibility(
                item.pr_number,
                item.repo,
                False,
                "live_eligibility_unknown",
                current,
                True,
                "due",
            )
            continue
        if live_eligibility is not True:
            deferred_state = _defer_due_candidate(current_state, item, current)
            if store is not None:
                try:
                    current_state = store.save(deferred_state, expected_revision=current_state.revision)
                except ConcurrentModificationError:
                    current_state = store.load()
            else:
                current_state = deferred_state
            continue
        live = preflight_checker(item)
        if live is None:
            last_unknown = DispatchEligibility(
                item.pr_number,
                item.repo,
                False,
                "preflight_unknown",
                current,
                True,
                "due",
            )
            continue
        if live is not True:
            deferred_state = _defer_due_candidate(current_state, item, current)
            if store is not None:
                try:
                    current_state = store.save(deferred_state, expected_revision=current_state.revision)
                except ConcurrentModificationError:
                    current_state = store.load()
            else:
                current_state = deferred_state
            continue
        candidate_operation_id = operation_id
        if candidate_operation_id is None and operation_log is not None:
            from agentic_devtools.orchestration.safety.operation_id import compute_operation_id

            candidate_operation_id = compute_operation_id(
                "dispatch_due_work",
                "reconciliation.dispatch",
                {
                    "repo": item.repo,
                    "pr_number": item.pr_number,
                    "change_id": item.change_id,
                    "observation_watermark": item.observation_watermark,
                },
            )
        elif candidate_operation_id is None:
            candidate_operation_id = str(uuid4())
        assert candidate_operation_id is not None
        if operation_log is not None:
            from agentic_devtools.orchestration.idempotency import is_reconciliation_run_duplicate

            if is_reconciliation_run_duplicate(operation_log, operation_log.run_id, candidate_operation_id):
                continue
        try:
            claimed_state, claim = acquire_dispatch_claim(current_state, item.pr_number, candidate_operation_id)
            leased_state, lease = acquire_lease(claimed_state, claim)
        except DispatchConflictError:
            if store is not None:
                current_state = store.load()
            continue
        if store is not None:
            try:
                persisted = store.save(leased_state, expected_revision=current_state.revision)
            except ConcurrentModificationError:
                current_state = store.load()
                continue
            if operation_log is not None:
                from agentic_devtools.orchestration.safety.operation_log import OperationLogRecord

                operation_log.append(
                    OperationLogRecord(
                        operation_id=candidate_operation_id,
                        run_id=operation_log.run_id,
                        tool_name="reconciliation.dispatch",
                        node_name="dispatch_due_work",
                        status="pending",
                    )
                )
            return DispatchResult(eligibility, candidate_operation_id, lease, persisted)
        if operation_log is not None:
            from agentic_devtools.orchestration.safety.operation_log import OperationLogRecord

            operation_log.append(
                OperationLogRecord(
                    operation_id=candidate_operation_id,
                    run_id=operation_log.run_id,
                    tool_name="reconciliation.dispatch",
                    node_name="dispatch_due_work",
                    status="pending",
                )
            )
        return DispatchResult(eligibility, candidate_operation_id, lease, leased_state)
    return DispatchResult(
        last_unknown or DispatchEligibility(0, current_state.repo, False, "no_due_work", current, False, ""),
        state=current_state,
    )
