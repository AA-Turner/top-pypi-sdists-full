"""Tests for `generate_vdr_report` (v0.1.162 / #367).

VDR is the artifact FedRAMP 20x is moving toward as a replacement for
the traditional POA&M per RFC-0012. v0.1.162 ships the ahead-of-
finalization shape; these tests pin the shape so when RFC-0012 lands
and we revise, the diff is intentional.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest

from efterlev.models import Indicator
from efterlev.primitives.generate import (
    VDR_SCHEMA_VERSION,
    GenerateVdrReportInput,
    VdrClassificationInput,
    generate_vdr_report,
)


def _ind(ksi_id: str, controls: list[str] | None = None) -> Indicator:
    return Indicator(
        id=ksi_id,
        theme=ksi_id.split("-")[1],
        name=f"Test {ksi_id}",
        statement=f"Statement for {ksi_id}.",
        controls=controls or ["sc-28"],
    )


def _clf(
    ksi_id: str = "KSI-SVC-VRI",
    status: str = "partial",
    cve_ids: list[str] | None = None,
) -> VdrClassificationInput:
    return VdrClassificationInput(
        ksi_id=ksi_id,
        status=status,
        rationale=f"Rationale for {ksi_id}",
        evidence_ids=["sha256:" + "a" * 64],
        cve_ids=cve_ids or [],
    )


def _input(
    classifications: list[VdrClassificationInput],
    *,
    output_format: str = "json",
) -> GenerateVdrReportInput:
    indicators = {c.ksi_id: _ind(c.ksi_id) for c in classifications}
    return GenerateVdrReportInput(
        classifications=classifications,
        indicators=indicators,
        baseline_id="fedramp-20x-moderate",
        frmr_version="0.9.43-beta",
        generated_at=datetime(2026, 5, 19, 12, 0, 0, tzinfo=UTC),
        output_format=output_format,  # type: ignore[arg-type]
    )


# --- Status filtering -----------------------------------------------------


def test_only_partial_and_not_implemented_become_entries() -> None:
    """`implemented`, `not_applicable`, and `evidence_layer_inapplicable`
    are not vulnerabilities — they don't appear in the VDR."""
    classifications = [
        _clf("KSI-SVC-VRI", status="partial"),
        _clf("KSI-IAM-MFA", status="implemented"),
        _clf("KSI-SVC-SNT", status="not_implemented"),
        _clf("KSI-CED-RGT", status="not_applicable"),
        _clf("KSI-CNA-RNT", status="evidence_layer_inapplicable"),
    ]
    result = generate_vdr_report(_input(classifications))
    assert result.entry_count == 2
    statuses = {e.ksi_id for e in result.entries}
    assert statuses == {"KSI-SVC-VRI", "KSI-SVC-SNT"}


# --- Sort order -----------------------------------------------------------


def test_entries_sorted_high_severity_first_then_alphabetical() -> None:
    classifications = [
        _clf("KSI-SVC-PRR", status="partial"),
        _clf("KSI-SVC-VRI", status="not_implemented"),
        _clf("KSI-IAM-MFA", status="partial"),
        _clf("KSI-IAM-SUS", status="not_implemented"),
    ]
    result = generate_vdr_report(_input(classifications))
    # HIGH (not_implemented) before MEDIUM (partial); alphabetical within
    # each tier.
    assert [e.ksi_id for e in result.entries] == [
        "KSI-IAM-SUS",
        "KSI-SVC-VRI",
        "KSI-IAM-MFA",
        "KSI-SVC-PRR",
    ]


# --- RFC-0012 required fields --------------------------------------------


def test_entry_carries_every_rfc_0012_required_field() -> None:
    """RFC-0012 enumerates required fields; this test pins the shape so
    when we revise post-finalization the diff is intentional."""
    result = generate_vdr_report(_input([_clf("KSI-SVC-VRI", status="not_implemented")]))
    e = result.entries[0]
    # Required by RFC-0012:
    assert e.internal_id.startswith("VDR-")
    assert isinstance(e.cve_ids, list)
    assert e.detection_timestamp == "2026-05-19T12:00:00+00:00"
    assert e.mitigation_deadline  # ISO date
    assert e.remediation_deadline
    assert e.internet_reachable in ("true", "false", "REVIEW")
    assert e.exploitability
    assert e.impact in ("HIGH", "MEDIUM", "LOW", "TBD")
    assert e.mitigation_plan
    assert e.remediation_plan
    assert isinstance(e.actions_taken, list)
    assert e.status in ("open", "in_progress", "mitigated", "remediated")
    # Traceability fields:
    assert e.ksi_id == "KSI-SVC-VRI"
    assert e.severity == "HIGH"  # not_implemented → HIGH
    assert "Rationale" in e.rationale
    assert e.evidence_ids
    assert e.mitigation_deadline_basis


