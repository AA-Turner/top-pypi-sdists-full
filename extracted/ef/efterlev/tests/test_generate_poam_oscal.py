"""Tests for the OSCAL POA&M generator (v0.1.105).

The primitive is deterministic — same inputs produce byte-identical
JSON. UUIDs are derived via uuid5 from a fixed namespace + the
underlying KSI/control identifiers, so re-runs of the same scan
produce stable diffs (important for tracking deltas across releases
and for downstream consumers like RegScale OSCAL Hub that may
detect "changes" via UUID comparison).
"""

from __future__ import annotations

from datetime import UTC, datetime

from efterlev.models.indicator import Indicator
from efterlev.primitives.generate import (
    GeneratePoamOscalInput,
    PoamClassificationInput,
    generate_poam_oscal,
)


def _indicator(ksi_id: str, controls: list[str], statement: str = "Test KSI.") -> Indicator:
    """Build a minimal Indicator for testing."""
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
    system_id: str = "test-system-123",
    last_modified: datetime | None = None,
) -> GeneratePoamOscalInput:
    """Helper to build a GeneratePoamOscalInput with sane defaults."""
    return GeneratePoamOscalInput(
        classifications=classifications,
        indicators=indicators,
        baseline_id="fedramp-20x-moderate",
        frmr_version="0.9.43-beta",
        system_name=system_name,
        system_id=system_id,
        last_modified=last_modified or datetime(2026, 5, 14, 12, 0, 0, tzinfo=UTC),
    )


# --- Top-level OSCAL document shape ------------------------------------


def test_minimal_oscal_poam_shape() -> None:
    """A POA&M with one open KSI produces a valid-shape OSCAL document."""
    indicators = {
        "KSI-SVC-SNT": _indicator("KSI-SVC-SNT", ["sc-13"]),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-SVC-SNT",
            status="not_implemented",
            rationale="No KMS-encryption configured.",
            evidence_ids=["abc123"],
        ),
    ]
    out = generate_poam_oscal(_input(classifications, indicators))
    poam = out.oscal_document["plan-of-action-and-milestones"]

    assert poam["uuid"]
    assert poam["metadata"]["title"] == "Plan of Action and Milestones for Test System"
    assert poam["metadata"]["oscal-version"] == "1.0.4"
    assert poam["metadata"]["version"] == "1.0.0"
    assert poam["system-id"]["id"] == "test-system-123"
    assert len(poam["poam-items"]) == 1
    assert len(poam["risks"]) == 1
    assert len(poam["observations"]) == 1
    assert out.item_count == 1


def test_uuid_determinism_across_runs() -> None:
    """Same input → same UUIDs. Re-running produces stable diffs."""
    indicators = {
        "KSI-SVC-SNT": _indicator("KSI-SVC-SNT", ["sc-13"]),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-SVC-SNT",
            status="not_implemented",
            rationale="No KMS.",
            evidence_ids=["abc123"],
        ),
    ]
    pinned = datetime(2026, 5, 14, 12, 0, 0, tzinfo=UTC)
    out1 = generate_poam_oscal(_input(classifications, indicators, last_modified=pinned))
    out2 = generate_poam_oscal(_input(classifications, indicators, last_modified=pinned))
    assert out1.oscal_document == out2.oscal_document


def test_uuid_changes_when_system_id_changes() -> None:
    """Different system-id → different root UUID (different POA&M document)."""
    indicators = {"KSI-X": _indicator("KSI-X", ["sc-1"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-X", status="not_implemented", rationale="r", evidence_ids=[]
        )
    ]
    out_a = generate_poam_oscal(_input(classifications, indicators, system_id="system-a"))
    out_b = generate_poam_oscal(_input(classifications, indicators, system_id="system-b"))
    assert (
        out_a.oscal_document["plan-of-action-and-milestones"]["uuid"]
        != out_b.oscal_document["plan-of-action-and-milestones"]["uuid"]
    )


# --- POA&M item shape --------------------------------------------------


def test_poam_item_severity_heuristic() -> None:
    """not_implemented → high; partial → moderate (FedRAMP convention)."""
    indicators = {
        "KSI-A": _indicator("KSI-A", ["sc-1"]),
        "KSI-B": _indicator("KSI-B", ["sc-2"]),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-A", status="not_implemented", rationale="r", evidence_ids=[]
        ),
        PoamClassificationInput(
            ksi_id="KSI-B",
            status="partial",
            rationale="r",
            evidence_ids=["e1"],
        ),
    ]
    out = generate_poam_oscal(_input(classifications, indicators))
    items = out.oscal_document["plan-of-action-and-milestones"]["poam-items"]
    sev_by_ksi = {
        next(p["value"] for p in i["props"] if p["name"] == "weakness-source-identifier"): next(
            p["value"] for p in i["props"] if p["name"] == "severity"
        )
        for i in items
    }
    assert sev_by_ksi == {"KSI-A": "high", "KSI-B": "moderate"}


