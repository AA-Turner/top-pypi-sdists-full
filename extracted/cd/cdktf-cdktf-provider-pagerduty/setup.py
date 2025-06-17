import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-pagerduty",
    "version": "14.0.2",
    "description": "Prebuilt pagerduty Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-pagerduty.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-pagerduty.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_pagerduty",
        "cdktf_cdktf_provider_pagerduty._jsii",
        "cdktf_cdktf_provider_pagerduty.addon",
        "cdktf_cdktf_provider_pagerduty.alert_grouping_setting",
        "cdktf_cdktf_provider_pagerduty.automation_actions_action",
        "cdktf_cdktf_provider_pagerduty.automation_actions_action_service_association",
        "cdktf_cdktf_provider_pagerduty.automation_actions_action_team_association",
        "cdktf_cdktf_provider_pagerduty.automation_actions_runner",
        "cdktf_cdktf_provider_pagerduty.automation_actions_runner_team_association",
        "cdktf_cdktf_provider_pagerduty.business_service",
        "cdktf_cdktf_provider_pagerduty.business_service_subscriber",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_alert_grouping_setting",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_automation_actions_action",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_automation_actions_runner",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_business_service",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_escalation_policy",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_event_orchestration",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_event_orchestration_global_cache_variable",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_event_orchestration_integration",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_event_orchestration_service_cache_variable",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_event_orchestrations",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_extension_schema",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_incident_custom_field",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_incident_type",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_incident_type_custom_field",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_incident_workflow",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_jira_cloud_account_mapping",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_license",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_licenses",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_priority",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_ruleset",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_schedule",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_service",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_service_custom_field",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_service_custom_field_value",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_service_integration",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_standards",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_standards_resource_scores",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_standards_resources_scores",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_tag",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_team",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_team_members",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_teams",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_user",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_user_contact_method",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_users",
        "cdktf_cdktf_provider_pagerduty.data_pagerduty_vendor",
        "cdktf_cdktf_provider_pagerduty.escalation_policy",
        "cdktf_cdktf_provider_pagerduty.event_orchestration",
        "cdktf_cdktf_provider_pagerduty.event_orchestration_global",
        "cdktf_cdktf_provider_pagerduty.event_orchestration_global_cache_variable",
        "cdktf_cdktf_provider_pagerduty.event_orchestration_integration",
        "cdktf_cdktf_provider_pagerduty.event_orchestration_router",
        "cdktf_cdktf_provider_pagerduty.event_orchestration_service",
        "cdktf_cdktf_provider_pagerduty.event_orchestration_service_cache_variable",
        "cdktf_cdktf_provider_pagerduty.event_orchestration_unrouted",
        "cdktf_cdktf_provider_pagerduty.event_rule",
        "cdktf_cdktf_provider_pagerduty.extension",
        "cdktf_cdktf_provider_pagerduty.extension_servicenow",
        "cdktf_cdktf_provider_pagerduty.incident_custom_field",
        "cdktf_cdktf_provider_pagerduty.incident_custom_field_option",
        "cdktf_cdktf_provider_pagerduty.incident_type",
        "cdktf_cdktf_provider_pagerduty.incident_type_custom_field",
        "cdktf_cdktf_provider_pagerduty.incident_workflow",
        "cdktf_cdktf_provider_pagerduty.incident_workflow_trigger",
        "cdktf_cdktf_provider_pagerduty.jira_cloud_account_mapping_rule",
        "cdktf_cdktf_provider_pagerduty.maintenance_window",
        "cdktf_cdktf_provider_pagerduty.provider",
        "cdktf_cdktf_provider_pagerduty.response_play",
        "cdktf_cdktf_provider_pagerduty.ruleset",
        "cdktf_cdktf_provider_pagerduty.ruleset_rule",
        "cdktf_cdktf_provider_pagerduty.schedule",
        "cdktf_cdktf_provider_pagerduty.service",
        "cdktf_cdktf_provider_pagerduty.service_custom_field",
        "cdktf_cdktf_provider_pagerduty.service_custom_field_value",
        "cdktf_cdktf_provider_pagerduty.service_dependency",
        "cdktf_cdktf_provider_pagerduty.service_event_rule",
        "cdktf_cdktf_provider_pagerduty.service_integration",
        "cdktf_cdktf_provider_pagerduty.slack_connection",
        "cdktf_cdktf_provider_pagerduty.tag",
        "cdktf_cdktf_provider_pagerduty.tag_assignment",
        "cdktf_cdktf_provider_pagerduty.team",
        "cdktf_cdktf_provider_pagerduty.team_membership",
        "cdktf_cdktf_provider_pagerduty.user",
        "cdktf_cdktf_provider_pagerduty.user_contact_method",
        "cdktf_cdktf_provider_pagerduty.user_handoff_notification_rule",
        "cdktf_cdktf_provider_pagerduty.user_notification_rule",
        "cdktf_cdktf_provider_pagerduty.webhook_subscription"
    ],
    "package_data": {
        "cdktf_cdktf_provider_pagerduty._jsii": [
            "provider-pagerduty@14.0.2.jsii.tgz"
        ],
        "cdktf_cdktf_provider_pagerduty": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdktf>=0.21.0, <0.22.0",
        "constructs>=10.4.2, <11.0.0",
        "jsii>=1.112.0, <2.0.0",
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
