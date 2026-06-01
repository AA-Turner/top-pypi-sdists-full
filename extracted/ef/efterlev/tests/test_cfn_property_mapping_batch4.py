"""Tests for PR gamma.2 batch 4 mappings (v0.1.77).

Long-tail high-yield services: CloudTrail + SNS + SQS + DynamoDB +
Secrets Manager.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cloudformation import adapt_cfn_resources, apply_mapping, parse_cfn_file
from efterlev.detectors.aws.cloudtrail_audit_logging import detector as ct_audit_detector
from efterlev.detectors.aws.cloudtrail_log_file_validation import (
    detector as ct_validation_detector,
)
from efterlev.detectors.aws.secrets_manager_rotation import detector as secrets_detector
from efterlev.detectors.aws.sns_topic_encryption import detector as sns_detector
from efterlev.detectors.aws.sqs_queue_encryption import detector as sqs_detector

# --- AWS::CloudTrail::Trail ------------------------------------------------


def test_cloudtrail_basic_translation() -> None:
    [m] = apply_mapping(
        "AWS::CloudTrail::Trail",
        {
            "TrailName": "audit",
            "S3BucketName": "audit-logs",
            "EnableLogFileValidation": True,
            "IsMultiRegionTrail": True,
            "IncludeGlobalServiceEvents": True,
            "KMSKeyId": "arn:aws:kms:us-east-1:123:key/abc",
        },
    )
    assert m.tf_type == "aws_cloudtrail"
    assert m.body["enable_log_file_validation"] is True
    assert m.body["is_multi_region_trail"] is True
    assert m.body["include_global_service_events"] is True
    assert m.body["s3_bucket_name"] == "audit-logs"
    assert m.body["kms_key_id"] == "arn:aws:kms:us-east-1:123:key/abc"


def test_cloudtrail_log_file_validation_detector_fires(tmp_path: Path) -> None:
    """`aws.cloudtrail_log_file_validation` reads `enable_log_file_validation`."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Audit:\n"
        "    Type: AWS::CloudTrail::Trail\n"
        "    Properties:\n"
        "      TrailName: audit\n"
        "      S3BucketName: audit-logs\n"
        "      EnableLogFileValidation: true\n"
        "      IsLogging: true\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = ct_validation_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_cloudtrail"


