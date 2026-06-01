"""Fixture-driven tests for `aws.api_gateway_auth_required`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 2 #3 design", this is detector gamma of
the Tier 2 #3 batch. Locks the three emission states across both REST v1
and HTTP v2 route resources.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.api_gateway_auth_required.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "api_gateway_auth_required"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_v1_method_iam_auth_emits_auth_required() -> None:
    """REST v1 method with explicit AWS_IAM auth."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "v1_method_iam_auth.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.api_gateway_auth_required"
    assert ev.ksis_evidenced == ["KSI-CNA-EIS", "KSI-CNA-DFP"]
    assert ev.controls_evidenced == ["AC-3", "AC-6"]
    assert ev.content["resource_type"] == "aws_api_gateway_method"
    assert ev.content["resource_name"] == "get_users_authed"
    assert ev.content["route_label"] == "GET get_users_authed"
    assert ev.content["auth_state"] == "auth_required"
    assert ev.content["pattern"] == "rest_api_v1_method_auth"
    assert ev.content["auth_mode"] == "AWS_IAM"


def test_v2_route_jwt_auth_emits_auth_required() -> None:
    """HTTP v2 route with explicit JWT auth (v2-only mode)."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "v2_route_jwt_auth.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_apigatewayv2_route"
    assert ev.content["resource_name"] == "get_orders_jwt"
    assert ev.content["route_label"] == "GET /orders"
    assert ev.content["auth_state"] == "auth_required"
    assert ev.content["pattern"] == "http_api_v2_route_auth"
    assert ev.content["auth_mode"] == "JWT"


# --- should_not_match (negative-evidence emission) ----------------------------


def test_v1_method_none_auth_emits_auth_none() -> None:
    """REST v1 method with explicit NONE auth: emit gap with description
    that explicitly notes the intentional-public case so reviewers
    understand why it's flagged."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "v1_method_none_auth.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["auth_state"] == "auth_none"
    assert ev.content["auth_mode"] == "NONE"
    assert "publicly invokable" in ev.content["gap"]
    assert "intentionally public" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------


def test_v2_route_omitted_authorization_type_emits_auth_none() -> None:
    """HTTP v2 route with authorization_type field omitted: defaults to
    NONE per provider docs. Detector emits the gap with the
    "(provider default ...)" note so reviewers see why."""
    from efterlev.models import SourceRef, TerraformResource

    route = TerraformResource(
        type="aws_apigatewayv2_route",
        name="default_public",
        kind="resource",
        body={
            "api_id": "v2-api-id",
            "route_key": "POST /webhook",
            # authorization_type omitted -> defaults to NONE
        },
        source_ref=SourceRef(file="v2.tf", line_start=1, line_end=5),
    )
    results = detect([route])
    assert len(results) == 1
    assert results[0].content["auth_state"] == "auth_none"
    assert "default" in results[0].content["gap"]


def test_interpolated_authorization_emits_unverifiable() -> None:
    """authorization field uses Terraform interpolation: detector
    cannot resolve. Emit `unverifiable` so the Gap Agent surfaces this
    as a reviewer flag rather than a gap."""
    from efterlev.models import SourceRef, TerraformResource

    method = TerraformResource(
        type="aws_api_gateway_method",
        name="dynamic_auth",
        kind="resource",
        body={
            "rest_api_id": "api-id",
            "resource_id": "res-id",
            "http_method": "POST",
            "authorization": "${var.auth_mode}",
        },
        source_ref=SourceRef(file="dynamic.tf", line_start=1, line_end=8),
    )
    results = detect([method])
    assert len(results) == 1
    assert results[0].content["auth_state"] == "unverifiable"
    assert "interpolation" in results[0].content["detail"]


def test_cognito_user_pools_counts_as_auth_required() -> None:
    """COGNITO_USER_POOLS is a v1-supported mode; detector treats it as
    auth_required."""
    from efterlev.models import SourceRef, TerraformResource

    method = TerraformResource(
        type="aws_api_gateway_method",
        name="cognito_auth",
        kind="resource",
        body={
            "rest_api_id": "api-id",
            "resource_id": "res-id",
            "http_method": "POST",
            "authorization": "COGNITO_USER_POOLS",
            "authorizer_id": "cognito-id",
        },
        source_ref=SourceRef(file="cognito.tf", line_start=1, line_end=8),
    )
    results = detect([method])
    assert len(results) == 1
    assert results[0].content["auth_state"] == "auth_required"
    assert results[0].content["auth_mode"] == "COGNITO_USER_POOLS"


def test_mixed_v1_and_v2_routes_each_emit_one_evidence() -> None:
    """Repo with both v1 + v2 routes, mixed auth posture: each route
    gets its own evidence with the right pattern label."""
    from efterlev.models import SourceRef, TerraformResource

    v1_authed = TerraformResource(
        type="aws_api_gateway_method",
        name="v1_authed",
        kind="resource",
        body={
            "rest_api_id": "api1",
            "resource_id": "res1",
            "http_method": "GET",
            "authorization": "AWS_IAM",
        },
        source_ref=SourceRef(file="api.tf", line_start=1, line_end=8),
    )
    v2_open = TerraformResource(
        type="aws_apigatewayv2_route",
        name="v2_open",
        kind="resource",
        body={
            "api_id": "api2",
            "route_key": "GET /health",
            "authorization_type": "NONE",
        },
        source_ref=SourceRef(file="api.tf", line_start=10, line_end=15),
    )
    results = detect([v1_authed, v2_open])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["v1_authed"].content["auth_state"] == "auth_required"
    assert by_name["v1_authed"].content["pattern"] == "rest_api_v1_method_auth"
    assert by_name["v2_open"].content["auth_state"] == "auth_none"
    assert by_name["v2_open"].content["pattern"] == "http_api_v2_route_auth"
