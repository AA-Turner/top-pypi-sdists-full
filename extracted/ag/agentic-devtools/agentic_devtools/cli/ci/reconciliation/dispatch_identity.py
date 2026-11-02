"""Stable identity for reconciliation dispatch attempts."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem


class DispatchRetryExhaustedError(RuntimeError):
    """Raised when queue CAS conflicts exhaust the bounded dispatch retry budget."""

    def __init__(
        self,
        message: str,
        *,
        pr_number: int | None = None,
        change_id: str = "",
        operation_id: str = "",
    ) -> None:
        super().__init__(message)
        self.pr_number = pr_number
        self.change_id = change_id
        self.operation_id = operation_id


def derive_dispatch_operation_id(
    item: WorkItem,
    *,
    operation_id: str | None = None,
    operation_identity: str | None = None,
) -> str:
    """Return the stable operation ID that dispatch_due_work() will use for an item."""
    if operation_id is not None:
        return operation_id
    from agentic_devtools.orchestration.safety.operation_id import compute_operation_id

    return compute_operation_id(
        "dispatch_due_work",
        "reconciliation.dispatch",
        {
            "repo": item.repo,
            "pr_number": item.pr_number,
            "change_id": item.change_id,
            "observation_watermark": (
                operation_identity if operation_identity is not None else item.observation_watermark
            ),
        },
    )


def derive_persisted_dispatch_operation_id(
    state: QueueState | None,
    pr_number: int | None,
    change_id: str,
) -> str | None:
    """Return the operation ID evidenced by a matching item in a queue snapshot."""
    if state is None or pr_number is None or not change_id:
        return None
    item = state.items.get(pr_number)
    if item is None or item.pr_number != pr_number or item.change_id != change_id:
        return None
    return derive_dispatch_operation_id(item)
