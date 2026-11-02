"""Tests for TokenBudget class."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.review.budget import (
    FALLBACK_BUDGET_TOKENS,
    TokenBudget,
)


class TestTokenBudgetConstruction:
    """Tests for TokenBudget initialization."""

    def test_explicit_budget(self) -> None:
        """Explicit budget_tokens is used directly."""
        budget = TokenBudget(budget_tokens=50000)
        assert budget.total_budget == 50000
        assert budget.budget_source == "explicit"

    def test_model_derived_budget(self) -> None:
        """Budget derived from model context window (60%)."""
        budget = TokenBudget(model_id="gpt-4o")
        # gpt-4o has 128000 context window, 60% = 76800
        assert budget.total_budget == 76800
        assert "model-derived" in budget.budget_source

    def test_fallback_budget(self) -> None:
        """Fallback to hardcoded default when no explicit or model."""
        budget = TokenBudget()
        assert budget.total_budget == FALLBACK_BUDGET_TOKENS
        assert budget.budget_source == "fallback"

    def test_unknown_model_uses_fallback(self) -> None:
        """Unknown model ID falls back to hardcoded default."""
        budget = TokenBudget(model_id="unknown-model-xyz")
        assert budget.total_budget == FALLBACK_BUDGET_TOKENS

    def test_safety_margin_applied(self) -> None:
        """10% safety margin reduces effective budget."""
        budget = TokenBudget(budget_tokens=100000, safety_margin=0.10)
        assert budget.effective_budget == 90000

    def test_invalid_safety_margin_raises(self) -> None:
        """Invalid safety margin raises ValueError."""
        with pytest.raises(ValueError):
            TokenBudget(safety_margin=-0.1)
        with pytest.raises(ValueError):
            TokenBudget(safety_margin=1.0)


class TestTokenBudgetConsumption:
    """Tests for budget consumption tracking."""

    def test_can_accommodate_within_budget(self) -> None:
        budget = TokenBudget(budget_tokens=1000, safety_margin=0.0)
        assert budget.can_accommodate(500) is True

    def test_can_accommodate_exceeds_budget(self) -> None:
        budget = TokenBudget(budget_tokens=1000, safety_margin=0.0)
        assert budget.can_accommodate(1001) is False

    def test_record_consumption_updates_remaining(self) -> None:
        budget = TokenBudget(budget_tokens=1000, safety_margin=0.0)
        budget.record_consumption(400)
        assert budget.consumed == 400
        assert budget.remaining == 600

    def test_estimate_and_check(self) -> None:
        budget = TokenBudget(budget_tokens=100, safety_margin=0.0)
        tokens, fits = budget.estimate_and_check("x" * 350)  # ~100 tokens
        assert tokens == 100
        assert fits is True


class TestTokenBudgetValidation:
    """Tests for TokenBudget parameter validation."""

    def test_invalid_chars_per_token(self) -> None:
        """chars_per_token <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="chars_per_token"):
            TokenBudget(budget_tokens=1000, chars_per_token=0)

    def test_invalid_budget_token_type_raises(self) -> None:
        """Non-numeric budget_tokens raises ValueError."""
        with pytest.raises(ValueError, match="budget_tokens"):
            TokenBudget(budget_tokens="abc")  # type: ignore[arg-type]

    def test_non_positive_budget_tokens_raise(self) -> None:
        """Explicit non-positive budget_tokens raises ValueError."""
        with pytest.raises(ValueError, match="budget_tokens"):
            TokenBudget(budget_tokens=0)
        with pytest.raises(ValueError, match="budget_tokens"):
            TokenBudget(budget_tokens=-1)
