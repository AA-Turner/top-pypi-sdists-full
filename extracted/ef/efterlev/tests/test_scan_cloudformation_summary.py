"""Tests for the v0.1.103 scan_cloudformation summary fields.

Regression tests for the QA-surfaced bundle (v0.1.103):
- `nested_stack_refs` field counts AWS::CloudFormation::Stack references
- `parse_failures` list propagates from parse_cfn_tree to the primitive output

The QA scan that surfaced these (aws-quickstart/quickstart-aws-aurora-
postgresql) silently dropped a 1091-line template because the parser
crashed on a Rules-section `!ValueOf` intrinsic, AND the main template
was mostly nested-stack references that the user had no signal about.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.primitives.scan.scan_cloudformation import (
    ScanCloudFormationInput,
    scan_cloudformation,
)


def test_nested_stack_refs_counted(tmp_path: Path) -> None:
    """`AWS::CloudFormation::Stack` resources are counted in `nested_stack_refs`."""
    cfn = tmp_path / "main.yaml"
    cfn.write_text(
        "Resources:\n"
        "  ChildA:\n"
        "    Type: AWS::CloudFormation::Stack\n"
        "    Properties:\n"
        "      TemplateURL: https://example.com/a.yaml\n"
        "  ChildB:\n"
        "    Type: AWS::CloudFormation::Stack\n"
        "    Properties:\n"
        "      TemplateURL: https://example.com/b.yaml\n"
        "  Bucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties: {}\n"
    )
    out = scan_cloudformation(ScanCloudFormationInput(target_dir=tmp_path))
    assert out.nested_stack_refs == 2
    # The bucket counts toward resources_parsed but not nested_stack_refs.
    assert out.resources_parsed == 3


def test_nested_stack_refs_zero_when_no_nested_stacks(tmp_path: Path) -> None:
    """Plain CFN with no nested-stack references reports `nested_stack_refs=0`."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text("Resources:\n  Bucket:\n    Type: AWS::S3::Bucket\n    Properties: {}\n")
    out = scan_cloudformation(ScanCloudFormationInput(target_dir=tmp_path))
    assert out.nested_stack_refs == 0


def test_parse_failures_surfaced_when_template_unparseable(tmp_path: Path) -> None:
    """Parse failures from parse_cfn_tree propagate to the primitive output."""
    # Valid CFN
    (tmp_path / "good.yaml").write_text(
        "Resources:\n  Bucket:\n    Type: AWS::S3::Bucket\n    Properties: {}\n"
    )
    # Malformed YAML that triggers a parse error AFTER passing the
    # content-sniff (it has Resources: at the top so it's recognized as
    # CFN, but the yaml is structurally broken).
    (tmp_path / "bad.yaml").write_text(
        "Resources:\n"
        "  Bucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      BadIndent:\n"
        "  - this is not valid yaml here\n"
    )
    out = scan_cloudformation(ScanCloudFormationInput(target_dir=tmp_path))
    # The good template parses to 1 resource; the bad one fails.
    assert out.resources_parsed == 1
    assert len(out.parse_failures) == 1
    assert out.parse_failures[0].file.name == "bad.yaml"
    assert out.parse_failures[0].reason  # non-empty reason string


def test_value_of_intrinsic_no_longer_silent_failure(tmp_path: Path) -> None:
    """Regression: pre-v0.1.103 a `!ValueOf` in Rules silently dropped the template.

    Mirrors the aws-quickstart/quickstart-aws-aurora-postgresql QA finding.
    Now the template parses cleanly and `parse_failures` stays empty.
    """
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Bucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties: {}\n"
        "Rules:\n"
        "  SubnetsInVPC:\n"
        "    Assertions:\n"
        "      - Assert: !Equals [!ValueOf [Subnet1ID, VpcId], vpc-abc]\n"
        "        AssertDescription: All subnets must be in the same VPC\n"
    )
    out = scan_cloudformation(ScanCloudFormationInput(target_dir=tmp_path))
    assert out.resources_parsed == 1
    assert out.parse_failures == []
