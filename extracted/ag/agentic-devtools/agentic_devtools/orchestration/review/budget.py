"""Token budget calculation and enforcement for source context retrieval.

Provides ``TokenBudget`` for tracking token consumption against a configurable
budget, and ``estimate_tokens`` for character-based token estimation (1 token
per 3.5 characters as the primary enforcement heuristic per FR-004).
"""

from __future__ import annotations

import logging
import math
from typing import Any

logger = logging.getLogger(__name__)

# Default character-to-token ratio (conservative estimate).
DEFAULT_CHARS_PER_TOKEN: float = 3.5

# Default safety margin (10% of total budget is reserved).
DEFAULT_SAFETY_MARGIN: float = 0.10

# Hardcoded fallback budget when no explicit or model-derived budget is available.
FALLBACK_BUDGET_TOKENS: int = 100_000

# Fraction of model context window allocated to source context.
MODEL_CONTEXT_FRACTION: float = 0.60


def estimate_tokens(text: str, chars_per_token: float = DEFAULT_CHARS_PER_TOKEN) -> int:
    """Estimate token count using character-based heuristic.

    Args:
        text: The text to estimate tokens for.
        chars_per_token: Characters per token ratio (default: 3.5).

    Returns:
        Estimated token count (ceiling of len(text) / chars_per_token).
    """
    if not text:
        return 0
    if chars_per_token <= 0:
        raise ValueError("chars_per_token must be > 0")
    return math.ceil(len(text) / chars_per_token)


def resolve_model_context_window(model_id: str | None) -> int | None:
    """Resolve context window size for a model ID.

    Uses prefix-matching against the known model context windows table
    in ``token_counter.py``.

    Args:
        model_id: Model identifier (e.g., "gpt-4o", "gpt-4o-2024-05-13").

    Returns:
        Context window size in tokens, or ``None`` if model is unknown.
    """
    if not model_id:
        return None

    from agentic_devtools.orchestration.llm.token_counter import (
        MODEL_CONTEXT_WINDOWS,
        _prefix_lookup,
    )

    # Use a sentinel to detect "no match" vs "matched to default"
    _SENTINEL = -1
    result = _prefix_lookup(MODEL_CONTEXT_WINDOWS, model_id, _SENTINEL)
    if result == _SENTINEL:
        return None
    return result


class TokenBudget:
    """Tracks token consumption against a configured budget.

    Budget resolution priority:
    1. Explicit ``budget_tokens`` parameter
    2. Model-derived (60% of model context window)
    3. Hardcoded fallback (100,000 tokens)

    A safety margin (default 10%) is subtracted from the total budget.
    """

    def __init__(
        self,
        *,
        budget_tokens: int | str | None = None,
        model_id: str | None = None,
        safety_margin: float = DEFAULT_SAFETY_MARGIN,
        chars_per_token: float = DEFAULT_CHARS_PER_TOKEN,
    ) -> None:
        if safety_margin < 0 or safety_margin >= 1:
            raise ValueError("safety_margin must be >= 0 and < 1")
        if chars_per_token <= 0:
            raise ValueError("chars_per_token must be > 0")

        self._chars_per_token = chars_per_token
        self._safety_margin = safety_margin
        self._consumed: int = 0

        # Resolve total budget
        explicit_budget: int | None = None
        if budget_tokens is not None:
            try:
                explicit_budget = int(budget_tokens)
            except (TypeError, ValueError) as exc:
                raise ValueError("budget_tokens must be an integer > 0 when provided") from exc
            if explicit_budget <= 0:
                raise ValueError("budget_tokens must be > 0 when provided")

        if explicit_budget is not None:
            self._total_budget = explicit_budget
            self._budget_source = "explicit"
        else:
            model_window = resolve_model_context_window(model_id)
            if model_window is not None:
                self._total_budget = int(model_window * MODEL_CONTEXT_FRACTION)
                self._budget_source = f"model-derived ({model_id}, {MODEL_CONTEXT_FRACTION:.0%} of {model_window})"
            else:
                self._total_budget = FALLBACK_BUDGET_TOKENS
                self._budget_source = "fallback"

        self._effective_budget = int(self._total_budget * (1 - self._safety_margin))

        logger.info(
            "TokenBudget initialized: source=%s, total=%d, effective=%d (margin=%.0f%%)",
            self._budget_source,
            self._total_budget,
            self._effective_budget,
            self._safety_margin * 100,
        )

    @property
    def budget_source(self) -> str:
        """Human-readable description of how the budget was resolved."""
        return self._budget_source

    @property
    def total_budget(self) -> int:
        """Total budget before safety margin."""
        return self._total_budget

    @property
    def effective_budget(self) -> int:
        """Effective budget after safety margin subtraction."""
        return self._effective_budget

    @property
    def consumed(self) -> int:
        """Total tokens consumed so far."""
        return self._consumed

    @property
    def remaining(self) -> int:
        """Tokens remaining in the effective budget."""
        return max(0, self._effective_budget - self._consumed)

    @property
    def chars_per_token(self) -> float:
        """Characters-per-token ratio used for estimation."""
        return self._chars_per_token

    def can_accommodate(self, tokens: int) -> bool:
        """Check if the budget can accommodate additional tokens.

        Args:
            tokens: Number of tokens to check.

        Returns:
            True if tokens fit within remaining budget.
        """
        return (self._consumed + tokens) <= self._effective_budget

    def record_consumption(self, tokens: int) -> None:
        """Record token consumption.

        Args:
            tokens: Number of tokens consumed.
        """
        self._consumed += tokens

    def estimate_and_check(self, text: str) -> tuple[int, bool]:
        """Estimate tokens for text and check if it fits.

        Args:
            text: Text to estimate.

        Returns:
            Tuple of (estimated_tokens, fits_in_budget).
        """
        tokens = estimate_tokens(text, self._chars_per_token)
        return tokens, self.can_accommodate(tokens)


def allocate_budget_by_priority(
    budget: TokenBudget,
    items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Allocate budget across items by priority tier.

    Priority tiers (FR-005):
    1. Diff hunks (changed regions) — always included
    2. Unchanged regions of changed files (full_content)
    3. Related test files
    4. Imported modules
    5. Config/docs files

    Items are expected to have ``priority`` (int 1-5) and ``content`` (str) fields.
    Returns items with an ``allocated`` boolean field added.

    Args:
        budget: The token budget to allocate from.
        items: List of content items with priority and content fields.

    Returns:
        Items with ``allocated`` and ``estimated_tokens`` fields added.
    """
    # Sort by priority (lower = higher priority)
    sorted_items = sorted(items, key=lambda x: x.get("priority", 5))

    result = []
    for item in sorted_items:
        content = item.get("content", "")
        tokens = estimate_tokens(content, budget.chars_per_token)
        allocated = budget.can_accommodate(tokens)
        if allocated:
            budget.record_consumption(tokens)
        result.append({**item, "allocated": allocated, "estimated_tokens": tokens})

    return result
