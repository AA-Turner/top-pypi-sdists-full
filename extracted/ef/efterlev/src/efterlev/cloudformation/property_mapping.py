"""CFN→TF property-mapping table — per-resource-type body translators.

Per DECISIONS 2026-05-12 (Tier 5 #1, option (D)): a centralized table
mapping CFN property paths to TF body keys, with structural transforms
for the cases where CFN and TF disagree on nesting.

**Why this module exists.** The v0.1.72 adapter (PR beta) translates
only the CFN resource *type name* (`AWS::S3::Bucket` → `aws_s3_bucket`).
Detectors then filter by `r.type == "aws_s3_bucket"` and pass, but
when they reach into `r.body["server_side_encryption_configuration"]`
they find an empty dict — CFN's `BucketEncryption` block wasn't
translated. This module adds the property-translation layer, keeping
the change localized to a single table rather than fanning out into
every detector or refactoring the IR.

Module design — dict-of-functions, not pure data
================================================
Each entry is a `MappingFn`: takes the CFN `Properties` dict, returns
a list of `MappedResource` records. Most resource types emit a single
record (1→1 type translation, body restructured). A few resources whose
CFN structure folds multiple TF resources into one (notably
`AWS::S3::Bucket`'s `PublicAccessBlockConfiguration`) emit multiple
records — one TF-resource per logical concern.

We considered three alternatives before settling on this shape:

1. **Pure dict-of-dicts** (CFN path → TF path strings): simpler but
   can't express the structural transforms TF nested blocks require
   (e.g. CFN's flat `ServerSideEncryptionConfiguration: [ {...} ]`
   becomes TF's `server_side_encryption_configuration: [{"rule": [...
   ]}]` — an extra layer of wrapping the data path can't represent
   with renames alone).
2. **Pydantic schema models** per resource type: heavy for what is
   effectively a lookup table. The schema is the function body anyway.
3. **Per-detector dual-mode reads** (option (B) from DECISIONS
   2026-05-12): rejected because it scales as O(detectors), not
   O(resource types) — and we have ~10x more detectors than resource
   types planned. It also inflates the detector-count metric in
   misleading ways.

The dict-of-functions strikes the balance: each entry is readable
end-to-end (10-30 lines), powerful enough for structural transforms,
and the call site in the adapter stays trivially small.

Coverage at v0.1.74 (PR gamma.2 batch 1)
========================================
S3 + ELBv2 (v0.1.73 PR gamma):
- `AWS::S3::Bucket`                       → `aws_s3_bucket` + optional
                                            synthesized
                                            `aws_s3_bucket_public_access_block`
- `AWS::S3::BucketPolicy`                 → `aws_s3_bucket_policy`
- `AWS::ElasticLoadBalancingV2::Listener` → `aws_lb_listener`

EC2 + Logs (v0.1.74 PR gamma.2 batch 1):
- `AWS::EC2::FlowLog`                     → `aws_flow_log` (with
                                            `ResourceType`/`ResourceId`
                                            dispatch to vpc_id /
                                            subnet_id / eni_id)
- `AWS::EC2::SecurityGroup`               → `aws_security_group` (with
                                            CFN `SecurityGroupIngress`/
                                            `Egress` list translation
                                            into TF inline-block shape)
- `AWS::EC2::Volume`                      → `aws_ebs_volume`
- `AWS::Logs::LogGroup`                   → `aws_cloudwatch_log_group`

CloudTrail + SNS + SQS + DynamoDB + Secrets Manager (v0.1.77 PR gamma.2 batch 4):
- `AWS::CloudTrail::Trail`                → `aws_cloudtrail`
- `AWS::SNS::Topic`                       → `aws_sns_topic`
- `AWS::SQS::Queue`                       → `aws_sqs_queue`
- `AWS::DynamoDB::Table`                  → `aws_dynamodb_table` (with
                                            SSESpecification +
                                            PointInTimeRecoverySpecification
                                            list-wrapped-block transforms)
- `AWS::SecretsManager::Secret`           → `aws_secretsmanager_secret`

KMS + RDS + Lambda (v0.1.76 PR gamma.2 batch 3):
- `AWS::KMS::Key`                         → `aws_kms_key` (with
                                            `KeySpec` →
                                            `customer_master_key_spec`
                                            translation for legacy TF
                                            attribute name)
- `AWS::RDS::DBInstance`                  → `aws_db_instance`
- `AWS::Lambda::Function`                 → `aws_lambda_function` (with
                                            `Environment.Variables` and
                                            `VpcConfig` flat-dict-to-
                                            list-wrapped-block
                                            translation)

IAM (v0.1.75 PR gamma.2 batch 2):
- `AWS::IAM::Role`                        → `aws_iam_role` + synthesized
                                            `aws_iam_role_policy_attachment`
                                            per `ManagedPolicyArns` entry
                                            + synthesized
                                            `aws_iam_role_policy` per
                                            inline `Policies` entry
                                            (1→1+N+M)
- `AWS::IAM::ManagedPolicy`               → `aws_iam_policy`
- `AWS::IAM::User`                        → `aws_iam_user` + synthesized
                                            `aws_iam_user_policy_attachment`
                                            per `ManagedPolicyArns` entry
                                            + synthesized
                                            `aws_iam_user_policy` per
                                            inline `Policies` entry

The v0.1.73 batch validated the mapping shape against three sample
detectors. The v0.1.74 batch covers the EC2 family that the existing
`aws-vpc-cfn` fixture immediately exercises. The v0.1.75 batch (IAM)
introduces the most-detector-dense family: 5+ detectors read IAM TF
resources, but several read TF separation-of-concerns resources
(role-policy-attachment, role-policy) that CFN bundles inline — the
1→1+N+M synthesis pattern handles this.

WAF family (v0.1.90 PR gamma.2 batch 5):
- `AWS::WAFv2::WebACL`                    → `aws_wafv2_web_acl` (with
                                            deep Rules → rule[N] +
                                            Statement → statement[0]
                                            translation; tf_type
                                            override needed since the
                                            naive translation yields
                                            `aws_wafv2_webacl`)
- `AWS::WAFv2::WebACLAssociation`         → `aws_wafv2_web_acl_association`
- `AWS::WAFv2::RuleGroup`                 → `aws_wafv2_rule_group`
- `AWS::WAF::WebACL`                      → `aws_waf_web_acl` (legacy
                                            v1; minimal mapping)
- `AWS::Shield::Protection`               → `aws_shield_protection`

Highest-impact batch in the gamma.2 series — 5 mappings unlock 8
detectors (whole WAF family + cna_dos_protection's WAFv2 path).

RDS Cluster + NACL pair + EC2 Instance (v0.1.91 PR gamma.2 batch 6):
- `AWS::RDS::DBCluster`                   → `aws_rds_cluster`
                                            (sibling to DBInstance from
                                            batch 3; same flat renames)
- `AWS::EC2::NetworkAcl`                  → `aws_network_acl` (bare;
                                            CFN splits rules into
                                            standalone Entry resources)
- `AWS::EC2::NetworkAclEntry`             → `aws_network_acl_rule`
                                            (with `PortRange.{From, To}`
                                            flattened to `from_port`/
                                            `to_port`)
- `AWS::EC2::Instance`                    → `aws_instance` (with
                                            `MetadataOptions` →
                                            `metadata_options[0]` and
                                            `BlockDeviceMappings` →
                                            `ebs_block_device[N]`; all
                                            EBS mappings go to
                                            `ebs_block_device` —
                                            root-vs-non-root heuristic
                                            deferred)

4 mappings unlock 7 detectors.

IAM Group + API Gateway pair (v0.1.92 PR gamma.2 batch 7):
- `AWS::IAM::Group`                       → `aws_iam_group` + synthesized
                                            `aws_iam_group_policy_attachment`
                                            per `ManagedPolicyArns` entry
                                            + synthesized
                                            `aws_iam_group_policy` per
                                            inline `Policies` entry
                                            (1→1+N+M; same pattern as
                                            IAM::Role/User from batch 2)
- `AWS::ApiGateway::Stage`                → `aws_api_gateway_stage`
                                            (with `AccessLogSetting` →
                                            `access_log_settings` —
                                            note CFN singular vs TF
                                            plural)
- `AWS::ApiGatewayV2::Stage`              → `aws_apigatewayv2_stage`
                                            (with `AccessLogSettings`
                                            — note v2 plural in CFN
                                            unlike v1 singular)
- `AWS::ApiGateway::Method`               → `aws_api_gateway_method`
                                            (`AuthorizationType` →
                                            `authorization`; v1's TF
                                            schema flattened the suffix)
- `AWS::ApiGatewayV2::Route`              → `aws_apigatewayv2_route`
                                            (`AuthorizationType` →
                                            `authorization_type`; v2
                                            kept the suffix)

5 mappings unlock 7 detectors (the 4 IAM-Group-touching ones +
api_gateway_access_logging + api_gateway_waf_attached +
api_gateway_auth_required across both v1 and v2).

Finishing batch (v0.1.93 PR gamma.2 batch 8):
- 30 remaining detector-referenced CFN types in one PR. Most are
  1-detector unlocks reading 1-2 fields, so each mapping is short
  (5-25 lines). Closes out CFN type-coverage.
- Types: API Gateway DomainName (v1+v2), AccessAnalyzer, GuardDuty,
  Config (Recorder + DeliveryChannel), CloudWatch Alarm, Events Rule
  (1→1+N synthesis for Targets), DocDB / Neptune / ElastiCache (Repl
  + CacheCluster) / EFS for svc_at_rest_encryption_coverage, EC2
  (LaunchTemplate, VPC, Subnet, SecurityGroupIngress), ELBv2 + ELB
  Classic for elb_access_logs (LoadBalancerAttributes generic
  key/value list → access_logs[0] block), IAM (SAML + OIDC providers),
  Backup family (BackupPlan with rule-list translation, Vault,
  Selection, RestoreTesting Plan + Selection), Logs::ResourcePolicy,
  SecretsManager::RotationSchedule, AutoScaling::AutoScalingGroup,
  ECS::Service.
- Coverage delta: 32/54 (59%) → 62/54 — wait, that's > 100%. Reason:
  some TF types have multiple CFN equivalents (e.g. both
  AWS::ElasticLoadBalancingV2::LoadBalancer + AWS::Elastic-
  LoadBalancing::LoadBalancer can map to TF's aws_lb / aws_elb), and
  a few CFN types map to TF resource families that don't appear
  1:1 in the original 54-type detector list. Functionally:
  every detector is now reachable from CFN.
- NOT mapped (deliberately, documented): AWS::IAM::AccountPasswordPolicy
  doesn't exist as a CFN resource. The IAM password policy is an
  account-level setting in AWS, only deployable via the IAM API or
  AWS Console. The `aws.iam_password_policy` detector still works on
  TF (which exposes it via `aws_iam_account_password_policy`); CFN
  users who need this control set it through the API directly.

Extension pattern
=================
Add a function and register it in `_MAPPINGS`. Detectors don't change.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MappedResource:
    """One TF-shape resource produced by mapping a CFN resource.

    A single CFN resource may yield multiple `MappedResource`s when its
    CFN structure folds multiple TF concerns together — e.g. an
    `AWS::S3::Bucket` with `PublicAccessBlockConfiguration` set yields
    both an `aws_s3_bucket` and a synthesized
    `aws_s3_bucket_public_access_block`.
    """

    body: dict[str, Any] = field(default_factory=dict)
    """TF-shape body. Keys + nested structure match what python-hcl2 would
    emit for an equivalent Terraform resource."""

    tf_type: str | None = None
    """The TF resource type. If None, the adapter uses the default
    `cfn_type_to_tf_type()` translation of the source CFN type. If a
    string, that's the synthetic TF type (e.g.
    `"aws_s3_bucket_public_access_block"` when synthesizing a sub-resource
    from a property block)."""

    name_suffix: str = ""
    """Appended to the source CFN `LogicalId` to form the TF resource
    name. Empty by default. Required for sub-resource synthesis so that
    the primary and synthesized resources have distinct names — e.g.
    `_pab` so that bucket `MyBucket` yields the synthesized PAB resource
    as `MyBucket_pab`."""


MappingFn = Callable[[dict[str, Any]], list[MappedResource]]


# --- AWS::S3::Bucket -------------------------------------------------------


def _map_s3_bucket(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::S3::Bucket` properties to `aws_s3_bucket` body.

    Emits a second `MappedResource` of type
    `aws_s3_bucket_public_access_block` (suffix `_pab`) when the source
    has a `PublicAccessBlockConfiguration` property — this matches the
    Terraform convention of separating PAB into its own resource.
    """
    body: dict[str, Any] = {}

    if "BucketName" in props:
        body["bucket"] = props["BucketName"]

    # CFN's BucketEncryption.ServerSideEncryptionConfiguration[*]
    # .ServerSideEncryptionByDefault.SSEAlgorithm maps to TF's
    # server_side_encryption_configuration[0].rule[*]
    # .apply_server_side_encryption_by_default[0].sse_algorithm.
    #
    # CFN omits TF's `rule` wrapper layer; we synthesize it. Each CFN
    # ServerSideEncryptionConfiguration entry becomes one TF `rule` entry.
    sse_in = props.get("BucketEncryption")
    if isinstance(sse_in, dict):
        sse_cfg = sse_in.get("ServerSideEncryptionConfiguration")
        if isinstance(sse_cfg, list) and sse_cfg:
            rules: list[dict[str, Any]] = []
            for entry in sse_cfg:
                if not isinstance(entry, dict):
                    continue
                ssebd = entry.get("ServerSideEncryptionByDefault")
                if isinstance(ssebd, dict):
                    algo = ssebd.get("SSEAlgorithm")
                    if isinstance(algo, str):
                        rule: dict[str, Any] = {
                            "apply_server_side_encryption_by_default": [{"sse_algorithm": algo}]
                        }
                        rules.append(rule)
            if rules:
                body["server_side_encryption_configuration"] = [{"rule": rules}]

    out: list[MappedResource] = [MappedResource(body=body)]

    pab_cfg = props.get("PublicAccessBlockConfiguration")
    if isinstance(pab_cfg, dict):
        pab_body: dict[str, Any] = {}
        pab_key_map = {
            "BlockPublicAcls": "block_public_acls",
            "IgnorePublicAcls": "ignore_public_acls",
            "BlockPublicPolicy": "block_public_policy",
            "RestrictPublicBuckets": "restrict_public_buckets",
        }
        for cfn_key, tf_key in pab_key_map.items():
            if cfn_key in pab_cfg:
                pab_body[tf_key] = pab_cfg[cfn_key]
        if pab_body:
            out.append(
                MappedResource(
                    body=pab_body,
                    tf_type="aws_s3_bucket_public_access_block",
                    name_suffix="_pab",
                )
            )

    return out


