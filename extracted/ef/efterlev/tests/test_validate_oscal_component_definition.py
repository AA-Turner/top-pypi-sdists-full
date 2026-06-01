"""Tests for `validate_oscal_component_definition` (v0.1.108).

Sibling to `test_validate_oscal_poam.py`. Same shape: round-trip the
generator output through the schema, expect zero errors. Negative tests
confirm the validator actually catches structural breakage.
"""

from __future__ import annotations

from datetime import UTC, datetime

from efterlev.models.indicator import Indicator
from efterlev.primitives.generate import (
    GenerateComponentDefinitionOscalInput,
    PoamClassificationInput,
    generate_component_definition_oscal,
)
from efterlev.primitives.validate import (
    ValidateOscalComponentDefinitionInput,
    validate_oscal_component_definition,
)


def _build_realistic_cd() -> dict:
    indicators = {
        "KSI-IAM-MFA": Indicator(
            id="KSI-IAM-MFA",
            theme="IAM",
            name="Phishing-Resistant MFA",
            statement="Enforce phishing-resistant MFA.",
            controls=["ia-2"],
        ),
        "KSI-SVC-SNT": Indicator(
            id="KSI-SVC-SNT",
            theme="SVC",
            name="Securing Network Traffic",
            statement="Encrypt network traffic.",
            controls=["sc-8", "sc-13"],
        ),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-IAM-MFA",
            status="implemented",
            rationale="MFA via IAM policy.",
            evidence_ids=["e1"],
        ),
        PoamClassificationInput(
            ksi_id="KSI-SVC-SNT",
            status="partial",
            rationale="ALB uses HTTPS; internal traffic on HTTP.",
            evidence_ids=["e2"],
        ),
    ]
    out = generate_component_definition_oscal(
        GenerateComponentDefinitionOscalInput(
            classifications=classifications,
            indicators=indicators,
            baseline_id="fedramp-20x-moderate",
            frmr_version="0.9.43-beta",
            system_name="Test System",
            system_id="test-cd-001",
            last_modified=datetime(2026, 5, 14, 12, 0, 0, tzinfo=UTC),
        )
    )
    return out.oscal_document


def test_generator_output_validates_against_schema() -> None:
    """Round-trip: CD generator output must be schema-conformant."""
    document = _build_realistic_cd()
    result = validate_oscal_component_definition(
        ValidateOscalComponentDefinitionInput(oscal_document=document)
    )
    assert result.valid, (
        f"Generated CD should validate against the vendored schema. "
        f"Errors: {[(e.path, e.message) for e in result.errors]}"
    )
    assert result.errors == []
    assert "oscal-component-definition-schema" in result.schema_id


def test_validator_rejects_empty_doc() -> None:
    """Empty doc fails — confirms the validator isn't a no-op."""
    result = validate_oscal_component_definition(
        ValidateOscalComponentDefinitionInput(oscal_document={})
    )
    assert not result.valid
    assert len(result.errors) >= 1


def test_validator_rejects_missing_uuid() -> None:
    """A CD without uuid is invalid per OSCAL."""
    document = _build_realistic_cd()
    del document["component-definition"]["uuid"]
    result = validate_oscal_component_definition(
        ValidateOscalComponentDefinitionInput(oscal_document=document)
    )
    assert not result.valid


def test_validator_rejects_malformed_uuid() -> None:
    """OSCAL UUIDs must match the v4/v5 regex pattern."""
    document = _build_realistic_cd()
    document["component-definition"]["uuid"] = "not-a-uuid"
    result = validate_oscal_component_definition(
        ValidateOscalComponentDefinitionInput(oscal_document=document)
    )
    assert not result.valid
    assert any(e.validator == "pattern" for e in result.errors)


def test_validator_rejects_missing_required_component_field() -> None:
    """A component without `type` (a required field) fails validation."""
    document = _build_realistic_cd()
    del document["component-definition"]["components"][0]["type"]
    result = validate_oscal_component_definition(
        ValidateOscalComponentDefinitionInput(oscal_document=document)
    )
    assert not result.valid
