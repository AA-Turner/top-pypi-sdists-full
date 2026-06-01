"""Tests for `validate_oscal_poam` — OSCAL 1.0.4 POA&M JSON-schema gate.

The high-value test is the **round-trip**: generate POA&M from a realistic
input set, validate it, expect zero errors. Catches structural regressions in
the generator (e.g., dropped required field, malformed UUID, bad enum value)
before they reach a 3PAO.

Negative tests confirm the validator actually fails when fed broken input —
otherwise the round-trip test could pass against a no-op validator.
"""

from __future__ import annotations

from datetime import UTC, datetime

from efterlev.models.indicator import Indicator
from efterlev.primitives.generate import (
    GeneratePoamOscalInput,
    PoamClassificationInput,
    generate_poam_oscal,
)
from efterlev.primitives.validate import (
    ValidateOscalPoamInput,
    validate_oscal_poam,
)


def _indicator(ksi_id: str, controls: list[str], statement: str = "test statement") -> Indicator:
    return Indicator(
        id=ksi_id,
        theme=ksi_id.split("-")[1] if "-" in ksi_id else "TEST",
        name=f"Test indicator {ksi_id}",
        statement=statement,
        controls=controls,
    )


def _classification(
    ksi_id: str,
    status: str = "not_implemented",
    evidence_ids: list[str] | None = None,
    rationale: str = "test rationale",
) -> PoamClassificationInput:
    return PoamClassificationInput(
        ksi_id=ksi_id,
        status=status,  # type: ignore[arg-type]
        rationale=rationale,
        evidence_ids=evidence_ids or [],
    )


_FIXED_TIMESTAMP = datetime(2026, 5, 14, 12, 0, 0, tzinfo=UTC)


def _build_realistic_oscal() -> dict:
    indicators = {
        "KSI-CMT-RMV": _indicator("KSI-CMT-RMV", ["cm-3", "cm-4"]),
        "KSI-IAM-MFA": _indicator("KSI-IAM-MFA", ["ia-2"]),
        "KSI-CNA-RNT": _indicator("KSI-CNA-RNT", ["ac-4", "sc-7"]),
    }
    classifications = [
        _classification("KSI-CMT-RMV", "not_implemented", ["abc123def456"]),
        _classification("KSI-IAM-MFA", "partial", ["xyz789ghi012", "abc123def456"]),
        _classification("KSI-CNA-RNT", "not_implemented", ["mno345pqr678"]),
    ]
    out = generate_poam_oscal(
        GeneratePoamOscalInput(
            classifications=classifications,
            indicators=indicators,
            baseline_id="fedramp-20x-moderate",
            frmr_version="0.9.43-beta",
            system_name="Test System",
            system_id="test-system-001",
            last_modified=_FIXED_TIMESTAMP,
        )
    )
    return out.oscal_document


def test_generator_output_validates_against_schema() -> None:
    """Round-trip: generator output must be schema-conformant by construction."""
    document = _build_realistic_oscal()
    result = validate_oscal_poam(ValidateOscalPoamInput(oscal_document=document))
    assert result.valid, (
        f"Generated OSCAL should validate against the vendored schema. "
        f"Errors: {[(e.path, e.message) for e in result.errors]}"
    )
    assert result.errors == []
    assert "oscal-poam-schema" in result.schema_id


def test_validator_rejects_missing_root() -> None:
    """Empty doc should fail — confirms the validator isn't a no-op."""
    result = validate_oscal_poam(ValidateOscalPoamInput(oscal_document={}))
    assert not result.valid
    assert len(result.errors) >= 1


def test_validator_rejects_missing_uuid() -> None:
    """A POA&M without uuid is structurally invalid per OSCAL."""
    document = _build_realistic_oscal()
    del document["plan-of-action-and-milestones"]["uuid"]
    result = validate_oscal_poam(ValidateOscalPoamInput(oscal_document=document))
    assert not result.valid
    assert any("uuid" in e.message.lower() or e.path.endswith("uuid") for e in result.errors)


def test_validator_rejects_malformed_uuid() -> None:
    """OSCAL UUIDs must match the v4/v5 regex pattern."""
    document = _build_realistic_oscal()
    document["plan-of-action-and-milestones"]["uuid"] = "not-a-uuid"
    result = validate_oscal_poam(ValidateOscalPoamInput(oscal_document=document))
    assert not result.valid
    assert any(e.validator == "pattern" for e in result.errors)


def test_validator_surfaces_all_errors_not_first_fail() -> None:
    """Multiple violations should all surface; we don't early-exit."""
    document = _build_realistic_oscal()
    del document["plan-of-action-and-milestones"]["uuid"]
    del document["plan-of-action-and-milestones"]["metadata"]
    result = validate_oscal_poam(ValidateOscalPoamInput(oscal_document=document))
    assert not result.valid
    assert len(result.errors) >= 2


def test_schema_id_reports_oscal_version() -> None:
    """Schema id should reference the 1.0.4 OSCAL POA&M schema."""
    document = _build_realistic_oscal()
    result = validate_oscal_poam(ValidateOscalPoamInput(oscal_document=document))
    assert "1.0.4" in result.schema_id
