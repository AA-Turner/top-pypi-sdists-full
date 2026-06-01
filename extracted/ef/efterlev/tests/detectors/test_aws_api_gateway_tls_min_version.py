"""Fixture-driven tests for `aws.api_gateway_tls_min_version`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-09 "Tier 2 #1 design: Lambda + API Gateway detector
batch v0", this is detector gamma of the v0 batch. Pairs with PR beta
(`aws.lambda_logging_configured`) for the most common serverless edge
(Lambda behind API Gateway).
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.api_gateway_tls_min_version.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "api_gateway_tls_min_version"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_v1_explicit_tls_1_2_emits_configured() -> None:
    """Happy path on REST API v1: explicit security_policy = TLS_1_2."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "v1_tls_1_2.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.api_gateway_tls_min_version"
    assert ev.ksis_evidenced == ["KSI-SVC-SNT"]
    assert ev.controls_evidenced == ["SC-8", "SC-13", "SC-23"]
    assert ev.content["resource_type"] == "aws_api_gateway_domain_name"
    assert ev.content["resource_name"] == "compliant"
    assert ev.content["tls_min_state"] == "configured"
    assert ev.content["pattern"] == "rest_api_v1_custom_domain"
    assert ev.content["security_policy"] == "TLS_1_2"


def test_v2_omitted_security_policy_emits_configured() -> None:
    """HTTP API v2: security_policy absent within the
    domain_name_configuration block resolves to TLS_1_2 (the only
    value v2 supports)."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "v2_default.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_apigatewayv2_domain_name"
    assert ev.content["resource_name"] == "v2_compliant"
    assert ev.content["tls_min_state"] == "configured"
    assert ev.content["pattern"] == "http_api_v2_custom_domain"
    assert ev.content["security_policy"] == "TLS_1_2"
    assert "v2 service default" in ev.content["detail"]


# --- should_not_match (negative-evidence emission) ----------------------------


def test_v1_explicit_tls_1_0_emits_absent_with_gap() -> None:
    """REST API v1 with explicit security_policy = TLS_1_0: the canonical
    explicit gap. Detector emits `absent` with a gap description."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "v1_tls_1_0.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["tls_min_state"] == "absent"
    assert ev.content["security_policy"] == "TLS_1_0"
    assert "TLS_1_0" in ev.content["gap"]
    assert "FedRAMP" in ev.content["gap"]
    # The "(provider default ...)" note should NOT appear here -- the
    # value was explicit, not defaulted.
    assert "default" not in ev.content["gap"]


def test_v1_omitted_security_policy_emits_absent_with_default_note() -> None:
    """REST API v1 with security_policy omitted: AWS provider defaults to
    TLS_1_0. Detector emits `absent` with a gap note that mentions the
    default-attribute behavior so reviewers see why the resource fails."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "v1_default.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["tls_min_state"] == "absent"
    assert ev.content["security_policy"] == "TLS_1_0"
    assert "default" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------
# Cover edge cases that fixture files don't cleanly express.


def test_v1_interpolated_security_policy_emits_unverifiable() -> None:
    """security_policy uses Terraform interpolation: detector cannot
    resolve the value at scan time. Emit `unverifiable` so the Gap
    Agent surfaces this as a reviewer flag rather than a gap."""
    from efterlev.models import SourceRef, TerraformResource

    domain = TerraformResource(
        type="aws_api_gateway_domain_name",
        name="dynamic",
        kind="resource",
        body={
            "domain_name": "${var.api_domain}",
            "regional_certificate_arn": "arn:...",
            "security_policy": "${var.tls_floor}",
        },
        source_ref=SourceRef(file="dynamic.tf", line_start=1, line_end=10),
    )
    results = detect([domain])
    assert len(results) == 1
    assert results[0].content["tls_min_state"] == "unverifiable"
    assert "interpolation" in results[0].content["detail"]


def test_v2_missing_domain_name_configuration_emits_no_evidence() -> None:
    """v2 resource without the required domain_name_configuration block
    is malformed; AWS provider rejects it at apply. Detector skips
    rather than emitting noisy evidence."""
    from efterlev.models import SourceRef, TerraformResource

    malformed = TerraformResource(
        type="aws_apigatewayv2_domain_name",
        name="malformed",
        kind="resource",
        body={"domain_name": "broken.example.com"},
        source_ref=SourceRef(file="malformed.tf", line_start=1, line_end=4),
    )
    results = detect([malformed])
    assert results == []


def test_mixed_v1_v2_each_emits_one_evidence() -> None:
    """A repo with both v1 and v2 custom domains should produce one
    evidence record per resource."""
    from efterlev.models import SourceRef, TerraformResource

    v1 = TerraformResource(
        type="aws_api_gateway_domain_name",
        name="v1_legacy",
        kind="resource",
        body={
            "domain_name": "legacy.example.com",
            "regional_certificate_arn": "arn:...",
        },
        source_ref=SourceRef(file="api.tf", line_start=1, line_end=8),
    )
    v2 = TerraformResource(
        type="aws_apigatewayv2_domain_name",
        name="v2_modern",
        kind="resource",
        body={
            "domain_name": "modern.example.com",
            "domain_name_configuration": {
                "certificate_arn": "arn:...",
                "endpoint_type": "REGIONAL",
                "security_policy": "TLS_1_2",
            },
        },
        source_ref=SourceRef(file="api.tf", line_start=10, line_end=20),
    )
    results = detect([v1, v2])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["v1_legacy"].content["tls_min_state"] == "absent"
    assert by_name["v2_modern"].content["tls_min_state"] == "configured"
