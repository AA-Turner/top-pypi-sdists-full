"""Example factories for shared domain models.

Provides factory functions that return new, realistic instances of shared models.
"""

from __future__ import annotations

from typing import Any

from ..shared.escalation import EscalationReason
from ..shared.stop_condition import StopCondition


def make_escalation_reason(**kwargs: Any) -> EscalationReason:
    """Create a realistic EscalationReason instance."""
    defaults: dict[str, Any] = {
        "category": "ambiguous_requirements",
        "description": (
            "The issue description does not specify whether the API "
            "should support pagination or return all results at once."
        ),
        "context": "Issue #1234, endpoint GET /api/users",
        "suggested_action": (
            "Ask the product owner to clarify pagination requirements before implementing the endpoint."
        ),
    }
    defaults.update(kwargs)
    return EscalationReason(**defaults)


def make_stop_condition(**kwargs: Any) -> StopCondition:
    """Create a realistic StopCondition instance."""
    defaults: dict[str, Any] = {
        "reason": ("Token budget exceeded: 45,000 tokens used of 40,000 budget for this workflow step."),
        "is_recoverable": True,
        "details": (
            "The implementation plan generation consumed more tokens "
            "than allocated. Consider increasing the budget or breaking "
            "the issue into smaller sub-tasks."
        ),
    }
    defaults.update(kwargs)
    return StopCondition(**defaults)


def make_confidence_score() -> float:
    """Create a realistic ConfidenceScore value (0.0-1.0)."""
    return 0.87
