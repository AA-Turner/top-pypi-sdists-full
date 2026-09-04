# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for the strict OMN-17013 v2 delegation terminal transport."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

import pytest
from pydantic import TypeAdapter, ValidationError

from omnibase_compat.contracts.delegation.terminal_v2 import (
    EnumDelegationRoutingDisposition,
    EnumDelegationTerminalFailureCause,
    EnumDelegationTerminalOutcome,
    EnumDelegationUnroutedReason,
    EnumQualityScoreComparison,
    ModelDelegationTerminalRoutedV2,
    ModelDelegationTerminalTransportV2,
)


def _common_payload() -> dict[str, Any]:
    return {
        "correlation_id": str(uuid4()),
        "task_type": "code_review",
        "model_used": "qwen3-coder",
        "endpoint_url": "https://diagnostic.example/v1",
        "content": "review complete",
        "quality_passed": True,
        "quality_score": 0.95,
        "required_quality_bar": 0.9,
        "score_vs_required_bar": EnumQualityScoreComparison.AT_OR_ABOVE_BAR.value,
        "failed_acceptance_criteria": [],
        "latency_ms": 42,
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "total_tokens": 30,
        "fallback_to_claude": False,
        "failure_reason": "",
        "tokens_to_compliance": 30,
        "compliance_attempts": 1,
        "escalation_count": 0,
        "escalation_history": [],
        "terminal_failure_reason": None,
        "terminal_failure_cause": None,
        "routing_tiers_hash": None,
        "escalation_config_hash": None,
        "attempts_count": 1,
        "cumulative_attempt_cost": 0.01,
        "cumulative_input_tokens": 10,
        "cumulative_output_tokens": 20,
        "final_attempt_cost": 0.01,
        "context_pack_hash": "",
        "cost_tier_name": "local",
        "tenant_id": None,
    }


def _routed_payload() -> dict[str, Any]:
    return {
        **_common_payload(),
        "routing_disposition": EnumDelegationRoutingDisposition.ROUTED.value,
        "terminal_outcome": EnumDelegationTerminalOutcome.COMPLETED.value,
        "backend_ref": "local-coder",
        "pricing_manifest_version": 7,
    }


def _unrouted_payload() -> dict[str, Any]:
    return {
        **_common_payload(),
        "routing_disposition": EnumDelegationRoutingDisposition.UNROUTED.value,
        "terminal_outcome": EnumDelegationTerminalOutcome.FAILED.value,
        "quality_passed": False,
        "quality_score": 0.0,
        "required_quality_bar": None,
        "score_vs_required_bar": None,
        "failure_reason": "no backend matched the route",
        "unrouted_reason": EnumDelegationUnroutedReason.NO_ELIGIBLE_BACKEND.value,
    }


def test_routed_terminal_round_trips_through_discriminated_transport() -> None:
    adapter = TypeAdapter(ModelDelegationTerminalTransportV2)
    terminal = adapter.validate_python(_routed_payload())

    restored = adapter.validate_json(terminal.model_dump_json())

    assert isinstance(restored, ModelDelegationTerminalRoutedV2)
    assert restored.backend_ref == "local-coder"
    assert restored.pricing_manifest_version == 7
    assert restored.routing_disposition is EnumDelegationRoutingDisposition.ROUTED


def test_transport_schema_exposes_closed_routing_discriminator() -> None:
    schema = TypeAdapter(ModelDelegationTerminalTransportV2).json_schema()

    discriminator = schema["discriminator"]
    assert discriminator["propertyName"] == "routing_disposition"
    assert set(discriminator["mapping"]) == {"routed", "unrouted"}
    assert "route_disposition" not in str(schema)


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("backend_ref", "   ", "nonblank"),
        ("backend_ref", "https://backend.example/v1", "not a URL"),
        ("backend_ref", "//backend.example", "not a URL"),
        ("backend_ref", "mailto:ops@example.com", "not a URL"),
        ("backend_ref", "backend.example:8443", "not a URL"),
        ("pricing_manifest_version", 0, "greater than 0"),
    ],
)
def test_routed_terminal_rejects_unstable_or_missing_provenance(
    field: str, value: object, match: str
) -> None:
    payload = _routed_payload()
    payload[field] = value

    with pytest.raises(ValidationError, match=match):
        ModelDelegationTerminalRoutedV2.model_validate(payload)


def test_backend_ref_is_not_derived_from_diagnostic_fields() -> None:
    payload = _routed_payload()
    del payload["backend_ref"]

    with pytest.raises(ValidationError, match="backend_ref"):
        ModelDelegationTerminalRoutedV2.model_validate(payload)


def test_unrouted_terminal_rejects_backend_and_manifest_fields() -> None:
    payload = _unrouted_payload()
    payload["backend_ref"] = "local-coder"
    payload["pricing_manifest_version"] = 7

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        TypeAdapter(ModelDelegationTerminalTransportV2).validate_python(payload)


def test_unrouted_terminal_requires_failed_outcome_and_closed_reason() -> None:
    completed = _unrouted_payload()
    completed["terminal_outcome"] = EnumDelegationTerminalOutcome.COMPLETED.value
    bad_reason = _unrouted_payload()
    bad_reason["unrouted_reason"] = "legacy"
    adapter = TypeAdapter(ModelDelegationTerminalTransportV2)

    with pytest.raises(ValidationError):
        adapter.validate_python(completed)
    with pytest.raises(ValidationError, match="unrouted_reason"):
        adapter.validate_python(bad_reason)


def test_completed_terminal_must_be_quality_accepted() -> None:
    payload = _routed_payload()
    payload["quality_passed"] = False
    payload["required_quality_bar"] = None
    payload["score_vs_required_bar"] = None

    with pytest.raises(ValidationError, match="requires quality_passed=true"):
        ModelDelegationTerminalRoutedV2.model_validate(payload)


def test_common_terminal_fields_have_no_defaults() -> None:
    required_fields = ModelDelegationTerminalRoutedV2.model_fields

    assert all(field.is_required() for field in required_fields.values())


def test_failure_cause_vocabulary_mirrors_existing_terminal_taxonomy() -> None:
    assert {member.value for member in EnumDelegationTerminalFailureCause} == {
        "provider_quota_exhausted",
        "auth_failed",
        "provider_error",
    }
