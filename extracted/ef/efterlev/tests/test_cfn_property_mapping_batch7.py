"""Tests for PR gamma.2 batch 7 mappings (v0.1.92).

IAM Group + API Gateway pair — 5 mappings unlock 7 detectors.

Notable patterns:

- IAM Group reuses the 1→(1+N+M) synthesis pattern from PR gamma.2
  batch 2 (IAM::Role/User): each ManagedPolicyArns entry becomes a
  synthesized aws_iam_group_policy_attachment, each inline Policies
  entry becomes a synthesized aws_iam_group_policy.

- API Gateway v1 vs v2 CFN naming inconsistency:
  - v1 Stage uses singular `AccessLogSetting`; v2 Stage uses plural
    `AccessLogSettings`. Both translate to TF's plural
    `access_log_settings`.
  - v1 Method uses `AuthorizationType` → TF's `authorization`
    (TF schema flattens the suffix for v1 only).
  - v2 Route uses `AuthorizationType` → TF's `authorization_type`
    (v2 keeps the suffix).
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cloudformation import adapt_cfn_resources, apply_mapping, parse_cfn_file
from efterlev.detectors.aws.api_gateway_access_logging import (
    detector as access_log_detector,
)
from efterlev.detectors.aws.api_gateway_auth_required import detector as auth_detector
from efterlev.detectors.aws.iam_admin_policy_usage import detector as admin_detector

# --- AWS::IAM::Group ------------------------------------------------------


def test_iam_group_basic_translation() -> None:
    """Bare group: GroupName → name + Path."""
    mapped = apply_mapping(
        "AWS::IAM::Group",
        {"GroupName": "developers", "Path": "/teams/"},
    )
    # Just the bare group, no attachments / inline policies.
    assert len(mapped) == 1
    assert mapped[0].tf_type == "aws_iam_group"
    assert mapped[0].body == {"name": "developers", "path": "/teams/"}


def test_iam_group_managed_policy_attachments_synthesized() -> None:
    """ManagedPolicyArns list → one aws_iam_group_policy_attachment per ARN."""
    mapped = apply_mapping(
        "AWS::IAM::Group",
        {
            "GroupName": "admins",
            "ManagedPolicyArns": [
                "arn:aws:iam::aws:policy/AdministratorAccess",
                "arn:aws:iam::aws:policy/IAMFullAccess",
            ],
        },
    )
    # 1 group + 2 attachments
    assert len(mapped) == 3
    attachments = [m for m in mapped if m.tf_type == "aws_iam_group_policy_attachment"]
    assert len(attachments) == 2
    arns = sorted(a.body["policy_arn"] for a in attachments)
    assert arns == [
        "arn:aws:iam::aws:policy/AdministratorAccess",
        "arn:aws:iam::aws:policy/IAMFullAccess",
    ]


def test_iam_group_inline_policies_synthesized() -> None:
    """Policies list → one aws_iam_group_policy per entry; PolicyDocument JSON-stringified."""
    mapped = apply_mapping(
        "AWS::IAM::Group",
        {
            "GroupName": "ops",
            "Policies": [
                {
                    "PolicyName": "ReadAllS3",
                    "PolicyDocument": {
                        "Version": "2012-10-17",
                        "Statement": [{"Effect": "Allow", "Action": "s3:Get*", "Resource": "*"}],
                    },
                },
            ],
        },
    )
    inline_policies = [m for m in mapped if m.tf_type == "aws_iam_group_policy"]
    assert len(inline_policies) == 1
    assert inline_policies[0].body["name"] == "ReadAllS3"
    assert "Statement" in inline_policies[0].body["policy"]


def test_iam_group_admin_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.iam_admin_policy_usage` flags AdministratorAccess attachment via group."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Admins:\n"
        "    Type: AWS::IAM::Group\n"
        "    Properties:\n"
        "      GroupName: admins\n"
        "      ManagedPolicyArns:\n"
        "        - arn:aws:iam::aws:policy/AdministratorAccess\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = admin_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_iam_group_policy_attachment"
    assert evidence[0].content["policy_arn"] == "arn:aws:iam::aws:policy/AdministratorAccess"


# --- AWS::ApiGateway::Stage (v1) -----------------------------------------


def test_api_gateway_stage_basic_translation() -> None:
    """Top-level renames; AccessLogSetting (singular) → access_log_settings."""
    [m] = apply_mapping(
        "AWS::ApiGateway::Stage",
        {
            "StageName": "prod",
            "RestApiId": "abc123",
            "DeploymentId": "deploy-1",
            "Description": "production stage",
            "TracingEnabled": True,
            "AccessLogSetting": {
                "DestinationArn": "arn:aws:logs:us-east-1:123:log-group:api/prod",
                "Format": '{"requestId":"$context.requestId"}',
            },
        },
    )
    assert m.tf_type == "aws_api_gateway_stage"
    assert m.body["stage_name"] == "prod"
    assert m.body["rest_api_id"] == "abc123"
    assert m.body["xray_tracing_enabled"] is True
    assert m.body["access_log_settings"] == {
        "destination_arn": "arn:aws:logs:us-east-1:123:log-group:api/prod",
        "format": '{"requestId":"$context.requestId"}',
    }


def test_api_gateway_stage_access_logging_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.api_gateway_access_logging` reads access_log_settings from CFN."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Stage:\n"
        "    Type: AWS::ApiGateway::Stage\n"
        "    Properties:\n"
        "      StageName: prod\n"
        "      RestApiId: api-1\n"
        "      AccessLogSetting:\n"
        "        DestinationArn: arn:aws:logs:us-east-1:123:log-group:api/prod\n"
        '        Format: \'{"requestId":"$context.requestId"}\'\n'
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = access_log_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_api_gateway_stage"
    assert evidence[0].content["destination_arn"] == "arn:aws:logs:us-east-1:123:log-group:api/prod"


# --- AWS::ApiGatewayV2::Stage (v2 HTTP/WebSocket) ------------------------


def test_apigatewayv2_stage_basic_translation() -> None:
    """v2 Stage uses plural AccessLogSettings; StageName → name (not stage_name)."""
    [m] = apply_mapping(
        "AWS::ApiGatewayV2::Stage",
        {
            "StageName": "$default",
            "ApiId": "v2-abc",
            "AutoDeploy": True,
            "AccessLogSettings": {
                "DestinationArn": "arn:aws:logs:us-east-1:123:log-group:apiv2/default",
                "Format": '{"sourceIp":"$context.identity.sourceIp"}',
            },
        },
    )
    # Default tf_type: cfn_type_to_tf_type("AWS::ApiGatewayV2::Stage") yields
    # aws_apigatewayv2_stage which IS the canonical TF type — no override needed.
    assert m.tf_type is None
    assert m.body["name"] == "$default"
    assert m.body["api_id"] == "v2-abc"
    assert m.body["auto_deploy"] is True
    assert m.body["access_log_settings"]["destination_arn"].endswith("log-group:apiv2/default")


def test_apigatewayv2_stage_routes_through_adapter_to_correct_tf_type(
    tmp_path: Path,
) -> None:
    """End-to-end: AWS::ApiGatewayV2::Stage emits as aws_apigatewayv2_stage."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Stage:\n"
        "    Type: AWS::ApiGatewayV2::Stage\n"
        "    Properties:\n"
        "      StageName: $default\n"
        "      ApiId: api-v2\n"
        "      AccessLogSettings:\n"
        "        DestinationArn: arn:aws:logs:us-east-1:123:log-group:v2/default\n"
        '        Format: \'{"sourceIp":"$context.identity.sourceIp"}\'\n'
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    assert len(tf_resources) == 1
    assert tf_resources[0].type == "aws_apigatewayv2_stage"


