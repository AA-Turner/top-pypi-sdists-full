"""Fixture-driven tests for `aws.lambda_vpc_isolation`.

Loads each `.tf` file in the detector's `fixtures/{should_match,should_not_match}/`
directories, parses it via the Terraform parser, runs the detector, and
asserts on the emitted Evidence shape.

Per DECISIONS 2026-05-10 "Tier 2 #3 design", this is detector beta of
the Tier 2 #3 batch. Locks the three emission states: `vpc_isolated`,
`internet_facing`, `unverifiable`.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.detectors.aws.lambda_vpc_isolation.detector import detect
from efterlev.terraform import parse_terraform_file

DETECTOR_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "efterlev"
    / "detectors"
    / "aws"
    / "lambda_vpc_isolation"
)


def _run(path: Path) -> list:
    return detect(parse_terraform_file(path))


# --- should_match -------------------------------------------------------------


def test_lambda_with_vpc_config_emits_vpc_isolated() -> None:
    """Happy path: function declares vpc_config with literal subnet + SG IDs."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_match" / "lambda_with_vpc_config.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.detector_id == "aws.lambda_vpc_isolation"
    assert ev.ksis_evidenced == ["KSI-CNA-MAT"]
    assert ev.controls_evidenced == ["SC-7", "SC-7(3)"]
    assert ev.content["resource_type"] == "aws_lambda_function"
    assert ev.content["resource_name"] == "isolated_handler"
    assert ev.content["function_name"] == "isolated-handler"
    assert ev.content["isolation_state"] == "vpc_isolated"
    assert ev.content["pattern"] == "lambda_vpc_isolation"
    assert ev.content["subnet_count"] == 2
    assert ev.content["security_group_count"] == 1


# --- should_not_match (negative-evidence emission) ----------------------------


def test_lambda_without_vpc_config_emits_internet_facing() -> None:
    """Function with no vpc_config: emits the gap with a description
    that explicitly notes the intentional-internet case (webhook
    handlers, public health endpoints) so reviewers see why the
    detector still flagged it."""
    results = _run(DETECTOR_DIR / "fixtures" / "should_not_match" / "lambda_no_vpc_config.tf")
    assert len(results) == 1
    ev = results[0]
    assert ev.content["function_name"] == "webhook-handler"
    assert ev.content["isolation_state"] == "internet_facing"
    assert "webhook-handler" in ev.content["gap"]
    assert "intentionally internet-facing" in ev.content["gap"]


# --- in-process synthetic-resource tests --------------------------------------
# Cover edge cases that fixture files don't cleanly express.


def test_interpolated_subnet_ids_emits_vpc_isolated() -> None:
    """vpc_config with subnet_ids via interpolation (e.g.
    `${module.vpc.private_subnets}`) still attaches the function to a VPC, so
    it's vpc_isolated — flagged as reference-based (counts may be dynamic).
    Whether the subnet is itself private is out of scope."""
    from efterlev.models import SourceRef, TerraformResource

    fn = TerraformResource(
        type="aws_lambda_function",
        name="dynamic_vpc",
        kind="resource",
        body={
            "function_name": "dynamic-vpc-handler",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
            "vpc_config": {
                "subnet_ids": "${module.vpc.private_subnets}",
                "security_group_ids": ["sg-literal"],
            },
        },
        source_ref=SourceRef(file="dynamic.tf", line_start=1, line_end=12),
    )
    results = detect([fn])
    assert len(results) == 1
    assert results[0].content["isolation_state"] == "vpc_isolated"
    assert results[0].content["references_interpolated"] is True


def test_interpolated_sg_ids_emits_vpc_isolated() -> None:
    """Literal subnets + a resource-reference security group (the common
    `[aws_security_group.x.id]` shape) is still vpc_isolated."""
    from efterlev.models import SourceRef, TerraformResource

    fn = TerraformResource(
        type="aws_lambda_function",
        name="dynamic_sg",
        kind="resource",
        body={
            "function_name": "dynamic-sg-handler",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
            "vpc_config": {
                "subnet_ids": ["subnet-abc"],
                "security_group_ids": ["${aws_security_group.lambda.id}"],
            },
        },
        source_ref=SourceRef(file="dynamic.tf", line_start=1, line_end=12),
    )
    results = detect([fn])
    assert len(results) == 1
    assert results[0].content["isolation_state"] == "vpc_isolated"
    assert results[0].content["references_interpolated"] is True


def test_function_name_falls_back_to_resource_name() -> None:
    """function_name omitted (rare; provider rejects at apply): detector
    falls back to the Terraform resource name rather than crashing."""
    from efterlev.models import SourceRef, TerraformResource

    fn = TerraformResource(
        type="aws_lambda_function",
        name="fallback",
        kind="resource",
        body={
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
        },
        source_ref=SourceRef(file="incomplete.tf", line_start=1, line_end=5),
    )
    results = detect([fn])
    assert len(results) == 1
    assert results[0].content["function_name"] == "fallback"
    assert results[0].content["isolation_state"] == "internet_facing"


def test_mixed_lambdas_each_emits_correct_evidence() -> None:
    """Multiple functions with mixed posture: each gets its own evidence."""
    from efterlev.models import SourceRef, TerraformResource

    isolated = TerraformResource(
        type="aws_lambda_function",
        name="isolated",
        kind="resource",
        body={
            "function_name": "isolated",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
            "vpc_config": {
                "subnet_ids": ["subnet-1", "subnet-2"],
                "security_group_ids": ["sg-1"],
            },
        },
        source_ref=SourceRef(file="main.tf", line_start=1, line_end=10),
    )
    public = TerraformResource(
        type="aws_lambda_function",
        name="public",
        kind="resource",
        body={
            "function_name": "public",
            "role": "arn:...",
            "handler": "index.handler",
            "runtime": "python3.12",
        },
        source_ref=SourceRef(file="main.tf", line_start=12, line_end=18),
    )
    results = detect([isolated, public])
    assert len(results) == 2
    by_name = {ev.content["resource_name"]: ev for ev in results}
    assert by_name["isolated"].content["isolation_state"] == "vpc_isolated"
    assert by_name["public"].content["isolation_state"] == "internet_facing"
