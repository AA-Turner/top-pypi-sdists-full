"""Tests for PR gamma.2 batch 2 mappings (v0.1.75) — IAM family.

Adds: AWS::IAM::Role, AWS::IAM::ManagedPolicy, AWS::IAM::User. Each of
Role and User uses the 1→(1+N+M) sub-resource synthesis pattern: CFN
bundles managed-policy attachments + inline policies into the
principal's own properties; TF separates them.

Per-detector parity:
- aws.iam_admin_policy_usage reads aws_iam_role_policy_attachment;
  CFN's inline ManagedPolicyArns must synthesize attachments to make
  this fire.
- aws.iam_inline_policies_audit reads aws_iam_role_policy; CFN's
  inline Policies must synthesize per-policy resources.
"""

from __future__ import annotations

import json
from pathlib import Path

from efterlev.cloudformation import adapt_cfn_resources, apply_mapping, parse_cfn_file
from efterlev.detectors.aws.iam_admin_policy_usage import detector as admin_detector
from efterlev.detectors.aws.iam_inline_policies_audit import detector as inline_detector

_ADMIN_ARN = "arn:aws:iam::aws:policy/AdministratorAccess"


# --- AWS::IAM::Role basic translation -------------------------------------


def test_iam_role_basic_fields() -> None:
    """RoleName/Path/Description rename simply."""
    mapped = apply_mapping(
        "AWS::IAM::Role",
        {
            "RoleName": "deploy-bot",
            "Path": "/automation/",
            "Description": "CI deploy role",
            "MaxSessionDuration": 3600,
        },
    )
    assert len(mapped) == 1
    role = mapped[0]
    assert role.tf_type == "aws_iam_role"
    assert role.body["name"] == "deploy-bot"
    assert role.body["path"] == "/automation/"
    assert role.body["description"] == "CI deploy role"
    assert role.body["max_session_duration"] == 3600


def test_iam_role_assume_role_policy_dict_to_json() -> None:
    """AssumeRolePolicyDocument dict → assume_role_policy JSON-string."""
    arpd = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }
    [role] = apply_mapping(
        "AWS::IAM::Role",
        {"RoleName": "ec2-role", "AssumeRolePolicyDocument": arpd},
    )
    assert isinstance(role.body["assume_role_policy"], str)
    assert json.loads(role.body["assume_role_policy"]) == arpd


# --- AWS::IAM::Role 1→1+N synthesis (managed policy attachments) ----------


def test_iam_role_synthesizes_attachment_per_managed_policy_arn() -> None:
    """ManagedPolicyArns: [arn1, arn2] → role + 2 attachments."""
    mapped = apply_mapping(
        "AWS::IAM::Role",
        {
            "RoleName": "audit",
            "ManagedPolicyArns": [
                "arn:aws:iam::aws:policy/ReadOnlyAccess",
                _ADMIN_ARN,
            ],
        },
    )
    assert len(mapped) == 3
    role, attach0, attach1 = mapped
    assert role.tf_type == "aws_iam_role"
    assert attach0.tf_type == "aws_iam_role_policy_attachment"
    assert attach0.name_suffix == "_attach_0"
    assert attach0.body == {"policy_arn": "arn:aws:iam::aws:policy/ReadOnlyAccess"}
    assert attach1.body == {"policy_arn": _ADMIN_ARN}
    assert attach1.name_suffix == "_attach_1"


def test_iam_admin_attachment_detected_via_synthesis(tmp_path: Path) -> None:
    """The full closure: CFN role with AdministratorAccess inline → admin detector fires."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  BreakGlass:\n"
        "    Type: AWS::IAM::Role\n"
        "    Properties:\n"
        "      RoleName: break-glass\n"
        "      ManagedPolicyArns:\n"
        f"        - {_ADMIN_ARN}\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    assert len(tf_resources) == 2  # role + 1 synthesized attachment

    evidence = admin_detector.detect(tf_resources)
    assert len(evidence) == 1
    e = evidence[0]
    assert e.content["resource_type"] == "aws_iam_role_policy_attachment"


def test_iam_role_no_attachment_for_non_admin_arn(tmp_path: Path) -> None:
    """Read-only managed policy doesn't fire admin detector (negative parity)."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  AuditRole:\n"
        "    Type: AWS::IAM::Role\n"
        "    Properties:\n"
        "      RoleName: audit\n"
        "      ManagedPolicyArns:\n"
        "        - arn:aws:iam::aws:policy/ReadOnlyAccess\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    assert admin_detector.detect(tf_resources) == []


# --- AWS::IAM::Role 1→1+M synthesis (inline policies) ---------------------


