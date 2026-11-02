"""Tests for CostEstimator."""

import pytest

from agentic_devtools.orchestration.llm.cost_estimator import CostEstimator, PricingTable, estimate_cost
from agentic_devtools.orchestration.llm.types import TokenUsage


class TestCostEstimator:
    """Tests for CostEstimator."""

    def test_estimate_known_model(self):
        estimator = CostEstimator()
        usage = TokenUsage(input_tokens=1_000_000, output_tokens=500_000, total_tokens=1_500_000)
        cost = estimator.estimate_cost("gpt-4o", usage)
        assert cost is not None
        # gpt-4o: $2.50/1M input + $10.00/1M output
        expected = 2.50 + 5.00
        assert abs(cost - expected) < 0.01

    def test_estimate_unknown_model_returns_none(self):
        estimator = CostEstimator()
        usage = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        cost = estimator.estimate_cost("unknown-model", usage)
        assert cost is None

    def test_longest_prefix_wins_over_shorter_prefix(self):
        """When two keys are both prefixes, the longest one should be matched."""
        pricing = PricingTable(
            prices={
                "gpt-4": {"input": 30.00, "output": 60.00},
                "gpt-4o": {"input": 2.50, "output": 10.00},
            }
        )
        estimator = CostEstimator(pricing=pricing)
        usage = TokenUsage(input_tokens=1_000_000, output_tokens=0, total_tokens=1_000_000)
        # "gpt-4o-2024-05-13" starts with both "gpt-4" and "gpt-4o";
        # the longer prefix "gpt-4o" must win regardless of insertion order.
        cost = estimator.estimate_cost("gpt-4o-2024-05-13", usage)
        assert cost is not None
        # gpt-4o input price: $2.50/1M  →  $2.50 for 1M tokens
        assert abs(cost - 2.50) < 0.01

    def test_longest_prefix_with_shorter_first_in_dict(self):
        """Shorter prefix listed first in dict must not shadow a longer match."""
        pricing = PricingTable(
            prices={
                "gpt-4": {"input": 30.00, "output": 60.00},
                "gpt-4o": {"input": 2.50, "output": 10.00},
            }
        )
        estimator = CostEstimator(pricing=pricing)
        usage = TokenUsage(input_tokens=1_000_000, output_tokens=0, total_tokens=1_000_000)
        cost = estimator.estimate_cost("gpt-4-turbo-2024-04-09", usage)
        assert cost is not None
        # "gpt-4-turbo-..." starts with "gpt-4" only (not "gpt-4o"), so matches "gpt-4"
        assert abs(cost - 30.00) < 0.01

    def test_enrich_usage_adds_cost(self):
        estimator = CostEstimator()
        usage = TokenUsage(input_tokens=1000, output_tokens=500, total_tokens=1500)
        enriched = estimator.enrich_usage("gpt-4o", usage)
        assert enriched.estimated_cost_usd is not None
        assert enriched.input_tokens == 1000

    def test_custom_pricing_table(self):
        pricing = PricingTable(prices={"custom-model": {"input": 1.0, "output": 2.0}})
        estimator = CostEstimator(pricing=pricing)
        usage = TokenUsage(input_tokens=1_000_000, output_tokens=1_000_000, total_tokens=2_000_000)
        cost = estimator.estimate_cost("custom-model", usage)
        assert cost is not None
        assert abs(cost - 3.0) < 0.01

    def test_missing_output_price_raises_clear_error(self):
        pricing = PricingTable(prices={"custom-model": {"input": 1.0}})
        estimator = CostEstimator(pricing=pricing)
        usage = TokenUsage(input_tokens=1_000_000, output_tokens=1_000_000, total_tokens=2_000_000)

        with pytest.raises(ValueError, match="must define both 'input' and 'output' prices"):
            estimator.estimate_cost("custom-model", usage)

    def test_pricing_property(self):
        pricing = PricingTable(prices={"test": {"input": 1.0, "output": 2.0}})
        estimator = CostEstimator(pricing=pricing)
        assert estimator.pricing is pricing


class TestEstimateCost:
    """Tests for estimate_cost convenience function."""

    def test_returns_float(self):
        usage = TokenUsage(input_tokens=1000, output_tokens=500, total_tokens=1500)
        cost = estimate_cost("gpt-4o", usage)
        assert isinstance(cost, float)

    def test_unknown_returns_none(self):
        usage = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        assert estimate_cost("nonexistent", usage) is None


class TestPricingTableIsolation:
    """Tests that PricingTable nested mappings are fully immutable."""

    def test_prices_outer_mapping_is_immutable(self):
        """The outer prices mapping must not accept new keys."""
        table = PricingTable()
        with pytest.raises(TypeError):
            table.prices["new-model"] = {"input": 1.0, "output": 2.0}  # type: ignore[index]

    def test_prices_inner_mapping_is_immutable_via_direct_access(self):
        """The inner mapping must not be mutable via direct attribute access."""
        table = PricingTable()
        with pytest.raises(TypeError):
            table.prices["gpt-4o"]["input"] = 999.0  # type: ignore[index]

    def test_get_price_returns_immutable_mapping(self):
        """The mapping returned by get_price() must not be mutable."""
        table = PricingTable()
        price = table.get_price("gpt-4o")
        assert price is not None
        with pytest.raises(TypeError):
            price["input"] = 999.0  # type: ignore[index]

    def test_two_instances_have_independent_prices(self):
        """Two default PricingTable instances must have the same prices."""
        table1 = PricingTable()
        table2 = PricingTable()
        assert table1.prices["gpt-4o"]["input"] == table2.prices["gpt-4o"]["input"]
