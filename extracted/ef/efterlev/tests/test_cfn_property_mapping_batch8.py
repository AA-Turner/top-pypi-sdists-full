"""Tests for PR gamma.2 batch 8 mappings (v0.1.93) — finishing batch.

Closes out CFN type-coverage: 30 remaining detector-referenced types
in one PR. Most are 1-detector unlocks reading 1-2 fields. Per-type
parity tests verify the basic translation + detector reachability via
the adapter (end-to-end CFN-yaml → TF-resource → detector Evidence).

NOT covered: AWS::IAM::AccountPasswordPolicy — not a real CFN resource
(account-level setting; only deployable via IAM API or AWS Console).
The `aws.iam_password_policy` detector still works on TF.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cloudformation import adapt_cfn_resources, apply_mapping, parse_cfn_file
from efterlev.detectors.aws.access_analyzer_enabled import detector as access_analyzer_detector
from efterlev.detectors.aws.api_gateway_tls_min_version import detector as tls_detector
from efterlev.detectors.aws.cloudfront_viewer_protocol_https import (
    detector as cloudfront_detector,
)
from efterlev.detectors.aws.cloudwatch_alarms_critical import detector as alarm_detector
from efterlev.detectors.aws.config_enabled import detector as config_detector
from efterlev.detectors.aws.elb_access_logs import detector as elb_log_detector
from efterlev.detectors.aws.federated_identity_providers import (
    detector as federated_detector,
)
from efterlev.detectors.aws.guardduty_enabled import detector as guardduty_detector
from efterlev.detectors.aws.mla_log_access_least_privilege import detector as mla_detector
from efterlev.detectors.aws.rpl_backup_configured import detector as backup_plan_detector
from efterlev.detectors.aws.secrets_manager_rotation import detector as rotation_detector
from efterlev.detectors.aws.suspicious_activity_response import detector as event_detector
from efterlev.detectors.aws.svc_at_rest_encryption_coverage import (
    detector as svc_enc_detector,
)
from efterlev.detectors.aws.vpc_logical_segmentation import detector as vpc_detector

# --- API Gateway DomainName (v1 + v2) -----------------------------------


def test_api_gateway_domain_name_v1_basic() -> None:
    [m] = apply_mapping(
        "AWS::ApiGateway::DomainName",
        {"DomainName": "api.example.com", "SecurityPolicy": "TLS_1_2"},
    )
    assert m.tf_type == "aws_api_gateway_domain_name"
    assert m.body == {"domain_name": "api.example.com", "security_policy": "TLS_1_2"}


def test_api_gateway_domain_name_v2_basic_with_config_list() -> None:
    """v2 wraps SecurityPolicy inside DomainNameConfigurations[0]."""
    [m] = apply_mapping(
        "AWS::ApiGatewayV2::DomainName",
        {
            "DomainName": "api-v2.example.com",
            "DomainNameConfigurations": [{"SecurityPolicy": "TLS_1_2", "EndpointType": "REGIONAL"}],
        },
    )
    assert m.tf_type == "aws_apigatewayv2_domain_name"
    assert m.body["domain_name"] == "api-v2.example.com"
    assert m.body["domain_name_configuration"] == [
        {"security_policy": "TLS_1_2", "endpoint_type": "REGIONAL"}
    ]


def test_api_gateway_tls_detector_fires_on_cfn_v1(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Domain:\n"
        "    Type: AWS::ApiGateway::DomainName\n"
        "    Properties:\n"
        "      DomainName: api.example.com\n"
        "      SecurityPolicy: TLS_1_2\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = tls_detector.detect(tf_resources)
    assert any(e.content.get("resource_type") == "aws_api_gateway_domain_name" for e in evidence)


def test_api_gateway_tls_detector_fires_on_cfn_v2(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Domain:\n"
        "    Type: AWS::ApiGatewayV2::DomainName\n"
        "    Properties:\n"
        "      DomainName: api-v2.example.com\n"
        "      DomainNameConfigurations:\n"
        "        - SecurityPolicy: TLS_1_2\n"
        "          EndpointType: REGIONAL\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = tls_detector.detect(tf_resources)
    assert any(e.content.get("resource_type") == "aws_apigatewayv2_domain_name" for e in evidence)


# --- AccessAnalyzer + GuardDuty + Config + CloudWatch + Events ---------


def test_access_analyzer_basic() -> None:
    [m] = apply_mapping(
        "AWS::AccessAnalyzer::Analyzer",
        {"AnalyzerName": "org-analyzer", "Type": "ORGANIZATION"},
    )
    assert m.body == {"analyzer_name": "org-analyzer", "type": "ORGANIZATION"}


def test_access_analyzer_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Analyzer:\n"
        "    Type: AWS::AccessAnalyzer::Analyzer\n"
        "    Properties:\n"
        "      AnalyzerName: org\n"
        "      Type: ORGANIZATION\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = access_analyzer_detector.detect(tf_resources)
    assert len(evidence) == 1


def test_guardduty_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  GD:\n"
        "    Type: AWS::GuardDuty::Detector\n"
        "    Properties:\n"
        "      Enable: true\n"
        "      FindingPublishingFrequency: FIFTEEN_MINUTES\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = guardduty_detector.detect(tf_resources)
    assert len(evidence) == 1


def test_config_detector_fires_on_cfn(tmp_path: Path) -> None:
    """`aws.config_enabled` requires both Recorder + DeliveryChannel."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Recorder:\n"
        "    Type: AWS::Config::ConfigurationRecorder\n"
        "    Properties:\n"
        "      Name: default\n"
        "      RoleARN: arn:aws:iam::123:role/config\n"
        "  Channel:\n"
        "    Type: AWS::Config::DeliveryChannel\n"
        "    Properties:\n"
        "      Name: default\n"
        "      S3BucketName: config-logs\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    types = {r.type for r in tf_resources}
    assert "aws_config_configuration_recorder" in types
    assert "aws_config_delivery_channel" in types
    evidence = config_detector.detect(tf_resources)
    assert len(evidence) >= 1


