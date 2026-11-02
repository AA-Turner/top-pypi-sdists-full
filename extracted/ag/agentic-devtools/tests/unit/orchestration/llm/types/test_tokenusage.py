"""Tests for TokenUsage dataclass."""

from agentic_devtools.orchestration.llm.types import TokenUsage


class TestTokenUsage:
    """Tests for TokenUsage."""

    def test_basic_creation(self):
        usage = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        assert usage.input_tokens == 100
        assert usage.output_tokens == 50
        assert usage.total_tokens == 150
        assert usage.estimated_cost_usd is None

    def test_with_cost(self):
        usage = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150, estimated_cost_usd=0.005)
        assert usage.estimated_cost_usd == 0.005

    def test_frozen(self):
        usage = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        try:
            usage.input_tokens = 200  # type: ignore[misc]
            assert False, "Should have raised"
        except AttributeError:
            pass

    def test_equality(self):
        u1 = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        u2 = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        assert u1 == u2

    def test_inequality(self):
        u1 = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        u2 = TokenUsage(input_tokens=200, output_tokens=50, total_tokens=250)
        assert u1 != u2