def test_implemented_ksis_skipped() -> None:
    """implemented / not_applicable / evidence_layer_inapplicable → no POA&M item."""
    indicators = {
        "KSI-IMPL": _indicator("KSI-IMPL", ["sc-1"]),
        "KSI-NA": _indicator("KSI-NA", ["sc-2"]),
        "KSI-INAPP": _indicator("KSI-INAPP", ["sc-3"]),
        "KSI-OPEN": _indicator("KSI-OPEN", ["sc-4"]),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-IMPL",
            status="implemented",
            rationale="r",
            evidence_ids=["e"],
        ),
        PoamClassificationInput(
            ksi_id="KSI-NA",
            status="not_applicable",
            rationale="r",
            evidence_ids=[],
        ),
        PoamClassificationInput(
            ksi_id="KSI-INAPP",
            status="evidence_layer_inapplicable",
            rationale="r",
            evidence_ids=[],
        ),
        PoamClassificationInput(
            ksi_id="KSI-OPEN",
            status="not_implemented",
            rationale="r",
            evidence_ids=[],
        ),
    ]
    out = generate_poam_oscal(_input(classifications, indicators))
    items = out.oscal_document["plan-of-action-and-milestones"]["poam-items"]
    assert len(items) == 1
    assert "KSI-OPEN" in items[0]["title"]


def test_unknown_ksi_skipped_and_reported() -> None:
    """KSI not in indicator dict is skipped + reported (no fabrication)."""
    indicators = {"KSI-KNOWN": _indicator("KSI-KNOWN", ["sc-1"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-KNOWN",
            status="not_implemented",
            rationale="r",
            evidence_ids=[],
        ),
        PoamClassificationInput(
            ksi_id="KSI-UNKNOWN",
            status="not_implemented",
            rationale="r",
            evidence_ids=[],
        ),
    ]
    out = generate_poam_oscal(_input(classifications, indicators))
    assert out.item_count == 1
    assert out.skipped_unknown_ksi == ["KSI-UNKNOWN"]


# --- Risk + observation shape ----------------------------------------


def test_one_risk_per_control() -> None:
    """A KSI with N controls produces N risks (per-control deficiency).

    OSCAL POA&M models per-control deficiencies as `risks`, not `findings`
    (findings live in assessment-results, a sibling layer). Each risk
    carries a control-id prop so 3PAOs can scan by 800-53 control.
    """
    indicators = {
        "KSI-MULTI": _indicator("KSI-MULTI", ["sc-13", "sc-28", "ia-2"]),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-MULTI",
            status="not_implemented",
            rationale="r",
            evidence_ids=["e1"],
        ),
    ]
    out = generate_poam_oscal(_input(classifications, indicators))
    risks = out.oscal_document["plan-of-action-and-milestones"]["risks"]
    assert len(risks) == 3
    control_ids = sorted(
        next(p["value"] for p in r["props"] if p["name"] == "control-id") for r in risks
    )
    assert control_ids == ["ia-2", "sc-13", "sc-28"]


def test_observations_deduplicated_by_evidence_id() -> None:
    """One observation per unique evidence_id, even if multiple risks cite it."""
    indicators = {"KSI-A": _indicator("KSI-A", ["sc-1", "sc-2"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-A",
            status="not_implemented",
            rationale="r",
            evidence_ids=["shared-evidence-1"],
        ),
    ]
    out = generate_poam_oscal(_input(classifications, indicators))
    observations = out.oscal_document["plan-of-action-and-milestones"]["observations"]
    assert len(observations) == 1


def test_risk_status_is_open_for_all_emitted_risks() -> None:
    """Every emitted risk gets status=open. Reviewers transition to
    investigating/remediation-pending/closed downstream.
    """
    indicators = {
        "KSI-NI": _indicator("KSI-NI", ["sc-1"]),
        "KSI-PA": _indicator("KSI-PA", ["sc-2"]),
    }
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-NI", status="not_implemented", rationale="r", evidence_ids=[]
        ),
        PoamClassificationInput(
            ksi_id="KSI-PA",
            status="partial",
            rationale="r",
            evidence_ids=["e1"],
        ),
    ]
    out = generate_poam_oscal(_input(classifications, indicators))
    risks = out.oscal_document["plan-of-action-and-milestones"]["risks"]
    assert {r["status"] for r in risks} == {"open"}


# --- JSON serializability --------------------------------------------


def test_custom_props_carry_ns_field() -> None:
    """v0.1.110: every custom prop name must carry an `ns` namespace field.

    Caught by NIST oscal-cli — OSCAL constrains `prop.name` to a small
    well-known set (`marking` etc.) unless namespace-qualified via `ns`.
    Regression guard for the v0.1.110 fix.
    """
    indicators = {"KSI-A": _indicator("KSI-A", ["sc-1"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-A", status="not_implemented", rationale="r", evidence_ids=["e1"]
        )
    ]
    out = generate_poam_oscal(_input(classifications, indicators))
    poam = out.oscal_document["plan-of-action-and-milestones"]

    # Every prop on every poam-item carries ns
    for item in poam["poam-items"]:
        for prop in item["props"]:
            assert "ns" in prop, f"poam-item prop {prop['name']!r} missing ns"

    # Every prop on every risk carries ns
    for risk in poam["risks"]:
        for prop in risk["props"]:
            assert "ns" in prop, f"risk prop {prop['name']!r} missing ns"


def test_oscal_document_json_serializable() -> None:
    """Output dict must json.dumps cleanly (no unhashable, no datetime, no UUID)."""
    import json

    indicators = {"KSI-A": _indicator("KSI-A", ["sc-1"])}
    classifications = [
        PoamClassificationInput(
            ksi_id="KSI-A",
            status="not_implemented",
            rationale="r",
            evidence_ids=["e1"],
        )
    ]
    out = generate_poam_oscal(_input(classifications, indicators))
    # Round-trip — ensures JSON-serializable + structurally stable.
    encoded = json.dumps(out.oscal_document, indent=2, sort_keys=False)
    decoded = json.loads(encoded)
    assert decoded == out.oscal_document