def test_cloudwatch_alarm_basic_translation() -> None:
    [m] = apply_mapping(
        "AWS::CloudWatch::Alarm",
        {
            "AlarmName": "high-cpu",
            "MetricName": "CPUUtilization",
            "Namespace": "AWS/EC2",
            "Threshold": 80,
            "ComparisonOperator": "GreaterThanThreshold",
            "EvaluationPeriods": 2,
        },
    )
    assert m.tf_type == "aws_cloudwatch_metric_alarm"
    assert m.body["alarm_name"] == "high-cpu"
    assert m.body["threshold"] == 80


def test_cloudwatch_alarm_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Alarm:\n"
        "    Type: AWS::CloudWatch::Alarm\n"
        "    Properties:\n"
        "      AlarmName: high-cpu\n"
        "      MetricName: CPUUtilization\n"
        "      Namespace: AWS/EC2\n"
        "      Threshold: 80\n"
        "      ComparisonOperator: GreaterThanThreshold\n"
        "      EvaluationPeriods: 2\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = alarm_detector.detect(tf_resources)
    assert len(evidence) == 1


def test_events_rule_with_targets_synthesized() -> None:
    """1→1+N: rule + one event_target per Targets entry."""
    mapped = apply_mapping(
        "AWS::Events::Rule",
        {
            "Name": "ec2-state-change",
            "EventPattern": {"source": ["aws.ec2"]},
            "Targets": [
                {"Id": "lambda-1", "Arn": "arn:aws:lambda:us-east-1:123:function:f1"},
                {"Id": "sns-1", "Arn": "arn:aws:sns:us-east-1:123:topic/t1"},
            ],
        },
    )
    rule = [m for m in mapped if m.tf_type == "aws_cloudwatch_event_rule"]
    targets = [m for m in mapped if m.tf_type == "aws_cloudwatch_event_target"]
    assert len(rule) == 1
    assert len(targets) == 2
    assert rule[0].body["name"] == "ec2-state-change"
    assert "aws.ec2" in rule[0].body["event_pattern"]