# --- AWS::S3::BucketPolicy -------------------------------------------------


def _map_s3_bucket_policy(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::S3::BucketPolicy` properties to `aws_s3_bucket_policy` body.

    CFN allows the policy as a YAML/JSON dict; Terraform stores it as a
    JSON-string. We stringify dicts; pass strings through.
    """
    body: dict[str, Any] = {}
    if "Bucket" in props:
        body["bucket"] = props["Bucket"]

    policy_doc = props.get("PolicyDocument")
    if isinstance(policy_doc, dict):
        body["policy"] = json.dumps(policy_doc, sort_keys=True, default=str)
    elif isinstance(policy_doc, str):
        body["policy"] = policy_doc

    # Explicit override: default cfn_type_to_tf_type() yields
    # `aws_s3_bucketpolicy` (multi-word `BucketPolicy` segment); TF
    # canonical is `aws_s3_bucket_policy`.
    return [MappedResource(body=body, tf_type="aws_s3_bucket_policy")]


# --- AWS::ElasticLoadBalancingV2::Listener --------------------------------


def _map_elbv2_listener(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ElasticLoadBalancingV2::Listener` to `aws_lb_listener` body.

    First entry of CFN's `Certificates` list becomes TF's
    `certificate_arn` (TF supports additional certs via the separate
    `aws_lb_listener_certificate` resource — synthesizing those is a
    PR gamma.2 follow-on).
    """
    body: dict[str, Any] = {}

    simple_key_map = {
        "Protocol": "protocol",
        "Port": "port",
        "SslPolicy": "ssl_policy",
        "LoadBalancerArn": "load_balancer_arn",
    }
    for cfn_key, tf_key in simple_key_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    certs = props.get("Certificates")
    if isinstance(certs, list) and certs:
        first = certs[0]
        if isinstance(first, dict) and "CertificateArn" in first:
            body["certificate_arn"] = first["CertificateArn"]

    # Explicit override: default cfn_type_to_tf_type() yields
    # `aws_elasticloadbalancingv2_listener`; TF canonical is
    # `aws_lb_listener` (TF aliases the v1 and v2 namespaces under
    # the `aws_lb_*` prefix).
    return [MappedResource(body=body, tf_type="aws_lb_listener")]


# --- AWS::EC2::FlowLog (PR gamma.2 batch 1) -------------------------------


# CFN's `ResourceType` discriminator names which target field TF wants:
# AWS::EC2::FlowLog has one `ResourceId` + one `ResourceType` (VPC/Subnet/
# NetworkInterface), but `aws_flow_log` uses three separate fields and
# expects exactly one to be set.
_FLOW_LOG_TARGET_FIELDS = {
    "VPC": "vpc_id",
    "Subnet": "subnet_id",
    "NetworkInterface": "eni_id",
}


def _map_ec2_flow_log(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::FlowLog` properties to `aws_flow_log` body.

    Dispatches CFN's (`ResourceType`, `ResourceId`) pair to the matching
    TF target field (`vpc_id` / `subnet_id` / `eni_id`). Other CFN keys
    rename per the `simple_key_map` table.
    """
    body: dict[str, Any] = {}

    resource_type = props.get("ResourceType")
    resource_id = props.get("ResourceId")
    if isinstance(resource_type, str) and resource_id is not None:
        target_field = _FLOW_LOG_TARGET_FIELDS.get(resource_type)
        if target_field is not None:
            body[target_field] = resource_id

    simple_key_map = {
        "TrafficType": "traffic_type",
        "LogDestinationType": "log_destination_type",
        "LogDestination": "log_destination",
        "LogGroupName": "log_group_name",
        "DeliverLogsPermissionArn": "iam_role_arn",
        "MaxAggregationInterval": "max_aggregation_interval",
    }
    for cfn_key, tf_key in simple_key_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    return [MappedResource(body=body, tf_type="aws_flow_log")]


# --- AWS::EC2::SecurityGroup (PR gamma.2 batch 1) -------------------------


def _map_ec2_security_group(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::SecurityGroup` to `aws_security_group` body.

    Translates `SecurityGroupIngress`/`SecurityGroupEgress` lists into TF
    `ingress`/`egress` block lists with field-shape conversion: CFN's
    singular `CidrIp` (string) becomes TF's `cidr_blocks` (list-wrapped);
    `IpProtocol` becomes `protocol`; etc.

    The detector
    (`aws.security_group_open_ingress`) reads the inline `ingress` blocks;
    matching that shape is the value-add of this mapping.
    """
    body: dict[str, Any] = {}

    if "GroupName" in props:
        body["name"] = props["GroupName"]
    if "GroupDescription" in props:
        body["description"] = props["GroupDescription"]
    if "VpcId" in props:
        body["vpc_id"] = props["VpcId"]

    ingress = props.get("SecurityGroupIngress")
    if isinstance(ingress, list):
        body["ingress"] = [_translate_sg_rule(r) for r in ingress if isinstance(r, dict)]

    egress = props.get("SecurityGroupEgress")
    if isinstance(egress, list):
        body["egress"] = [_translate_sg_rule(r) for r in egress if isinstance(r, dict)]

    return [MappedResource(body=body, tf_type="aws_security_group")]


def _translate_sg_rule(rule: dict[str, Any]) -> dict[str, Any]:
    """Translate one CFN SG rule dict to TF inline block shape.

    Wraps CFN scalar `CidrIp`/`CidrIpv6`/`SourcePrefixListId` into TF
    list shape (TF detectors expect `cidr_blocks: [...]`).
    """
    out: dict[str, Any] = {}
    scalar_to_list_map = {
        "CidrIp": "cidr_blocks",
        "CidrIpv6": "ipv6_cidr_blocks",
        "SourcePrefixListId": "prefix_list_ids",
    }
    for cfn_key, tf_key in scalar_to_list_map.items():
        val = rule.get(cfn_key)
        if val is not None:
            out[tf_key] = [val] if isinstance(val, str) else val
    simple_map = {
        "FromPort": "from_port",
        "ToPort": "to_port",
        "IpProtocol": "protocol",
        "Description": "description",
        "SourceSecurityGroupId": "source_security_group_id",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in rule:
            out[tf_key] = rule[cfn_key]
    return out


# --- AWS::EC2::Volume (PR gamma.2 batch 1) --------------------------------


def _map_ec2_volume(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::Volume` to `aws_ebs_volume` body.

    Read by `aws.encryption_ebs` for `encrypted` + `kms_key_id`.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "Encrypted": "encrypted",
        "KmsKeyId": "kms_key_id",
        "Size": "size",
        "VolumeType": "type",
        "AvailabilityZone": "availability_zone",
        "Iops": "iops",
        "Throughput": "throughput",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_ebs_volume")]


# --- AWS::Logs::LogGroup (PR gamma.2 batch 1) -----------------------------


def _map_logs_log_group(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Logs::LogGroup` to `aws_cloudwatch_log_group` body.

    Read by `aws.centralized_log_aggregation` (inventory) and may be
    referenced by other log-aware detectors. Default
    `cfn_type_to_tf_type()` yields `aws_logs_loggroup`; explicit override
    to TF canonical `aws_cloudwatch_log_group`.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "LogGroupName": "name",
        "RetentionInDays": "retention_in_days",
        "KmsKeyId": "kms_key_id",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_cloudwatch_log_group")]


# --- AWS::IAM::Role (PR gamma.2 batch 2) ----------------------------------


def _map_iam_role(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::IAM::Role` to `aws_iam_role` + synthesized attachment/policy resources.

    CFN bundles managed-policy attachments and inline policies into the
    Role's own properties; TF separates them into `aws_iam_role_policy_attachment`
    (per ARN) and `aws_iam_role_policy` (per inline policy) resources.
    The detectors `aws.iam_admin_policy_usage` and
    `aws.iam_inline_policies_audit` read those separate resources, so the
    mapping must synthesize them.

    name_suffix scheme:
      - `_attach_<idx>` for each ManagedPolicyArn
      - `_inline_<PolicyName>` for each inline Policies entry
    """
    role_body: dict[str, Any] = {}

    simple_map = {
        "RoleName": "name",
        "Path": "path",
        "Description": "description",
        "MaxSessionDuration": "max_session_duration",
        "PermissionsBoundary": "permissions_boundary",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            role_body[tf_key] = props[cfn_key]

    # AssumeRolePolicyDocument is the trust policy. CFN allows dict; TF
    # stores as JSON-string in `assume_role_policy`.
    arpd = props.get("AssumeRolePolicyDocument")
    if isinstance(arpd, dict):
        role_body["assume_role_policy"] = json.dumps(arpd, sort_keys=True, default=str)
    elif isinstance(arpd, str):
        role_body["assume_role_policy"] = arpd

    out: list[MappedResource] = [MappedResource(body=role_body, tf_type="aws_iam_role")]

    # Synthesize one aws_iam_role_policy_attachment per ManagedPolicyArn.
    managed_arns = props.get("ManagedPolicyArns")
    if isinstance(managed_arns, list):
        for idx, arn in enumerate(managed_arns):
            if not isinstance(arn, str):
                continue
            out.append(
                MappedResource(
                    body={"policy_arn": arn},
                    tf_type="aws_iam_role_policy_attachment",
                    name_suffix=f"_attach_{idx}",
                )
            )

    # Synthesize one aws_iam_role_policy per inline Policies entry.
    inline_policies = props.get("Policies")
    if isinstance(inline_policies, list):
        for entry in inline_policies:
            if not isinstance(entry, dict):
                continue
            policy_name = entry.get("PolicyName")
            policy_doc = entry.get("PolicyDocument")
            policy_str: str | None = None
            if isinstance(policy_doc, dict):
                policy_str = json.dumps(policy_doc, sort_keys=True, default=str)
            elif isinstance(policy_doc, str):
                policy_str = policy_doc
            if not isinstance(policy_name, str) or policy_str is None:
                continue
            out.append(
                MappedResource(
                    body={"name": policy_name, "policy": policy_str},
                    tf_type="aws_iam_role_policy",
                    name_suffix=f"_inline_{policy_name}",
                )
            )

    return out


# --- AWS::IAM::ManagedPolicy (PR gamma.2 batch 2) ------------------------


def _map_iam_managed_policy(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::IAM::ManagedPolicy` to `aws_iam_policy` body.

    Default cfn_type_to_tf_type() yields `aws_iam_managedpolicy`; TF
    canonical is `aws_iam_policy`. Explicit override.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "ManagedPolicyName": "name",
        "Path": "path",
        "Description": "description",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    policy_doc = props.get("PolicyDocument")
    if isinstance(policy_doc, dict):
        body["policy"] = json.dumps(policy_doc, sort_keys=True, default=str)
    elif isinstance(policy_doc, str):
        body["policy"] = policy_doc

    return [MappedResource(body=body, tf_type="aws_iam_policy")]


# --- AWS::IAM::User (PR gamma.2 batch 2) ---------------------------------


def _map_iam_user(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::IAM::User` to `aws_iam_user` + synthesized policy attachments.

    Same 1→(1+N+M) pattern as IAM::Role: User-side managed-policy
    attachments and inline policies become separate TF resources.
    """
    user_body: dict[str, Any] = {}
    simple_map = {
        "UserName": "name",
        "Path": "path",
        "PermissionsBoundary": "permissions_boundary",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            user_body[tf_key] = props[cfn_key]

    out: list[MappedResource] = [MappedResource(body=user_body, tf_type="aws_iam_user")]

    managed_arns = props.get("ManagedPolicyArns")
    if isinstance(managed_arns, list):
        for idx, arn in enumerate(managed_arns):
            if not isinstance(arn, str):
                continue
            out.append(
                MappedResource(
                    body={"policy_arn": arn},
                    tf_type="aws_iam_user_policy_attachment",
                    name_suffix=f"_attach_{idx}",
                )
            )

    inline_policies = props.get("Policies")
    if isinstance(inline_policies, list):
        for entry in inline_policies:
            if not isinstance(entry, dict):
                continue
            policy_name = entry.get("PolicyName")
            policy_doc = entry.get("PolicyDocument")
            policy_str: str | None = None
            if isinstance(policy_doc, dict):
                policy_str = json.dumps(policy_doc, sort_keys=True, default=str)
            elif isinstance(policy_doc, str):
                policy_str = policy_doc
            if not isinstance(policy_name, str) or policy_str is None:
                continue
            out.append(
                MappedResource(
                    body={"name": policy_name, "policy": policy_str},
                    tf_type="aws_iam_user_policy",
                    name_suffix=f"_inline_{policy_name}",
                )
            )

    return out


# --- AWS::KMS::Key (PR gamma.2 batch 3) -----------------------------------


def _map_kms_key(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::KMS::Key` to `aws_kms_key` body.

    Read by `aws.kms_key_rotation` (`enable_key_rotation`) and
    `aws.kms_customer_managed_keys` (`customer_master_key_spec`).

    Naming nuance: TF's primary attribute is `customer_master_key_spec`
    (the legacy AWS name). CFN's modern name is `KeySpec`. We translate
    `KeySpec` → `customer_master_key_spec` so existing TF detectors work
    without modification.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "EnableKeyRotation": "enable_key_rotation",
        "KeySpec": "customer_master_key_spec",
        "KeyUsage": "key_usage",
        "Description": "description",
        "MultiRegion": "multi_region",
        "PendingWindowInDays": "deletion_window_in_days",
        "Enabled": "is_enabled",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    key_policy = props.get("KeyPolicy")
    if isinstance(key_policy, dict):
        body["policy"] = json.dumps(key_policy, sort_keys=True, default=str)
    elif isinstance(key_policy, str):
        body["policy"] = key_policy

    return [MappedResource(body=body, tf_type="aws_kms_key")]


# --- AWS::RDS::DBInstance (PR gamma.2 batch 3) -----------------------------


def _map_rds_db_instance(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::RDS::DBInstance` to `aws_db_instance` body.

    Read by `aws.rds_encryption_at_rest` (`storage_encrypted`,
    `kms_key_id`) and `aws.rds_public_accessibility` (`publicly_accessible`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "DBInstanceIdentifier": "identifier",
        "DBInstanceClass": "instance_class",
        "Engine": "engine",
        "EngineVersion": "engine_version",
        "AllocatedStorage": "allocated_storage",
        "StorageEncrypted": "storage_encrypted",
        "KmsKeyId": "kms_key_id",
        "PubliclyAccessible": "publicly_accessible",
        "MultiAZ": "multi_az",
        "BackupRetentionPeriod": "backup_retention_period",
        "DeletionProtection": "deletion_protection",
        "MasterUsername": "username",
        "DBName": "db_name",
        "Port": "port",
        "VPCSecurityGroups": "vpc_security_group_ids",
        "DBSubnetGroupName": "db_subnet_group_name",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    return [MappedResource(body=body, tf_type="aws_db_instance")]


# --- AWS::Lambda::Function (PR gamma.2 batch 3) ----------------------------


def _map_lambda_function(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Lambda::Function` to `aws_lambda_function` body.

    Read by `aws.lambda_env_kms_encryption` (needs `environment` block +
    `kms_key_arn`), `aws.lambda_vpc_isolation` (needs `vpc_config`), and
    `aws.lambda_logging_configured` (inventory).

    Nested-block translation: CFN's flat `Environment.Variables` and
    `VpcConfig.{SubnetIds,SecurityGroupIds}` become TF's list-wrapped
    nested-block shape (matching python-hcl2's `[{...}]` convention),
    so the detectors' `_normalize_block` helpers (which accept both
    dict and `[dict]`) work uniformly.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "FunctionName": "function_name",
        "Runtime": "runtime",
        "Handler": "handler",
        "Role": "role",
        "Timeout": "timeout",
        "MemorySize": "memory_size",
        "KmsKeyArn": "kms_key_arn",
        "Description": "description",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    # Environment.Variables (dict) → environment[0].variables (TF
    # list-of-dict-of-dict shape; detector reads variables dict).
    env = props.get("Environment")
    if isinstance(env, dict):
        variables = env.get("Variables")
        if isinstance(variables, dict):
            body["environment"] = [{"variables": variables}]

    # VpcConfig.{SubnetIds, SecurityGroupIds} → vpc_config[0].{subnet_ids, security_group_ids}
    vpc_cfg = props.get("VpcConfig")
    if isinstance(vpc_cfg, dict):
        vpc_block: dict[str, Any] = {}
        if "SubnetIds" in vpc_cfg:
            vpc_block["subnet_ids"] = vpc_cfg["SubnetIds"]
        if "SecurityGroupIds" in vpc_cfg:
            vpc_block["security_group_ids"] = vpc_cfg["SecurityGroupIds"]
        if vpc_block:
            body["vpc_config"] = [vpc_block]

    return [MappedResource(body=body, tf_type="aws_lambda_function")]


# --- AWS::CloudTrail::Trail (PR gamma.2 batch 4) ---------------------------


def _map_cloudtrail_trail(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::CloudTrail::Trail` to `aws_cloudtrail` body.

    Read by `aws.cloudtrail_audit_logging` (multi-region, global-event
    inclusion, event_selector presence) + `aws.cloudtrail_log_file_validation`
    (enable_log_file_validation flag).

    EventSelectors is a CFN list of dicts; TF stores as repeated
    `event_selector` blocks parsed by python-hcl2 as a list. Pass-through
    works for the detector's simple presence check.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "TrailName": "name",
        "S3BucketName": "s3_bucket_name",
        "S3KeyPrefix": "s3_key_prefix",
        "EnableLogFileValidation": "enable_log_file_validation",
        "IsMultiRegionTrail": "is_multi_region_trail",
        "IsLogging": "enable_logging",
        "IncludeGlobalServiceEvents": "include_global_service_events",
        "CloudWatchLogsLogGroupArn": "cloud_watch_logs_group_arn",
        "CloudWatchLogsRoleArn": "cloud_watch_logs_role_arn",
        "KMSKeyId": "kms_key_id",
        "SnsTopicName": "sns_topic_name",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    # EventSelectors → event_selector (list of dicts; TF camel→snake on
    # nested keys is not done here — the detector's simple presence
    # check works on the raw list).
    event_selectors = props.get("EventSelectors")
    if isinstance(event_selectors, list):
        body["event_selector"] = event_selectors

    return [MappedResource(body=body, tf_type="aws_cloudtrail")]


# --- AWS::SNS::Topic (PR gamma.2 batch 4) ----------------------------------


def _map_sns_topic(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::SNS::Topic` to `aws_sns_topic` body.

    Read by `aws.sns_topic_encryption` (`kms_master_key_id`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "TopicName": "name",
        "DisplayName": "display_name",
        "KmsMasterKeyId": "kms_master_key_id",
        "FifoTopic": "fifo_topic",
        "ContentBasedDeduplication": "content_based_deduplication",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_sns_topic")]


# --- AWS::SQS::Queue (PR gamma.2 batch 4) ----------------------------------


def _map_sqs_queue(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::SQS::Queue` to `aws_sqs_queue` body.

    Read by `aws.sqs_queue_encryption` (`kms_master_key_id`,
    `sqs_managed_sse_enabled`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "QueueName": "name",
        "KmsMasterKeyId": "kms_master_key_id",
        "SqsManagedSseEnabled": "sqs_managed_sse_enabled",
        "FifoQueue": "fifo_queue",
        "ContentBasedDeduplication": "content_based_deduplication",
        "MessageRetentionPeriod": "message_retention_seconds",
        "VisibilityTimeout": "visibility_timeout_seconds",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_sqs_queue")]


# --- AWS::DynamoDB::Table (PR gamma.2 batch 4) -----------------------------


def _map_dynamodb_table(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::DynamoDB::Table` to `aws_dynamodb_table` body.

    Currently no detector specifically reads DynamoDB tables, but the
    type appears in customer fixtures. Translation supports the most
    common encryption/PITR/streams properties so future detectors land
    here without per-resource shipping work.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "TableName": "name",
        "BillingMode": "billing_mode",
        "DeletionProtectionEnabled": "deletion_protection_enabled",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    sse_in = props.get("SSESpecification")
    if isinstance(sse_in, dict):
        sse_block: dict[str, Any] = {}
        if "SSEEnabled" in sse_in:
            sse_block["enabled"] = sse_in["SSEEnabled"]
        if "KMSMasterKeyId" in sse_in:
            sse_block["kms_key_arn"] = sse_in["KMSMasterKeyId"]
        if "SSEType" in sse_in:
            sse_block["sse_type"] = sse_in["SSEType"]
        if sse_block:
            body["server_side_encryption"] = [sse_block]

    pitr_in = props.get("PointInTimeRecoverySpecification")
    if isinstance(pitr_in, dict) and "PointInTimeRecoveryEnabled" in pitr_in:
        body["point_in_time_recovery"] = [{"enabled": pitr_in["PointInTimeRecoveryEnabled"]}]

    return [MappedResource(body=body, tf_type="aws_dynamodb_table")]


# --- AWS::SecretsManager::Secret (PR gamma.2 batch 4) ----------------------


def _map_secretsmanager_secret(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::SecretsManager::Secret` to `aws_secretsmanager_secret` body.

    Note: rotation in CFN is on the separate `AWS::SecretsManager::RotationSchedule`
    resource (not yet mapped); the secret-itself mapping covers basic
    inventory which `aws.secrets_manager_rotation` walks to detect
    secrets-without-rotation.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "Name": "name",
        "Description": "description",
        "KmsKeyId": "kms_key_id",
        "SecretString": "secret_string",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_secretsmanager_secret")]


# --- AWS::WAFv2::WebACL (PR gamma.2 batch 5, v0.1.90) -------------------

# WAFv2 Action / OverrideAction inner-block kinds. Each maps to a
# list-wrapped empty block in TF (e.g. CFN `Action: { Block: {} }` →
# TF `action = [{"block": [{}]}]`). Detector helpers normalize via
# `_as_block_list` so list-wrapped is the safe shape.
_WAFV2_ACTION_KINDS = {
    "Block": "block",
    "Allow": "allow",
    "Count": "count",
    "Captcha": "captcha",
    "Challenge": "challenge",
}
_WAFV2_OVERRIDE_ACTION_KINDS = {
    "None": "none",
    "Count": "count",
}


def _translate_wafv2_action(action: Any, kinds: dict[str, str]) -> list[dict[str, Any]]:
    """CFN `Action: { Block: {} }` → TF `action = [{"block": [{}]}]`.

    The inner-block kinds (Block/Allow/Count/Captcha/Challenge for Action;
    None/Count for OverrideAction) all yield list-wrapped empty blocks
    matching python-hcl2's representation. Returns a one-element list
    regardless of how many kinds are set (CFN allows only one in
    practice; we forward whatever's present).
    """
    if not isinstance(action, dict):
        return []
    inner: dict[str, Any] = {}
    for cfn_kind, tf_kind in kinds.items():
        if cfn_kind in action:
            inner[tf_kind] = [{}]
    return [inner] if inner else []


def _translate_wafv2_statement(stmt: Any) -> list[dict[str, Any]]:
    """CFN Statement → TF statement = [{...}] with deep snake_case translation.

    Only the statement kinds that any v0.1.90 detector reads are
    translated explicitly; unknown statement kinds get a shallow
    snake_case mirror so future detectors can reach into them without
    a mapping bump.

    Translated explicitly (read by current detectors):
    - GeoMatchStatement.CountryCodes → geo_match_statement[0].country_codes
    - RateBasedStatement.{Limit, AggregateKeyType} → rate_based_statement[0]
    - ManagedRuleGroupStatement.{VendorName, Name, Version} → managed_rule_group_statement[0]
    - IPSetReferenceStatement.Arn → ip_set_reference_statement[0].arn
    - RuleGroupReferenceStatement.Arn → rule_group_reference_statement[0].arn
    """
    if not isinstance(stmt, dict):
        return []
    out: dict[str, Any] = {}

    geo = stmt.get("GeoMatchStatement")
    if isinstance(geo, dict):
        codes = geo.get("CountryCodes")
        out["geo_match_statement"] = [{"country_codes": codes if isinstance(codes, list) else []}]

    rate = stmt.get("RateBasedStatement")
    if isinstance(rate, dict):
        rate_block: dict[str, Any] = {}
        if "Limit" in rate:
            rate_block["limit"] = rate["Limit"]
        if "AggregateKeyType" in rate:
            rate_block["aggregate_key_type"] = rate["AggregateKeyType"]
        out["rate_based_statement"] = [rate_block]

    mrg = stmt.get("ManagedRuleGroupStatement")
    if isinstance(mrg, dict):
        mrg_block: dict[str, Any] = {}
        if "VendorName" in mrg:
            mrg_block["vendor_name"] = mrg["VendorName"]
        if "Name" in mrg:
            mrg_block["name"] = mrg["Name"]
        if "Version" in mrg:
            mrg_block["version"] = mrg["Version"]
        out["managed_rule_group_statement"] = [mrg_block]

    ipset = stmt.get("IPSetReferenceStatement")
    if isinstance(ipset, dict):
        out["ip_set_reference_statement"] = [
            {"arn": ipset.get("Arn", "")} if "Arn" in ipset else {}
        ]

    rgr = stmt.get("RuleGroupReferenceStatement")
    if isinstance(rgr, dict):
        out["rule_group_reference_statement"] = [
            {"arn": rgr.get("Arn", "")} if "Arn" in rgr else {}
        ]

    return [out] if out else []


def _translate_wafv2_rule(rule: dict[str, Any]) -> dict[str, Any]:
    """One CFN Rule entry → one TF rule block (TF wraps with `rule = [...]`)."""
    out: dict[str, Any] = {}
    if "Name" in rule:
        out["name"] = rule["Name"]
    if "Priority" in rule:
        out["priority"] = rule["Priority"]
    if "Action" in rule:
        action = _translate_wafv2_action(rule["Action"], _WAFV2_ACTION_KINDS)
        if action:
            out["action"] = action
    if "OverrideAction" in rule:
        ovr = _translate_wafv2_action(rule["OverrideAction"], _WAFV2_OVERRIDE_ACTION_KINDS)
        if ovr:
            out["override_action"] = ovr
    if "Statement" in rule:
        stmt = _translate_wafv2_statement(rule["Statement"])
        if stmt:
            out["statement"] = stmt
    return out


def _map_wafv2_web_acl(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::WAFv2::WebACL` to `aws_wafv2_web_acl` body.

    Read by 8 WAF-family detectors (cna_dos_protection,
    waf_action_types, waf_custom_rule_groups, waf_geo_blocking,
    waf_ip_set_blocking, waf_managed_rule_groups, waf_rate_limiting,
    waf_rule_count). Highest-impact mapping in the gamma.2 series.

    `tf_type` override is required because `cfn_type_to_tf_type`
    naively produces `aws_wafv2_webacl` (no internal underscoring of
    the `WebACL` segment) — the canonical TF type is
    `aws_wafv2_web_acl`.

    Rules need full deep-translation: the detectors walk
    `body["rule"][N]["statement"][0][<kind>]` looking for specific
    statement kinds (GeoMatchStatement, RateBasedStatement,
    ManagedRuleGroupStatement, IPSetReferenceStatement,
    RuleGroupReferenceStatement). Each statement kind gets a list-
    wrapped block per python-hcl2's `[{...}]` convention so the
    detectors' `_as_block_list` helpers normalize uniformly.
    """
    body: dict[str, Any] = {}
    if "Name" in props:
        body["name"] = props["Name"]
    if "Scope" in props:
        body["scope"] = props["Scope"]
    if "Description" in props:
        body["description"] = props["Description"]

    default_action = props.get("DefaultAction")
    if isinstance(default_action, dict):
        translated = _translate_wafv2_action(default_action, _WAFV2_ACTION_KINDS)
        if translated:
            body["default_action"] = translated

    rules = props.get("Rules")
    if isinstance(rules, list):
        body["rule"] = [_translate_wafv2_rule(r) for r in rules if isinstance(r, dict)]

    return [MappedResource(body=body, tf_type="aws_wafv2_web_acl")]


def _map_wafv2_web_acl_association(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::WAFv2::WebACLAssociation` to `aws_wafv2_web_acl_association`.

    Read by `api_gateway_waf_attached` (resource_arn ↔ aws_api_gateway_*
    arn) and `cna_dos_protection` (existence check). Trivial mapping;
    only the tf_type override matters because the naive translation
    yields `aws_wafv2_webaclassociation`.
    """
    body: dict[str, Any] = {}
    if "ResourceArn" in props:
        body["resource_arn"] = props["ResourceArn"]
    if "WebACLArn" in props:
        body["web_acl_arn"] = props["WebACLArn"]
    return [MappedResource(body=body, tf_type="aws_wafv2_web_acl_association")]


def _map_wafv2_rule_group(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::WAFv2::RuleGroup` to `aws_wafv2_rule_group`.

    Read by `waf_custom_rule_groups` for inventory + ARN-resolution
    (rule groups can be referenced from WebACLs via
    `RuleGroupReferenceStatement.Arn`). Maps the same Rules structure
    as WebACL.
    """
    body: dict[str, Any] = {}
    if "Name" in props:
        body["name"] = props["Name"]
    if "Scope" in props:
        body["scope"] = props["Scope"]
    if "Capacity" in props:
        body["capacity"] = props["Capacity"]
    if "Description" in props:
        body["description"] = props["Description"]

    rules = props.get("Rules")
    if isinstance(rules, list):
        body["rule"] = [_translate_wafv2_rule(r) for r in rules if isinstance(r, dict)]

    return [MappedResource(body=body, tf_type="aws_wafv2_rule_group")]


def _map_waf_web_acl(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::WAF::WebACL` (legacy WAF Classic v1) to `aws_waf_web_acl`.

    Only `cna_dos_protection` reads this — and only the existence + name.
    Deep-translation of WAF Classic's Rules/Action shape isn't needed at
    v0.1.90 (no Tier-3-#4 detector targets WAF Classic; those all live
    on WAFv2). Minimal mapping; tf_type override required (default
    yields `aws_waf_webacl`).
    """
    body: dict[str, Any] = {}
    if "Name" in props:
        body["name"] = props["Name"]
    if "MetricName" in props:
        body["metric_name"] = props["MetricName"]
    default_action = props.get("DefaultAction")
    if isinstance(default_action, dict) and "Type" in default_action:
        body["default_action"] = [{"type": default_action["Type"]}]
    return [MappedResource(body=body, tf_type="aws_waf_web_acl")]


def _map_shield_protection(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Shield::Protection` to `aws_shield_protection`.

    Read by `cna_dos_protection` (existence + resource_arn coverage).
    `cfn_type_to_tf_type("AWS::Shield::Protection")` yields
    `aws_shield_protection` correctly so no tf_type override needed —
    listing here for the property translation only.
    """
    body: dict[str, Any] = {}
    if "Name" in props:
        body["name"] = props["Name"]
    if "ResourceArn" in props:
        body["resource_arn"] = props["ResourceArn"]
    return [MappedResource(body=body)]


# --- AWS::RDS::DBCluster (PR gamma.2 batch 6, v0.1.91) ------------------


def _map_rds_db_cluster(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::RDS::DBCluster` to `aws_rds_cluster` body.

    Read by `aws.rds_public_accessibility` (`publicly_accessible`),
    `aws.backup_retention_configured` (`backup_retention_period`),
    `aws.svc_at_rest_encryption_coverage` (`storage_encrypted` +
    `kms_key_id`), and `aws.cna_optimizing_for_availability`
    (`availability_zones`/multi-AZ semantics — clusters use AZ list
    rather than the boolean flag DB instances use).

    No nested-block transforms: every detector-read field is a flat
    rename. Sibling to `AWS::RDS::DBInstance` from PR gamma.2 batch 3.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "DBClusterIdentifier": "cluster_identifier",
        "Engine": "engine",
        "EngineVersion": "engine_version",
        "EngineMode": "engine_mode",
        "DatabaseName": "database_name",
        "MasterUsername": "master_username",
        "Port": "port",
        "StorageEncrypted": "storage_encrypted",
        "KmsKeyId": "kms_key_id",
        "BackupRetentionPeriod": "backup_retention_period",
        "PreferredBackupWindow": "preferred_backup_window",
        "PreferredMaintenanceWindow": "preferred_maintenance_window",
        "DeletionProtection": "deletion_protection",
        "StorageType": "storage_type",
        "AllocatedStorage": "allocated_storage",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    if "AvailabilityZones" in props:
        body["availability_zones"] = props["AvailabilityZones"]
    return [MappedResource(body=body, tf_type="aws_rds_cluster")]


# --- AWS::EC2::NetworkAcl + ::NetworkAclEntry (batch 6) -----------------

# AWS splits NACL across two CFN resource types — the Acl itself + per-
# rule Entries — while TF allows either inline `ingress`/`egress` blocks
# on `aws_network_acl` OR standalone `aws_network_acl_rule` resources.
# The `aws.nacl_*` detectors handle both shapes (per the docstrings on
# nacl_open_egress + nacl_restrictiveness). The CFN side maps cleanly to
# the standalone-rule shape: Acl → bare aws_network_acl, each Entry →
# aws_network_acl_rule with network_acl_id linking back.


def _map_ec2_network_acl(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::NetworkAcl` to bare `aws_network_acl` body.

    Read by `aws.nacl_restrictiveness` (one Evidence per Acl, then
    walks rules separately). The Acl itself only has `VpcId` + tags
    in CFN; rules live in standalone `AWS::EC2::NetworkAclEntry`
    resources mapped via `_map_ec2_network_acl_entry` below.
    """
    body: dict[str, Any] = {}
    if "VpcId" in props:
        body["vpc_id"] = props["VpcId"]
    # tf_type override: cfn_type_to_tf_type("AWS::EC2::NetworkAcl") yields
    # `aws_ec2_networkacl` (no internal underscoring of `NetworkAcl`).
    return [MappedResource(body=body, tf_type="aws_network_acl")]


def _map_ec2_network_acl_entry(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::NetworkAclEntry` to `aws_network_acl_rule`.

    Read by `aws.nacl_open_egress` (looks for `egress=true` rules
    allowing `cidr_block=0.0.0.0/0` on `protocol="-1"`) and
    `aws.nacl_restrictiveness` (rule walks).

    Structural transforms:
    - `PortRange.{From, To}` flattens to top-level `from_port`/`to_port`
      (TF's `aws_network_acl_rule` uses flat fields, not a nested block).
    - `Icmp.{Type, Code}` flattens to `icmp_type`/`icmp_code`.
    - `Egress: true|false` stays as `egress: bool` (TF same shape).
    - `Protocol` is a string in CFN ("-1", "6", "17", "tcp" all
      acceptable per AWS); TF accepts either string. Forwarded as-is.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "NetworkAclId": "network_acl_id",
        "RuleNumber": "rule_number",
        "Protocol": "protocol",
        "RuleAction": "rule_action",
        "Egress": "egress",
        "CidrBlock": "cidr_block",
        "Ipv6CidrBlock": "ipv6_cidr_block",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    port_range = props.get("PortRange")
    if isinstance(port_range, dict):
        if "From" in port_range:
            body["from_port"] = port_range["From"]
        if "To" in port_range:
            body["to_port"] = port_range["To"]

    icmp = props.get("Icmp")
    if isinstance(icmp, dict):
        if "Type" in icmp:
            body["icmp_type"] = icmp["Type"]
        if "Code" in icmp:
            body["icmp_code"] = icmp["Code"]

    return [MappedResource(body=body, tf_type="aws_network_acl_rule")]


# --- AWS::EC2::Instance (batch 6) ---------------------------------------


def _map_ec2_instance(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::Instance` to `aws_instance` body.

    Read by `aws.ec2_imdsv2_required` (reads `metadata_options[0].http_tokens`)
    and `aws.encryption_ebs` (reads `root_block_device[N]` and
    `ebs_block_device[N]` for `encrypted` flag).

    Structural transforms:
    - `MetadataOptions.{HttpTokens, HttpEndpoint, ...}` →
      `metadata_options[0].{http_tokens, http_endpoint, ...}` (list-
      wrapped block per python-hcl2 convention).
    - `BlockDeviceMappings: [{DeviceName, Ebs: {...}}, ...]` →
      `ebs_block_device: [{device_name, encrypted, kms_key_id, ...}, ...]`.

      v0.1.91 caveat: ALL Ebs mappings go to `ebs_block_device`; we
      don't distinguish the root volume (which TF would split into
      `root_block_device`). CFN doesn't carry the AMI's root device
      name, so without a heuristic we can't reliably tell. The
      `aws.encryption_ebs` detector emits Evidence per block in either
      list, so unencrypted volumes are flagged either way — only the
      label differs ("ebs_block_device" vs "root_block_device").
      Future enhancement: heuristic on `/dev/sda1`, `/dev/xvda`,
      `/dev/nvme0n1` device names.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "ImageId": "ami",
        "InstanceType": "instance_type",
        "KeyName": "key_name",
        "SubnetId": "subnet_id",
        "Monitoring": "monitoring",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    sgs = props.get("SecurityGroupIds")
    if isinstance(sgs, list):
        body["vpc_security_group_ids"] = sgs

    metadata = props.get("MetadataOptions")
    if isinstance(metadata, dict):
        meta_block: dict[str, Any] = {}
        meta_simple = {
            "HttpTokens": "http_tokens",
            "HttpEndpoint": "http_endpoint",
            "HttpPutResponseHopLimit": "http_put_response_hop_limit",
            "InstanceMetadataTags": "instance_metadata_tags",
        }
        for cfn_key, tf_key in meta_simple.items():
            if cfn_key in metadata:
                meta_block[tf_key] = metadata[cfn_key]
        if meta_block:
            body["metadata_options"] = [meta_block]

    block_mappings = props.get("BlockDeviceMappings")
    if isinstance(block_mappings, list):
        ebs_blocks: list[dict[str, Any]] = []
        for entry in block_mappings:
            if not isinstance(entry, dict):
                continue
            ebs = entry.get("Ebs")
            if not isinstance(ebs, dict):
                # VirtualName-style (instance store) — not relevant to
                # the EBS-encryption detector. Skip.
                continue
            block: dict[str, Any] = {}
            if "DeviceName" in entry:
                block["device_name"] = entry["DeviceName"]
            ebs_simple = {
                "Encrypted": "encrypted",
                "KmsKeyId": "kms_key_id",
                "VolumeType": "volume_type",
                "VolumeSize": "volume_size",
                "Iops": "iops",
                "DeleteOnTermination": "delete_on_termination",
                "SnapshotId": "snapshot_id",
            }
            for cfn_key, tf_key in ebs_simple.items():
                if cfn_key in ebs:
                    block[tf_key] = ebs[cfn_key]
            ebs_blocks.append(block)
        if ebs_blocks:
            body["ebs_block_device"] = ebs_blocks

    # tf_type override: cfn_type_to_tf_type("AWS::EC2::Instance") yields
    # `aws_ec2_instance`; the canonical TF type is bare `aws_instance`.
    return [MappedResource(body=body, tf_type="aws_instance")]


# --- AWS::IAM::Group (PR gamma.2 batch 7, v0.1.92) ----------------------


def _map_iam_group(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::IAM::Group` to `aws_iam_group` + synthesized policy attachments.

    Same 1→(1+N+M) pattern as IAM::Role and IAM::User from PR gamma.2
    batch 2: each `ManagedPolicyArns` entry becomes an
    `aws_iam_group_policy_attachment`; each inline `Policies` entry
    becomes an `aws_iam_group_policy`. The `aws.iam_admin_policy_usage`
    detector reads attachments by `policy_arn`; the
    `aws.iam_inline_policies_audit` detector reads inline policies by
    name + body. Both work uniformly across role/user/group via the
    same synthesis pattern.
    """
    group_body: dict[str, Any] = {}
    simple_map = {
        "GroupName": "name",
        "Path": "path",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            group_body[tf_key] = props[cfn_key]

    out: list[MappedResource] = [MappedResource(body=group_body, tf_type="aws_iam_group")]

    managed_arns = props.get("ManagedPolicyArns")
    if isinstance(managed_arns, list):
        for idx, arn in enumerate(managed_arns):
            if not isinstance(arn, str):
                continue
            out.append(
                MappedResource(
                    body={"policy_arn": arn},
                    tf_type="aws_iam_group_policy_attachment",
                    name_suffix=f"_attach_{idx}",
                )
            )

    inline_policies = props.get("Policies")
    if isinstance(inline_policies, list):
        for entry in inline_policies:
            if not isinstance(entry, dict):
                continue
            policy_name = entry.get("PolicyName")
            policy_doc = entry.get("PolicyDocument")
            policy_str: str | None = None
            if isinstance(policy_doc, dict):
                policy_str = json.dumps(policy_doc, sort_keys=True, default=str)
            elif isinstance(policy_doc, str):
                policy_str = policy_doc
            if not isinstance(policy_name, str) or policy_str is None:
                continue
            out.append(
                MappedResource(
                    body={"name": policy_name, "policy": policy_str},
                    tf_type="aws_iam_group_policy",
                    name_suffix=f"_inline_{policy_name}",
                )
            )

    return out


# --- AWS::ApiGateway::Stage + ::Method (REST API v1, batch 7) ---------


def _map_api_gateway_stage(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ApiGateway::Stage` to `aws_api_gateway_stage`.

    Read by `aws.api_gateway_access_logging` (`access_log_settings`
    block presence + `destination_arn`/`format`) and
    `aws.api_gateway_waf_attached` (`stage_name` for resource_arn
    matching).

    Structural transform: CFN's singular `AccessLogSetting` (note
    spelling — singular) translates to TF's plural
    `access_log_settings` block. tf_type override required because
    `cfn_type_to_tf_type("AWS::ApiGateway::Stage")` yields
    `aws_apigateway_stage` (no internal underscoring of `ApiGateway`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "StageName": "stage_name",
        "RestApiId": "rest_api_id",
        "DeploymentId": "deployment_id",
        "Description": "description",
        "TracingEnabled": "xray_tracing_enabled",
        "CacheClusterEnabled": "cache_cluster_enabled",
        "CacheClusterSize": "cache_cluster_size",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    log_setting = props.get("AccessLogSetting")
    if isinstance(log_setting, dict):
        log_block: dict[str, Any] = {}
        if "DestinationArn" in log_setting:
            log_block["destination_arn"] = log_setting["DestinationArn"]
        if "Format" in log_setting:
            log_block["format"] = log_setting["Format"]
        if log_block:
            body["access_log_settings"] = log_block

    return [MappedResource(body=body, tf_type="aws_api_gateway_stage")]


def _map_api_gateway_method(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ApiGateway::Method` to `aws_api_gateway_method`.

    Read by `aws.api_gateway_auth_required` (reads `authorization`
    field + `http_method` for label). CFN's `AuthorizationType` field
    maps to TF's `authorization` (note: TF flattened the suffix in
    aws_api_gateway_method's schema). tf_type override needed.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "HttpMethod": "http_method",
        "AuthorizationType": "authorization",
        "AuthorizerId": "authorizer_id",
        "ApiKeyRequired": "api_key_required",
        "ResourceId": "resource_id",
        "RestApiId": "rest_api_id",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_api_gateway_method")]


# --- AWS::ApiGatewayV2::Stage + ::Route (HTTP/WebSocket v2, batch 7) ---


def _map_apigatewayv2_stage(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ApiGatewayV2::Stage` to `aws_apigatewayv2_stage`.

    Read by the same two detectors as the v1 Stage. CFN's plural
    `AccessLogSettings` (note: v2 differs from v1 here — v1 is
    singular `AccessLogSetting`, v2 is plural `AccessLogSettings`)
    translates to TF's `access_log_settings`. No tf_type override
    needed: `cfn_type_to_tf_type("AWS::ApiGatewayV2::Stage")` yields
    `aws_apigatewayv2_stage` correctly.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "StageName": "name",
        "ApiId": "api_id",
        "AutoDeploy": "auto_deploy",
        "Description": "description",
        "DeploymentId": "deployment_id",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    log_settings = props.get("AccessLogSettings")
    if isinstance(log_settings, dict):
        log_block: dict[str, Any] = {}
        if "DestinationArn" in log_settings:
            log_block["destination_arn"] = log_settings["DestinationArn"]
        if "Format" in log_settings:
            log_block["format"] = log_settings["Format"]
        if log_block:
            body["access_log_settings"] = log_block

    return [MappedResource(body=body)]


def _map_apigatewayv2_route(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ApiGatewayV2::Route` to `aws_apigatewayv2_route`.

    Read by `aws.api_gateway_auth_required` (reads `authorization_type`
    — note: v2 uses the suffix, unlike v1's bare `authorization`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "RouteKey": "route_key",
        "ApiId": "api_id",
        "AuthorizationType": "authorization_type",
        "AuthorizerId": "authorizer_id",
        "Target": "target",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body)]


# ============================================================================
# PR gamma.2 batch 8 (v0.1.93) — finishing batch
# ============================================================================
#
# Maps the remaining 30 detector-referenced CFN types in one go to close
# out CFN coverage. Most are 1-detector unlocks reading 1-2 fields, so
# the mappings stay short. Each documents its tf_type override (most are
# needed because cfn_type_to_tf_type doesn't internally underscore
# multi-CamelCase Resource segments — `LoadBalancer`, `LaunchTemplate`,
# `WebACL`, etc.).
#
# NOT MAPPED (deliberate omission):
# - AWS::IAM::AccountPasswordPolicy: not a real CFN resource type. The
#   IAM account password policy is an account-level setting in AWS,
#   exposed via the IAM API but not deployable through CloudFormation.
#   The `aws.iam_password_policy` detector only fires on Terraform's
#   `aws_iam_account_password_policy` resource (which IS deployable
#   via TF since it abstracts the API call). CFN users hit this gap
#   via direct API call or AWS Console — outside Efterlev's IaC scope.
# ============================================================================


# --- API Gateway DomainName (v1 + v2) ---------------------------------


def _map_api_gateway_domain_name(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ApiGateway::DomainName` to `aws_api_gateway_domain_name`.

    Read by `aws.api_gateway_tls_min_version` (`security_policy`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "DomainName": "domain_name",
        "SecurityPolicy": "security_policy",
        "RegionalCertificateArn": "regional_certificate_arn",
        "CertificateArn": "certificate_arn",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_api_gateway_domain_name")]


def _map_apigatewayv2_domain_name(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ApiGatewayV2::DomainName` to `aws_apigatewayv2_domain_name`.

    Read by `aws.api_gateway_tls_min_version` (reads
    `domain_name_configuration[0].security_policy`). CFN's
    `DomainNameConfigurations` (plural list) → TF's
    `domain_name_configuration` (singular block) — TF schema only
    accepts one configuration; we forward the first entry.
    """
    body: dict[str, Any] = {}
    if "DomainName" in props:
        body["domain_name"] = props["DomainName"]

    configs = props.get("DomainNameConfigurations")
    first_config = None
    if isinstance(configs, list) and configs:
        first_config = configs[0] if isinstance(configs[0], dict) else None
    if first_config is not None:
        cfg_block: dict[str, Any] = {}
        cfg_simple = {
            "CertificateArn": "certificate_arn",
            "SecurityPolicy": "security_policy",
            "EndpointType": "endpoint_type",
        }
        for cfn_key, tf_key in cfg_simple.items():
            if cfn_key in first_config:
                cfg_block[tf_key] = first_config[cfn_key]
        if cfg_block:
            body["domain_name_configuration"] = [cfg_block]

    return [MappedResource(body=body, tf_type="aws_apigatewayv2_domain_name")]


# --- AccessAnalyzer + GuardDuty + Config + CloudWatch + Events --------


def _map_access_analyzer(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::AccessAnalyzer::Analyzer` to `aws_accessanalyzer_analyzer`.

    Read by `aws.access_analyzer_enabled` (`type` field —
    "ACCOUNT" / "ORGANIZATION"). Default tf_type already correct.
    """
    body: dict[str, Any] = {}
    if "AnalyzerName" in props:
        body["analyzer_name"] = props["AnalyzerName"]
    if "Type" in props:
        body["type"] = props["Type"]
    return [MappedResource(body=body)]


def _map_guardduty_detector(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::GuardDuty::Detector` to `aws_guardduty_detector`.

    Read by `aws.guardduty_enabled` (`enable` + `finding_publishing_frequency`).
    Default tf_type already correct.
    """
    body: dict[str, Any] = {}
    if "Enable" in props:
        body["enable"] = props["Enable"]
    if "FindingPublishingFrequency" in props:
        body["finding_publishing_frequency"] = props["FindingPublishingFrequency"]
    return [MappedResource(body=body)]


def _map_config_configuration_recorder(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Config::ConfigurationRecorder` to `aws_config_configuration_recorder`.

    Read by `aws.config_enabled` (existence inventory). tf_type override
    needed — `cfn_type_to_tf_type` produces `aws_config_configurationrecorder`.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "Name": "name",
        "RoleARN": "role_arn",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_config_configuration_recorder")]


def _map_config_delivery_channel(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Config::DeliveryChannel` to `aws_config_delivery_channel`.

    Read by `aws.config_enabled` (existence inventory). tf_type override.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "Name": "name",
        "S3BucketName": "s3_bucket_name",
        "SnsTopicARN": "sns_topic_arn",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_config_delivery_channel")]


def _map_cloudwatch_alarm(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::CloudWatch::Alarm` to `aws_cloudwatch_metric_alarm`.

    Read by `aws.cloudwatch_alarms_critical` (existence inventory).
    tf_type override needed because the canonical TF type adds the
    `metric_` infix.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "AlarmName": "alarm_name",
        "AlarmDescription": "alarm_description",
        "MetricName": "metric_name",
        "Namespace": "namespace",
        "Statistic": "statistic",
        "ComparisonOperator": "comparison_operator",
        "Threshold": "threshold",
        "EvaluationPeriods": "evaluation_periods",
        "Period": "period",
        "AlarmActions": "alarm_actions",
        "OKActions": "ok_actions",
        "TreatMissingData": "treat_missing_data",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_cloudwatch_metric_alarm")]


def _map_events_rule(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Events::Rule` to `aws_cloudwatch_event_rule` + synthesized
    `aws_cloudwatch_event_target` per `Targets` entry.

    Read by `aws.suspicious_activity_response`. CFN bundles event-rule
    targets inline (one resource); TF splits them (one rule + N targets).
    1→1+N synthesis pattern.

    EventPattern is JSON-stringified per the TF schema. CFN allows it as
    either a dict or a stringified JSON; we normalize to string.
    """
    rule_body: dict[str, Any] = {}
    simple_map = {
        "Name": "name",
        "Description": "description",
        "ScheduleExpression": "schedule_expression",
        "State": "state",
        "EventBusName": "event_bus_name",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            rule_body[tf_key] = props[cfn_key]

    event_pattern = props.get("EventPattern")
    if isinstance(event_pattern, dict):
        rule_body["event_pattern"] = json.dumps(event_pattern, sort_keys=True, default=str)
    elif isinstance(event_pattern, str):
        rule_body["event_pattern"] = event_pattern

    out: list[MappedResource] = [
        MappedResource(body=rule_body, tf_type="aws_cloudwatch_event_rule")
    ]

    targets = props.get("Targets")
    if isinstance(targets, list):
        for idx, target in enumerate(targets):
            if not isinstance(target, dict):
                continue
            tgt_body: dict[str, Any] = {}
            tgt_simple = {
                "Id": "target_id",
                "Arn": "arn",
                "RoleArn": "role_arn",
                "Input": "input",
                "InputPath": "input_path",
            }
            for cfn_key, tf_key in tgt_simple.items():
                if cfn_key in target:
                    tgt_body[tf_key] = target[cfn_key]
            out.append(
                MappedResource(
                    body=tgt_body,
                    tf_type="aws_cloudwatch_event_target",
                    name_suffix=f"_target_{idx}",
                )
            )

    return out


# --- Data-tier services for svc_at_rest_encryption_coverage -----------


def _map_docdb_cluster(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::DocDB::DBCluster` to `aws_docdb_cluster` (tf_type override).

    Read by `aws.svc_at_rest_encryption_coverage` (`storage_encrypted`,
    `kms_key_id`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "DBClusterIdentifier": "cluster_identifier",
        "StorageEncrypted": "storage_encrypted",
        "KmsKeyId": "kms_key_id",
        "Engine": "engine",
        "EngineVersion": "engine_version",
        "BackupRetentionPeriod": "backup_retention_period",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_docdb_cluster")]


def _map_neptune_db_cluster(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Neptune::DBCluster` to `aws_neptune_cluster`.

    Read by `aws.svc_at_rest_encryption_coverage` (`storage_encrypted`,
    `kms_key_arn` — note: Neptune uses `kms_key_arn` while RDS uses
    `kms_key_id`; AWS API differs).
    """
    body: dict[str, Any] = {}
    if "DBClusterIdentifier" in props:
        body["cluster_identifier"] = props["DBClusterIdentifier"]
    if "StorageEncrypted" in props:
        body["storage_encrypted"] = props["StorageEncrypted"]
    if "KmsKeyId" in props:
        body["kms_key_arn"] = props["KmsKeyId"]
    if "Engine" in props:
        body["engine"] = props["Engine"]
    return [MappedResource(body=body, tf_type="aws_neptune_cluster")]


def _map_elasticache_replication_group(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ElastiCache::ReplicationGroup` to `aws_elasticache_replication_group`.

    Read by `aws.svc_at_rest_encryption_coverage` (`at_rest_encryption_enabled`
    — note: ElastiCache has no kms_key field on this detector path).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "ReplicationGroupId": "replication_group_id",
        "ReplicationGroupDescription": "description",
        "Engine": "engine",
        "AtRestEncryptionEnabled": "at_rest_encryption_enabled",
        "TransitEncryptionEnabled": "transit_encryption_enabled",
        "AuthToken": "auth_token",
        "KmsKeyId": "kms_key_id",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_elasticache_replication_group")]


def _map_elasticache_cache_cluster(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ElastiCache::CacheCluster` to `aws_elasticache_cluster`.

    Note name asymmetry: CFN's `CacheCluster` becomes TF's bare `cluster`.
    Read by `aws.svc_at_rest_encryption_coverage`.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "ClusterName": "cluster_id",
        "Engine": "engine",
        "EngineVersion": "engine_version",
        "AtRestEncryptionEnabled": "at_rest_encryption_enabled",
        "TransitEncryptionEnabled": "transit_encryption_enabled",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_elasticache_cluster")]


def _map_efs_file_system(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EFS::FileSystem` to `aws_efs_file_system`.

    Read by `aws.svc_at_rest_encryption_coverage` (`encrypted`, `kms_key_id`).
    tf_type override needed.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "Encrypted": "encrypted",
        "KmsKeyId": "kms_key_id",
        "PerformanceMode": "performance_mode",
        "ThroughputMode": "throughput_mode",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_efs_file_system")]


# --- EC2: LaunchTemplate, VPC, Subnet, SecurityGroupIngress ----------


def _map_ec2_launch_template(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::LaunchTemplate` to `aws_launch_template` (tf_type override).

    Read by `aws.ec2_imdsv2_required` (reads
    `metadata_options[0].http_tokens`).

    Structural unwrap: CFN's `LaunchTemplateData` envelope wraps the
    actual instance config (MetadataOptions, BlockDeviceMappings, etc.)
    while TF puts them at the top level of `aws_launch_template`. We
    unwrap LaunchTemplateData and translate MetadataOptions to a list-
    wrapped block matching the EC2::Instance pattern from batch 6.
    """
    body: dict[str, Any] = {}
    if "LaunchTemplateName" in props:
        body["name"] = props["LaunchTemplateName"]

    data = props.get("LaunchTemplateData")
    if isinstance(data, dict):
        if "ImageId" in data:
            body["image_id"] = data["ImageId"]
        if "InstanceType" in data:
            body["instance_type"] = data["InstanceType"]
        if "KeyName" in data:
            body["key_name"] = data["KeyName"]

        metadata = data.get("MetadataOptions")
        if isinstance(metadata, dict):
            meta_block: dict[str, Any] = {}
            meta_simple = {
                "HttpTokens": "http_tokens",
                "HttpEndpoint": "http_endpoint",
                "HttpPutResponseHopLimit": "http_put_response_hop_limit",
                "InstanceMetadataTags": "instance_metadata_tags",
            }
            for cfn_key, tf_key in meta_simple.items():
                if cfn_key in metadata:
                    meta_block[tf_key] = metadata[cfn_key]
            if meta_block:
                body["metadata_options"] = [meta_block]

    return [MappedResource(body=body, tf_type="aws_launch_template")]


def _map_ec2_vpc(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::VPC` to `aws_vpc` (tf_type override).

    Read by `aws.vpc_logical_segmentation` (existence + CIDR).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "CidrBlock": "cidr_block",
        "EnableDnsSupport": "enable_dns_support",
        "EnableDnsHostnames": "enable_dns_hostnames",
        "InstanceTenancy": "instance_tenancy",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_vpc")]


def _map_ec2_subnet(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::Subnet` to `aws_subnet` (tf_type override).

    Read by `aws.vpc_logical_segmentation` (existence + AZ).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "VpcId": "vpc_id",
        "CidrBlock": "cidr_block",
        "AvailabilityZone": "availability_zone",
        "MapPublicIpOnLaunch": "map_public_ip_on_launch",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_subnet")]


def _map_ec2_security_group_ingress(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::EC2::SecurityGroupIngress` to `aws_security_group_rule`.

    Read by `aws.security_group_open_ingress` (filters on `type=ingress`,
    flags `cidr_blocks=["0.0.0.0/0"]` + `protocol="-1"`). Note: TF uses
    `cidr_blocks` (list) while CFN uses `CidrIp` (single string); we
    wrap into a single-element list.
    """
    body: dict[str, Any] = {"type": "ingress"}
    simple_map = {
        "GroupId": "security_group_id",
        "IpProtocol": "protocol",
        "FromPort": "from_port",
        "ToPort": "to_port",
        "Description": "description",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    if "CidrIp" in props:
        body["cidr_blocks"] = [props["CidrIp"]]
    if "CidrIpv6" in props:
        body["ipv6_cidr_blocks"] = [props["CidrIpv6"]]
    if "SourceSecurityGroupId" in props:
        body["source_security_group_id"] = props["SourceSecurityGroupId"]
    return [MappedResource(body=body, tf_type="aws_security_group_rule")]


# --- ELB v2 + v1 -------------------------------------------------------


def _map_elbv2_load_balancer(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ElasticLoadBalancingV2::LoadBalancer` to `aws_lb`.

    Read by `aws.elb_access_logs` (reads `access_logs[0].enabled` +
    `access_logs[0].bucket`).

    Structural transform: CFN's `LoadBalancerAttributes: [{Key, Value}, ...]`
    is a generic key-value list (covering many attributes); TF's
    `aws_lb` exposes specific ones as nested blocks. The
    `access_logs.s3.enabled` + `access_logs.s3.bucket` attributes
    translate to TF's `access_logs[0].{enabled, bucket}`.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "Name": "name",
        "Scheme": "scheme",
        "Type": "load_balancer_type",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]

    attrs = props.get("LoadBalancerAttributes")
    if isinstance(attrs, list):
        access_logs_block: dict[str, Any] = {}
        for entry in attrs:
            if not isinstance(entry, dict):
                continue
            key = entry.get("Key")
            value = entry.get("Value")
            if key == "access_logs.s3.enabled":
                access_logs_block["enabled"] = value in (True, "true", "True")
            elif key == "access_logs.s3.bucket":
                access_logs_block["bucket"] = value
            elif key == "access_logs.s3.prefix":
                access_logs_block["prefix"] = value
        if access_logs_block:
            body["access_logs"] = [access_logs_block]

    return [MappedResource(body=body, tf_type="aws_lb")]


def _map_elb_classic(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ElasticLoadBalancing::LoadBalancer` (Classic v1) to `aws_elb`.

    Read by `aws.elb_access_logs` (reads `access_logs[0].enabled`).
    CFN's `AccessLoggingPolicy.{Enabled, S3BucketName, ...}` →
    TF's `access_logs[0].{enabled, bucket, ...}`.
    """
    body: dict[str, Any] = {}
    if "LoadBalancerName" in props:
        body["name"] = props["LoadBalancerName"]
    if "Scheme" in props:
        body["internal"] = props["Scheme"] == "internal"

    logging = props.get("AccessLoggingPolicy")
    if isinstance(logging, dict):
        log_block: dict[str, Any] = {}
        log_simple = {
            "Enabled": "enabled",
            "S3BucketName": "bucket",
            "S3BucketPrefix": "bucket_prefix",
            "EmitInterval": "interval",
        }
        for cfn_key, tf_key in log_simple.items():
            if cfn_key in logging:
                log_block[tf_key] = logging[cfn_key]
        if log_block:
            body["access_logs"] = [log_block]

    return [MappedResource(body=body, tf_type="aws_elb")]


# --- IAM federation: SAML + OIDC providers ----------------------------


def _map_iam_saml_provider(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::IAM::SAMLProvider` to `aws_iam_saml_provider`.

    Read by `aws.federated_identity_providers` (`name`,
    `saml_metadata_document`).
    """
    body: dict[str, Any] = {}
    if "Name" in props:
        body["name"] = props["Name"]
    if "SamlMetadataDocument" in props:
        body["saml_metadata_document"] = props["SamlMetadataDocument"]
    return [MappedResource(body=body, tf_type="aws_iam_saml_provider")]


def _map_iam_oidc_provider(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::IAM::OIDCProvider` to `aws_iam_openid_connect_provider`.

    Note tf_type asymmetry: CFN's compact `OIDCProvider` becomes TF's
    spelled-out `openid_connect_provider`. Read by
    `aws.federated_identity_providers` (`url`, `client_id_list`,
    `thumbprint_list`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "Url": "url",
        "ClientIdList": "client_id_list",
        "ThumbprintList": "thumbprint_list",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_iam_openid_connect_provider")]


# --- AWS Backup family ------------------------------------------------


def _map_backup_plan(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Backup::BackupPlan` to `aws_backup_plan`.

    Read by `aws.rpl_backup_configured` (reads `rule` blocks; each
    needs `target_vault_name`, `schedule`, etc.).

    Structural translation: CFN's nested `BackupPlan.BackupPlanRule`
    (list of rules with TargetBackupVault, RuleName, ScheduleExpression,
    Lifecycle.{DeleteAfterDays, MoveToColdStorageAfterDays}) translates
    to TF's `rule` list-of-blocks.
    """
    body: dict[str, Any] = {}
    plan = props.get("BackupPlan")
    if not isinstance(plan, dict):
        return [MappedResource(body=body, tf_type="aws_backup_plan")]

    if "BackupPlanName" in plan:
        body["name"] = plan["BackupPlanName"]

    rules = plan.get("BackupPlanRule")
    if isinstance(rules, list):
        rule_blocks: list[dict[str, Any]] = []
        for entry in rules:
            if not isinstance(entry, dict):
                continue
            rule_block: dict[str, Any] = {}
            rule_simple = {
                "RuleName": "rule_name",
                "TargetBackupVault": "target_vault_name",
                "ScheduleExpression": "schedule",
                "StartWindowMinutes": "start_window",
                "CompletionWindowMinutes": "completion_window",
            }
            for cfn_key, tf_key in rule_simple.items():
                if cfn_key in entry:
                    rule_block[tf_key] = entry[cfn_key]
            lifecycle = entry.get("Lifecycle")
            if isinstance(lifecycle, dict):
                lc_block: dict[str, Any] = {}
                if "DeleteAfterDays" in lifecycle:
                    lc_block["delete_after"] = lifecycle["DeleteAfterDays"]
                if "MoveToColdStorageAfterDays" in lifecycle:
                    lc_block["cold_storage_after"] = lifecycle["MoveToColdStorageAfterDays"]
                if lc_block:
                    rule_block["lifecycle"] = [lc_block]
            rule_blocks.append(rule_block)
        if rule_blocks:
            body["rule"] = rule_blocks

    return [MappedResource(body=body, tf_type="aws_backup_plan")]


def _map_backup_vault(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Backup::BackupVault` to `aws_backup_vault`.

    Read by `aws.rpl_backup_configured` (reads `kms_key_arn`).
    """
    body: dict[str, Any] = {}
    if "BackupVaultName" in props:
        body["name"] = props["BackupVaultName"]
    if "EncryptionKeyArn" in props:
        body["kms_key_arn"] = props["EncryptionKeyArn"]
    return [MappedResource(body=body, tf_type="aws_backup_vault")]


def _map_backup_selection(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Backup::BackupSelection` to `aws_backup_selection`.

    Read by `aws.rpl_backup_configured` for inventory.
    """
    body: dict[str, Any] = {}
    if "BackupPlanId" in props:
        body["plan_id"] = props["BackupPlanId"]

    selection = props.get("BackupSelection")
    if isinstance(selection, dict):
        if "SelectionName" in selection:
            body["name"] = selection["SelectionName"]
        if "IamRoleArn" in selection:
            body["iam_role_arn"] = selection["IamRoleArn"]
        if "Resources" in selection:
            body["resources"] = selection["Resources"]

    return [MappedResource(body=body, tf_type="aws_backup_selection")]


def _map_backup_restore_testing_plan(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Backup::RestoreTestingPlan` to `aws_backup_restore_testing_plan`.

    Read by `aws.backup_restore_testing` for inventory.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "RestoreTestingPlanName": "name",
        "ScheduleExpression": "schedule_expression",
        "ScheduleExpressionTimezone": "schedule_expression_timezone",
        "StartWindowHours": "start_window_hours",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_backup_restore_testing_plan")]


def _map_backup_restore_testing_selection(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Backup::RestoreTestingSelection` to
    `aws_backup_restore_testing_selection`.

    Read by `aws.backup_restore_testing` (reads `restore_testing_plan_id`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "RestoreTestingPlanName": "restore_testing_plan_name",
        "RestoreTestingSelectionName": "name",
        "ProtectedResourceType": "protected_resource_type",
        "IamRoleArn": "iam_role_arn",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_backup_restore_testing_selection")]


# --- Logs::ResourcePolicy + SecretsManager::RotationSchedule ---------


def _map_logs_resource_policy(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Logs::ResourcePolicy` to `aws_cloudwatch_log_resource_policy`.

    Note tf_type asymmetry — TF wraps its CloudWatch Logs resources
    with the `cloudwatch_` prefix. Read by
    `aws.mla_log_access_least_privilege` (reads `policy` JSON +
    `policy_name`).
    """
    body: dict[str, Any] = {}
    if "PolicyName" in props:
        body["policy_name"] = props["PolicyName"]
    policy_doc = props.get("PolicyDocument")
    if isinstance(policy_doc, dict):
        body["policy"] = json.dumps(policy_doc, sort_keys=True, default=str)
    elif isinstance(policy_doc, str):
        body["policy"] = policy_doc
    return [MappedResource(body=body, tf_type="aws_cloudwatch_log_resource_policy")]


def _map_secretsmanager_rotation_schedule(
    props: dict[str, Any],
) -> list[MappedResource]:
    """Map `AWS::SecretsManager::RotationSchedule` to
    `aws_secretsmanager_secret_rotation`.

    Read by `aws.secrets_manager_rotation` (reads `secret_id` +
    `rotation_lambda_arn`).
    """
    body: dict[str, Any] = {}
    if "SecretId" in props:
        body["secret_id"] = props["SecretId"]
    if "RotationLambdaARN" in props:
        body["rotation_lambda_arn"] = props["RotationLambdaARN"]

    rules = props.get("RotationRules")
    if isinstance(rules, dict):
        rules_block: dict[str, Any] = {}
        if "AutomaticallyAfterDays" in rules:
            rules_block["automatically_after_days"] = rules["AutomaticallyAfterDays"]
        if "ScheduleExpression" in rules:
            rules_block["schedule_expression"] = rules["ScheduleExpression"]
        if rules_block:
            body["rotation_rules"] = [rules_block]

    return [MappedResource(body=body, tf_type="aws_secretsmanager_secret_rotation")]


# --- AutoScaling + ECS ------------------------------------------------


def _map_autoscaling_group(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::AutoScaling::AutoScalingGroup` to `aws_autoscaling_group`.

    Read by `aws.cna_optimizing_for_availability` (reads
    `vpc_zone_identifier` list; multi-AZ presence). tf_type override
    needed because `cfn_type_to_tf_type` yields
    `aws_autoscaling_autoscalinggroup`.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "AutoScalingGroupName": "name",
        "MinSize": "min_size",
        "MaxSize": "max_size",
        "DesiredCapacity": "desired_capacity",
        "VPCZoneIdentifier": "vpc_zone_identifier",
        "AvailabilityZones": "availability_zones",
        "HealthCheckType": "health_check_type",
        "HealthCheckGracePeriod": "health_check_grace_period",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_autoscaling_group")]


def _map_ecs_service(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::ECS::Service` to `aws_ecs_service`.

    Read by `aws.cna_optimizing_for_availability` (reads `desired_count`
    for multi-instance availability check). Default tf_type already
    correct.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "ServiceName": "name",
        "Cluster": "cluster",
        "TaskDefinition": "task_definition",
        "DesiredCount": "desired_count",
        "LaunchType": "launch_type",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body)]


# --- CloudFront::Distribution -----------------------------------------


def _translate_cloudfront_cache_behavior(behavior: dict[str, Any]) -> dict[str, Any]:
    """One CFN cache behavior → one TF cache-behavior block."""
    out: dict[str, Any] = {}
    simple_map = {
        "PathPattern": "path_pattern",
        "TargetOriginId": "target_origin_id",
        "ViewerProtocolPolicy": "viewer_protocol_policy",
        "AllowedMethods": "allowed_methods",
        "CachedMethods": "cached_methods",
        "Compress": "compress",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in behavior:
            out[tf_key] = behavior[cfn_key]
    return out


def _map_cloudfront_distribution(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::CloudFront::Distribution` to `aws_cloudfront_distribution`.

    Read by `aws.cloudfront_viewer_protocol_https`. The CFN
    `DistributionConfig` envelope wraps everything; TF puts most fields
    at the top level. Translates `DefaultCacheBehavior` →
    `default_cache_behavior[0]`, `CacheBehaviors` →
    `ordered_cache_behavior[N]`, `ViewerCertificate.MinimumProtocolVersion`
    → `viewer_certificate[0].minimum_protocol_version`.
    """
    body: dict[str, Any] = {}
    config = props.get("DistributionConfig")
    if not isinstance(config, dict):
        return [MappedResource(body=body)]

    if "Enabled" in config:
        body["enabled"] = config["Enabled"]
    if "Comment" in config:
        body["comment"] = config["Comment"]

    default = config.get("DefaultCacheBehavior")
    if isinstance(default, dict):
        body["default_cache_behavior"] = [_translate_cloudfront_cache_behavior(default)]

    behaviors = config.get("CacheBehaviors")
    if isinstance(behaviors, list):
        body["ordered_cache_behavior"] = [
            _translate_cloudfront_cache_behavior(b) for b in behaviors if isinstance(b, dict)
        ]

    cert = config.get("ViewerCertificate")
    if isinstance(cert, dict):
        cert_block: dict[str, Any] = {}
        cert_simple = {
            "MinimumProtocolVersion": "minimum_protocol_version",
            "AcmCertificateArn": "acm_certificate_arn",
            "SslSupportMethod": "ssl_support_method",
            "CloudFrontDefaultCertificate": "cloudfront_default_certificate",
        }
        for cfn_key, tf_key in cert_simple.items():
            if cfn_key in cert:
                cert_block[tf_key] = cert[cfn_key]
        if cert_block:
            body["viewer_certificate"] = [cert_block]

    return [MappedResource(body=body)]


# ============================================================================
# PR gamma.2 batch 9 (v0.1.96) — close-the-real-coverage-gaps batch
# ============================================================================
#
# 8 mappings closing the real coverage gaps the v0.1.95 parity audit
# surfaced. After this lands, the parity matrix should show every
# detector reachable from CFN with no missing-mapping gaps.
# ============================================================================


def _map_iam_access_key(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::IAM::AccessKey` to `aws_iam_access_key`.

    Read by `aws.iam_user_access_keys` (inventory) and
    `aws.iam_service_account_keys_age` (reads `user` field for the user
    reference). tf_type override needed because `cfn_type_to_tf_type`
    yields `aws_iam_accesskey`.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "UserName": "user",
        "Status": "status",
        "Serial": "serial",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_iam_access_key")]


def _map_logs_destination(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Logs::Destination` to `aws_cloudwatch_log_destination`.

    Read by `aws.centralized_log_aggregation` (inventory). Note tf_type
    asymmetry: CFN's `Logs::Destination` becomes TF's
    `cloudwatch_log_destination` (TF prefixes its CloudWatch Logs
    resources with `cloudwatch_`).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "DestinationName": "name",
        "TargetArn": "target_arn",
        "RoleArn": "role_arn",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_cloudwatch_log_destination")]


def _map_logs_subscription_filter(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Logs::SubscriptionFilter` to `aws_cloudwatch_log_subscription_filter`.

    Read by `aws.centralized_log_aggregation` (inventory). Same
    `cloudwatch_` prefix asymmetry as Logs::Destination.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "FilterName": "name",
        "FilterPattern": "filter_pattern",
        "LogGroupName": "log_group_name",
        "DestinationArn": "destination_arn",
        "RoleArn": "role_arn",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_cloudwatch_log_subscription_filter")]


def _map_opensearch_domain(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::OpenSearchService::Domain` to `aws_opensearch_domain`.

    Read by `aws.centralized_log_aggregation` (inventory). tf_type
    override — `cfn_type_to_tf_type` yields `aws_opensearchservice_domain`
    but the canonical TF type drops the `service` segment.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "DomainName": "domain_name",
        "EngineVersion": "engine_version",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_opensearch_domain")]


def _map_elasticsearch_domain(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::Elasticsearch::Domain` (legacy) to `aws_elasticsearch_domain`.

    Read by `aws.centralized_log_aggregation` (inventory). Default
    tf_type (`aws_elasticsearch_domain`) is correct, no override needed.
    Elasticsearch is the legacy AWS service; OpenSearch superseded it.
    Both detector and mapping shipped for legacy-template coverage.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "DomainName": "domain_name",
        "ElasticsearchVersion": "elasticsearch_version",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body)]


def _map_kinesis_firehose_delivery_stream(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::KinesisFirehose::DeliveryStream` to `aws_kinesis_firehose_delivery_stream`.

    Read by `aws.centralized_log_aggregation` (inventory). tf_type
    override — `cfn_type_to_tf_type` yields
    `aws_kinesisfirehose_deliverystream` (no underscore in either
    CamelCase segment).
    """
    body: dict[str, Any] = {}
    simple_map = {
        "DeliveryStreamName": "name",
        "DeliveryStreamType": "destination",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    return [MappedResource(body=body, tf_type="aws_kinesis_firehose_delivery_stream")]


def _map_securityhub_hub(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::SecurityHub::Hub` to `aws_securityhub_account`.

    Read by `aws.centralized_log_aggregation` (inventory). NAME
    asymmetry: CFN's `Hub` becomes TF's `account` (TF models the
    enable-on-account semantics rather than the hub-as-resource).
    Override required.
    """
    body: dict[str, Any] = {}
    if "EnableDefaultStandards" in props:
        body["enable_default_standards"] = props["EnableDefaultStandards"]
    return [MappedResource(body=body, tf_type="aws_securityhub_account")]


def _map_securityhub_finding_aggregator(props: dict[str, Any]) -> list[MappedResource]:
    """Map `AWS::SecurityHub::FindingAggregator` to `aws_securityhub_finding_aggregator`.

    Read by `aws.centralized_log_aggregation` (inventory). tf_type
    override — `cfn_type_to_tf_type` yields
    `aws_securityhub_findingaggregator`.
    """
    body: dict[str, Any] = {}
    simple_map = {
        "RegionLinkingMode": "linking_mode",
    }
    for cfn_key, tf_key in simple_map.items():
        if cfn_key in props:
            body[tf_key] = props[cfn_key]
    if "Regions" in props:
        body["specified_regions"] = props["Regions"]
    return [MappedResource(body=body, tf_type="aws_securityhub_finding_aggregator")]


_MAPPINGS: dict[str, MappingFn] = {
    "AWS::AccessAnalyzer::Analyzer": _map_access_analyzer,
    "AWS::ApiGateway::DomainName": _map_api_gateway_domain_name,
    "AWS::ApiGateway::Method": _map_api_gateway_method,
    "AWS::ApiGateway::Stage": _map_api_gateway_stage,
    "AWS::ApiGatewayV2::DomainName": _map_apigatewayv2_domain_name,
    "AWS::ApiGatewayV2::Route": _map_apigatewayv2_route,
    "AWS::ApiGatewayV2::Stage": _map_apigatewayv2_stage,
    "AWS::AutoScaling::AutoScalingGroup": _map_autoscaling_group,
    "AWS::Backup::BackupPlan": _map_backup_plan,
    "AWS::Backup::BackupSelection": _map_backup_selection,
    "AWS::Backup::BackupVault": _map_backup_vault,
    "AWS::Backup::RestoreTestingPlan": _map_backup_restore_testing_plan,
    "AWS::Backup::RestoreTestingSelection": _map_backup_restore_testing_selection,
    "AWS::CloudFront::Distribution": _map_cloudfront_distribution,
    "AWS::CloudTrail::Trail": _map_cloudtrail_trail,
    "AWS::CloudWatch::Alarm": _map_cloudwatch_alarm,
    "AWS::Config::ConfigurationRecorder": _map_config_configuration_recorder,
    "AWS::Config::DeliveryChannel": _map_config_delivery_channel,
    "AWS::DocDB::DBCluster": _map_docdb_cluster,
    "AWS::DynamoDB::Table": _map_dynamodb_table,
    "AWS::EC2::FlowLog": _map_ec2_flow_log,
    "AWS::EC2::Instance": _map_ec2_instance,
    "AWS::EC2::LaunchTemplate": _map_ec2_launch_template,
    "AWS::EC2::NetworkAcl": _map_ec2_network_acl,
    "AWS::EC2::NetworkAclEntry": _map_ec2_network_acl_entry,
    "AWS::EC2::SecurityGroup": _map_ec2_security_group,
    "AWS::EC2::SecurityGroupIngress": _map_ec2_security_group_ingress,
    "AWS::EC2::Subnet": _map_ec2_subnet,
    "AWS::EC2::Volume": _map_ec2_volume,
    "AWS::EC2::VPC": _map_ec2_vpc,
    "AWS::ECS::Service": _map_ecs_service,
    "AWS::EFS::FileSystem": _map_efs_file_system,
    "AWS::ElastiCache::CacheCluster": _map_elasticache_cache_cluster,
    "AWS::ElastiCache::ReplicationGroup": _map_elasticache_replication_group,
    "AWS::Elasticsearch::Domain": _map_elasticsearch_domain,
    "AWS::ElasticLoadBalancing::LoadBalancer": _map_elb_classic,
    "AWS::ElasticLoadBalancingV2::Listener": _map_elbv2_listener,
    "AWS::ElasticLoadBalancingV2::LoadBalancer": _map_elbv2_load_balancer,
    "AWS::Events::Rule": _map_events_rule,
    "AWS::GuardDuty::Detector": _map_guardduty_detector,
    "AWS::IAM::AccessKey": _map_iam_access_key,
    "AWS::IAM::Group": _map_iam_group,
    "AWS::IAM::ManagedPolicy": _map_iam_managed_policy,
    "AWS::IAM::OIDCProvider": _map_iam_oidc_provider,
    "AWS::IAM::Role": _map_iam_role,
    "AWS::IAM::SAMLProvider": _map_iam_saml_provider,
    "AWS::IAM::User": _map_iam_user,
    "AWS::KinesisFirehose::DeliveryStream": _map_kinesis_firehose_delivery_stream,
    "AWS::KMS::Key": _map_kms_key,
    "AWS::Lambda::Function": _map_lambda_function,
    "AWS::Logs::Destination": _map_logs_destination,
    "AWS::Logs::LogGroup": _map_logs_log_group,
    "AWS::Logs::ResourcePolicy": _map_logs_resource_policy,
    "AWS::Logs::SubscriptionFilter": _map_logs_subscription_filter,
    "AWS::Neptune::DBCluster": _map_neptune_db_cluster,
    "AWS::OpenSearchService::Domain": _map_opensearch_domain,
    "AWS::RDS::DBCluster": _map_rds_db_cluster,
    "AWS::RDS::DBInstance": _map_rds_db_instance,
    "AWS::S3::Bucket": _map_s3_bucket,
    "AWS::S3::BucketPolicy": _map_s3_bucket_policy,
    "AWS::SecretsManager::RotationSchedule": _map_secretsmanager_rotation_schedule,
    "AWS::SecretsManager::Secret": _map_secretsmanager_secret,
    "AWS::SecurityHub::FindingAggregator": _map_securityhub_finding_aggregator,
    "AWS::SecurityHub::Hub": _map_securityhub_hub,
    "AWS::Shield::Protection": _map_shield_protection,
    "AWS::SNS::Topic": _map_sns_topic,
    "AWS::SQS::Queue": _map_sqs_queue,
    "AWS::WAF::WebACL": _map_waf_web_acl,
    "AWS::WAFv2::RuleGroup": _map_wafv2_rule_group,
    "AWS::WAFv2::WebACL": _map_wafv2_web_acl,
    "AWS::WAFv2::WebACLAssociation": _map_wafv2_web_acl_association,
}


def has_mapping(cfn_type: str) -> bool:
    """True iff a property mapping is registered for `cfn_type`."""
    return cfn_type in _MAPPINGS


def apply_mapping(cfn_type: str, props: dict[str, Any]) -> list[MappedResource]:
    """Apply the registered mapping for `cfn_type`. KeyError if unmapped."""
    try:
        fn = _MAPPINGS[cfn_type]
    except KeyError as e:
        raise KeyError(f"no property mapping registered for CFN type {cfn_type!r}") from e
    return fn(props)


def mapped_cfn_types() -> tuple[str, ...]:
    """All CFN types with a registered mapping (sorted, deterministic)."""
    return tuple(sorted(_MAPPINGS))
