"""Shared domain models for structured LLM output schemas.

Provides cross-cutting types used by both PR review and work-on-issue domains.
"""

from .confidence import ConfidenceScore
from .escalation import EscalationReason
from .stop_condition import StopCondition

__all__ = [
    "ConfidenceScore",
    "EscalationReason",
    "StopCondition",
]