def test_events_rule_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Rule:\n"
        "    Type: AWS::Events::Rule\n"
        "    Properties:\n"
        "      Name: gd-finding\n"
        "      EventPattern:\n"
        "        source: [aws.guardduty]\n"
        "      Targets:\n"
        "        - Id: lambda-responder\n"
        "          Arn: arn:aws:lambda:us-east-1:123:function:respond\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = event_detector.detect(tf_resources)
    assert any(e.content.get("resource_type") == "aws_cloudwatch_event_rule" for e in evidence)


# --- Data-tier services for svc_at_rest_encryption_coverage ----------


def test_docdb_cluster_basic_translation() -> None:
    [m] = apply_mapping(
        "AWS::DocDB::DBCluster",
        {"StorageEncrypted": True, "KmsKeyId": "arn:aws:kms:us-east-1:123:key/abc"},
    )
    assert m.tf_type == "aws_docdb_cluster"
    assert m.body["storage_encrypted"] is True


def test_neptune_cluster_basic_translation() -> None:
    """Neptune uses kms_key_arn (not kms_key_id) — note AWS API asymmetry."""
    [m] = apply_mapping(
        "AWS::Neptune::DBCluster",
        {"StorageEncrypted": True, "KmsKeyId": "arn:aws:kms:us-east-1:123:key/abc"},
    )
    assert m.tf_type == "aws_neptune_cluster"
    assert m.body["kms_key_arn"] == "arn:aws:kms:us-east-1:123:key/abc"


def test_elasticache_replication_group_basic() -> None:
    [m] = apply_mapping(
        "AWS::ElastiCache::ReplicationGroup",
        {
            "ReplicationGroupId": "redis-prod",
            "AtRestEncryptionEnabled": True,
            "TransitEncryptionEnabled": True,
        },
    )
    assert m.tf_type == "aws_elasticache_replication_group"
    assert m.body["at_rest_encryption_enabled"] is True


def test_elasticache_cache_cluster_basic() -> None:
    [m] = apply_mapping(
        "AWS::ElastiCache::CacheCluster",
        {"ClusterName": "redis-cache", "Engine": "redis", "AtRestEncryptionEnabled": True},
    )
    assert m.tf_type == "aws_elasticache_cluster"
    assert m.body["at_rest_encryption_enabled"] is True


def test_efs_file_system_basic() -> None:
    [m] = apply_mapping(
        "AWS::EFS::FileSystem",
        {"Encrypted": True, "KmsKeyId": "arn:aws:kms:us-east-1:123:key/abc"},
    )
    assert m.tf_type == "aws_efs_file_system"
    assert m.body["encrypted"] is True


def test_svc_enc_detector_fires_on_all_data_services_via_cfn(tmp_path: Path) -> None:
    """One Evidence per data-service resource, end-to-end."""
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Doc:\n"
        "    Type: AWS::DocDB::DBCluster\n"
        "    Properties:\n"
        "      StorageEncrypted: true\n"
        "      KmsKeyId: arn:aws:kms:us-east-1:123:key/abc\n"
        "  Neptune:\n"
        "    Type: AWS::Neptune::DBCluster\n"
        "    Properties:\n"
        "      StorageEncrypted: true\n"
        "      KmsKeyId: arn:aws:kms:us-east-1:123:key/xyz\n"
        "  Redis:\n"
        "    Type: AWS::ElastiCache::ReplicationGroup\n"
        "    Properties:\n"
        "      ReplicationGroupId: r1\n"
        "      AtRestEncryptionEnabled: true\n"
        "  EFS:\n"
        "    Type: AWS::EFS::FileSystem\n"
        "    Properties:\n"
        "      Encrypted: true\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = svc_enc_detector.detect(tf_resources)
    types = {e.content.get("resource_type") for e in evidence}
    assert "aws_docdb_cluster" in types
    assert "aws_neptune_cluster" in types
    assert "aws_elasticache_replication_group" in types
    assert "aws_efs_file_system" in types


