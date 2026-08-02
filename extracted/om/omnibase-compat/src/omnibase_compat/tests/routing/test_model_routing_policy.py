# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for ModelRoutingPolicy and ModelRoutingDegradedEvent contract models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from omnibase_compat.routing.model_routing_degraded_event import ModelRoutingDegradedEvent
from omnibase_compat.routing.model_routing_policy import ModelCiOverridePolicy, ModelRoutingPolicy


def test_model_routing_policy_defaults() -> None:
    policy = ModelRoutingPolicy(primary="qwen3-coder-30b")
    assert policy.primary == "qwen3-coder-30b"
    assert policy.fallback is None
    assert policy.timeout_per_attempt_s == 30.0
    assert policy.max_retries == 2
    assert policy.call_style == "async"
    assert policy.ci_override is None
    assert policy.fallback_allowed_roles == []


def test_model_routing_policy_frozen() -> None:
    policy = ModelRoutingPolicy(primary="qwen3-coder-30b")
    with pytest.raises(ValidationError):
        policy.primary = "other-model"


def test_model_routing_policy_extra_field_forbidden() -> None:
    with pytest.raises(ValidationError):
        ModelRoutingPolicy(primary="qwen3-coder-30b", nonexistent_field="bad")  # type: ignore[call-arg]


def test_model_routing_policy_with_fallback_and_ci_override() -> None:
    policy = ModelRoutingPolicy(
        primary="qwen3-coder-30b",
        fallback="claude-sonnet",
        timeout_per_attempt_s=60.0,
        max_retries=3,
        reason_for_fallback="local timeout or unavailable",
        fallback_allowed_roles=["reviewer", "designer", "fixer"],
        max_tokens=8192,
        temperature=0.1,
        call_style="async",
        ci_override=ModelCiOverridePolicy(primary="claude-sonnet"),
    )
    assert policy.fallback == "claude-sonnet"
    assert policy.timeout_per_attempt_s == 60.0
    assert "fixer" in policy.fallback_allowed_roles
    assert policy.ci_override is not None
    assert policy.ci_override.primary == "claude-sonnet"


def test_model_routing_policy_timeout_math() -> None:
    """Total budget must always be timeout_per_attempt_s * max_retries, never total/retries."""
    policy = ModelRoutingPolicy(
        primary="qwen3-coder-30b", timeout_per_attempt_s=60.0, max_retries=3
    )
    total_budget = policy.timeout_per_attempt_s * policy.max_retries
    assert total_budget == 180.0


def test_model_routing_policy_fallback_required_when_roles_declared() -> None:
    """fallback must be set when fallback_allowed_roles is non-empty."""
    with pytest.raises(ValidationError, match="fallback must be set"):
        ModelRoutingPolicy(
            primary="qwen3-coder-30b",
            fallback_allowed_roles=["fixer"],
        )


def test_model_routing_degraded_event_required_fields() -> None:
    event = ModelRoutingDegradedEvent(
        primary="qwen3-coder-30b",
        reason="3 consecutive health check failures",
        attempts=3,
        elapsed_ms=1500.0,
        model_key="qwen3-coder-30b",
        correlation_id="test-corr-id",
    )
    assert event.primary == "qwen3-coder-30b"
    assert event.attempts == 3
    assert event.correlation_id == "test-corr-id"


def test_model_routing_degraded_event_frozen() -> None:
    event = ModelRoutingDegradedEvent(
        primary="qwen3-coder-30b",
        reason="test",
        attempts=1,
        elapsed_ms=0.0,
        model_key="qwen3-coder-30b",
        correlation_id="x",
    )
    with pytest.raises(ValidationError):
        event.primary = "changed"
