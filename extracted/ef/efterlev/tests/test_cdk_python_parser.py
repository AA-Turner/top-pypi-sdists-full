"""Tests for v0.1.126 — CDK Python source parser.

Stage 1 of the CDK source-mode arc per DECISIONS 2026-05-15. Walks
.py files, identifies supported `aws_cdk.*` construct invocations
under both import styles, returns `CdkConstruct` records with the
`.py` source line preserved (the source-mode value proposition).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from efterlev.cdk_python import CdkConstruct, parse_cdk_python_file, parse_cdk_python_tree
from efterlev.errors import DetectorError

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = REPO_ROOT / "evals/fixtures/cdk-python-sample"
SAMPLE_STACK = SAMPLE_DIR / "infra/storage_stack.py"


def test_parse_sample_stack_finds_both_buckets() -> None:
    """Sample stack uses both alias-style and direct-style imports → 2 constructs."""
    constructs = parse_cdk_python_file(SAMPLE_STACK)
    assert len(constructs) == 2
    ids = {c.construct_id for c in constructs}
    assert ids == {"LogsBucket", "AssetsBucket"}
    assert all(c.cfn_type == "AWS::S3::Bucket" for c in constructs)


def test_parse_security_stack_finds_stage2_constructs() -> None:
    """Stage 2 (v0.1.127): KMS Key + EC2 SecurityGroup + IAM Role + CloudTrail Trail."""
    constructs = parse_cdk_python_file(SAMPLE_DIR / "infra/security_stack.py")
    by_type = {c.cfn_type: c for c in constructs}
    assert "AWS::KMS::Key" in by_type
    assert "AWS::EC2::SecurityGroup" in by_type
    assert "AWS::IAM::Role" in by_type
    assert "AWS::CloudTrail::Trail" in by_type
    # IAM Role uses direct-import style (`from aws_cdk.aws_iam import Role`);
    # confirm the parser resolves that path too.
    assert by_type["AWS::IAM::Role"].construct_id == "AppRole"


def test_parse_compute_stack_finds_stage3_constructs() -> None:
    """Stage 3 (v0.1.128): Lambda + RDS DB + DynamoDB Table + Logs LogGroup."""
    constructs = parse_cdk_python_file(SAMPLE_DIR / "infra/compute_stack.py")
    by_type = {c.cfn_type: c for c in constructs}
    assert "AWS::Lambda::Function" in by_type
    assert "AWS::RDS::DBInstance" in by_type
    assert "AWS::DynamoDB::Table" in by_type
    assert "AWS::Logs::LogGroup" in by_type


def test_parse_services_stack_finds_stage4_constructs() -> None:
    """Stage 4 (v0.1.129): finisher batch — 18 constructs across remaining service families."""
    constructs = parse_cdk_python_file(SAMPLE_DIR / "infra/services_stack.py")
    cfn_types = {c.cfn_type for c in constructs}
    expected = {
        "AWS::SNS::Topic",
        "AWS::SQS::Queue",
        "AWS::EFS::FileSystem",
        "AWS::EKS::Cluster",
        "AWS::EC2::VPC",
        "AWS::SecretsManager::Secret",
        "AWS::ApiGateway::RestApi",
        "AWS::ApiGatewayV2::Api",
        "AWS::AutoScaling::AutoScalingGroup",
        "AWS::ElasticLoadBalancingV2::LoadBalancer",
        "AWS::CloudWatch::Alarm",
        "AWS::Events::Rule",
        "AWS::Backup::BackupVault",
        "AWS::Backup::BackupPlan",
        "AWS::IAM::User",
        "AWS::IAM::Group",
        "AWS::Kinesis::Stream",
        "AWS::OpenSearchService::Domain",
    }
    assert expected.issubset(cfn_types), f"missing: {expected - cfn_types}"
    assert len(constructs) == 18


def test_parser_records_source_line() -> None:
    """The whole point of source-mode: each construct has a .py line number."""
    constructs = parse_cdk_python_file(SAMPLE_STACK)
    for c in constructs:
        assert c.source_line > 0
        assert c.source_file == SAMPLE_STACK


def test_parser_extracts_kwargs_with_attribute_resolution(tmp_path: Path) -> None:
    """Constants come through as Python literals; attribute access (e.g.
    `s3.BucketEncryption.S3_MANAGED`) renders as a dotted string so the
    detector layer can see "explicitly set, opaque value" rather than missing.
    """
    src = tmp_path / "stack.py"
    src.write_text(
        "from aws_cdk import aws_s3 as s3\n"
        "from constructs import Construct\n"
        "\n"
        "def make(scope):\n"
        "    return s3.Bucket(scope, 'B', "
        "bucket_name='x', versioned=True, "
        "encryption=s3.BucketEncryption.S3_MANAGED)\n",
        encoding="utf-8",
    )
    [c] = parse_cdk_python_file(src)
    assert c.kwargs["bucket_name"] == "x"
    assert c.kwargs["versioned"] is True
    assert c.kwargs["encryption"] == "s3.BucketEncryption.S3_MANAGED"


def test_parser_handles_direct_construct_import(tmp_path: Path) -> None:
    """`from aws_cdk.aws_s3 import Bucket` style should also resolve."""
    src = tmp_path / "stack.py"
    src.write_text(
        "from aws_cdk.aws_s3 import Bucket\n"
        "from constructs import Construct\n"
        "\n"
        "def make(scope):\n"
        "    return Bucket(scope, 'B', bucket_name='y')\n",
        encoding="utf-8",
    )
    [c] = parse_cdk_python_file(src)
    assert c.construct_id == "B"
    assert c.cfn_type == "AWS::S3::Bucket"


def test_parser_returns_empty_for_files_without_aws_cdk_imports(tmp_path: Path) -> None:
    """No CDK imports → empty result (cheap content-sniff for the rglob walker)."""
    src = tmp_path / "ordinary.py"
    src.write_text("def foo():\n    return 42\n", encoding="utf-8")
    assert parse_cdk_python_file(src) == []


def test_parser_skips_unsupported_constructs(tmp_path: Path) -> None:
    """Constructs not in `_SUPPORTED_CONSTRUCTS` are silently skipped.
    `aws_stepfunctions.StateMachine` is not in v0.1.129's supported map;
    only the Bucket should come through.
    """
    src = tmp_path / "stack.py"
    src.write_text(
        "from aws_cdk import aws_s3 as s3, aws_stepfunctions as sfn\n"
        "def make(scope):\n"
        "    return [s3.Bucket(scope, 'B'), sfn.StateMachine(scope, 'SM')]\n",
        encoding="utf-8",
    )
    [c] = parse_cdk_python_file(src)
    assert c.construct_id == "B"


def test_parser_raises_on_syntax_error(tmp_path: Path) -> None:
    """Soft schema drift: parse errors raise; the tree walker catches and continues."""
    src = tmp_path / "broken.py"
    src.write_text("from aws_cdk import aws_s3 as s3\ndef:\n", encoding="utf-8")
    with pytest.raises(DetectorError):
        parse_cdk_python_file(src)


def test_tree_walker_aggregates_constructs() -> None:
    """End-to-end: walk the sample fixture across all 4 stacks (S1+S2+S3+S4)."""
    constructs, failures = parse_cdk_python_tree(SAMPLE_DIR)
    # Stage 1: 2 buckets; Stage 2: 4 security; Stage 3: 4 compute;
    # Stage 4: 18 services → 28 total. (Note: 27 supported types but
    # storage_stack.py declares 2 buckets so total instances = 28.)
    assert len(constructs) == 28
    assert failures == []
    cfn_types = {c.cfn_type for c in constructs}
    # 27 distinct supported types from _SUPPORTED_CONSTRUCTS.
    assert len(cfn_types) == 27


def test_tree_walker_skips_excluded_dirs(tmp_path: Path) -> None:
    """`.venv`, `__pycache__`, `cdk.out` etc. are skipped during the walk."""
    (tmp_path / "infra").mkdir()
    (tmp_path / "infra/stack.py").write_text(
        "from aws_cdk import aws_s3 as s3\n"
        "from constructs import Construct\n"
        "def make(scope):\n"
        "    return s3.Bucket(scope, 'Real')\n",
        encoding="utf-8",
    )
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv/should_skip.py").write_text(
        "from aws_cdk import aws_s3 as s3\n"
        "def make(scope):\n"
        "    return s3.Bucket(scope, 'ShouldNotSeeThisOne')\n",
        encoding="utf-8",
    )
    constructs, failures = parse_cdk_python_tree(tmp_path)
    ids = {c.construct_id for c in constructs}
    assert ids == {"Real"}
    assert failures == []


def test_construct_record_is_immutable() -> None:
    """`CdkConstruct` is frozen so detectors can rely on hashability."""
    c = CdkConstruct(
        construct_id="X",
        cfn_type="AWS::S3::Bucket",
        kwargs={},
        source_file=Path("/tmp/x.py"),
        source_line=1,
    )
    with pytest.raises((AttributeError, TypeError)):
        c.construct_id = "Y"  # type: ignore[misc]
