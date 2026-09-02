"""Decision types and result containers."""

from __future__ import annotations

import enum
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class ApprovalDecision(enum.Enum):
    """Possible outcomes of a PR review approval evaluation."""

    approve = "approve"
    request_changes = "request_changes"
    escalate = "escalate"


class BudgetDecision(enum.Enum):
    """Possible outcomes of a budget evaluation."""

    continue_ = "continue"
    halt = "halt"


class BlockedDecision(enum.Enum):
    """Possible outcomes of a blocked-state detection."""

    progressing = "progressing"
    blocked = "blocked"


class RetryDecision(enum.Enum):
    """Possible outcomes of a retry evaluation."""

    retry = "retry"
    stop = "stop"


@dataclass(frozen=True)
class DecisionResult(Generic[T]):
    """Container for a decision with rationale and optional metadata.

    Attributes:
        decision: The enum value representing the decision outcome.
        rationale: Human-readable explanation (≤500 chars, non-empty).
        metadata: Additional structured data about the decision.  After
            construction this field holds an immutable ``MappingProxyType``
            (not a plain ``dict``), so ``isinstance(result.metadata, dict)``
            returns ``False``.  Use ``dict(result.metadata)`` to obtain a
            shallow mutable copy; note that values may include non-JSON-serializable
            objects (e.g. ``BudgetViolation`` instances from budget evaluations).
    """

    decision: T
    rationale: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.rationale or not self.rationale.strip():
            msg = "rationale must be non-empty"
            raise ValueError(msg)
        if len(self.rationale) > 500:
            msg = f"rationale must be ≤500 chars, got {len(self.rationale)}"
            raise ValueError(msg)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True)
class BudgetViolation:
    """Represents a single budget constraint violation.

    Attributes:
        constraint_name: Name of the violated constraint (e.g., 'token_budget').
        configured_limit: The configured limit value.
        actual_value: The actual measured value that exceeded the limit.
        message: Human-readable description of the violation.
    """

    constraint_name: str
    configured_limit: object
    actual_value: object
    message: str
