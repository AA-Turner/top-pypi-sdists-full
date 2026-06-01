"""Tests for the CloudFormation → Terraform adapter shim.

v0.1.73 (PR gamma) scope: type-name translation + property-mapping
table covering 3 resource types + sub-resource synthesis (1→N).
Unmapped types still get a shallow snake_case body mirror (fallback).

The 1→N signature change (adapt_cfn_to_terraform returns a list) is
also pinned here.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cloudformation.adapter import (
    adapt_cfn_resources,
    adapt_cfn_to_terraform,
    cfn_type_to_tf_type,
)
from efterlev.cloudformation.parser import CfnResource

# --- cfn_type_to_tf_type ------------------------------------------------------


def test_simple_aws_type() -> None:
    """`AWS::S3::Bucket` → `aws_s3_bucket`."""
    assert cfn_type_to_tf_type("AWS::S3::Bucket") == "aws_s3_bucket"


def test_common_single_word_resources_translate_cleanly() -> None:
    """The ~80% case: single-word Resource segment matches TF convention."""
    assert cfn_type_to_tf_type("AWS::Lambda::Function") == "aws_lambda_function"
    assert cfn_type_to_tf_type("AWS::EC2::Instance") == "aws_ec2_instance"
    assert cfn_type_to_tf_type("AWS::SNS::Topic") == "aws_sns_topic"
    assert cfn_type_to_tf_type("AWS::SQS::Queue") == "aws_sqs_queue"
    assert cfn_type_to_tf_type("AWS::IAM::Role") == "aws_iam_role"
    assert cfn_type_to_tf_type("AWS::DynamoDB::Table") == "aws_dynamodb_table"


def test_multi_word_resource_segment_loses_word_boundary() -> None:
    """`AWS::WAFv2::WebACL` → `aws_wafv2_webacl` (documented limitation)."""
    assert cfn_type_to_tf_type("AWS::WAFv2::WebACL") == "aws_wafv2_webacl"


def test_custom_resource_type() -> None:
    """Non-AWS namespaces translate too (won't match any AWS detector)."""
    assert cfn_type_to_tf_type("Custom::MyHandler") == "custom_myhandler"


# --- adapt_cfn_to_terraform ---------------------------------------------------


def _resource(
    logical_id: str = "MyBucket",
    cfn_type: str = "AWS::S3::Bucket",
    properties: dict | None = None,
    file: Path = Path("stack.yaml"),
) -> CfnResource:
    return CfnResource(
        logical_id=logical_id,
        type=cfn_type,
        properties=properties or {},
        file=file,
    )


def test_adapter_returns_list() -> None:
    """v0.1.73 signature: 1→N. Most resources yield a single-element list."""
    result = adapt_cfn_to_terraform(_resource())
    assert isinstance(result, list)
    assert len(result) == 1


def test_type_translation_registered() -> None:
    """Registered CFN types use property mapping; tf.type still translates."""
    tf = adapt_cfn_to_terraform(_resource())[0]
    assert tf.type == "aws_s3_bucket"


def test_type_translation_unmapped() -> None:
    """Unmapped CFN types use default translation + fallback body mirror."""
    tf = adapt_cfn_to_terraform(_resource(cfn_type="AWS::CloudFront::Distribution"))[0]
    assert tf.type == "aws_cloudfront_distribution"


def test_name_preservation() -> None:
    """CFN `LogicalId` (CamelCase) → TF `name` (preserved verbatim)."""
    tf = adapt_cfn_to_terraform(_resource(logical_id="MyAppBucket"))[0]
    assert tf.name == "MyAppBucket"


def test_unmapped_body_shallow_snake_case_mirror() -> None:
    """Unmapped types: top-level keys snake_cased, values unchanged.

    Uses `AWS::Athena::WorkGroup` — no detector reads Athena at v0.1.93,
    so the type is reliably unmapped and the fallback path runs. CFN
    types previously used here (CloudFront::Distribution) are now
    explicitly mapped per PR gamma.2 batch 8.
    """
    tf = adapt_cfn_to_terraform(
        _resource(
            cfn_type="AWS::Athena::WorkGroup",
            properties={
                "WorkGroupConfiguration": {"PublishCloudWatchMetricsEnabled": True},
                "Tags": [{"Key": "env", "Value": "prod"}],
            },
        )
    )[0]
    assert "work_group_configuration" in tf.body
    # NESTED keys NOT converted at fallback layer (intentional honest scope).
    assert tf.body["work_group_configuration"] == {"PublishCloudWatchMetricsEnabled": True}
    assert tf.body["tags"] == [{"Key": "env", "Value": "prod"}]


def test_kind_is_resource() -> None:
    """CFN has no equivalent of TF's data sources at this layer."""
    tf = adapt_cfn_to_terraform(_resource())[0]
    assert tf.kind == "resource"


def test_source_ref_uses_relative_path_when_scan_root_given() -> None:
    """`scan_root=...` makes `source_ref.file` relative-to-root."""
    file = Path("/repo/infra/stack.yaml")
    scan_root = Path("/repo")
    tf = adapt_cfn_to_terraform(_resource(file=file), scan_root=scan_root)[0]
    assert tf.source_ref.file == Path("infra/stack.yaml")


def test_source_ref_line_numbers_null() -> None:
    """v0.1.73 line numbers still deferred per DECISIONS 2026-05-12 #4."""
    tf = adapt_cfn_to_terraform(_resource())[0]
    assert tf.source_ref.line_start is None
    assert tf.source_ref.line_end is None


def test_adapt_batch_flattens_1_to_n() -> None:
    """`adapt_cfn_resources` flattens the 1→N expansion across the batch."""
    resources = [
        _resource(logical_id="A", cfn_type="AWS::S3::Bucket"),
        _resource(logical_id="B", cfn_type="AWS::SNS::Topic"),
    ]
    adapted = adapt_cfn_resources(resources)
    assert len(adapted) == 2
    assert adapted[0].type == "aws_s3_bucket"
    assert adapted[1].type == "aws_sns_topic"


# --- Property-mapping integration: AWS::S3::Bucket ---------------------------


def test_s3_bucket_encryption_maps_to_tf_shape() -> None:
    """CFN BucketEncryption → TF server_side_encryption_configuration (nested)."""
    tf = adapt_cfn_to_terraform(
        _resource(
            properties={
                "BucketName": "my-bucket",
                "BucketEncryption": {
                    "ServerSideEncryptionConfiguration": [
                        {"ServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
                    ]
                },
            }
        )
    )[0]
    assert tf.body["bucket"] == "my-bucket"
    sse = tf.body["server_side_encryption_configuration"]
    # TF shape: list-of-dict with `rule` wrapper that CFN omits.
    assert sse == [
        {"rule": [{"apply_server_side_encryption_by_default": [{"sse_algorithm": "AES256"}]}]}
    ]


def test_s3_bucket_public_access_block_synthesizes_separate_resource() -> None:
    """CFN PublicAccessBlockConfiguration → synthesized aws_s3_bucket_public_access_block."""
    resources = adapt_cfn_to_terraform(
        _resource(
            logical_id="MyBucket",
            properties={
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": True,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True,
                }
            },
        )
    )
    assert len(resources) == 2
    bucket, pab = resources
    assert bucket.type == "aws_s3_bucket"
    assert bucket.name == "MyBucket"
    assert pab.type == "aws_s3_bucket_public_access_block"
    assert pab.name == "MyBucket_pab"
    assert pab.body == {
        "block_public_acls": True,
        "ignore_public_acls": True,
        "block_public_policy": True,
        "restrict_public_buckets": True,
    }


def test_s3_bucket_partial_pab_only_translates_set_flags() -> None:
    """Missing PAB flags don't appear in the synthesized body (detector sees them as None)."""
    resources = adapt_cfn_to_terraform(
        _resource(
            logical_id="HalfBlocked",
            properties={
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": True,
                    "BlockPublicPolicy": False,
                }
            },
        )
    )
    pab = resources[1]
    assert pab.body == {
        "block_public_acls": True,
        "block_public_policy": False,
    }


