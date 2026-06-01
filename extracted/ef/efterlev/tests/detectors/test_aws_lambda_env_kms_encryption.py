"""Fixture-driven tests for `aws.lambda_env_kms_encryption`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 2 #2 design", this is detector beta of
the Tier 2 #2 batch. Locks the four emission paths: configured,
absent, unverifiable, and skipped (function with no env vars).
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.lambda_env_kms_encryption.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "lambda_env_kms_encryption"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_lambda_with_env_vars_and_cmk_emits_configured() -> None:
    """Happy path: function declares env vars AND kms_key_arn."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "lambda_with_cmk.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.lambda_env_kms_encryption"
    assert ev.ksis_evidenced == ["KSI-AFR-UCM"]
    assert ev.controls_evidenced == ["SC-28", "SC-28(1)"]
    assert ev.content["resource_type"] == "aws_lambda_function"
    assert ev.content["resource_name"] == "secrets_handler"
    assert ev.content["function_name"] == "secrets-handler"
    assert ev.content["kms_state"] == "configured"
    assert ev.content["pattern"] == "lambda_env_var_cmk"
    assert "abc-123" in ev.content["kms_key_arn"]


# --- should_not_match (negative-evidence emission) ----------------------------


def test_lambda_with_env_vars_no_cmk_emits_absent() -> None:
    """Function has env vars but no kms_key_arn: gap with description."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "lambda_default_kms.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["function_name"] == "default-kms-handler"
    assert ev.content["kms_state"] == "absent"
    assert "default-kms-handler" in ev.content["gap"]
    assert "AWS-managed" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------
# Cover edge cases that fixture files don't cleanly express.


def test_lambda_without_env_vars_emits_no_evidence() -> None:
    """Function with no environment block at all: detector skips. Adding
    noisy "no env vars" evidence would dilute M3 signal on the KSIs the
    agent later classifies."""
    from efterlev.models import SourceRef, TerraformResource

    fn = TerraformResource(
        type="aws_lambda_function",
        name="stateless",
        kind="resource",
        body={
            "function_name": "stateless-handler",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
        },
        source_ref=SourceRef(file="stateless.tf", line_start=1, line_end=8),
    )
    assert detect([fn]) == []


def test_lambda_with_empty_env_variables_emits_no_evidence() -> None:
    """Function declares `environment { variables = {} }`: empty map
    means no secrets to protect; detector skips."""
    from efterlev.models import SourceRef, TerraformResource

    fn = TerraformResource(
        type="aws_lambda_function",
        name="empty_env",
        kind="resource",
        body={
            "function_name": "empty-env-handler",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
            "environment": {"variables": {}},
        },
        source_ref=SourceRef(file="empty.tf", line_start=1, line_end=10),
    )
    assert detect([fn]) == []


def test_interpolated_kms_key_arn_emits_unverifiable() -> None:
    """kms_key_arn uses `${...}`: detector cannot resolve. Emit
    `unverifiable` so the Gap Agent surfaces this as a reviewer flag
    rather than guessing."""
    from efterlev.models import SourceRef, TerraformResource

    fn = TerraformResource(
        type="aws_lambda_function",
        name="dynamic_kms",
        kind="resource",
        body={
            "function_name": "dynamic-kms-handler",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
            "kms_key_arn": "${aws_kms_key.lambda_secrets.arn}",
            "environment": {"variables": {"FOO": "bar"}},
        },
        source_ref=SourceRef(file="dynamic.tf", line_start=1, line_end=12),
    )
    results = detect([fn])
    assert len(results) == 1
    assert results[0].content["kms_state"] == "unverifiable"
    assert "interpolation" in results[0].content["detail"]


def test_mixed_lambdas_each_emits_correct_evidence() -> None:
    """Multiple functions with mixed posture: each gets its own
    evidence record. Functions without env vars are skipped from the
    output entirely."""
    from efterlev.models import SourceRef, TerraformResource

    with_cmk = TerraformResource(
        type="aws_lambda_function",
        name="with_cmk",
        kind="resource",
        body={
            "function_name": "with-cmk",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
            "kms_key_arn": "arn:aws:kms:...:key/abc",
            "environment": {"variables": {"X": "1"}},
        },
        source_ref=SourceRef(file="main.tf", line_start=1, line_end=10),
    )
    no_cmk = TerraformResource(
        type="aws_lambda_function",
        name="no_cmk",
        kind="resource",
        body={
            "function_name": "no-cmk",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
            "environment": {"variables": {"Y": "2"}},
        },
        source_ref=SourceRef(file="main.tf", line_start=12, line_end=21),
    )
    no_env = TerraformResource(
        type="aws_lambda_function",
        name="no_env",
        kind="resource",
        body={
            "function_name": "no-env",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
        },
        source_ref=SourceRef(file="main.tf", line_start=23, line_end=29),
    )
    results = detect([with_cmk, no_cmk, no_env])
    assert len(results) == 2  # no_env is skipped
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["with_cmk"].content["kms_state"] == "configured"
    assert by_name["no_cmk"].content["kms_state"] == "absent"
    assert "no_env" not in by_name
