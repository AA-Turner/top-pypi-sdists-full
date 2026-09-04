"""Tests for ``resolve_round_assignments``."""

import pytest

from agentic_devtools.orchestration.trio_config import (
    RoleDiversityViolation,
    resolve_round_assignments,
    validate_trio_config,
)
from tests.unit.orchestration.trio_config._samples import availability, canonical_metadata, document, metadata


def test_resolve_round_assignments_uses_ordered_fallbacks_attempts_and_escalation() -> None:
    config = validate_trio_config(document())
    available = metadata(
        "mai-code-1.1-flash",
        "gpt-5.6-luna",
        "claude-sonnet-5",
        "gemini-3.1-pro-preview",
        "claude-opus-5",
        "claude-opus-4.8",
    )
    assignments = resolve_round_assignments(config, phase="standard", available_models=available)
    assert assignments.assignments == {
        "doer": "mai-code-1.1-flash",
        "duckA": "claude-sonnet-5",
        "duckB": "gpt-5.6-luna",
        "adjudicator": "claude-opus-5",
    }
    assert assignments.effective_phase == "standard"
    assert not assignments.escalated
    attempted = {role: [model] for role, model in assignments.items()}
    rotated = resolve_round_assignments(
        config,
        phase="standard",
        available_models=available,
        attempted_models=attempted,
    )
    assert rotated.assignments == {
        "doer": "gpt-5.6-luna",
        "duckA": "gemini-3.1-pro-preview",
        "duckB": "mai-code-1.1-flash",
        "adjudicator": "claude-opus-4.8",
    }

    canonical = canonical_metadata(
        "mai-code-1.1-flash",
        "gpt-5.6-luna",
        "claude-sonnet-5",
        "gemini-3.1-pro-preview",
        "claude-opus-5",
    )
    assert resolve_round_assignments(config, phase="standard", available_models=canonical)["duckA"] == "claude-sonnet-5"
    statuses = availability(
        "mai-code-1.1-flash",
        "gpt-5.6-luna",
        "gemini-3.1-pro-preview",
        "claude-opus-5",
        "claude-opus-4.8",
    )
    assert (
        resolve_round_assignments(
            config,
            phase="standard",
            available_models=canonical,
            availability=statuses,
        )["duckA"]
        == "gemini-3.1-pro-preview"
    )
    partial_config_document = document()
    partial_config_document["roles"]["doer"]["tier"] = "tier-2"
    partial_config_document["roles"]["doer"]["modelPreference"] = "claude-sonnet-5"
    partial_config_document["roles"]["doer"]["fallbackModels"] = ["gemini-3.1-pro-preview"]
    partial_config_document["roles"]["duckA"]["tier"] = "tier-1"
    partial_config_document["roles"]["duckA"]["modelPreference"] = "gpt-5.6-luna"
    partial_config_document["roles"]["duckA"]["fallbackModels"] = ["mai-code-1.1-flash"]
    partial_config_document["roles"]["duckB"]["modelPreference"] = "mai-code-1.1-flash"
    partial_config_document["roles"]["duckB"]["fallbackModels"] = ["gpt-5.6-luna"]
    partial_config = validate_trio_config(partial_config_document)
    partial_available = metadata(
        "mai-code-1.1-flash",
        "gpt-5.6-luna",
        "claude-sonnet-5",
        "gemini-3.1-pro-preview",
        "claude-opus-5",
    )
    partial_statuses: dict[str, object] = {}
    partial_statuses.update(
        availability(
            "gemini-3.1-pro-preview",
            "gpt-5.6-luna",
            "mai-code-1.1-flash",
            "claude-opus-5",
        )
    )
    partial_statuses["claude-sonnet-5"] = {}
    assert (
        resolve_round_assignments(
            partial_config,
            phase="standard",
            available_models=partial_available,
            availability=partial_statuses,
        )["doer"]
        == "gemini-3.1-pro-preview"
    )
    with pytest.raises(ValueError):
        resolve_round_assignments(
            config,
            phase="standard",
            available_models=available,
            attempted_models="invalid",  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError):
        resolve_round_assignments(
            config,
            phase="standard",
            available_models=available,
            attempted_models={"doer": "mai-code-1.1-flash"},  # type: ignore[dict-item]
        )

    exhausted: dict[str, dict[str, str]] = {}
    with pytest.raises(RoleDiversityViolation):
        resolve_round_assignments(config, phase="standard", available_models=exhausted)

    heavy_only = metadata("mai-code-1.1-flash", "claude-opus-4.8", "claude-opus-4.6", "claude-opus-5")
    heavy_only["claude-opus-4.8"]["modelFamily"] = "heavy-a"
    heavy_only["claude-opus-4.6"]["modelFamily"] = "heavy-b"
    escalation = resolve_round_assignments(config, phase="standard", available_models=heavy_only)
    assert escalation.assignments == {
        "doer": "mai-code-1.1-flash",
        "heavyweightDuckA": "claude-opus-4.8",
        "heavyweightDuckB": "claude-opus-4.6",
        "heavyweightAdjudicator": "claude-opus-5",
    }
    assert escalation.effective_phase == "heavyweight_checkpoint"
    assert escalation.escalated
    attempted_doer_exhausted = {"doer": ["mai-code-1.1-flash", "gpt-5.6-luna"]}
    escalated_with_exhausted_doer = resolve_round_assignments(
        config,
        phase="standard",
        available_models=heavy_only,
        attempted_models=attempted_doer_exhausted,
    )
    assert escalated_with_exhausted_doer.assignments == {
        "doer": "mai-code-1.1-flash",
        "heavyweightDuckA": "claude-opus-4.8",
        "heavyweightDuckB": "claude-opus-4.6",
        "heavyweightAdjudicator": "claude-opus-5",
    }
    assert escalated_with_exhausted_doer.effective_phase == "heavyweight_checkpoint"
    assert escalated_with_exhausted_doer.escalated
    with pytest.raises(RoleDiversityViolation):
        resolve_round_assignments(config, phase="standard", available_models=canonical_metadata(*heavy_only))

    fail_closed = document()
    fail_closed["rotationPolicy"]["onExhaustion"] = "fail_closed"
    with pytest.raises(RoleDiversityViolation):
        resolve_round_assignments(validate_trio_config(fail_closed), phase="standard", available_models={})
    with pytest.raises(ValueError):
        resolve_round_assignments(object(), phase="standard", available_models={})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        resolve_round_assignments(config, phase="invalid", available_models={})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        resolve_round_assignments(config, phase="standard", available_models=available, availability="invalid")  # type: ignore[arg-type]
    no_heavy_roles = document()
    del no_heavy_roles["roles"]["heavyweightDuckA"]
    del no_heavy_roles["roles"]["heavyweightDuckB"]
    del no_heavy_roles["roles"]["heavyweightAdjudicator"]
    with pytest.raises(RoleDiversityViolation):
        resolve_round_assignments(validate_trio_config(no_heavy_roles), phase="standard", available_models=heavy_only)


