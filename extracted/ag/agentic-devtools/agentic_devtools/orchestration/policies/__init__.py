"""Autonomous decision policy framework.

This package provides configurable policy evaluators that replace human
judgment in autonomous workflows. Each evaluator accepts structured inputs
and returns a DecisionResult containing the decision, rationale, and metadata.

Public API (7 symbols):
    PolicyLoader - Loads policy configuration from YAML with defaults
    ApprovalEvaluator - Evaluates PR review approval decisions
    BudgetEvaluator - Enforces token/time/retry budgets
    BlockedStateDetector - Detects blocked workflow states
    RetryEvaluator - Evaluates retry vs stop decisions
    PolicyConfig - Top-level frozen policy configuration
    DecisionResult - Generic decision container with rationale
"""

from .approval import ApprovalEvaluator
from .blocked import BlockedStateDetector
from .budget import BudgetEvaluator
from .config import PolicyConfig
from .loader import PolicyLoader
from .retry import RetryEvaluator
from .types import DecisionResult

__all__ = [
    "ApprovalEvaluator",
    "BlockedStateDetector",
    "BudgetEvaluator",
    "DecisionResult",
    "PolicyConfig",
    "PolicyLoader",
    "RetryEvaluator",
]
