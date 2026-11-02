"""Verification of persisted due work after a pre-dispatch CAS conflict."""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from agentic_devtools.cli.ci.reconciliation.dispatch_identity import derive_dispatch_operation_id
from agentic_devtools.cli.ci.reconciliation.models import WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import QueueStore

logger = logging.getLogger(__name__)


def verify_persisted_due_work(
    store: QueueStore,
    *,
    pr_number: int | None,
    head_sha: str,
    expected_operation_id: str | None,
    now: datetime | None = None,
) -> str | None:
    """Return the matching persisted operation ID only when its queue row is due."""
    if pr_number is None or not head_sha or not expected_operation_id:
        return None
    try:
        winning_state = store.load()
    except Exception as exc:  # noqa: BLE001
        logger.error("Unable to confirm persisted due work after queue CAS exhaustion: %s", exc)
        return None

    item = winning_state.items.get(pr_number)
    current = now if now is not None else datetime.now(UTC)
    try:
        if current.utcoffset() is None:
            return None
        current = current.astimezone(UTC)
    except OverflowError, ValueError:
        return None
    timestamps = (item.due_at, item.last_observed_at, item.completed_at) if item is not None else ()
    try:
        if any(
            timestamp is not None
            and (
                not isinstance(timestamp, datetime)
                or timestamp.utcoffset() is None
                or timestamp.astimezone(UTC) > current
            )
            for timestamp in timestamps
        ):
            return None
    except OverflowError, ValueError:
        return None
    if (
        item is None
        or item.pr_number != pr_number
        or item.repo != winning_state.repo
        or item.change_id != head_sha
        or item.status is not WorkItemStatus.QUEUED
        or item.eligibility != "eligible"
        or (item.due_at is not None and item.due_at > current)
    ):
        return None
    operation_id = derive_dispatch_operation_id(item)
    return operation_id if operation_id == expected_operation_id else None
