"""Cost estimation based on model pricing tables."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from agentic_devtools.orchestration.llm.types import TokenUsage

# Default pricing per 1M tokens (USD)
DEFAULT_PRICING: dict[str, dict[str, float]] = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
}


@dataclass(frozen=True)
class PricingTable:
    """Model pricing configuration.

    Prices are per 1 million tokens in USD.
    """

    prices: Mapping[str, Mapping[str, float]] = field(
        default_factory=lambda: {k: dict(v) for k, v in DEFAULT_PRICING.items()}
    )

    def __post_init__(self) -> None:
        # Fully freeze the nested mappings so neither direct access nor get_price()
        # callers can mutate future cost estimates, consistent with frozen=True intent.
        frozen = MappingProxyType({k: MappingProxyType(dict(v)) for k, v in self.prices.items()})
        object.__setattr__(self, "prices", frozen)

    def get_price(self, model: str) -> Mapping[str, float] | None:
        """Get pricing for a model. Returns None if unknown."""
        # Try exact match first
        if model in self.prices:
            return self.prices[model]
        # Try prefix match (e.g., "gpt-4o-2024-05-13" matches "gpt-4o").
        # Sort by length descending to prefer the most-specific (longest) prefix,
        # so "gpt-4o-..." matches "gpt-4o" rather than the shorter "gpt-4".
        for key in sorted(self.prices, key=len, reverse=True):
            if model.startswith(key):
                return self.prices[key]
        return None


class CostEstimator:
    """Estimates cost of LLM calls based on token usage and pricing."""

    def __init__(self, pricing: PricingTable | None = None) -> None:
        self._pricing = pricing or PricingTable()

    @property
    def pricing(self) -> PricingTable:
        """Return the pricing table."""
        return self._pricing

    def estimate_cost(self, model: str, usage: TokenUsage) -> float | None:
        """Estimate cost for a single call.

        Args:
            model: Model identifier.
            usage: Token usage from the call.

        Returns:
            Estimated cost in USD, or None if model pricing unknown.
        """
        price = self._pricing.get_price(model)
        if price is None:
            return None
        if "input" not in price or "output" not in price:
            raise ValueError(f"Pricing for model {model!r} must define both 'input' and 'output' prices")

        input_cost = (usage.input_tokens / 1_000_000) * price["input"]
        output_cost = (usage.output_tokens / 1_000_000) * price["output"]
        return input_cost + output_cost

    def enrich_usage(self, model: str, usage: TokenUsage) -> TokenUsage:
        """Return a new TokenUsage with estimated cost filled in.

        Args:
            model: Model identifier.
            usage: Token usage without cost.

        Returns:
            New TokenUsage with estimated_cost_usd set.
        """
        cost = self.estimate_cost(model, usage)
        return TokenUsage(
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            total_tokens=usage.total_tokens,
            estimated_cost_usd=cost,
        )


def estimate_cost(model: str, usage: TokenUsage) -> float | None:
    """Convenience function to estimate cost for a single call."""
    estimator = CostEstimator()
    return estimator.estimate_cost(model, usage)
