"""Fixture-driven tests for `aws.mla_log_access_least_privilege`."""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.mla_log_access_least_privilege.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "mla_log_access_least_privilege"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_explicit_resource_policy_emits_configured_evidence() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "explicit_resource_policy.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.mla_log_access_least_privilege"
    assert ev.ksis_evidenced == ["KSI-MLA-ALA"]
    assert set(ev.controls_evidenced) == {"AC-3", "AC-6"}
    assert ev.content["resource_type"] == "aws_cloudwatch_log_resource_policy"
    assert ev.content["log_access_state"] == "configured"
    assert ev.content["pattern"] == "explicit_resource_policy"


def test_scoped_iam_policy_emits_scoped_evidence() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "scoped_iam_policy.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_iam_policy"
    assert ev.content["resource_name"] == "audit_log_reader"
    assert ev.content["log_access_state"] == "scoped"
    assert ev.content["pattern"] == "iam_policy_with_logs_actions"
    assert "log_statements=1" in ev.content["detail"]


def test_scoped_via_data_source_resolves_and_emits_scoped() -> None:
    """`policy = data.aws_iam_policy_document.X.json` resolves through
    the data-source registry."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "scoped_via_data_source.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "log_reader"
    assert ev.content["log_access_state"] == "scoped"


# --- should_not_match (negative-evidence + ignored cases) ---------------------


def test_overly_permissive_iam_policy_emits_negative_evidence() -> None:
    """`logs:*` on `Resource: "*"` → overly_permissive negative evidence."""
    results = _run(
        DETECTOR_DIR / "fixtures" / "should_not_match" / "overly_permissive_iam_policy.tf"
    )
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "log_admin"
    assert ev.content["log_access_state"] == "overly_permissive"
    assert "logs:*" in ev.content["gap"]
    assert "no scoping" in ev.content["gap"]


def test_overly_permissive_via_data_source_emits_negative_evidence() -> None:
    """Same negative pattern via aws_iam_policy_document data source."""
    results = _run(
        DETECTOR_DIR / "fixtures" / "should_not_match" / "overly_permissive_via_data_source.tf"
    )
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "log_admin_via_doc"
    assert ev.content["log_access_state"] == "overly_permissive"


def test_no_logs_actions_emits_no_evidence() -> None:
    """IAM policies with no `logs:` actions are ignored — they're
    not relevant to KSI-MLA-ALA."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "no_logs_actions.tf")
    assert results == []


# --- contract pins ------------------------------------------------------------


def test_detector_declares_expected_mappings() -> None:
    from efterlev.detectors.base import _REGISTRY

    spec = _REGISTRY.get("aws.mla_log_access_least_privilege")
    assert spec is not None, "detector did not register"
    assert list(spec.ksis) == ["KSI-MLA-ALA"]
    assert set(spec.controls) == {"AC-3", "AC-6"}


def test_detector_emits_only_documented_states() -> None:
    """Lock the evidence schema: every emitted record must have
    log_access_state in {configured, scoped, overly_permissive,
    unparseable}."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.tf"))
    seen = set()
    for f in fixtures:
        for ev in _run(f):
            seen.add(ev.content.get("log_access_state"))
    assert seen <= {"configured", "scoped", "overly_permissive", "unparseable"}, (
        f"detector emitted unexpected log_access_state values: {seen}"
    )


def test_detector_emits_only_documented_patterns() -> None:
    """Lock the schema: pattern in {explicit_resource_policy,
    iam_policy_with_logs_actions}."""
    fixtures = list((DETECTOR_DIR / "fixtures").rglob("*.tf"))
    seen = set()
    for f in fixtures:
        for ev in _run(f):
            seen.add(ev.content.get("pattern"))
    assert seen <= {"explicit_resource_policy", "iam_policy_with_logs_actions"}, (
        f"detector emitted unexpected pattern values: {seen}"
    )
