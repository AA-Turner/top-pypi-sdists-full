"""Tests for v0.1.123 M1 Stage 5 — Prowler ingestion."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from efterlev.imports.prowler import (
    IngestProwlerInput,
    ProwlerFinding,
    ProwlerMapping,
    ingest_prowler,
    load_prowler_mapping,
    parse_prowler_document,
)
from efterlev.imports.prowler.parser import ProwlerParseError

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_FIXTURE = REPO_ROOT / "evals/fixtures/prowler-sample/findings.json"


# --- Parser ----------------------------------------------------------------


def test_parse_sample_fixture() -> None:
    """Parser handles the vendored sample (top-level array shape)."""
    findings = parse_prowler_document(SAMPLE_FIXTURE)
    assert len(findings) == 6
    check_ids = {f.CheckID for f in findings}
    assert "ec2_securitygroup_default_restrict_traffic" in check_ids
    assert "iam_unused_credentials_review" in check_ids


def test_parser_handles_findings_key_shape(tmp_path: Path) -> None:
    """The {"findings": [...]} wrapper shape works too."""
    doc = {
        "findings": [
            {
                "CheckID": "test_check",
                "Status": "PASS",
                "CheckTitle": "t",
                "ServiceName": "test",
            }
        ]
    }
    p = tmp_path / "prowler.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    findings = parse_prowler_document(p)
    assert len(findings) == 1


def test_parser_skips_findings_missing_required_fields(tmp_path: Path) -> None:
    """Soft schema drift: skip un-validatable, don't abort."""
    doc = [
        {"CheckID": "broken"},  # missing Status, CheckTitle, ServiceName
        {"CheckID": "ok", "Status": "PASS", "CheckTitle": "t", "ServiceName": "s"},
    ]
    p = tmp_path / "mixed.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    findings = parse_prowler_document(p)
    assert len(findings) == 1
    assert findings[0].CheckID == "ok"


def test_parser_rejects_invalid_json(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("not json", encoding="utf-8")
    with pytest.raises(ProwlerParseError):
        parse_prowler_document(p)


def test_parser_rejects_unknown_top_level_shape(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"NotFindings": []}), encoding="utf-8")
    with pytest.raises(ProwlerParseError):
        parse_prowler_document(p)


def test_finding_status_literal_validation() -> None:
    f = ProwlerFinding(CheckID="x", Status="PASS", CheckTitle="t", ServiceName="s")
    assert f.Status == "PASS"


# --- Mapping ---------------------------------------------------------------


def test_mapping_loads_vendored_yaml() -> None:
    mapping = load_prowler_mapping()
    assert isinstance(mapping, ProwlerMapping)
    # v0.1.123 ships 8 initial mappings.
    assert len(mapping.mappings) >= 8


def test_mapping_lookup_hits() -> None:
    mapping = load_prowler_mapping()
    entry = mapping.lookup("ec2_securitygroup_default_restrict_traffic")
    assert entry is not None
    assert "KSI-CNA-RNT" in entry.ksis
    assert "sc-7" in entry.controls


def test_mapping_lookup_unknown_returns_none() -> None:
    mapping = load_prowler_mapping()
    assert mapping.lookup("nonexistent_check") is None


# --- Ingest ----------------------------------------------------------------


def test_ingest_emits_evidence_for_mapped_findings() -> None:
    """Sample fixture: 4 mapped → 4 Evidence records (1 MANUAL skipped, 1 unmapped)."""
    out = ingest_prowler(IngestProwlerInput(prowler_path=SAMPLE_FIXTURE))
    assert out.findings_total == 6
    assert out.findings_emitted == 4
    assert out.skipped_manual_status == 1
    assert out.skipped_unmapped_check_ids == ["iam_unused_credentials_review"]


def test_ingest_evidence_carries_prowler_metadata() -> None:
    out = ingest_prowler(IngestProwlerInput(prowler_path=SAMPLE_FIXTURE))
    sg_evidence = [e for e in out.evidence if "ec2_securitygroup" in e.detector_id]
    assert len(sg_evidence) == 1
    e = sg_evidence[0]
    assert "KSI-CNA-RNT" in e.ksis_evidenced
    assert e.content["prowler_status"] == "FAIL"
    assert e.content["prowler_check_id"] == "ec2_securitygroup_default_restrict_traffic"
    assert e.content["import_source"] == "aws.prowler.native"


def test_ingest_with_mapping_override(tmp_path: Path) -> None:
    """Mapping override is the test seam for unit-testing without yaml."""
    mapping = ProwlerMapping(
        mappings=[
            {
                "check_id": "test_check",
                "title": "Test",
                "ksis": ["KSI-X"],
                "controls": ["xx-1"],
            }
        ]
    )
    doc = [
        {
            "CheckID": "test_check",
            "Status": "FAIL",
            "CheckTitle": "t",
            "ServiceName": "s",
        }
    ]
    p = tmp_path / "prowler.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    out = ingest_prowler(IngestProwlerInput(prowler_path=p, mapping_override=mapping))
    assert out.findings_emitted == 1
    assert out.evidence[0].ksis_evidenced == ["KSI-X"]


def test_ingest_skips_manual_status(tmp_path: Path) -> None:
    """MANUAL status carries no signal; skip + count."""
    mapping = ProwlerMapping(
        mappings=[
            {
                "check_id": "test_check",
                "title": "Test",
                "ksis": ["KSI-X"],
                "controls": ["xx-1"],
            }
        ]
    )
    doc = [
        {
            "CheckID": "test_check",
            "Status": "MANUAL",
            "CheckTitle": "t",
            "ServiceName": "s",
        }
    ]
    p = tmp_path / "prowler.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    out = ingest_prowler(IngestProwlerInput(prowler_path=p, mapping_override=mapping))
    assert out.findings_emitted == 0
    assert out.skipped_manual_status == 1