def test_iam_role_synthesizes_inline_policy_per_policies_entry() -> None:
    """Policies: [{PolicyName, PolicyDocument}] → role + N inline-policy resources."""
    inline_doc = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Action": "s3:GetObject", "Resource": "*"}],
    }
    mapped = apply_mapping(
        "AWS::IAM::Role",
        {
            "RoleName": "data-reader",
            "Policies": [
                {"PolicyName": "S3Read", "PolicyDocument": inline_doc},
            ],
        },
    )
    assert len(mapped) == 2
    role, inline = mapped
    assert role.tf_type == "aws_iam_role"
    assert inline.tf_type == "aws_iam_role_policy"
    assert inline.name_suffix == "_inline_S3Read"
    assert inline.body["name"] == "S3Read"
    assert json.loads(inline.body["policy"]) == inline_doc


def test_iam_inline_audit_detector_fires_on_synthesized(tmp_path: Path) -> None:
    """The closure: CFN inline Policies → inline-audit detector fires per entry."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  RoleWithInline:\n"
        "    Type: AWS::IAM::Role\n"
        "    Properties:\n"
        "      RoleName: role-with-inline\n"
        "      Policies:\n"
        "        - PolicyName: AllowS3\n"
        "          PolicyDocument:\n"
        "            Version: '2012-10-17'\n"
        "            Statement:\n"
        "              - Effect: Allow\n"
        "                Action: s3:GetObject\n"
        "                Resource: '*'\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = inline_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_iam_role_policy"


# --- AWS::IAM::Role both attachments AND inline policies (1→1+N+M) --------


def test_iam_role_combined_synthesis() -> None:
    """ManagedPolicyArns + Policies both present → role + N attachments + M inline."""
    mapped = apply_mapping(
        "AWS::IAM::Role",
        {
            "RoleName": "kitchen-sink",
            "ManagedPolicyArns": [_ADMIN_ARN, "arn:aws:iam::aws:policy/ReadOnlyAccess"],
            "Policies": [
                {
                    "PolicyName": "Custom1",
                    "PolicyDocument": {"Version": "2012-10-17", "Statement": []},
                },
                {
                    "PolicyName": "Custom2",
                    "PolicyDocument": {"Version": "2012-10-17", "Statement": []},
                },
            ],
        },
    )
    # 1 role + 2 attachments + 2 inline policies = 5 total
    assert len(mapped) == 5
    types = [m.tf_type for m in mapped]
    assert types.count("aws_iam_role") == 1
    assert types.count("aws_iam_role_policy_attachment") == 2
    assert types.count("aws_iam_role_policy") == 2


# --- AWS::IAM::ManagedPolicy ----------------------------------------------


def test_managed_policy_translates_to_aws_iam_policy() -> None:
    """AWS::IAM::ManagedPolicy → aws_iam_policy (NOT default aws_iam_managedpolicy)."""
    [m] = apply_mapping(
        "AWS::IAM::ManagedPolicy",
        {
            "ManagedPolicyName": "S3ReadOnly",
            "Description": "S3 read everywhere",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [{"Effect": "Allow", "Action": "s3:Get*", "Resource": "*"}],
            },
        },
    )
    assert m.tf_type == "aws_iam_policy"
    assert m.body["name"] == "S3ReadOnly"
    assert m.body["description"] == "S3 read everywhere"
    assert "Statement" in m.body["policy"]


# --- AWS::IAM::User -------------------------------------------------------


def test_iam_user_synthesizes_attachments() -> None:
    """User-side ManagedPolicyArns → 1 user + N user_policy_attachment."""
    mapped = apply_mapping(
        "AWS::IAM::User",
        {
            "UserName": "admin-user",
            "ManagedPolicyArns": [_ADMIN_ARN],
        },
    )
    assert len(mapped) == 2
    user, attach = mapped
    assert user.tf_type == "aws_iam_user"
    assert user.body["name"] == "admin-user"
    assert attach.tf_type == "aws_iam_user_policy_attachment"
    assert attach.body["policy_arn"] == _ADMIN_ARN


def test_iam_user_admin_attachment_fires_admin_detector(tmp_path: Path) -> None:
    """User+AdministratorAccess fires the admin detector via synthesized attachment."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  AdminUser:\n"
        "    Type: AWS::IAM::User\n"
        "    Properties:\n"
        "      UserName: emergency-admin\n"
        "      ManagedPolicyArns:\n"
        f"        - {_ADMIN_ARN}\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = admin_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_iam_user_policy_attachment"


# --- Coverage list pin update ----------------------------------------------


def test_v0_1_75_batch2_coverage_subset_still_present() -> None:
    """The 3 IAM batch-2 resource types must remain present across future batches."""
    from efterlev.cloudformation.property_mapping import mapped_cfn_types

    coverage = set(mapped_cfn_types())
    assert {
        "AWS::IAM::ManagedPolicy",
        "AWS::IAM::Role",
        "AWS::IAM::User",
    }.issubset(coverage)
