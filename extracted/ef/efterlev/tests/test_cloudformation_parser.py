"""Tests for the CloudFormation parser.

Covers:
- YAML loading with CFN intrinsic-function tags (!Ref, !Sub, !GetAtt, etc.)
- JSON loading
- Content-sniff (only files with `AWSTemplateFormatVersion` or `Resources`
  are treated as CFN; other YAML/JSON is silently skipped)
- Partial-success collect-and-continue across many files in a tree
"""

from __future__ import annotations

from pathlib import Path

import pytest

from efterlev.cloudformation.parser import (
    _CfnSafeLoader,
    parse_cfn_file,
    parse_cfn_tree,
)
from efterlev.errors import DetectorError


def test_parse_minimal_yaml(tmp_path: Path) -> None:
    """A minimal CFN YAML with one bucket parses to one CfnResource."""
    f = tmp_path / "stack.yaml"
    f.write_text(
        "AWSTemplateFormatVersion: '2010-09-09'\n"
        "Resources:\n"
        "  MyBucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      BucketName: my-bucket\n"
    )
    resources = parse_cfn_file(f)
    assert len(resources) == 1
    r = resources[0]
    assert r.logical_id == "MyBucket"
    assert r.type == "AWS::S3::Bucket"
    assert r.properties == {"BucketName": "my-bucket"}


def test_parse_minimal_json(tmp_path: Path) -> None:
    """A `cdk synth`-style JSON template parses identically."""
    f = tmp_path / "stack.json"
    f.write_text(
        '{"AWSTemplateFormatVersion": "2010-09-09",'
        ' "Resources": {"MyBucket": {"Type": "AWS::S3::Bucket",'
        ' "Properties": {"BucketName": "my-bucket"}}}}'
    )
    resources = parse_cfn_file(f)
    assert len(resources) == 1
    assert resources[0].logical_id == "MyBucket"
    assert resources[0].type == "AWS::S3::Bucket"


def test_intrinsic_ref_yaml(tmp_path: Path) -> None:
    """`!Ref X` resolves to long-form `{"Ref": "X"}`."""
    f = tmp_path / "stack.yaml"
    f.write_text(
        "Resources:\n"
        "  Bucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      BucketName: !Ref BucketNameParam\n"
    )
    resources = parse_cfn_file(f)
    assert resources[0].properties == {"BucketName": {"Ref": "BucketNameParam"}}


def test_intrinsic_sub_yaml(tmp_path: Path) -> None:
    """`!Sub` short form (scalar) → `{"Fn::Sub": "..."}`."""
    f = tmp_path / "stack.yaml"
    f.write_text(
        "Resources:\n"
        "  Bucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        '      BucketName: !Sub "${AWS::Region}-bucket"\n'
    )
    resources = parse_cfn_file(f)
    assert resources[0].properties == {"BucketName": {"Fn::Sub": "${AWS::Region}-bucket"}}


def test_intrinsic_getatt_short_form(tmp_path: Path) -> None:
    """`!GetAtt LogicalId.Attr` → `{"Fn::GetAtt": ["LogicalId", "Attr"]}`."""
    f = tmp_path / "stack.yaml"
    f.write_text(
        "Resources:\n"
        "  Policy:\n"
        "    Type: AWS::IAM::Policy\n"
        "    Properties:\n"
        "      Resource: !GetAtt MyBucket.Arn\n"
    )
    resources = parse_cfn_file(f)
    assert resources[0].properties == {"Resource": {"Fn::GetAtt": ["MyBucket", "Arn"]}}


def test_intrinsic_join_sequence(tmp_path: Path) -> None:
    """`!Join [delim, list]` → long form."""
    f = tmp_path / "stack.yaml"
    f.write_text(
        "Resources:\n"
        "  Bucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      BucketName:\n"
        "        !Join\n"
        "        - '-'\n"
        "        - - prefix\n"
        "          - suffix\n"
    )
    resources = parse_cfn_file(f)
    assert resources[0].properties == {"BucketName": {"Fn::Join": ["-", ["prefix", "suffix"]]}}


def test_intrinsic_value_of_in_rules_section(tmp_path: Path) -> None:
    """`!ValueOf` is a Rules-section intrinsic — must parse without crashing.

    Regression for v0.1.103 QA finding: aws-quickstart/quickstart-aws-aurora-
    postgresql ships a `Rules:` block using `!ValueOf` for parameter
    validation. Pre-v0.1.103 the parser crashed with
    "could not determine a constructor for the tag '!ValueOf'" and
    silently dropped the whole template.
    """
    f = tmp_path / "stack.yaml"
    f.write_text(
        "Resources:\n"
        "  Bucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties: {}\n"
        "Rules:\n"
        "  SubnetsInVPC:\n"
        "    Assertions:\n"
        "      - Assert: !Equals [!ValueOf [Subnet1ID, VpcId], !Ref VpcId]\n"
        "        AssertDescription: All subnets must be in the same VPC\n"
    )
    # The whole template should parse — Rules section presence shouldn't
    # block resource extraction. We assert resources[0] exists and is the bucket.
    resources = parse_cfn_file(f)
    assert len(resources) == 1
    assert resources[0].type == "AWS::S3::Bucket"


