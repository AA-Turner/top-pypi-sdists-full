"""Tests for the OSCAL Component-Definition generator (v0.1.108).

Same determinism guarantees as the POA&M generator: same inputs +
pinned `last_modified` produce byte-identical JSON.
"""

from __future__ import annotations

from datetime import UTC, datetime

from efterlev.models.indicator import Indicator
from efterlev.primitives.generate import (
    GenerateComponentDefinitionOscalInput,
    PoamClassificationInput,
    generate_component_definition_oscal,
)


def _indicator(ksi_id: str, controls: list[str], statement: str = "Test KSI.") -> Indicator:
    return Indicator(
        id=ksi_id,
        theme=ksi_id.split("-")[1] if "-" in ksi_id else "TEST",
        name=f"Test indicator {ksi_id}",
        statement=statement,
        controls=controls,
    )


def _input(
    classifications: list[PoamClassificationInput],
    indicators: dict[str, Indicator],
    *,
    system_name: str = "Test System",
    system_id: str = "test-system-cd-123",
    last_modified: datetime | None = None,
) -> GenerateComponentDefinitionOscalInput:
    return GenerateComponentDefinitionOscalInput(
        classifications=classifications,
        indicators=indicators,
        baseline_id="fedramp-20x-moderate",
        frmr_version="0.9.43-beta",
        system_name=system_name,
        system_id=system_id,
        last_modified=last_modified or datetime(2026, 5, 14, 12, 0, 0, tzinfo=UTC),
    )