def test_s3_bucket_no_pab_no_synthesis() -> None:
    """No PublicAccessBlockConfiguration → single resource, no synthesis."""
    resources = adapt_cfn_to_terraform(_resource(properties={"BucketName": "plain"}))
    assert len(resources) == 1
    assert resources[0].type == "aws_s3_bucket"


# --- Property-mapping integration: AWS::S3::BucketPolicy --------------------


def test_s3_bucket_policy_dict_to_json_string() -> None:
    """CFN PolicyDocument dict → TF policy JSON-string."""
    import json as json_

    policy_dict = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*"}],
    }
    tf = adapt_cfn_to_terraform(
        _resource(
            cfn_type="AWS::S3::BucketPolicy",
            properties={"Bucket": "my-bucket", "PolicyDocument": policy_dict},
        )
    )[0]
    assert tf.type == "aws_s3_bucket_policy"
    assert tf.body["bucket"] == "my-bucket"
    # Stringified deterministically (sort_keys=True).
    assert isinstance(tf.body["policy"], str)
    assert json_.loads(tf.body["policy"]) == policy_dict


def test_s3_bucket_policy_string_passthrough() -> None:
    """CFN PolicyDocument already a string passes through unchanged."""
    tf = adapt_cfn_to_terraform(
        _resource(
            cfn_type="AWS::S3::BucketPolicy",
            properties={"Bucket": "b", "PolicyDocument": '{"already": "json"}'},
        )
    )[0]
    assert tf.body["policy"] == '{"already": "json"}'