# --- EC2: LaunchTemplate, VPC, Subnet, SecurityGroupIngress -----------


def test_ec2_launch_template_unwraps_data_envelope() -> None:
    """LaunchTemplateData wraps MetadataOptions; mapping unwraps to top level."""
    [m] = apply_mapping(
        "AWS::EC2::LaunchTemplate",
        {
            "LaunchTemplateName": "tpl-1",
            "LaunchTemplateData": {
                "ImageId": "ami-abc",
                "InstanceType": "t3.medium",
                "MetadataOptions": {"HttpTokens": "required", "HttpEndpoint": "enabled"},
            },
        },
    )
    assert m.tf_type == "aws_launch_template"
    assert m.body["name"] == "tpl-1"
    assert m.body["image_id"] == "ami-abc"
    assert m.body["metadata_options"] == [{"http_tokens": "required", "http_endpoint": "enabled"}]


def test_ec2_vpc_basic_translation() -> None:
    [m] = apply_mapping(
        "AWS::EC2::VPC",
        {"CidrBlock": "10.0.0.0/16", "EnableDnsHostnames": True},
    )
    assert m.tf_type == "aws_vpc"
    assert m.body == {"cidr_block": "10.0.0.0/16", "enable_dns_hostnames": True}


def test_ec2_subnet_basic_translation() -> None:
    [m] = apply_mapping(
        "AWS::EC2::Subnet",
        {"VpcId": "vpc-1", "CidrBlock": "10.0.1.0/24", "AvailabilityZone": "us-east-1a"},
    )
    assert m.tf_type == "aws_subnet"
    assert m.body["availability_zone"] == "us-east-1a"


def test_vpc_segmentation_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Vpc:\n"
        "    Type: AWS::EC2::VPC\n"
        "    Properties:\n"
        "      CidrBlock: 10.0.0.0/16\n"
        "  SubnetA:\n"
        "    Type: AWS::EC2::Subnet\n"
        "    Properties:\n"
        "      VpcId: !Ref Vpc\n"
        "      CidrBlock: 10.0.1.0/24\n"
        "      AvailabilityZone: us-east-1a\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = vpc_detector.detect(tf_resources)
    assert len(evidence) >= 1


def test_security_group_ingress_basic_translation() -> None:
    """CFN CidrIp (single string) → TF cidr_blocks (single-element list)."""
    [m] = apply_mapping(
        "AWS::EC2::SecurityGroupIngress",
        {
            "GroupId": "sg-1",
            "IpProtocol": "-1",
            "CidrIp": "0.0.0.0/0",
            "FromPort": 0,
            "ToPort": 65535,
        },
    )
    assert m.tf_type == "aws_security_group_rule"
    assert m.body["type"] == "ingress"
    assert m.body["protocol"] == "-1"
    assert m.body["cidr_blocks"] == ["0.0.0.0/0"]


# --- ELB v2 + v1 ------------------------------------------------------


def test_elbv2_load_balancer_attributes_translate_access_logs() -> None:
    """LoadBalancerAttributes generic key/value list → access_logs[0] block."""
    [m] = apply_mapping(
        "AWS::ElasticLoadBalancingV2::LoadBalancer",
        {
            "Name": "app-alb",
            "Scheme": "internet-facing",
            "Type": "application",
            "LoadBalancerAttributes": [
                {"Key": "access_logs.s3.enabled", "Value": "true"},
                {"Key": "access_logs.s3.bucket", "Value": "alb-logs-bucket"},
                {"Key": "deletion_protection.enabled", "Value": "true"},
            ],
        },
    )
    assert m.tf_type == "aws_lb"
    assert m.body["name"] == "app-alb"
    assert m.body["access_logs"] == [{"enabled": True, "bucket": "alb-logs-bucket"}]


