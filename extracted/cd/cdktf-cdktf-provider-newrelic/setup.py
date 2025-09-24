import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-newrelic",
    "version": "13.6.2",
    "description": "Prebuilt newrelic Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-newrelic.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-newrelic.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_newrelic",
        "cdktf_cdktf_provider_newrelic._jsii",
        "cdktf_cdktf_provider_newrelic.account_management",
        "cdktf_cdktf_provider_newrelic.alert_channel",
        "cdktf_cdktf_provider_newrelic.alert_condition",
        "cdktf_cdktf_provider_newrelic.alert_muting_rule",
        "cdktf_cdktf_provider_newrelic.alert_policy",
        "cdktf_cdktf_provider_newrelic.alert_policy_channel",
        "cdktf_cdktf_provider_newrelic.api_access_key",
        "cdktf_cdktf_provider_newrelic.application_settings",
        "cdktf_cdktf_provider_newrelic.browser_application",
        "cdktf_cdktf_provider_newrelic.cloud_aws_govcloud_integrations",
        "cdktf_cdktf_provider_newrelic.cloud_aws_govcloud_link_account",
        "cdktf_cdktf_provider_newrelic.cloud_aws_integrations",
        "cdktf_cdktf_provider_newrelic.cloud_aws_link_account",
        "cdktf_cdktf_provider_newrelic.cloud_azure_integrations",
        "cdktf_cdktf_provider_newrelic.cloud_azure_link_account",
        "cdktf_cdktf_provider_newrelic.cloud_gcp_integrations",
        "cdktf_cdktf_provider_newrelic.cloud_gcp_link_account",
        "cdktf_cdktf_provider_newrelic.data_newrelic_account",
        "cdktf_cdktf_provider_newrelic.data_newrelic_alert_channel",
        "cdktf_cdktf_provider_newrelic.data_newrelic_alert_policy",
        "cdktf_cdktf_provider_newrelic.data_newrelic_application",
        "cdktf_cdktf_provider_newrelic.data_newrelic_authentication_domain",
        "cdktf_cdktf_provider_newrelic.data_newrelic_cloud_account",
        "cdktf_cdktf_provider_newrelic.data_newrelic_entity",
        "cdktf_cdktf_provider_newrelic.data_newrelic_group",
        "cdktf_cdktf_provider_newrelic.data_newrelic_key_transaction",
        "cdktf_cdktf_provider_newrelic.data_newrelic_notification_destination",
        "cdktf_cdktf_provider_newrelic.data_newrelic_obfuscation_expression",
        "cdktf_cdktf_provider_newrelic.data_newrelic_service_level_alert_helper",
        "cdktf_cdktf_provider_newrelic.data_newrelic_synthetics_private_location",
        "cdktf_cdktf_provider_newrelic.data_newrelic_synthetics_secure_credential",
        "cdktf_cdktf_provider_newrelic.data_newrelic_test_grok_pattern",
        "cdktf_cdktf_provider_newrelic.data_newrelic_user",
        "cdktf_cdktf_provider_newrelic.data_partition_rule",
        "cdktf_cdktf_provider_newrelic.entity_tags",
        "cdktf_cdktf_provider_newrelic.events_to_metrics_rule",
        "cdktf_cdktf_provider_newrelic.group",
        "cdktf_cdktf_provider_newrelic.infra_alert_condition",
        "cdktf_cdktf_provider_newrelic.insights_event",
        "cdktf_cdktf_provider_newrelic.key_transaction",
        "cdktf_cdktf_provider_newrelic.log_parsing_rule",
        "cdktf_cdktf_provider_newrelic.monitor_downtime",
        "cdktf_cdktf_provider_newrelic.notification_channel",
        "cdktf_cdktf_provider_newrelic.notification_destination",
        "cdktf_cdktf_provider_newrelic.nrql_alert_condition",
        "cdktf_cdktf_provider_newrelic.nrql_drop_rule",
        "cdktf_cdktf_provider_newrelic.obfuscation_expression",
        "cdktf_cdktf_provider_newrelic.obfuscation_rule",
        "cdktf_cdktf_provider_newrelic.one_dashboard",
        "cdktf_cdktf_provider_newrelic.one_dashboard_json",
        "cdktf_cdktf_provider_newrelic.one_dashboard_raw",
        "cdktf_cdktf_provider_newrelic.pipeline_cloud_rule",
        "cdktf_cdktf_provider_newrelic.provider",
        "cdktf_cdktf_provider_newrelic.service_level",
        "cdktf_cdktf_provider_newrelic.synthetics_alert_condition",
        "cdktf_cdktf_provider_newrelic.synthetics_broken_links_monitor",
        "cdktf_cdktf_provider_newrelic.synthetics_cert_check_monitor",
        "cdktf_cdktf_provider_newrelic.synthetics_monitor",
        "cdktf_cdktf_provider_newrelic.synthetics_multilocation_alert_condition",
        "cdktf_cdktf_provider_newrelic.synthetics_private_location",
        "cdktf_cdktf_provider_newrelic.synthetics_script_monitor",
        "cdktf_cdktf_provider_newrelic.synthetics_secure_credential",
        "cdktf_cdktf_provider_newrelic.synthetics_step_monitor",
        "cdktf_cdktf_provider_newrelic.user",
        "cdktf_cdktf_provider_newrelic.workflow",
        "cdktf_cdktf_provider_newrelic.workload"
    ],
    "package_data": {
        "cdktf_cdktf_provider_newrelic._jsii": [
            "provider-newrelic@13.6.2.jsii.tgz"
        ],
        "cdktf_cdktf_provider_newrelic": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdktf>=0.21.0, <0.22.0",
        "constructs>=10.4.2, <11.0.0",
        "jsii>=1.114.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