def test_resolve_round_assignments_backtracks_and_rejects_bad_candidates() -> None:
    config = validate_trio_config(document())
    available = metadata(
        "mai-code-1.1-flash",
        "gpt-5.6-luna",
        "claude-sonnet-5",
        "gemini-3.1-pro-preview",
        "claude-opus-5",
    )
    available["claude-sonnet-5"]["tier"] = "tier-1"
    result = resolve_round_assignments(config, phase="standard", available_models=available)
    assert result["duckA"] == "gemini-3.1-pro-preview"
    same_family = metadata(
        "mai-code-1.1-flash",
        "gpt-5.6-luna",
        "claude-sonnet-5",
        "gemini-3.1-pro-preview",
        "claude-opus-5",
    )
    same_family["claude-sonnet-5"]["modelFamily"] = " Reviewer "
    same_family["gpt-5.6-luna"]["modelFamily"] = "reviewer"
    same_family["gemini-3.1-pro-preview"]["modelFamily"] = "reviewer"
    with pytest.raises(RoleDiversityViolation):
        resolve_round_assignments(
            config,
            phase="standard",
            available_models=same_family,
            attempted_models={"doer": ["gpt-5.6-luna"]},
        )
    tier_mismatch = document(doer_tier="tier-2")
    tier_mismatch["roles"]["doer"]["modelPreference"] = "mai-code-1.1-flash"
    tier_mismatch["roles"]["doer"]["fallbackModels"] = ["gemini-3.1-pro-preview"]
    assert (
        resolve_round_assignments(
            validate_trio_config(tier_mismatch),
            phase="standard",
            available_models=metadata(
                "mai-code-1.1-flash",
                "gpt-5.6-luna",
                "claude-sonnet-5",
                "gemini-3.1-pro-preview",
                "claude-opus-5",
            ),
        )["doer"]
        == "gemini-3.1-pro-preview"
    )
    with pytest.raises(RoleDiversityViolation):
        resolve_round_assignments(
            config,
            phase="standard",
            available_models={
                "mai-code-1.1-flash": {"tier": "tier-1"},
                "claude-sonnet-5": {"tier": "tier-9"},  # type: ignore[dict-item]
                "unknown": {"modelId": "unknown"},
                1: {},  # type: ignore[dict-item]
            },
            availability={"mai-code-1.1-flash": {"status": "available"}},
        )