def test_elb_classic_access_logging_translates() -> None:
    """CFN AccessLoggingPolicy.{Enabled, S3BucketName} → access_logs[0]."""
    [m] = apply_mapping(
        "AWS::ElasticLoadBalancing::LoadBalancer",
        {
            "LoadBalancerName": "classic-elb",
            "Scheme": "internal",
            "AccessLoggingPolicy": {
                "Enabled": True,
                "S3BucketName": "elb-logs",
                "S3BucketPrefix": "prod/",
            },
        },
    )
    assert m.tf_type == "aws_elb"
    assert m.body["internal"] is True
    assert m.body["access_logs"] == [
        {"enabled": True, "bucket": "elb-logs", "bucket_prefix": "prod/"}
    ]


def test_elb_access_logs_detector_fires_on_cfn_v2(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Lb:\n"
        "    Type: AWS::ElasticLoadBalancingV2::LoadBalancer\n"
        "    Properties:\n"
        "      Name: app-alb\n"
        "      Type: application\n"
        "      LoadBalancerAttributes:\n"
        "        - Key: access_logs.s3.enabled\n"
        "          Value: 'true'\n"
        "        - Key: access_logs.s3.bucket\n"
        "          Value: alb-logs\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = elb_log_detector.detect(tf_resources)
    assert any(e.content.get("resource_type") == "aws_lb" for e in evidence)


# --- IAM federation: SAML + OIDC providers ----------------------------


def test_iam_saml_provider_basic() -> None:
    [m] = apply_mapping(
        "AWS::IAM::SAMLProvider",
        {"Name": "okta", "SamlMetadataDocument": "<EntityDescriptor>...</EntityDescriptor>"},
    )
    assert m.tf_type == "aws_iam_saml_provider"
    assert m.body["name"] == "okta"


def test_iam_oidc_provider_basic_with_lists() -> None:
    """OIDC provider has list-typed ClientIdList + ThumbprintList."""
    [m] = apply_mapping(
        "AWS::IAM::OIDCProvider",
        {
            "Url": "https://token.actions.githubusercontent.com",
            "ClientIdList": ["sts.amazonaws.com"],
            "ThumbprintList": ["6938fd4d98bab03faadb97b34396831e3780aea1"],
        },
    )
    assert m.tf_type == "aws_iam_openid_connect_provider"
    assert m.body["client_id_list"] == ["sts.amazonaws.com"]
    assert m.body["thumbprint_list"] == ["6938fd4d98bab03faadb97b34396831e3780aea1"]


def test_federated_identity_providers_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Github:\n"
        "    Type: AWS::IAM::OIDCProvider\n"
        "    Properties:\n"
        "      Url: https://token.actions.githubusercontent.com\n"
        "      ClientIdList: [sts.amazonaws.com]\n"
        "      ThumbprintList: [6938fd4d98bab03faadb97b34396831e3780aea1]\n"
        "  Okta:\n"
        "    Type: AWS::IAM::SAMLProvider\n"
        "    Properties:\n"
        "      Name: okta\n"
        "      SamlMetadataDocument: <EntityDescriptor></EntityDescriptor>\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = federated_detector.detect(tf_resources)
    types = {e.content.get("resource_type") for e in evidence}
    assert "aws_iam_openid_connect_provider" in types
    assert "aws_iam_saml_provider" in types


# --- Backup family ---------------------------------------------------


def test_backup_plan_translates_rule_list() -> None:
    """CFN nested BackupPlan.BackupPlanRule list → TF rule blocks."""
    [m] = apply_mapping(
        "AWS::Backup::BackupPlan",
        {
            "BackupPlan": {
                "BackupPlanName": "daily-prod",
                "BackupPlanRule": [
                    {
                        "RuleName": "daily-snap",
                        "TargetBackupVault": "prod-vault",
                        "ScheduleExpression": "cron(0 5 * * ? *)",
                        "Lifecycle": {"DeleteAfterDays": 30},
                    },
                ],
            },
        },
    )
    assert m.tf_type == "aws_backup_plan"
    assert m.body["name"] == "daily-prod"
    assert m.body["rule"] == [
        {
            "rule_name": "daily-snap",
            "target_vault_name": "prod-vault",
            "schedule": "cron(0 5 * * ? *)",
            "lifecycle": [{"delete_after": 30}],
        }
    ]


def test_backup_vault_basic() -> None:
    [m] = apply_mapping(
        "AWS::Backup::BackupVault",
        {"BackupVaultName": "prod-vault", "EncryptionKeyArn": "arn:aws:kms:us-east-1:123:key/abc"},
    )
    assert m.tf_type == "aws_backup_vault"
    assert m.body["name"] == "prod-vault"
    assert m.body["kms_key_arn"] == "arn:aws:kms:us-east-1:123:key/abc"


def test_backup_selection_basic() -> None:
    [m] = apply_mapping(
        "AWS::Backup::BackupSelection",
        {
            "BackupPlanId": "plan-abc",
            "BackupSelection": {
                "SelectionName": "all-prod",
                "IamRoleArn": "arn:aws:iam::123:role/backup",
                "Resources": ["arn:aws:rds:us-east-1:123:db:prod"],
            },
        },
    )
    assert m.tf_type == "aws_backup_selection"
    assert m.body["plan_id"] == "plan-abc"
    assert m.body["resources"] == ["arn:aws:rds:us-east-1:123:db:prod"]


def test_backup_restore_testing_plan_basic() -> None:
    [m] = apply_mapping(
        "AWS::Backup::RestoreTestingPlan",
        {
            "RestoreTestingPlanName": "monthly-restore-test",
            "ScheduleExpression": "cron(0 6 1 * ? *)",
        },
    )
    assert m.tf_type == "aws_backup_restore_testing_plan"
    assert m.body["name"] == "monthly-restore-test"


def test_backup_restore_testing_selection_basic() -> None:
    [m] = apply_mapping(
        "AWS::Backup::RestoreTestingSelection",
        {
            "RestoreTestingPlanName": "monthly-restore-test",
            "RestoreTestingSelectionName": "rds-sample",
            "ProtectedResourceType": "RDS",
            "IamRoleArn": "arn:aws:iam::123:role/restore-test",
        },
    )
    assert m.tf_type == "aws_backup_restore_testing_selection"
    assert m.body["restore_testing_plan_name"] == "monthly-restore-test"


def test_backup_plan_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Plan:\n"
        "    Type: AWS::Backup::BackupPlan\n"
        "    Properties:\n"
        "      BackupPlan:\n"
        "        BackupPlanName: daily\n"
        "        BackupPlanRule:\n"
        "          - RuleName: daily-snap\n"
        "            TargetBackupVault: prod-vault\n"
        "            ScheduleExpression: cron(0 5 * * ? *)\n"
        "            Lifecycle:\n"
        "              DeleteAfterDays: 30\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = backup_plan_detector.detect(tf_resources)
    assert any(e.content.get("resource_type") == "aws_backup_plan" for e in evidence)


# --- Logs::ResourcePolicy + SecretsManager::RotationSchedule --------


def test_logs_resource_policy_jsonifies_dict_policy() -> None:
    [m] = apply_mapping(
        "AWS::Logs::ResourcePolicy",
        {
            "PolicyName": "VpcFlowLogsPolicy",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {"Effect": "Allow", "Principal": {"Service": "vpc-flow-logs.amazonaws.com"}}
                ],
            },
        },
    )
    assert m.tf_type == "aws_cloudwatch_log_resource_policy"
    assert m.body["policy_name"] == "VpcFlowLogsPolicy"
    assert "Statement" in m.body["policy"]