def test_minimal_cd_shape() -> None:
    """One KSI, one control → one component, one implemented-requirement."""
    indicators = {"KSI-IAM-MFA": _indicator("KSI-IAM-MFA", ["ia-2"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-IAM-MFA",
            status="implemented",
            rationale="MFA enforced via IAM policy.",
            evidence_ids=["e1"],
        )
    ]
    out = generate_component_definition_oscal(_input(classifications, indicators))
    cd = out.oscal_document["component-definition"]

    assert cd["uuid"]
    assert cd["metadata"]["title"] == "Component Definition for Test System"
    assert cd["metadata"]["oscal-version"] == "1.0.4"
    assert len(cd["components"]) == 1
    component = cd["components"][0]
    assert component["type"] == "service"
    assert component["title"] == "Test System"
    assert len(component["control-implementations"]) == 1
    ci = component["control-implementations"][0]
    assert len(ci["implemented-requirements"]) == 1
    ir = ci["implemented-requirements"][0]
    assert ir["control-id"] == "ia-2"
    assert out.component_count == 1
    assert out.implemented_requirement_count == 1


def test_one_implemented_requirement_per_cited_control() -> None:
    """A KSI with N controls produces N implemented-requirements."""
    indicators = {"KSI-MULTI": _indicator("KSI-MULTI", ["sc-13", "sc-28", "ia-2"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-MULTI",
            status="partial",
            rationale="r",
            evidence_ids=["e1"],
        )
    ]
    out = generate_component_definition_oscal(_input(classifications, indicators))
    irs = out.oscal_document["component-definition"]["components"][0]["control-implementations"][0][
        "implemented-requirements"
    ]
    control_ids = sorted(ir["control-id"] for ir in irs)
    assert control_ids == ["ia-2", "sc-13", "sc-28"]


def test_implementation_status_prop_reflects_classification() -> None:
    """Each implemented-requirement carries an `implementation-status` prop."""
    indicators = {
        "KSI-IMPL": _indicator("KSI-IMPL", ["sc-1"]),
        "KSI-PART": _indicator("KSI-PART", ["sc-2"]),
        "KSI-NI": _indicator("KSI-NI", ["sc-3"]),
        "KSI-NA": _indicator("KSI-NA", ["sc-4"]),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-IMPL", status="implemented", rationale="r", evidence_ids=["e"]
        ),
        PoamClassificationInput(
            ksi_id="KSI-PART", status="partial", rationale="r", evidence_ids=["e"]
        ),
        PoamClassificationInput(
            ksi_id="KSI-NI", status="not_implemented", rationale="r", evidence_ids=[]
        ),
        PoamClassificationInput(
            ksi_id="KSI-NA", status="not_applicable", rationale="r", evidence_ids=[]
        ),
    ]
    out = generate_component_definition_oscal(_input(classifications, indicators))
    irs = out.oscal_document["component-definition"]["components"][0]["control-implementations"][0][
        "implemented-requirements"
    ]
    status_by_control = {
        ir["control-id"]: next(
            p["value"] for p in ir["props"] if p["name"] == "implementation-status"
        )
        for ir in irs
    }
    assert status_by_control == {
        "sc-1": "implemented",
        "sc-2": "partial",
        "sc-3": "planned",  # not_implemented → planned per OSCAL conventions
        "sc-4": "not-applicable",
    }


def test_uuid_determinism_across_runs() -> None:
    """Same input → same UUIDs across runs."""
    indicators = {"KSI-X": _indicator("KSI-X", ["sc-1"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-X", status="implemented", rationale="r", evidence_ids=["e1"]
        )
    ]
    pinned = datetime(2026, 5, 14, 12, 0, 0, tzinfo=UTC)
    out1 = generate_component_definition_oscal(
        _input(classifications, indicators, last_modified=pinned)
    )
    out2 = generate_component_definition_oscal(
        _input(classifications, indicators, last_modified=pinned)
    )
    assert out1.oscal_document == out2.oscal_document


def test_unknown_ksi_skipped_and_reported() -> None:
    """KSI not in indicator dict is skipped + reported (no fabrication)."""
    indicators = {"KSI-KNOWN": _indicator("KSI-KNOWN", ["sc-1"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-KNOWN", status="implemented", rationale="r", evidence_ids=[]
        ),
        PoamClassificationInput(
            ksi_id="KSI-UNKNOWN", status="implemented", rationale="r", evidence_ids=[]
        ),
    ]
    out = generate_component_definition_oscal(_input(classifications, indicators))
    assert out.implemented_requirement_count == 1
    assert out.skipped_unknown_ksi == ["KSI-UNKNOWN"]


def test_narratives_emit_as_statements() -> None:
    """v0.1.108.5: Documentation Agent narratives populate implemented-requirement.statements[]."""
    indicators = {
        "KSI-IAM-MFA": _indicator("KSI-IAM-MFA", ["ia-2"]),
        "KSI-NO-NARR": _indicator("KSI-NO-NARR", ["sc-1"]),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-IAM-MFA", status="implemented", rationale="r", evidence_ids=["e1"]
        ),
        PoamClassificationInput(
            ksi_id="KSI-NO-NARR", status="implemented", rationale="r", evidence_ids=["e2"]
        ),
    ]
    out = generate_component_definition_oscal(
        GenerateComponentDefinitionOscalInput(
            classifications=classifications,
            indicators=indicators,
            baseline_id="fedramp-20x-moderate",
            frmr_version="0.9.43-beta",
            system_name="Test",
            system_id="test-narratives-001",
            narratives={
                "KSI-IAM-MFA": "MFA is enforced via IAM password policy + MFA-required IAM policy.",
            },
            last_modified=datetime(2026, 5, 14, 12, 0, 0, tzinfo=UTC),
        )
    )
    irs = out.oscal_document["component-definition"]["components"][0]["control-implementations"][0][
        "implemented-requirements"
    ]
    by_control = {ir["control-id"]: ir for ir in irs}

    # KSI-IAM-MFA has a narrative → statements[] populated
    mfa_stmts = by_control["ia-2"].get("statements", [])
    assert len(mfa_stmts) == 1
    assert mfa_stmts[0]["statement-id"] == "ia-2_smt"
    assert "MFA is enforced" in mfa_stmts[0]["description"]

    # KSI-NO-NARR has no narrative → no statements key (omitted, not empty)
    assert "statements" not in by_control["sc-1"]


def test_narratives_are_optional_backward_compatible() -> None:
    """v0.1.108 callers without narratives still produce valid output."""
    indicators = {"KSI-A": _indicator("KSI-A", ["sc-1"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-A", status="implemented", rationale="r", evidence_ids=["e1"]
        )
    ]
    out = generate_component_definition_oscal(_input(classifications, indicators))
    irs = out.oscal_document["component-definition"]["components"][0]["control-implementations"][0][
        "implemented-requirements"
    ]
    # No narratives provided → no statements key
    assert all("statements" not in ir for ir in irs)


def test_custom_props_carry_ns_field() -> None:
    """v0.1.110 regression guard: every custom prop carries `ns`."""
    indicators = {"KSI-A": _indicator("KSI-A", ["sc-1"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-A", status="implemented", rationale="r", evidence_ids=["e1"]
        )
    ]
    out = generate_component_definition_oscal(_input(classifications, indicators))
    irs = out.oscal_document["component-definition"]["components"][0]["control-implementations"][0][
        "implemented-requirements"
    ]
    for ir in irs:
        for prop in ir.get("props", []):
            assert "ns" in prop, f"implemented-requirement prop {prop['name']!r} missing ns"


def test_oscal_document_json_serializable() -> None:
    """Output must json.dumps cleanly."""
    import json

    indicators = {"KSI-A": _indicator("KSI-A", ["sc-1"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-A", status="implemented", rationale="r", evidence_ids=["e1"]
        )
    ]
    out = generate_component_definition_oscal(_input(classifications, indicators))
    encoded = json.dumps(out.oscal_document, indent=2, sort_keys=False)
    decoded = json.loads(encoded)
    assert decoded == out.oscal_document
