"""Node status tracking and resumable node decorator (FR-002, FR-003, FR-010).

Provides ``NodeStatus`` (frozen dataclass tracking per-node completion state),
``NodeFailedError`` (exception carrying state update for failed nodes), and
``resumable_node()`` (decorator adding skip-completed / retry-with-budget logic).
"""

from __future__ import annotations

import dataclasses
import logging
from typing import Any

logger = logging.getLogger(__name__)

_ERROR_SUMMARY_MAX_LENGTH = 200


@dataclasses.dataclass(frozen=True)
class NodeStatus:
    """Terminal status of a workflow node (FR-010).

    Attributes:
        status: One of "completed", "failed", "failed_permanent".
        attempt_count: Total number of execution attempts (>= 1).
        error_summary: Brief error description (None when completed).
    """

    status: str
    attempt_count: int
    error_summary: str | None = None

    def __post_init__(self) -> None:
        """Validate invariants."""
        if self.attempt_count < 1:
            raise ValueError(f"attempt_count must be >= 1, got {self.attempt_count}")
        if self.status == "completed" and self.error_summary is not None:
            raise ValueError("error_summary must be None for completed status")
        if self.status in ("failed", "failed_permanent") and not self.error_summary:
            raise ValueError(f"error_summary must be non-empty for {self.status} status")
        if self.status not in ("completed", "failed", "failed_permanent"):
            raise ValueError(f"Invalid status: {self.status!r}")

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary for state channel persistence."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> NodeStatus:
        """Deserialize from a dictionary."""
        return cls(
            status=data["status"],
            attempt_count=data["attempt_count"],
            error_summary=data.get("error_summary"),
        )


class NodeFailedError(Exception):
    """Raised when a node fails, carrying state update for checkpoint persistence.

    Attributes:
        state_update: Dict to merge into graph state before checkpoint write.
    """

    def __init__(self, message: str, *, state_update: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.state_update = state_update or {}


def resumable_node(node_name: str, *, retry_budget: int = 3):
    """Decorator adding skip/retry/status-write logic around a node function.

    Args:
        node_name: Unique name for this node in the workflow graph.
        retry_budget: Maximum retries beyond the initial attempt.
            A node with retry_budget=3 may execute at most 4 total attempts.

    The decorated function receives the graph state dict and returns a
    state update dict. The decorator:
    - Skips completed nodes (returns empty dict)
    - Checks retry budget and marks failed_permanent when exhausted
    - Records completed/failed status in ``_node_statuses``

    Raises:
        ValueError: If ``node_name`` is empty/whitespace or ``retry_budget`` is negative.
    """
    if not node_name.strip():
        raise ValueError(
            "node_name must be a non-empty, non-whitespace string — all node statuses "
            "are keyed by node_name, so an empty name would collide across nodes and "
            "corrupt skip/retry semantics."
        )
    if retry_budget < 0:
        raise ValueError(f"retry_budget must be >= 0, got {retry_budget!r}.")

    def decorator(fn):
        def wrapper(state: dict[str, Any]) -> dict[str, Any]:
            raw_statuses = state.get("_node_statuses", {})
            # Guard against checkpoint corruption: _node_statuses must be a dict.
            # While normal operation always writes a dict here, defensive handling
            # ensures that a future schema change or a corrupted checkpoint entry
            # never prevents resume — the node simply re-executes from scratch.
            statuses: dict[str, Any] = raw_statuses if isinstance(raw_statuses, dict) else {}
            current_data = statuses.get(node_name)

            # Parse existing status if present
            current: NodeStatus | None = None
            if current_data is not None:
                if isinstance(current_data, dict):
                    try:
                        current = NodeStatus.from_dict(current_data)
                    except (KeyError, ValueError, TypeError):
                        current = None

            # Skip completed nodes
            if current is not None and current.status == "completed":
                logger.info("Skipping completed node: %s", node_name)
                return {}

            # Short-circuit on permanently failed nodes — terminal state, no retry.
            if current is not None and current.status == "failed_permanent":
                raise NodeFailedError(
                    f"Node '{node_name}' has permanently failed after "
                    f"{current.attempt_count} attempt(s): {current.error_summary}",
                    state_update={},
                )

            # Check retry budget for failed nodes
            if current is not None and current.status == "failed":
                if current.attempt_count >= retry_budget + 1:
                    # Budget exhausted — mark as failed_permanent
                    permanent = NodeStatus(
                        status="failed_permanent",
                        attempt_count=current.attempt_count,
                        error_summary=current.error_summary,
                    )
                    state_update = {
                        "_node_statuses": {
                            **statuses,
                            node_name: permanent.to_dict(),
                        }
                    }
                    raise NodeFailedError(
                        f"Retry budget exhausted for node '{node_name}' "
                        f"(attempts: {current.attempt_count}, budget: {retry_budget})",
                        state_update=state_update,
                    )

            # Execute the node
            attempt = (current.attempt_count if current else 0) + 1
            try:
                result = fn(state)
                if not isinstance(result, dict):
                    result = {}

                # Record completed status
                completed = NodeStatus(
                    status="completed",
                    attempt_count=attempt,
                    error_summary=None,
                )
                result["_node_statuses"] = {
                    **statuses,
                    node_name: completed.to_dict(),
                }
                return result
            except NodeFailedError:
                # Re-raise NodeFailedError without wrapping
                raise
            except Exception as exc:
                # Record failed status
                error_msg = str(exc)[:_ERROR_SUMMARY_MAX_LENGTH] or "unknown error"
                failed = NodeStatus(
                    status="failed",
                    attempt_count=attempt,
                    error_summary=error_msg,
                )
                state_update = {
                    "_node_statuses": {
                        **statuses,
                        node_name: failed.to_dict(),
                    }
                }
                raise NodeFailedError(
                    str(exc),
                    state_update=state_update,
                ) from exc

        wrapper.__name__ = fn.__name__
        wrapper.__qualname__ = fn.__qualname__
        wrapper._node_name = node_name  # type: ignore[attr-defined]
        return wrapper

    return decorator