def test_internet_reachable_defaults_to_review_not_a_guess() -> None:
    """IaC scanners can't reliably infer internet-reachability — a bucket
    might be reachable via a CloudFront distribution not in this Terraform
    stack. Don't pretend. Defaulting to 'REVIEW' forces reviewer action."""
    result = generate_vdr_report(_input([_clf()]))
    assert result.entries[0].internet_reachable == "REVIEW"


def test_deadline_basis_explains_rfc_0012_3_day_tightening() -> None:
    """Reviewer marking internet_reachable=true must tighten deadline to
    3 days per RFC-0012. The basis text spells out the rule so the
    reviewer doesn't have to look it up."""
    result = generate_vdr_report(_input([_clf(status="not_implemented")]))
    basis = result.entries[0].mitigation_deadline_basis
    assert "RFC-0012" in basis
    assert "3d" in basis
    assert "internet_reachable=true" in basis


# --- Severity mapping -----------------------------------------------------


def test_severity_mapping_mirrors_poam_for_consistency() -> None:
    """VDR and POA&M ship side-by-side today; same severity for the same
    classification means cross-artifact reads don't surprise reviewers."""
    high = generate_vdr_report(_input([_clf(status="not_implemented")]))
    medium = generate_vdr_report(_input([_clf(status="partial")]))
    assert high.entries[0].severity == "HIGH"
    assert high.entries[0].impact == "HIGH"
    assert medium.entries[0].severity == "MEDIUM"
    assert medium.entries[0].impact == "MEDIUM"


# --- Determinism ----------------------------------------------------------


def test_same_input_produces_byte_identical_json() -> None:
    """Deterministic primitive: re-runs are diffable."""
    inp = _input([_clf(), _clf("KSI-IAM-MFA", status="not_implemented")])
    a = generate_vdr_report(inp)
    b = generate_vdr_report(inp)
    assert a.rendered == b.rendered


def test_same_input_produces_byte_identical_markdown() -> None:
    inp = _input([_clf(), _clf("KSI-IAM-MFA", status="not_implemented")], output_format="markdown")
    a = generate_vdr_report(inp)
    b = generate_vdr_report(inp)
    assert a.rendered == b.rendered


# --- JSON output shape ---------------------------------------------------


def test_json_output_includes_schema_version_and_rfc_reference() -> None:
    """Schema version pin is load-bearing: when RFC-0012 finalizes and we
    revise the shape, consumers detect the break via this field."""
    result = generate_vdr_report(_input([_clf()]))
    doc = json.loads(result.rendered)
    assert doc["vdr_schema_version"] == VDR_SCHEMA_VERSION
    assert "RFC-0012" in doc["rfc_reference"]


def test_json_output_includes_entry_count_and_entries_list() -> None:
    classifications = [
        _clf("KSI-SVC-VRI", status="partial"),
        _clf("KSI-IAM-MFA", status="not_implemented"),
    ]
    result = generate_vdr_report(_input(classifications))
    doc = json.loads(result.rendered)
    assert doc["entry_count"] == 2
    assert len(doc["entries"]) == 2


def test_json_output_includes_draft_notice() -> None:
    """Every VDR artifact carries a DRAFT notice so a reviewer can't
    accidentally treat it as ready-for-submission."""
    result = generate_vdr_report(_input([_clf()]))
    doc = json.loads(result.rendered)
    assert "DRAFT" in doc["_draft_notice"]
    assert "RFC-0012" in doc["_draft_notice"]


# --- Markdown output shape -----------------------------------------------


def test_markdown_output_has_header_summary_and_entries_sections() -> None:
    result = generate_vdr_report(
        _input(
            [_clf("KSI-SVC-VRI", status="not_implemented")],
            output_format="markdown",
        )
    )
    md = result.rendered
    assert "# VDR — fedramp-20x-moderate" in md
    assert VDR_SCHEMA_VERSION in md
    assert "RFC-0012" in md
    assert "## Summary" in md
    assert "## Entries" in md
    assert "KSI-SVC-VRI" in md
    # Summary table has the right columns.
    assert "| Internal ID | KSI | Severity | Internet-reachable |" in md


def test_markdown_empty_workspace_shows_no_open_entries() -> None:
    """Empty input produces a clean message — no malformed empty table."""
    result = generate_vdr_report(_input([], output_format="markdown"))
    assert result.entry_count == 0
    assert "_No open VDR entries._" in result.rendered


