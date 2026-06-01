"""Tests for `validate_oscal_fedramp_rules` (v0.1.107 OSCAL arc step 3).

Layer 2 of the OSCAL conformance gate. Layer 1 (`validate_oscal_poam`,
v0.1.106) ensures structural conformance; this layer enforces FedRAMP-
specific rules ported from the GSA fedramp-automation rule set.

Round-trip is the high-value test: the generator + Layer 1 + Layer 2
should all agree on the same input. Negative tests confirm each rule
actually fires.
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
    ValidateOscalFedrampRulesInput,
    validate_oscal_fedramp_rules,
)


def _indicator(ksi_id: str, controls: list[str]) -> Indicator:
    return Indicator(
        id=ksi_id,
        theme=ksi_id.split("-")[1] if "-" in ksi_id else "TEST",
        name=f"Test indicator {ksi_id}",
        statement="test statement",
        controls=controls,
    )


def _build_realistic_oscal() -> dict:
    indicators = {
        "KSI-IAM-MFA": _indicator("KSI-IAM-MFA", ["ia-2"]),
        "KSI-SVC-SNT": _indicator("KSI-SVC-SNT", ["sc-13"]),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-IAM-MFA",
            status="not_implemented",
            rationale="No MFA policy.",
            evidence_ids=["e1"],
        ),
        PoamClassificationInput(
            ksi_id="KSI-SVC-SNT",
            status="partial",
            rationale="Partial encryption.",
            evidence_ids=["e2"],
        ),
    ]
    out = generate_poam_oscal(
        GeneratePoamOscalInput(
            classifications=classifications,
            indicators=indicators,
            baseline_id="fedramp-20x-moderate",
            frmr_version="0.9.43-beta",
            system_name="Test",
            system_id="test-001",
            last_modified=datetime(2026, 5, 14, 12, 0, 0, tzinfo=UTC),
        )
    )
    return out.oscal_document


# --- Round-trip ---------------------------------------------------------


def test_generator_output_passes_all_fedramp_rules() -> None:
    """v0.1.107 generator must satisfy every shipped FedRAMP rule."""
    document = _build_realistic_oscal()
    result = validate_oscal_fedramp_rules(ValidateOscalFedrampRulesInput(oscal_document=document))
    assert result.valid, (
        f"Generator output should pass all FedRAMP rules. "
        f"Violations: {[(v.rule_id, v.path, v.message) for v in result.violations]}"
    )
    assert result.rules_evaluated == 5


# --- FRMP-OSCAL-001: severity enum --------------------------------------


def test_rule_001_rejects_non_fedramp_severity() -> None:
    """severity must be one of {high, moderate, low}."""
    document = _build_realistic_oscal()
    poam_items = document["plan-of-action-and-milestones"]["poam-items"]
    for prop in poam_items[0]["props"]:
        if prop["name"] == "severity":
            prop["value"] = "medium"  # Bad: should be "moderate"
    result = validate_oscal_fedramp_rules(ValidateOscalFedrampRulesInput(oscal_document=document))
    assert not result.valid
    assert any(v.rule_id == "FRMP-OSCAL-001" for v in result.violations)


def test_rule_001_rejects_missing_severity() -> None:
    """A POA&M item without a severity prop fails FRMP-OSCAL-001."""
    document = _build_realistic_oscal()
    item = document["plan-of-action-and-milestones"]["poam-items"][0]
    item["props"] = [p for p in item["props"] if p["name"] != "severity"]
    result = validate_oscal_fedramp_rules(ValidateOscalFedrampRulesInput(oscal_document=document))
    assert not result.valid
    assert any(v.rule_id == "FRMP-OSCAL-001" for v in result.violations)


# --- FRMP-OSCAL-002: risk status enum -----------------------------------


def test_rule_002_rejects_non_fedramp_risk_status() -> None:
    """risk status must be in the FedRAMP enumeration."""
    document = _build_realistic_oscal()
    document["plan-of-action-and-milestones"]["risks"][0]["status"] = "in-progress"
    result = validate_oscal_fedramp_rules(ValidateOscalFedrampRulesInput(oscal_document=document))
    assert not result.valid
    assert any(v.rule_id == "FRMP-OSCAL-002" for v in result.violations)


# --- FRMP-OSCAL-003: poam-item must reference evidence ------------------


def test_rule_003_rejects_orphan_poam_item() -> None:
    """A POA&M item with neither related-risks nor related-observations fails."""
    document = _build_realistic_oscal()
    document["plan-of-action-and-milestones"]["poam-items"][0]["related-risks"] = []
    if "related-observations" in document["plan-of-action-and-milestones"]["poam-items"][0]:
        del document["plan-of-action-and-milestones"]["poam-items"][0]["related-observations"]
    result = validate_oscal_fedramp_rules(ValidateOscalFedrampRulesInput(oscal_document=document))
    assert not result.valid
    assert any(v.rule_id == "FRMP-OSCAL-003" for v in result.violations)


# --- FRMP-OSCAL-004: baseline enum --------------------------------------


def test_rule_004_rejects_unknown_baseline() -> None:
    """frmr-baseline prop must reference a FedRAMP 20x baseline."""
    document = _build_realistic_oscal()
    item = document["plan-of-action-and-milestones"]["poam-items"][0]
    for prop in item["props"]:
        if prop["name"] == "frmr-baseline":
            prop["value"] = "fedramp-rev5-moderate"  # Wrong: not 20x
    result = validate_oscal_fedramp_rules(ValidateOscalFedrampRulesInput(oscal_document=document))
    assert not result.valid
    assert any(v.rule_id == "FRMP-OSCAL-004" for v in result.violations)


# --- FRMP-OSCAL-005: oscal-version enum ---------------------------------


def test_rule_005_rejects_unknown_oscal_version() -> None:
    """oscal-version must be in the FedRAMP-accepted set."""
    document = _build_realistic_oscal()
    document["plan-of-action-and-milestones"]["metadata"]["oscal-version"] = "1.1.0"
    result = validate_oscal_fedramp_rules(ValidateOscalFedrampRulesInput(oscal_document=document))
    assert not result.valid
    assert any(v.rule_id == "FRMP-OSCAL-005" for v in result.violations)


# --- All-rules surfacing ------------------------------------------------


def test_multiple_violations_all_surfaced() -> None:
    """Multiple bad fields produce multiple violations (no early-exit)."""
    document = _build_realistic_oscal()
    document["plan-of-action-and-milestones"]["risks"][0]["status"] = "bogus"
    document["plan-of-action-and-milestones"]["metadata"]["oscal-version"] = "9.9.9"
    result = validate_oscal_fedramp_rules(ValidateOscalFedrampRulesInput(oscal_document=document))
    assert not result.valid
    rule_ids = {v.rule_id for v in result.violations}
    assert "FRMP-OSCAL-002" in rule_ids
    assert "FRMP-OSCAL-005" in rule_ids
