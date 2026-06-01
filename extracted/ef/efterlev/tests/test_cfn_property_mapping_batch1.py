"""Tests for PR gamma.2 batch 1 mappings (v0.1.74).

Adds: AWS::EC2::FlowLog, AWS::EC2::SecurityGroup, AWS::EC2::Volume,
AWS::Logs::LogGroup.

Includes the first integration test that runs a real detector
(`aws.vpc_flow_logs_enabled`) against the existing `aws-vpc-cfn`
vendored fixture — validating that property-mapping makes the
plumbing-shipped-in-v0.1.72 actually emit Evidence on real input.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cloudformation import (
    adapt_cfn_resources,
    apply_mapping,
    parse_cfn_file,
    parse_cfn_tree,
)
from efterlev.detectors.aws.encryption_ebs import detector as ebs_detector
from efterlev.detectors.aws.security_group_open_ingress import detector as sg_detector
from efterlev.detectors.aws.vpc_flow_logs_enabled import detector as flow_log_detector

# --- AWS::EC2::FlowLog -----------------------------------------------------


def test_flow_log_dispatches_resource_type_vpc() -> None:
    """ResourceType=VPC + ResourceId → vpc_id field."""
    [m] = apply_mapping(
        "AWS::EC2::FlowLog",
        {
            "ResourceType": "VPC",
            "ResourceId": "vpc-abc123",
            "TrafficType": "ALL",
            "LogDestinationType": "s3",
            "LogDestination": "arn:aws:s3:::my-bucket/prefix",
        },
    )
    assert m.tf_type == "aws_flow_log"
    assert m.body == {
        "vpc_id": "vpc-abc123",
        "traffic_type": "ALL",
        "log_destination_type": "s3",
        "log_destination": "arn:aws:s3:::my-bucket/prefix",
    }


def test_flow_log_dispatches_resource_type_subnet() -> None:
    """ResourceType=Subnet → subnet_id field."""
    [m] = apply_mapping(
        "AWS::EC2::FlowLog",
        {
            "ResourceType": "Subnet",
            "ResourceId": "subnet-xyz",
            "TrafficType": "REJECT",
        },
    )
    assert m.body["subnet_id"] == "subnet-xyz"
    assert "vpc_id" not in m.body
    assert "eni_id" not in m.body


def test_flow_log_dispatches_resource_type_eni() -> None:
    """ResourceType=NetworkInterface → eni_id field."""
    [m] = apply_mapping(
        "AWS::EC2::FlowLog",
        {"ResourceType": "NetworkInterface", "ResourceId": "eni-aaa"},
    )
    assert m.body["eni_id"] == "eni-aaa"


def test_flow_log_unknown_resource_type_drops_target_field() -> None:
    """Unknown ResourceType → no target field set; detector handles as 'unknown'."""
    [m] = apply_mapping(
        "AWS::EC2::FlowLog",
        {"ResourceType": "WeirdType", "ResourceId": "x"},
    )
    assert "vpc_id" not in m.body
    assert "subnet_id" not in m.body
    assert "eni_id" not in m.body


def test_flow_log_parity_with_real_detector(tmp_path: Path) -> None:
    """`aws.vpc_flow_logs_enabled` emits the same Evidence on CFN as on TF equivalent."""
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  VpcFlowLog:\n"
        "    Type: AWS::EC2::FlowLog\n"
        "    Properties:\n"
        "      ResourceType: VPC\n"
        "      ResourceId: vpc-prod-1\n"
        "      TrafficType: ALL\n"
        "      LogDestinationType: cloud-watch-logs\n"
        "      LogGroupName: /aws/vpc/flowlogs\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn_path), scan_root=tmp_path)
    evidence = flow_log_detector.detect(tf_resources)
    assert len(evidence) == 1
    e = evidence[0]
    assert e.content["target_kind"] == "vpc"
    assert e.content["target_ref"] == "vpc-prod-1"
    assert e.content["traffic_type"] == "ALL"
    assert e.content["destination_type"] == "cloud-watch-logs"


# --- AWS::EC2::SecurityGroup -----------------------------------------------


def test_security_group_basic_translation() -> None:
    """GroupName/GroupDescription/VpcId rename simply."""
    [m] = apply_mapping(
        "AWS::EC2::SecurityGroup",
        {
            "GroupName": "web-tier",
            "GroupDescription": "allow public web",
            "VpcId": "vpc-1",
        },
    )
    assert m.tf_type == "aws_security_group"
    assert m.body["name"] == "web-tier"
    assert m.body["description"] == "allow public web"
    assert m.body["vpc_id"] == "vpc-1"


def test_security_group_ingress_open_to_world_translates_to_tf_shape() -> None:
    """CFN scalar CidrIp → TF cidr_blocks list — what the detector expects."""
    [m] = apply_mapping(
        "AWS::EC2::SecurityGroup",
        {
            "GroupName": "ssh-open",
            "GroupDescription": "SSH open to world (the exact misconfig the detector catches)",
            "SecurityGroupIngress": [
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "CidrIp": "0.0.0.0/0",
                }
            ],
        },
    )
    ingress = m.body["ingress"]
    assert isinstance(ingress, list)
    assert len(ingress) == 1
    rule = ingress[0]
    assert rule == {
        "cidr_blocks": ["0.0.0.0/0"],
        "from_port": 22,
        "to_port": 22,
        "protocol": "tcp",
    }


def test_security_group_parity_with_open_ingress_detector(tmp_path: Path) -> None:
    """`aws.security_group_open_ingress` flags an SSH-to-world CFN SG just like TF."""
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  OpenSshSg:\n"
        "    Type: AWS::EC2::SecurityGroup\n"
        "    Properties:\n"
        "      GroupName: open-ssh\n"
        "      GroupDescription: SSH wide-open\n"
        "      VpcId: vpc-1\n"
        "      SecurityGroupIngress:\n"
        "        - IpProtocol: tcp\n"
        "          FromPort: 22\n"
        "          ToPort: 22\n"
        "          CidrIp: 0.0.0.0/0\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn_path), scan_root=tmp_path)
    evidence = sg_detector.detect(tf_resources)
    assert len(evidence) == 1
    e = evidence[0]
    assert e.content["exposure_state"] == "open_to_world"
    assert e.content["from_port"] == 22
    assert e.content["to_port"] == 22
    assert e.content["protocol"] == "tcp"
    assert e.content["open_ipv4"] is True


def test_security_group_https_to_world_passes() -> None:
    """HTTPS-to-world is intentional, not a finding (parity with TF behavior)."""
    [m] = apply_mapping(
        "AWS::EC2::SecurityGroup",
        {
            "GroupName": "web",
            "GroupDescription": "public web",
            "SecurityGroupIngress": [
                {
                    "IpProtocol": "tcp",
                    "FromPort": 443,
                    "ToPort": 443,
                    "CidrIp": "0.0.0.0/0",
                }
            ],
        },
    )
    # No Evidence because port 443 is in the public-web allowlist.
    from efterlev.models import SourceRef, TerraformResource

    tf = TerraformResource(
        type=m.tf_type or "aws_security_group",
        name="web",
        body=m.body,
        source_ref=SourceRef(file=Path("stack.yaml"), line_start=None, line_end=None),
        kind="resource",
    )
    assert sg_detector.detect([tf]) == []


# --- AWS::EC2::Volume ------------------------------------------------------


def test_volume_encrypted_with_kms() -> None:
    """Encrypted+KmsKeyId rename simply."""
    [m] = apply_mapping(
        "AWS::EC2::Volume",
        {
            "Encrypted": True,
            "KmsKeyId": "arn:aws:kms:us-east-1:123:key/abc",
            "Size": 100,
            "VolumeType": "gp3",
        },
    )
    assert m.tf_type == "aws_ebs_volume"
    assert m.body == {
        "encrypted": True,
        "kms_key_id": "arn:aws:kms:us-east-1:123:key/abc",
        "size": 100,
        "type": "gp3",
    }


def test_volume_encryption_detector_parity(tmp_path: Path) -> None:
    """`aws.encryption_ebs` accepts the CFN-translated body shape."""
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  EncryptedVol:\n"
        "    Type: AWS::EC2::Volume\n"
        "    Properties:\n"
        "      AvailabilityZone: us-east-1a\n"
        "      Size: 100\n"
        "      Encrypted: true\n"
        "      KmsKeyId: arn:aws:kms:us-east-1:123:key/abc\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn_path), scan_root=tmp_path)
    evidence = ebs_detector.detect(tf_resources)
    # Detector emits something — we don't lock the exact content shape since
    # encryption_ebs is structurally complex; we just assert it sees the
    # resource and emits a record (the TF-equivalent does the same).
    assert len(evidence) == 1


# --- AWS::Logs::LogGroup ---------------------------------------------------


def test_log_group_translates_with_canonical_tf_type() -> None:
    """AWS::Logs::LogGroup → aws_cloudwatch_log_group (NOT default aws_logs_loggroup)."""
    [m] = apply_mapping(
        "AWS::Logs::LogGroup",
        {"LogGroupName": "/aws/lambda/my-func", "RetentionInDays": 30},
    )
    assert m.tf_type == "aws_cloudwatch_log_group"
    assert m.body == {
        "name": "/aws/lambda/my-func",
        "retention_in_days": 30,
    }


# --- Integration: aws-vpc-cfn vendored fixture ----------------------------


def test_aws_vpc_cfn_fixture_emits_flow_log_evidence() -> None:
    """The PR β-shipped vendored CFN fixture now emits real Evidence at v0.1.74.

    This is the v0.1.72→v0.1.74 closure: parser shipped at v0.1.72,
    but adapter had no property mapping for AWS::EC2::FlowLog → no
    Evidence. With the v0.1.74 mapping, parsing the same vendored file
    + running the same detector now emits a real Evidence record.
    """
    fixture_dir = Path(__file__).parent.parent / "evals" / "fixtures" / "aws-vpc-cfn" / "infra"
    parse_result = parse_cfn_tree(fixture_dir)
    tf_resources = adapt_cfn_resources(parse_result.resources, scan_root=fixture_dir)

    # The vendored fixture has 1 AWS::EC2::FlowLog → should yield 1 evidence.
    flow_log_evidence = flow_log_detector.detect(tf_resources)
    assert len(flow_log_evidence) == 1
    e = flow_log_evidence[0]
    # The aws-vpc-cfn flow log targets the VPC.
    assert e.content["target_kind"] == "vpc"


# --- Coverage list pin update ----------------------------------------------


def test_v0_1_74_batch1_coverage_subset_still_present() -> None:
    """The 4 batch-1 resource types must remain in the registry across batches.

    Same "subset present" pattern as the v0.1.73 pin — each batch test
    file keeps its slice honest without breaking on later additions.
    """
    from efterlev.cloudformation.property_mapping import mapped_cfn_types

    coverage = set(mapped_cfn_types())
    assert {
        "AWS::EC2::FlowLog",
        "AWS::EC2::SecurityGroup",
        "AWS::EC2::Volume",
        "AWS::Logs::LogGroup",
    }.issubset(coverage)
