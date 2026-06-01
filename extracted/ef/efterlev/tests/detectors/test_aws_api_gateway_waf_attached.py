"""Fixture-driven tests for `aws.api_gateway_waf_attached`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 2 #3 design", this is detector delta of
the Tier 2 #3 batch. Locks the binary `waf_attached` / `waf_absent`
emission and the cross-resource name-substring matching against
aws_wafv2_web_acl_association.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.api_gateway_waf_attached.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "api_gateway_waf_attached"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_v1_stage_with_waf_emits_waf_attached() -> None:
    """REST v1 stage with matching aws_wafv2_web_acl_association."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "v1_stage_with_waf.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.api_gateway_waf_attached"
    assert ev.ksis_evidenced == ["KSI-CNA-RVP"]
    assert ev.controls_evidenced == ["SI-3", "SC-5"]
    assert ev.content["resource_type"] == "aws_api_gateway_stage"
    assert ev.content["resource_name"] == "prod_v1"
    assert ev.content["stage_name"] == "prod"
    assert ev.content["waf_state"] == "waf_attached"
    assert ev.content["pattern"] == "rest_api_v1_stage_waf"
    assert ev.content["association_resource_name"] == "protect_prod_v1"


def test_v2_stage_with_waf_emits_waf_attached() -> None:
    """HTTP v2 stage with matching association."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "v2_stage_with_waf.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_apigatewayv2_stage"
    assert ev.content["resource_name"] == "protected_v2"
    assert ev.content["stage_name"] == "prod"
    assert ev.content["waf_state"] == "waf_attached"
    assert ev.content["pattern"] == "http_api_v2_stage_waf"


# --- should_not_match (negative-evidence emission) ----------------------------


def test_v1_stage_without_waf_emits_waf_absent() -> None:
    """REST v1 stage with no association: emit gap with description
    that explicitly notes the intentionally-private case so reviewers
    see why the detector still flagged it."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "v1_stage_without_waf.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "internal_v1"
    assert ev.content["stage_name"] == "internal"
    assert ev.content["waf_state"] == "waf_absent"
    assert "L7 boundary" in ev.content["gap"]
    assert "intentionally private" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------


def test_v2_stage_without_waf_emits_waf_absent() -> None:
    """Same gap on the v2 side."""
    from efterlev.models import SourceRef, TerraformResource

    stage = TerraformResource(
        type="aws_apigatewayv2_stage",
        name="dev_v2",
        kind="resource",
        body={
            "api_id": "v2-api-id",
            "name": "dev",
            "auto_deploy": True,
        },
        source_ref=SourceRef(file="v2.tf", line_start=1, line_end=8),
    )
    results = detect([stage])
    assert len(results) == 1
    assert results[0].content["waf_state"] == "waf_absent"
    assert results[0].content["pattern"] == "http_api_v2_stage_waf"


def test_association_for_different_stage_does_not_match() -> None:
    """An association whose resource_arn references a different stage
    does NOT count for our stage. Lock the discrimination."""
    from efterlev.models import SourceRef, TerraformResource

    stage_a = TerraformResource(
        type="aws_apigatewayv2_stage",
        name="prod",
        kind="resource",
        body={"api_id": "id1", "name": "prod"},
        source_ref=SourceRef(file="api.tf", line_start=1, line_end=5),
    )
    stage_b = TerraformResource(
        type="aws_apigatewayv2_stage",
        name="staging",
        kind="resource",
        body={"api_id": "id2", "name": "staging"},
        source_ref=SourceRef(file="api.tf", line_start=7, line_end=11),
    )
    # Association references stage_a, NOT stage_b.
    assoc = TerraformResource(
        type="aws_wafv2_web_acl_association",
        name="protect_prod",
        kind="resource",
        body={
            "resource_arn": "${aws_apigatewayv2_stage.prod.arn}",
            "web_acl_arn": "${aws_wafv2_web_acl.x.arn}",
        },
        source_ref=SourceRef(file="api.tf", line_start=13, line_end=17),
    )
    results = detect([stage_a, stage_b, assoc])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["prod"].content["waf_state"] == "waf_attached"
    assert by_name["staging"].content["waf_state"] == "waf_absent"


def test_interpolation_in_resource_arn_still_matches() -> None:
    """Per DECISIONS Decision #3: resource_arn is almost always a
    Terraform interpolation. The detector should match by name-
    substring on the interpolation expression itself, NOT treat it
    as `unverifiable`. This test locks that contract."""
    from efterlev.models import SourceRef, TerraformResource

    stage = TerraformResource(
        type="aws_api_gateway_stage",
        name="prod",
        kind="resource",
        body={
            "rest_api_id": "id",
            "deployment_id": "dep",
            "stage_name": "prod",
        },
        source_ref=SourceRef(file="api.tf", line_start=1, line_end=5),
    )
    assoc = TerraformResource(
        type="aws_wafv2_web_acl_association",
        name="protect_prod",
        kind="resource",
        body={
            # Interpolation reference -- detector should match on
            # `aws_api_gateway_stage.prod` substring.
            "resource_arn": "${aws_api_gateway_stage.prod.arn}",
            "web_acl_arn": "arn:...",
        },
        source_ref=SourceRef(file="api.tf", line_start=7, line_end=11),
    )
    results = detect([stage, assoc])
    assert len(results) == 1
    assert results[0].content["waf_state"] == "waf_attached"


def test_mixed_v1_and_v2_stages_each_emit_one_evidence() -> None:
    """Repo with both flavors, mixed posture: each stage gets its own
    evidence."""
    from efterlev.models import SourceRef, TerraformResource

    v1 = TerraformResource(
        type="aws_api_gateway_stage",
        name="v1_prod",
        kind="resource",
        body={"rest_api_id": "id", "deployment_id": "dep", "stage_name": "prod"},
        source_ref=SourceRef(file="api.tf", line_start=1, line_end=5),
    )
    v2 = TerraformResource(
        type="aws_apigatewayv2_stage",
        name="v2_prod",
        kind="resource",
        body={"api_id": "id", "name": "prod"},
        source_ref=SourceRef(file="api.tf", line_start=7, line_end=11),
    )
    assoc = TerraformResource(
        type="aws_wafv2_web_acl_association",
        name="protect_v1",
        kind="resource",
        body={
            "resource_arn": "${aws_api_gateway_stage.v1_prod.arn}",
            "web_acl_arn": "arn:...",
        },
        source_ref=SourceRef(file="api.tf", line_start=13, line_end=17),
    )
    results = detect([v1, v2, assoc])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["v1_prod"].content["waf_state"] == "waf_attached"
    assert by_name["v1_prod"].content["pattern"] == "rest_api_v1_stage_waf"
    assert by_name["v2_prod"].content["waf_state"] == "waf_absent"
    assert by_name["v2_prod"].content["pattern"] == "http_api_v2_stage_waf"
