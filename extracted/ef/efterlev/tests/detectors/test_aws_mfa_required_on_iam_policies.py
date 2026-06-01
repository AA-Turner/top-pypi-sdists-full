"""Fixture-driven tests for `aws.mfa_required_on_iam_policies`."""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.mfa_required_on_iam_policies.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "mfa_required_on_iam_policies"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


def test_mfa_gated_policy_emits_present_evidence() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "mfa_gated_policy.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.ksis_evidenced == ["KSI-IAM-MFA"]
    assert ev.controls_evidenced == ["IA-2"]
    assert ev.content["mfa_required"] == "present"
    assert ev.content["allow_statement_count"] == 1


def test_policy_without_mfa_emits_absent_evidence() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "no_mfa_policy.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["mfa_required"] == "absent"
    assert ev.content["allow_statement_count"] == 1
    assert "gap" in ev.content


def test_jsonencode_policy_without_mfa_is_absent() -> None:
    # `jsonencode({...})` is now static-eval'd (python-hcl2 renders the inner
    # object as a Python literal). This fixture is Allow-* with no MFA
    # condition, so it parses to mfa_required="absent" (not "unparseable").
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "jsonencode_policy.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["mfa_required"] == "absent"
    assert "gap" in ev.content


def test_jsonencode_deny_without_mfa_idiom_is_present() -> None:
    # The AWS-recommended deny-without-MFA idiom inside jsonencode: Deny unless
    # aws:MultiFactorAuthPresent. Detector recognizes it as MFA enforcement.
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "jsonencode_deny_mfa.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.ksis_evidenced == ["KSI-IAM-MFA"]
    assert ev.content["mfa_required"] == "present"


def test_no_iam_resources_emits_nothing() -> None:
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "no_iam_resources.tf")
    assert results == []


def test_detector_registered_with_expected_metadata() -> None:
    from efterlev.detectors.base import get_registry

    spec = get_registry()["aws.mfa_required_on_iam_policies"]
    assert spec.ksis == ("KSI-IAM-MFA",)
    assert spec.controls == ("IA-2",)
    assert spec.source == "terraform"


# --- v0.1.10: aws_iam_policy_document data-source resolution ---


def test_data_source_policy_with_mfa_resolves_to_present() -> None:
    """v0.1.10 fix for v0.1.5-0.1.9 carry-forward Bug A. The canonical
    Terraform pattern is `aws_iam_policy_document` data sources rendered
    via `data.X.json` references. Pre-v0.1.10 these were flagged as
    `unparseable`, classifying KSI-IAM-MFA as not_implemented even when
    the policy DID enforce MFA. v0.1.10 walks the data source's HCL
    statement/condition blocks."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "data_source_policy.tf")
    # The detector iterates only `kind="resource"` resources; the data
    # source is consulted as cross-reference, not emitted on its own.
    iam_policy_evidence = [e for e in results if e.content["resource_type"] == "aws_iam_policy"]
    assert len(iam_policy_evidence) == 1
    ev = iam_policy_evidence[0]
    assert ev.content["mfa_required"] == "present"
    assert ev.content["allow_statement_count"] == 1
    # Surface the data source name so reviewers can navigate back to
    # the actual statement block.
    assert ev.content["resolved_via_data_source"] == "platform_admin"
    assert "gap" not in ev.content


def test_data_source_policy_without_mfa_resolves_to_absent() -> None:
    """v0.1.10: a fully-resolvable data source whose statements simply
    don't carry the MFA condition reports `mfa_required: absent` (a
    real gap, not unparseable)."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "data_source_policy_no_mfa.tf")
    iam_policy_evidence = [e for e in results if e.content["resource_type"] == "aws_iam_policy"]
    assert len(iam_policy_evidence) == 1
    ev = iam_policy_evidence[0]
    assert ev.content["mfa_required"] == "absent"
    assert ev.content["resolved_via_data_source"] == "readonly_auditor"
    assert "gap" in ev.content
    assert "MultiFactorAuthPresent" in ev.content["gap"]


def test_data_source_reference_with_no_matching_data_block_unparseable() -> None:
    """If the policy references `data.aws_iam_policy_document.X.json` but
    no `data` block named `X` is in scope (cross-module reference,
    typo, etc.), report `unparseable` with a clear hint."""
    import tempfile

    from efterlev.terraform import parse_terraform_file

    with tempfile.NamedTemporaryFile(mode="w", suffix=".tf", delete=False, encoding="utf-8") as f:
        f.write(
            'resource "aws_iam_policy" "orphan" {\n'
            '  name   = "orphan"\n'
            "  policy = data.aws_iam_policy_document.does_not_exist.json\n"
            "}\n"
        )
        f.flush()
        results = detect(parse_terraform_file(Path(f.name)))
    assert len(results) == 1
    ev = results[0]
    assert ev.content["mfa_required"] == "unparseable"
    assert "does_not_exist" in ev.content["gap"]
    assert "no matching data source was found" in ev.content["gap"]
