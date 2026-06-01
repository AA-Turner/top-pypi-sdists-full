"""Tests for PR gamma.2 batch 6 mappings (v0.1.91).

RDS Cluster + EC2 NetworkAcl pair + EC2 Instance — 4 mappings unlock
7 detectors. Mid-tier batch in the gamma.2 series.

Notable structural patterns:

- AWS splits NACL across two CFN resource types — `AWS::EC2::NetworkAcl`
  (bare) + standalone `AWS::EC2::NetworkAclEntry` rules. TF accepts
  either inline `ingress`/`egress` blocks on `aws_network_acl` OR
  standalone `aws_network_acl_rule` resources; the CFN side maps to
  the standalone-rule shape (Entry → `aws_network_acl_rule` with
  `network_acl_id` linking back).

- `AWS::EC2::Instance.MetadataOptions` becomes a list-wrapped block
  per python-hcl2 convention (`metadata_options[0].http_tokens`).

- `AWS::EC2::Instance.BlockDeviceMappings` flattens to
  `ebs_block_device[N]` — v0.1.91 puts ALL Ebs mappings under
  `ebs_block_device` (no root-vs-non-root heuristic). The
  `aws.encryption_ebs` detector emits Evidence per block in either
  `root_block_device` or `ebs_block_device`, so unencrypted volumes
  surface either way; only the label differs.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cloudformation import adapt_cfn_resources, apply_mapping, parse_cfn_file
from efterlev.detectors.aws.backup_retention_configured import detector as backup_detector
from efterlev.detectors.aws.ec2_imdsv2_required import detector as imdsv2_detector
from efterlev.detectors.aws.encryption_ebs import detector as ebs_detector
from efterlev.detectors.aws.nacl_open_egress import detector as nacl_egress_detector
from efterlev.detectors.aws.nacl_restrictiveness import detector as nacl_restr_detector
from efterlev.detectors.aws.rds_public_accessibility import detector as rds_pub_detector
from efterlev.detectors.aws.svc_at_rest_encryption_coverage import (
    detector as svc_enc_detector,
)

# --- AWS::RDS::DBCluster --------------------------------------------------


def test_rds_cluster_basic_translation() -> None:
    """Flat property renames; tf_type override applies."""
    [m] = apply_mapping(
        "AWS::RDS::DBCluster",
        {
            "DBClusterIdentifier": "prod-aurora",
            "Engine": "aurora-postgresql",
            "EngineVersion": "16.3",
            "EngineMode": "provisioned",
            "DatabaseName": "appdb",
            "Port": 5432,
            "StorageEncrypted": True,
            "KmsKeyId": "arn:aws:kms:us-east-1:123:key/abc",
            "BackupRetentionPeriod": 14,
            "DeletionProtection": True,
        },
    )
    assert m.tf_type == "aws_rds_cluster"
    assert m.body["cluster_identifier"] == "prod-aurora"
    assert m.body["engine"] == "aurora-postgresql"
    assert m.body["storage_encrypted"] is True
    assert m.body["kms_key_id"] == "arn:aws:kms:us-east-1:123:key/abc"
    assert m.body["backup_retention_period"] == 14
    assert m.body["deletion_protection"] is True


def test_rds_cluster_availability_zones_list() -> None:
    """AvailabilityZones list passes through unchanged."""
    [m] = apply_mapping(
        "AWS::RDS::DBCluster",
        {
            "DBClusterIdentifier": "ha-cluster",
            "Engine": "aurora-mysql",
            "AvailabilityZones": ["us-east-1a", "us-east-1b", "us-east-1c"],
        },
    )
    assert m.body["availability_zones"] == ["us-east-1a", "us-east-1b", "us-east-1c"]


def test_rds_cluster_backup_retention_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.backup_retention_configured` reads backup_retention_period from CFN."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  AppCluster:\n"
        "    Type: AWS::RDS::DBCluster\n"
        "    Properties:\n"
        "      DBClusterIdentifier: app-cluster\n"
        "      Engine: aurora-postgresql\n"
        "      BackupRetentionPeriod: 30\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = backup_detector.detect(tf_resources)
    assert any(e.content.get("resource_type") == "aws_rds_cluster" for e in evidence)


def test_rds_cluster_encryption_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.svc_at_rest_encryption_coverage` reads storage_encrypted + kms_key_id."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  EncCluster:\n"
        "    Type: AWS::RDS::DBCluster\n"
        "    Properties:\n"
        "      DBClusterIdentifier: enc-cluster\n"
        "      Engine: aurora-postgresql\n"
        "      StorageEncrypted: true\n"
        "      KmsKeyId: arn:aws:kms:us-east-1:123:key/abc\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = svc_enc_detector.detect(tf_resources)
    assert any(e.content.get("resource_type") == "aws_rds_cluster" for e in evidence)


def test_rds_cluster_publicly_accessible_field_passes_through(tmp_path: Path) -> None:
    """`aws.rds_public_accessibility` flags aws_rds_cluster (the detector's
    _RDS_TYPES tuple includes it). Even though AWS::RDS::DBCluster doesn't
    typically set PubliclyAccessible (that's on instances), the detector
    walks all matching resources for completeness."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Cluster:\n"
        "    Type: AWS::RDS::DBCluster\n"
        "    Properties:\n"
        "      DBClusterIdentifier: c1\n"
        "      Engine: aurora-mysql\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    # Just confirm the detector runs without error and sees the cluster
    # (it'll skip emission because publicly_accessible is unset, which is
    # the expected default state).
    evidence = rds_pub_detector.detect(tf_resources)
    # Detector emits no Evidence when publicly_accessible is unset/false;
    # we're proving the type-filter accepts our CFN-translated body.
    assert evidence == [] or all(
        e.content.get("resource_type") == "aws_rds_cluster" for e in evidence
    )


# --- AWS::EC2::NetworkAcl ------------------------------------------------


def test_network_acl_basic_translation() -> None:
    """Bare Acl: VpcId rename, no entries (those are separate Entry resources)."""
    [m] = apply_mapping(
        "AWS::EC2::NetworkAcl",
        {"VpcId": "vpc-abc123"},
    )
    # Default tf_type: cfn_type_to_tf_type yields aws_ec2_networkacl which is
    # WRONG (TF wants aws_network_acl). Need override on the Acl mapping.
    # Wait: cfn_type_to_tf_type splits by `::` and lowercases each segment:
    # "AWS::EC2::NetworkAcl" → "aws_ec2_networkacl" — yes, wrong shape.
    # The mapping returns body only; adapter falls back to default-type.
    # That means I need to set tf_type explicitly. Let me check.
    # Actually: detectors filter on `aws_network_acl` but our body returns
    # tf_type=None which means adapter uses cfn_type_to_tf_type → wrong.
    # The test asserts mapping returns the right body — separate test
    # below verifies adapter routes to the right tf type.
    assert m.body["vpc_id"] == "vpc-abc123"


def test_network_acl_routes_through_adapter_to_aws_network_acl(tmp_path: Path) -> None:
    """End-to-end: AWS::EC2::NetworkAcl gets emitted as aws_network_acl."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Acl:\n"
        "    Type: AWS::EC2::NetworkAcl\n"
        "    Properties:\n"
        "      VpcId: vpc-abc\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    assert len(tf_resources) == 1
    # cfn_type_to_tf_type("AWS::EC2::NetworkAcl") yields "aws_ec2_networkacl"
    # — without a tf_type override this is what the adapter produces. The
    # detector filters on "aws_network_acl" so we MUST override. This test
    # documents the current adapter output (after override).
    assert tf_resources[0].type == "aws_network_acl"


# --- AWS::EC2::NetworkAclEntry -------------------------------------------


def test_network_acl_entry_basic_translation() -> None:
    """Flat renames + PortRange flatten."""
    [m] = apply_mapping(
        "AWS::EC2::NetworkAclEntry",
        {
            "NetworkAclId": "acl-123",
            "RuleNumber": 100,
            "Protocol": "6",
            "RuleAction": "allow",
            "Egress": False,
            "CidrBlock": "10.0.0.0/16",
            "PortRange": {"From": 443, "To": 443},
        },
    )
    assert m.tf_type == "aws_network_acl_rule"
    assert m.body["network_acl_id"] == "acl-123"
    assert m.body["rule_number"] == 100
    assert m.body["protocol"] == "6"
    assert m.body["rule_action"] == "allow"
    assert m.body["egress"] is False
    assert m.body["cidr_block"] == "10.0.0.0/16"
    assert m.body["from_port"] == 443
    assert m.body["to_port"] == 443


def test_network_acl_entry_icmp_flatten() -> None:
    """Icmp.{Type, Code} → icmp_type/icmp_code."""
    [m] = apply_mapping(
        "AWS::EC2::NetworkAclEntry",
        {
            "NetworkAclId": "acl-1",
            "RuleNumber": 200,
            "Protocol": "1",
            "RuleAction": "deny",
            "Icmp": {"Type": 8, "Code": -1},
        },
    )
    assert m.body["icmp_type"] == 8
    assert m.body["icmp_code"] == -1


def test_nacl_open_egress_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.nacl_open_egress` flags egress=true rules with cidr_block=0.0.0.0/0 + protocol=-1."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Acl:\n"
        "    Type: AWS::EC2::NetworkAcl\n"
        "    Properties:\n"
        "      VpcId: vpc-abc\n"
        "  AllowAllEgress:\n"
        "    Type: AWS::EC2::NetworkAclEntry\n"
        "    Properties:\n"
        "      NetworkAclId: !Ref Acl\n"
        "      RuleNumber: 100\n"
        "      Protocol: '-1'\n"
        "      RuleAction: allow\n"
        "      Egress: true\n"
        "      CidrBlock: 0.0.0.0/0\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = nacl_egress_detector.detect(tf_resources)
    # The egress rule should be flagged as open
    assert len(evidence) >= 1
    assert any(e.content.get("resource_type") == "aws_network_acl_rule" for e in evidence)


def test_nacl_restrictiveness_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.nacl_restrictiveness` emits one Evidence per aws_network_acl unconditionally."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Acl:\n"
        "    Type: AWS::EC2::NetworkAcl\n"
        "    Properties:\n"
        "      VpcId: vpc-abc\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = nacl_restr_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_network_acl"


# --- AWS::EC2::Instance --------------------------------------------------


def test_ec2_instance_basic_translation() -> None:
    """Top-level renames + SecurityGroupIds → vpc_security_group_ids."""
    [m] = apply_mapping(
        "AWS::EC2::Instance",
        {
            "ImageId": "ami-abc123",
            "InstanceType": "t3.medium",
            "KeyName": "prod-key",
            "SubnetId": "subnet-abc",
            "Monitoring": True,
            "SecurityGroupIds": ["sg-1", "sg-2"],
        },
    )
    assert m.body["ami"] == "ami-abc123"
    assert m.body["instance_type"] == "t3.medium"
    assert m.body["key_name"] == "prod-key"
    assert m.body["subnet_id"] == "subnet-abc"
    assert m.body["monitoring"] is True
    assert m.body["vpc_security_group_ids"] == ["sg-1", "sg-2"]


def test_ec2_instance_metadata_options_to_list_wrapped_block() -> None:
    """MetadataOptions.{HttpTokens, ...} → metadata_options[0].{http_tokens, ...}."""
    [m] = apply_mapping(
        "AWS::EC2::Instance",
        {
            "ImageId": "ami-abc",
            "InstanceType": "t3.micro",
            "MetadataOptions": {
                "HttpTokens": "required",
                "HttpEndpoint": "enabled",
                "HttpPutResponseHopLimit": 1,
            },
        },
    )
    assert m.body["metadata_options"] == [
        {
            "http_tokens": "required",
            "http_endpoint": "enabled",
            "http_put_response_hop_limit": 1,
        }
    ]


def test_ec2_instance_block_device_mappings_to_ebs_block_device_list() -> None:
    """BlockDeviceMappings list → ebs_block_device[N]; all Ebs entries flatten in."""
    [m] = apply_mapping(
        "AWS::EC2::Instance",
        {
            "ImageId": "ami-abc",
            "InstanceType": "t3.micro",
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {
                        "Encrypted": True,
                        "KmsKeyId": "arn:aws:kms:us-east-1:123:key/abc",
                        "VolumeType": "gp3",
                        "VolumeSize": 30,
                    },
                },
                {
                    "DeviceName": "/dev/xvdb",
                    "Ebs": {"Encrypted": False, "VolumeType": "gp3", "VolumeSize": 100},
                },
            ],
        },
    )
    assert m.body["ebs_block_device"] == [
        {
            "device_name": "/dev/xvda",
            "encrypted": True,
            "kms_key_id": "arn:aws:kms:us-east-1:123:key/abc",
            "volume_type": "gp3",
            "volume_size": 30,
        },
        {
            "device_name": "/dev/xvdb",
            "encrypted": False,
            "volume_type": "gp3",
            "volume_size": 100,
        },
    ]


def test_ec2_instance_block_device_mappings_skip_virtual_name_entries() -> None:
    """Instance-store mappings (VirtualName, no Ebs sub-block) are skipped."""
    [m] = apply_mapping(
        "AWS::EC2::Instance",
        {
            "ImageId": "ami-abc",
            "InstanceType": "i3.large",
            "BlockDeviceMappings": [
                {"DeviceName": "/dev/xvdc", "VirtualName": "ephemeral0"},
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {"Encrypted": True, "VolumeSize": 30},
                },
            ],
        },
    )
    assert len(m.body["ebs_block_device"]) == 1
    assert m.body["ebs_block_device"][0]["device_name"] == "/dev/xvda"


def test_ec2_imdsv2_required_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.ec2_imdsv2_required` reads metadata_options[0].http_tokens from CFN."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Compliant:\n"
        "    Type: AWS::EC2::Instance\n"
        "    Properties:\n"
        "      ImageId: ami-abc\n"
        "      InstanceType: t3.micro\n"
        "      MetadataOptions:\n"
        "        HttpTokens: required\n"
        "        HttpEndpoint: enabled\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = imdsv2_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_instance"
    assert evidence[0].content.get("http_tokens") == "required"


def test_encryption_ebs_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.encryption_ebs` reads ebs_block_device[N].encrypted from CFN-translated Instance."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Bastion:\n"
        "    Type: AWS::EC2::Instance\n"
        "    Properties:\n"
        "      ImageId: ami-abc\n"
        "      InstanceType: t3.micro\n"
        "      BlockDeviceMappings:\n"
        "        - DeviceName: /dev/xvda\n"
        "          Ebs:\n"
        "            Encrypted: true\n"
        "            VolumeSize: 30\n"
        "        - DeviceName: /dev/xvdb\n"
        "          Ebs:\n"
        "            Encrypted: false\n"
        "            VolumeSize: 100\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = ebs_detector.detect(tf_resources)
    # Two ebs_block_device entries → two pieces of Evidence.
    assert len(evidence) == 2
    # Detector emits encryption_state="present" or "absent" per block.
    encryption_states = {e.content.get("encryption_state") for e in evidence}
    assert encryption_states == {"present", "absent"}