def test_intrinsic_rules_section_others(tmp_path: Path) -> None:
    """Other Rules-section intrinsics also parse: !RefAll, !EachMemberEquals, etc."""
    f = tmp_path / "stack.yaml"
    f.write_text(
        "Resources:\n"
        "  Bucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties: {}\n"
        "Rules:\n"
        "  AllSubnetsValid:\n"
        "    Assertions:\n"
        "      - Assert: !EachMemberEquals [!RefAll AWS::EC2::Subnet::Id, foo]\n"
        "      - Assert: !Contains [[a, b, c], !ValueOfAll [Param, Default]]\n"
        "      - Assert: !EachMemberIn [!RefAll AWS::EC2::Subnet::Id, [foo, bar]]\n"
    )
    resources = parse_cfn_file(f)
    assert len(resources) == 1


def test_non_cfn_yaml_returns_empty(tmp_path: Path) -> None:
    """YAML files without `Resources` / `AWSTemplateFormatVersion` are not CFN.

    A k8s manifest or config file should parse to empty (silent skip),
    NOT raise.
    """
    f = tmp_path / "kubernetes.yaml"
    f.write_text("apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: foo\n")
    assert parse_cfn_file(f) == []


def test_malformed_yaml_raises(tmp_path: Path) -> None:
    """Genuinely broken YAML raises DetectorError."""
    f = tmp_path / "broken.yaml"
    f.write_text(
        "Resources:\n"
        "  MyBucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      BucketName: [unclosed\n"
    )
    with pytest.raises(DetectorError, match="CFN parse error"):
        parse_cfn_file(f)


def test_parse_tree_walks_yaml_and_json(tmp_path: Path) -> None:
    """`parse_cfn_tree` finds CFN files of either extension under target."""
    (tmp_path / "yaml_stack.yaml").write_text(
        "Resources:\n  A: {Type: AWS::S3::Bucket, Properties: {}}\n"
    )
    (tmp_path / "json_stack.json").write_text(
        '{"Resources": {"B": {"Type": "AWS::SNS::Topic", "Properties": {}}}}'
    )
    (tmp_path / "k8s.yaml").write_text("apiVersion: v1\nkind: Pod\n")
    result = parse_cfn_tree(tmp_path)
    assert result.files_scanned == 3
    assert len(result.resources) == 2
    types = {r.type for r in result.resources}
    assert types == {"AWS::S3::Bucket", "AWS::SNS::Topic"}


def test_parse_tree_skips_hidden_dirs(tmp_path: Path) -> None:
    """`.git/` and similar hidden dirs are skipped during the walk."""
    hidden = tmp_path / ".git" / "objects"
    hidden.mkdir(parents=True)
    (hidden / "stack.yaml").write_text("Resources:\n  X: {Type: AWS::S3::Bucket, Properties: {}}\n")
    visible = tmp_path / "infra"
    visible.mkdir()
    (visible / "stack.yaml").write_text(
        "Resources:\n  Y: {Type: AWS::S3::Bucket, Properties: {}}\n"
    )
    result = parse_cfn_tree(tmp_path)
    # Only the non-hidden one is picked up.
    assert len(result.resources) == 1
    assert result.resources[0].logical_id == "Y"


def test_parse_tree_collects_failures(tmp_path: Path) -> None:
    """One malformed file in a tree doesn't block the rest."""
    (tmp_path / "good.yaml").write_text(
        "Resources:\n  A: {Type: AWS::S3::Bucket, Properties: {}}\n"
    )
    (tmp_path / "broken.yaml").write_text(
        "Resources:\n  B:\n    Type: AWS::S3::Bucket\n    Properties: [unclosed\n"
    )
    result = parse_cfn_tree(tmp_path)
    assert len(result.resources) == 1  # good.yaml's A
    assert len(result.parse_failures) == 1
    assert result.parse_failures[0].file.name == "broken.yaml"


def test_safeloader_subclass_does_not_pollute_global_yaml(tmp_path: Path) -> None:
    """The CFN loader doesn't leak `!Ref` into yaml.SafeLoader.

    Critical: efterlev's manifest loader uses the standard SafeLoader.
    If we accidentally mutated it, manifest YAMLs with stray `!Ref`-style
    custom tags would silently parse as CFN intrinsics. This test pins
    the subclass-not-mutate posture.
    """
    import yaml

    assert _CfnSafeLoader is not yaml.SafeLoader

    # A document that has `!Ref` but is NOT being parsed by the CFN loader
    # should fail with the standard loader (since `!Ref` is non-standard).
    f = tmp_path / "ref.yaml"
    f.write_text("foo: !Ref BarParam\n")
    with pytest.raises(yaml.YAMLError):
        yaml.safe_load(f.read_text())
