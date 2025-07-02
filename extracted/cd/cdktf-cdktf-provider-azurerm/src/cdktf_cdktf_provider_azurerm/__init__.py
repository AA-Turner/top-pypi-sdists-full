r'''
# CDKTF prebuilt bindings for hashicorp/azurerm provider version 4.35.0

This repo builds and publishes the [Terraform azurerm provider](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-azurerm](https://www.npmjs.com/package/@cdktf/provider-azurerm).

`npm install @cdktf/provider-azurerm`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-azurerm](https://pypi.org/project/cdktf-cdktf-provider-azurerm).

`pipenv install cdktf-cdktf-provider-azurerm`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Azurerm](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Azurerm).

`dotnet add package HashiCorp.Cdktf.Providers.Azurerm`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-azurerm](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-azurerm).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-azurerm</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-azurerm-go`](https://github.com/cdktf/cdktf-provider-azurerm-go) package.

`go get github.com/cdktf/cdktf-provider-azurerm-go/azurerm/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-azurerm-go/blob/main/azurerm/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-azurerm).

## Versioning

This project is explicitly not tracking the Terraform azurerm provider version 1:1. In fact, it always tracks `latest` of `~> 4.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform azurerm provider](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0)
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
    "aadb2_c_directory",
    "active_directory_domain_service",
    "active_directory_domain_service_replica_set",
    "active_directory_domain_service_trust",
    "advanced_threat_protection",
    "advisor_suppression",
    "ai_foundry",
    "ai_foundry_project",
    "ai_services",
    "analysis_services_server",
    "api_connection",
    "api_management",
    "api_management_api",
    "api_management_api_diagnostic",
    "api_management_api_operation",
    "api_management_api_operation_policy",
    "api_management_api_operation_tag",
    "api_management_api_policy",
    "api_management_api_release",
    "api_management_api_schema",
    "api_management_api_tag",
    "api_management_api_tag_description",
    "api_management_api_version_set",
    "api_management_authorization_server",
    "api_management_backend",
    "api_management_certificate",
    "api_management_custom_domain",
    "api_management_diagnostic",
    "api_management_email_template",
    "api_management_gateway",
    "api_management_gateway_api",
    "api_management_gateway_certificate_authority",
    "api_management_gateway_host_name_configuration",
    "api_management_global_schema",
    "api_management_group",
    "api_management_group_user",
    "api_management_identity_provider_aad",
    "api_management_identity_provider_aadb2_c",
    "api_management_identity_provider_facebook",
    "api_management_identity_provider_google",
    "api_management_identity_provider_microsoft",
    "api_management_identity_provider_twitter",
    "api_management_logger",
    "api_management_named_value",
    "api_management_notification_recipient_email",
    "api_management_notification_recipient_user",
    "api_management_openid_connect_provider",
    "api_management_policy",
    "api_management_policy_fragment",
    "api_management_product",
    "api_management_product_api",
    "api_management_product_group",
    "api_management_product_policy",
    "api_management_product_tag",
    "api_management_redis_cache",
    "api_management_subscription",
    "api_management_tag",
    "api_management_user",
    "app_configuration",
    "app_configuration_feature",
    "app_configuration_key",
    "app_service",
    "app_service_active_slot",
    "app_service_certificate",
    "app_service_certificate_binding",
    "app_service_certificate_order",
    "app_service_connection",
    "app_service_custom_hostname_binding",
    "app_service_environment_v3",
    "app_service_hybrid_connection",
    "app_service_managed_certificate",
    "app_service_plan",
    "app_service_public_certificate",
    "app_service_slot",
    "app_service_slot_custom_hostname_binding",
    "app_service_slot_virtual_network_swift_connection",
    "app_service_source_control",
    "app_service_source_control_slot",
    "app_service_source_control_token",
    "app_service_virtual_network_swift_connection",
    "application_gateway",
    "application_insights",
    "application_insights_analytics_item",
    "application_insights_api_key",
    "application_insights_smart_detection_rule",
    "application_insights_standard_web_test",
    "application_insights_web_test",
    "application_insights_workbook",
    "application_insights_workbook_template",
    "application_load_balancer",
    "application_load_balancer_frontend",
    "application_load_balancer_subnet_association",
    "application_security_group",
    "arc_kubernetes_cluster",
    "arc_kubernetes_cluster_extension",
    "arc_kubernetes_flux_configuration",
    "arc_kubernetes_provisioned_cluster",
    "arc_machine",
    "arc_machine_automanage_configuration_assignment",
    "arc_machine_extension",
    "arc_private_link_scope",
    "arc_resource_bridge_appliance",
    "attestation_provider",
    "automanage_configuration",
    "automation_account",
    "automation_certificate",
    "automation_connection",
    "automation_connection_certificate",
    "automation_connection_classic_certificate",
    "automation_connection_service_principal",
    "automation_connection_type",
    "automation_credential",
    "automation_dsc_configuration",
    "automation_dsc_nodeconfiguration",
    "automation_hybrid_runbook_worker",
    "automation_hybrid_runbook_worker_group",
    "automation_job_schedule",
    "automation_module",
    "automation_powershell72_module",
    "automation_python3_package",
    "automation_runbook",
    "automation_schedule",
    "automation_software_update_configuration",
    "automation_source_control",
    "automation_variable_bool",
    "automation_variable_datetime",
    "automation_variable_int",
    "automation_variable_object",
    "automation_variable_string",
    "automation_watcher",
    "automation_webhook",
    "availability_set",
    "backup_container_storage_account",
    "backup_policy_file_share",
    "backup_policy_vm",
    "backup_policy_vm_workload",
    "backup_protected_file_share",
    "backup_protected_vm",
    "bastion_host",
    "batch_account",
    "batch_application",
    "batch_certificate",
    "batch_job",
    "batch_pool",
    "billing_account_cost_management_export",
    "blueprint_assignment",
    "bot_channel_alexa",
    "bot_channel_direct_line_speech",
    "bot_channel_directline",
    "bot_channel_email",
    "bot_channel_facebook",
    "bot_channel_line",
    "bot_channel_ms_teams",
    "bot_channel_slack",
    "bot_channel_sms",
    "bot_channel_web_chat",
    "bot_channels_registration",
    "bot_connection",
    "bot_service_azure_bot",
    "bot_web_app",
    "capacity_reservation",
    "capacity_reservation_group",
    "cdn_endpoint",
    "cdn_endpoint_custom_domain",
    "cdn_frontdoor_custom_domain",
    "cdn_frontdoor_custom_domain_association",
    "cdn_frontdoor_endpoint",
    "cdn_frontdoor_firewall_policy",
    "cdn_frontdoor_origin",
    "cdn_frontdoor_origin_group",
    "cdn_frontdoor_profile",
    "cdn_frontdoor_route",
    "cdn_frontdoor_rule",
    "cdn_frontdoor_rule_set",
    "cdn_frontdoor_secret",
    "cdn_frontdoor_security_policy",
    "cdn_profile",
    "chaos_studio_capability",
    "chaos_studio_experiment",
    "chaos_studio_target",
    "cognitive_account",
    "cognitive_account_customer_managed_key",
    "cognitive_account_rai_blocklist",
    "cognitive_account_rai_policy",
    "cognitive_deployment",
    "communication_service",
    "communication_service_email_domain_association",
    "confidential_ledger",
    "consumption_budget_management_group",
    "consumption_budget_resource_group",
    "consumption_budget_subscription",
    "container_app",
    "container_app_custom_domain",
    "container_app_environment",
    "container_app_environment_certificate",
    "container_app_environment_custom_domain",
    "container_app_environment_dapr_component",
    "container_app_environment_storage",
    "container_app_job",
    "container_connected_registry",
    "container_group",
    "container_registry",
    "container_registry_agent_pool",
    "container_registry_cache_rule",
    "container_registry_credential_set",
    "container_registry_scope_map",
    "container_registry_task",
    "container_registry_task_schedule_run_now",
    "container_registry_token",
    "container_registry_token_password",
    "container_registry_webhook",
    "cosmosdb_account",
    "cosmosdb_cassandra_cluster",
    "cosmosdb_cassandra_datacenter",
    "cosmosdb_cassandra_keyspace",
    "cosmosdb_cassandra_table",
    "cosmosdb_gremlin_database",
    "cosmosdb_gremlin_graph",
    "cosmosdb_mongo_collection",
    "cosmosdb_mongo_database",
    "cosmosdb_mongo_role_definition",
    "cosmosdb_mongo_user_definition",
    "cosmosdb_postgresql_cluster",
    "cosmosdb_postgresql_coordinator_configuration",
    "cosmosdb_postgresql_firewall_rule",
    "cosmosdb_postgresql_node_configuration",
    "cosmosdb_postgresql_role",
    "cosmosdb_sql_container",
    "cosmosdb_sql_database",
    "cosmosdb_sql_dedicated_gateway",
    "cosmosdb_sql_function",
    "cosmosdb_sql_role_assignment",
    "cosmosdb_sql_role_definition",
    "cosmosdb_sql_stored_procedure",
    "cosmosdb_sql_trigger",
    "cosmosdb_table",
    "cost_anomaly_alert",
    "cost_management_scheduled_action",
    "custom_ip_prefix",
    "custom_provider",
    "dashboard_grafana",
    "dashboard_grafana_managed_private_endpoint",
    "data_azurerm_aadb2_c_directory",
    "data_azurerm_active_directory_domain_service",
    "data_azurerm_advisor_recommendations",
    "data_azurerm_api_management",
    "data_azurerm_api_management_api",
    "data_azurerm_api_management_api_version_set",
    "data_azurerm_api_management_gateway",
    "data_azurerm_api_management_gateway_host_name_configuration",
    "data_azurerm_api_management_group",
    "data_azurerm_api_management_product",
    "data_azurerm_api_management_subscription",
    "data_azurerm_api_management_user",
    "data_azurerm_app_configuration",
    "data_azurerm_app_configuration_key",
    "data_azurerm_app_configuration_keys",
    "data_azurerm_app_service",
    "data_azurerm_app_service_certificate",
    "data_azurerm_app_service_certificate_order",
    "data_azurerm_app_service_environment_v3",
    "data_azurerm_app_service_plan",
    "data_azurerm_application_gateway",
    "data_azurerm_application_insights",
    "data_azurerm_application_security_group",
    "data_azurerm_arc_machine",
    "data_azurerm_arc_resource_bridge_appliance",
    "data_azurerm_attestation_provider",
    "data_azurerm_automation_account",
    "data_azurerm_automation_runbook",
    "data_azurerm_automation_variable_bool",
    "data_azurerm_automation_variable_datetime",
    "data_azurerm_automation_variable_int",
    "data_azurerm_automation_variable_object",
    "data_azurerm_automation_variable_string",
    "data_azurerm_automation_variables",
    "data_azurerm_availability_set",
    "data_azurerm_backup_policy_file_share",
    "data_azurerm_backup_policy_vm",
    "data_azurerm_bastion_host",
    "data_azurerm_batch_account",
    "data_azurerm_batch_application",
    "data_azurerm_batch_certificate",
    "data_azurerm_batch_pool",
    "data_azurerm_billing_enrollment_account_scope",
    "data_azurerm_billing_mca_account_scope",
    "data_azurerm_billing_mpa_account_scope",
    "data_azurerm_blueprint_definition",
    "data_azurerm_blueprint_published_version",
    "data_azurerm_cdn_frontdoor_custom_domain",
    "data_azurerm_cdn_frontdoor_endpoint",
    "data_azurerm_cdn_frontdoor_firewall_policy",
    "data_azurerm_cdn_frontdoor_origin_group",
    "data_azurerm_cdn_frontdoor_profile",
    "data_azurerm_cdn_frontdoor_rule_set",
    "data_azurerm_cdn_frontdoor_secret",
    "data_azurerm_cdn_profile",
    "data_azurerm_client_config",
    "data_azurerm_cognitive_account",
    "data_azurerm_communication_service",
    "data_azurerm_confidential_ledger",
    "data_azurerm_consumption_budget_resource_group",
    "data_azurerm_consumption_budget_subscription",
    "data_azurerm_container_app",
    "data_azurerm_container_app_environment",
    "data_azurerm_container_app_environment_certificate",
    "data_azurerm_container_group",
    "data_azurerm_container_registry",
    "data_azurerm_container_registry_cache_rule",
    "data_azurerm_container_registry_scope_map",
    "data_azurerm_container_registry_token",
    "data_azurerm_cosmosdb_account",
    "data_azurerm_cosmosdb_mongo_database",
    "data_azurerm_cosmosdb_restorable_database_accounts",
    "data_azurerm_cosmosdb_sql_database",
    "data_azurerm_cosmosdb_sql_role_definition",
    "data_azurerm_dashboard_grafana",
    "data_azurerm_data_factory",
    "data_azurerm_data_factory_trigger_schedule",
    "data_azurerm_data_factory_trigger_schedules",
    "data_azurerm_data_protection_backup_vault",
    "data_azurerm_data_share",
    "data_azurerm_data_share_account",
    "data_azurerm_data_share_dataset_blob_storage",
    "data_azurerm_data_share_dataset_data_lake_gen2",
    "data_azurerm_data_share_dataset_kusto_cluster",
    "data_azurerm_data_share_dataset_kusto_database",
    "data_azurerm_database_migration_project",
    "data_azurerm_database_migration_service",
    "data_azurerm_databox_edge_device",
    "data_azurerm_databricks_access_connector",
    "data_azurerm_databricks_workspace",
    "data_azurerm_databricks_workspace_private_endpoint_connection",
    "data_azurerm_dedicated_host",
    "data_azurerm_dedicated_host_group",
    "data_azurerm_dev_center",
    "data_azurerm_dev_center_attached_network",
    "data_azurerm_dev_center_catalog",
    "data_azurerm_dev_center_dev_box_definition",
    "data_azurerm_dev_center_environment_type",
    "data_azurerm_dev_center_gallery",
    "data_azurerm_dev_center_network_connection",
    "data_azurerm_dev_center_project",
    "data_azurerm_dev_center_project_environment_type",
    "data_azurerm_dev_center_project_pool",
    "data_azurerm_dev_test_lab",
    "data_azurerm_dev_test_virtual_network",
    "data_azurerm_digital_twins_instance",
    "data_azurerm_disk_access",
    "data_azurerm_disk_encryption_set",
    "data_azurerm_dns_a_record",
    "data_azurerm_dns_aaaa_record",
    "data_azurerm_dns_caa_record",
    "data_azurerm_dns_cname_record",
    "data_azurerm_dns_mx_record",
    "data_azurerm_dns_ns_record",
    "data_azurerm_dns_ptr_record",
    "data_azurerm_dns_soa_record",
    "data_azurerm_dns_srv_record",
    "data_azurerm_dns_txt_record",
    "data_azurerm_dns_zone",
    "data_azurerm_dynatrace_monitor",
    "data_azurerm_elastic_cloud_elasticsearch",
    "data_azurerm_elastic_san",
    "data_azurerm_elastic_san_volume_group",
    "data_azurerm_elastic_san_volume_snapshot",
    "data_azurerm_eventgrid_domain",
    "data_azurerm_eventgrid_domain_topic",
    "data_azurerm_eventgrid_system_topic",
    "data_azurerm_eventgrid_topic",
    "data_azurerm_eventhub",
    "data_azurerm_eventhub_authorization_rule",
    "data_azurerm_eventhub_cluster",
    "data_azurerm_eventhub_consumer_group",
    "data_azurerm_eventhub_namespace",
    "data_azurerm_eventhub_namespace_authorization_rule",
    "data_azurerm_eventhub_sas",
    "data_azurerm_express_route_circuit",
    "data_azurerm_express_route_circuit_peering",
    "data_azurerm_extended_location_custom_location",
    "data_azurerm_extended_locations",
    "data_azurerm_firewall",
    "data_azurerm_firewall_policy",
    "data_azurerm_function_app",
    "data_azurerm_function_app_host_keys",
    "data_azurerm_hdinsight_cluster",
    "data_azurerm_healthcare_dicom_service",
    "data_azurerm_healthcare_fhir_service",
    "data_azurerm_healthcare_medtech_service",
    "data_azurerm_healthcare_service",
    "data_azurerm_healthcare_workspace",
    "data_azurerm_image",
    "data_azurerm_images",
    "data_azurerm_iothub",
    "data_azurerm_iothub_dps",
    "data_azurerm_iothub_dps_shared_access_policy",
    "data_azurerm_iothub_shared_access_policy",
    "data_azurerm_ip_group",
    "data_azurerm_ip_groups",
    "data_azurerm_key_vault",
    "data_azurerm_key_vault_access_policy",
    "data_azurerm_key_vault_certificate",
    "data_azurerm_key_vault_certificate_data",
    "data_azurerm_key_vault_certificate_issuer",
    "data_azurerm_key_vault_certificates",
    "data_azurerm_key_vault_encrypted_value",
    "data_azurerm_key_vault_key",
    "data_azurerm_key_vault_managed_hardware_security_module",
    "data_azurerm_key_vault_managed_hardware_security_module_key",
    "data_azurerm_key_vault_managed_hardware_security_module_role_definition",
    "data_azurerm_key_vault_secret",
    "data_azurerm_key_vault_secrets",
    "data_azurerm_kubernetes_cluster",
    "data_azurerm_kubernetes_cluster_node_pool",
    "data_azurerm_kubernetes_fleet_manager",
    "data_azurerm_kubernetes_node_pool_snapshot",
    "data_azurerm_kubernetes_service_versions",
    "data_azurerm_kusto_cluster",
    "data_azurerm_kusto_database",
    "data_azurerm_lb",
    "data_azurerm_lb_backend_address_pool",
    "data_azurerm_lb_outbound_rule",
    "data_azurerm_lb_rule",
    "data_azurerm_linux_function_app",
    "data_azurerm_linux_web_app",
    "data_azurerm_load_test",
    "data_azurerm_local_network_gateway",
    "data_azurerm_location",
    "data_azurerm_log_analytics_workspace",
    "data_azurerm_logic_app_integration_account",
    "data_azurerm_logic_app_standard",
    "data_azurerm_logic_app_workflow",
    "data_azurerm_machine_learning_workspace",
    "data_azurerm_maintenance_configuration",
    "data_azurerm_managed_api",
    "data_azurerm_managed_application_definition",
    "data_azurerm_managed_disk",
    "data_azurerm_management_group",
    "data_azurerm_management_group_template_deployment",
    "data_azurerm_maps_account",
    "data_azurerm_marketplace_agreement",
    "data_azurerm_mobile_network",
    "data_azurerm_mobile_network_attached_data_network",
    "data_azurerm_mobile_network_data_network",
    "data_azurerm_mobile_network_packet_core_control_plane",
    "data_azurerm_mobile_network_packet_core_data_plane",
    "data_azurerm_mobile_network_service",
    "data_azurerm_mobile_network_sim",
    "data_azurerm_mobile_network_sim_group",
    "data_azurerm_mobile_network_sim_policy",
    "data_azurerm_mobile_network_site",
    "data_azurerm_mobile_network_slice",
    "data_azurerm_monitor_action_group",
    "data_azurerm_monitor_data_collection_endpoint",
    "data_azurerm_monitor_data_collection_rule",
    "data_azurerm_monitor_diagnostic_categories",
    "data_azurerm_monitor_scheduled_query_rules_alert",
    "data_azurerm_monitor_scheduled_query_rules_log",
    "data_azurerm_monitor_workspace",
    "data_azurerm_mssql_database",
    "data_azurerm_mssql_elasticpool",
    "data_azurerm_mssql_managed_database",
    "data_azurerm_mssql_managed_instance",
    "data_azurerm_mssql_server",
    "data_azurerm_mysql_flexible_server",
    "data_azurerm_nat_gateway",
    "data_azurerm_netapp_account",
    "data_azurerm_netapp_account_encryption",
    "data_azurerm_netapp_backup_policy",
    "data_azurerm_netapp_backup_vault",
    "data_azurerm_netapp_pool",
    "data_azurerm_netapp_snapshot",
    "data_azurerm_netapp_snapshot_policy",
    "data_azurerm_netapp_volume",
    "data_azurerm_netapp_volume_group_oracle",
    "data_azurerm_netapp_volume_group_sap_hana",
    "data_azurerm_netapp_volume_quota_rule",
    "data_azurerm_network_ddos_protection_plan",
    "data_azurerm_network_interface",
    "data_azurerm_network_manager",
    "data_azurerm_network_manager_connectivity_configuration",
    "data_azurerm_network_manager_network_group",
    "data_azurerm_network_security_group",
    "data_azurerm_network_service_tags",
    "data_azurerm_network_watcher",
    "data_azurerm_nginx_api_key",
    "data_azurerm_nginx_certificate",
    "data_azurerm_nginx_configuration",
    "data_azurerm_nginx_deployment",
    "data_azurerm_notification_hub",
    "data_azurerm_notification_hub_namespace",
    "data_azurerm_oracle_adbs_character_sets",
    "data_azurerm_oracle_adbs_national_character_sets",
    "data_azurerm_oracle_autonomous_database",
    "data_azurerm_oracle_cloud_vm_cluster",
    "data_azurerm_oracle_db_nodes",
    "data_azurerm_oracle_db_servers",
    "data_azurerm_oracle_db_system_shapes",
    "data_azurerm_oracle_exadata_infrastructure",
    "data_azurerm_oracle_gi_versions",
    "data_azurerm_orchestrated_virtual_machine_scale_set",
    "data_azurerm_palo_alto_local_rulestack",
    "data_azurerm_platform_image",
    "data_azurerm_policy_assignment",
    "data_azurerm_policy_definition",
    "data_azurerm_policy_definition_built_in",
    "data_azurerm_policy_set_definition",
    "data_azurerm_policy_virtual_machine_configuration_assignment",
    "data_azurerm_portal_dashboard",
    "data_azurerm_postgresql_flexible_server",
    "data_azurerm_postgresql_server",
    "data_azurerm_private_dns_a_record",
    "data_azurerm_private_dns_aaaa_record",
    "data_azurerm_private_dns_cname_record",
    "data_azurerm_private_dns_mx_record",
    "data_azurerm_private_dns_ptr_record",
    "data_azurerm_private_dns_resolver",
    "data_azurerm_private_dns_resolver_dns_forwarding_ruleset",
    "data_azurerm_private_dns_resolver_forwarding_rule",
    "data_azurerm_private_dns_resolver_inbound_endpoint",
    "data_azurerm_private_dns_resolver_outbound_endpoint",
    "data_azurerm_private_dns_resolver_virtual_network_link",
    "data_azurerm_private_dns_soa_record",
    "data_azurerm_private_dns_srv_record",
    "data_azurerm_private_dns_txt_record",
    "data_azurerm_private_dns_zone",
    "data_azurerm_private_dns_zone_virtual_network_link",
    "data_azurerm_private_endpoint_connection",
    "data_azurerm_private_link_service",
    "data_azurerm_private_link_service_endpoint_connections",
    "data_azurerm_proximity_placement_group",
    "data_azurerm_public_ip",
    "data_azurerm_public_ip_prefix",
    "data_azurerm_public_ips",
    "data_azurerm_public_maintenance_configurations",
    "data_azurerm_recovery_services_vault",
    "data_azurerm_redis_cache",
    "data_azurerm_redis_enterprise_database",
    "data_azurerm_resource_group",
    "data_azurerm_resource_group_template_deployment",
    "data_azurerm_resources",
    "data_azurerm_role_assignments",
    "data_azurerm_role_definition",
    "data_azurerm_role_management_policy",
    "data_azurerm_route_filter",
    "data_azurerm_route_table",
    "data_azurerm_search_service",
    "data_azurerm_sentinel_alert_rule",
    "data_azurerm_sentinel_alert_rule_anomaly",
    "data_azurerm_sentinel_alert_rule_template",
    "data_azurerm_service_plan",
    "data_azurerm_servicebus_namespace",
    "data_azurerm_servicebus_namespace_authorization_rule",
    "data_azurerm_servicebus_namespace_disaster_recovery_config",
    "data_azurerm_servicebus_queue",
    "data_azurerm_servicebus_queue_authorization_rule",
    "data_azurerm_servicebus_subscription",
    "data_azurerm_servicebus_topic",
    "data_azurerm_servicebus_topic_authorization_rule",
    "data_azurerm_shared_image",
    "data_azurerm_shared_image_gallery",
    "data_azurerm_shared_image_version",
    "data_azurerm_shared_image_versions",
    "data_azurerm_signalr_service",
    "data_azurerm_site_recovery_fabric",
    "data_azurerm_site_recovery_protection_container",
    "data_azurerm_site_recovery_replication_policy",
    "data_azurerm_site_recovery_replication_recovery_plan",
    "data_azurerm_snapshot",
    "data_azurerm_source_control_token",
    "data_azurerm_spatial_anchors_account",
    "data_azurerm_spring_cloud_app",
    "data_azurerm_spring_cloud_service",
    "data_azurerm_ssh_public_key",
    "data_azurerm_stack_hci_cluster",
    "data_azurerm_stack_hci_storage_path",
    "data_azurerm_static_web_app",
    "data_azurerm_storage_account",
    "data_azurerm_storage_account_blob_container_sas",
    "data_azurerm_storage_account_sas",
    "data_azurerm_storage_blob",
    "data_azurerm_storage_container",
    "data_azurerm_storage_containers",
    "data_azurerm_storage_encryption_scope",
    "data_azurerm_storage_management_policy",
    "data_azurerm_storage_queue",
    "data_azurerm_storage_share",
    "data_azurerm_storage_sync",
    "data_azurerm_storage_sync_group",
    "data_azurerm_storage_table",
    "data_azurerm_storage_table_entities",
    "data_azurerm_storage_table_entity",
    "data_azurerm_stream_analytics_job",
    "data_azurerm_subnet",
    "data_azurerm_subscription",
    "data_azurerm_subscription_template_deployment",
    "data_azurerm_subscriptions",
    "data_azurerm_synapse_workspace",
    "data_azurerm_system_center_virtual_machine_manager_inventory_items",
    "data_azurerm_template_spec_version",
    "data_azurerm_tenant_template_deployment",
    "data_azurerm_traffic_manager_geographical_location",
    "data_azurerm_traffic_manager_profile",
    "data_azurerm_user_assigned_identity",
    "data_azurerm_virtual_desktop_application_group",
    "data_azurerm_virtual_desktop_host_pool",
    "data_azurerm_virtual_desktop_workspace",
    "data_azurerm_virtual_hub",
    "data_azurerm_virtual_hub_connection",
    "data_azurerm_virtual_hub_route_table",
    "data_azurerm_virtual_machine",
    "data_azurerm_virtual_machine_scale_set",
    "data_azurerm_virtual_network",
    "data_azurerm_virtual_network_gateway",
    "data_azurerm_virtual_network_gateway_connection",
    "data_azurerm_virtual_network_peering",
    "data_azurerm_virtual_wan",
    "data_azurerm_vmware_private_cloud",
    "data_azurerm_vpn_gateway",
    "data_azurerm_vpn_server_configuration",
    "data_azurerm_web_application_firewall_policy",
    "data_azurerm_web_pubsub",
    "data_azurerm_web_pubsub_private_link_resource",
    "data_azurerm_windows_function_app",
    "data_azurerm_windows_web_app",
    "data_factory",
    "data_factory_credential_service_principal",
    "data_factory_credential_user_managed_identity",
    "data_factory_custom_dataset",
    "data_factory_data_flow",
    "data_factory_dataset_azure_blob",
    "data_factory_dataset_azure_sql_table",
    "data_factory_dataset_binary",
    "data_factory_dataset_cosmosdb_sqlapi",
    "data_factory_dataset_delimited_text",
    "data_factory_dataset_http",
    "data_factory_dataset_json",
    "data_factory_dataset_mysql",
    "data_factory_dataset_parquet",
    "data_factory_dataset_postgresql",
    "data_factory_dataset_snowflake",
    "data_factory_dataset_sql_server_table",
    "data_factory_flowlet_data_flow",
    "data_factory_integration_runtime_azure",
    "data_factory_integration_runtime_azure_ssis",
    "data_factory_integration_runtime_self_hosted",
    "data_factory_linked_custom_service",
    "data_factory_linked_service_azure_blob_storage",
    "data_factory_linked_service_azure_databricks",
    "data_factory_linked_service_azure_file_storage",
    "data_factory_linked_service_azure_function",
    "data_factory_linked_service_azure_search",
    "data_factory_linked_service_azure_sql_database",
    "data_factory_linked_service_azure_table_storage",
    "data_factory_linked_service_cosmosdb",
    "data_factory_linked_service_cosmosdb_mongoapi",
    "data_factory_linked_service_data_lake_storage_gen2",
    "data_factory_linked_service_key_vault",
    "data_factory_linked_service_kusto",
    "data_factory_linked_service_mysql",
    "data_factory_linked_service_odata",
    "data_factory_linked_service_odbc",
    "data_factory_linked_service_postgresql",
    "data_factory_linked_service_sftp",
    "data_factory_linked_service_snowflake",
    "data_factory_linked_service_sql_server",
    "data_factory_linked_service_synapse",
    "data_factory_linked_service_web",
    "data_factory_managed_private_endpoint",
    "data_factory_pipeline",
    "data_factory_trigger_blob_event",
    "data_factory_trigger_custom_event",
    "data_factory_trigger_schedule",
    "data_factory_trigger_tumbling_window",
    "data_protection_backup_instance_blob_storage",
    "data_protection_backup_instance_disk",
    "data_protection_backup_instance_kubernetes_cluster",
    "data_protection_backup_instance_mysql_flexible_server",
    "data_protection_backup_instance_postgresql",
    "data_protection_backup_instance_postgresql_flexible_server",
    "data_protection_backup_policy_blob_storage",
    "data_protection_backup_policy_disk",
    "data_protection_backup_policy_kubernetes_cluster",
    "data_protection_backup_policy_mysql_flexible_server",
    "data_protection_backup_policy_postgresql",
    "data_protection_backup_policy_postgresql_flexible_server",
    "data_protection_backup_vault",
    "data_protection_backup_vault_customer_managed_key",
    "data_protection_resource_guard",
    "data_share",
    "data_share_account",
    "data_share_dataset_blob_storage",
    "data_share_dataset_data_lake_gen2",
    "data_share_dataset_kusto_cluster",
    "data_share_dataset_kusto_database",
    "database_migration_project",
    "database_migration_service",
    "databox_edge_device",
    "databricks_access_connector",
    "databricks_virtual_network_peering",
    "databricks_workspace",
    "databricks_workspace_customer_managed_key",
    "databricks_workspace_root_dbfs_customer_managed_key",
    "datadog_monitor",
    "datadog_monitor_sso_configuration",
    "datadog_monitor_tag_rule",
    "dedicated_hardware_security_module",
    "dedicated_host",
    "dedicated_host_group",
    "dev_center",
    "dev_center_attached_network",
    "dev_center_catalog",
    "dev_center_dev_box_definition",
    "dev_center_environment_type",
    "dev_center_gallery",
    "dev_center_network_connection",
    "dev_center_project",
    "dev_center_project_environment_type",
    "dev_center_project_pool",
    "dev_test_global_vm_shutdown_schedule",
    "dev_test_lab",
    "dev_test_linux_virtual_machine",
    "dev_test_policy",
    "dev_test_schedule",
    "dev_test_virtual_network",
    "dev_test_windows_virtual_machine",
    "digital_twins_endpoint_eventgrid",
    "digital_twins_endpoint_eventhub",
    "digital_twins_endpoint_servicebus",
    "digital_twins_instance",
    "digital_twins_time_series_database_connection",
    "disk_access",
    "disk_encryption_set",
    "dns_a_record",
    "dns_aaaa_record",
    "dns_caa_record",
    "dns_cname_record",
    "dns_mx_record",
    "dns_ns_record",
    "dns_ptr_record",
    "dns_srv_record",
    "dns_txt_record",
    "dns_zone",
    "dynatrace_monitor",
    "dynatrace_tag_rules",
    "elastic_cloud_elasticsearch",
    "elastic_san",
    "elastic_san_volume",
    "elastic_san_volume_group",
    "email_communication_service",
    "email_communication_service_domain",
    "email_communication_service_domain_sender_username",
    "eventgrid_domain",
    "eventgrid_domain_topic",
    "eventgrid_event_subscription",
    "eventgrid_namespace",
    "eventgrid_partner_configuration",
    "eventgrid_system_topic",
    "eventgrid_system_topic_event_subscription",
    "eventgrid_topic",
    "eventhub",
    "eventhub_authorization_rule",
    "eventhub_cluster",
    "eventhub_consumer_group",
    "eventhub_namespace",
    "eventhub_namespace_authorization_rule",
    "eventhub_namespace_customer_managed_key",
    "eventhub_namespace_disaster_recovery_config",
    "eventhub_namespace_schema_group",
    "express_route_circuit",
    "express_route_circuit_authorization",
    "express_route_circuit_connection",
    "express_route_circuit_peering",
    "express_route_connection",
    "express_route_gateway",
    "express_route_port",
    "express_route_port_authorization",
    "extended_custom_location",
    "extended_location_custom_location",
    "fabric_capacity",
    "federated_identity_credential",
    "firewall",
    "firewall_application_rule_collection",
    "firewall_nat_rule_collection",
    "firewall_network_rule_collection",
    "firewall_policy",
    "firewall_policy_rule_collection_group",
    "fluid_relay_server",
    "frontdoor",
    "frontdoor_custom_https_configuration",
    "frontdoor_firewall_policy",
    "frontdoor_rules_engine",
    "function_app",
    "function_app_active_slot",
    "function_app_connection",
    "function_app_flex_consumption",
    "function_app_function",
    "function_app_hybrid_connection",
    "function_app_slot",
    "gallery_application",
    "gallery_application_version",
    "graph_services_account",
    "hdinsight_hadoop_cluster",
    "hdinsight_hbase_cluster",
    "hdinsight_interactive_query_cluster",
    "hdinsight_kafka_cluster",
    "hdinsight_spark_cluster",
    "healthbot",
    "healthcare_dicom_service",
    "healthcare_fhir_service",
    "healthcare_medtech_service",
    "healthcare_medtech_service_fhir_destination",
    "healthcare_service",
    "healthcare_workspace",
    "hpc_cache",
    "hpc_cache_access_policy",
    "hpc_cache_blob_nfs_target",
    "hpc_cache_blob_target",
    "hpc_cache_nfs_target",
    "image",
    "iot_security_device_group",
    "iot_security_solution",
    "iotcentral_application",
    "iotcentral_application_network_rule_set",
    "iotcentral_organization",
    "iothub",
    "iothub_certificate",
    "iothub_consumer_group",
    "iothub_device_update_account",
    "iothub_device_update_instance",
    "iothub_dps",
    "iothub_dps_certificate",
    "iothub_dps_shared_access_policy",
    "iothub_endpoint_cosmosdb_account",
    "iothub_endpoint_eventhub",
    "iothub_endpoint_servicebus_queue",
    "iothub_endpoint_servicebus_topic",
    "iothub_endpoint_storage_container",
    "iothub_enrichment",
    "iothub_fallback_route",
    "iothub_file_upload",
    "iothub_route",
    "iothub_shared_access_policy",
    "ip_group",
    "ip_group_cidr",
    "key_vault",
    "key_vault_access_policy",
    "key_vault_certificate",
    "key_vault_certificate_contacts",
    "key_vault_certificate_issuer",
    "key_vault_key",
    "key_vault_managed_hardware_security_module",
    "key_vault_managed_hardware_security_module_key",
    "key_vault_managed_hardware_security_module_key_rotation_policy",
    "key_vault_managed_hardware_security_module_role_assignment",
    "key_vault_managed_hardware_security_module_role_definition",
    "key_vault_managed_storage_account",
    "key_vault_managed_storage_account_sas_token_definition",
    "key_vault_secret",
    "kubernetes_cluster",
    "kubernetes_cluster_extension",
    "kubernetes_cluster_node_pool",
    "kubernetes_cluster_trusted_access_role_binding",
    "kubernetes_fleet_manager",
    "kubernetes_fleet_member",
    "kubernetes_fleet_update_run",
    "kubernetes_fleet_update_strategy",
    "kubernetes_flux_configuration",
    "kusto_attached_database_configuration",
    "kusto_cluster",
    "kusto_cluster_customer_managed_key",
    "kusto_cluster_managed_private_endpoint",
    "kusto_cluster_principal_assignment",
    "kusto_cosmosdb_data_connection",
    "kusto_database",
    "kusto_database_principal_assignment",
    "kusto_eventgrid_data_connection",
    "kusto_eventhub_data_connection",
    "kusto_iothub_data_connection",
    "kusto_script",
    "lb",
    "lb_backend_address_pool",
    "lb_backend_address_pool_address",
    "lb_nat_pool",
    "lb_nat_rule",
    "lb_outbound_rule",
    "lb_probe",
    "lb_rule",
    "lighthouse_assignment",
    "lighthouse_definition",
    "linux_function_app",
    "linux_function_app_slot",
    "linux_virtual_machine",
    "linux_virtual_machine_scale_set",
    "linux_web_app",
    "linux_web_app_slot",
    "load_test",
    "local_network_gateway",
    "log_analytics_cluster",
    "log_analytics_cluster_customer_managed_key",
    "log_analytics_data_export_rule",
    "log_analytics_datasource_windows_event",
    "log_analytics_datasource_windows_performance_counter",
    "log_analytics_linked_service",
    "log_analytics_linked_storage_account",
    "log_analytics_query_pack",
    "log_analytics_query_pack_query",
    "log_analytics_saved_search",
    "log_analytics_solution",
    "log_analytics_storage_insights",
    "log_analytics_workspace",
    "log_analytics_workspace_table",
    "logic_app_action_custom",
    "logic_app_action_http",
    "logic_app_integration_account",
    "logic_app_integration_account_agreement",
    "logic_app_integration_account_assembly",
    "logic_app_integration_account_batch_configuration",
    "logic_app_integration_account_certificate",
    "logic_app_integration_account_map",
    "logic_app_integration_account_partner",
    "logic_app_integration_account_schema",
    "logic_app_integration_account_session",
    "logic_app_standard",
    "logic_app_trigger_custom",
    "logic_app_trigger_http_request",
    "logic_app_trigger_recurrence",
    "logic_app_workflow",
    "machine_learning_compute_cluster",
    "machine_learning_compute_instance",
    "machine_learning_datastore_blobstorage",
    "machine_learning_datastore_datalake_gen2",
    "machine_learning_datastore_fileshare",
    "machine_learning_inference_cluster",
    "machine_learning_synapse_spark",
    "machine_learning_workspace",
    "machine_learning_workspace_network_outbound_rule_fqdn",
    "machine_learning_workspace_network_outbound_rule_private_endpoint",
    "machine_learning_workspace_network_outbound_rule_service_tag",
    "maintenance_assignment_dedicated_host",
    "maintenance_assignment_dynamic_scope",
    "maintenance_assignment_virtual_machine",
    "maintenance_assignment_virtual_machine_scale_set",
    "maintenance_configuration",
    "managed_application",
    "managed_application_definition",
    "managed_disk",
    "managed_disk_sas_token",
    "managed_lustre_file_system",
    "management_group",
    "management_group_policy_assignment",
    "management_group_policy_exemption",
    "management_group_policy_remediation",
    "management_group_policy_set_definition",
    "management_group_subscription_association",
    "management_group_template_deployment",
    "management_lock",
    "maps_account",
    "maps_creator",
    "marketplace_agreement",
    "marketplace_role_assignment",
    "mobile_network",
    "mobile_network_attached_data_network",
    "mobile_network_data_network",
    "mobile_network_packet_core_control_plane",
    "mobile_network_packet_core_data_plane",
    "mobile_network_service",
    "mobile_network_sim",
    "mobile_network_sim_group",
    "mobile_network_sim_policy",
    "mobile_network_site",
    "mobile_network_slice",
    "mongo_cluster",
    "monitor_aad_diagnostic_setting",
    "monitor_action_group",
    "monitor_activity_log_alert",
    "monitor_alert_processing_rule_action_group",
    "monitor_alert_processing_rule_suppression",
    "monitor_alert_prometheus_rule_group",
    "monitor_autoscale_setting",
    "monitor_data_collection_endpoint",
    "monitor_data_collection_rule",
    "monitor_data_collection_rule_association",
    "monitor_diagnostic_setting",
    "monitor_metric_alert",
    "monitor_private_link_scope",
    "monitor_private_link_scoped_service",
    "monitor_scheduled_query_rules_alert",
    "monitor_scheduled_query_rules_alert_v2",
    "monitor_scheduled_query_rules_log",
    "monitor_smart_detector_alert_rule",
    "monitor_workspace",
    "mssql_database",
    "mssql_database_extended_auditing_policy",
    "mssql_database_vulnerability_assessment_rule_baseline",
    "mssql_elasticpool",
    "mssql_failover_group",
    "mssql_firewall_rule",
    "mssql_job",
    "mssql_job_agent",
    "mssql_job_credential",
    "mssql_job_schedule",
    "mssql_job_step",
    "mssql_job_target_group",
    "mssql_managed_database",
    "mssql_managed_instance",
    "mssql_managed_instance_active_directory_administrator",
    "mssql_managed_instance_failover_group",
    "mssql_managed_instance_security_alert_policy",
    "mssql_managed_instance_transparent_data_encryption",
    "mssql_managed_instance_vulnerability_assessment",
    "mssql_outbound_firewall_rule",
    "mssql_server",
    "mssql_server_dns_alias",
    "mssql_server_extended_auditing_policy",
    "mssql_server_microsoft_support_auditing_policy",
    "mssql_server_security_alert_policy",
    "mssql_server_transparent_data_encryption",
    "mssql_server_vulnerability_assessment",
    "mssql_virtual_machine",
    "mssql_virtual_machine_availability_group_listener",
    "mssql_virtual_machine_group",
    "mssql_virtual_network_rule",
    "mysql_flexible_database",
    "mysql_flexible_server",
    "mysql_flexible_server_active_directory_administrator",
    "mysql_flexible_server_configuration",
    "mysql_flexible_server_firewall_rule",
    "nat_gateway",
    "nat_gateway_public_ip_association",
    "nat_gateway_public_ip_prefix_association",
    "netapp_account",
    "netapp_account_encryption",
    "netapp_backup_policy",
    "netapp_backup_vault",
    "netapp_pool",
    "netapp_snapshot",
    "netapp_snapshot_policy",
    "netapp_volume",
    "netapp_volume_group_oracle",
    "netapp_volume_group_sap_hana",
    "netapp_volume_quota_rule",
    "network_connection_monitor",
    "network_ddos_protection_plan",
    "network_function_azure_traffic_collector",
    "network_function_collector_policy",
    "network_interface",
    "network_interface_application_gateway_backend_address_pool_association",
    "network_interface_application_security_group_association",
    "network_interface_backend_address_pool_association",
    "network_interface_nat_rule_association",
    "network_interface_security_group_association",
    "network_manager",
    "network_manager_admin_rule",
    "network_manager_admin_rule_collection",
    "network_manager_connectivity_configuration",
    "network_manager_deployment",
    "network_manager_ipam_pool",
    "network_manager_management_group_connection",
    "network_manager_network_group",
    "network_manager_routing_configuration",
    "network_manager_scope_connection",
    "network_manager_security_admin_configuration",
    "network_manager_static_member",
    "network_manager_subscription_connection",
    "network_manager_verifier_workspace",
    "network_packet_capture",
    "network_profile",
    "network_security_group",
    "network_security_rule",
    "network_watcher",
    "network_watcher_flow_log",
    "new_relic_monitor",
    "new_relic_tag_rule",
    "nginx_api_key",
    "nginx_certificate",
    "nginx_configuration",
    "nginx_deployment",
    "notification_hub",
    "notification_hub_authorization_rule",
    "notification_hub_namespace",
    "oracle_autonomous_database",
    "oracle_cloud_vm_cluster",
    "oracle_exadata_infrastructure",
    "orbital_contact",
    "orbital_contact_profile",
    "orbital_spacecraft",
    "orchestrated_virtual_machine_scale_set",
    "palo_alto_local_rulestack",
    "palo_alto_local_rulestack_certificate",
    "palo_alto_local_rulestack_fqdn_list",
    "palo_alto_local_rulestack_outbound_trust_certificate_association",
    "palo_alto_local_rulestack_outbound_untrust_certificate_association",
    "palo_alto_local_rulestack_prefix_list",
    "palo_alto_local_rulestack_rule",
    "palo_alto_next_generation_firewall_virtual_hub_local_rulestack",
    "palo_alto_next_generation_firewall_virtual_hub_panorama",
    "palo_alto_next_generation_firewall_virtual_network_local_rulestack",
    "palo_alto_next_generation_firewall_virtual_network_panorama",
    "palo_alto_virtual_network_appliance",
    "pim_active_role_assignment",
    "pim_eligible_role_assignment",
    "point_to_site_vpn_gateway",
    "policy_definition",
    "policy_set_definition",
    "policy_virtual_machine_configuration_assignment",
    "portal_dashboard",
    "portal_tenant_configuration",
    "postgresql_active_directory_administrator",
    "postgresql_configuration",
    "postgresql_database",
    "postgresql_firewall_rule",
    "postgresql_flexible_server",
    "postgresql_flexible_server_active_directory_administrator",
    "postgresql_flexible_server_configuration",
    "postgresql_flexible_server_database",
    "postgresql_flexible_server_firewall_rule",
    "postgresql_flexible_server_virtual_endpoint",
    "postgresql_server",
    "postgresql_server_key",
    "postgresql_virtual_network_rule",
    "powerbi_embedded",
    "private_dns_a_record",
    "private_dns_aaaa_record",
    "private_dns_cname_record",
    "private_dns_mx_record",
    "private_dns_ptr_record",
    "private_dns_resolver",
    "private_dns_resolver_dns_forwarding_ruleset",
    "private_dns_resolver_forwarding_rule",
    "private_dns_resolver_inbound_endpoint",
    "private_dns_resolver_outbound_endpoint",
    "private_dns_resolver_virtual_network_link",
    "private_dns_srv_record",
    "private_dns_txt_record",
    "private_dns_zone",
    "private_dns_zone_virtual_network_link",
    "private_endpoint",
    "private_endpoint_application_security_group_association",
    "private_link_service",
    "provider",
    "proximity_placement_group",
    "public_ip",
    "public_ip_prefix",
    "purview_account",
    "qumulo_file_system",
    "recovery_services_vault",
    "recovery_services_vault_resource_guard_association",
    "redhat_openshift_cluster",
    "redis_cache",
    "redis_cache_access_policy",
    "redis_cache_access_policy_assignment",
    "redis_enterprise_cluster",
    "redis_enterprise_database",
    "redis_firewall_rule",
    "redis_linked_server",
    "relay_hybrid_connection",
    "relay_hybrid_connection_authorization_rule",
    "relay_namespace",
    "relay_namespace_authorization_rule",
    "resource_deployment_script_azure_cli",
    "resource_deployment_script_azure_power_shell",
    "resource_group",
    "resource_group_cost_management_export",
    "resource_group_cost_management_view",
    "resource_group_policy_assignment",
    "resource_group_policy_exemption",
    "resource_group_policy_remediation",
    "resource_group_template_deployment",
    "resource_management_private_link",
    "resource_management_private_link_association",
    "resource_policy_assignment",
    "resource_policy_exemption",
    "resource_policy_remediation",
    "resource_provider_registration",
    "restore_point_collection",
    "role_assignment",
    "role_definition",
    "role_management_policy",
    "route",
    "route_filter",
    "route_map",
    "route_server",
    "route_server_bgp_connection",
    "route_table",
    "search_service",
    "search_shared_private_link_service",
    "security_center_assessment",
    "security_center_assessment_policy",
    "security_center_auto_provisioning",
    "security_center_automation",
    "security_center_contact",
    "security_center_server_vulnerability_assessment_virtual_machine",
    "security_center_server_vulnerability_assessments_setting",
    "security_center_setting",
    "security_center_storage_defender",
    "security_center_subscription_pricing",
    "security_center_workspace",
    "sentinel_alert_rule_anomaly_built_in",
    "sentinel_alert_rule_anomaly_duplicate",
    "sentinel_alert_rule_fusion",
    "sentinel_alert_rule_machine_learning_behavior_analytics",
    "sentinel_alert_rule_ms_security_incident",
    "sentinel_alert_rule_nrt",
    "sentinel_alert_rule_scheduled",
    "sentinel_alert_rule_threat_intelligence",
    "sentinel_automation_rule",
    "sentinel_data_connector_aws_cloud_trail",
    "sentinel_data_connector_aws_s3",
    "sentinel_data_connector_azure_active_directory",
    "sentinel_data_connector_azure_advanced_threat_protection",
    "sentinel_data_connector_azure_security_center",
    "sentinel_data_connector_dynamics365",
    "sentinel_data_connector_iot",
    "sentinel_data_connector_microsoft_cloud_app_security",
    "sentinel_data_connector_microsoft_defender_advanced_threat_protection",
    "sentinel_data_connector_microsoft_threat_intelligence",
    "sentinel_data_connector_microsoft_threat_protection",
    "sentinel_data_connector_office365",
    "sentinel_data_connector_office365_project",
    "sentinel_data_connector_office_atp",
    "sentinel_data_connector_office_irm",
    "sentinel_data_connector_office_power_bi",
    "sentinel_data_connector_threat_intelligence",
    "sentinel_data_connector_threat_intelligence_taxii",
    "sentinel_log_analytics_workspace_onboarding",
    "sentinel_metadata",
    "sentinel_threat_intelligence_indicator",
    "sentinel_watchlist",
    "sentinel_watchlist_item",
    "service_fabric_cluster",
    "service_fabric_managed_cluster",
    "service_plan",
    "servicebus_namespace",
    "servicebus_namespace_authorization_rule",
    "servicebus_namespace_customer_managed_key",
    "servicebus_namespace_disaster_recovery_config",
    "servicebus_queue",
    "servicebus_queue_authorization_rule",
    "servicebus_subscription",
    "servicebus_subscription_rule",
    "servicebus_topic",
    "servicebus_topic_authorization_rule",
    "shared_image",
    "shared_image_gallery",
    "shared_image_version",
    "signalr_service",
    "signalr_service_custom_certificate",
    "signalr_service_custom_domain",
    "signalr_service_network_acl",
    "signalr_shared_private_link_resource",
    "site_recovery_fabric",
    "site_recovery_hyperv_network_mapping",
    "site_recovery_hyperv_replication_policy",
    "site_recovery_hyperv_replication_policy_association",
    "site_recovery_network_mapping",
    "site_recovery_protection_container",
    "site_recovery_protection_container_mapping",
    "site_recovery_replicated_vm",
    "site_recovery_replication_policy",
    "site_recovery_replication_recovery_plan",
    "site_recovery_services_vault_hyperv_site",
    "site_recovery_vmware_replicated_vm",
    "site_recovery_vmware_replication_policy",
    "site_recovery_vmware_replication_policy_association",
    "snapshot",
    "source_control_token",
    "spatial_anchors_account",
    "spring_cloud_accelerator",
    "spring_cloud_active_deployment",
    "spring_cloud_api_portal",
    "spring_cloud_api_portal_custom_domain",
    "spring_cloud_app",
    "spring_cloud_app_cosmosdb_association",
    "spring_cloud_app_dynamics_application_performance_monitoring",
    "spring_cloud_app_mysql_association",
    "spring_cloud_app_redis_association",
    "spring_cloud_application_insights_application_performance_monitoring",
    "spring_cloud_application_live_view",
    "spring_cloud_build_deployment",
    "spring_cloud_build_pack_binding",
    "spring_cloud_builder",
    "spring_cloud_certificate",
    "spring_cloud_configuration_service",
    "spring_cloud_connection",
    "spring_cloud_container_deployment",
    "spring_cloud_custom_domain",
    "spring_cloud_customized_accelerator",
    "spring_cloud_dev_tool_portal",
    "spring_cloud_dynatrace_application_performance_monitoring",
    "spring_cloud_elastic_application_performance_monitoring",
    "spring_cloud_gateway",
    "spring_cloud_gateway_custom_domain",
    "spring_cloud_gateway_route_config",
    "spring_cloud_java_deployment",
    "spring_cloud_new_relic_application_performance_monitoring",
    "spring_cloud_service",
    "spring_cloud_storage",
    "ssh_public_key",
    "stack_hci_cluster",
    "stack_hci_deployment_setting",
    "stack_hci_extension",
    "stack_hci_logical_network",
    "stack_hci_marketplace_gallery_image",
    "stack_hci_network_interface",
    "stack_hci_storage_path",
    "stack_hci_virtual_hard_disk",
    "static_site",
    "static_site_custom_domain",
    "static_web_app",
    "static_web_app_custom_domain",
    "static_web_app_function_app_registration",
    "storage_account",
    "storage_account_customer_managed_key",
    "storage_account_local_user",
    "storage_account_network_rules",
    "storage_account_queue_properties",
    "storage_account_static_website",
    "storage_blob",
    "storage_blob_inventory_policy",
    "storage_container",
    "storage_container_immutability_policy",
    "storage_data_lake_gen2_filesystem",
    "storage_data_lake_gen2_path",
    "storage_encryption_scope",
    "storage_management_policy",
    "storage_mover",
    "storage_mover_agent",
    "storage_mover_job_definition",
    "storage_mover_project",
    "storage_mover_source_endpoint",
    "storage_mover_target_endpoint",
    "storage_object_replication",
    "storage_queue",
    "storage_share",
    "storage_share_directory",
    "storage_share_file",
    "storage_sync",
    "storage_sync_cloud_endpoint",
    "storage_sync_group",
    "storage_sync_server_endpoint",
    "storage_table",
    "storage_table_entity",
    "stream_analytics_cluster",
    "stream_analytics_function_javascript_uda",
    "stream_analytics_function_javascript_udf",
    "stream_analytics_job",
    "stream_analytics_job_schedule",
    "stream_analytics_job_storage_account",
    "stream_analytics_managed_private_endpoint",
    "stream_analytics_output_blob",
    "stream_analytics_output_cosmosdb",
    "stream_analytics_output_eventhub",
    "stream_analytics_output_function",
    "stream_analytics_output_mssql",
    "stream_analytics_output_powerbi",
    "stream_analytics_output_servicebus_queue",
    "stream_analytics_output_servicebus_topic",
    "stream_analytics_output_synapse",
    "stream_analytics_output_table",
    "stream_analytics_reference_input_blob",
    "stream_analytics_reference_input_mssql",
    "stream_analytics_stream_input_blob",
    "stream_analytics_stream_input_eventhub",
    "stream_analytics_stream_input_eventhub_v2",
    "stream_analytics_stream_input_iothub",
    "subnet",
    "subnet_nat_gateway_association",
    "subnet_network_security_group_association",
    "subnet_route_table_association",
    "subnet_service_endpoint_storage_policy",
    "subscription",
    "subscription_cost_management_export",
    "subscription_cost_management_view",
    "subscription_policy_assignment",
    "subscription_policy_exemption",
    "subscription_policy_remediation",
    "subscription_template_deployment",
    "synapse_firewall_rule",
    "synapse_integration_runtime_azure",
    "synapse_integration_runtime_self_hosted",
    "synapse_linked_service",
    "synapse_managed_private_endpoint",
    "synapse_private_link_hub",
    "synapse_role_assignment",
    "synapse_spark_pool",
    "synapse_sql_pool",
    "synapse_sql_pool_extended_auditing_policy",
    "synapse_sql_pool_security_alert_policy",
    "synapse_sql_pool_vulnerability_assessment",
    "synapse_sql_pool_vulnerability_assessment_baseline",
    "synapse_sql_pool_workload_classifier",
    "synapse_sql_pool_workload_group",
    "synapse_workspace",
    "synapse_workspace_aad_admin",
    "synapse_workspace_extended_auditing_policy",
    "synapse_workspace_key",
    "synapse_workspace_security_alert_policy",
    "synapse_workspace_sql_aad_admin",
    "synapse_workspace_vulnerability_assessment",
    "system_center_virtual_machine_manager_availability_set",
    "system_center_virtual_machine_manager_cloud",
    "system_center_virtual_machine_manager_server",
    "system_center_virtual_machine_manager_virtual_machine_instance",
    "system_center_virtual_machine_manager_virtual_machine_instance_guest_agent",
    "system_center_virtual_machine_manager_virtual_machine_template",
    "system_center_virtual_machine_manager_virtual_network",
    "tenant_template_deployment",
    "traffic_manager_azure_endpoint",
    "traffic_manager_external_endpoint",
    "traffic_manager_nested_endpoint",
    "traffic_manager_profile",
    "trusted_signing_account",
    "user_assigned_identity",
    "video_indexer_account",
    "virtual_desktop_application",
    "virtual_desktop_application_group",
    "virtual_desktop_host_pool",
    "virtual_desktop_host_pool_registration_info",
    "virtual_desktop_scaling_plan",
    "virtual_desktop_scaling_plan_host_pool_association",
    "virtual_desktop_workspace",
    "virtual_desktop_workspace_application_group_association",
    "virtual_hub",
    "virtual_hub_bgp_connection",
    "virtual_hub_connection",
    "virtual_hub_ip",
    "virtual_hub_route_table",
    "virtual_hub_route_table_route",
    "virtual_hub_routing_intent",
    "virtual_hub_security_partner_provider",
    "virtual_machine",
    "virtual_machine_automanage_configuration_assignment",
    "virtual_machine_data_disk_attachment",
    "virtual_machine_extension",
    "virtual_machine_gallery_application_assignment",
    "virtual_machine_implicit_data_disk_from_source",
    "virtual_machine_packet_capture",
    "virtual_machine_restore_point",
    "virtual_machine_restore_point_collection",
    "virtual_machine_run_command",
    "virtual_machine_scale_set",
    "virtual_machine_scale_set_extension",
    "virtual_machine_scale_set_packet_capture",
    "virtual_machine_scale_set_standby_pool",
    "virtual_network",
    "virtual_network_dns_servers",
    "virtual_network_gateway",
    "virtual_network_gateway_connection",
    "virtual_network_gateway_nat_rule",
    "virtual_network_peering",
    "virtual_wan",
    "vmware_cluster",
    "vmware_express_route_authorization",
    "vmware_netapp_volume_attachment",
    "vmware_private_cloud",
    "voice_services_communications_gateway",
    "voice_services_communications_gateway_test_line",
    "vpn_gateway",
    "vpn_gateway_connection",
    "vpn_gateway_nat_rule",
    "vpn_server_configuration",
    "vpn_server_configuration_policy_group",
    "vpn_site",
    "web_app_active_slot",
    "web_app_hybrid_connection",
    "web_application_firewall_policy",
    "web_pubsub",
    "web_pubsub_custom_certificate",
    "web_pubsub_custom_domain",
    "web_pubsub_hub",
    "web_pubsub_network_acl",
    "web_pubsub_shared_private_link_resource",
    "web_pubsub_socketio",
    "windows_function_app",
    "windows_function_app_slot",
    "windows_virtual_machine",
    "windows_virtual_machine_scale_set",
    "windows_web_app",
    "windows_web_app_slot",
    "workloads_sap_discovery_virtual_instance",
    "workloads_sap_single_node_virtual_instance",
    "workloads_sap_three_tier_virtual_instance",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import aadb2_c_directory
from . import active_directory_domain_service
from . import active_directory_domain_service_replica_set
from . import active_directory_domain_service_trust
from . import advanced_threat_protection
from . import advisor_suppression
from . import ai_foundry
from . import ai_foundry_project
from . import ai_services
from . import analysis_services_server
from . import api_connection
from . import api_management
from . import api_management_api
from . import api_management_api_diagnostic
from . import api_management_api_operation
from . import api_management_api_operation_policy
from . import api_management_api_operation_tag
from . import api_management_api_policy
from . import api_management_api_release
from . import api_management_api_schema
from . import api_management_api_tag
from . import api_management_api_tag_description
from . import api_management_api_version_set
from . import api_management_authorization_server
from . import api_management_backend
from . import api_management_certificate
from . import api_management_custom_domain
from . import api_management_diagnostic
from . import api_management_email_template
from . import api_management_gateway
from . import api_management_gateway_api
from . import api_management_gateway_certificate_authority
from . import api_management_gateway_host_name_configuration
from . import api_management_global_schema
from . import api_management_group
from . import api_management_group_user
from . import api_management_identity_provider_aad
from . import api_management_identity_provider_aadb2_c
from . import api_management_identity_provider_facebook
from . import api_management_identity_provider_google
from . import api_management_identity_provider_microsoft
from . import api_management_identity_provider_twitter
from . import api_management_logger
from . import api_management_named_value
from . import api_management_notification_recipient_email
from . import api_management_notification_recipient_user
from . import api_management_openid_connect_provider
from . import api_management_policy
from . import api_management_policy_fragment
from . import api_management_product
from . import api_management_product_api
from . import api_management_product_group
from . import api_management_product_policy
from . import api_management_product_tag
from . import api_management_redis_cache
from . import api_management_subscription
from . import api_management_tag
from . import api_management_user
from . import app_configuration
from . import app_configuration_feature
from . import app_configuration_key
from . import app_service
from . import app_service_active_slot
from . import app_service_certificate
from . import app_service_certificate_binding
from . import app_service_certificate_order
from . import app_service_connection
from . import app_service_custom_hostname_binding
from . import app_service_environment_v3
from . import app_service_hybrid_connection
from . import app_service_managed_certificate
from . import app_service_plan
from . import app_service_public_certificate
from . import app_service_slot
from . import app_service_slot_custom_hostname_binding
from . import app_service_slot_virtual_network_swift_connection
from . import app_service_source_control
from . import app_service_source_control_slot
from . import app_service_source_control_token
from . import app_service_virtual_network_swift_connection
from . import application_gateway
from . import application_insights
from . import application_insights_analytics_item
from . import application_insights_api_key
from . import application_insights_smart_detection_rule
from . import application_insights_standard_web_test
from . import application_insights_web_test
from . import application_insights_workbook
from . import application_insights_workbook_template
from . import application_load_balancer
from . import application_load_balancer_frontend
from . import application_load_balancer_subnet_association
from . import application_security_group
from . import arc_kubernetes_cluster
from . import arc_kubernetes_cluster_extension
from . import arc_kubernetes_flux_configuration
from . import arc_kubernetes_provisioned_cluster
from . import arc_machine
from . import arc_machine_automanage_configuration_assignment
from . import arc_machine_extension
from . import arc_private_link_scope
from . import arc_resource_bridge_appliance
from . import attestation_provider
from . import automanage_configuration
from . import automation_account
from . import automation_certificate
from . import automation_connection
from . import automation_connection_certificate
from . import automation_connection_classic_certificate
from . import automation_connection_service_principal
from . import automation_connection_type
from . import automation_credential
from . import automation_dsc_configuration
from . import automation_dsc_nodeconfiguration
from . import automation_hybrid_runbook_worker
from . import automation_hybrid_runbook_worker_group
from . import automation_job_schedule
from . import automation_module
from . import automation_powershell72_module
from . import automation_python3_package
from . import automation_runbook
from . import automation_schedule
from . import automation_software_update_configuration
from . import automation_source_control
from . import automation_variable_bool
from . import automation_variable_datetime
from . import automation_variable_int
from . import automation_variable_object
from . import automation_variable_string
from . import automation_watcher
from . import automation_webhook
from . import availability_set
from . import backup_container_storage_account
from . import backup_policy_file_share
from . import backup_policy_vm
from . import backup_policy_vm_workload
from . import backup_protected_file_share
from . import backup_protected_vm
from . import bastion_host
from . import batch_account
from . import batch_application
from . import batch_certificate
from . import batch_job
from . import batch_pool
from . import billing_account_cost_management_export
from . import blueprint_assignment
from . import bot_channel_alexa
from . import bot_channel_direct_line_speech
from . import bot_channel_directline
from . import bot_channel_email
from . import bot_channel_facebook
from . import bot_channel_line
from . import bot_channel_ms_teams
from . import bot_channel_slack
from . import bot_channel_sms
from . import bot_channel_web_chat
from . import bot_channels_registration
from . import bot_connection
from . import bot_service_azure_bot
from . import bot_web_app
from . import capacity_reservation
from . import capacity_reservation_group
from . import cdn_endpoint
from . import cdn_endpoint_custom_domain
from . import cdn_frontdoor_custom_domain
from . import cdn_frontdoor_custom_domain_association
from . import cdn_frontdoor_endpoint
from . import cdn_frontdoor_firewall_policy
from . import cdn_frontdoor_origin
from . import cdn_frontdoor_origin_group
from . import cdn_frontdoor_profile
from . import cdn_frontdoor_route
from . import cdn_frontdoor_rule
from . import cdn_frontdoor_rule_set
from . import cdn_frontdoor_secret
from . import cdn_frontdoor_security_policy
from . import cdn_profile
from . import chaos_studio_capability
from . import chaos_studio_experiment
from . import chaos_studio_target
from . import cognitive_account
from . import cognitive_account_customer_managed_key
from . import cognitive_account_rai_blocklist
from . import cognitive_account_rai_policy
from . import cognitive_deployment
from . import communication_service
from . import communication_service_email_domain_association
from . import confidential_ledger
from . import consumption_budget_management_group
from . import consumption_budget_resource_group
from . import consumption_budget_subscription
from . import container_app
from . import container_app_custom_domain
from . import container_app_environment
from . import container_app_environment_certificate
from . import container_app_environment_custom_domain
from . import container_app_environment_dapr_component
from . import container_app_environment_storage
from . import container_app_job
from . import container_connected_registry
from . import container_group
from . import container_registry
from . import container_registry_agent_pool
from . import container_registry_cache_rule
from . import container_registry_credential_set
from . import container_registry_scope_map
from . import container_registry_task
from . import container_registry_task_schedule_run_now
from . import container_registry_token
from . import container_registry_token_password
from . import container_registry_webhook
from . import cosmosdb_account
from . import cosmosdb_cassandra_cluster
from . import cosmosdb_cassandra_datacenter
from . import cosmosdb_cassandra_keyspace
from . import cosmosdb_cassandra_table
from . import cosmosdb_gremlin_database
from . import cosmosdb_gremlin_graph
from . import cosmosdb_mongo_collection
from . import cosmosdb_mongo_database
from . import cosmosdb_mongo_role_definition
from . import cosmosdb_mongo_user_definition
from . import cosmosdb_postgresql_cluster
from . import cosmosdb_postgresql_coordinator_configuration
from . import cosmosdb_postgresql_firewall_rule
from . import cosmosdb_postgresql_node_configuration
from . import cosmosdb_postgresql_role
from . import cosmosdb_sql_container
from . import cosmosdb_sql_database
from . import cosmosdb_sql_dedicated_gateway
from . import cosmosdb_sql_function
from . import cosmosdb_sql_role_assignment
from . import cosmosdb_sql_role_definition
from . import cosmosdb_sql_stored_procedure
from . import cosmosdb_sql_trigger
from . import cosmosdb_table
from . import cost_anomaly_alert
from . import cost_management_scheduled_action
from . import custom_ip_prefix
from . import custom_provider
from . import dashboard_grafana
from . import dashboard_grafana_managed_private_endpoint
from . import data_azurerm_aadb2_c_directory
from . import data_azurerm_active_directory_domain_service
from . import data_azurerm_advisor_recommendations
from . import data_azurerm_api_management
from . import data_azurerm_api_management_api
from . import data_azurerm_api_management_api_version_set
from . import data_azurerm_api_management_gateway
from . import data_azurerm_api_management_gateway_host_name_configuration
from . import data_azurerm_api_management_group
from . import data_azurerm_api_management_product
from . import data_azurerm_api_management_subscription
from . import data_azurerm_api_management_user
from . import data_azurerm_app_configuration
from . import data_azurerm_app_configuration_key
from . import data_azurerm_app_configuration_keys
from . import data_azurerm_app_service
from . import data_azurerm_app_service_certificate
from . import data_azurerm_app_service_certificate_order
from . import data_azurerm_app_service_environment_v3
from . import data_azurerm_app_service_plan
from . import data_azurerm_application_gateway
from . import data_azurerm_application_insights
from . import data_azurerm_application_security_group
from . import data_azurerm_arc_machine
from . import data_azurerm_arc_resource_bridge_appliance
from . import data_azurerm_attestation_provider
from . import data_azurerm_automation_account
from . import data_azurerm_automation_runbook
from . import data_azurerm_automation_variable_bool
from . import data_azurerm_automation_variable_datetime
from . import data_azurerm_automation_variable_int
from . import data_azurerm_automation_variable_object
from . import data_azurerm_automation_variable_string
from . import data_azurerm_automation_variables
from . import data_azurerm_availability_set
from . import data_azurerm_backup_policy_file_share
from . import data_azurerm_backup_policy_vm
from . import data_azurerm_bastion_host
from . import data_azurerm_batch_account
from . import data_azurerm_batch_application
from . import data_azurerm_batch_certificate
from . import data_azurerm_batch_pool
from . import data_azurerm_billing_enrollment_account_scope
from . import data_azurerm_billing_mca_account_scope
from . import data_azurerm_billing_mpa_account_scope
from . import data_azurerm_blueprint_definition
from . import data_azurerm_blueprint_published_version
from . import data_azurerm_cdn_frontdoor_custom_domain
from . import data_azurerm_cdn_frontdoor_endpoint
from . import data_azurerm_cdn_frontdoor_firewall_policy
from . import data_azurerm_cdn_frontdoor_origin_group
from . import data_azurerm_cdn_frontdoor_profile
from . import data_azurerm_cdn_frontdoor_rule_set
from . import data_azurerm_cdn_frontdoor_secret
from . import data_azurerm_cdn_profile
from . import data_azurerm_client_config
from . import data_azurerm_cognitive_account
from . import data_azurerm_communication_service
from . import data_azurerm_confidential_ledger
from . import data_azurerm_consumption_budget_resource_group
from . import data_azurerm_consumption_budget_subscription
from . import data_azurerm_container_app
from . import data_azurerm_container_app_environment
from . import data_azurerm_container_app_environment_certificate
from . import data_azurerm_container_group
from . import data_azurerm_container_registry
from . import data_azurerm_container_registry_cache_rule
from . import data_azurerm_container_registry_scope_map
from . import data_azurerm_container_registry_token
from . import data_azurerm_cosmosdb_account
from . import data_azurerm_cosmosdb_mongo_database
from . import data_azurerm_cosmosdb_restorable_database_accounts
from . import data_azurerm_cosmosdb_sql_database
from . import data_azurerm_cosmosdb_sql_role_definition
from . import data_azurerm_dashboard_grafana
from . import data_azurerm_data_factory
from . import data_azurerm_data_factory_trigger_schedule
from . import data_azurerm_data_factory_trigger_schedules
from . import data_azurerm_data_protection_backup_vault
from . import data_azurerm_data_share
from . import data_azurerm_data_share_account
from . import data_azurerm_data_share_dataset_blob_storage
from . import data_azurerm_data_share_dataset_data_lake_gen2
from . import data_azurerm_data_share_dataset_kusto_cluster
from . import data_azurerm_data_share_dataset_kusto_database
from . import data_azurerm_database_migration_project
from . import data_azurerm_database_migration_service
from . import data_azurerm_databox_edge_device
from . import data_azurerm_databricks_access_connector
from . import data_azurerm_databricks_workspace
from . import data_azurerm_databricks_workspace_private_endpoint_connection
from . import data_azurerm_dedicated_host
from . import data_azurerm_dedicated_host_group
from . import data_azurerm_dev_center
from . import data_azurerm_dev_center_attached_network
from . import data_azurerm_dev_center_catalog
from . import data_azurerm_dev_center_dev_box_definition
from . import data_azurerm_dev_center_environment_type
from . import data_azurerm_dev_center_gallery
from . import data_azurerm_dev_center_network_connection
from . import data_azurerm_dev_center_project
from . import data_azurerm_dev_center_project_environment_type
from . import data_azurerm_dev_center_project_pool
from . import data_azurerm_dev_test_lab
from . import data_azurerm_dev_test_virtual_network
from . import data_azurerm_digital_twins_instance
from . import data_azurerm_disk_access
from . import data_azurerm_disk_encryption_set
from . import data_azurerm_dns_a_record
from . import data_azurerm_dns_aaaa_record
from . import data_azurerm_dns_caa_record
from . import data_azurerm_dns_cname_record
from . import data_azurerm_dns_mx_record
from . import data_azurerm_dns_ns_record
from . import data_azurerm_dns_ptr_record
from . import data_azurerm_dns_soa_record
from . import data_azurerm_dns_srv_record
from . import data_azurerm_dns_txt_record
from . import data_azurerm_dns_zone
from . import data_azurerm_dynatrace_monitor
from . import data_azurerm_elastic_cloud_elasticsearch
from . import data_azurerm_elastic_san
from . import data_azurerm_elastic_san_volume_group
from . import data_azurerm_elastic_san_volume_snapshot
from . import data_azurerm_eventgrid_domain
from . import data_azurerm_eventgrid_domain_topic
from . import data_azurerm_eventgrid_system_topic
from . import data_azurerm_eventgrid_topic
from . import data_azurerm_eventhub
from . import data_azurerm_eventhub_authorization_rule
from . import data_azurerm_eventhub_cluster
from . import data_azurerm_eventhub_consumer_group
from . import data_azurerm_eventhub_namespace
from . import data_azurerm_eventhub_namespace_authorization_rule
from . import data_azurerm_eventhub_sas
from . import data_azurerm_express_route_circuit
from . import data_azurerm_express_route_circuit_peering
from . import data_azurerm_extended_location_custom_location
from . import data_azurerm_extended_locations
from . import data_azurerm_firewall
from . import data_azurerm_firewall_policy
from . import data_azurerm_function_app
from . import data_azurerm_function_app_host_keys
from . import data_azurerm_hdinsight_cluster
from . import data_azurerm_healthcare_dicom_service
from . import data_azurerm_healthcare_fhir_service
from . import data_azurerm_healthcare_medtech_service
from . import data_azurerm_healthcare_service
from . import data_azurerm_healthcare_workspace
from . import data_azurerm_image
from . import data_azurerm_images
from . import data_azurerm_iothub
from . import data_azurerm_iothub_dps
from . import data_azurerm_iothub_dps_shared_access_policy
from . import data_azurerm_iothub_shared_access_policy
from . import data_azurerm_ip_group
from . import data_azurerm_ip_groups
from . import data_azurerm_key_vault
from . import data_azurerm_key_vault_access_policy
from . import data_azurerm_key_vault_certificate
from . import data_azurerm_key_vault_certificate_data
from . import data_azurerm_key_vault_certificate_issuer
from . import data_azurerm_key_vault_certificates
from . import data_azurerm_key_vault_encrypted_value
from . import data_azurerm_key_vault_key
from . import data_azurerm_key_vault_managed_hardware_security_module
from . import data_azurerm_key_vault_managed_hardware_security_module_key
from . import data_azurerm_key_vault_managed_hardware_security_module_role_definition
from . import data_azurerm_key_vault_secret
from . import data_azurerm_key_vault_secrets
from . import data_azurerm_kubernetes_cluster
from . import data_azurerm_kubernetes_cluster_node_pool
from . import data_azurerm_kubernetes_fleet_manager
from . import data_azurerm_kubernetes_node_pool_snapshot
from . import data_azurerm_kubernetes_service_versions
from . import data_azurerm_kusto_cluster
from . import data_azurerm_kusto_database
from . import data_azurerm_lb
from . import data_azurerm_lb_backend_address_pool
from . import data_azurerm_lb_outbound_rule
from . import data_azurerm_lb_rule
from . import data_azurerm_linux_function_app
from . import data_azurerm_linux_web_app
from . import data_azurerm_load_test
from . import data_azurerm_local_network_gateway
from . import data_azurerm_location
from . import data_azurerm_log_analytics_workspace
from . import data_azurerm_logic_app_integration_account
from . import data_azurerm_logic_app_standard
from . import data_azurerm_logic_app_workflow
from . import data_azurerm_machine_learning_workspace
from . import data_azurerm_maintenance_configuration
from . import data_azurerm_managed_api
from . import data_azurerm_managed_application_definition
from . import data_azurerm_managed_disk
from . import data_azurerm_management_group
from . import data_azurerm_management_group_template_deployment
from . import data_azurerm_maps_account
from . import data_azurerm_marketplace_agreement
from . import data_azurerm_mobile_network
from . import data_azurerm_mobile_network_attached_data_network
from . import data_azurerm_mobile_network_data_network
from . import data_azurerm_mobile_network_packet_core_control_plane
from . import data_azurerm_mobile_network_packet_core_data_plane
from . import data_azurerm_mobile_network_service
from . import data_azurerm_mobile_network_sim
from . import data_azurerm_mobile_network_sim_group
from . import data_azurerm_mobile_network_sim_policy
from . import data_azurerm_mobile_network_site
from . import data_azurerm_mobile_network_slice
from . import data_azurerm_monitor_action_group
from . import data_azurerm_monitor_data_collection_endpoint
from . import data_azurerm_monitor_data_collection_rule
from . import data_azurerm_monitor_diagnostic_categories
from . import data_azurerm_monitor_scheduled_query_rules_alert
from . import data_azurerm_monitor_scheduled_query_rules_log
from . import data_azurerm_monitor_workspace
from . import data_azurerm_mssql_database
from . import data_azurerm_mssql_elasticpool
from . import data_azurerm_mssql_managed_database
from . import data_azurerm_mssql_managed_instance
from . import data_azurerm_mssql_server
from . import data_azurerm_mysql_flexible_server
from . import data_azurerm_nat_gateway
from . import data_azurerm_netapp_account
from . import data_azurerm_netapp_account_encryption
from . import data_azurerm_netapp_backup_policy
from . import data_azurerm_netapp_backup_vault
from . import data_azurerm_netapp_pool
from . import data_azurerm_netapp_snapshot
from . import data_azurerm_netapp_snapshot_policy
from . import data_azurerm_netapp_volume
from . import data_azurerm_netapp_volume_group_oracle
from . import data_azurerm_netapp_volume_group_sap_hana
from . import data_azurerm_netapp_volume_quota_rule
from . import data_azurerm_network_ddos_protection_plan
from . import data_azurerm_network_interface
from . import data_azurerm_network_manager
from . import data_azurerm_network_manager_connectivity_configuration
from . import data_azurerm_network_manager_network_group
from . import data_azurerm_network_security_group
from . import data_azurerm_network_service_tags
from . import data_azurerm_network_watcher
from . import data_azurerm_nginx_api_key
from . import data_azurerm_nginx_certificate
from . import data_azurerm_nginx_configuration
from . import data_azurerm_nginx_deployment
from . import data_azurerm_notification_hub
from . import data_azurerm_notification_hub_namespace
from . import data_azurerm_oracle_adbs_character_sets
from . import data_azurerm_oracle_adbs_national_character_sets
from . import data_azurerm_oracle_autonomous_database
from . import data_azurerm_oracle_cloud_vm_cluster
from . import data_azurerm_oracle_db_nodes
from . import data_azurerm_oracle_db_servers
from . import data_azurerm_oracle_db_system_shapes
from . import data_azurerm_oracle_exadata_infrastructure
from . import data_azurerm_oracle_gi_versions
from . import data_azurerm_orchestrated_virtual_machine_scale_set
from . import data_azurerm_palo_alto_local_rulestack
from . import data_azurerm_platform_image
from . import data_azurerm_policy_assignment
from . import data_azurerm_policy_definition
from . import data_azurerm_policy_definition_built_in
from . import data_azurerm_policy_set_definition
from . import data_azurerm_policy_virtual_machine_configuration_assignment
from . import data_azurerm_portal_dashboard
from . import data_azurerm_postgresql_flexible_server
from . import data_azurerm_postgresql_server
from . import data_azurerm_private_dns_a_record
from . import data_azurerm_private_dns_aaaa_record
from . import data_azurerm_private_dns_cname_record
from . import data_azurerm_private_dns_mx_record
from . import data_azurerm_private_dns_ptr_record
from . import data_azurerm_private_dns_resolver
from . import data_azurerm_private_dns_resolver_dns_forwarding_ruleset
from . import data_azurerm_private_dns_resolver_forwarding_rule
from . import data_azurerm_private_dns_resolver_inbound_endpoint
from . import data_azurerm_private_dns_resolver_outbound_endpoint
from . import data_azurerm_private_dns_resolver_virtual_network_link
from . import data_azurerm_private_dns_soa_record
from . import data_azurerm_private_dns_srv_record
from . import data_azurerm_private_dns_txt_record
from . import data_azurerm_private_dns_zone
from . import data_azurerm_private_dns_zone_virtual_network_link
from . import data_azurerm_private_endpoint_connection
from . import data_azurerm_private_link_service
from . import data_azurerm_private_link_service_endpoint_connections
from . import data_azurerm_proximity_placement_group
from . import data_azurerm_public_ip
from . import data_azurerm_public_ip_prefix
from . import data_azurerm_public_ips
from . import data_azurerm_public_maintenance_configurations
from . import data_azurerm_recovery_services_vault
from . import data_azurerm_redis_cache
from . import data_azurerm_redis_enterprise_database
from . import data_azurerm_resource_group
from . import data_azurerm_resource_group_template_deployment
from . import data_azurerm_resources
from . import data_azurerm_role_assignments
from . import data_azurerm_role_definition
from . import data_azurerm_role_management_policy
from . import data_azurerm_route_filter
from . import data_azurerm_route_table
from . import data_azurerm_search_service
from . import data_azurerm_sentinel_alert_rule
from . import data_azurerm_sentinel_alert_rule_anomaly
from . import data_azurerm_sentinel_alert_rule_template
from . import data_azurerm_service_plan
from . import data_azurerm_servicebus_namespace
from . import data_azurerm_servicebus_namespace_authorization_rule
from . import data_azurerm_servicebus_namespace_disaster_recovery_config
from . import data_azurerm_servicebus_queue
from . import data_azurerm_servicebus_queue_authorization_rule
from . import data_azurerm_servicebus_subscription
from . import data_azurerm_servicebus_topic
from . import data_azurerm_servicebus_topic_authorization_rule
from . import data_azurerm_shared_image
from . import data_azurerm_shared_image_gallery
from . import data_azurerm_shared_image_version
from . import data_azurerm_shared_image_versions
from . import data_azurerm_signalr_service
from . import data_azurerm_site_recovery_fabric
from . import data_azurerm_site_recovery_protection_container
from . import data_azurerm_site_recovery_replication_policy
from . import data_azurerm_site_recovery_replication_recovery_plan
from . import data_azurerm_snapshot
from . import data_azurerm_source_control_token
from . import data_azurerm_spatial_anchors_account
from . import data_azurerm_spring_cloud_app
from . import data_azurerm_spring_cloud_service
from . import data_azurerm_ssh_public_key
from . import data_azurerm_stack_hci_cluster
from . import data_azurerm_stack_hci_storage_path
from . import data_azurerm_static_web_app
from . import data_azurerm_storage_account
from . import data_azurerm_storage_account_blob_container_sas
from . import data_azurerm_storage_account_sas
from . import data_azurerm_storage_blob
from . import data_azurerm_storage_container
from . import data_azurerm_storage_containers
from . import data_azurerm_storage_encryption_scope
from . import data_azurerm_storage_management_policy
from . import data_azurerm_storage_queue
from . import data_azurerm_storage_share
from . import data_azurerm_storage_sync
from . import data_azurerm_storage_sync_group
from . import data_azurerm_storage_table
from . import data_azurerm_storage_table_entities
from . import data_azurerm_storage_table_entity
from . import data_azurerm_stream_analytics_job
from . import data_azurerm_subnet
from . import data_azurerm_subscription
from . import data_azurerm_subscription_template_deployment
from . import data_azurerm_subscriptions
from . import data_azurerm_synapse_workspace
from . import data_azurerm_system_center_virtual_machine_manager_inventory_items
from . import data_azurerm_template_spec_version
from . import data_azurerm_tenant_template_deployment
from . import data_azurerm_traffic_manager_geographical_location
from . import data_azurerm_traffic_manager_profile
from . import data_azurerm_user_assigned_identity
from . import data_azurerm_virtual_desktop_application_group
from . import data_azurerm_virtual_desktop_host_pool
from . import data_azurerm_virtual_desktop_workspace
from . import data_azurerm_virtual_hub
from . import data_azurerm_virtual_hub_connection
from . import data_azurerm_virtual_hub_route_table
from . import data_azurerm_virtual_machine
from . import data_azurerm_virtual_machine_scale_set
from . import data_azurerm_virtual_network
from . import data_azurerm_virtual_network_gateway
from . import data_azurerm_virtual_network_gateway_connection
from . import data_azurerm_virtual_network_peering
from . import data_azurerm_virtual_wan
from . import data_azurerm_vmware_private_cloud
from . import data_azurerm_vpn_gateway
from . import data_azurerm_vpn_server_configuration
from . import data_azurerm_web_application_firewall_policy
from . import data_azurerm_web_pubsub
from . import data_azurerm_web_pubsub_private_link_resource
from . import data_azurerm_windows_function_app
from . import data_azurerm_windows_web_app
from . import data_factory
from . import data_factory_credential_service_principal
from . import data_factory_credential_user_managed_identity
from . import data_factory_custom_dataset
from . import data_factory_data_flow
from . import data_factory_dataset_azure_blob
from . import data_factory_dataset_azure_sql_table
from . import data_factory_dataset_binary
from . import data_factory_dataset_cosmosdb_sqlapi
from . import data_factory_dataset_delimited_text
from . import data_factory_dataset_http
from . import data_factory_dataset_json
from . import data_factory_dataset_mysql
from . import data_factory_dataset_parquet
from . import data_factory_dataset_postgresql
from . import data_factory_dataset_snowflake
from . import data_factory_dataset_sql_server_table
from . import data_factory_flowlet_data_flow
from . import data_factory_integration_runtime_azure
from . import data_factory_integration_runtime_azure_ssis
from . import data_factory_integration_runtime_self_hosted
from . import data_factory_linked_custom_service
from . import data_factory_linked_service_azure_blob_storage
from . import data_factory_linked_service_azure_databricks
from . import data_factory_linked_service_azure_file_storage
from . import data_factory_linked_service_azure_function
from . import data_factory_linked_service_azure_search
from . import data_factory_linked_service_azure_sql_database
from . import data_factory_linked_service_azure_table_storage
from . import data_factory_linked_service_cosmosdb
from . import data_factory_linked_service_cosmosdb_mongoapi
from . import data_factory_linked_service_data_lake_storage_gen2
from . import data_factory_linked_service_key_vault
from . import data_factory_linked_service_kusto
from . import data_factory_linked_service_mysql
from . import data_factory_linked_service_odata
from . import data_factory_linked_service_odbc
from . import data_factory_linked_service_postgresql
from . import data_factory_linked_service_sftp
from . import data_factory_linked_service_snowflake
from . import data_factory_linked_service_sql_server
from . import data_factory_linked_service_synapse
from . import data_factory_linked_service_web
from . import data_factory_managed_private_endpoint
from . import data_factory_pipeline
from . import data_factory_trigger_blob_event
from . import data_factory_trigger_custom_event
from . import data_factory_trigger_schedule
from . import data_factory_trigger_tumbling_window
from . import data_protection_backup_instance_blob_storage
from . import data_protection_backup_instance_disk
from . import data_protection_backup_instance_kubernetes_cluster
from . import data_protection_backup_instance_mysql_flexible_server
from . import data_protection_backup_instance_postgresql
from . import data_protection_backup_instance_postgresql_flexible_server
from . import data_protection_backup_policy_blob_storage
from . import data_protection_backup_policy_disk
from . import data_protection_backup_policy_kubernetes_cluster
from . import data_protection_backup_policy_mysql_flexible_server
from . import data_protection_backup_policy_postgresql
from . import data_protection_backup_policy_postgresql_flexible_server
from . import data_protection_backup_vault
from . import data_protection_backup_vault_customer_managed_key
from . import data_protection_resource_guard
from . import data_share
from . import data_share_account
from . import data_share_dataset_blob_storage
from . import data_share_dataset_data_lake_gen2
from . import data_share_dataset_kusto_cluster
from . import data_share_dataset_kusto_database
from . import database_migration_project
from . import database_migration_service
from . import databox_edge_device
from . import databricks_access_connector
from . import databricks_virtual_network_peering
from . import databricks_workspace
from . import databricks_workspace_customer_managed_key
from . import databricks_workspace_root_dbfs_customer_managed_key
from . import datadog_monitor
from . import datadog_monitor_sso_configuration
from . import datadog_monitor_tag_rule
from . import dedicated_hardware_security_module
from . import dedicated_host
from . import dedicated_host_group
from . import dev_center
from . import dev_center_attached_network
from . import dev_center_catalog
from . import dev_center_dev_box_definition
from . import dev_center_environment_type
from . import dev_center_gallery
from . import dev_center_network_connection
from . import dev_center_project
from . import dev_center_project_environment_type
from . import dev_center_project_pool
from . import dev_test_global_vm_shutdown_schedule
from . import dev_test_lab
from . import dev_test_linux_virtual_machine
from . import dev_test_policy
from . import dev_test_schedule
from . import dev_test_virtual_network
from . import dev_test_windows_virtual_machine
from . import digital_twins_endpoint_eventgrid
from . import digital_twins_endpoint_eventhub
from . import digital_twins_endpoint_servicebus
from . import digital_twins_instance
from . import digital_twins_time_series_database_connection
from . import disk_access
from . import disk_encryption_set
from . import dns_a_record
from . import dns_aaaa_record
from . import dns_caa_record
from . import dns_cname_record
from . import dns_mx_record
from . import dns_ns_record
from . import dns_ptr_record
from . import dns_srv_record
from . import dns_txt_record
from . import dns_zone
from . import dynatrace_monitor
from . import dynatrace_tag_rules
from . import elastic_cloud_elasticsearch
from . import elastic_san
from . import elastic_san_volume
from . import elastic_san_volume_group
from . import email_communication_service
from . import email_communication_service_domain
from . import email_communication_service_domain_sender_username
from . import eventgrid_domain
from . import eventgrid_domain_topic
from . import eventgrid_event_subscription
from . import eventgrid_namespace
from . import eventgrid_partner_configuration
from . import eventgrid_system_topic
from . import eventgrid_system_topic_event_subscription
from . import eventgrid_topic
from . import eventhub
from . import eventhub_authorization_rule
from . import eventhub_cluster
from . import eventhub_consumer_group
from . import eventhub_namespace
from . import eventhub_namespace_authorization_rule
from . import eventhub_namespace_customer_managed_key
from . import eventhub_namespace_disaster_recovery_config
from . import eventhub_namespace_schema_group
from . import express_route_circuit
from . import express_route_circuit_authorization
from . import express_route_circuit_connection
from . import express_route_circuit_peering
from . import express_route_connection
from . import express_route_gateway
from . import express_route_port
from . import express_route_port_authorization
from . import extended_custom_location
from . import extended_location_custom_location
from . import fabric_capacity
from . import federated_identity_credential
from . import firewall
from . import firewall_application_rule_collection
from . import firewall_nat_rule_collection
from . import firewall_network_rule_collection
from . import firewall_policy
from . import firewall_policy_rule_collection_group
from . import fluid_relay_server
from . import frontdoor
from . import frontdoor_custom_https_configuration
from . import frontdoor_firewall_policy
from . import frontdoor_rules_engine
from . import function_app
from . import function_app_active_slot
from . import function_app_connection
from . import function_app_flex_consumption
from . import function_app_function
from . import function_app_hybrid_connection
from . import function_app_slot
from . import gallery_application
from . import gallery_application_version
from . import graph_services_account
from . import hdinsight_hadoop_cluster
from . import hdinsight_hbase_cluster
from . import hdinsight_interactive_query_cluster
from . import hdinsight_kafka_cluster
from . import hdinsight_spark_cluster
from . import healthbot
from . import healthcare_dicom_service
from . import healthcare_fhir_service
from . import healthcare_medtech_service
from . import healthcare_medtech_service_fhir_destination
from . import healthcare_service
from . import healthcare_workspace
from . import hpc_cache
from . import hpc_cache_access_policy
from . import hpc_cache_blob_nfs_target
from . import hpc_cache_blob_target
from . import hpc_cache_nfs_target
from . import image
from . import iot_security_device_group
from . import iot_security_solution
from . import iotcentral_application
from . import iotcentral_application_network_rule_set
from . import iotcentral_organization
from . import iothub
from . import iothub_certificate
from . import iothub_consumer_group
from . import iothub_device_update_account
from . import iothub_device_update_instance
from . import iothub_dps
from . import iothub_dps_certificate
from . import iothub_dps_shared_access_policy
from . import iothub_endpoint_cosmosdb_account
from . import iothub_endpoint_eventhub
from . import iothub_endpoint_servicebus_queue
from . import iothub_endpoint_servicebus_topic
from . import iothub_endpoint_storage_container
from . import iothub_enrichment
from . import iothub_fallback_route
from . import iothub_file_upload
from . import iothub_route
from . import iothub_shared_access_policy
from . import ip_group
from . import ip_group_cidr
from . import key_vault
from . import key_vault_access_policy
from . import key_vault_certificate
from . import key_vault_certificate_contacts
from . import key_vault_certificate_issuer
from . import key_vault_key
from . import key_vault_managed_hardware_security_module
from . import key_vault_managed_hardware_security_module_key
from . import key_vault_managed_hardware_security_module_key_rotation_policy
from . import key_vault_managed_hardware_security_module_role_assignment
from . import key_vault_managed_hardware_security_module_role_definition
from . import key_vault_managed_storage_account
from . import key_vault_managed_storage_account_sas_token_definition
from . import key_vault_secret
from . import kubernetes_cluster
from . import kubernetes_cluster_extension
from . import kubernetes_cluster_node_pool
from . import kubernetes_cluster_trusted_access_role_binding
from . import kubernetes_fleet_manager
from . import kubernetes_fleet_member
from . import kubernetes_fleet_update_run
from . import kubernetes_fleet_update_strategy
from . import kubernetes_flux_configuration
from . import kusto_attached_database_configuration
from . import kusto_cluster
from . import kusto_cluster_customer_managed_key
from . import kusto_cluster_managed_private_endpoint
from . import kusto_cluster_principal_assignment
from . import kusto_cosmosdb_data_connection
from . import kusto_database
from . import kusto_database_principal_assignment
from . import kusto_eventgrid_data_connection
from . import kusto_eventhub_data_connection
from . import kusto_iothub_data_connection
from . import kusto_script
from . import lb
from . import lb_backend_address_pool
from . import lb_backend_address_pool_address
from . import lb_nat_pool
from . import lb_nat_rule
from . import lb_outbound_rule
from . import lb_probe
from . import lb_rule
from . import lighthouse_assignment
from . import lighthouse_definition
from . import linux_function_app
from . import linux_function_app_slot
from . import linux_virtual_machine
from . import linux_virtual_machine_scale_set
from . import linux_web_app
from . import linux_web_app_slot
from . import load_test
from . import local_network_gateway
from . import log_analytics_cluster
from . import log_analytics_cluster_customer_managed_key
from . import log_analytics_data_export_rule
from . import log_analytics_datasource_windows_event
from . import log_analytics_datasource_windows_performance_counter
from . import log_analytics_linked_service
from . import log_analytics_linked_storage_account
from . import log_analytics_query_pack
from . import log_analytics_query_pack_query
from . import log_analytics_saved_search
from . import log_analytics_solution
from . import log_analytics_storage_insights
from . import log_analytics_workspace
from . import log_analytics_workspace_table
from . import logic_app_action_custom
from . import logic_app_action_http
from . import logic_app_integration_account
from . import logic_app_integration_account_agreement
from . import logic_app_integration_account_assembly
from . import logic_app_integration_account_batch_configuration
from . import logic_app_integration_account_certificate
from . import logic_app_integration_account_map
from . import logic_app_integration_account_partner
from . import logic_app_integration_account_schema
from . import logic_app_integration_account_session
from . import logic_app_standard
from . import logic_app_trigger_custom
from . import logic_app_trigger_http_request
from . import logic_app_trigger_recurrence
from . import logic_app_workflow
from . import machine_learning_compute_cluster
from . import machine_learning_compute_instance
from . import machine_learning_datastore_blobstorage
from . import machine_learning_datastore_datalake_gen2
from . import machine_learning_datastore_fileshare
from . import machine_learning_inference_cluster
from . import machine_learning_synapse_spark
from . import machine_learning_workspace
from . import machine_learning_workspace_network_outbound_rule_fqdn
from . import machine_learning_workspace_network_outbound_rule_private_endpoint
from . import machine_learning_workspace_network_outbound_rule_service_tag
from . import maintenance_assignment_dedicated_host
from . import maintenance_assignment_dynamic_scope
from . import maintenance_assignment_virtual_machine
from . import maintenance_assignment_virtual_machine_scale_set
from . import maintenance_configuration
from . import managed_application
from . import managed_application_definition
from . import managed_disk
from . import managed_disk_sas_token
from . import managed_lustre_file_system
from . import management_group
from . import management_group_policy_assignment
from . import management_group_policy_exemption
from . import management_group_policy_remediation
from . import management_group_policy_set_definition
from . import management_group_subscription_association
from . import management_group_template_deployment
from . import management_lock
from . import maps_account
from . import maps_creator
from . import marketplace_agreement
from . import marketplace_role_assignment
from . import mobile_network
from . import mobile_network_attached_data_network
from . import mobile_network_data_network
from . import mobile_network_packet_core_control_plane
from . import mobile_network_packet_core_data_plane
from . import mobile_network_service
from . import mobile_network_sim
from . import mobile_network_sim_group
from . import mobile_network_sim_policy
from . import mobile_network_site
from . import mobile_network_slice
from . import mongo_cluster
from . import monitor_aad_diagnostic_setting
from . import monitor_action_group
from . import monitor_activity_log_alert
from . import monitor_alert_processing_rule_action_group
from . import monitor_alert_processing_rule_suppression
from . import monitor_alert_prometheus_rule_group
from . import monitor_autoscale_setting
from . import monitor_data_collection_endpoint
from . import monitor_data_collection_rule
from . import monitor_data_collection_rule_association
from . import monitor_diagnostic_setting
from . import monitor_metric_alert
from . import monitor_private_link_scope
from . import monitor_private_link_scoped_service
from . import monitor_scheduled_query_rules_alert
from . import monitor_scheduled_query_rules_alert_v2
from . import monitor_scheduled_query_rules_log
from . import monitor_smart_detector_alert_rule
from . import monitor_workspace
from . import mssql_database
from . import mssql_database_extended_auditing_policy
from . import mssql_database_vulnerability_assessment_rule_baseline
from . import mssql_elasticpool
from . import mssql_failover_group
from . import mssql_firewall_rule
from . import mssql_job
from . import mssql_job_agent
from . import mssql_job_credential
from . import mssql_job_schedule
from . import mssql_job_step
from . import mssql_job_target_group
from . import mssql_managed_database
from . import mssql_managed_instance
from . import mssql_managed_instance_active_directory_administrator
from . import mssql_managed_instance_failover_group
from . import mssql_managed_instance_security_alert_policy
from . import mssql_managed_instance_transparent_data_encryption
from . import mssql_managed_instance_vulnerability_assessment
from . import mssql_outbound_firewall_rule
from . import mssql_server
from . import mssql_server_dns_alias
from . import mssql_server_extended_auditing_policy
from . import mssql_server_microsoft_support_auditing_policy
from . import mssql_server_security_alert_policy
from . import mssql_server_transparent_data_encryption
from . import mssql_server_vulnerability_assessment
from . import mssql_virtual_machine
from . import mssql_virtual_machine_availability_group_listener
from . import mssql_virtual_machine_group
from . import mssql_virtual_network_rule
from . import mysql_flexible_database
from . import mysql_flexible_server
from . import mysql_flexible_server_active_directory_administrator
from . import mysql_flexible_server_configuration
from . import mysql_flexible_server_firewall_rule
from . import nat_gateway
from . import nat_gateway_public_ip_association
from . import nat_gateway_public_ip_prefix_association
from . import netapp_account
from . import netapp_account_encryption
from . import netapp_backup_policy
from . import netapp_backup_vault
from . import netapp_pool
from . import netapp_snapshot
from . import netapp_snapshot_policy
from . import netapp_volume
from . import netapp_volume_group_oracle
from . import netapp_volume_group_sap_hana
from . import netapp_volume_quota_rule
from . import network_connection_monitor
from . import network_ddos_protection_plan
from . import network_function_azure_traffic_collector
from . import network_function_collector_policy
from . import network_interface
from . import network_interface_application_gateway_backend_address_pool_association
from . import network_interface_application_security_group_association
from . import network_interface_backend_address_pool_association
from . import network_interface_nat_rule_association
from . import network_interface_security_group_association
from . import network_manager
from . import network_manager_admin_rule
from . import network_manager_admin_rule_collection
from . import network_manager_connectivity_configuration
from . import network_manager_deployment
from . import network_manager_ipam_pool
from . import network_manager_management_group_connection
from . import network_manager_network_group
from . import network_manager_routing_configuration
from . import network_manager_scope_connection
from . import network_manager_security_admin_configuration
from . import network_manager_static_member
from . import network_manager_subscription_connection
from . import network_manager_verifier_workspace
from . import network_packet_capture
from . import network_profile
from . import network_security_group
from . import network_security_rule
from . import network_watcher
from . import network_watcher_flow_log
from . import new_relic_monitor
from . import new_relic_tag_rule
from . import nginx_api_key
from . import nginx_certificate
from . import nginx_configuration
from . import nginx_deployment
from . import notification_hub
from . import notification_hub_authorization_rule
from . import notification_hub_namespace
from . import oracle_autonomous_database
from . import oracle_cloud_vm_cluster
from . import oracle_exadata_infrastructure
from . import orbital_contact
from . import orbital_contact_profile
from . import orbital_spacecraft
from . import orchestrated_virtual_machine_scale_set
from . import palo_alto_local_rulestack
from . import palo_alto_local_rulestack_certificate
from . import palo_alto_local_rulestack_fqdn_list
from . import palo_alto_local_rulestack_outbound_trust_certificate_association
from . import palo_alto_local_rulestack_outbound_untrust_certificate_association
from . import palo_alto_local_rulestack_prefix_list
from . import palo_alto_local_rulestack_rule
from . import palo_alto_next_generation_firewall_virtual_hub_local_rulestack
from . import palo_alto_next_generation_firewall_virtual_hub_panorama
from . import palo_alto_next_generation_firewall_virtual_network_local_rulestack
from . import palo_alto_next_generation_firewall_virtual_network_panorama
from . import palo_alto_virtual_network_appliance
from . import pim_active_role_assignment
from . import pim_eligible_role_assignment
from . import point_to_site_vpn_gateway
from . import policy_definition
from . import policy_set_definition
from . import policy_virtual_machine_configuration_assignment
from . import portal_dashboard
from . import portal_tenant_configuration
from . import postgresql_active_directory_administrator
from . import postgresql_configuration
from . import postgresql_database
from . import postgresql_firewall_rule
from . import postgresql_flexible_server
from . import postgresql_flexible_server_active_directory_administrator
from . import postgresql_flexible_server_configuration
from . import postgresql_flexible_server_database
from . import postgresql_flexible_server_firewall_rule
from . import postgresql_flexible_server_virtual_endpoint
from . import postgresql_server
from . import postgresql_server_key
from . import postgresql_virtual_network_rule
from . import powerbi_embedded
from . import private_dns_a_record
from . import private_dns_aaaa_record
from . import private_dns_cname_record
from . import private_dns_mx_record
from . import private_dns_ptr_record
from . import private_dns_resolver
from . import private_dns_resolver_dns_forwarding_ruleset
from . import private_dns_resolver_forwarding_rule
from . import private_dns_resolver_inbound_endpoint
from . import private_dns_resolver_outbound_endpoint
from . import private_dns_resolver_virtual_network_link
from . import private_dns_srv_record
from . import private_dns_txt_record
from . import private_dns_zone
from . import private_dns_zone_virtual_network_link
from . import private_endpoint
from . import private_endpoint_application_security_group_association
from . import private_link_service
from . import provider
from . import proximity_placement_group
from . import public_ip
from . import public_ip_prefix
from . import purview_account
from . import qumulo_file_system
from . import recovery_services_vault
from . import recovery_services_vault_resource_guard_association
from . import redhat_openshift_cluster
from . import redis_cache
from . import redis_cache_access_policy
from . import redis_cache_access_policy_assignment
from . import redis_enterprise_cluster
from . import redis_enterprise_database
from . import redis_firewall_rule
from . import redis_linked_server
from . import relay_hybrid_connection
from . import relay_hybrid_connection_authorization_rule
from . import relay_namespace
from . import relay_namespace_authorization_rule
from . import resource_deployment_script_azure_cli
from . import resource_deployment_script_azure_power_shell
from . import resource_group
from . import resource_group_cost_management_export
from . import resource_group_cost_management_view
from . import resource_group_policy_assignment
from . import resource_group_policy_exemption
from . import resource_group_policy_remediation
from . import resource_group_template_deployment
from . import resource_management_private_link
from . import resource_management_private_link_association
from . import resource_policy_assignment
from . import resource_policy_exemption
from . import resource_policy_remediation
from . import resource_provider_registration
from . import restore_point_collection
from . import role_assignment
from . import role_definition
from . import role_management_policy
from . import route
from . import route_filter
from . import route_map
from . import route_server
from . import route_server_bgp_connection
from . import route_table
from . import search_service
from . import search_shared_private_link_service
from . import security_center_assessment
from . import security_center_assessment_policy
from . import security_center_auto_provisioning
from . import security_center_automation
from . import security_center_contact
from . import security_center_server_vulnerability_assessment_virtual_machine
from . import security_center_server_vulnerability_assessments_setting
from . import security_center_setting
from . import security_center_storage_defender
from . import security_center_subscription_pricing
from . import security_center_workspace
from . import sentinel_alert_rule_anomaly_built_in
from . import sentinel_alert_rule_anomaly_duplicate
from . import sentinel_alert_rule_fusion
from . import sentinel_alert_rule_machine_learning_behavior_analytics
from . import sentinel_alert_rule_ms_security_incident
from . import sentinel_alert_rule_nrt
from . import sentinel_alert_rule_scheduled
from . import sentinel_alert_rule_threat_intelligence
from . import sentinel_automation_rule
from . import sentinel_data_connector_aws_cloud_trail
from . import sentinel_data_connector_aws_s3
from . import sentinel_data_connector_azure_active_directory
from . import sentinel_data_connector_azure_advanced_threat_protection
from . import sentinel_data_connector_azure_security_center
from . import sentinel_data_connector_dynamics365
from . import sentinel_data_connector_iot
from . import sentinel_data_connector_microsoft_cloud_app_security
from . import sentinel_data_connector_microsoft_defender_advanced_threat_protection
from . import sentinel_data_connector_microsoft_threat_intelligence
from . import sentinel_data_connector_microsoft_threat_protection
from . import sentinel_data_connector_office_atp
from . import sentinel_data_connector_office_irm
from . import sentinel_data_connector_office_power_bi
from . import sentinel_data_connector_office365
from . import sentinel_data_connector_office365_project
from . import sentinel_data_connector_threat_intelligence
from . import sentinel_data_connector_threat_intelligence_taxii
from . import sentinel_log_analytics_workspace_onboarding
from . import sentinel_metadata
from . import sentinel_threat_intelligence_indicator
from . import sentinel_watchlist
from . import sentinel_watchlist_item
from . import service_fabric_cluster
from . import service_fabric_managed_cluster
from . import service_plan
from . import servicebus_namespace
from . import servicebus_namespace_authorization_rule
from . import servicebus_namespace_customer_managed_key
from . import servicebus_namespace_disaster_recovery_config
from . import servicebus_queue
from . import servicebus_queue_authorization_rule
from . import servicebus_subscription
from . import servicebus_subscription_rule
from . import servicebus_topic
from . import servicebus_topic_authorization_rule
from . import shared_image
from . import shared_image_gallery
from . import shared_image_version
from . import signalr_service
from . import signalr_service_custom_certificate
from . import signalr_service_custom_domain
from . import signalr_service_network_acl
from . import signalr_shared_private_link_resource
from . import site_recovery_fabric
from . import site_recovery_hyperv_network_mapping
from . import site_recovery_hyperv_replication_policy
from . import site_recovery_hyperv_replication_policy_association
from . import site_recovery_network_mapping
from . import site_recovery_protection_container
from . import site_recovery_protection_container_mapping
from . import site_recovery_replicated_vm
from . import site_recovery_replication_policy
from . import site_recovery_replication_recovery_plan
from . import site_recovery_services_vault_hyperv_site
from . import site_recovery_vmware_replicated_vm
from . import site_recovery_vmware_replication_policy
from . import site_recovery_vmware_replication_policy_association
from . import snapshot
from . import source_control_token
from . import spatial_anchors_account
from . import spring_cloud_accelerator
from . import spring_cloud_active_deployment
from . import spring_cloud_api_portal
from . import spring_cloud_api_portal_custom_domain
from . import spring_cloud_app
from . import spring_cloud_app_cosmosdb_association
from . import spring_cloud_app_dynamics_application_performance_monitoring
from . import spring_cloud_app_mysql_association
from . import spring_cloud_app_redis_association
from . import spring_cloud_application_insights_application_performance_monitoring
from . import spring_cloud_application_live_view
from . import spring_cloud_build_deployment
from . import spring_cloud_build_pack_binding
from . import spring_cloud_builder
from . import spring_cloud_certificate
from . import spring_cloud_configuration_service
from . import spring_cloud_connection
from . import spring_cloud_container_deployment
from . import spring_cloud_custom_domain
from . import spring_cloud_customized_accelerator
from . import spring_cloud_dev_tool_portal
from . import spring_cloud_dynatrace_application_performance_monitoring
from . import spring_cloud_elastic_application_performance_monitoring
from . import spring_cloud_gateway
from . import spring_cloud_gateway_custom_domain
from . import spring_cloud_gateway_route_config
from . import spring_cloud_java_deployment
from . import spring_cloud_new_relic_application_performance_monitoring
from . import spring_cloud_service
from . import spring_cloud_storage
from . import ssh_public_key
from . import stack_hci_cluster
from . import stack_hci_deployment_setting
from . import stack_hci_extension
from . import stack_hci_logical_network
from . import stack_hci_marketplace_gallery_image
from . import stack_hci_network_interface
from . import stack_hci_storage_path
from . import stack_hci_virtual_hard_disk
from . import static_site
from . import static_site_custom_domain
from . import static_web_app
from . import static_web_app_custom_domain
from . import static_web_app_function_app_registration
from . import storage_account
from . import storage_account_customer_managed_key
from . import storage_account_local_user
from . import storage_account_network_rules
from . import storage_account_queue_properties
from . import storage_account_static_website
from . import storage_blob
from . import storage_blob_inventory_policy
from . import storage_container
from . import storage_container_immutability_policy
from . import storage_data_lake_gen2_filesystem
from . import storage_data_lake_gen2_path
from . import storage_encryption_scope
from . import storage_management_policy
from . import storage_mover
from . import storage_mover_agent
from . import storage_mover_job_definition
from . import storage_mover_project
from . import storage_mover_source_endpoint
from . import storage_mover_target_endpoint
from . import storage_object_replication
from . import storage_queue
from . import storage_share
from . import storage_share_directory
from . import storage_share_file
from . import storage_sync
from . import storage_sync_cloud_endpoint
from . import storage_sync_group
from . import storage_sync_server_endpoint
from . import storage_table
from . import storage_table_entity
from . import stream_analytics_cluster
from . import stream_analytics_function_javascript_uda
from . import stream_analytics_function_javascript_udf
from . import stream_analytics_job
from . import stream_analytics_job_schedule
from . import stream_analytics_job_storage_account
from . import stream_analytics_managed_private_endpoint
from . import stream_analytics_output_blob
from . import stream_analytics_output_cosmosdb
from . import stream_analytics_output_eventhub
from . import stream_analytics_output_function
from . import stream_analytics_output_mssql
from . import stream_analytics_output_powerbi
from . import stream_analytics_output_servicebus_queue
from . import stream_analytics_output_servicebus_topic
from . import stream_analytics_output_synapse
from . import stream_analytics_output_table
from . import stream_analytics_reference_input_blob
from . import stream_analytics_reference_input_mssql
from . import stream_analytics_stream_input_blob
from . import stream_analytics_stream_input_eventhub
from . import stream_analytics_stream_input_eventhub_v2
from . import stream_analytics_stream_input_iothub
from . import subnet
from . import subnet_nat_gateway_association
from . import subnet_network_security_group_association
from . import subnet_route_table_association
from . import subnet_service_endpoint_storage_policy
from . import subscription
from . import subscription_cost_management_export
from . import subscription_cost_management_view
from . import subscription_policy_assignment
from . import subscription_policy_exemption
from . import subscription_policy_remediation
from . import subscription_template_deployment
from . import synapse_firewall_rule
from . import synapse_integration_runtime_azure
from . import synapse_integration_runtime_self_hosted
from . import synapse_linked_service
from . import synapse_managed_private_endpoint
from . import synapse_private_link_hub
from . import synapse_role_assignment
from . import synapse_spark_pool
from . import synapse_sql_pool
from . import synapse_sql_pool_extended_auditing_policy
from . import synapse_sql_pool_security_alert_policy
from . import synapse_sql_pool_vulnerability_assessment
from . import synapse_sql_pool_vulnerability_assessment_baseline
from . import synapse_sql_pool_workload_classifier
from . import synapse_sql_pool_workload_group
from . import synapse_workspace
from . import synapse_workspace_aad_admin
from . import synapse_workspace_extended_auditing_policy
from . import synapse_workspace_key
from . import synapse_workspace_security_alert_policy
from . import synapse_workspace_sql_aad_admin
from . import synapse_workspace_vulnerability_assessment
from . import system_center_virtual_machine_manager_availability_set
from . import system_center_virtual_machine_manager_cloud
from . import system_center_virtual_machine_manager_server
from . import system_center_virtual_machine_manager_virtual_machine_instance
from . import system_center_virtual_machine_manager_virtual_machine_instance_guest_agent
from . import system_center_virtual_machine_manager_virtual_machine_template
from . import system_center_virtual_machine_manager_virtual_network
from . import tenant_template_deployment
from . import traffic_manager_azure_endpoint
from . import traffic_manager_external_endpoint
from . import traffic_manager_nested_endpoint
from . import traffic_manager_profile
from . import trusted_signing_account
from . import user_assigned_identity
from . import video_indexer_account
from . import virtual_desktop_application
from . import virtual_desktop_application_group
from . import virtual_desktop_host_pool
from . import virtual_desktop_host_pool_registration_info
from . import virtual_desktop_scaling_plan
from . import virtual_desktop_scaling_plan_host_pool_association
from . import virtual_desktop_workspace
from . import virtual_desktop_workspace_application_group_association
from . import virtual_hub
from . import virtual_hub_bgp_connection
from . import virtual_hub_connection
from . import virtual_hub_ip
from . import virtual_hub_route_table
from . import virtual_hub_route_table_route
from . import virtual_hub_routing_intent
from . import virtual_hub_security_partner_provider
from . import virtual_machine
from . import virtual_machine_automanage_configuration_assignment
from . import virtual_machine_data_disk_attachment
from . import virtual_machine_extension
from . import virtual_machine_gallery_application_assignment
from . import virtual_machine_implicit_data_disk_from_source
from . import virtual_machine_packet_capture
from . import virtual_machine_restore_point
from . import virtual_machine_restore_point_collection
from . import virtual_machine_run_command
from . import virtual_machine_scale_set
from . import virtual_machine_scale_set_extension
from . import virtual_machine_scale_set_packet_capture
from . import virtual_machine_scale_set_standby_pool
from . import virtual_network
from . import virtual_network_dns_servers
from . import virtual_network_gateway
from . import virtual_network_gateway_connection
from . import virtual_network_gateway_nat_rule
from . import virtual_network_peering
from . import virtual_wan
from . import vmware_cluster
from . import vmware_express_route_authorization
from . import vmware_netapp_volume_attachment
from . import vmware_private_cloud
from . import voice_services_communications_gateway
from . import voice_services_communications_gateway_test_line
from . import vpn_gateway
from . import vpn_gateway_connection
from . import vpn_gateway_nat_rule
from . import vpn_server_configuration
from . import vpn_server_configuration_policy_group
from . import vpn_site
from . import web_app_active_slot
from . import web_app_hybrid_connection
from . import web_application_firewall_policy
from . import web_pubsub
from . import web_pubsub_custom_certificate
from . import web_pubsub_custom_domain
from . import web_pubsub_hub
from . import web_pubsub_network_acl
from . import web_pubsub_shared_private_link_resource
from . import web_pubsub_socketio
from . import windows_function_app
from . import windows_function_app_slot
from . import windows_virtual_machine
from . import windows_virtual_machine_scale_set
from . import windows_web_app
from . import windows_web_app_slot
from . import workloads_sap_discovery_virtual_instance
from . import workloads_sap_single_node_virtual_instance
from . import workloads_sap_three_tier_virtual_instance
