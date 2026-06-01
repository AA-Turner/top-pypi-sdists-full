"""Tests for PR gamma.2 batch 9 (v0.1.96) — close-the-real-coverage-gaps batch.

Closes the 8 missing CFN-type mappings the v0.1.95 parity audit
surfaced. After this lands, the parity matrix should show every
detector reachable from CFN with no missing-mapping gaps (only the
2 TF-only-by-design detectors remain TF-only, which is intentional).
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cloudformation import adapt_cfn_resources, apply_mapping, parse_cfn_file
from efterlev.detectors.aws.centralized_log_aggregation import (
    detector as central_log_detector,
)
from efterlev.detectors.aws.iam_service_account_keys_age import (
    detector as iam_keys_age_detector,
)
from efterlev.detectors.aws.iam_user_access_keys import detector as iam_user_keys_detector

# --- AWS::IAM::AccessKey -----------------------------------------------


def test_iam_access_key_basic_translation() -> None:
    """UserName → user; Status → status. tf_type override applies."""
    [m] = apply_mapping(
        "AWS::IAM::AccessKey",
        {"UserName": "alice", "Status": "Active", "Serial": 1},
    )
    assert m.tf_type == "aws_iam_access_key"
    assert m.body == {"user": "alice", "status": "Active", "serial": 1}


def test_iam_user_access_keys_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  AliceKey:\n"
        "    Type: AWS::IAM::AccessKey\n"
        "    Properties:\n"
        "      UserName: alice\n"
        "      Status: Active\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = iam_user_keys_detector.detect(tf_resources)
    assert any(e.content.get("resource_type") == "aws_iam_access_key" for e in evidence)


def test_iam_service_account_keys_age_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  SvcKey:\n"
        "    Type: AWS::IAM::AccessKey\n"
        "    Properties:\n"
        "      UserName: ci-bot\n"
        "      Status: Active\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = iam_keys_age_detector.detect(tf_resources)
    assert any(e.content.get("resource_type") == "aws_iam_access_key" for e in evidence)


# --- AWS::Logs::Destination + AWS::Logs::SubscriptionFilter ----------


def test_logs_destination_basic_translation() -> None:
    """DestinationName → name; tf_type prefixes cloudwatch_."""
    [m] = apply_mapping(
        "AWS::Logs::Destination",
        {
            "DestinationName": "central-logs",
            "TargetArn": "arn:aws:logs:us-east-1:123:log-group:central",
            "RoleArn": "arn:aws:iam::123:role/logs",
        },
    )
    assert m.tf_type == "aws_cloudwatch_log_destination"
    assert m.body["name"] == "central-logs"
    assert m.body["target_arn"].startswith("arn:aws:logs")


def test_logs_subscription_filter_basic_translation() -> None:
    """FilterName → name; FilterPattern + LogGroupName + DestinationArn rename."""
    [m] = apply_mapping(
        "AWS::Logs::SubscriptionFilter",
        {
            "FilterName": "errors",
            "FilterPattern": "ERROR",
            "LogGroupName": "/app/prod",
            "DestinationArn": "arn:aws:logs:us-east-1:123:destination:central",
        },
    )
    assert m.tf_type == "aws_cloudwatch_log_subscription_filter"
    assert m.body["filter_pattern"] == "ERROR"
    assert m.body["log_group_name"] == "/app/prod"


# --- OpenSearch + Elasticsearch (legacy) -----------------------------


def test_opensearch_domain_basic_translation() -> None:
    """tf_type drops the `service` segment (CFN service-namespace artifact)."""
    [m] = apply_mapping(
        "AWS::OpenSearchService::Domain",
        {"DomainName": "logs-search", "EngineVersion": "OpenSearch_2.11"},
    )
    assert m.tf_type == "aws_opensearch_domain"
    assert m.body["domain_name"] == "logs-search"


def test_elasticsearch_domain_basic_translation() -> None:
    """Default tf_type (aws_elasticsearch_domain) — no override needed."""
    [m] = apply_mapping(
        "AWS::Elasticsearch::Domain",
        {"DomainName": "legacy-search", "ElasticsearchVersion": "7.10"},
    )
    # tf_type=None -> adapter falls back to cfn_type_to_tf_type, yielding aws_elasticsearch_domain
    assert m.tf_type is None
    assert m.body["domain_name"] == "legacy-search"


# --- KinesisFirehose + SecurityHub ----------------------------------


def test_kinesis_firehose_basic_translation() -> None:
    """DeliveryStreamName → name; tf_type override needed."""
    [m] = apply_mapping(
        "AWS::KinesisFirehose::DeliveryStream",
        {"DeliveryStreamName": "log-stream", "DeliveryStreamType": "DirectPut"},
    )
    assert m.tf_type == "aws_kinesis_firehose_delivery_stream"
    assert m.body["name"] == "log-stream"
    assert m.body["destination"] == "DirectPut"


def test_securityhub_hub_basic_translation() -> None:
    """CFN's `Hub` becomes TF's `account` — name asymmetry."""
    [m] = apply_mapping(
        "AWS::SecurityHub::Hub",
        {"EnableDefaultStandards": True},
    )
    assert m.tf_type == "aws_securityhub_account"
    assert m.body["enable_default_standards"] is True


def test_securityhub_finding_aggregator_basic_translation() -> None:
    """RegionLinkingMode + Regions; tf_type override needed."""
    [m] = apply_mapping(
        "AWS::SecurityHub::FindingAggregator",
        {"RegionLinkingMode": "SPECIFIED_REGIONS", "Regions": ["us-east-1", "us-west-2"]},
    )
    assert m.tf_type == "aws_securityhub_finding_aggregator"
    assert m.body["linking_mode"] == "SPECIFIED_REGIONS"
    assert m.body["specified_regions"] == ["us-east-1", "us-west-2"]


# --- centralized_log_aggregation end-to-end --------------------------


def test_centralized_log_aggregation_detector_fires_on_cfn_with_full_stack(
    tmp_path: Path,
) -> None:
    """End-to-end: a CFN stack with central-logging primitives across all 7
    previously-unmapped types lights up `aws.centralized_log_aggregation`.
    """
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  TrailLogs:\n"
        "    Type: AWS::Logs::LogGroup\n"
        "    Properties:\n"
        "      LogGroupName: /aws/cloudtrail\n"
        "      RetentionInDays: 90\n"
        "  Trail:\n"
        "    Type: AWS::CloudTrail::Trail\n"
        "    Properties:\n"
        "      TrailName: prod-audit\n"
        "      S3BucketName: audit-bucket\n"
        "      IsMultiRegionTrail: true\n"
        "      IsLogging: true\n"
        "  ErrorFilter:\n"
        "    Type: AWS::Logs::SubscriptionFilter\n"
        "    Properties:\n"
        "      LogGroupName: /aws/cloudtrail\n"
        "      FilterName: errors\n"
        "      FilterPattern: ERROR\n"
        "      DestinationArn: arn:aws:logs:us-east-1:123:destination:central\n"
        "  Central:\n"
        "    Type: AWS::Logs::Destination\n"
        "    Properties:\n"
        "      DestinationName: central\n"
        "      TargetArn: arn:aws:logs:us-east-1:123:log-group:central\n"
        "      RoleArn: arn:aws:iam::123:role/logs\n"
        "  LogStream:\n"
        "    Type: AWS::KinesisFirehose::DeliveryStream\n"
        "    Properties:\n"
        "      DeliveryStreamName: central-logs\n"
        "      DeliveryStreamType: DirectPut\n"
        "  LogSearch:\n"
        "    Type: AWS::OpenSearchService::Domain\n"
        "    Properties:\n"
        "      DomainName: log-search\n"
        "      EngineVersion: OpenSearch_2.11\n"
        "  LegacySearch:\n"
        "    Type: AWS::Elasticsearch::Domain\n"
        "    Properties:\n"
        "      DomainName: legacy-search\n"
        "      ElasticsearchVersion: 7.10\n"
        "  Hub:\n"
        "    Type: AWS::SecurityHub::Hub\n"
        "    Properties:\n"
        "      EnableDefaultStandards: true\n"
        "  Aggregator:\n"
        "    Type: AWS::SecurityHub::FindingAggregator\n"
        "    Properties:\n"
        "      RegionLinkingMode: ALL_REGIONS\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    # Confirm all 9 expected TF types appear in the adapter output.
    types = {r.type for r in tf_resources}
    expected = {
        "aws_cloudwatch_log_group",
        "aws_cloudtrail",
        "aws_cloudwatch_log_subscription_filter",
        "aws_cloudwatch_log_destination",
        "aws_kinesis_firehose_delivery_stream",
        "aws_opensearch_domain",
        "aws_elasticsearch_domain",
        "aws_securityhub_account",
        "aws_securityhub_finding_aggregator",
    }
    assert expected.issubset(types), f"Missing types: {expected - types}"
    # `aws.centralized_log_aggregation` should fire and reach into the stack.
    evidence = central_log_detector.detect(tf_resources)
    assert len(evidence) >= 1
