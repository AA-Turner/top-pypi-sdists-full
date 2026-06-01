"""Fixture-driven tests for `aws.api_gateway_access_logging`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 2 #2 design", this is detector gamma of
the Tier 2 #2 batch. Locks the binary `configured` / `absent`
emission on both REST v1 and HTTP v2 stage resources.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.api_gateway_access_logging.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "api_gateway_access_logging"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_v1_stage_with_logs_emits_configured() -> None:
    """REST API v1 stage with access_log_settings declared."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "v1_stage_with_logs.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.api_gateway_access_logging"
    assert ev.ksis_evidenced == ["KSI-MLA-LET"]
    assert ev.controls_evidenced == ["AU-2", "AU-3"]
    assert ev.content["resource_type"] == "aws_api_gateway_stage"
    assert ev.content["resource_name"] == "prod"
    assert ev.content["stage_name"] == "prod"
    assert ev.content["logging_state"] == "configured"
    assert ev.content["pattern"] == "rest_api_v1_stage_access_logs"
    assert "destination_arn" in ev.content
    assert ev.content.get("format_present") is True


def test_v2_stage_with_logs_emits_configured() -> None:
    """HTTP API v2 stage with access_log_settings declared."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "v2_stage_with_logs.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_apigatewayv2_stage"
    assert ev.content["resource_name"] == "prod_v2"
    assert ev.content["logging_state"] == "configured"
    assert ev.content["pattern"] == "http_api_v2_stage_access_logs"
    assert ev.content.get("format_present") is True


# --- should_not_match (negative-evidence emission) ----------------------------


def test_v1_stage_without_logs_emits_absent() -> None:
    """Stage with no access_log_settings: gap with description naming
    the request-path-blind problem."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "v1_stage_without_logs.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_name"] == "staging"
    assert ev.content["logging_state"] == "absent"
    assert "staging" in ev.content["gap"]
    assert "request-path" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------
# Cover edge cases that fixture files don't cleanly express.


def test_v2_stage_without_logs_emits_absent() -> None:
    """Same gap on the v2 side. Pattern label distinguishes from v1."""
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
    assert results[0].content["logging_state"] == "absent"
    assert results[0].content["pattern"] == "http_api_v2_stage_access_logs"


def test_stage_name_falls_back_to_resource_name_when_absent() -> None:
    """Some stage resources omit stage_name (rare; AWS provider rejects
    at apply for v1 but is tolerant for v2). Detector should fall back
    to the Terraform resource name rather than crashing."""
    from efterlev.models import SourceRef, TerraformResource

    stage = TerraformResource(
        type="aws_apigatewayv2_stage",
        name="fallback_named",
        kind="resource",
        body={
            "api_id": "v2-api-id",
            # stage `name` field omitted
        },
        source_ref=SourceRef(file="incomplete.tf", line_start=1, line_end=5),
    )
    results = detect([stage])
    assert len(results) == 1
    assert results[0].content["stage_name"] == "fallback_named"


def test_mixed_v1_and_v2_each_emits_one_evidence() -> None:
    """Repo with both flavors: each stage gets its own evidence record
    with the right pattern label."""
    from efterlev.models import SourceRef, TerraformResource

    v1 = TerraformResource(
        type="aws_api_gateway_stage",
        name="v1_prod",
        kind="resource",
        body={
            "rest_api_id": "api1",
            "deployment_id": "dep1",
            "stage_name": "prod",
            "access_log_settings": {
                "destination_arn": "arn:...",
                "format": "$context.requestId",
            },
        },
        source_ref=SourceRef(file="api.tf", line_start=1, line_end=10),
    )
    v2 = TerraformResource(
        type="aws_apigatewayv2_stage",
        name="v2_prod",
        kind="resource",
        body={"api_id": "api2", "name": "prod"},
        source_ref=SourceRef(file="api.tf", line_start=12, line_end=18),
    )
    results = detect([v1, v2])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["v1_prod"].content["logging_state"] == "configured"
    assert by_name["v1_prod"].content["pattern"] == "rest_api_v1_stage_access_logs"
    assert by_name["v2_prod"].content["logging_state"] == "absent"
    assert by_name["v2_prod"].content["pattern"] == "http_api_v2_stage_access_logs"
