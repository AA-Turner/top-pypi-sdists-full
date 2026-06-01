"""Tests for v0.1.113 M1 Stage 1 — Security Hub ASFF ingestion."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from efterlev.imports.security_hub import (
    AsffFinding,
    AsffMapping,
    IngestSecurityHubInput,
    ingest_security_hub,
    load_asff_mapping,
    parse_asff_document,
)
from efterlev.imports.security_hub.parser import AsffParseError

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_FIXTURE = REPO_ROOT / "evals/fixtures/security-hub-asff-sample/findings.json"


# --- Parser ----------------------------------------------------------------


def test_parse_sample_fixture() -> None:
    """Parser handles the vendored sample (Findings-key shape)."""
    findings = parse_asff_document(SAMPLE_FIXTURE)
    assert len(findings) == 4
    generator_ids = {f.GeneratorId for f in findings}
    assert "aws-foundational-security-best-practices/v/1.0.0/EC2.2" in generator_ids
    assert "aws-foundational-security-best-practices/v/1.0.0/UNMAPPED.99" in generator_ids


def test_parser_handles_bare_array(tmp_path: Path) -> None:
    """Top-level array is the EventBridge-export shape; parser accepts it."""
    bare = [
        {
            "Id": "arn:aws:securityhub::1:finding/x",
            "ProductArn": "arn:aws:securityhub:::product/aws/securityhub",
            "GeneratorId": "test/g/1",
            "Title": "t",
            "Description": "d",
        }
    ]
    p = tmp_path / "bare.json"
    p.write_text(json.dumps(bare), encoding="utf-8")
    findings = parse_asff_document(p)
    assert len(findings) == 1


def test_parser_skips_findings_missing_required_fields(tmp_path: Path) -> None:
    """Soft schema drift in the wild: skip un-validatable, don't abort."""
    doc = {
        "Findings": [
            {
                # missing Id, GeneratorId, etc.
                "Title": "broken",
            },
            {
                "Id": "arn:x",
                "ProductArn": "arn:p",
                "GeneratorId": "g/1",
                "Title": "ok",
                "Description": "d",
            },
        ]
    }
    p = tmp_path / "mixed.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    findings = parse_asff_document(p)
    assert len(findings) == 1
    assert findings[0].Title == "ok"


def test_parser_rejects_invalid_json(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("not json", encoding="utf-8")
    with pytest.raises(AsffParseError):
        parse_asff_document(p)


def test_parser_rejects_unknown_top_level_shape(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"NotFindings": []}), encoding="utf-8")
    with pytest.raises(AsffParseError):
        parse_asff_document(p)


def test_finding_compliance_status_property() -> None:
    f = AsffFinding(
        Id="x",
        ProductArn="p",
        GeneratorId="g/1",
        Title="t",
        Description="d",
        Compliance={"Status": "FAILED"},
        Severity={"Label": "HIGH"},
    )
    assert f.compliance_status == "FAILED"
    assert f.severity_label == "HIGH"


def test_finding_compliance_status_unknown_returns_none() -> None:
    f = AsffFinding(
        Id="x",
        ProductArn="p",
        GeneratorId="g/1",
        Title="t",
        Description="d",
        Compliance={"Status": "BOGUS"},
    )
    assert f.compliance_status is None


def test_finding_cve_ids_property_v0_1_163() -> None:
    """v0.1.163 / #368: parser harvests CVE IDs from ASFF
    Vulnerabilities[] so the VDR generator can thread them into the
    RFC-0012 `cve_ids` field on each entry."""
    f = AsffFinding(
        Id="x",
        ProductArn="p",
        GeneratorId="g/1",
        Title="t",
        Description="d",
        Vulnerabilities=[
            {"Id": "CVE-2024-12345", "Cvss": [{"Version": "3.1"}]},
            {"Id": "CVE-2025-67890"},
        ],
    )
    assert f.cve_ids == ["CVE-2024-12345", "CVE-2025-67890"]


def test_finding_cve_ids_default_empty_when_no_vulnerabilities() -> None:
    """The majority of compliance-control findings have no
    Vulnerabilities[] block — empty list is the correct default."""
    f = AsffFinding(
        Id="x",
        ProductArn="p",
        GeneratorId="g/1",
        Title="t",
        Description="d",
    )
    assert f.cve_ids == []


def test_finding_cve_ids_dedupes_across_repeated_entries() -> None:
    """Defensive: ASFF spec allows but doesn't forbid repeated CVE
    entries; downstream VDR consumers expect a deduped list so the
    same CVE doesn't show up twice in one entry."""
    f = AsffFinding(
        Id="x",
        ProductArn="p",
        GeneratorId="g/1",
        Title="t",
        Description="d",
        Vulnerabilities=[
            {"Id": "CVE-2024-12345"},
            {"Id": "CVE-2024-12345"},  # dup
            {"Id": "CVE-2025-67890"},
        ],
    )
    assert f.cve_ids == ["CVE-2024-12345", "CVE-2025-67890"]


