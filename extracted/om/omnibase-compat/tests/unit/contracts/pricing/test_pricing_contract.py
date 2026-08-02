# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.contracts.pricing.model_llm_pricing import ModelLlmPricing
from omnibase_compat.contracts.pricing.model_pricing_contract import ModelPricingContract


@pytest.mark.unit
def test_pricing_contract_parses() -> None:
    pricing = ModelPricingContract(
        name="delegation-pricing-v1",
        version=1,
        baseline_model="claude-sonnet-4-6",
        savings_method="counterfactual",
        models={
            "qwen3-coder": ModelLlmPricing(
                input_cost_per_1k_tokens=0.0,
                output_cost_per_1k_tokens=0.0,
                runner_cost_per_hour=0.15,
            ),
            "claude-sonnet-4-6": ModelLlmPricing(
                input_cost_per_1k_tokens=0.003,
                output_cost_per_1k_tokens=0.015,
                runner_cost_per_hour=0.0,
            ),
        },
    )
    assert pricing.version == 1
    assert pricing.models["qwen3-coder"].input_cost_per_1k_tokens == 0.0
    assert pricing.models["claude-sonnet-4-6"].output_cost_per_1k_tokens == 0.015


@pytest.mark.unit
def test_savings_method_must_be_declared() -> None:
    with pytest.raises(ValueError):
        ModelPricingContract(
            name="test",
            version=1,
            baseline_model="claude-sonnet-4-6",
            savings_method="",
            models={},
        )


@pytest.mark.unit
def test_frozen_immutability() -> None:
    pricing = ModelPricingContract(
        name="test",
        version=1,
        baseline_model="claude-sonnet-4-6",
        savings_method="counterfactual",
        models={},
    )
    with pytest.raises(ValidationError):
        pricing.version = 2  # type: ignore[misc]


@pytest.mark.unit
def test_models_mapping_is_immutable() -> None:
    pricing = ModelPricingContract(
        name="test",
        version=1,
        baseline_model="claude-sonnet-4-6",
        savings_method="counterfactual",
        models={},
    )
    with pytest.raises(TypeError):
        pricing.models["new_key"] = ModelLlmPricing(  # type: ignore[index]
            input_cost_per_1k_tokens=0.0,
            output_cost_per_1k_tokens=0.0,
        )


@pytest.mark.unit
def test_rejects_negative_costs() -> None:
    with pytest.raises(ValueError):
        ModelLlmPricing(
            input_cost_per_1k_tokens=-0.001,
            output_cost_per_1k_tokens=0.0,
            runner_cost_per_hour=0.0,
        )


@pytest.mark.unit
def test_rejects_negative_output_cost() -> None:
    with pytest.raises(ValueError):
        ModelLlmPricing(
            input_cost_per_1k_tokens=0.0,
            output_cost_per_1k_tokens=-0.01,
            runner_cost_per_hour=0.0,
        )


@pytest.mark.unit
def test_rejects_negative_runner_cost() -> None:
    with pytest.raises(ValueError):
        ModelLlmPricing(
            input_cost_per_1k_tokens=0.0,
            output_cost_per_1k_tokens=0.0,
            runner_cost_per_hour=-0.01,
        )


@pytest.mark.unit
def test_model_pricing_frozen() -> None:
    mp = ModelLlmPricing(
        input_cost_per_1k_tokens=0.001,
        output_cost_per_1k_tokens=0.002,
        runner_cost_per_hour=0.0,
    )
    with pytest.raises(ValidationError):
        mp.input_cost_per_1k_tokens = 99.0  # type: ignore[misc]


@pytest.mark.unit
def test_version_must_be_positive() -> None:
    with pytest.raises(ValueError):
        ModelPricingContract(
            name="test",
            version=0,
            baseline_model="claude-sonnet-4-6",
            savings_method="counterfactual",
            models={},
        )


@pytest.mark.unit
def test_baseline_model_must_be_nonempty() -> None:
    with pytest.raises(ValueError):
        ModelPricingContract(
            name="test",
            version=1,
            baseline_model="",
            savings_method="counterfactual",
            models={},
        )


@pytest.mark.unit
def test_name_must_be_nonempty() -> None:
    with pytest.raises(ValueError):
        ModelPricingContract(
            name="",
            version=1,
            baseline_model="claude-sonnet-4-6",
            savings_method="counterfactual",
            models={},
        )


@pytest.mark.unit
def test_extra_fields_rejected_on_pricing_contract() -> None:
    with pytest.raises(ValueError):
        ModelPricingContract(
            name="test",
            version=1,
            baseline_model="claude-sonnet-4-6",
            savings_method="counterfactual",
            models={},
            unknown_field="oops",  # type: ignore[call-arg]
        )


@pytest.mark.unit
def test_extra_fields_rejected_on_model_pricing() -> None:
    with pytest.raises(ValueError):
        ModelLlmPricing(
            input_cost_per_1k_tokens=0.0,
            output_cost_per_1k_tokens=0.0,
            runner_cost_per_hour=0.0,
            unknown_field="oops",  # type: ignore[call-arg]
        )


@pytest.mark.unit
def test_runner_cost_defaults_to_zero() -> None:
    mp = ModelLlmPricing(
        input_cost_per_1k_tokens=0.003,
        output_cost_per_1k_tokens=0.015,
    )
    assert mp.runner_cost_per_hour == 0.0


@pytest.mark.unit
def test_baseline_model_must_be_in_models_when_nonempty() -> None:
    with pytest.raises(ValueError):
        ModelPricingContract(
            name="test",
            version=1,
            baseline_model="claude-sonnet-4-6",
            savings_method="counterfactual",
            models={
                "qwen3-coder": ModelLlmPricing(
                    input_cost_per_1k_tokens=0.0,
                    output_cost_per_1k_tokens=0.0,
                )
            },
        )


@pytest.mark.unit
def test_models_defaults_to_empty_dict() -> None:
    pricing = ModelPricingContract(
        name="test",
        version=1,
        baseline_model="claude-sonnet-4-6",
        savings_method="counterfactual",
    )
    assert pricing.models == {}
