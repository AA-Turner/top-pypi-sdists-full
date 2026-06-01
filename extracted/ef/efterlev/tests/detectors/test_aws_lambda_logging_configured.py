"""Fixture-driven tests for `aws.lambda_logging_configured`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-09 "Tier 2 #1 design: Lambda + API Gateway detector
batch v0", this is the v0 batch's first detector. Locks the three
emission states: `configured`, `absent`, `unverifiable`.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.lambda_logging_configured.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "lambda_logging_configured"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_lambda_with_matching_log_group_emits_configured() -> None:
    """Happy path: function_name is literal, matching log group exists."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "lambda_with_log_group.tf")
    assert len(results) == 1, f"expected 1 evidence, got {len(results)}"
    ev = results[0]
    assert ev.detector_id == "aws.lambda_logging_configured"
    assert ev.ksis_evidenced == ["KSI-MLA-LET"]
    assert ev.controls_evidenced == ["AU-2", "AU-12"]
    assert ev.content["resource_type"] == "aws_lambda_function"
    assert ev.content["resource_name"] == "handler"
    assert ev.content["logging_state"] == "configured"
    assert ev.content["pattern"] == "log_group_per_function"
    assert "my-handler" in ev.content["detail"]
    assert "/aws/lambda/my-handler" in ev.content["detail"]


# --- should_not_match (negative-evidence emission) ----------------------------


def test_lambda_without_log_group_emits_absent() -> None:
    """Function declared with no matching aws_cloudwatch_log_group:
    detector emits negative evidence with a `gap` description."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "lambda_without_log_group.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["resource_type"] == "aws_lambda_function"
    assert ev.content["resource_name"] == "auto_logs_only"
    assert ev.content["logging_state"] == "absent"
    assert ev.content["pattern"] == "log_group_per_function"
    assert "auto-logs-only" in ev.content["gap"]
    assert "/aws/lambda/auto-logs-only" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------
# These cover edge cases that fixture-files don't cleanly express
# (interpolated function_name; log group with interpolated name; etc.)


def test_interpolated_function_name_emits_unverifiable() -> None:
    """function_name uses `${...}` -- detector cannot resolve the
    expected log group name. Emit `unverifiable`, not `absent`, so the
    Gap Agent surfaces this as a reviewer flag rather than a gap."""
    from efterlev.models import SourceRef, TerraformResource

    fn = TerraformResource(
        type="aws_lambda_function",
        name="interpolated",
        kind="resource",
        body={
            "function_name": "${var.app_prefix}-handler",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
        },
        source_ref=SourceRef(file="dynamic.tf", line_start=1, line_end=10),
    )
    results = detect([fn])
    assert len(results) == 1
    assert results[0].content["logging_state"] == "unverifiable"
    assert "interpolation" in results[0].content["detail"]


def test_missing_function_name_emits_no_evidence() -> None:
    """function_name absent (schema-malformed): detector skips rather
    than emitting noisy evidence. AWS provider rejects it at apply
    time anyway."""
    from efterlev.models import SourceRef, TerraformResource

    fn = TerraformResource(
        type="aws_lambda_function",
        name="malformed",
        kind="resource",
        body={
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
        },
        source_ref=SourceRef(file="malformed.tf", line_start=1, line_end=8),
    )
    results = detect([fn])
    assert results == []


def test_log_group_with_interpolated_name_does_not_match() -> None:
    """Log group whose `name` itself uses interpolation can't be matched
    against a literal function_name; detector treats the function as
    `absent` rather than guessing."""
    from efterlev.models import SourceRef, TerraformResource

    fn = TerraformResource(
        type="aws_lambda_function",
        name="literal_fn",
        kind="resource",
        body={
            "function_name": "literal-handler",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
        },
        source_ref=SourceRef(file="main.tf", line_start=1, line_end=8),
    )
    log_group = TerraformResource(
        type="aws_cloudwatch_log_group",
        name="dynamic_logs",
        kind="resource",
        body={"name": "/aws/lambda/${var.app_name}", "retention_in_days": 90},
        source_ref=SourceRef(file="main.tf", line_start=10, line_end=14),
    )
    results = detect([fn, log_group])
    assert len(results) == 1
    assert results[0].content["logging_state"] == "absent"


def test_multiple_lambdas_emit_one_evidence_each() -> None:
    """Mixed posture: one function with log group, one without.
    Each function gets its own evidence; log group is only counted
    against its matching function."""
    from efterlev.models import SourceRef, TerraformResource

    compliant_fn = TerraformResource(
        type="aws_lambda_function",
        name="compliant",
        kind="resource",
        body={
            "function_name": "compliant-handler",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
        },
        source_ref=SourceRef(file="main.tf", line_start=1, line_end=8),
    )
    gap_fn = TerraformResource(
        type="aws_lambda_function",
        name="gap",
        kind="resource",
        body={
            "function_name": "gap-handler",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
        },
        source_ref=SourceRef(file="main.tf", line_start=10, line_end=17),
    )
    log_group = TerraformResource(
        type="aws_cloudwatch_log_group",
        name="compliant_logs",
        kind="resource",
        body={"name": "/aws/lambda/compliant-handler", "retention_in_days": 90},
        source_ref=SourceRef(file="main.tf", line_start=19, line_end=22),
    )
    results = detect([compliant_fn, gap_fn, log_group])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["compliant"].content["logging_state"] == "configured"
    assert by_name["gap"].content["logging_state"] == "absent"
