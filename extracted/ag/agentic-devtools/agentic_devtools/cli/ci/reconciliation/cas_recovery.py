"""Fail-closed reporting for exhausted pre-dispatch queue CAS retries."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Callable
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO

from agentic_devtools.cli.ci.reconciliation.cas_recovery_verification import verify_persisted_due_work
from agentic_devtools.cli.ci.reconciliation.contention import QueueTransitionRetryExhaustedError
from agentic_devtools.cli.ci.reconciliation.dispatch_identity import (
    DispatchRetryExhaustedError,
    derive_persisted_dispatch_operation_id,
)
from agentic_devtools.cli.ci.reconciliation.models import QueueState, ReconciliationAction
from agentic_devtools.cli.ci.reconciliation.queue_store import ConcurrentModificationError, QueueStore

logger = logging.getLogger(__name__)


class _PreDispatchCASRetry(Exception):
    """Signal that reconciliation should restart after a pre-dispatch CAS conflict."""

    def __init__(
        self,
        message: str,
        *,
        queue_store: QueueStore | None = None,
        pr_number: int | None = None,
        head_sha: str = "",
        expected_operation_id: str | None = None,
        json_output: bool = False,
    ) -> None:
        super().__init__(message)
        self.queue_store = queue_store
        self.pr_number = pr_number
        self.head_sha = head_sha
        self.expected_operation_id = expected_operation_id
        self.json_output = json_output


class CASExhaustionReporter:
    """Classify bounded pre-dispatch exhaustion only after verifying persisted due work."""

    @classmethod
    def run_with_outer_retries(
        cls,
        operation: Callable[[_PreDispatchCASRetry | None], int],
        retry_budget: int,
        wait_for_retry: Callable[[int], None],
    ) -> int:
        """Retry the command while retaining the first triggering operation identity."""
        attempt = 0
        triggering_retry: _PreDispatchCASRetry | None = None
        while True:
            try:
                if triggering_retry is None:
                    result = operation(None)
                else:
                    output = StringIO()
                    with redirect_stdout(output):
                        result = operation(triggering_retry)
                    if result == 0 and not cls._trigger_operation_is_persisted(triggering_retry):
                        logger.error("Outer retry did not preserve the triggering operation in persisted queue state")
                        return 1
                    sys.stdout.write(output.getvalue())
            except _PreDispatchCASRetry as exc:
                if triggering_retry is None:
                    triggering_retry = exc
                else:
                    triggering_retry.queue_store = exc.queue_store
                attempt += 1
                if attempt >= retry_budget:
                    return cls.outer_retry_result(exc, retry_budget, triggering_retry=triggering_retry)
                logger.warning(
                    "Queue revision conflict before provider dispatch; retrying reconciliation from the winning state "
                    "(attempt %d/%d): %s",
                    attempt,
                    retry_budget,
                    exc,
                )
                wait_for_retry(attempt)
                continue
            if attempt > 0 and result == 0:
                logger.info("Pre-dispatch queue CAS retry succeeded")
            return result

    @staticmethod
    def _trigger_operation_is_persisted(triggering_retry: _PreDispatchCASRetry) -> bool:
        if triggering_retry.pr_number is None or not triggering_retry.head_sha:
            return True
        if triggering_retry.queue_store is None or not triggering_retry.expected_operation_id:
            return False
        try:
            state = triggering_retry.queue_store.load()
        except Exception as exc:  # noqa: BLE001
            logger.error("Unable to confirm outer retry trigger in persisted queue state: %s", exc)
            return False
        return (
            derive_persisted_dispatch_operation_id(
                state,
                triggering_retry.pr_number,
                triggering_retry.head_sha,
            )
            == triggering_retry.expected_operation_id
        )

    @staticmethod
    def update_retry_store(triggering_retry: _PreDispatchCASRetry | None, store: QueueStore) -> None:
        if triggering_retry is not None:
            triggering_retry.queue_store = store

    @staticmethod
    def _report_deferred_if_due_work_is_confirmed(
        store: QueueStore,
        *,
        pr_number: int | None,
        head_sha: str,
        expected_operation_id: str | None,
        json_output: bool,
        now: datetime | None = None,
    ) -> bool:
        operation_id = verify_persisted_due_work(
            store,
            pr_number=pr_number,
            head_sha=head_sha,
            expected_operation_id=expected_operation_id,
            now=now,
        )
        if operation_id is None:
            return False

        message = (
            "Reconciliation is incomplete: matching eligible due work is persisted for the scheduled "
            "reconciler; no provider dispatch or product/security success is claimed."
        )
        logger.warning("%s", message)
        if json_output:
            print(
                json.dumps(
                    {
                        "action": ReconciliationAction.DEFERRED.value,
                        "message": message,
                        "lease_id": None,
                        "operation_id": operation_id,
                        "pr_number": pr_number,
                    },
                    indent=2,
                )
            )
        else:
            print(message)
        return True

    @classmethod
    def dispatch_retry_result(
        cls,
        store: QueueStore,
        args: argparse.Namespace,
        exc: DispatchRetryExhaustedError,
        *,
        triggering_retry: _PreDispatchCASRetry | None = None,
    ) -> int:
        if (
            exc.pr_number == args.trusted_pr_number
            and exc.change_id == args.trusted_head_sha
            and cls._report_deferred_if_due_work_is_confirmed(
                store,
                pr_number=args.trusted_pr_number,
                head_sha=args.trusted_head_sha,
                expected_operation_id=(
                    triggering_retry.expected_operation_id if triggering_retry is not None else exc.operation_id
                ),
                json_output=args.json_output,
            )
        ):
            return 0
        logger.error("Dispatch queue CAS retry budget exhausted: %s", exc)
        return 1

    @classmethod
    def transition_retry_result(
        cls,
        store: QueueStore,
        args: argparse.Namespace,
        exc: QueueTransitionRetryExhaustedError,
        *,
        triggering_retry: _PreDispatchCASRetry | None = None,
    ) -> int:
        if cls._report_deferred_if_due_work_is_confirmed(
            store,
            pr_number=args.trusted_pr_number,
            head_sha=args.trusted_head_sha,
            expected_operation_id=(
                triggering_retry.expected_operation_id if triggering_retry is not None else exc.operation_id
            ),
            json_output=args.json_output,
        ):
            return 0
        logger.error("Pre-dispatch queue CAS retry budget exhausted; matching due work was not confirmed: %s", exc)
        return 1

    @staticmethod
    def retry_after_conflict(
        exc: ConcurrentModificationError,
        store: QueueStore,
        args: argparse.Namespace,
        triggering_state: QueueState | None,
    ) -> _PreDispatchCASRetry:
        expected_operation_id = derive_persisted_dispatch_operation_id(
            triggering_state,
            args.trusted_pr_number,
            args.trusted_head_sha,
        )
        return _PreDispatchCASRetry(
            str(exc),
            queue_store=store,
            pr_number=args.trusted_pr_number,
            head_sha=args.trusted_head_sha,
            expected_operation_id=expected_operation_id,
            json_output=args.json_output,
        )

    @classmethod
    def outer_retry_result(
        cls,
        exc: _PreDispatchCASRetry,
        retry_budget: int,
        *,
        triggering_retry: _PreDispatchCASRetry | None = None,
    ) -> int:
        identity = triggering_retry if triggering_retry is not None else exc
        if exc.queue_store is not None and cls._report_deferred_if_due_work_is_confirmed(
            exc.queue_store,
            pr_number=exc.pr_number,
            head_sha=exc.head_sha,
            expected_operation_id=identity.expected_operation_id,
            json_output=exc.json_output,
        ):
            return 0
        logger.error("Pre-dispatch queue CAS retry budget of %d exhausted: %s", retry_budget, exc)
        return 1