# --- Skipped-unknown KSI posture -----------------------------------------


def test_unknown_ksi_skipped_not_fabricated() -> None:
    """Same posture as POA&M and FRMR attestation: unknown KSI ids
    are reported separately, never fabricated into entries."""
    inp = GenerateVdrReportInput(
        classifications=[
            _clf("KSI-SVC-VRI", status="partial"),
            _clf("KSI-FAKE-XYZ", status="not_implemented"),
        ],
        indicators={"KSI-SVC-VRI": _ind("KSI-SVC-VRI")},  # KSI-FAKE-XYZ deliberately absent
        baseline_id="fedramp-20x-moderate",
        frmr_version="0.9.43-beta",
        generated_at=datetime(2026, 5, 19, 12, 0, 0, tzinfo=UTC),
    )
    result = generate_vdr_report(inp)
    assert result.entry_count == 1
    assert result.skipped_unknown_ksi == ["KSI-FAKE-XYZ"]


# --- CVE field population -------------------------------------------------


def test_cve_ids_carried_through_when_present_in_input() -> None:
    """v0.1.162 ships the CVE field; population from Security Hub
    findings lands in v0.1.163. Verify the field WORKS when populated
    so that v0.1.163 wiring is just an upstream change."""
    inp = _input([_clf(cve_ids=["CVE-2024-12345", "CVE-2025-67890"])])
    result = generate_vdr_report(inp)
    assert result.entries[0].cve_ids == ["CVE-2024-12345", "CVE-2025-67890"]


def test_cve_ids_default_empty_for_iac_detector_evidence() -> None:
    """IaC detectors don't emit CVE references today — the VDR entry
    just has an empty CVE list. Not an error; the entry is still valid."""
    result = generate_vdr_report(_input([_clf()]))
    assert result.entries[0].cve_ids == []


# --- Determinism stress test ---------------------------------------------


def test_repeat_invocation_yields_stable_entry_ids() -> None:
    """Internal id must be stable across runs so consumers tracking
    a specific VDR entry across re-runs can find it (e.g., ticket
    linkage). VDR-<ksi>-<idx> meets this — idx is stable because the
    sort is deterministic."""
    inp = _input(
        [
            _clf("KSI-SVC-PRR", status="partial"),
            _clf("KSI-SVC-VRI", status="not_implemented"),
        ]
    )
    a = generate_vdr_report(inp)
    b = generate_vdr_report(inp)
    assert [e.internal_id for e in a.entries] == [e.internal_id for e in b.entries]


# --- Format selection ----------------------------------------------------


def test_output_format_json_returns_json_body() -> None:
    result = generate_vdr_report(_input([_clf()], output_format="json"))
    assert result.output_format == "json"
    # Should parse as JSON.
    json.loads(result.rendered)


def test_output_format_markdown_returns_markdown_body() -> None:
    result = generate_vdr_report(_input([_clf()], output_format="markdown"))
    assert result.output_format == "markdown"
    # Should NOT parse as JSON.
    with pytest.raises(json.JSONDecodeError):
        json.loads(result.rendered)


# --- Boundary-excluded counter --------------------------------------------


def test_out_of_boundary_count_surfaces_in_json_header() -> None:
    """Parallel to POA&M: surface the boundary-driven exclusion count on
    the artifact itself so a 3PAO reading the VDR sees scope context."""
    inp = GenerateVdrReportInput(
        classifications=[_clf()],
        indicators={"KSI-SVC-VRI": _ind("KSI-SVC-VRI")},
        baseline_id="fedramp-20x-moderate",
        frmr_version="0.9.43-beta",
        generated_at=datetime(2026, 5, 19, 12, 0, 0, tzinfo=UTC),
        out_of_boundary_excluded_count=4,
    )
    result = generate_vdr_report(inp)
    doc = json.loads(result.rendered)
    assert doc["out_of_boundary_excluded_count"] == 4


def test_out_of_boundary_count_surfaces_in_markdown_header() -> None:
    inp = GenerateVdrReportInput(
        classifications=[_clf()],
        indicators={"KSI-SVC-VRI": _ind("KSI-SVC-VRI")},
        baseline_id="fedramp-20x-moderate",
        frmr_version="0.9.43-beta",
        generated_at=datetime(2026, 5, 19, 12, 0, 0, tzinfo=UTC),
        out_of_boundary_excluded_count=4,
        output_format="markdown",
    )
    result = generate_vdr_report(inp)
    assert "Excluded as out-of-boundary" in result.rendered
    assert "4 item(s)" in result.rendered