def test_finding_cve_ids_ignores_malformed_entries() -> None:
    """ASFF input might be sloppy. Don't crash on a missing/non-string
    Id; just skip the entry."""
    f = AsffFinding(
        Id="x",
        ProductArn="p",
        GeneratorId="g/1",
        Title="t",
        Description="d",
        Vulnerabilities=[
            {"Id": "CVE-2024-1"},
            {"NoId": "huh"},
            {"Id": 12345},  # not a string
            {"Id": "CVE-2024-2"},
        ],
    )
    assert f.cve_ids == ["CVE-2024-1", "CVE-2024-2"]


# --- Mapping ---------------------------------------------------------------


def test_mapping_loads_vendored_yaml() -> None:
    mapping = load_asff_mapping()
    assert isinstance(mapping, AsffMapping)
    # v0.1.113 ships 5 initial mappings.
    # Floor: 13 entries at v0.1.121 (5 initial v0.1.113 + 8 batch v0.1.121).
    # Future expansion can raise this floor; the >= keeps the test robust to
    # additive changes without false positives on every batch.
    assert len(mapping.mappings) >= 13


def test_mapping_lookup_hits() -> None:
    mapping = load_asff_mapping()
    entry = mapping.lookup("aws-foundational-security-best-practices/v/1.0.0/EC2.2")
    assert entry is not None
    assert "KSI-CNA-RNT" in entry.ksis
    assert "sc-7" in entry.controls


def test_mapping_lookup_unknown_returns_none() -> None:
    mapping = load_asff_mapping()
    assert mapping.lookup("nonexistent/g/1") is None


# --- Ingest ----------------------------------------------------------------


def test_ingest_emits_evidence_for_mapped_findings() -> None:
    """Sample fixture: 3 mapped findings → 3 Evidence records."""
    out = ingest_security_hub(IngestSecurityHubInput(asff_path=SAMPLE_FIXTURE))
    assert out.findings_total == 4
    assert out.findings_emitted == 3
    assert len(out.evidence) == 3
    # Unmapped one should be reported.
    assert out.skipped_unmapped_generator_ids == [
        "aws-foundational-security-best-practices/v/1.0.0/UNMAPPED.99"
    ]


def test_ingest_evidence_carries_asff_metadata() -> None:
    out = ingest_security_hub(IngestSecurityHubInput(asff_path=SAMPLE_FIXTURE))
    ec2_evidence = [e for e in out.evidence if e.detector_id.endswith("EC2.2")]
    assert len(ec2_evidence) == 1
    e = ec2_evidence[0]
    assert "KSI-CNA-RNT" in e.ksis_evidenced
    assert e.content["asff_compliance_status"] == "FAILED"
    assert e.content["asff_generator_id"] == (
        "aws-foundational-security-best-practices/v/1.0.0/EC2.2"
    )
    assert e.content["import_source"] == "aws.security_hub.asff"


def test_ingest_passed_compliance_emits_evidence() -> None:
    """PASSED findings flow through too — Gap Agent sees both signals."""
    out = ingest_security_hub(IngestSecurityHubInput(asff_path=SAMPLE_FIXTURE))
    passed = [e for e in out.evidence if e.content["asff_compliance_status"] == "PASSED"]
    # IAM.6 + CloudTrail.1 both PASSED in the fixture.
    assert len(passed) == 2


def test_ingest_with_mapping_override(tmp_path: Path) -> None:
    """Mapping override is the test seam for unit-testing without yaml."""
    mapping = AsffMapping(
        mappings=[
            {
                "generator_id": "test/g/1",
                "title": "Test",
                "ksis": ["KSI-X"],
                "controls": ["xx-1"],
            }
        ]
    )
    doc = {
        "Findings": [
            {
                "Id": "arn:x",
                "ProductArn": "arn:p",
                "GeneratorId": "test/g/1",
                "Title": "t",
                "Description": "d",
                "Compliance": {"Status": "FAILED"},
            }
        ]
    }
    p = tmp_path / "asff.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    out = ingest_security_hub(IngestSecurityHubInput(asff_path=p, mapping_override=mapping))
    assert out.findings_emitted == 1
    assert out.evidence[0].ksis_evidenced == ["KSI-X"]


def test_ingest_skips_not_available_status(tmp_path: Path) -> None:
    """NOT_AVAILABLE findings carry no signal; skip + count."""
    mapping = AsffMapping(
        mappings=[
            {
                "generator_id": "test/g/1",
                "title": "Test",
                "ksis": ["KSI-X"],
                "controls": ["xx-1"],
            }
        ]
    )
    doc = {
        "Findings": [
            {
                "Id": "arn:x",
                "ProductArn": "arn:p",
                "GeneratorId": "test/g/1",
                "Title": "t",
                "Description": "d",
                "Compliance": {"Status": "NOT_AVAILABLE"},
            }
        ]
    }
    p = tmp_path / "asff.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    out = ingest_security_hub(IngestSecurityHubInput(asff_path=p, mapping_override=mapping))
    assert out.findings_emitted == 0
    assert out.skipped_status_not_available == 1