def test_cloudtrail_audit_detector_fires(tmp_path: Path) -> None:
    """`aws.cloudtrail_audit_logging` reads multi-region + global-event flags."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Audit:\n"
        "    Type: AWS::CloudTrail::Trail\n"
        "    Properties:\n"
        "      TrailName: audit\n"
        "      S3BucketName: audit-logs\n"
        "      IsMultiRegionTrail: true\n"
        "      IncludeGlobalServiceEvents: true\n"
        "      IsLogging: true\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = ct_audit_detector.detect(tf_resources)
    assert len(evidence) == 1


# --- AWS::SNS::Topic -------------------------------------------------------


def test_sns_topic_basic_translation() -> None:
    [m] = apply_mapping(
        "AWS::SNS::Topic",
        {
            "TopicName": "alerts",
            "DisplayName": "Alerts",
            "KmsMasterKeyId": "alias/aws/sns",
        },
    )
    assert m.tf_type == "aws_sns_topic"
    assert m.body["name"] == "alerts"
    assert m.body["display_name"] == "Alerts"
    assert m.body["kms_master_key_id"] == "alias/aws/sns"


def test_sns_encryption_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.sns_topic_encryption` reads kms_master_key_id."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  EncTopic:\n"
        "    Type: AWS::SNS::Topic\n"
        "    Properties:\n"
        "      TopicName: enc-topic\n"
        "      KmsMasterKeyId: alias/aws/sns\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = sns_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_sns_topic"


# --- AWS::SQS::Queue -------------------------------------------------------


def test_sqs_queue_basic_translation() -> None:
    [m] = apply_mapping(
        "AWS::SQS::Queue",
        {
            "QueueName": "work",
            "KmsMasterKeyId": "alias/aws/sqs",
            "SqsManagedSseEnabled": False,
        },
    )
    assert m.tf_type == "aws_sqs_queue"
    assert m.body["name"] == "work"
    assert m.body["kms_master_key_id"] == "alias/aws/sqs"
    assert m.body["sqs_managed_sse_enabled"] is False


def test_sqs_encryption_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.sqs_queue_encryption` reads kms_master_key_id + sqs_managed_sse_enabled."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  EncQueue:\n"
        "    Type: AWS::SQS::Queue\n"
        "    Properties:\n"
        "      QueueName: enc-queue\n"
        "      SqsManagedSseEnabled: true\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = sqs_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_sqs_queue"


# --- AWS::DynamoDB::Table --------------------------------------------------


def test_dynamodb_basic_translation() -> None:
    [m] = apply_mapping(
        "AWS::DynamoDB::Table",
        {
            "TableName": "users",
            "BillingMode": "PAY_PER_REQUEST",
            "DeletionProtectionEnabled": True,
        },
    )
    assert m.tf_type == "aws_dynamodb_table"
    assert m.body["name"] == "users"
    assert m.body["billing_mode"] == "PAY_PER_REQUEST"
    assert m.body["deletion_protection_enabled"] is True


def test_dynamodb_sse_translates_to_list_wrapped_block() -> None:
    """SSESpecification → server_side_encryption[0] list-wrapped block."""
    [m] = apply_mapping(
        "AWS::DynamoDB::Table",
        {
            "TableName": "secrets",
            "SSESpecification": {
                "SSEEnabled": True,
                "SSEType": "KMS",
                "KMSMasterKeyId": "arn:aws:kms:us-east-1:123:key/abc",
            },
        },
    )
    assert m.body["server_side_encryption"] == [
        {
            "enabled": True,
            "sse_type": "KMS",
            "kms_key_arn": "arn:aws:kms:us-east-1:123:key/abc",
        }
    ]


def test_dynamodb_pitr_translates_to_list_wrapped_block() -> None:
    """PointInTimeRecoverySpecification → point_in_time_recovery[0] list-wrapped."""
    [m] = apply_mapping(
        "AWS::DynamoDB::Table",
        {
            "TableName": "audit",
            "PointInTimeRecoverySpecification": {"PointInTimeRecoveryEnabled": True},
        },
    )
    assert m.body["point_in_time_recovery"] == [{"enabled": True}]


# --- AWS::SecretsManager::Secret ------------------------------------------


def test_secrets_manager_basic_translation() -> None:
    [m] = apply_mapping(
        "AWS::SecretsManager::Secret",
        {
            "Name": "db-password",
            "Description": "Postgres prod",
            "KmsKeyId": "arn:aws:kms:us-east-1:123:key/abc",
        },
    )
    assert m.tf_type == "aws_secretsmanager_secret"
    assert m.body["name"] == "db-password"
    assert m.body["description"] == "Postgres prod"
    assert m.body["kms_key_id"] == "arn:aws:kms:us-east-1:123:key/abc"


def test_secrets_rotation_detector_emits_no_rotation_evidence(tmp_path: Path) -> None:
    """Secret without rotation_lambda_arn → `aws.secrets_manager_rotation` emits Evidence."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Pwd:\n"
        "    Type: AWS::SecretsManager::Secret\n"
        "    Properties:\n"
        "      Name: db-password\n"
        "      Description: Postgres prod\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = secrets_detector.detect(tf_resources)
    # Detector emits one evidence per secret (presence + rotation status).
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_secretsmanager_secret"


# --- Coverage list pin ----------------------------------------------------


def test_v0_1_77_batch4_coverage_subset_still_present() -> None:
    """The 5 batch-4 resource types must remain present across future batches."""
    from efterlev.cloudformation.property_mapping import mapped_cfn_types

    coverage = set(mapped_cfn_types())
    assert {
        "AWS::CloudTrail::Trail",
        "AWS::DynamoDB::Table",
        "AWS::SNS::Topic",
        "AWS::SQS::Queue",
        "AWS::SecretsManager::Secret",
    }.issubset(coverage)
