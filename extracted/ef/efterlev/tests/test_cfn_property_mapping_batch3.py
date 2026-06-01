"""Tests for PR gamma.2 batch 3 mappings (v0.1.76) — KMS + RDS + Lambda.

The Lambda mapping introduces flat-dict-to-list-wrapped-block translation
for `Environment.Variables` and `VpcConfig`, mirroring python-hcl2's
`[{...}]` shape so detector helpers `_normalize_block` work uniformly.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cloudformation import adapt_cfn_resources, apply_mapping, parse_cfn_file
from efterlev.detectors.aws.kms_key_rotation import detector as kms_rotation_detector
from efterlev.detectors.aws.lambda_env_kms_encryption import detector as lambda_env_detector
from efterlev.detectors.aws.lambda_vpc_isolation import detector as lambda_vpc_detector
from efterlev.detectors.aws.rds_encryption_at_rest import detector as rds_enc_detector
from efterlev.detectors.aws.rds_public_accessibility import detector as rds_pub_detector

# --- AWS::KMS::Key ---------------------------------------------------------


def test_kms_key_basic_translation() -> None:
    """KeySpec → customer_master_key_spec; EnableKeyRotation → enable_key_rotation."""
    [m] = apply_mapping(
        "AWS::KMS::Key",
        {
            "Description": "data-tier KMS",
            "KeySpec": "SYMMETRIC_DEFAULT",
            "KeyUsage": "ENCRYPT_DECRYPT",
            "EnableKeyRotation": True,
            "MultiRegion": False,
        },
    )
    assert m.tf_type == "aws_kms_key"
    assert m.body["customer_master_key_spec"] == "SYMMETRIC_DEFAULT"
    assert m.body["key_usage"] == "ENCRYPT_DECRYPT"
    assert m.body["enable_key_rotation"] is True
    assert m.body["multi_region"] is False
    assert m.body["description"] == "data-tier KMS"


def test_kms_key_policy_dict_to_json() -> None:
    """KeyPolicy dict → policy JSON-string."""
    pol = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": "*", "Action": "kms:*", "Resource": "*"}],
    }
    [m] = apply_mapping("AWS::KMS::Key", {"KeyPolicy": pol})
    assert isinstance(m.body["policy"], str)
    assert "Statement" in m.body["policy"]


def test_kms_rotation_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.kms_key_rotation` reads `enable_key_rotation` — fires on CFN-translated body."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  AppKey:\n"
        "    Type: AWS::KMS::Key\n"
        "    Properties:\n"
        "      Description: app KMS\n"
        "      EnableKeyRotation: true\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = kms_rotation_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_kms_key"


# --- AWS::RDS::DBInstance --------------------------------------------------


def test_rds_basic_translation() -> None:
    """StorageEncrypted/KmsKeyId/PubliclyAccessible rename simply."""
    [m] = apply_mapping(
        "AWS::RDS::DBInstance",
        {
            "DBInstanceIdentifier": "prod-db",
            "DBInstanceClass": "db.r6g.large",
            "Engine": "postgres",
            "EngineVersion": "16.3",
            "AllocatedStorage": 100,
            "StorageEncrypted": True,
            "KmsKeyId": "arn:aws:kms:us-east-1:123:key/abc",
            "PubliclyAccessible": False,
            "MultiAZ": True,
            "BackupRetentionPeriod": 7,
            "DeletionProtection": True,
        },
    )
    assert m.tf_type == "aws_db_instance"
    assert m.body["storage_encrypted"] is True
    assert m.body["kms_key_id"] == "arn:aws:kms:us-east-1:123:key/abc"
    assert m.body["publicly_accessible"] is False
    assert m.body["multi_az"] is True
    assert m.body["backup_retention_period"] == 7
    assert m.body["engine"] == "postgres"


def test_rds_encryption_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.rds_encryption_at_rest` fires on CFN-translated body identically to TF."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  EncryptedDb:\n"
        "    Type: AWS::RDS::DBInstance\n"
        "    Properties:\n"
        "      DBInstanceIdentifier: enc-db\n"
        "      DBInstanceClass: db.t3.micro\n"
        "      Engine: postgres\n"
        "      AllocatedStorage: 20\n"
        "      StorageEncrypted: true\n"
        "      KmsKeyId: arn:aws:kms:us-east-1:123:key/abc\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = rds_enc_detector.detect(tf_resources)
    assert len(evidence) == 1
    e = evidence[0]
    assert e.content["resource_type"] == "aws_db_instance"


def test_rds_public_accessibility_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.rds_public_accessibility` flags PubliclyAccessible:true via CFN."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  PublicDb:\n"
        "    Type: AWS::RDS::DBInstance\n"
        "    Properties:\n"
        "      DBInstanceIdentifier: pub-db\n"
        "      DBInstanceClass: db.t3.micro\n"
        "      Engine: mysql\n"
        "      AllocatedStorage: 20\n"
        "      PubliclyAccessible: true\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = rds_pub_detector.detect(tf_resources)
    assert len(evidence) == 1


# --- AWS::Lambda::Function -------------------------------------------------


def test_lambda_basic_translation() -> None:
    """FunctionName/Runtime/Handler/Role/KmsKeyArn rename simply."""
    [m] = apply_mapping(
        "AWS::Lambda::Function",
        {
            "FunctionName": "my-handler",
            "Runtime": "python3.12",
            "Handler": "index.handler",
            "Role": "arn:aws:iam::123:role/lambda-exec",
            "Timeout": 30,
            "MemorySize": 512,
            "KmsKeyArn": "arn:aws:kms:us-east-1:123:key/abc",
        },
    )
    assert m.tf_type == "aws_lambda_function"
    assert m.body["function_name"] == "my-handler"
    assert m.body["runtime"] == "python3.12"
    assert m.body["handler"] == "index.handler"
    assert m.body["kms_key_arn"] == "arn:aws:kms:us-east-1:123:key/abc"
    assert m.body["timeout"] == 30
    assert m.body["memory_size"] == 512


def test_lambda_environment_translates_to_list_wrapped_block() -> None:
    """CFN flat Environment.Variables → TF list-wrapped environment[0].variables."""
    [m] = apply_mapping(
        "AWS::Lambda::Function",
        {
            "FunctionName": "f",
            "Environment": {"Variables": {"FOO": "bar", "DB_URL": "postgres://x"}},
        },
    )
    assert m.body["environment"] == [{"variables": {"FOO": "bar", "DB_URL": "postgres://x"}}]


def test_lambda_vpc_config_translates_to_list_wrapped_block() -> None:
    """CFN flat VpcConfig → TF list-wrapped vpc_config[0].{subnet_ids, security_group_ids}."""
    [m] = apply_mapping(
        "AWS::Lambda::Function",
        {
            "FunctionName": "f",
            "VpcConfig": {
                "SubnetIds": ["subnet-1", "subnet-2"],
                "SecurityGroupIds": ["sg-1"],
            },
        },
    )
    assert m.body["vpc_config"] == [
        {"subnet_ids": ["subnet-1", "subnet-2"], "security_group_ids": ["sg-1"]}
    ]


def test_lambda_env_kms_detector_parity_unencrypted(tmp_path: Path) -> None:
    """Lambda with env vars but no kms_key_arn → env-kms detector emits absent Evidence."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  EnvLambda:\n"
        "    Type: AWS::Lambda::Function\n"
        "    Properties:\n"
        "      FunctionName: env-lambda\n"
        "      Runtime: python3.12\n"
        "      Handler: index.handler\n"
        "      Role: arn:aws:iam::123:role/r\n"
        "      Environment:\n"
        "        Variables:\n"
        "          FOO: bar\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = lambda_env_detector.detect(tf_resources)
    assert len(evidence) == 1
    e = evidence[0]
    assert e.content["resource_type"] == "aws_lambda_function"


def test_lambda_vpc_isolation_detector_fires_on_cfn(tmp_path: Path) -> None:
    """Lambda with VpcConfig set → vpc-isolation detector emits Evidence."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  VpcLambda:\n"
        "    Type: AWS::Lambda::Function\n"
        "    Properties:\n"
        "      FunctionName: vpc-lambda\n"
        "      Runtime: python3.12\n"
        "      Handler: index.handler\n"
        "      Role: arn:aws:iam::123:role/r\n"
        "      VpcConfig:\n"
        "        SubnetIds:\n"
        "          - subnet-1\n"
        "          - subnet-2\n"
        "        SecurityGroupIds:\n"
        "          - sg-1\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = lambda_vpc_detector.detect(tf_resources)
    assert len(evidence) == 1


# --- Coverage list pin ----------------------------------------------------


def test_v0_1_76_batch3_coverage_subset_still_present() -> None:
    """The 3 batch-3 resource types must remain present across future batches."""
    from efterlev.cloudformation.property_mapping import mapped_cfn_types

    coverage = set(mapped_cfn_types())
    assert {
        "AWS::KMS::Key",
        "AWS::Lambda::Function",
        "AWS::RDS::DBInstance",
    }.issubset(coverage)
