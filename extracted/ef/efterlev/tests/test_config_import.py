"""Tests for v0.1.114 M1 Stage 3 — AWS Config evaluations ingestion."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from efterlev.imports.config import (
    ConfigEvaluation,
    ConfigMapping,
    IngestConfigInput,
    ingest_config,
    load_config_mapping,
    parse_config_document,
)
from efterlev.imports.config.parser import ConfigParseError

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_FIXTURE = REPO_ROOT / "evals/fixtures/config-evaluations-sample/evaluations.json"


# --- Parser ----------------------------------------------------------------


def test_parse_sample_fixture() -> None:
    """Parser handles the vendored sample (EvaluationResults-key shape)."""
    evaluations = parse_config_document(SAMPLE_FIXTURE)
    assert len(evaluations) == 5
    rule_names = {e.config_rule_name for e in evaluations}
    assert "encrypted-volumes" in rule_names
    assert "custom-unmapped-rule" in rule_names


def test_parser_handles_bare_array(tmp_path: Path) -> None:
    """Top-level array is the EventBridge-export shape; parser accepts it."""
    bare = [
        {
            "EvaluationResultIdentifier": {
                "EvaluationResultQualifier": {
                    "ConfigRuleName": "test-rule",
                    "ResourceType": "AWS::EC2::Instance",
                    "ResourceId": "i-x",
                }
            },
            "ComplianceType": "COMPLIANT",
        }
    ]
    p = tmp_path / "bare.json"
    p.write_text(json.dumps(bare), encoding="utf-8")
    evaluations = parse_config_document(p)
    assert len(evaluations) == 1


def test_parser_skips_evaluations_missing_required(tmp_path: Path) -> None:
    """Soft schema drift handling — skip un-validatable, don't abort."""
    doc = {
        "EvaluationResults": [
            {"EvaluationResultIdentifier": {}},  # malformed
            {
                "EvaluationResultIdentifier": {
                    "EvaluationResultQualifier": {
                        "ConfigRuleName": "ok-rule",
                        "ResourceType": "AWS::EC2::Instance",
                        "ResourceId": "i-x",
                    }
                },
                "ComplianceType": "COMPLIANT",
            },
        ]
    }
    p = tmp_path / "mixed.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    evaluations = parse_config_document(p)
    assert len(evaluations) == 1
    assert evaluations[0].config_rule_name == "ok-rule"


def test_parser_rejects_invalid_json(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("not json", encoding="utf-8")
    with pytest.raises(ConfigParseError):
        parse_config_document(p)


def test_parser_rejects_unknown_top_level_shape(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"NotEvaluationResults": []}), encoding="utf-8")
    with pytest.raises(ConfigParseError):
        parse_config_document(p)


def test_evaluation_property_accessors() -> None:
    e = ConfigEvaluation.model_validate(
        {
            "EvaluationResultIdentifier": {
                "EvaluationResultQualifier": {
                    "ConfigRuleName": "r",
                    "ResourceType": "T",
                    "ResourceId": "i",
                }
            },
            "ComplianceType": "NON_COMPLIANT",
        }
    )
    assert e.config_rule_name == "r"
    assert e.resource_type == "T"
    assert e.resource_id == "i"


# --- Mapping ---------------------------------------------------------------


def test_mapping_loads_vendored_yaml() -> None:
    mapping = load_config_mapping()
    assert isinstance(mapping, ConfigMapping)
    # Floor: 13 entries at v0.1.122 (5 initial v0.1.114 + 8 batch v0.1.122).
    assert len(mapping.mappings) >= 13


def test_mapping_lookup_hits() -> None:
    mapping = load_config_mapping()
    entry = mapping.lookup("encrypted-volumes")
    assert entry is not None
    assert "KSI-CNA-OFA" in entry.ksis


def test_mapping_lookup_unknown_returns_none() -> None:
    mapping = load_config_mapping()
    assert mapping.lookup("nonexistent-rule") is None


# --- Ingest ----------------------------------------------------------------


def test_ingest_emits_evidence_for_mapped_evaluations() -> None:
    """Sample fixture: 4 mapped → 4 Evidence records."""
    out = ingest_config(IngestConfigInput(config_path=SAMPLE_FIXTURE))
    assert out.evaluations_total == 5
    assert out.evaluations_emitted == 4
    assert len(out.evidence) == 4
    assert out.skipped_unmapped_config_rule_names == ["custom-unmapped-rule"]


def test_ingest_evidence_carries_config_metadata() -> None:
    out = ingest_config(IngestConfigInput(config_path=SAMPLE_FIXTURE))
    encrypted = [e for e in out.evidence if "encrypted-volumes" in e.detector_id]
    assert len(encrypted) == 1
    e = encrypted[0]
    assert "KSI-CNA-OFA" in e.ksis_evidenced
    assert e.content["config_compliance_type"] == "NON_COMPLIANT"
    assert e.content["import_source"] == "aws.config.evaluations"
    assert e.content["config_resource_type"] == "AWS::EC2::Volume"


def test_ingest_with_mapping_override(tmp_path: Path) -> None:
    """Mapping override is the test seam for unit-testing without yaml."""
    mapping = ConfigMapping(
        mappings=[
            {
                "config_rule_name": "test-rule",
                "title": "Test",
                "ksis": ["KSI-X"],
                "controls": ["xx-1"],
            }
        ]
    )
    doc = {
        "EvaluationResults": [
            {
                "EvaluationResultIdentifier": {
                    "EvaluationResultQualifier": {
                        "ConfigRuleName": "test-rule",
                        "ResourceType": "T",
                        "ResourceId": "i",
                    }
                },
                "ComplianceType": "COMPLIANT",
            }
        ]
    }
    p = tmp_path / "config.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    out = ingest_config(IngestConfigInput(config_path=p, mapping_override=mapping))
    assert out.evaluations_emitted == 1
    assert out.evidence[0].ksis_evidenced == ["KSI-X"]


def test_ingest_skips_insufficient_data(tmp_path: Path) -> None:
    """INSUFFICIENT_DATA evaluations carry no signal; skip + count."""
    mapping = ConfigMapping(
        mappings=[
            {
                "config_rule_name": "test-rule",
                "title": "Test",
                "ksis": ["KSI-X"],
                "controls": ["xx-1"],
            }
        ]
    )
    doc = {
        "EvaluationResults": [
            {
                "EvaluationResultIdentifier": {
                    "EvaluationResultQualifier": {
                        "ConfigRuleName": "test-rule",
                        "ResourceType": "T",
                        "ResourceId": "i",
                    }
                },
                "ComplianceType": "INSUFFICIENT_DATA",
            }
        ]
    }
    p = tmp_path / "config.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    out = ingest_config(IngestConfigInput(config_path=p, mapping_override=mapping))
    assert out.evaluations_emitted == 0
    assert out.skipped_insufficient_data == 1