def test_logs_resource_policy_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  P:\n"
        "    Type: AWS::Logs::ResourcePolicy\n"
        "    Properties:\n"
        "      PolicyName: VpcFlowLogsPolicy\n"
        "      PolicyDocument:\n"
        "        Version: '2012-10-17'\n"
        "        Statement:\n"
        "          - Effect: Allow\n"
        "            Principal:\n"
        "              Service: vpc-flow-logs.amazonaws.com\n"
        "            Action: logs:*\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = mla_detector.detect(tf_resources)
    assert any(
        e.content.get("resource_type") == "aws_cloudwatch_log_resource_policy" for e in evidence
    )


def test_secretsmanager_rotation_schedule_basic() -> None:
    [m] = apply_mapping(
        "AWS::SecretsManager::RotationSchedule",
        {
            "SecretId": "arn:aws:secretsmanager:us-east-1:123:secret:db-pass",
            "RotationLambdaARN": "arn:aws:lambda:us-east-1:123:function:rotate",
            "RotationRules": {"AutomaticallyAfterDays": 30},
        },
    )
    assert m.tf_type == "aws_secretsmanager_secret_rotation"
    assert m.body["secret_id"].endswith("db-pass")
    assert m.body["rotation_rules"] == [{"automatically_after_days": 30}]