# --- Property-mapping integration: AWS::ElasticLoadBalancingV2::Listener ----


def test_elbv2_listener_simple_keys() -> None:
    """Per-key rename: Protocol/Port/SslPolicy."""
    tf = adapt_cfn_to_terraform(
        _resource(
            cfn_type="AWS::ElasticLoadBalancingV2::Listener",
            properties={
                "Protocol": "HTTPS",
                "Port": 443,
                "SslPolicy": "ELBSecurityPolicy-TLS-1-2-2017-01",
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:...:loadbalancer/app/x/1",
            },
        )
    )[0]
    assert tf.type == "aws_lb_listener"
    assert tf.body["protocol"] == "HTTPS"
    assert tf.body["port"] == 443
    assert tf.body["ssl_policy"] == "ELBSecurityPolicy-TLS-1-2-2017-01"
    assert tf.body["load_balancer_arn"].startswith("arn:aws:elasticloadbalancing:")


def test_elbv2_listener_first_cert_extracted() -> None:
    """Certificates[0].CertificateArn → certificate_arn."""
    tf = adapt_cfn_to_terraform(
        _resource(
            cfn_type="AWS::ElasticLoadBalancingV2::Listener",
            properties={
                "Protocol": "HTTPS",
                "Certificates": [
                    {"CertificateArn": "arn:aws:acm:...:certificate/abc"},
                    {"CertificateArn": "arn:aws:acm:...:certificate/def"},
                ],
            },
        )
    )[0]
    assert tf.body["certificate_arn"] == "arn:aws:acm:...:certificate/abc"


def test_elbv2_listener_plain_http() -> None:
    """No SSL: protocol still translates; no certificate_arn key."""
    tf = adapt_cfn_to_terraform(
        _resource(
            cfn_type="AWS::ElasticLoadBalancingV2::Listener",
            properties={"Protocol": "HTTP", "Port": 80},
        )
    )[0]
    assert tf.body["protocol"] == "HTTP"
    assert tf.body["port"] == 80
    assert "certificate_arn" not in tf.body
    assert "ssl_policy" not in tf.body


# --- Integration: parser + adapter end-to-end --------------------------------


def test_parser_plus_adapter_round_trip_unmapped(tmp_path: Path) -> None:
    """Unmapped type: parser+adapter round-trips to shallow snake_case body.

    Uses `AWS::Athena::WorkGroup` since CloudFront::Distribution is now
    explicitly mapped per PR gamma.2 batch 8 (v0.1.93).
    """
    from efterlev.cloudformation.parser import parse_cfn_file

    f = tmp_path / "stack.yaml"
    f.write_text(
        "Resources:\n"
        "  Wg:\n"
        "    Type: AWS::Athena::WorkGroup\n"
        "    Properties:\n"
        "      WorkGroupConfiguration:\n"
        "        PublishCloudWatchMetricsEnabled: true\n"
    )
    cfn_resources = parse_cfn_file(f)
    tf_resources = adapt_cfn_resources(cfn_resources, scan_root=tmp_path)
    assert len(tf_resources) == 1
    r = tf_resources[0]
    assert r.type == "aws_athena_workgroup"
    assert r.name == "Wg"
    assert "work_group_configuration" in r.body
    assert r.source_ref.file == Path("stack.yaml")


def test_parser_plus_adapter_round_trip_s3_with_pab(tmp_path: Path) -> None:
    """Mapped S3 bucket with PAB: parser + adapter round-trips to 2 TF resources."""
    from efterlev.cloudformation.parser import parse_cfn_file

    f = tmp_path / "stack.yaml"
    f.write_text(
        "Resources:\n"
        "  Locked:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      BucketName: locked-bucket\n"
        "      PublicAccessBlockConfiguration:\n"
        "        BlockPublicAcls: true\n"
        "        IgnorePublicAcls: true\n"
        "        BlockPublicPolicy: true\n"
        "        RestrictPublicBuckets: true\n"
    )
    cfn_resources = parse_cfn_file(f)
    tf_resources = adapt_cfn_resources(cfn_resources, scan_root=tmp_path)
    assert len(tf_resources) == 2
    types = {r.type for r in tf_resources}
    assert types == {"aws_s3_bucket", "aws_s3_bucket_public_access_block"}
