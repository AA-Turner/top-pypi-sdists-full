r'''
# CDKTF prebuilt bindings for DataDog/datadog provider version 3.60.1

This repo builds and publishes the [Terraform datadog provider](https://registry.terraform.io/providers/DataDog/datadog/3.60.1/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-datadog](https://www.npmjs.com/package/@cdktf/provider-datadog).

`npm install @cdktf/provider-datadog`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-datadog](https://pypi.org/project/cdktf-cdktf-provider-datadog).

`pipenv install cdktf-cdktf-provider-datadog`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Datadog](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Datadog).

`dotnet add package HashiCorp.Cdktf.Providers.Datadog`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-datadog](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-datadog).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-datadog</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-datadog-go`](https://github.com/cdktf/cdktf-provider-datadog-go) package.

`go get github.com/cdktf/cdktf-provider-datadog-go/datadog/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-datadog-go/blob/main/datadog/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-datadog).

## Versioning

This project is explicitly not tracking the Terraform datadog provider version 1:1. In fact, it always tracks `latest` of `~> 3.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform datadog provider](https://registry.terraform.io/providers/DataDog/datadog/3.60.1)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://github.com/projen/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktf/cdktf-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTF Repository Manager](https://github.com/cdktf/cdktf-repository-manager/).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

__all__ = [
    "action_connection",
    "api_key",
    "apm_retention_filter",
    "apm_retention_filter_order",
    "app_builder_app",
    "application_key",
    "appsec_waf_custom_rule",
    "appsec_waf_exclusion_filter",
    "authn_mapping",
    "child_organization",
    "cloud_configuration_rule",
    "cloud_workload_security_agent_rule",
    "csm_threats_agent_rule",
    "dashboard",
    "dashboard_json",
    "dashboard_list",
    "data_datadog_action_connection",
    "data_datadog_api_key",
    "data_datadog_apm_retention_filters_order",
    "data_datadog_app_builder_app",
    "data_datadog_application_key",
    "data_datadog_cloud_workload_security_agent_rules",
    "data_datadog_csm_threats_agent_rules",
    "data_datadog_dashboard",
    "data_datadog_dashboard_list",
    "data_datadog_hosts",
    "data_datadog_integration_aws_available_logs_services",
    "data_datadog_integration_aws_available_namespaces",
    "data_datadog_integration_aws_logs_services",
    "data_datadog_integration_aws_namespace_rules",
    "data_datadog_ip_ranges",
    "data_datadog_logs_archives_order",
    "data_datadog_logs_indexes",
    "data_datadog_logs_indexes_order",
    "data_datadog_logs_pipelines",
    "data_datadog_logs_pipelines_order",
    "data_datadog_monitor",
    "data_datadog_monitor_config_policies",
    "data_datadog_monitors",
    "data_datadog_permissions",
    "data_datadog_powerpack",
    "data_datadog_role",
    "data_datadog_role_users",
    "data_datadog_roles",
    "data_datadog_rum_application",
    "data_datadog_rum_retention_filters",
    "data_datadog_security_monitoring_filters",
    "data_datadog_security_monitoring_rules",
    "data_datadog_security_monitoring_suppressions",
    "data_datadog_sensitive_data_scanner_group_order",
    "data_datadog_sensitive_data_scanner_standard_pattern",
    "data_datadog_service_account",
    "data_datadog_service_level_objective",
    "data_datadog_service_level_objectives",
    "data_datadog_software_catalog",
    "data_datadog_synthetics_global_variable",
    "data_datadog_synthetics_locations",
    "data_datadog_synthetics_test",
    "data_datadog_team",
    "data_datadog_team_memberships",
    "data_datadog_teams",
    "data_datadog_user",
    "data_datadog_users",
    "data_datadog_workflow_automation",
    "domain_allowlist",
    "downtime",
    "downtime_schedule",
    "integration_aws",
    "integration_aws_account",
    "integration_aws_event_bridge",
    "integration_aws_external_id",
    "integration_aws_lambda_arn",
    "integration_aws_log_collection",
    "integration_aws_tag_filter",
    "integration_azure",
    "integration_cloudflare_account",
    "integration_confluent_account",
    "integration_confluent_resource",
    "integration_fastly_account",
    "integration_fastly_service",
    "integration_gcp",
    "integration_gcp_sts",
    "integration_ms_teams_tenant_based_handle",
    "integration_ms_teams_workflows_webhook_handle",
    "integration_opsgenie_service_object",
    "integration_pagerduty",
    "integration_pagerduty_service_object",
    "integration_slack_channel",
    "ip_allowlist",
    "logs_archive",
    "logs_archive_order",
    "logs_custom_destination",
    "logs_custom_pipeline",
    "logs_index",
    "logs_index_order",
    "logs_integration_pipeline",
    "logs_metric",
    "logs_pipeline_order",
    "metric_metadata",
    "metric_tag_configuration",
    "monitor",
    "monitor_config_policy",
    "monitor_json",
    "observability_pipeline",
    "openapi_api",
    "organization_settings",
    "powerpack",
    "provider",
    "restriction_policy",
    "role",
    "rum_application",
    "rum_metric",
    "rum_retention_filter",
    "rum_retention_filters_order",
    "security_monitoring_default_rule",
    "security_monitoring_filter",
    "security_monitoring_rule",
    "security_monitoring_suppression",
    "security_notification_rule",
    "sensitive_data_scanner_group",
    "sensitive_data_scanner_group_order",
    "sensitive_data_scanner_rule",
    "service_account",
    "service_account_application_key",
    "service_definition_yaml",
    "service_level_objective",
    "slo_correction",
    "software_catalog",
    "spans_metric",
    "synthetics_concurrency_cap",
    "synthetics_global_variable",
    "synthetics_private_location",
    "synthetics_test",
    "team",
    "team_link",
    "team_membership",
    "team_permission_setting",
    "user",
    "user_role",
    "webhook",
    "webhook_custom_variable",
    "workflow_automation",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import action_connection
from . import api_key
from . import apm_retention_filter
from . import apm_retention_filter_order
from . import app_builder_app
from . import application_key
from . import appsec_waf_custom_rule
from . import appsec_waf_exclusion_filter
from . import authn_mapping
from . import child_organization
from . import cloud_configuration_rule
from . import cloud_workload_security_agent_rule
from . import csm_threats_agent_rule
from . import dashboard
from . import dashboard_json
from . import dashboard_list
from . import data_datadog_action_connection
from . import data_datadog_api_key
from . import data_datadog_apm_retention_filters_order
from . import data_datadog_app_builder_app
from . import data_datadog_application_key
from . import data_datadog_cloud_workload_security_agent_rules
from . import data_datadog_csm_threats_agent_rules
from . import data_datadog_dashboard
from . import data_datadog_dashboard_list
from . import data_datadog_hosts
from . import data_datadog_integration_aws_available_logs_services
from . import data_datadog_integration_aws_available_namespaces
from . import data_datadog_integration_aws_logs_services
from . import data_datadog_integration_aws_namespace_rules
from . import data_datadog_ip_ranges
from . import data_datadog_logs_archives_order
from . import data_datadog_logs_indexes
from . import data_datadog_logs_indexes_order
from . import data_datadog_logs_pipelines
from . import data_datadog_logs_pipelines_order
from . import data_datadog_monitor
from . import data_datadog_monitor_config_policies
from . import data_datadog_monitors
from . import data_datadog_permissions
from . import data_datadog_powerpack
from . import data_datadog_role
from . import data_datadog_role_users
from . import data_datadog_roles
from . import data_datadog_rum_application
from . import data_datadog_rum_retention_filters
from . import data_datadog_security_monitoring_filters
from . import data_datadog_security_monitoring_rules
from . import data_datadog_security_monitoring_suppressions
from . import data_datadog_sensitive_data_scanner_group_order
from . import data_datadog_sensitive_data_scanner_standard_pattern
from . import data_datadog_service_account
from . import data_datadog_service_level_objective
from . import data_datadog_service_level_objectives
from . import data_datadog_software_catalog
from . import data_datadog_synthetics_global_variable
from . import data_datadog_synthetics_locations
from . import data_datadog_synthetics_test
from . import data_datadog_team
from . import data_datadog_team_memberships
from . import data_datadog_teams
from . import data_datadog_user
from . import data_datadog_users
from . import data_datadog_workflow_automation
from . import domain_allowlist
from . import downtime
from . import downtime_schedule
from . import integration_aws
from . import integration_aws_account
from . import integration_aws_event_bridge
from . import integration_aws_external_id
from . import integration_aws_lambda_arn
from . import integration_aws_log_collection
from . import integration_aws_tag_filter
from . import integration_azure
from . import integration_cloudflare_account
from . import integration_confluent_account
from . import integration_confluent_resource
from . import integration_fastly_account
from . import integration_fastly_service
from . import integration_gcp
from . import integration_gcp_sts
from . import integration_ms_teams_tenant_based_handle
from . import integration_ms_teams_workflows_webhook_handle
from . import integration_opsgenie_service_object
from . import integration_pagerduty
from . import integration_pagerduty_service_object
from . import integration_slack_channel
from . import ip_allowlist
from . import logs_archive
from . import logs_archive_order
from . import logs_custom_destination
from . import logs_custom_pipeline
from . import logs_index
from . import logs_index_order
from . import logs_integration_pipeline
from . import logs_metric
from . import logs_pipeline_order
from . import metric_metadata
from . import metric_tag_configuration
from . import monitor
from . import monitor_config_policy
from . import monitor_json
from . import observability_pipeline
from . import openapi_api
from . import organization_settings
from . import powerpack
from . import provider
from . import restriction_policy
from . import role
from . import rum_application
from . import rum_metric
from . import rum_retention_filter
from . import rum_retention_filters_order
from . import security_monitoring_default_rule
from . import security_monitoring_filter
from . import security_monitoring_rule
from . import security_monitoring_suppression
from . import security_notification_rule
from . import sensitive_data_scanner_group
from . import sensitive_data_scanner_group_order
from . import sensitive_data_scanner_rule
from . import service_account
from . import service_account_application_key
from . import service_definition_yaml
from . import service_level_objective
from . import slo_correction
from . import software_catalog
from . import spans_metric
from . import synthetics_concurrency_cap
from . import synthetics_global_variable
from . import synthetics_private_location
from . import synthetics_test
from . import team
from . import team_link
from . import team_membership
from . import team_permission_setting
from . import user
from . import user_role
from . import webhook
from . import webhook_custom_variable
from . import workflow_automation
