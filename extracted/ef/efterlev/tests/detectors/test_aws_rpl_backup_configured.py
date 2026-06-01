"""Fixture-driven tests for `aws.rpl_backup_configured`."""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.rpl_backup_configured.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "rpl_backup_configured"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_backup_plan_with_copy_actions_emits_rule_and_copy_counts() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "backup_plan_with_copy_actions.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.rpl_backup_configured"
    assert ev.ksis_evidenced == ["KSI-RPL-ARP"]
    assert set(ev.controls_evidenced) == {"CP-7", "CP-10"}
    assert ev.content["resource_type"] == "aws_backup_plan"
    assert ev.content["recovery_state"] == "configured"
    assert ev.content["pattern"] == "backup_plan"
    # 2 rules total, 1 copy_action (only on the daily-prod rule)
    assert "rules=2" in ev.content["detail"]
    assert "copy_actions=1" in ev.content["detail"]


def test_backup_vault_with_cmk_emits_cmk_detail() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "backup_vault_with_cmk.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_backup_vault"
    assert ev.content["pattern"] == "backup_vault"
    assert ev.content.get("detail") == "cmk=true"


def test_backup_selection_emits_selection_pattern() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "backup_selection.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_backup_selection"
    assert ev.content["pattern"] == "backup_selection"


def test_rds_cross_region_replication_emits_pattern_with_source() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "rds_cross_region_replication.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_db_instance_automated_backups_replication"
    assert ev.content["pattern"] == "rds_cross_region_replication"
    assert "rds:us-east-1" in ev.content["detail"]


# --- should_not_match ---------------------------------------------------------


def test_no_backup_resources_emits_no_evidence() -> None:
    """RDS + S3 only (covered by existing backup_retention_configured)
    → no evidence from THIS detector."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "no_backup_resources.tf")
    assert results == []


# --- contract pins ------------------------------------------------------------


def test_detector_declares_expected_mappings() -> None:
    from efterlev.detectors.base import _REGISTRY

    spec = _REGISTRY.get("aws.rpl_backup_configured")
    assert spec is not None
    assert list(spec.ksis) == ["KSI-RPL-ARP"]
    assert set(spec.controls) == {"CP-7", "CP-10"}


def test_detector_emits_only_documented_patterns() -> None:
    """Lock the schema: pattern in {backup_plan, backup_vault,
    backup_selection, rds_cross_region_replication}."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.tf"))
    seen = set()
    for f in fixtures:
        for ev in _run(f):
            seen.add(ev.content.get("pattern"))
    assert seen <= {
        "backup_plan",
        "backup_vault",
        "backup_selection",
        "rds_cross_region_replication",
    }, f"detector emitted unexpected pattern values: {seen}"


def test_detector_emits_only_configured_state() -> None:
    """Positive-only emission. Negative path is intentionally absent —
    absence of AWS Backup isn't a gap per se."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.tf"))
    seen = set()
    for f in fixtures:
        for ev in _run(f):
            seen.add(ev.content.get("recovery_state"))
    assert seen <= {"configured"}, (
        f"detector emitted recovery_state values other than 'configured': {seen}. "
        f"v0.1.33 contract: positive-only. Adding negatives needs a design entry."
    )


def test_detector_does_not_overlap_with_backup_retention_configured() -> None:
    """Verify this detector handles ONLY the AWS Backup orchestration +
    cross-region replication resources — none of the resource types
    covered by `aws.backup_retention_configured` (RDS, S3 versioning)."""
    from efterlev.detectors.aws.backup_retention_configured.detector import (
        detect as retention_detect,
    )

    # The no-backup-resources fixture has aws_db_instance + aws_s3_bucket;
    # backup_retention_configured may emit evidence on it, but this detector
    # must not.
    fixture = DETECTOR_DIR / "fixtures" / "should_not_match" / "no_backup_resources.tf"
    assert _run(fixture) == []
    # Sanity: the existing retention detector DOES see these resources.
    retention_results = retention_detect(parse_terraform_file(fixture))
    assert len(retention_results) >= 1, (
        "fixture should produce evidence on the retention detector "
        "(otherwise the no-overlap test isn't proving anything)"
    )
