"""Tests for UsageTracker."""

from agentic_devtools.orchestration.llm.types import TokenUsage
from agentic_devtools.orchestration.llm.usage_tracker import AggregateUsage, UsageTracker


class TestUsageTracker:
    """Tests for UsageTracker."""

    def test_initial_state_empty(self):
        tracker = UsageTracker()
        assert tracker.aggregate.total_calls == 0
        assert tracker.aggregate.total_tokens == 0
        assert tracker.calls == []

    def test_record_single_call(self):
        tracker = UsageTracker()
        usage = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        tracker.record(usage)
        assert tracker.aggregate.total_calls == 1
        assert tracker.aggregate.total_input_tokens == 100
        assert tracker.aggregate.total_output_tokens == 50
        assert tracker.aggregate.total_tokens == 150

    def test_record_multiple_calls(self):
        tracker = UsageTracker()
        tracker.record(TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150))
        tracker.record(TokenUsage(input_tokens=200, output_tokens=100, total_tokens=300))
        assert tracker.aggregate.total_calls == 2
        assert tracker.aggregate.total_tokens == 450

    def test_record_none_uses_zero_fill(self):
        tracker = UsageTracker()
        tracker.record(None)
        assert tracker.aggregate.total_calls == 1
        assert tracker.aggregate.total_tokens == 0

    def test_record_with_cost(self):
        tracker = UsageTracker()
        usage = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150, estimated_cost_usd=0.005)
        tracker.record(usage)
        assert tracker.aggregate.total_cost_usd == 0.005

    def test_reset_clears_all(self):
        tracker = UsageTracker()
        tracker.record(TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150))
        tracker.reset()
        assert tracker.aggregate.total_calls == 0
        assert tracker.calls == []


class TestAggregateUsage:
    """Tests for AggregateUsage."""

    def test_add_accumulates(self):
        agg = AggregateUsage()
        agg.add(TokenUsage(input_tokens=10, output_tokens=5, total_tokens=15))
        agg.add(TokenUsage(input_tokens=20, output_tokens=10, total_tokens=30))
        assert agg.total_input_tokens == 30
        assert agg.total_output_tokens == 15
        assert agg.total_tokens == 45
        assert agg.total_calls == 2
