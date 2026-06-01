"""Detector library.

Importing this package registers every detector in the library with the
global registry via the `@detector` decorator. The `scan_terraform`
primitive imports this module explicitly so the registry is populated
before it enumerates detectors at scan time.

Each detector is a self-contained folder at
`src/efterlev/detectors/<cloud>/<capability>/` with five files per the
contract in `CONTRIBUTING.md`. Adding a new detector means creating that
folder and adding one import line below.
"""

from __future__ import annotations

# Detector registrations. Each import triggers the @detector decorator
# that registers the detector with the module-level _REGISTRY.
from efterlev.detectors.aws import (
    access_analyzer_enabled,  # noqa: F401
    api_gateway_access_logging,  # noqa: F401
    api_gateway_auth_required,  # noqa: F401
    api_gateway_tls_min_version,  # noqa: F401
    api_gateway_waf_attached,  # noqa: F401
    backup_restore_testing,  # noqa: F401
    backup_retention_configured,  # noqa: F401
    centralized_log_aggregation,  # noqa: F401
    cloudfront_viewer_protocol_https,  # noqa: F401
    cloudtrail_audit_logging,  # noqa: F401
    cloudtrail_log_file_validation,  # noqa: F401
    cloudwatch_alarms_critical,  # noqa: F401
    cna_dos_protection,  # noqa: F401
    cna_optimizing_for_availability,  # noqa: F401
    config_enabled,  # noqa: F401
    ec2_imdsv2_required,  # noqa: F401
    elb_access_logs,  # noqa: F401
    encryption_ebs,  # noqa: F401
    encryption_s3_at_rest,  # noqa: F401
    federated_identity_providers,  # noqa: F401
    fips_ssl_policies_on_lb_listeners,  # noqa: F401
    guardduty_enabled,  # noqa: F401
    iam_admin_policy_usage,  # noqa: F401
    iam_inline_policies_audit,  # noqa: F401
    iam_managed_via_terraform,  # noqa: F401
    iam_password_policy,  # noqa: F401
    iam_service_account_keys_age,  # noqa: F401
    iam_user_access_keys,  # noqa: F401
    kms_customer_managed_keys,  # noqa: F401
    kms_key_rotation,  # noqa: F401
    lambda_env_kms_encryption,  # noqa: F401
    lambda_logging_configured,  # noqa: F401
    lambda_vpc_isolation,  # noqa: F401
    mfa_required_on_iam_policies,  # noqa: F401
    mla_log_access_least_privilege,  # noqa: F401
    nacl_open_egress,  # noqa: F401
    nacl_restrictiveness,  # noqa: F401
    rds_encryption_at_rest,  # noqa: F401
    rds_public_accessibility,  # noqa: F401
    rpl_backup_configured,  # noqa: F401
    s3_bucket_public_acl,  # noqa: F401
    s3_lifecycle_policies,  # noqa: F401
    s3_public_access_block,  # noqa: F401
    secrets_manager_rotation,  # noqa: F401
    security_group_open_ingress,  # noqa: F401
    sns_topic_encryption,  # noqa: F401
    sqs_queue_encryption,  # noqa: F401
    suspicious_activity_response,  # noqa: F401
    svc_at_rest_encryption_coverage,  # noqa: F401
    terraform_inventory,  # noqa: F401
    tls_on_lb_listeners,  # noqa: F401
    vpc_flow_logs_enabled,  # noqa: F401
    vpc_logical_segmentation,  # noqa: F401
    waf_action_types,  # noqa: F401
    waf_custom_rule_groups,  # noqa: F401
    waf_geo_blocking,  # noqa: F401
    waf_ip_set_blocking,  # noqa: F401
    waf_managed_rule_groups,  # noqa: F401
    waf_rate_limiting,  # noqa: F401
    waf_rule_count,  # noqa: F401
)

# GitHub-source detectors (Priority 1.2, 2026-04-27): repo-metadata
# detectors that read `.github/workflows/*.yml` rather than IaC.
from efterlev.detectors.github import (
    action_pinning,  # noqa: F401
    branch_protection,  # noqa: F401
    ci_validation_gates,  # noqa: F401
    immutable_deploy_patterns,  # noqa: F401
    piy_sdlc_security_gates,  # noqa: F401
    supply_chain_monitoring,  # noqa: F401
)
