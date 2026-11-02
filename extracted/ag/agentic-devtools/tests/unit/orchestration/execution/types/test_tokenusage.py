"""Tests for TokenUsage dataclass."""

from agentic_devtools.orchestration.execution.types import TokenUsage


class TestTokenUsage:
    def test_construction_required_fields(self) -> None:
        usage = TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
        assert usage.prompt_tokens == 10
        assert usage.completion_tokens == 20
        assert usage.total_tokens == 30

    def test_estimated_cost_defaults_none(self) -> None:
        usage = TokenUsage(prompt_tokens=1, completion_tokens=2, total_tokens=3)
        assert usage.estimated_cost_usd is None

    def test_estimated_cost_set(self) -> None:
        usage = TokenUsage(
            prompt_tokens=100,
            completion_tokens=200,
            total_tokens=300,
            estimated_cost_usd=0.005,
        )
        assert usage.estimated_cost_usd == 0.005

    def test_is_frozen(self) -> None:
        usage = TokenUsage(prompt_tokens=1, completion_tokens=2, total_tokens=3)
        try:
            usage.prompt_tokens = 999  # type: ignore[misc]
            raise AssertionError("Expected FrozenInstanceError")
        except AttributeError:
            pass