def test_apigatewayv2_access_logging_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.api_gateway_access_logging` reads v2 stage access_log_settings."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Stage:\n"
        "    Type: AWS::ApiGatewayV2::Stage\n"
        "    Properties:\n"
        "      StageName: $default\n"
        "      ApiId: api-v2\n"
        "      AccessLogSettings:\n"
        "        DestinationArn: arn:aws:logs:us-east-1:123:log-group:v2/default\n"
        '        Format: \'{"sourceIp":"$context.identity.sourceIp"}\'\n'
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = access_log_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_apigatewayv2_stage"


# --- AWS::ApiGateway::Method (v1) ----------------------------------------


def test_api_gateway_method_basic_translation() -> None:
    """AuthorizationType → authorization (note: TF v1 schema flattens the suffix)."""
    [m] = apply_mapping(
        "AWS::ApiGateway::Method",
        {
            "HttpMethod": "GET",
            "AuthorizationType": "AWS_IAM",
            "ResourceId": "res-1",
            "RestApiId": "api-1",
            "ApiKeyRequired": False,
        },
    )
    assert m.tf_type == "aws_api_gateway_method"
    assert m.body["http_method"] == "GET"
    assert m.body["authorization"] == "AWS_IAM"  # NOT authorization_type
    assert m.body["api_key_required"] is False


def test_api_gateway_method_auth_required_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.api_gateway_auth_required` reads `authorization` field for v1 methods."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  GetMethod:\n"
        "    Type: AWS::ApiGateway::Method\n"
        "    Properties:\n"
        "      HttpMethod: GET\n"
        "      AuthorizationType: AWS_IAM\n"
        "      ResourceId: res-1\n"
        "      RestApiId: api-1\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = auth_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_api_gateway_method"


# --- AWS::ApiGatewayV2::Route (v2) --------------------------------------


def test_apigatewayv2_route_basic_translation() -> None:
    """v2 Route keeps the suffix: AuthorizationType → authorization_type."""
    [m] = apply_mapping(
        "AWS::ApiGatewayV2::Route",
        {
            "RouteKey": "GET /widgets",
            "ApiId": "v2-abc",
            "AuthorizationType": "JWT",
            "AuthorizerId": "authzer-1",
            "Target": "integrations/integ-1",
        },
    )
    # Default tf_type already correct: aws_apigatewayv2_route
    assert m.tf_type is None
    assert m.body["route_key"] == "GET /widgets"
    assert m.body["api_id"] == "v2-abc"
    assert m.body["authorization_type"] == "JWT"


def test_apigatewayv2_route_auth_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.api_gateway_auth_required` reads `authorization_type` for v2 routes."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  WidgetsRoute:\n"
        "    Type: AWS::ApiGatewayV2::Route\n"
        "    Properties:\n"
        "      RouteKey: GET /widgets\n"
        "      ApiId: api-v2\n"
        "      AuthorizationType: JWT\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = auth_detector.detect(tf_resources)
    assert len(evidence) == 1
    assert evidence[0].content["resource_type"] == "aws_apigatewayv2_route"