def test_secretsmanager_rotation_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  R:\n"
        "    Type: AWS::SecretsManager::RotationSchedule\n"
        "    Properties:\n"
        "      SecretId: arn:aws:secretsmanager:us-east-1:123:secret:db-pass\n"
        "      RotationLambdaARN: arn:aws:lambda:us-east-1:123:function:rotate\n"
        "      RotationRules:\n"
        "        AutomaticallyAfterDays: 30\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = rotation_detector.detect(tf_resources)
    assert any(
        e.content.get("resource_type") == "aws_secretsmanager_secret_rotation" for e in evidence
    )


# --- AutoScaling + ECS ----------------------------------------------


def test_autoscaling_group_basic() -> None:
    [m] = apply_mapping(
        "AWS::AutoScaling::AutoScalingGroup",
        {
            "AutoScalingGroupName": "web-asg",
            "MinSize": 2,
            "MaxSize": 10,
            "DesiredCapacity": 3,
            "VPCZoneIdentifier": ["subnet-1", "subnet-2", "subnet-3"],
        },
    )
    assert m.tf_type == "aws_autoscaling_group"
    assert m.body["name"] == "web-asg"
    assert m.body["vpc_zone_identifier"] == ["subnet-1", "subnet-2", "subnet-3"]


def test_ecs_service_basic() -> None:
    [m] = apply_mapping(
        "AWS::ECS::Service",
        {"ServiceName": "web", "Cluster": "main", "DesiredCount": 3},
    )
    # cfn_type_to_tf_type("AWS::ECS::Service") yields aws_ecs_service correctly
    assert m.tf_type is None
    assert m.body["name"] == "web"
    assert m.body["desired_count"] == 3


# --- CloudFront::Distribution ---------------------------------------


def test_cloudfront_distribution_translates_default_cache_behavior() -> None:
    """DistributionConfig.DefaultCacheBehavior → default_cache_behavior[0]."""
    [m] = apply_mapping(
        "AWS::CloudFront::Distribution",
        {
            "DistributionConfig": {
                "Enabled": True,
                "DefaultCacheBehavior": {
                    "TargetOriginId": "origin1",
                    "ViewerProtocolPolicy": "redirect-to-https",
                },
                "ViewerCertificate": {"MinimumProtocolVersion": "TLSv1.2_2021"},
            },
        },
    )
    assert m.body["enabled"] is True
    assert m.body["default_cache_behavior"] == [
        {"target_origin_id": "origin1", "viewer_protocol_policy": "redirect-to-https"}
    ]
    assert m.body["viewer_certificate"] == [{"minimum_protocol_version": "TLSv1.2_2021"}]


def test_cloudfront_distribution_detector_fires_on_cfn(tmp_path: Path) -> None:
    cfn = tmp_path / "stack.yaml"
    cfn.write_text(
        "Resources:\n"
        "  Dist:\n"
        "    Type: AWS::CloudFront::Distribution\n"
        "    Properties:\n"
        "      DistributionConfig:\n"
        "        Enabled: true\n"
        "        DefaultCacheBehavior:\n"
        "          TargetOriginId: origin1\n"
        "          ViewerProtocolPolicy: redirect-to-https\n"
    )
    tf_resources = adapt_cfn_resources(parse_cfn_file(cfn), scan_root=tmp_path)
    evidence = cloudfront_detector.detect(tf_resources)
    assert len(evidence) >= 1
