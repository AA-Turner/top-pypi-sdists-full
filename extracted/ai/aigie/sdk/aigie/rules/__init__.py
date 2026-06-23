"""
Aigie Rules Module - Local rules engine for fast interception decisions.

This module provides a fast, local rules engine that can make interception
decisions without network calls, enabling sub-5ms decision latency.
"""

from aigie.rules.builtin import (
    BlockedPatternsRule,
    ContextDriftRule,
    CostLimitRule,
    RateLimitRule,
    TokenLimitRule,
)
from aigie.rules.engine import LocalRulesEngine, Rule, RuleDecision, RuleResult

__all__ = [
    # Core
    "LocalRulesEngine",
    "Rule",
    "RuleResult",
    "RuleDecision",
    # Built-in Rules
    "CostLimitRule",
    "TokenLimitRule",
    "BlockedPatternsRule",
    "RateLimitRule",
    "ContextDriftRule",
]
