"""Fixture-driven tests for `aws.cna_optimizing_for_availability`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.cna_optimizing_for_availability.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "cna_optimizing_for_availability"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_db_multi_az_emits_configured_evidence() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "db_multi_az.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.cna_optimizing_for_availability"
    assert ev.ksis_evidenced == ["KSI-CNA-OFA"]
    assert ev.controls_evidenced == []
    assert ev.content["resource_type"] == "aws_db_instance"
    assert ev.content["resource_name"] == "primary"
    assert ev.content["availability_state"] == "configured"
    assert ev.content["pattern"] == "multi_az"


def test_db_read_replica_emits_replica_pattern() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "db_read_replica.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["availability_state"] == "configured"
    assert ev.content["pattern"] == "read_replica"
    assert "replicate_source_db=app-prod" in ev.content["detail"]


def test_asg_multi_az_emits_configured_evidence() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "asg_multi_az.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_autoscaling_group"
    assert ev.content["availability_state"] == "configured"
    assert ev.content["pattern"] == "asg_multi_az"
    assert "3 subnets" in ev.content["detail"]


def test_aurora_multi_az_emits_configured_evidence() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "aurora_multi_az.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_rds_cluster"
    assert ev.content["pattern"] == "multi_az"
    assert "availability_zones=3" in ev.content["detail"]


def test_s3_replication_emits_configured_evidence() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "s3_replication.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_s3_bucket_replication_configuration"
    assert ev.content["pattern"] == "s3_replication"
    assert ev.content["availability_state"] == "configured"


def test_ecs_spread_emits_configured_evidence() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "ecs_spread.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_ecs_service"
    assert ev.content["pattern"] == "ecs_service_spread"
    assert ev.content["availability_state"] == "configured"


# --- should_not_match ---------------------------------------------------------


def test_db_single_az_emits_absent_evidence() -> None:
    """multi_az = false on aws_db_instance → negative evidence."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "db_single_az.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "lonely"
    assert ev.content["availability_state"] == "absent"
    assert ev.content["pattern"] == "multi_az"
    assert "without multi_az=true" in ev.content["gap"]


def test_asg_single_subnet_emits_absent_evidence() -> None:
    """ASG referencing only 1 subnet → negative evidence (single-AZ)."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "asg_single_subnet.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_autoscaling_group"
    assert ev.content["availability_state"] == "absent"
    assert "1 subnet" in ev.content["gap"]


def test_no_availability_resources_emits_no_evidence() -> None:
    """Workspace with no DB/ASG/replication/ECS resources → no evidence."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "no_availability_resources.tf")
    assert results == []


# --- contract pins ------------------------------------------------------------


def test_detector_declares_no_800_53_controls() -> None:
    """KSI-CNA-OFA has no mapped 800-53 controls in FRMR 0.9.43-beta;
    the @detector decorator should declare controls=[] explicitly to
    avoid silently asserting unmapped control coverage."""
    from efterlev.detectors.base import _REGISTRY

    spec = _REGISTRY.get("aws.cna_optimizing_for_availability")
    assert spec is not None, "detector did not register"
    assert list(spec.controls) == [], (
        f"detector should declare controls=[] (KSI-CNA-OFA has no FRMR-mapped "
        f"controls); got {spec.controls!r}"
    )
    assert list(spec.ksis) == ["KSI-CNA-OFA"]


def test_detector_emits_only_configured_or_absent_state() -> None:
    """Lock the evidence schema: every emitted record must have
    availability_state in {configured, absent} — no other values."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.tf"))
    seen_states = set()
    for f in fixtures:
        for ev in _run(f):
            seen_states.add(ev.content.get("availability_state"))
    assert seen_states <= {"configured", "absent"}, (
        f"detector emitted unexpected availability_state values: {seen_states}"
    )
