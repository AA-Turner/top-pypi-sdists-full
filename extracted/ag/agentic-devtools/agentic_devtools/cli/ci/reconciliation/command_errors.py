"""Unexpected-error and classified rate-limit outcomes for the reconciliation CLI."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from datetime import UTC, datetime

from agentic_devtools.cli.ci.exceptions import ProviderRateLimitError
from agentic_devtools.cli.ci.reconciliation.models import Lease, ReconciliationAction
from agentic_devtools.cli.ci.reconciliation.queue_store import QueueStore

logger = logging.getLogger(__name__)


def _get_rate_limit_timing(error: ProviderRateLimitError) -> str:
    """Return the most precise representable rate-limit timing."""
    if error.reset_timestamp is not None:
        try:
            return f"reset at {datetime.fromtimestamp(error.reset_timestamp, UTC).isoformat()}"
        except OverflowError, ValueError, OSError:
            pass
    if error.retry_after_seconds is not None:
        return f"retry after {error.retry_after_seconds:g} seconds"
    return "reset timing unknown"


def handle_reconciliation_error(
    error: Exception,
    *,
    json_output: bool,
    repo: str,
    dispatch_context: tuple[QueueStore, int, Lease | None] | None,
    fence_unknown_dispatch_outcome: Callable[..., bool],
) -> int:
    """Defer only classified rate limits, preserving fencing and genuine failures."""
    if not (isinstance(error, ProviderRateLimitError) and error.is_rate_limit is True):
        logger.error("Unexpected reconciliation error: %s", error)
        if dispatch_context is not None:
            store, failed_pr_number, lease = dispatch_context
            fence_unknown_dispatch_outcome(
                store,
                repo,
                failed_pr_number,
                f"unexpected reconciliation error after provider dispatch for pr_number={failed_pr_number}: {error}",
                lease=lease,
            )
        return 1

    lease = None
    pr_number = None
    if dispatch_context is not None:
        store, pr_number, lease = dispatch_context
        try:
            fenced = fence_unknown_dispatch_outcome(
                store,
                repo,
                pr_number,
                (
                    f"provider rate-limit exhaustion after provider dispatch for pr_number={pr_number}; "
                    "dispatch outcome remains unknown"
                ),
                lease=lease,
            )
        except Exception as fence_error:  # noqa: BLE001
            logger.error("Unable to fence unknown dispatch outcome after provider rate limit: %s", fence_error)
            return 1
        if not fenced:
            logger.error("Unable to defer reconciliation safely: unknown dispatch outcome fencing failed")
            return 1

    timing = _get_rate_limit_timing(error)
    message = (
        f"Reconciliation deferred due to provider rate-limit exhaustion ({timing}); "
        "work was not completed in this run and will not be automatically resumed."
    )
    if dispatch_context is not None:
        message += " Provider dispatch outcome remains unknown and has been fenced."
    logger.warning("%s", message)
    if json_output:
        print(
            json.dumps(
                {
                    "action": ReconciliationAction.DEFERRED.value,
                    "message": message,
                    "lease_id": lease.lease_id if lease else None,
                    "operation_id": lease.operation_id if lease else None,
                    "pr_number": pr_number,
                },
                indent=2,
            )
        )
    else:
        print(message)
    return 0
