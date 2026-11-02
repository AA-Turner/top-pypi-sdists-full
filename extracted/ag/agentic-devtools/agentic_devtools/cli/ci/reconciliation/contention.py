"""Bounded, jittered retries for queue transitions without external side effects."""

from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable
from dataclasses import replace

from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.dispatch_identity import derive_persisted_dispatch_operation_id
from agentic_devtools.cli.ci.reconciliation.models import OperationStatus, QueueState, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import ConcurrentModificationError, QueueStore

logger = logging.getLogger(__name__)


class QueueTransitionRetryExhaustedError(RuntimeError):
    """Raised when pure queue-transition CAS retries exhaust their bounded budget."""

    def __init__(
        self,
        message: str,
        *,
        operation_id: str = "",
    ) -> None:
        super().__init__(message)
        self.operation_id = operation_id


def wait_for_contention(attempt: int) -> None:
    """Desynchronize writers with exponential jitter capped at five seconds."""
    if attempt < 1:
        raise ValueError("attempt must be positive")
    time.sleep(random.uniform(0.25, min(5.0, 0.25 * 2 ** min(attempt, 5))))


def reload_after_conflict(store: QueueStore, attempt: int) -> QueueState:
    """Wait before reading the latest queue revision, not after taking a snapshot."""
    wait_for_contention(attempt)
    return store.load()


def rebase_rehydration(
    current: QueueState,
    seed: QueueState,
    *,
    unresolved_dispatch_pr: int | None = None,
) -> QueueState:
    """Retain recovery authority and a matching unresolved-dispatch fence."""
    if (
        current.recovery_epoch > seed.recovery_epoch
        or [replace(record, rehydration_attempted=True) for record in current.quarantines] != seed.quarantines
    ):
        raise RuntimeError("Recovery authority changed during inventory observation")
    rebased = replace(current, recovery_epoch=seed.recovery_epoch, quarantines=seed.quarantines)
    if unresolved_dispatch_pr is None:
        return rebased
    seed_item = seed.items.get(unresolved_dispatch_pr)
    if (
        seed_item is None
        or seed_item.pr_number != unresolved_dispatch_pr
        or seed_item.status is not WorkItemStatus.UNKNOWN
        or not all((seed_item.change_id, seed_item.claim_id, seed_item.lease_id, seed_item.operation_id))
    ):
        return rebased
    winning_item = current.items.get(unresolved_dispatch_pr)
    if winning_item is None:
        return rebased
    if (
        winning_item.pr_number != unresolved_dispatch_pr
        or winning_item.status not in {WorkItemStatus.CLAIMED, WorkItemStatus.LEASED, WorkItemStatus.UNKNOWN}
        or winning_item.operation_status is not OperationStatus.ACTIVE
        or (
            winning_item.change_id,
            winning_item.claim_id,
            winning_item.lease_id,
            winning_item.operation_id,
        )
        != (seed_item.change_id, seed_item.claim_id, seed_item.lease_id, seed_item.operation_id)
    ):
        return rebased
    return replace(
        rebased,
        items={
            **current.items,
            unresolved_dispatch_pr: replace(
                winning_item,
                eligibility="ineligible",
                due_at=None,
                status=WorkItemStatus.UNKNOWN,
            ),
        },
    )


def retry_queue_transition(
    store: QueueStore,
    state: QueueState,
    transition: Callable[[QueueState], QueueState],
    *,
    authoritative: bool = False,
    triggering_pr: tuple[int | None, str] | None = None,
) -> QueueState:
    """Recompute a pure transition on each winning revision, never retrying dispatch."""
    triggering_pr_number, triggering_change_id = triggering_pr or (None, "")
    triggering_operation_id: str | None = None
    for attempt in range(1, config.MAX_RETRY_ATTEMPTS + 1):
        updated = transition(state)
        if attempt == 1:
            triggering_operation_id = derive_persisted_dispatch_operation_id(
                updated,
                triggering_pr_number,
                triggering_change_id,
            )
        if updated == state:
            logger.info("Winning queue state already covers observation; no update needed")
            return state
        try:
            save = store.save_rehydration if authoritative else store.save
            saved = save(updated, expected_revision=state.revision)
        except ConcurrentModificationError as exc:
            if attempt == config.MAX_RETRY_ATTEMPTS:
                raise QueueTransitionRetryExhaustedError(
                    f"Pre-dispatch queue CAS retry budget of {config.MAX_RETRY_ATTEMPTS} exhausted: {exc}",
                    operation_id=triggering_operation_id or "",
                ) from exc
            logger.warning("Pre-dispatch queue CAS conflict; reloading winning state (attempt %s): %s", attempt, exc)
            state = reload_after_conflict(store, attempt)
        else:
            if attempt > 1:
                logger.info("Pre-dispatch queue CAS retry recovered at revision %s", saved.revision)
            return saved
    raise ValueError("MAX_RETRY_ATTEMPTS must be positive")
