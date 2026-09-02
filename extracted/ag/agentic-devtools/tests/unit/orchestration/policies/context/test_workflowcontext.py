"""Tests for WorkflowContext dataclass."""

from __future__ import annotations

from agentic_devtools.orchestration.policies.context import WorkflowContext


class TestWorkflowContext:
    """Test WorkflowContext field preservation."""

    def test_default_construction(self) -> None:
        ctx = WorkflowContext()
        assert ctx.tokens_consumed is None
        assert ctx.elapsed_minutes == 0.0
        assert ctx.retry_counts == {}
        assert ctx.step_history == []
        assert ctx.recent_outcomes == []

    def test_custom_values(self) -> None:
        ctx = WorkflowContext(
            tokens_consumed=100000,
            elapsed_minutes=25.5,
            retry_counts={"implementation": 2},
            step_history=[{"step": "planning", "entered_at": "2024-01-01T00:00:00Z"}],
            recent_outcomes=["pass", "fail"],
        )
        assert ctx.tokens_consumed == 100000
        assert ctx.elapsed_minutes == 25.5
        assert ctx.retry_counts == {"implementation": 2}
        assert len(ctx.step_history) == 1
        assert ctx.step_history[0]["step"] == "planning"
        assert ctx.recent_outcomes == ["pass", "fail"]

    def test_tokens_consumed_none(self) -> None:
        ctx = WorkflowContext(tokens_consumed=None)
        assert ctx.tokens_consumed is None

    def test_mutable_fields_are_independent(self) -> None:
        ctx1 = WorkflowContext()
        ctx2 = WorkflowContext()
        ctx1.retry_counts["test"] = 1
        assert ctx2.retry_counts == {}
