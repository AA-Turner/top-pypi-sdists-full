"""Fixture-driven tests for `aws.svc_at_rest_encryption_coverage`."""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.svc_at_rest_encryption_coverage.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "svc_at_rest_encryption_coverage"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_dynamodb_with_cmk_emits_configured_with_cmk_detail() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "dynamodb_with_cmk.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.svc_at_rest_encryption_coverage"
    assert ev.ksis_evidenced == ["KSI-SVC-PRR"]
    assert ev.controls_evidenced == ["SC-4"]
    assert ev.content["resource_type"] == "aws_dynamodb_table"
    assert ev.content["encryption_state"] == "configured"
    assert ev.content["pattern"] == "at_rest_encryption"
    assert ev.content.get("detail") == "cmk=true"


def test_efs_encrypted_with_cmk_emits_configured() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "efs_encrypted.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_efs_file_system"
    assert ev.content["encryption_state"] == "configured"
    assert ev.content.get("detail") == "cmk=true"


def test_elasticache_replication_group_emits_configured() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "elasticache_encrypted.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_elasticache_replication_group"
    assert ev.content["encryption_state"] == "configured"


def test_aurora_cluster_emits_configured_with_cmk() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "aurora_cluster_encrypted.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_rds_cluster"
    assert ev.content["encryption_state"] == "configured"
    assert ev.content.get("detail") == "cmk=true"


# --- should_not_match (negative-evidence + ignored cases) ---------------------


def test_elasticache_cluster_without_encryption_emits_absent() -> None:
    """`at_rest_encryption_enabled` flag missing → negative evidence."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "elasticache_unencrypted.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_elasticache_cluster"
    assert ev.content["encryption_state"] == "absent"
    assert "at_rest_encryption_enabled" in ev.content["gap"]


def test_efs_explicit_false_emits_absent() -> None:
    """`encrypted = false` → negative evidence."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "efs_unencrypted.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "scratch"
    assert ev.content["encryption_state"] == "absent"
    assert "encrypted" in ev.content["gap"]


def test_no_data_resources_emits_no_evidence() -> None:
    """Workspaces with no data-store resources → no evidence emitted."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "no_data_resources.tf")
    assert results == []


# --- contract pins ------------------------------------------------------------


def test_detector_declares_expected_mappings() -> None:
    from efterlev.detectors.base import _REGISTRY

    spec = _REGISTRY.get("aws.svc_at_rest_encryption_coverage")
    assert spec is not None
    assert list(spec.ksis) == ["KSI-SVC-PRR"]
    assert list(spec.controls) == ["SC-4"]


def test_detector_emits_only_documented_states() -> None:
    """Lock the schema: encryption_state in {configured, absent}."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.tf"))
    seen = set()
    for f in fixtures:
        for ev in _run(f):
            seen.add(ev.content.get("encryption_state"))
    assert seen <= {"configured", "absent"}, (
        f"detector emitted unexpected encryption_state values: {seen}"
    )
