# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for ModelRoutingDecision — OMN-8038."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.model_routing_decision import (
    EnumCapabilityTier,
    EnumProvider,
    EnumRetryType,
    EnumRiskLevel,
    ModelRoutingDecision,
)


def _make_decision(**kwargs: Any) -> ModelRoutingDecision:
    defaults: dict[str, Any] = {
        "selected_model": "qwen3-coder-30b",
        "capability_tier": EnumCapabilityTier.LOCAL,
        "provider": EnumProvider.LOCAL_VLLM,
    }
    defaults.update(kwargs)
    return ModelRoutingDecision(**defaults)


def test_routing_decision_requires_selected_model() -> None:
    with pytest.raises(ValidationError):
        ModelRoutingDecision(  # type: ignore[call-arg]
            capability_tier=EnumCapabilityTier.LOCAL,
            provider=EnumProvider.LOCAL_VLLM,
        )


def test_routing_decision_retry_budget_non_negative() -> None:
    with pytest.raises(ValidationError):
        _make_decision(retry_budget=-1)


def test_routing_decision_frozen() -> None:
    decision = _make_decision()
    with pytest.raises(ValidationError):
        decision.selected_model = "other-model"


def test_routing_decision_defaults() -> None:
    decision = _make_decision()
    assert decision.retry_type == EnumRetryType.NONE
    assert decision.fallback_model is None
    assert decision.risk_level == EnumRiskLevel.LOW
    assert decision.retry_budget == 0
    assert decision.rationale == ""
    assert decision.exploration_score is None
    assert decision.cost_estimate_usd is None


def test_routing_decision_full_fields() -> None:
    decision = _make_decision(
        capability_tier=EnumCapabilityTier.CHEAP_FRONTIER,
        provider=EnumProvider.ANTHROPIC,
        retry_type=EnumRetryType.FALLBACK_MODEL,
        fallback_model="claude-haiku-4-5",
        risk_level=EnumRiskLevel.HIGH,
        retry_budget=2,
        rationale="primary exhausted",
        exploration_score=0.3,
        cost_estimate_usd=0.001,
    )
    assert decision.capability_tier == EnumCapabilityTier.CHEAP_FRONTIER
    assert decision.provider == EnumProvider.ANTHROPIC
    assert decision.retry_type == EnumRetryType.FALLBACK_MODEL
    assert decision.fallback_model == "claude-haiku-4-5"
    assert decision.risk_level == EnumRiskLevel.HIGH
    assert decision.retry_budget == 2
    assert decision.exploration_score == 0.3
    assert decision.cost_estimate_usd == 0.001


def test_routing_decision_exploration_score_bounds() -> None:
    with pytest.raises(ValidationError):
        _make_decision(exploration_score=1.5)
    with pytest.raises(ValidationError):
        _make_decision(exploration_score=-0.1)


def test_routing_decision_cost_estimate_non_negative() -> None:
    with pytest.raises(ValidationError):
        _make_decision(cost_estimate_usd=-0.001)


def test_routing_decision_extra_fields_forbidden() -> None:
    with pytest.raises(ValidationError):
        _make_decision(unknown_field="oops")


def test_fallback_model_required_when_retry_type_fallback_model() -> None:
    with pytest.raises(ValidationError, match="fallback_model is required"):
        _make_decision(retry_type=EnumRetryType.FALLBACK_MODEL, fallback_model=None)


def test_fallback_model_must_be_none_unless_fallback_retry_type() -> None:
    with pytest.raises(ValidationError, match="fallback_model must be None"):
        _make_decision(retry_type=EnumRetryType.NONE, fallback_model="some-model")


def test_fallback_model_valid_when_retry_type_fallback_model() -> None:
    decision = _make_decision(
        retry_type=EnumRetryType.FALLBACK_MODEL, fallback_model="claude-haiku-4-5"
    )
    assert decision.fallback_model == "claude-haiku-4-5"


def test_fallback_model_none_valid_for_non_fallback_retry_types() -> None:
    for retry_type in (EnumRetryType.NONE, EnumRetryType.SAME_MODEL, EnumRetryType.ESCALATE_TIER):
        decision = _make_decision(retry_type=retry_type, fallback_model=None)
        assert decision.fallback_model is None
