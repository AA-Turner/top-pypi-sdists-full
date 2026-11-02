"""Tests for ``calculate_modelled_session_cost``."""

import json

import pytest

from agentic_devtools.cli.config.project_config import calculate_modelled_session_cost


class TestCalculateModelledSessionCost:
    """Tests for exact-decimal session cost calculation."""

    def test_canonical_example_produces_exact_string(self):
        cost = calculate_modelled_session_cost(3, 15, 100_000, 10_000)
        assert cost == "0.45"

    def test_result_is_json_safe(self):
        cost = calculate_modelled_session_cost(3, 15, 100_000, 10_000)
        assert json.loads(json.dumps({"cost": cost}))["cost"] == "0.45"

    def test_zero_rates_produce_zero_cost(self):
        cost = calculate_modelled_session_cost(0, 0, 100_000, 10_000)
        assert cost == "0"

    def test_string_inputs_are_accepted(self):
        cost = calculate_modelled_session_cost("3", "15", "100000", "10000")
        assert cost == "0.45"

    def test_nan_rate_raises(self):
        with pytest.raises(ValueError, match="must be finite"):
            calculate_modelled_session_cost(float("nan"), 15, 100_000, 10_000)

    def test_non_numeric_rate_raises(self):
        with pytest.raises(ValueError, match="must be numeric"):
            calculate_modelled_session_cost(object(), 15, 100_000, 10_000)

    def test_negative_input_rate_raises(self):
        with pytest.raises(ValueError, match="inputRatePerM must be non-negative"):
            calculate_modelled_session_cost(-1, 15, 100_000, 10_000)

    def test_negative_output_rate_raises(self):
        with pytest.raises(ValueError, match="outputRatePerM must be non-negative"):
            calculate_modelled_session_cost(3, -1, 100_000, 10_000)

    def test_negative_input_tokens_raises(self):
        with pytest.raises(ValueError, match="assumedInputTokens must be a non-negative integer"):
            calculate_modelled_session_cost(3, 15, -1, 10_000)

    def test_negative_output_tokens_raises(self):
        with pytest.raises(ValueError, match="assumedOutputTokens must be a non-negative integer"):
            calculate_modelled_session_cost(3, 15, 100_000, -1)

    def test_fractional_input_tokens_raises(self):
        with pytest.raises(ValueError, match="assumedInputTokens must be a non-negative integer"):
            calculate_modelled_session_cost(3, 15, 100_000.5, 10_000)

    def test_fractional_output_tokens_raises(self):
        with pytest.raises(ValueError, match="assumedOutputTokens must be a non-negative integer"):
            calculate_modelled_session_cost(3, 15, 100_000, 10_000.5)
