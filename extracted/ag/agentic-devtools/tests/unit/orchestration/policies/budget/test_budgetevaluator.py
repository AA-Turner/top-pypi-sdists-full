"""Tests for BudgetEvaluator."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.policies.budget import BudgetEvaluator
from agentic_devtools.orchestration.policies.config import (
    PolicyConfig,
    SharedBudgetPolicy,
    WorkOnIssuePolicy,
)
from agentic_devtools.orchestration.policies.context import WorkflowContext
from agentic_devtools.orchestration.policies.types import BudgetDecision


class TestBudgetEvaluatorAcceptance:
    """Acceptance scenarios from User Story 2."""

    def test_token_exceeded_halts(self) -> None:
        """US2 Scenario 1: 520000 > 500000 -> halt."""
        policy = PolicyConfig()
        context = WorkflowContext(tokens_consumed=520000, elapsed_minutes=10.0)
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.halt
        assert "520000" in result.rationale
        assert "500000" in result.rationale
        violations = result.metadata["violations"]
        assert any(v.constraint_name == "token_budget" for v in violations)

    def test_time_exceeded_halts(self) -> None:
        """US2 Scenario 2: 65 minutes > 60 -> halt."""
        policy = PolicyConfig()
        context = WorkflowContext(tokens_consumed=100000, elapsed_minutes=65.0)
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.halt
        assert "65" in result.rationale
        assert "60" in result.rationale
        violations = result.metadata["violations"]
        assert any(v.constraint_name == "time_budget" for v in violations)

    def test_retry_exhausted_halts(self) -> None:
        """US2 Scenario 3: 3/3 retries for 'implementation' -> halt."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(retry_budget=3))
        context = WorkflowContext(
            tokens_consumed=100000,
            elapsed_minutes=10.0,
            retry_counts={"implementation": 4},  # > 3
        )
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.halt
        violations = result.metadata["violations"]
        assert any(v.constraint_name == "retry_budget" for v in violations)

    def test_multiple_violations_reported(self) -> None:
        """US2 Scenario 4: Token AND time exceeded -> both reported."""
        policy = PolicyConfig()
        context = WorkflowContext(tokens_consumed=520000, elapsed_minutes=65.0)
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.halt
        violations = result.metadata["violations"]
        assert len(violations) >= 2
        constraint_names = [v.constraint_name for v in violations]
        assert "token_budget" in constraint_names
        assert "time_budget" in constraint_names

    def test_exact_threshold_continues(self) -> None:
        """US2 Scenario 5: exactly 500000 tokens -> continue (> not >=)."""
        policy = PolicyConfig()
        context = WorkflowContext(tokens_consumed=500000, elapsed_minutes=60.0)
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.continue_


class TestBudgetEvaluatorEdgeCases:
    """Edge case tests."""

    def test_tokens_none_skips_dimension(self) -> None:
        """tokens_consumed=None skips token check with skipped_dimensions."""
        policy = PolicyConfig()
        context = WorkflowContext(tokens_consumed=None, elapsed_minutes=10.0)
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.continue_
        assert "token_budget" in result.metadata["skipped_dimensions"]

    def test_multiple_concurrent_violations(self) -> None:
        """All 3 dimensions violated simultaneously."""
        policy = PolicyConfig(
            shared=SharedBudgetPolicy(max_tokens=100, max_wall_clock_minutes=5),
            work_on_issue=WorkOnIssuePolicy(retry_budget=1),
        )
        context = WorkflowContext(
            tokens_consumed=200,
            elapsed_minutes=10.0,
            retry_counts={"task": 5},
        )
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.halt
        violations = result.metadata["violations"]
        assert len(violations) == 3

    def test_zero_budget_tokens(self) -> None:
        """Zero token budget: any consumption violates."""
        policy = PolicyConfig(shared=SharedBudgetPolicy(max_tokens=0))
        context = WorkflowContext(tokens_consumed=1, elapsed_minutes=0.0)
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.halt

    def test_zero_time_budget(self) -> None:
        """Zero time budget: any elapsed time violates."""
        policy = PolicyConfig(shared=SharedBudgetPolicy(max_wall_clock_minutes=0))
        context = WorkflowContext(tokens_consumed=0, elapsed_minutes=0.1)
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.halt

    def test_all_within_limits_continues(self) -> None:
        policy = PolicyConfig()
        context = WorkflowContext(
            tokens_consumed=100000,
            elapsed_minutes=30.0,
            retry_counts={"task": 1},
        )
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.continue_

    @pytest.mark.parametrize("retry_count", [2, 3])
    def test_retry_at_and_below_budget(self, retry_count: int) -> None:
        """Retry count at budget (3) does not violate (> not >=)."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(retry_budget=3))
        context = WorkflowContext(
            tokens_consumed=100,
            elapsed_minutes=1.0,
            retry_counts={"op": retry_count},
        )
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.continue_

    def test_long_rationale_truncated(self) -> None:
        """Many violations produce a rationale that gets truncated to 500 chars."""
        policy = PolicyConfig(
            shared=SharedBudgetPolicy(max_tokens=0, max_wall_clock_minutes=0),
            work_on_issue=WorkOnIssuePolicy(retry_budget=0),
        )
        context = WorkflowContext(
            tokens_consumed=999999999,
            elapsed_minutes=999999.0,
            retry_counts={f"op_{i}": 1 for i in range(50)},
        )
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.halt
        assert len(result.rationale) <= 500

    def test_halt_metadata_uses_immutable_sequences(self) -> None:
        """Halt metadata should not expose mutable list values."""
        policy = PolicyConfig(shared=SharedBudgetPolicy(max_tokens=0))
        context = WorkflowContext(tokens_consumed=1, elapsed_minutes=0.0)
        result = BudgetEvaluator(context, policy)
        assert isinstance(result.metadata["violations"], tuple)
        assert isinstance(result.metadata["skipped_dimensions"], tuple)

    def test_continue_metadata_uses_immutable_sequences(self) -> None:
        """Continue metadata should not expose mutable list values."""
        policy = PolicyConfig()
        context = WorkflowContext(tokens_consumed=None, elapsed_minutes=0.0)
        result = BudgetEvaluator(context, policy)
        assert result.decision == BudgetDecision.continue_
        assert result.metadata["violations"] == ()
        assert result.metadata["skipped_dimensions"] == ("token_budget",)
