r'''
# CDKTF prebuilt bindings for hashicorp/google-beta provider version 6.39.0

This repo builds and publishes the [Terraform google-beta provider](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-google-beta](https://www.npmjs.com/package/@cdktf/provider-google-beta).

`npm install @cdktf/provider-google-beta`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-google_beta](https://pypi.org/project/cdktf-cdktf-provider-google_beta).

`pipenv install cdktf-cdktf-provider-google_beta`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.GoogleBeta](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.GoogleBeta).

`dotnet add package HashiCorp.Cdktf.Providers.GoogleBeta`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-google-beta](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-google-beta).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-google-beta</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-googlebeta-go`](https://github.com/cdktf/cdktf-provider-googlebeta-go) package.

`go get github.com/cdktf/cdktf-provider-googlebeta-go/googlebeta/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-googlebeta-go/blob/main/googlebeta/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-google-beta).

## Versioning

This project is explicitly not tracking the Terraform google-beta provider version 1:1. In fact, it always tracks `latest` of `~> 6.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform google-beta provider](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0)
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
    "data_google_access_approval_folder_service_account",
    "data_google_access_approval_organization_service_account",
    "data_google_access_approval_project_service_account",
    "data_google_access_context_manager_access_policy",
    "data_google_access_context_manager_access_policy_iam_policy",
    "data_google_active_folder",
    "data_google_alloydb_cluster",
    "data_google_alloydb_instance",
    "data_google_alloydb_locations",
    "data_google_alloydb_supported_database_flags",
    "data_google_api_gateway_api_config_iam_policy",
    "data_google_api_gateway_api_iam_policy",
    "data_google_api_gateway_gateway_iam_policy",
    "data_google_apigee_environment_iam_policy",
    "data_google_app_engine_default_service_account",
    "data_google_apphub_application",
    "data_google_apphub_discovered_service",
    "data_google_apphub_discovered_workload",
    "data_google_artifact_registry_docker_image",
    "data_google_artifact_registry_locations",
    "data_google_artifact_registry_repository",
    "data_google_artifact_registry_repository_iam_policy",
    "data_google_backup_dr_backup",
    "data_google_backup_dr_backup_plan",
    "data_google_backup_dr_backup_plan_association",
    "data_google_backup_dr_backup_vault",
    "data_google_backup_dr_data_source",
    "data_google_backup_dr_management_server",
    "data_google_beyondcorp_app_connection",
    "data_google_beyondcorp_app_connector",
    "data_google_beyondcorp_app_gateway",
    "data_google_beyondcorp_application_iam_policy",
    "data_google_beyondcorp_security_gateway",
    "data_google_beyondcorp_security_gateway_application_iam_policy",
    "data_google_beyondcorp_security_gateway_iam_policy",
    "data_google_bigquery_analytics_hub_data_exchange_iam_policy",
    "data_google_bigquery_analytics_hub_listing_iam_policy",
    "data_google_bigquery_connection_iam_policy",
    "data_google_bigquery_datapolicy_data_policy_iam_policy",
    "data_google_bigquery_dataset",
    "data_google_bigquery_dataset_iam_policy",
    "data_google_bigquery_datasets",
    "data_google_bigquery_default_service_account",
    "data_google_bigquery_table",
    "data_google_bigquery_table_iam_policy",
    "data_google_bigquery_tables",
    "data_google_bigtable_instance_iam_policy",
    "data_google_bigtable_table_iam_policy",
    "data_google_billing_account",
    "data_google_billing_account_iam_policy",
    "data_google_binary_authorization_attestor_iam_policy",
    "data_google_certificate_manager_certificate_map",
    "data_google_certificate_manager_certificates",
    "data_google_client_config",
    "data_google_client_openid_userinfo",
    "data_google_cloud_asset_resources_search_all",
    "data_google_cloud_asset_search_all_resources",
    "data_google_cloud_identity_group_lookup",
    "data_google_cloud_identity_group_memberships",
    "data_google_cloud_identity_group_transitive_memberships",
    "data_google_cloud_identity_groups",
    "data_google_cloud_quotas_quota_info",
    "data_google_cloud_quotas_quota_infos",
    "data_google_cloud_run_locations",
    "data_google_cloud_run_service",
    "data_google_cloud_run_service_iam_policy",
    "data_google_cloud_run_v2_job",
    "data_google_cloud_run_v2_job_iam_policy",
    "data_google_cloud_run_v2_service",
    "data_google_cloud_run_v2_service_iam_policy",
    "data_google_cloud_run_v2_worker_pool",
    "data_google_cloud_run_v2_worker_pool_iam_policy",
    "data_google_cloud_tasks_queue_iam_policy",
    "data_google_cloudbuild_trigger",
    "data_google_cloudbuildv2_connection_iam_policy",
    "data_google_clouddeploy_custom_target_type_iam_policy",
    "data_google_clouddeploy_delivery_pipeline_iam_policy",
    "data_google_clouddeploy_target_iam_policy",
    "data_google_cloudfunctions2_function",
    "data_google_cloudfunctions2_function_iam_policy",
    "data_google_cloudfunctions_function",
    "data_google_cloudfunctions_function_iam_policy",
    "data_google_colab_runtime_template_iam_policy",
    "data_google_composer_environment",
    "data_google_composer_image_versions",
    "data_google_composer_user_workloads_config_map",
    "data_google_composer_user_workloads_secret",
    "data_google_compute_address",
    "data_google_compute_addresses",
    "data_google_compute_backend_bucket",
    "data_google_compute_backend_bucket_iam_policy",
    "data_google_compute_backend_service",
    "data_google_compute_backend_service_iam_policy",
    "data_google_compute_default_service_account",
    "data_google_compute_disk",
    "data_google_compute_disk_iam_policy",
    "data_google_compute_forwarding_rule",
    "data_google_compute_forwarding_rules",
    "data_google_compute_global_address",
    "data_google_compute_global_forwarding_rule",
    "data_google_compute_ha_vpn_gateway",
    "data_google_compute_health_check",
    "data_google_compute_image",
    "data_google_compute_image_iam_policy",
    "data_google_compute_images",
    "data_google_compute_instance",
    "data_google_compute_instance_group",
    "data_google_compute_instance_group_manager",
    "data_google_compute_instance_guest_attributes",
    "data_google_compute_instance_iam_policy",
    "data_google_compute_instance_serial_port",
    "data_google_compute_instance_template",
    "data_google_compute_instance_template_iam_policy",
    "data_google_compute_instant_snapshot_iam_policy",
    "data_google_compute_lb_ip_ranges",
    "data_google_compute_machine_image_iam_policy",
    "data_google_compute_machine_types",
    "data_google_compute_network",
    "data_google_compute_network_endpoint_group",
    "data_google_compute_network_peering",
    "data_google_compute_networks",
    "data_google_compute_node_types",
    "data_google_compute_region_backend_service",
    "data_google_compute_region_backend_service_iam_policy",
    "data_google_compute_region_disk",
    "data_google_compute_region_disk_iam_policy",
    "data_google_compute_region_instance_group",
    "data_google_compute_region_instance_group_manager",
    "data_google_compute_region_instance_template",
    "data_google_compute_region_network_endpoint_group",
    "data_google_compute_region_ssl_certificate",
    "data_google_compute_region_ssl_policy",
    "data_google_compute_regions",
    "data_google_compute_reservation",
    "data_google_compute_resource_policy",
    "data_google_compute_router",
    "data_google_compute_router_nat",
    "data_google_compute_router_status",
    "data_google_compute_security_policy",
    "data_google_compute_snapshot",
    "data_google_compute_snapshot_iam_policy",
    "data_google_compute_ssl_certificate",
    "data_google_compute_ssl_policy",
    "data_google_compute_storage_pool_iam_policy",
    "data_google_compute_storage_pool_types",
    "data_google_compute_subnetwork",
    "data_google_compute_subnetwork_iam_policy",
    "data_google_compute_subnetworks",
    "data_google_compute_vpn_gateway",
    "data_google_compute_zones",
    "data_google_container_analysis_note_iam_policy",
    "data_google_container_attached_install_manifest",
    "data_google_container_attached_versions",
    "data_google_container_aws_versions",
    "data_google_container_azure_versions",
    "data_google_container_cluster",
    "data_google_container_engine_versions",
    "data_google_container_registry_image",
    "data_google_container_registry_repository",
    "data_google_data_catalog_entry_group_iam_policy",
    "data_google_data_catalog_policy_tag_iam_policy",
    "data_google_data_catalog_tag_template_iam_policy",
    "data_google_data_catalog_taxonomy_iam_policy",
    "data_google_data_fusion_instance_iam_policy",
    "data_google_dataform_repository_iam_policy",
    "data_google_dataplex_aspect_type_iam_policy",
    "data_google_dataplex_asset_iam_policy",
    "data_google_dataplex_datascan_iam_policy",
    "data_google_dataplex_entry_group_iam_policy",
    "data_google_dataplex_entry_type_iam_policy",
    "data_google_dataplex_glossary_iam_policy",
    "data_google_dataplex_lake_iam_policy",
    "data_google_dataplex_task_iam_policy",
    "data_google_dataplex_zone_iam_policy",
    "data_google_dataproc_autoscaling_policy_iam_policy",
    "data_google_dataproc_cluster_iam_policy",
    "data_google_dataproc_job_iam_policy",
    "data_google_dataproc_metastore_database_iam_policy",
    "data_google_dataproc_metastore_federation_iam_policy",
    "data_google_dataproc_metastore_service",
    "data_google_dataproc_metastore_service_iam_policy",
    "data_google_dataproc_metastore_table_iam_policy",
    "data_google_datastream_static_ips",
    "data_google_dns_keys",
    "data_google_dns_managed_zone",
    "data_google_dns_managed_zone_iam_policy",
    "data_google_dns_managed_zones",
    "data_google_dns_record_set",
    "data_google_endpoints_service_consumers_iam_policy",
    "data_google_endpoints_service_iam_policy",
    "data_google_filestore_instance",
    "data_google_firebase_android_app",
    "data_google_firebase_android_app_config",
    "data_google_firebase_apple_app",
    "data_google_firebase_apple_app_config",
    "data_google_firebase_hosting_channel",
    "data_google_firebase_web_app",
    "data_google_firebase_web_app_config",
    "data_google_folder",
    "data_google_folder_iam_policy",
    "data_google_folder_organization_policy",
    "data_google_folders",
    "data_google_gemini_repository_group_iam_policy",
    "data_google_gke_backup_backup_plan_iam_policy",
    "data_google_gke_backup_restore_plan_iam_policy",
    "data_google_gke_hub_feature",
    "data_google_gke_hub_feature_iam_policy",
    "data_google_gke_hub_membership",
    "data_google_gke_hub_membership_binding",
    "data_google_gke_hub_membership_iam_policy",
    "data_google_gke_hub_scope_iam_policy",
    "data_google_healthcare_consent_store_iam_policy",
    "data_google_healthcare_dataset_iam_policy",
    "data_google_healthcare_dicom_store_iam_policy",
    "data_google_healthcare_fhir_store_iam_policy",
    "data_google_healthcare_hl7_v2_store_iam_policy",
    "data_google_iam_policy",
    "data_google_iam_role",
    "data_google_iam_testable_permissions",
    "data_google_iam_workload_identity_pool",
    "data_google_iam_workload_identity_pool_iam_policy",
    "data_google_iam_workload_identity_pool_provider",
    "data_google_iap_app_engine_service_iam_policy",
    "data_google_iap_app_engine_version_iam_policy",
    "data_google_iap_client",
    "data_google_iap_tunnel_dest_group_iam_policy",
    "data_google_iap_tunnel_iam_policy",
    "data_google_iap_tunnel_instance_iam_policy",
    "data_google_iap_web_backend_service_iam_policy",
    "data_google_iap_web_cloud_run_service_iam_policy",
    "data_google_iap_web_iam_policy",
    "data_google_iap_web_region_backend_service_iam_policy",
    "data_google_iap_web_type_app_engine_iam_policy",
    "data_google_iap_web_type_compute_iam_policy",
    "data_google_kms_autokey_config",
    "data_google_kms_crypto_key",
    "data_google_kms_crypto_key_iam_policy",
    "data_google_kms_crypto_key_latest_version",
    "data_google_kms_crypto_key_version",
    "data_google_kms_crypto_key_versions",
    "data_google_kms_crypto_keys",
    "data_google_kms_ekm_connection_iam_policy",
    "data_google_kms_key_handle",
    "data_google_kms_key_handles",
    "data_google_kms_key_ring",
    "data_google_kms_key_ring_iam_policy",
    "data_google_kms_key_rings",
    "data_google_kms_secret",
    "data_google_kms_secret_asymmetric",
    "data_google_kms_secret_ciphertext",
    "data_google_logging_folder_settings",
    "data_google_logging_log_view_iam_policy",
    "data_google_logging_organization_settings",
    "data_google_logging_project_cmek_settings",
    "data_google_logging_project_settings",
    "data_google_logging_sink",
    "data_google_lustre_instance",
    "data_google_memcache_instance",
    "data_google_memorystore_instance",
    "data_google_monitoring_app_engine_service",
    "data_google_monitoring_cluster_istio_service",
    "data_google_monitoring_istio_canonical_service",
    "data_google_monitoring_mesh_istio_service",
    "data_google_monitoring_notification_channel",
    "data_google_monitoring_uptime_check_ips",
    "data_google_netblock_ip_ranges",
    "data_google_network_security_address_group_iam_policy",
    "data_google_notebooks_instance_iam_policy",
    "data_google_notebooks_runtime_iam_policy",
    "data_google_oracle_database_autonomous_database",
    "data_google_oracle_database_autonomous_databases",
    "data_google_oracle_database_cloud_exadata_infrastructure",
    "data_google_oracle_database_cloud_exadata_infrastructures",
    "data_google_oracle_database_cloud_vm_cluster",
    "data_google_oracle_database_cloud_vm_clusters",
    "data_google_oracle_database_db_nodes",
    "data_google_oracle_database_db_servers",
    "data_google_organization",
    "data_google_organization_iam_custom_role",
    "data_google_organization_iam_custom_roles",
    "data_google_organization_iam_policy",
    "data_google_organizations",
    "data_google_parameter_manager_parameter",
    "data_google_parameter_manager_parameter_version",
    "data_google_parameter_manager_parameter_version_render",
    "data_google_parameter_manager_parameters",
    "data_google_parameter_manager_regional_parameter",
    "data_google_parameter_manager_regional_parameter_version",
    "data_google_parameter_manager_regional_parameter_version_render",
    "data_google_parameter_manager_regional_parameters",
    "data_google_privateca_ca_pool_iam_policy",
    "data_google_privateca_certificate_authority",
    "data_google_privateca_certificate_template_iam_policy",
    "data_google_privileged_access_manager_entitlement",
    "data_google_project",
    "data_google_project_ancestry",
    "data_google_project_iam_custom_role",
    "data_google_project_iam_custom_roles",
    "data_google_project_iam_policy",
    "data_google_project_organization_policy",
    "data_google_project_service",
    "data_google_projects",
    "data_google_pubsub_schema_iam_policy",
    "data_google_pubsub_subscription",
    "data_google_pubsub_subscription_iam_policy",
    "data_google_pubsub_topic",
    "data_google_pubsub_topic_iam_policy",
    "data_google_redis_instance",
    "data_google_runtimeconfig_config",
    "data_google_runtimeconfig_config_iam_policy",
    "data_google_runtimeconfig_variable",
    "data_google_scc_source_iam_policy",
    "data_google_scc_v2_organization_source_iam_policy",
    "data_google_secret_manager_regional_secret",
    "data_google_secret_manager_regional_secret_iam_policy",
    "data_google_secret_manager_regional_secret_version",
    "data_google_secret_manager_regional_secret_version_access",
    "data_google_secret_manager_regional_secrets",
    "data_google_secret_manager_secret",
    "data_google_secret_manager_secret_iam_policy",
    "data_google_secret_manager_secret_version",
    "data_google_secret_manager_secret_version_access",
    "data_google_secret_manager_secrets",
    "data_google_secure_source_manager_instance_iam_policy",
    "data_google_secure_source_manager_repository_iam_policy",
    "data_google_service_account",
    "data_google_service_account_access_token",
    "data_google_service_account_iam_policy",
    "data_google_service_account_id_token",
    "data_google_service_account_jwt",
    "data_google_service_account_key",
    "data_google_service_accounts",
    "data_google_service_directory_namespace_iam_policy",
    "data_google_service_directory_service_iam_policy",
    "data_google_service_networking_peered_dns_domain",
    "data_google_site_verification_token",
    "data_google_sourcerepo_repository",
    "data_google_sourcerepo_repository_iam_policy",
    "data_google_spanner_database",
    "data_google_spanner_database_iam_policy",
    "data_google_spanner_instance",
    "data_google_spanner_instance_iam_policy",
    "data_google_sql_backup_run",
    "data_google_sql_ca_certs",
    "data_google_sql_database",
    "data_google_sql_database_instance",
    "data_google_sql_database_instance_latest_recovery_time",
    "data_google_sql_database_instances",
    "data_google_sql_databases",
    "data_google_sql_tiers",
    "data_google_storage_bucket",
    "data_google_storage_bucket_iam_policy",
    "data_google_storage_bucket_object",
    "data_google_storage_bucket_object_content",
    "data_google_storage_bucket_objects",
    "data_google_storage_buckets",
    "data_google_storage_control_folder_intelligence_config",
    "data_google_storage_control_organization_intelligence_config",
    "data_google_storage_control_project_intelligence_config",
    "data_google_storage_managed_folder_iam_policy",
    "data_google_storage_object_signed_url",
    "data_google_storage_project_service_account",
    "data_google_storage_transfer_project_service_account",
    "data_google_tags_tag_key",
    "data_google_tags_tag_key_iam_policy",
    "data_google_tags_tag_keys",
    "data_google_tags_tag_value",
    "data_google_tags_tag_value_iam_policy",
    "data_google_tags_tag_values",
    "data_google_tpu_tensorflow_versions",
    "data_google_tpu_v2_accelerator_types",
    "data_google_tpu_v2_runtime_versions",
    "data_google_vertex_ai_endpoint_iam_policy",
    "data_google_vertex_ai_feature_group_iam_policy",
    "data_google_vertex_ai_feature_online_store_featureview_iam_policy",
    "data_google_vertex_ai_feature_online_store_iam_policy",
    "data_google_vertex_ai_featurestore_entitytype_iam_policy",
    "data_google_vertex_ai_featurestore_iam_policy",
    "data_google_vertex_ai_index",
    "data_google_vmwareengine_cluster",
    "data_google_vmwareengine_external_access_rule",
    "data_google_vmwareengine_external_address",
    "data_google_vmwareengine_network",
    "data_google_vmwareengine_network_peering",
    "data_google_vmwareengine_network_policy",
    "data_google_vmwareengine_nsx_credentials",
    "data_google_vmwareengine_private_cloud",
    "data_google_vmwareengine_subnet",
    "data_google_vmwareengine_vcenter_credentials",
    "data_google_vpc_access_connector",
    "data_google_workbench_instance_iam_policy",
    "data_google_workstations_workstation_config_iam_policy",
    "data_google_workstations_workstation_iam_policy",
    "google_access_context_manager_access_level",
    "google_access_context_manager_access_level_condition",
    "google_access_context_manager_access_levels",
    "google_access_context_manager_access_policy",
    "google_access_context_manager_access_policy_iam_binding",
    "google_access_context_manager_access_policy_iam_member",
    "google_access_context_manager_access_policy_iam_policy",
    "google_access_context_manager_authorized_orgs_desc",
    "google_access_context_manager_egress_policy",
    "google_access_context_manager_gcp_user_access_binding",
    "google_access_context_manager_ingress_policy",
    "google_access_context_manager_service_perimeter",
    "google_access_context_manager_service_perimeter_dry_run_egress_policy",
    "google_access_context_manager_service_perimeter_dry_run_ingress_policy",
    "google_access_context_manager_service_perimeter_dry_run_resource",
    "google_access_context_manager_service_perimeter_egress_policy",
    "google_access_context_manager_service_perimeter_ingress_policy",
    "google_access_context_manager_service_perimeter_resource",
    "google_access_context_manager_service_perimeters",
    "google_active_directory_domain",
    "google_active_directory_domain_trust",
    "google_active_directory_peering",
    "google_alloydb_backup",
    "google_alloydb_cluster",
    "google_alloydb_instance",
    "google_alloydb_user",
    "google_api_gateway_api",
    "google_api_gateway_api_config",
    "google_api_gateway_api_config_iam_binding",
    "google_api_gateway_api_config_iam_member",
    "google_api_gateway_api_config_iam_policy",
    "google_api_gateway_api_iam_binding",
    "google_api_gateway_api_iam_member",
    "google_api_gateway_api_iam_policy",
    "google_api_gateway_gateway",
    "google_api_gateway_gateway_iam_binding",
    "google_api_gateway_gateway_iam_member",
    "google_api_gateway_gateway_iam_policy",
    "google_apigee_addons_config",
    "google_apigee_api",
    "google_apigee_app_group",
    "google_apigee_control_plane_access",
    "google_apigee_developer",
    "google_apigee_dns_zone",
    "google_apigee_endpoint_attachment",
    "google_apigee_env_keystore",
    "google_apigee_env_references",
    "google_apigee_envgroup",
    "google_apigee_envgroup_attachment",
    "google_apigee_environment",
    "google_apigee_environment_addons_config",
    "google_apigee_environment_iam_binding",
    "google_apigee_environment_iam_member",
    "google_apigee_environment_iam_policy",
    "google_apigee_environment_keyvaluemaps",
    "google_apigee_environment_keyvaluemaps_entries",
    "google_apigee_flowhook",
    "google_apigee_instance",
    "google_apigee_instance_attachment",
    "google_apigee_keystores_aliases_key_cert_file",
    "google_apigee_keystores_aliases_pkcs12",
    "google_apigee_keystores_aliases_self_signed_cert",
    "google_apigee_nat_address",
    "google_apigee_organization",
    "google_apigee_security_monitoring_condition",
    "google_apigee_security_profile_v2",
    "google_apigee_sharedflow",
    "google_apigee_sharedflow_deployment",
    "google_apigee_sync_authorization",
    "google_apigee_target_server",
    "google_apihub_api_hub_instance",
    "google_apihub_curation",
    "google_apihub_host_project_registration",
    "google_apikeys_key",
    "google_app_engine_application",
    "google_app_engine_application_url_dispatch_rules",
    "google_app_engine_domain_mapping",
    "google_app_engine_firewall_rule",
    "google_app_engine_flexible_app_version",
    "google_app_engine_service_network_settings",
    "google_app_engine_service_split_traffic",
    "google_app_engine_standard_app_version",
    "google_apphub_application",
    "google_apphub_service",
    "google_apphub_service_project_attachment",
    "google_apphub_workload",
    "google_artifact_registry_repository",
    "google_artifact_registry_repository_iam_binding",
    "google_artifact_registry_repository_iam_member",
    "google_artifact_registry_repository_iam_policy",
    "google_artifact_registry_vpcsc_config",
    "google_assured_workloads_workload",
    "google_backup_dr_backup_plan",
    "google_backup_dr_backup_plan_association",
    "google_backup_dr_backup_vault",
    "google_backup_dr_management_server",
    "google_beyondcorp_app_connection",
    "google_beyondcorp_app_connector",
    "google_beyondcorp_app_gateway",
    "google_beyondcorp_application",
    "google_beyondcorp_application_iam_binding",
    "google_beyondcorp_application_iam_member",
    "google_beyondcorp_application_iam_policy",
    "google_beyondcorp_security_gateway",
    "google_beyondcorp_security_gateway_application",
    "google_beyondcorp_security_gateway_application_iam_binding",
    "google_beyondcorp_security_gateway_application_iam_member",
    "google_beyondcorp_security_gateway_application_iam_policy",
    "google_beyondcorp_security_gateway_iam_binding",
    "google_beyondcorp_security_gateway_iam_member",
    "google_beyondcorp_security_gateway_iam_policy",
    "google_biglake_catalog",
    "google_biglake_database",
    "google_biglake_table",
    "google_bigquery_analytics_hub_data_exchange",
    "google_bigquery_analytics_hub_data_exchange_iam_binding",
    "google_bigquery_analytics_hub_data_exchange_iam_member",
    "google_bigquery_analytics_hub_data_exchange_iam_policy",
    "google_bigquery_analytics_hub_listing",
    "google_bigquery_analytics_hub_listing_iam_binding",
    "google_bigquery_analytics_hub_listing_iam_member",
    "google_bigquery_analytics_hub_listing_iam_policy",
    "google_bigquery_analytics_hub_listing_subscription",
    "google_bigquery_bi_reservation",
    "google_bigquery_capacity_commitment",
    "google_bigquery_connection",
    "google_bigquery_connection_iam_binding",
    "google_bigquery_connection_iam_member",
    "google_bigquery_connection_iam_policy",
    "google_bigquery_data_transfer_config",
    "google_bigquery_datapolicy_data_policy",
    "google_bigquery_datapolicy_data_policy_iam_binding",
    "google_bigquery_datapolicy_data_policy_iam_member",
    "google_bigquery_datapolicy_data_policy_iam_policy",
    "google_bigquery_dataset",
    "google_bigquery_dataset_access",
    "google_bigquery_dataset_iam_binding",
    "google_bigquery_dataset_iam_member",
    "google_bigquery_dataset_iam_policy",
    "google_bigquery_job",
    "google_bigquery_reservation",
    "google_bigquery_reservation_assignment",
    "google_bigquery_routine",
    "google_bigquery_row_access_policy",
    "google_bigquery_table",
    "google_bigquery_table_iam_binding",
    "google_bigquery_table_iam_member",
    "google_bigquery_table_iam_policy",
    "google_bigtable_app_profile",
    "google_bigtable_authorized_view",
    "google_bigtable_gc_policy",
    "google_bigtable_instance",
    "google_bigtable_instance_iam_binding",
    "google_bigtable_instance_iam_member",
    "google_bigtable_instance_iam_policy",
    "google_bigtable_logical_view",
    "google_bigtable_materialized_view",
    "google_bigtable_table",
    "google_bigtable_table_iam_binding",
    "google_bigtable_table_iam_member",
    "google_bigtable_table_iam_policy",
    "google_billing_account_iam_binding",
    "google_billing_account_iam_member",
    "google_billing_account_iam_policy",
    "google_billing_budget",
    "google_billing_project_info",
    "google_billing_subaccount",
    "google_binary_authorization_attestor",
    "google_binary_authorization_attestor_iam_binding",
    "google_binary_authorization_attestor_iam_member",
    "google_binary_authorization_attestor_iam_policy",
    "google_binary_authorization_policy",
    "google_blockchain_node_engine_blockchain_nodes",
    "google_certificate_manager_certificate",
    "google_certificate_manager_certificate_issuance_config",
    "google_certificate_manager_certificate_map",
    "google_certificate_manager_certificate_map_entry",
    "google_certificate_manager_dns_authorization",
    "google_certificate_manager_trust_config",
    "google_chronicle_data_access_label",
    "google_chronicle_data_access_scope",
    "google_chronicle_reference_list",
    "google_chronicle_retrohunt",
    "google_chronicle_rule",
    "google_chronicle_rule_deployment",
    "google_chronicle_watchlist",
    "google_cloud_asset_folder_feed",
    "google_cloud_asset_organization_feed",
    "google_cloud_asset_project_feed",
    "google_cloud_identity_group",
    "google_cloud_identity_group_membership",
    "google_cloud_ids_endpoint",
    "google_cloud_quotas_quota_adjuster_settings",
    "google_cloud_quotas_quota_preference",
    "google_cloud_run_domain_mapping",
    "google_cloud_run_service",
    "google_cloud_run_service_iam_binding",
    "google_cloud_run_service_iam_member",
    "google_cloud_run_service_iam_policy",
    "google_cloud_run_v2_job",
    "google_cloud_run_v2_job_iam_binding",
    "google_cloud_run_v2_job_iam_member",
    "google_cloud_run_v2_job_iam_policy",
    "google_cloud_run_v2_service",
    "google_cloud_run_v2_service_iam_binding",
    "google_cloud_run_v2_service_iam_member",
    "google_cloud_run_v2_service_iam_policy",
    "google_cloud_run_v2_worker_pool",
    "google_cloud_run_v2_worker_pool_iam_binding",
    "google_cloud_run_v2_worker_pool_iam_member",
    "google_cloud_run_v2_worker_pool_iam_policy",
    "google_cloud_scheduler_job",
    "google_cloud_tasks_queue",
    "google_cloud_tasks_queue_iam_binding",
    "google_cloud_tasks_queue_iam_member",
    "google_cloud_tasks_queue_iam_policy",
    "google_cloudbuild_bitbucket_server_config",
    "google_cloudbuild_trigger",
    "google_cloudbuild_worker_pool",
    "google_cloudbuildv2_connection",
    "google_cloudbuildv2_connection_iam_binding",
    "google_cloudbuildv2_connection_iam_member",
    "google_cloudbuildv2_connection_iam_policy",
    "google_cloudbuildv2_repository",
    "google_clouddeploy_automation",
    "google_clouddeploy_custom_target_type",
    "google_clouddeploy_custom_target_type_iam_binding",
    "google_clouddeploy_custom_target_type_iam_member",
    "google_clouddeploy_custom_target_type_iam_policy",
    "google_clouddeploy_delivery_pipeline",
    "google_clouddeploy_delivery_pipeline_iam_binding",
    "google_clouddeploy_delivery_pipeline_iam_member",
    "google_clouddeploy_delivery_pipeline_iam_policy",
    "google_clouddeploy_deploy_policy",
    "google_clouddeploy_target",
    "google_clouddeploy_target_iam_binding",
    "google_clouddeploy_target_iam_member",
    "google_clouddeploy_target_iam_policy",
    "google_clouddomains_registration",
    "google_cloudfunctions2_function",
    "google_cloudfunctions2_function_iam_binding",
    "google_cloudfunctions2_function_iam_member",
    "google_cloudfunctions2_function_iam_policy",
    "google_cloudfunctions_function",
    "google_cloudfunctions_function_iam_binding",
    "google_cloudfunctions_function_iam_member",
    "google_cloudfunctions_function_iam_policy",
    "google_colab_notebook_execution",
    "google_colab_runtime",
    "google_colab_runtime_template",
    "google_colab_runtime_template_iam_binding",
    "google_colab_runtime_template_iam_member",
    "google_colab_runtime_template_iam_policy",
    "google_colab_schedule",
    "google_composer_environment",
    "google_composer_user_workloads_config_map",
    "google_composer_user_workloads_secret",
    "google_compute_address",
    "google_compute_attached_disk",
    "google_compute_autoscaler",
    "google_compute_backend_bucket",
    "google_compute_backend_bucket_iam_binding",
    "google_compute_backend_bucket_iam_member",
    "google_compute_backend_bucket_iam_policy",
    "google_compute_backend_bucket_signed_url_key",
    "google_compute_backend_service",
    "google_compute_backend_service_iam_binding",
    "google_compute_backend_service_iam_member",
    "google_compute_backend_service_iam_policy",
    "google_compute_backend_service_signed_url_key",
    "google_compute_cross_site_network",
    "google_compute_disk",
    "google_compute_disk_async_replication",
    "google_compute_disk_iam_binding",
    "google_compute_disk_iam_member",
    "google_compute_disk_iam_policy",
    "google_compute_disk_resource_policy_attachment",
    "google_compute_external_vpn_gateway",
    "google_compute_firewall",
    "google_compute_firewall_policy",
    "google_compute_firewall_policy_association",
    "google_compute_firewall_policy_rule",
    "google_compute_firewall_policy_with_rules",
    "google_compute_forwarding_rule",
    "google_compute_future_reservation",
    "google_compute_global_address",
    "google_compute_global_forwarding_rule",
    "google_compute_global_network_endpoint",
    "google_compute_global_network_endpoint_group",
    "google_compute_ha_vpn_gateway",
    "google_compute_health_check",
    "google_compute_http_health_check",
    "google_compute_https_health_check",
    "google_compute_image",
    "google_compute_image_iam_binding",
    "google_compute_image_iam_member",
    "google_compute_image_iam_policy",
    "google_compute_instance",
    "google_compute_instance_from_machine_image",
    "google_compute_instance_from_template",
    "google_compute_instance_group",
    "google_compute_instance_group_manager",
    "google_compute_instance_group_membership",
    "google_compute_instance_group_named_port",
    "google_compute_instance_iam_binding",
    "google_compute_instance_iam_member",
    "google_compute_instance_iam_policy",
    "google_compute_instance_settings",
    "google_compute_instance_template",
    "google_compute_instance_template_iam_binding",
    "google_compute_instance_template_iam_member",
    "google_compute_instance_template_iam_policy",
    "google_compute_instant_snapshot",
    "google_compute_instant_snapshot_iam_binding",
    "google_compute_instant_snapshot_iam_member",
    "google_compute_instant_snapshot_iam_policy",
    "google_compute_interconnect",
    "google_compute_interconnect_attachment",
    "google_compute_interconnect_attachment_group",
    "google_compute_interconnect_group",
    "google_compute_machine_image",
    "google_compute_machine_image_iam_binding",
    "google_compute_machine_image_iam_member",
    "google_compute_machine_image_iam_policy",
    "google_compute_managed_ssl_certificate",
    "google_compute_network",
    "google_compute_network_attachment",
    "google_compute_network_edge_security_service",
    "google_compute_network_endpoint",
    "google_compute_network_endpoint_group",
    "google_compute_network_endpoints",
    "google_compute_network_firewall_policy",
    "google_compute_network_firewall_policy_association",
    "google_compute_network_firewall_policy_packet_mirroring_rule",
    "google_compute_network_firewall_policy_rule",
    "google_compute_network_firewall_policy_with_rules",
    "google_compute_network_peering",
    "google_compute_network_peering_routes_config",
    "google_compute_node_group",
    "google_compute_node_template",
    "google_compute_organization_security_policy",
    "google_compute_organization_security_policy_association",
    "google_compute_organization_security_policy_rule",
    "google_compute_packet_mirroring",
    "google_compute_per_instance_config",
    "google_compute_project_cloud_armor_tier",
    "google_compute_project_default_network_tier",
    "google_compute_project_metadata",
    "google_compute_project_metadata_item",
    "google_compute_public_advertised_prefix",
    "google_compute_public_delegated_prefix",
    "google_compute_region_autoscaler",
    "google_compute_region_backend_service",
    "google_compute_region_backend_service_iam_binding",
    "google_compute_region_backend_service_iam_member",
    "google_compute_region_backend_service_iam_policy",
    "google_compute_region_commitment",
    "google_compute_region_disk",
    "google_compute_region_disk_iam_binding",
    "google_compute_region_disk_iam_member",
    "google_compute_region_disk_iam_policy",
    "google_compute_region_disk_resource_policy_attachment",
    "google_compute_region_health_check",
    "google_compute_region_instance_group_manager",
    "google_compute_region_instance_template",
    "google_compute_region_network_endpoint",
    "google_compute_region_network_endpoint_group",
    "google_compute_region_network_firewall_policy",
    "google_compute_region_network_firewall_policy_association",
    "google_compute_region_network_firewall_policy_rule",
    "google_compute_region_network_firewall_policy_with_rules",
    "google_compute_region_per_instance_config",
    "google_compute_region_resize_request",
    "google_compute_region_security_policy",
    "google_compute_region_security_policy_rule",
    "google_compute_region_ssl_certificate",
    "google_compute_region_ssl_policy",
    "google_compute_region_target_http_proxy",
    "google_compute_region_target_https_proxy",
    "google_compute_region_target_tcp_proxy",
    "google_compute_region_url_map",
    "google_compute_reservation",
    "google_compute_resize_request",
    "google_compute_resource_policy",
    "google_compute_resource_policy_attachment",
    "google_compute_route",
    "google_compute_router",
    "google_compute_router_interface",
    "google_compute_router_nat",
    "google_compute_router_nat_address",
    "google_compute_router_peer",
    "google_compute_router_route_policy",
    "google_compute_security_policy",
    "google_compute_security_policy_rule",
    "google_compute_service_attachment",
    "google_compute_shared_vpc_host_project",
    "google_compute_shared_vpc_service_project",
    "google_compute_snapshot",
    "google_compute_snapshot_iam_binding",
    "google_compute_snapshot_iam_member",
    "google_compute_snapshot_iam_policy",
    "google_compute_snapshot_settings",
    "google_compute_ssl_certificate",
    "google_compute_ssl_policy",
    "google_compute_storage_pool",
    "google_compute_storage_pool_iam_binding",
    "google_compute_storage_pool_iam_member",
    "google_compute_storage_pool_iam_policy",
    "google_compute_subnetwork",
    "google_compute_subnetwork_iam_binding",
    "google_compute_subnetwork_iam_member",
    "google_compute_subnetwork_iam_policy",
    "google_compute_target_grpc_proxy",
    "google_compute_target_http_proxy",
    "google_compute_target_https_proxy",
    "google_compute_target_instance",
    "google_compute_target_pool",
    "google_compute_target_ssl_proxy",
    "google_compute_target_tcp_proxy",
    "google_compute_url_map",
    "google_compute_vpn_gateway",
    "google_compute_vpn_tunnel",
    "google_container_analysis_note",
    "google_container_analysis_note_iam_binding",
    "google_container_analysis_note_iam_member",
    "google_container_analysis_note_iam_policy",
    "google_container_analysis_occurrence",
    "google_container_attached_cluster",
    "google_container_aws_cluster",
    "google_container_aws_node_pool",
    "google_container_azure_client",
    "google_container_azure_cluster",
    "google_container_azure_node_pool",
    "google_container_cluster",
    "google_container_node_pool",
    "google_container_registry",
    "google_data_catalog_entry",
    "google_data_catalog_entry_group",
    "google_data_catalog_entry_group_iam_binding",
    "google_data_catalog_entry_group_iam_member",
    "google_data_catalog_entry_group_iam_policy",
    "google_data_catalog_policy_tag",
    "google_data_catalog_policy_tag_iam_binding",
    "google_data_catalog_policy_tag_iam_member",
    "google_data_catalog_policy_tag_iam_policy",
    "google_data_catalog_tag",
    "google_data_catalog_tag_template",
    "google_data_catalog_tag_template_iam_binding",
    "google_data_catalog_tag_template_iam_member",
    "google_data_catalog_tag_template_iam_policy",
    "google_data_catalog_taxonomy",
    "google_data_catalog_taxonomy_iam_binding",
    "google_data_catalog_taxonomy_iam_member",
    "google_data_catalog_taxonomy_iam_policy",
    "google_data_fusion_instance",
    "google_data_fusion_instance_iam_binding",
    "google_data_fusion_instance_iam_member",
    "google_data_fusion_instance_iam_policy",
    "google_data_loss_prevention_deidentify_template",
    "google_data_loss_prevention_discovery_config",
    "google_data_loss_prevention_inspect_template",
    "google_data_loss_prevention_job_trigger",
    "google_data_loss_prevention_stored_info_type",
    "google_data_pipeline_pipeline",
    "google_database_migration_service_connection_profile",
    "google_database_migration_service_migration_job",
    "google_database_migration_service_private_connection",
    "google_dataflow_flex_template_job",
    "google_dataflow_job",
    "google_dataform_repository",
    "google_dataform_repository_iam_binding",
    "google_dataform_repository_iam_member",
    "google_dataform_repository_iam_policy",
    "google_dataform_repository_release_config",
    "google_dataform_repository_workflow_config",
    "google_dataplex_aspect_type",
    "google_dataplex_aspect_type_iam_binding",
    "google_dataplex_aspect_type_iam_member",
    "google_dataplex_aspect_type_iam_policy",
    "google_dataplex_asset",
    "google_dataplex_asset_iam_binding",
    "google_dataplex_asset_iam_member",
    "google_dataplex_asset_iam_policy",
    "google_dataplex_datascan",
    "google_dataplex_datascan_iam_binding",
    "google_dataplex_datascan_iam_member",
    "google_dataplex_datascan_iam_policy",
    "google_dataplex_entry",
    "google_dataplex_entry_group",
    "google_dataplex_entry_group_iam_binding",
    "google_dataplex_entry_group_iam_member",
    "google_dataplex_entry_group_iam_policy",
    "google_dataplex_entry_type",
    "google_dataplex_entry_type_iam_binding",
    "google_dataplex_entry_type_iam_member",
    "google_dataplex_entry_type_iam_policy",
    "google_dataplex_glossary",
    "google_dataplex_glossary_category",
    "google_dataplex_glossary_iam_binding",
    "google_dataplex_glossary_iam_member",
    "google_dataplex_glossary_iam_policy",
    "google_dataplex_glossary_term",
    "google_dataplex_lake",
    "google_dataplex_lake_iam_binding",
    "google_dataplex_lake_iam_member",
    "google_dataplex_lake_iam_policy",
    "google_dataplex_task",
    "google_dataplex_task_iam_binding",
    "google_dataplex_task_iam_member",
    "google_dataplex_task_iam_policy",
    "google_dataplex_zone",
    "google_dataplex_zone_iam_binding",
    "google_dataplex_zone_iam_member",
    "google_dataplex_zone_iam_policy",
    "google_dataproc_autoscaling_policy",
    "google_dataproc_autoscaling_policy_iam_binding",
    "google_dataproc_autoscaling_policy_iam_member",
    "google_dataproc_autoscaling_policy_iam_policy",
    "google_dataproc_batch",
    "google_dataproc_cluster",
    "google_dataproc_cluster_iam_binding",
    "google_dataproc_cluster_iam_member",
    "google_dataproc_cluster_iam_policy",
    "google_dataproc_gdc_application_environment",
    "google_dataproc_gdc_service_instance",
    "google_dataproc_gdc_spark_application",
    "google_dataproc_job",
    "google_dataproc_job_iam_binding",
    "google_dataproc_job_iam_member",
    "google_dataproc_job_iam_policy",
    "google_dataproc_metastore_database_iam_binding",
    "google_dataproc_metastore_database_iam_member",
    "google_dataproc_metastore_database_iam_policy",
    "google_dataproc_metastore_federation",
    "google_dataproc_metastore_federation_iam_binding",
    "google_dataproc_metastore_federation_iam_member",
    "google_dataproc_metastore_federation_iam_policy",
    "google_dataproc_metastore_service",
    "google_dataproc_metastore_service_iam_binding",
    "google_dataproc_metastore_service_iam_member",
    "google_dataproc_metastore_service_iam_policy",
    "google_dataproc_metastore_table_iam_binding",
    "google_dataproc_metastore_table_iam_member",
    "google_dataproc_metastore_table_iam_policy",
    "google_dataproc_workflow_template",
    "google_datastream_connection_profile",
    "google_datastream_private_connection",
    "google_datastream_stream",
    "google_deployment_manager_deployment",
    "google_developer_connect_account_connector",
    "google_developer_connect_connection",
    "google_developer_connect_git_repository_link",
    "google_dialogflow_agent",
    "google_dialogflow_cx_agent",
    "google_dialogflow_cx_entity_type",
    "google_dialogflow_cx_environment",
    "google_dialogflow_cx_flow",
    "google_dialogflow_cx_intent",
    "google_dialogflow_cx_page",
    "google_dialogflow_cx_security_settings",
    "google_dialogflow_cx_test_case",
    "google_dialogflow_cx_version",
    "google_dialogflow_cx_webhook",
    "google_dialogflow_entity_type",
    "google_dialogflow_fulfillment",
    "google_dialogflow_intent",
    "google_discovery_engine_chat_engine",
    "google_discovery_engine_data_store",
    "google_discovery_engine_schema",
    "google_discovery_engine_search_engine",
    "google_discovery_engine_sitemap",
    "google_discovery_engine_target_site",
    "google_dns_managed_zone",
    "google_dns_managed_zone_iam_binding",
    "google_dns_managed_zone_iam_member",
    "google_dns_managed_zone_iam_policy",
    "google_dns_policy",
    "google_dns_record_set",
    "google_dns_response_policy",
    "google_dns_response_policy_rule",
    "google_document_ai_processor",
    "google_document_ai_processor_default_version",
    "google_document_ai_warehouse_document_schema",
    "google_document_ai_warehouse_location",
    "google_edgecontainer_cluster",
    "google_edgecontainer_node_pool",
    "google_edgecontainer_vpn_connection",
    "google_edgenetwork_interconnect_attachment",
    "google_edgenetwork_network",
    "google_edgenetwork_subnet",
    "google_endpoints_service",
    "google_endpoints_service_consumers_iam_binding",
    "google_endpoints_service_consumers_iam_member",
    "google_endpoints_service_consumers_iam_policy",
    "google_endpoints_service_iam_binding",
    "google_endpoints_service_iam_member",
    "google_endpoints_service_iam_policy",
    "google_essential_contacts_contact",
    "google_eventarc_channel",
    "google_eventarc_enrollment",
    "google_eventarc_google_api_source",
    "google_eventarc_google_channel_config",
    "google_eventarc_message_bus",
    "google_eventarc_pipeline",
    "google_eventarc_trigger",
    "google_filestore_backup",
    "google_filestore_instance",
    "google_filestore_snapshot",
    "google_firebase_android_app",
    "google_firebase_app_check_app_attest_config",
    "google_firebase_app_check_debug_token",
    "google_firebase_app_check_device_check_config",
    "google_firebase_app_check_play_integrity_config",
    "google_firebase_app_check_recaptcha_enterprise_config",
    "google_firebase_app_check_recaptcha_v3_config",
    "google_firebase_app_check_service_config",
    "google_firebase_app_hosting_backend",
    "google_firebase_app_hosting_build",
    "google_firebase_app_hosting_default_domain",
    "google_firebase_app_hosting_domain",
    "google_firebase_app_hosting_traffic",
    "google_firebase_apple_app",
    "google_firebase_data_connect_service",
    "google_firebase_database_instance",
    "google_firebase_extensions_instance",
    "google_firebase_hosting_channel",
    "google_firebase_hosting_custom_domain",
    "google_firebase_hosting_release",
    "google_firebase_hosting_site",
    "google_firebase_hosting_version",
    "google_firebase_project",
    "google_firebase_storage_bucket",
    "google_firebase_web_app",
    "google_firebaserules_release",
    "google_firebaserules_ruleset",
    "google_firestore_backup_schedule",
    "google_firestore_database",
    "google_firestore_document",
    "google_firestore_field",
    "google_firestore_index",
    "google_folder",
    "google_folder_access_approval_settings",
    "google_folder_iam_audit_config",
    "google_folder_iam_binding",
    "google_folder_iam_member",
    "google_folder_iam_policy",
    "google_folder_organization_policy",
    "google_folder_service_identity",
    "google_gemini_code_repository_index",
    "google_gemini_code_tools_setting",
    "google_gemini_code_tools_setting_binding",
    "google_gemini_data_sharing_with_google_setting",
    "google_gemini_data_sharing_with_google_setting_binding",
    "google_gemini_gemini_gcp_enablement_setting",
    "google_gemini_gemini_gcp_enablement_setting_binding",
    "google_gemini_logging_setting",
    "google_gemini_logging_setting_binding",
    "google_gemini_release_channel_setting",
    "google_gemini_release_channel_setting_binding",
    "google_gemini_repository_group",
    "google_gemini_repository_group_iam_binding",
    "google_gemini_repository_group_iam_member",
    "google_gemini_repository_group_iam_policy",
    "google_gke_backup_backup_channel",
    "google_gke_backup_backup_plan",
    "google_gke_backup_backup_plan_iam_binding",
    "google_gke_backup_backup_plan_iam_member",
    "google_gke_backup_backup_plan_iam_policy",
    "google_gke_backup_restore_channel",
    "google_gke_backup_restore_plan",
    "google_gke_backup_restore_plan_iam_binding",
    "google_gke_backup_restore_plan_iam_member",
    "google_gke_backup_restore_plan_iam_policy",
    "google_gke_hub_feature",
    "google_gke_hub_feature_iam_binding",
    "google_gke_hub_feature_iam_member",
    "google_gke_hub_feature_iam_policy",
    "google_gke_hub_feature_membership",
    "google_gke_hub_fleet",
    "google_gke_hub_membership",
    "google_gke_hub_membership_binding",
    "google_gke_hub_membership_iam_binding",
    "google_gke_hub_membership_iam_member",
    "google_gke_hub_membership_iam_policy",
    "google_gke_hub_membership_rbac_role_binding",
    "google_gke_hub_namespace",
    "google_gke_hub_scope",
    "google_gke_hub_scope_iam_binding",
    "google_gke_hub_scope_iam_member",
    "google_gke_hub_scope_iam_policy",
    "google_gke_hub_scope_rbac_role_binding",
    "google_gkeonprem_bare_metal_admin_cluster",
    "google_gkeonprem_bare_metal_cluster",
    "google_gkeonprem_bare_metal_node_pool",
    "google_gkeonprem_vmware_admin_cluster",
    "google_gkeonprem_vmware_cluster",
    "google_gkeonprem_vmware_node_pool",
    "google_healthcare_consent_store",
    "google_healthcare_consent_store_iam_binding",
    "google_healthcare_consent_store_iam_member",
    "google_healthcare_consent_store_iam_policy",
    "google_healthcare_dataset",
    "google_healthcare_dataset_iam_binding",
    "google_healthcare_dataset_iam_member",
    "google_healthcare_dataset_iam_policy",
    "google_healthcare_dicom_store",
    "google_healthcare_dicom_store_iam_binding",
    "google_healthcare_dicom_store_iam_member",
    "google_healthcare_dicom_store_iam_policy",
    "google_healthcare_fhir_store",
    "google_healthcare_fhir_store_iam_binding",
    "google_healthcare_fhir_store_iam_member",
    "google_healthcare_fhir_store_iam_policy",
    "google_healthcare_hl7_v2_store",
    "google_healthcare_hl7_v2_store_iam_binding",
    "google_healthcare_hl7_v2_store_iam_member",
    "google_healthcare_hl7_v2_store_iam_policy",
    "google_healthcare_pipeline_job",
    "google_healthcare_workspace",
    "google_iam_access_boundary_policy",
    "google_iam_deny_policy",
    "google_iam_folders_policy_binding",
    "google_iam_oauth_client",
    "google_iam_oauth_client_credential",
    "google_iam_organizations_policy_binding",
    "google_iam_principal_access_boundary_policy",
    "google_iam_projects_policy_binding",
    "google_iam_workforce_pool",
    "google_iam_workforce_pool_provider",
    "google_iam_workforce_pool_provider_key",
    "google_iam_workload_identity_pool",
    "google_iam_workload_identity_pool_iam_binding",
    "google_iam_workload_identity_pool_iam_member",
    "google_iam_workload_identity_pool_iam_policy",
    "google_iam_workload_identity_pool_managed_identity",
    "google_iam_workload_identity_pool_namespace",
    "google_iam_workload_identity_pool_provider",
    "google_iap_app_engine_service_iam_binding",
    "google_iap_app_engine_service_iam_member",
    "google_iap_app_engine_service_iam_policy",
    "google_iap_app_engine_version_iam_binding",
    "google_iap_app_engine_version_iam_member",
    "google_iap_app_engine_version_iam_policy",
    "google_iap_brand",
    "google_iap_client",
    "google_iap_settings",
    "google_iap_tunnel_dest_group",
    "google_iap_tunnel_dest_group_iam_binding",
    "google_iap_tunnel_dest_group_iam_member",
    "google_iap_tunnel_dest_group_iam_policy",
    "google_iap_tunnel_iam_binding",
    "google_iap_tunnel_iam_member",
    "google_iap_tunnel_iam_policy",
    "google_iap_tunnel_instance_iam_binding",
    "google_iap_tunnel_instance_iam_member",
    "google_iap_tunnel_instance_iam_policy",
    "google_iap_web_backend_service_iam_binding",
    "google_iap_web_backend_service_iam_member",
    "google_iap_web_backend_service_iam_policy",
    "google_iap_web_cloud_run_service_iam_binding",
    "google_iap_web_cloud_run_service_iam_member",
    "google_iap_web_cloud_run_service_iam_policy",
    "google_iap_web_iam_binding",
    "google_iap_web_iam_member",
    "google_iap_web_iam_policy",
    "google_iap_web_region_backend_service_iam_binding",
    "google_iap_web_region_backend_service_iam_member",
    "google_iap_web_region_backend_service_iam_policy",
    "google_iap_web_type_app_engine_iam_binding",
    "google_iap_web_type_app_engine_iam_member",
    "google_iap_web_type_app_engine_iam_policy",
    "google_iap_web_type_compute_iam_binding",
    "google_iap_web_type_compute_iam_member",
    "google_iap_web_type_compute_iam_policy",
    "google_identity_platform_config",
    "google_identity_platform_default_supported_idp_config",
    "google_identity_platform_inbound_saml_config",
    "google_identity_platform_oauth_idp_config",
    "google_identity_platform_tenant",
    "google_identity_platform_tenant_default_supported_idp_config",
    "google_identity_platform_tenant_inbound_saml_config",
    "google_identity_platform_tenant_oauth_idp_config",
    "google_integration_connectors_connection",
    "google_integration_connectors_endpoint_attachment",
    "google_integration_connectors_managed_zone",
    "google_integrations_auth_config",
    "google_integrations_client",
    "google_kms_autokey_config",
    "google_kms_crypto_key",
    "google_kms_crypto_key_iam_binding",
    "google_kms_crypto_key_iam_member",
    "google_kms_crypto_key_iam_policy",
    "google_kms_crypto_key_version",
    "google_kms_ekm_connection",
    "google_kms_ekm_connection_iam_binding",
    "google_kms_ekm_connection_iam_member",
    "google_kms_ekm_connection_iam_policy",
    "google_kms_key_handle",
    "google_kms_key_ring",
    "google_kms_key_ring_iam_binding",
    "google_kms_key_ring_iam_member",
    "google_kms_key_ring_iam_policy",
    "google_kms_key_ring_import_job",
    "google_kms_secret_ciphertext",
    "google_logging_billing_account_bucket_config",
    "google_logging_billing_account_exclusion",
    "google_logging_billing_account_sink",
    "google_logging_folder_bucket_config",
    "google_logging_folder_exclusion",
    "google_logging_folder_settings",
    "google_logging_folder_sink",
    "google_logging_linked_dataset",
    "google_logging_log_scope",
    "google_logging_log_view",
    "google_logging_log_view_iam_binding",
    "google_logging_log_view_iam_member",
    "google_logging_log_view_iam_policy",
    "google_logging_metric",
    "google_logging_organization_bucket_config",
    "google_logging_organization_exclusion",
    "google_logging_organization_settings",
    "google_logging_organization_sink",
    "google_logging_project_bucket_config",
    "google_logging_project_exclusion",
    "google_logging_project_sink",
    "google_looker_instance",
    "google_lustre_instance",
    "google_managed_kafka_acl",
    "google_managed_kafka_cluster",
    "google_managed_kafka_connect_cluster",
    "google_managed_kafka_connector",
    "google_managed_kafka_topic",
    "google_memcache_instance",
    "google_memorystore_instance",
    "google_memorystore_instance_desired_user_created_endpoints",
    "google_migration_center_group",
    "google_migration_center_preference_set",
    "google_ml_engine_model",
    "google_monitoring_alert_policy",
    "google_monitoring_custom_service",
    "google_monitoring_dashboard",
    "google_monitoring_group",
    "google_monitoring_metric_descriptor",
    "google_monitoring_monitored_project",
    "google_monitoring_notification_channel",
    "google_monitoring_service",
    "google_monitoring_slo",
    "google_monitoring_uptime_check_config",
    "google_netapp_active_directory",
    "google_netapp_backup",
    "google_netapp_backup_policy",
    "google_netapp_backup_vault",
    "google_netapp_kmsconfig",
    "google_netapp_storage_pool",
    "google_netapp_volume",
    "google_netapp_volume_quota_rule",
    "google_netapp_volume_replication",
    "google_netapp_volume_snapshot",
    "google_network_connectivity_group",
    "google_network_connectivity_hub",
    "google_network_connectivity_internal_range",
    "google_network_connectivity_policy_based_route",
    "google_network_connectivity_regional_endpoint",
    "google_network_connectivity_service_connection_policy",
    "google_network_connectivity_spoke",
    "google_network_management_connectivity_test",
    "google_network_management_vpc_flow_logs_config",
    "google_network_security_address_group",
    "google_network_security_address_group_iam_binding",
    "google_network_security_address_group_iam_member",
    "google_network_security_address_group_iam_policy",
    "google_network_security_authorization_policy",
    "google_network_security_authz_policy",
    "google_network_security_backend_authentication_config",
    "google_network_security_client_tls_policy",
    "google_network_security_firewall_endpoint",
    "google_network_security_firewall_endpoint_association",
    "google_network_security_gateway_security_policy",
    "google_network_security_gateway_security_policy_rule",
    "google_network_security_intercept_deployment",
    "google_network_security_intercept_deployment_group",
    "google_network_security_intercept_endpoint_group",
    "google_network_security_intercept_endpoint_group_association",
    "google_network_security_mirroring_deployment",
    "google_network_security_mirroring_deployment_group",
    "google_network_security_mirroring_endpoint_group",
    "google_network_security_mirroring_endpoint_group_association",
    "google_network_security_security_profile",
    "google_network_security_security_profile_group",
    "google_network_security_server_tls_policy",
    "google_network_security_tls_inspection_policy",
    "google_network_security_url_lists",
    "google_network_services_authz_extension",
    "google_network_services_edge_cache_keyset",
    "google_network_services_edge_cache_origin",
    "google_network_services_edge_cache_service",
    "google_network_services_endpoint_policy",
    "google_network_services_gateway",
    "google_network_services_grpc_route",
    "google_network_services_http_route",
    "google_network_services_lb_route_extension",
    "google_network_services_lb_traffic_extension",
    "google_network_services_mesh",
    "google_network_services_service_binding",
    "google_network_services_service_lb_policies",
    "google_network_services_tcp_route",
    "google_network_services_tls_route",
    "google_notebooks_environment",
    "google_notebooks_instance",
    "google_notebooks_instance_iam_binding",
    "google_notebooks_instance_iam_member",
    "google_notebooks_instance_iam_policy",
    "google_notebooks_location",
    "google_notebooks_runtime",
    "google_notebooks_runtime_iam_binding",
    "google_notebooks_runtime_iam_member",
    "google_notebooks_runtime_iam_policy",
    "google_oracle_database_autonomous_database",
    "google_oracle_database_cloud_exadata_infrastructure",
    "google_oracle_database_cloud_vm_cluster",
    "google_org_policy_custom_constraint",
    "google_org_policy_policy",
    "google_organization_access_approval_settings",
    "google_organization_iam_audit_config",
    "google_organization_iam_binding",
    "google_organization_iam_custom_role",
    "google_organization_iam_member",
    "google_organization_iam_policy",
    "google_organization_policy",
    "google_os_config_guest_policies",
    "google_os_config_os_policy_assignment",
    "google_os_config_patch_deployment",
    "google_os_config_v2_policy_orchestrator",
    "google_os_config_v2_policy_orchestrator_for_folder",
    "google_os_config_v2_policy_orchestrator_for_organization",
    "google_os_login_ssh_public_key",
    "google_parallelstore_instance",
    "google_parameter_manager_parameter",
    "google_parameter_manager_parameter_version",
    "google_parameter_manager_regional_parameter",
    "google_parameter_manager_regional_parameter_version",
    "google_privateca_ca_pool",
    "google_privateca_ca_pool_iam_binding",
    "google_privateca_ca_pool_iam_member",
    "google_privateca_ca_pool_iam_policy",
    "google_privateca_certificate",
    "google_privateca_certificate_authority",
    "google_privateca_certificate_template",
    "google_privateca_certificate_template_iam_binding",
    "google_privateca_certificate_template_iam_member",
    "google_privateca_certificate_template_iam_policy",
    "google_privileged_access_manager_entitlement",
    "google_project",
    "google_project_access_approval_settings",
    "google_project_default_service_accounts",
    "google_project_iam_audit_config",
    "google_project_iam_binding",
    "google_project_iam_custom_role",
    "google_project_iam_member",
    "google_project_iam_member_remove",
    "google_project_iam_policy",
    "google_project_organization_policy",
    "google_project_service",
    "google_project_service_identity",
    "google_project_usage_export_bucket",
    "google_public_ca_external_account_key",
    "google_pubsub_lite_reservation",
    "google_pubsub_lite_subscription",
    "google_pubsub_lite_topic",
    "google_pubsub_schema",
    "google_pubsub_schema_iam_binding",
    "google_pubsub_schema_iam_member",
    "google_pubsub_schema_iam_policy",
    "google_pubsub_subscription",
    "google_pubsub_subscription_iam_binding",
    "google_pubsub_subscription_iam_member",
    "google_pubsub_subscription_iam_policy",
    "google_pubsub_topic",
    "google_pubsub_topic_iam_binding",
    "google_pubsub_topic_iam_member",
    "google_pubsub_topic_iam_policy",
    "google_recaptcha_enterprise_key",
    "google_redis_cluster",
    "google_redis_cluster_user_created_connections",
    "google_redis_instance",
    "google_resource_manager_capability",
    "google_resource_manager_lien",
    "google_runtimeconfig_config",
    "google_runtimeconfig_config_iam_binding",
    "google_runtimeconfig_config_iam_member",
    "google_runtimeconfig_config_iam_policy",
    "google_runtimeconfig_variable",
    "google_scc_event_threat_detection_custom_module",
    "google_scc_folder_custom_module",
    "google_scc_folder_notification_config",
    "google_scc_folder_scc_big_query_export",
    "google_scc_management_folder_security_health_analytics_custom_module",
    "google_scc_management_organization_event_threat_detection_custom_module",
    "google_scc_management_organization_security_health_analytics_custom_module",
    "google_scc_management_project_security_health_analytics_custom_module",
    "google_scc_mute_config",
    "google_scc_notification_config",
    "google_scc_organization_custom_module",
    "google_scc_organization_scc_big_query_export",
    "google_scc_project_custom_module",
    "google_scc_project_notification_config",
    "google_scc_project_scc_big_query_export",
    "google_scc_source",
    "google_scc_source_iam_binding",
    "google_scc_source_iam_member",
    "google_scc_source_iam_policy",
    "google_scc_v2_folder_mute_config",
    "google_scc_v2_folder_notification_config",
    "google_scc_v2_folder_scc_big_query_export",
    "google_scc_v2_organization_mute_config",
    "google_scc_v2_organization_notification_config",
    "google_scc_v2_organization_scc_big_query_export",
    "google_scc_v2_organization_scc_big_query_exports",
    "google_scc_v2_organization_source",
    "google_scc_v2_organization_source_iam_binding",
    "google_scc_v2_organization_source_iam_member",
    "google_scc_v2_organization_source_iam_policy",
    "google_scc_v2_project_mute_config",
    "google_scc_v2_project_notification_config",
    "google_scc_v2_project_scc_big_query_export",
    "google_secret_manager_regional_secret",
    "google_secret_manager_regional_secret_iam_binding",
    "google_secret_manager_regional_secret_iam_member",
    "google_secret_manager_regional_secret_iam_policy",
    "google_secret_manager_regional_secret_version",
    "google_secret_manager_secret",
    "google_secret_manager_secret_iam_binding",
    "google_secret_manager_secret_iam_member",
    "google_secret_manager_secret_iam_policy",
    "google_secret_manager_secret_version",
    "google_secure_source_manager_branch_rule",
    "google_secure_source_manager_instance",
    "google_secure_source_manager_instance_iam_binding",
    "google_secure_source_manager_instance_iam_member",
    "google_secure_source_manager_instance_iam_policy",
    "google_secure_source_manager_repository",
    "google_secure_source_manager_repository_iam_binding",
    "google_secure_source_manager_repository_iam_member",
    "google_secure_source_manager_repository_iam_policy",
    "google_security_scanner_scan_config",
    "google_securityposture_posture",
    "google_securityposture_posture_deployment",
    "google_service_account",
    "google_service_account_iam_binding",
    "google_service_account_iam_member",
    "google_service_account_iam_policy",
    "google_service_account_key",
    "google_service_directory_endpoint",
    "google_service_directory_namespace",
    "google_service_directory_namespace_iam_binding",
    "google_service_directory_namespace_iam_member",
    "google_service_directory_namespace_iam_policy",
    "google_service_directory_service",
    "google_service_directory_service_iam_binding",
    "google_service_directory_service_iam_member",
    "google_service_directory_service_iam_policy",
    "google_service_networking_connection",
    "google_service_networking_peered_dns_domain",
    "google_service_networking_vpc_service_controls",
    "google_service_usage_consumer_quota_override",
    "google_site_verification_owner",
    "google_site_verification_web_resource",
    "google_sourcerepo_repository",
    "google_sourcerepo_repository_iam_binding",
    "google_sourcerepo_repository_iam_member",
    "google_sourcerepo_repository_iam_policy",
    "google_spanner_backup_schedule",
    "google_spanner_database",
    "google_spanner_database_iam_binding",
    "google_spanner_database_iam_member",
    "google_spanner_database_iam_policy",
    "google_spanner_instance",
    "google_spanner_instance_config",
    "google_spanner_instance_iam_binding",
    "google_spanner_instance_iam_member",
    "google_spanner_instance_iam_policy",
    "google_spanner_instance_partition",
    "google_sql_database",
    "google_sql_database_instance",
    "google_sql_source_representation_instance",
    "google_sql_ssl_cert",
    "google_sql_user",
    "google_storage_anywhere_cache",
    "google_storage_batch_operations_job",
    "google_storage_bucket",
    "google_storage_bucket_access_control",
    "google_storage_bucket_acl",
    "google_storage_bucket_iam_binding",
    "google_storage_bucket_iam_member",
    "google_storage_bucket_iam_policy",
    "google_storage_bucket_object",
    "google_storage_control_folder_intelligence_config",
    "google_storage_control_organization_intelligence_config",
    "google_storage_control_project_intelligence_config",
    "google_storage_default_object_access_control",
    "google_storage_default_object_acl",
    "google_storage_folder",
    "google_storage_hmac_key",
    "google_storage_insights_report_config",
    "google_storage_managed_folder",
    "google_storage_managed_folder_iam_binding",
    "google_storage_managed_folder_iam_member",
    "google_storage_managed_folder_iam_policy",
    "google_storage_notification",
    "google_storage_object_access_control",
    "google_storage_object_acl",
    "google_storage_transfer_agent_pool",
    "google_storage_transfer_job",
    "google_tags_location_tag_binding",
    "google_tags_tag_binding",
    "google_tags_tag_key",
    "google_tags_tag_key_iam_binding",
    "google_tags_tag_key_iam_member",
    "google_tags_tag_key_iam_policy",
    "google_tags_tag_value",
    "google_tags_tag_value_iam_binding",
    "google_tags_tag_value_iam_member",
    "google_tags_tag_value_iam_policy",
    "google_tpu_node",
    "google_tpu_v2_queued_resource",
    "google_tpu_v2_vm",
    "google_transcoder_job",
    "google_transcoder_job_template",
    "google_vertex_ai_dataset",
    "google_vertex_ai_deployment_resource_pool",
    "google_vertex_ai_endpoint",
    "google_vertex_ai_endpoint_iam_binding",
    "google_vertex_ai_endpoint_iam_member",
    "google_vertex_ai_endpoint_iam_policy",
    "google_vertex_ai_feature_group",
    "google_vertex_ai_feature_group_feature",
    "google_vertex_ai_feature_group_iam_binding",
    "google_vertex_ai_feature_group_iam_member",
    "google_vertex_ai_feature_group_iam_policy",
    "google_vertex_ai_feature_online_store",
    "google_vertex_ai_feature_online_store_featureview",
    "google_vertex_ai_feature_online_store_featureview_iam_binding",
    "google_vertex_ai_feature_online_store_featureview_iam_member",
    "google_vertex_ai_feature_online_store_featureview_iam_policy",
    "google_vertex_ai_feature_online_store_iam_binding",
    "google_vertex_ai_feature_online_store_iam_member",
    "google_vertex_ai_feature_online_store_iam_policy",
    "google_vertex_ai_featurestore",
    "google_vertex_ai_featurestore_entitytype",
    "google_vertex_ai_featurestore_entitytype_feature",
    "google_vertex_ai_featurestore_entitytype_iam_binding",
    "google_vertex_ai_featurestore_entitytype_iam_member",
    "google_vertex_ai_featurestore_entitytype_iam_policy",
    "google_vertex_ai_featurestore_iam_binding",
    "google_vertex_ai_featurestore_iam_member",
    "google_vertex_ai_featurestore_iam_policy",
    "google_vertex_ai_index",
    "google_vertex_ai_index_endpoint",
    "google_vertex_ai_index_endpoint_deployed_index",
    "google_vertex_ai_metadata_store",
    "google_vertex_ai_tensorboard",
    "google_vmwareengine_cluster",
    "google_vmwareengine_external_access_rule",
    "google_vmwareengine_external_address",
    "google_vmwareengine_network",
    "google_vmwareengine_network_peering",
    "google_vmwareengine_network_policy",
    "google_vmwareengine_private_cloud",
    "google_vmwareengine_subnet",
    "google_vpc_access_connector",
    "google_workbench_instance",
    "google_workbench_instance_iam_binding",
    "google_workbench_instance_iam_member",
    "google_workbench_instance_iam_policy",
    "google_workflows_workflow",
    "google_workstations_workstation",
    "google_workstations_workstation_cluster",
    "google_workstations_workstation_config",
    "google_workstations_workstation_config_iam_binding",
    "google_workstations_workstation_config_iam_member",
    "google_workstations_workstation_config_iam_policy",
    "google_workstations_workstation_iam_binding",
    "google_workstations_workstation_iam_member",
    "google_workstations_workstation_iam_policy",
    "provider",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import data_google_access_approval_folder_service_account
from . import data_google_access_approval_organization_service_account
from . import data_google_access_approval_project_service_account
from . import data_google_access_context_manager_access_policy
from . import data_google_access_context_manager_access_policy_iam_policy
from . import data_google_active_folder
from . import data_google_alloydb_cluster
from . import data_google_alloydb_instance
from . import data_google_alloydb_locations
from . import data_google_alloydb_supported_database_flags
from . import data_google_api_gateway_api_config_iam_policy
from . import data_google_api_gateway_api_iam_policy
from . import data_google_api_gateway_gateway_iam_policy
from . import data_google_apigee_environment_iam_policy
from . import data_google_app_engine_default_service_account
from . import data_google_apphub_application
from . import data_google_apphub_discovered_service
from . import data_google_apphub_discovered_workload
from . import data_google_artifact_registry_docker_image
from . import data_google_artifact_registry_locations
from . import data_google_artifact_registry_repository
from . import data_google_artifact_registry_repository_iam_policy
from . import data_google_backup_dr_backup
from . import data_google_backup_dr_backup_plan
from . import data_google_backup_dr_backup_plan_association
from . import data_google_backup_dr_backup_vault
from . import data_google_backup_dr_data_source
from . import data_google_backup_dr_management_server
from . import data_google_beyondcorp_app_connection
from . import data_google_beyondcorp_app_connector
from . import data_google_beyondcorp_app_gateway
from . import data_google_beyondcorp_application_iam_policy
from . import data_google_beyondcorp_security_gateway
from . import data_google_beyondcorp_security_gateway_application_iam_policy
from . import data_google_beyondcorp_security_gateway_iam_policy
from . import data_google_bigquery_analytics_hub_data_exchange_iam_policy
from . import data_google_bigquery_analytics_hub_listing_iam_policy
from . import data_google_bigquery_connection_iam_policy
from . import data_google_bigquery_datapolicy_data_policy_iam_policy
from . import data_google_bigquery_dataset
from . import data_google_bigquery_dataset_iam_policy
from . import data_google_bigquery_datasets
from . import data_google_bigquery_default_service_account
from . import data_google_bigquery_table
from . import data_google_bigquery_table_iam_policy
from . import data_google_bigquery_tables
from . import data_google_bigtable_instance_iam_policy
from . import data_google_bigtable_table_iam_policy
from . import data_google_billing_account
from . import data_google_billing_account_iam_policy
from . import data_google_binary_authorization_attestor_iam_policy
from . import data_google_certificate_manager_certificate_map
from . import data_google_certificate_manager_certificates
from . import data_google_client_config
from . import data_google_client_openid_userinfo
from . import data_google_cloud_asset_resources_search_all
from . import data_google_cloud_asset_search_all_resources
from . import data_google_cloud_identity_group_lookup
from . import data_google_cloud_identity_group_memberships
from . import data_google_cloud_identity_group_transitive_memberships
from . import data_google_cloud_identity_groups
from . import data_google_cloud_quotas_quota_info
from . import data_google_cloud_quotas_quota_infos
from . import data_google_cloud_run_locations
from . import data_google_cloud_run_service
from . import data_google_cloud_run_service_iam_policy
from . import data_google_cloud_run_v2_job
from . import data_google_cloud_run_v2_job_iam_policy
from . import data_google_cloud_run_v2_service
from . import data_google_cloud_run_v2_service_iam_policy
from . import data_google_cloud_run_v2_worker_pool
from . import data_google_cloud_run_v2_worker_pool_iam_policy
from . import data_google_cloud_tasks_queue_iam_policy
from . import data_google_cloudbuild_trigger
from . import data_google_cloudbuildv2_connection_iam_policy
from . import data_google_clouddeploy_custom_target_type_iam_policy
from . import data_google_clouddeploy_delivery_pipeline_iam_policy
from . import data_google_clouddeploy_target_iam_policy
from . import data_google_cloudfunctions_function
from . import data_google_cloudfunctions_function_iam_policy
from . import data_google_cloudfunctions2_function
from . import data_google_cloudfunctions2_function_iam_policy
from . import data_google_colab_runtime_template_iam_policy
from . import data_google_composer_environment
from . import data_google_composer_image_versions
from . import data_google_composer_user_workloads_config_map
from . import data_google_composer_user_workloads_secret
from . import data_google_compute_address
from . import data_google_compute_addresses
from . import data_google_compute_backend_bucket
from . import data_google_compute_backend_bucket_iam_policy
from . import data_google_compute_backend_service
from . import data_google_compute_backend_service_iam_policy
from . import data_google_compute_default_service_account
from . import data_google_compute_disk
from . import data_google_compute_disk_iam_policy
from . import data_google_compute_forwarding_rule
from . import data_google_compute_forwarding_rules
from . import data_google_compute_global_address
from . import data_google_compute_global_forwarding_rule
from . import data_google_compute_ha_vpn_gateway
from . import data_google_compute_health_check
from . import data_google_compute_image
from . import data_google_compute_image_iam_policy
from . import data_google_compute_images
from . import data_google_compute_instance
from . import data_google_compute_instance_group
from . import data_google_compute_instance_group_manager
from . import data_google_compute_instance_guest_attributes
from . import data_google_compute_instance_iam_policy
from . import data_google_compute_instance_serial_port
from . import data_google_compute_instance_template
from . import data_google_compute_instance_template_iam_policy
from . import data_google_compute_instant_snapshot_iam_policy
from . import data_google_compute_lb_ip_ranges
from . import data_google_compute_machine_image_iam_policy
from . import data_google_compute_machine_types
from . import data_google_compute_network
from . import data_google_compute_network_endpoint_group
from . import data_google_compute_network_peering
from . import data_google_compute_networks
from . import data_google_compute_node_types
from . import data_google_compute_region_backend_service
from . import data_google_compute_region_backend_service_iam_policy
from . import data_google_compute_region_disk
from . import data_google_compute_region_disk_iam_policy
from . import data_google_compute_region_instance_group
from . import data_google_compute_region_instance_group_manager
from . import data_google_compute_region_instance_template
from . import data_google_compute_region_network_endpoint_group
from . import data_google_compute_region_ssl_certificate
from . import data_google_compute_region_ssl_policy
from . import data_google_compute_regions
from . import data_google_compute_reservation
from . import data_google_compute_resource_policy
from . import data_google_compute_router
from . import data_google_compute_router_nat
from . import data_google_compute_router_status
from . import data_google_compute_security_policy
from . import data_google_compute_snapshot
from . import data_google_compute_snapshot_iam_policy
from . import data_google_compute_ssl_certificate
from . import data_google_compute_ssl_policy
from . import data_google_compute_storage_pool_iam_policy
from . import data_google_compute_storage_pool_types
from . import data_google_compute_subnetwork
from . import data_google_compute_subnetwork_iam_policy
from . import data_google_compute_subnetworks
from . import data_google_compute_vpn_gateway
from . import data_google_compute_zones
from . import data_google_container_analysis_note_iam_policy
from . import data_google_container_attached_install_manifest
from . import data_google_container_attached_versions
from . import data_google_container_aws_versions
from . import data_google_container_azure_versions
from . import data_google_container_cluster
from . import data_google_container_engine_versions
from . import data_google_container_registry_image
from . import data_google_container_registry_repository
from . import data_google_data_catalog_entry_group_iam_policy
from . import data_google_data_catalog_policy_tag_iam_policy
from . import data_google_data_catalog_tag_template_iam_policy
from . import data_google_data_catalog_taxonomy_iam_policy
from . import data_google_data_fusion_instance_iam_policy
from . import data_google_dataform_repository_iam_policy
from . import data_google_dataplex_aspect_type_iam_policy
from . import data_google_dataplex_asset_iam_policy
from . import data_google_dataplex_datascan_iam_policy
from . import data_google_dataplex_entry_group_iam_policy
from . import data_google_dataplex_entry_type_iam_policy
from . import data_google_dataplex_glossary_iam_policy
from . import data_google_dataplex_lake_iam_policy
from . import data_google_dataplex_task_iam_policy
from . import data_google_dataplex_zone_iam_policy
from . import data_google_dataproc_autoscaling_policy_iam_policy
from . import data_google_dataproc_cluster_iam_policy
from . import data_google_dataproc_job_iam_policy
from . import data_google_dataproc_metastore_database_iam_policy
from . import data_google_dataproc_metastore_federation_iam_policy
from . import data_google_dataproc_metastore_service
from . import data_google_dataproc_metastore_service_iam_policy
from . import data_google_dataproc_metastore_table_iam_policy
from . import data_google_datastream_static_ips
from . import data_google_dns_keys
from . import data_google_dns_managed_zone
from . import data_google_dns_managed_zone_iam_policy
from . import data_google_dns_managed_zones
from . import data_google_dns_record_set
from . import data_google_endpoints_service_consumers_iam_policy
from . import data_google_endpoints_service_iam_policy
from . import data_google_filestore_instance
from . import data_google_firebase_android_app
from . import data_google_firebase_android_app_config
from . import data_google_firebase_apple_app
from . import data_google_firebase_apple_app_config
from . import data_google_firebase_hosting_channel
from . import data_google_firebase_web_app
from . import data_google_firebase_web_app_config
from . import data_google_folder
from . import data_google_folder_iam_policy
from . import data_google_folder_organization_policy
from . import data_google_folders
from . import data_google_gemini_repository_group_iam_policy
from . import data_google_gke_backup_backup_plan_iam_policy
from . import data_google_gke_backup_restore_plan_iam_policy
from . import data_google_gke_hub_feature
from . import data_google_gke_hub_feature_iam_policy
from . import data_google_gke_hub_membership
from . import data_google_gke_hub_membership_binding
from . import data_google_gke_hub_membership_iam_policy
from . import data_google_gke_hub_scope_iam_policy
from . import data_google_healthcare_consent_store_iam_policy
from . import data_google_healthcare_dataset_iam_policy
from . import data_google_healthcare_dicom_store_iam_policy
from . import data_google_healthcare_fhir_store_iam_policy
from . import data_google_healthcare_hl7_v2_store_iam_policy
from . import data_google_iam_policy
from . import data_google_iam_role
from . import data_google_iam_testable_permissions
from . import data_google_iam_workload_identity_pool
from . import data_google_iam_workload_identity_pool_iam_policy
from . import data_google_iam_workload_identity_pool_provider
from . import data_google_iap_app_engine_service_iam_policy
from . import data_google_iap_app_engine_version_iam_policy
from . import data_google_iap_client
from . import data_google_iap_tunnel_dest_group_iam_policy
from . import data_google_iap_tunnel_iam_policy
from . import data_google_iap_tunnel_instance_iam_policy
from . import data_google_iap_web_backend_service_iam_policy
from . import data_google_iap_web_cloud_run_service_iam_policy
from . import data_google_iap_web_iam_policy
from . import data_google_iap_web_region_backend_service_iam_policy
from . import data_google_iap_web_type_app_engine_iam_policy
from . import data_google_iap_web_type_compute_iam_policy
from . import data_google_kms_autokey_config
from . import data_google_kms_crypto_key
from . import data_google_kms_crypto_key_iam_policy
from . import data_google_kms_crypto_key_latest_version
from . import data_google_kms_crypto_key_version
from . import data_google_kms_crypto_key_versions
from . import data_google_kms_crypto_keys
from . import data_google_kms_ekm_connection_iam_policy
from . import data_google_kms_key_handle
from . import data_google_kms_key_handles
from . import data_google_kms_key_ring
from . import data_google_kms_key_ring_iam_policy
from . import data_google_kms_key_rings
from . import data_google_kms_secret
from . import data_google_kms_secret_asymmetric
from . import data_google_kms_secret_ciphertext
from . import data_google_logging_folder_settings
from . import data_google_logging_log_view_iam_policy
from . import data_google_logging_organization_settings
from . import data_google_logging_project_cmek_settings
from . import data_google_logging_project_settings
from . import data_google_logging_sink
from . import data_google_lustre_instance
from . import data_google_memcache_instance
from . import data_google_memorystore_instance
from . import data_google_monitoring_app_engine_service
from . import data_google_monitoring_cluster_istio_service
from . import data_google_monitoring_istio_canonical_service
from . import data_google_monitoring_mesh_istio_service
from . import data_google_monitoring_notification_channel
from . import data_google_monitoring_uptime_check_ips
from . import data_google_netblock_ip_ranges
from . import data_google_network_security_address_group_iam_policy
from . import data_google_notebooks_instance_iam_policy
from . import data_google_notebooks_runtime_iam_policy
from . import data_google_oracle_database_autonomous_database
from . import data_google_oracle_database_autonomous_databases
from . import data_google_oracle_database_cloud_exadata_infrastructure
from . import data_google_oracle_database_cloud_exadata_infrastructures
from . import data_google_oracle_database_cloud_vm_cluster
from . import data_google_oracle_database_cloud_vm_clusters
from . import data_google_oracle_database_db_nodes
from . import data_google_oracle_database_db_servers
from . import data_google_organization
from . import data_google_organization_iam_custom_role
from . import data_google_organization_iam_custom_roles
from . import data_google_organization_iam_policy
from . import data_google_organizations
from . import data_google_parameter_manager_parameter
from . import data_google_parameter_manager_parameter_version
from . import data_google_parameter_manager_parameter_version_render
from . import data_google_parameter_manager_parameters
from . import data_google_parameter_manager_regional_parameter
from . import data_google_parameter_manager_regional_parameter_version
from . import data_google_parameter_manager_regional_parameter_version_render
from . import data_google_parameter_manager_regional_parameters
from . import data_google_privateca_ca_pool_iam_policy
from . import data_google_privateca_certificate_authority
from . import data_google_privateca_certificate_template_iam_policy
from . import data_google_privileged_access_manager_entitlement
from . import data_google_project
from . import data_google_project_ancestry
from . import data_google_project_iam_custom_role
from . import data_google_project_iam_custom_roles
from . import data_google_project_iam_policy
from . import data_google_project_organization_policy
from . import data_google_project_service
from . import data_google_projects
from . import data_google_pubsub_schema_iam_policy
from . import data_google_pubsub_subscription
from . import data_google_pubsub_subscription_iam_policy
from . import data_google_pubsub_topic
from . import data_google_pubsub_topic_iam_policy
from . import data_google_redis_instance
from . import data_google_runtimeconfig_config
from . import data_google_runtimeconfig_config_iam_policy
from . import data_google_runtimeconfig_variable
from . import data_google_scc_source_iam_policy
from . import data_google_scc_v2_organization_source_iam_policy
from . import data_google_secret_manager_regional_secret
from . import data_google_secret_manager_regional_secret_iam_policy
from . import data_google_secret_manager_regional_secret_version
from . import data_google_secret_manager_regional_secret_version_access
from . import data_google_secret_manager_regional_secrets
from . import data_google_secret_manager_secret
from . import data_google_secret_manager_secret_iam_policy
from . import data_google_secret_manager_secret_version
from . import data_google_secret_manager_secret_version_access
from . import data_google_secret_manager_secrets
from . import data_google_secure_source_manager_instance_iam_policy
from . import data_google_secure_source_manager_repository_iam_policy
from . import data_google_service_account
from . import data_google_service_account_access_token
from . import data_google_service_account_iam_policy
from . import data_google_service_account_id_token
from . import data_google_service_account_jwt
from . import data_google_service_account_key
from . import data_google_service_accounts
from . import data_google_service_directory_namespace_iam_policy
from . import data_google_service_directory_service_iam_policy
from . import data_google_service_networking_peered_dns_domain
from . import data_google_site_verification_token
from . import data_google_sourcerepo_repository
from . import data_google_sourcerepo_repository_iam_policy
from . import data_google_spanner_database
from . import data_google_spanner_database_iam_policy
from . import data_google_spanner_instance
from . import data_google_spanner_instance_iam_policy
from . import data_google_sql_backup_run
from . import data_google_sql_ca_certs
from . import data_google_sql_database
from . import data_google_sql_database_instance
from . import data_google_sql_database_instance_latest_recovery_time
from . import data_google_sql_database_instances
from . import data_google_sql_databases
from . import data_google_sql_tiers
from . import data_google_storage_bucket
from . import data_google_storage_bucket_iam_policy
from . import data_google_storage_bucket_object
from . import data_google_storage_bucket_object_content
from . import data_google_storage_bucket_objects
from . import data_google_storage_buckets
from . import data_google_storage_control_folder_intelligence_config
from . import data_google_storage_control_organization_intelligence_config
from . import data_google_storage_control_project_intelligence_config
from . import data_google_storage_managed_folder_iam_policy
from . import data_google_storage_object_signed_url
from . import data_google_storage_project_service_account
from . import data_google_storage_transfer_project_service_account
from . import data_google_tags_tag_key
from . import data_google_tags_tag_key_iam_policy
from . import data_google_tags_tag_keys
from . import data_google_tags_tag_value
from . import data_google_tags_tag_value_iam_policy
from . import data_google_tags_tag_values
from . import data_google_tpu_tensorflow_versions
from . import data_google_tpu_v2_accelerator_types
from . import data_google_tpu_v2_runtime_versions
from . import data_google_vertex_ai_endpoint_iam_policy
from . import data_google_vertex_ai_feature_group_iam_policy
from . import data_google_vertex_ai_feature_online_store_featureview_iam_policy
from . import data_google_vertex_ai_feature_online_store_iam_policy
from . import data_google_vertex_ai_featurestore_entitytype_iam_policy
from . import data_google_vertex_ai_featurestore_iam_policy
from . import data_google_vertex_ai_index
from . import data_google_vmwareengine_cluster
from . import data_google_vmwareengine_external_access_rule
from . import data_google_vmwareengine_external_address
from . import data_google_vmwareengine_network
from . import data_google_vmwareengine_network_peering
from . import data_google_vmwareengine_network_policy
from . import data_google_vmwareengine_nsx_credentials
from . import data_google_vmwareengine_private_cloud
from . import data_google_vmwareengine_subnet
from . import data_google_vmwareengine_vcenter_credentials
from . import data_google_vpc_access_connector
from . import data_google_workbench_instance_iam_policy
from . import data_google_workstations_workstation_config_iam_policy
from . import data_google_workstations_workstation_iam_policy
from . import google_access_context_manager_access_level
from . import google_access_context_manager_access_level_condition
from . import google_access_context_manager_access_levels
from . import google_access_context_manager_access_policy
from . import google_access_context_manager_access_policy_iam_binding
from . import google_access_context_manager_access_policy_iam_member
from . import google_access_context_manager_access_policy_iam_policy
from . import google_access_context_manager_authorized_orgs_desc
from . import google_access_context_manager_egress_policy
from . import google_access_context_manager_gcp_user_access_binding
from . import google_access_context_manager_ingress_policy
from . import google_access_context_manager_service_perimeter
from . import google_access_context_manager_service_perimeter_dry_run_egress_policy
from . import google_access_context_manager_service_perimeter_dry_run_ingress_policy
from . import google_access_context_manager_service_perimeter_dry_run_resource
from . import google_access_context_manager_service_perimeter_egress_policy
from . import google_access_context_manager_service_perimeter_ingress_policy
from . import google_access_context_manager_service_perimeter_resource
from . import google_access_context_manager_service_perimeters
from . import google_active_directory_domain
from . import google_active_directory_domain_trust
from . import google_active_directory_peering
from . import google_alloydb_backup
from . import google_alloydb_cluster
from . import google_alloydb_instance
from . import google_alloydb_user
from . import google_api_gateway_api
from . import google_api_gateway_api_config
from . import google_api_gateway_api_config_iam_binding
from . import google_api_gateway_api_config_iam_member
from . import google_api_gateway_api_config_iam_policy
from . import google_api_gateway_api_iam_binding
from . import google_api_gateway_api_iam_member
from . import google_api_gateway_api_iam_policy
from . import google_api_gateway_gateway
from . import google_api_gateway_gateway_iam_binding
from . import google_api_gateway_gateway_iam_member
from . import google_api_gateway_gateway_iam_policy
from . import google_apigee_addons_config
from . import google_apigee_api
from . import google_apigee_app_group
from . import google_apigee_control_plane_access
from . import google_apigee_developer
from . import google_apigee_dns_zone
from . import google_apigee_endpoint_attachment
from . import google_apigee_env_keystore
from . import google_apigee_env_references
from . import google_apigee_envgroup
from . import google_apigee_envgroup_attachment
from . import google_apigee_environment
from . import google_apigee_environment_addons_config
from . import google_apigee_environment_iam_binding
from . import google_apigee_environment_iam_member
from . import google_apigee_environment_iam_policy
from . import google_apigee_environment_keyvaluemaps
from . import google_apigee_environment_keyvaluemaps_entries
from . import google_apigee_flowhook
from . import google_apigee_instance
from . import google_apigee_instance_attachment
from . import google_apigee_keystores_aliases_key_cert_file
from . import google_apigee_keystores_aliases_pkcs12
from . import google_apigee_keystores_aliases_self_signed_cert
from . import google_apigee_nat_address
from . import google_apigee_organization
from . import google_apigee_security_monitoring_condition
from . import google_apigee_security_profile_v2
from . import google_apigee_sharedflow
from . import google_apigee_sharedflow_deployment
from . import google_apigee_sync_authorization
from . import google_apigee_target_server
from . import google_apihub_api_hub_instance
from . import google_apihub_curation
from . import google_apihub_host_project_registration
from . import google_apikeys_key
from . import google_app_engine_application
from . import google_app_engine_application_url_dispatch_rules
from . import google_app_engine_domain_mapping
from . import google_app_engine_firewall_rule
from . import google_app_engine_flexible_app_version
from . import google_app_engine_service_network_settings
from . import google_app_engine_service_split_traffic
from . import google_app_engine_standard_app_version
from . import google_apphub_application
from . import google_apphub_service
from . import google_apphub_service_project_attachment
from . import google_apphub_workload
from . import google_artifact_registry_repository
from . import google_artifact_registry_repository_iam_binding
from . import google_artifact_registry_repository_iam_member
from . import google_artifact_registry_repository_iam_policy
from . import google_artifact_registry_vpcsc_config
from . import google_assured_workloads_workload
from . import google_backup_dr_backup_plan
from . import google_backup_dr_backup_plan_association
from . import google_backup_dr_backup_vault
from . import google_backup_dr_management_server
from . import google_beyondcorp_app_connection
from . import google_beyondcorp_app_connector
from . import google_beyondcorp_app_gateway
from . import google_beyondcorp_application
from . import google_beyondcorp_application_iam_binding
from . import google_beyondcorp_application_iam_member
from . import google_beyondcorp_application_iam_policy
from . import google_beyondcorp_security_gateway
from . import google_beyondcorp_security_gateway_application
from . import google_beyondcorp_security_gateway_application_iam_binding
from . import google_beyondcorp_security_gateway_application_iam_member
from . import google_beyondcorp_security_gateway_application_iam_policy
from . import google_beyondcorp_security_gateway_iam_binding
from . import google_beyondcorp_security_gateway_iam_member
from . import google_beyondcorp_security_gateway_iam_policy
from . import google_biglake_catalog
from . import google_biglake_database
from . import google_biglake_table
from . import google_bigquery_analytics_hub_data_exchange
from . import google_bigquery_analytics_hub_data_exchange_iam_binding
from . import google_bigquery_analytics_hub_data_exchange_iam_member
from . import google_bigquery_analytics_hub_data_exchange_iam_policy
from . import google_bigquery_analytics_hub_listing
from . import google_bigquery_analytics_hub_listing_iam_binding
from . import google_bigquery_analytics_hub_listing_iam_member
from . import google_bigquery_analytics_hub_listing_iam_policy
from . import google_bigquery_analytics_hub_listing_subscription
from . import google_bigquery_bi_reservation
from . import google_bigquery_capacity_commitment
from . import google_bigquery_connection
from . import google_bigquery_connection_iam_binding
from . import google_bigquery_connection_iam_member
from . import google_bigquery_connection_iam_policy
from . import google_bigquery_data_transfer_config
from . import google_bigquery_datapolicy_data_policy
from . import google_bigquery_datapolicy_data_policy_iam_binding
from . import google_bigquery_datapolicy_data_policy_iam_member
from . import google_bigquery_datapolicy_data_policy_iam_policy
from . import google_bigquery_dataset
from . import google_bigquery_dataset_access
from . import google_bigquery_dataset_iam_binding
from . import google_bigquery_dataset_iam_member
from . import google_bigquery_dataset_iam_policy
from . import google_bigquery_job
from . import google_bigquery_reservation
from . import google_bigquery_reservation_assignment
from . import google_bigquery_routine
from . import google_bigquery_row_access_policy
from . import google_bigquery_table
from . import google_bigquery_table_iam_binding
from . import google_bigquery_table_iam_member
from . import google_bigquery_table_iam_policy
from . import google_bigtable_app_profile
from . import google_bigtable_authorized_view
from . import google_bigtable_gc_policy
from . import google_bigtable_instance
from . import google_bigtable_instance_iam_binding
from . import google_bigtable_instance_iam_member
from . import google_bigtable_instance_iam_policy
from . import google_bigtable_logical_view
from . import google_bigtable_materialized_view
from . import google_bigtable_table
from . import google_bigtable_table_iam_binding
from . import google_bigtable_table_iam_member
from . import google_bigtable_table_iam_policy
from . import google_billing_account_iam_binding
from . import google_billing_account_iam_member
from . import google_billing_account_iam_policy
from . import google_billing_budget
from . import google_billing_project_info
from . import google_billing_subaccount
from . import google_binary_authorization_attestor
from . import google_binary_authorization_attestor_iam_binding
from . import google_binary_authorization_attestor_iam_member
from . import google_binary_authorization_attestor_iam_policy
from . import google_binary_authorization_policy
from . import google_blockchain_node_engine_blockchain_nodes
from . import google_certificate_manager_certificate
from . import google_certificate_manager_certificate_issuance_config
from . import google_certificate_manager_certificate_map
from . import google_certificate_manager_certificate_map_entry
from . import google_certificate_manager_dns_authorization
from . import google_certificate_manager_trust_config
from . import google_chronicle_data_access_label
from . import google_chronicle_data_access_scope
from . import google_chronicle_reference_list
from . import google_chronicle_retrohunt
from . import google_chronicle_rule
from . import google_chronicle_rule_deployment
from . import google_chronicle_watchlist
from . import google_cloud_asset_folder_feed
from . import google_cloud_asset_organization_feed
from . import google_cloud_asset_project_feed
from . import google_cloud_identity_group
from . import google_cloud_identity_group_membership
from . import google_cloud_ids_endpoint
from . import google_cloud_quotas_quota_adjuster_settings
from . import google_cloud_quotas_quota_preference
from . import google_cloud_run_domain_mapping
from . import google_cloud_run_service
from . import google_cloud_run_service_iam_binding
from . import google_cloud_run_service_iam_member
from . import google_cloud_run_service_iam_policy
from . import google_cloud_run_v2_job
from . import google_cloud_run_v2_job_iam_binding
from . import google_cloud_run_v2_job_iam_member
from . import google_cloud_run_v2_job_iam_policy
from . import google_cloud_run_v2_service
from . import google_cloud_run_v2_service_iam_binding
from . import google_cloud_run_v2_service_iam_member
from . import google_cloud_run_v2_service_iam_policy
from . import google_cloud_run_v2_worker_pool
from . import google_cloud_run_v2_worker_pool_iam_binding
from . import google_cloud_run_v2_worker_pool_iam_member
from . import google_cloud_run_v2_worker_pool_iam_policy
from . import google_cloud_scheduler_job
from . import google_cloud_tasks_queue
from . import google_cloud_tasks_queue_iam_binding
from . import google_cloud_tasks_queue_iam_member
from . import google_cloud_tasks_queue_iam_policy
from . import google_cloudbuild_bitbucket_server_config
from . import google_cloudbuild_trigger
from . import google_cloudbuild_worker_pool
from . import google_cloudbuildv2_connection
from . import google_cloudbuildv2_connection_iam_binding
from . import google_cloudbuildv2_connection_iam_member
from . import google_cloudbuildv2_connection_iam_policy
from . import google_cloudbuildv2_repository
from . import google_clouddeploy_automation
from . import google_clouddeploy_custom_target_type
from . import google_clouddeploy_custom_target_type_iam_binding
from . import google_clouddeploy_custom_target_type_iam_member
from . import google_clouddeploy_custom_target_type_iam_policy
from . import google_clouddeploy_delivery_pipeline
from . import google_clouddeploy_delivery_pipeline_iam_binding
from . import google_clouddeploy_delivery_pipeline_iam_member
from . import google_clouddeploy_delivery_pipeline_iam_policy
from . import google_clouddeploy_deploy_policy
from . import google_clouddeploy_target
from . import google_clouddeploy_target_iam_binding
from . import google_clouddeploy_target_iam_member
from . import google_clouddeploy_target_iam_policy
from . import google_clouddomains_registration
from . import google_cloudfunctions_function
from . import google_cloudfunctions_function_iam_binding
from . import google_cloudfunctions_function_iam_member
from . import google_cloudfunctions_function_iam_policy
from . import google_cloudfunctions2_function
from . import google_cloudfunctions2_function_iam_binding
from . import google_cloudfunctions2_function_iam_member
from . import google_cloudfunctions2_function_iam_policy
from . import google_colab_notebook_execution
from . import google_colab_runtime
from . import google_colab_runtime_template
from . import google_colab_runtime_template_iam_binding
from . import google_colab_runtime_template_iam_member
from . import google_colab_runtime_template_iam_policy
from . import google_colab_schedule
from . import google_composer_environment
from . import google_composer_user_workloads_config_map
from . import google_composer_user_workloads_secret
from . import google_compute_address
from . import google_compute_attached_disk
from . import google_compute_autoscaler
from . import google_compute_backend_bucket
from . import google_compute_backend_bucket_iam_binding
from . import google_compute_backend_bucket_iam_member
from . import google_compute_backend_bucket_iam_policy
from . import google_compute_backend_bucket_signed_url_key
from . import google_compute_backend_service
from . import google_compute_backend_service_iam_binding
from . import google_compute_backend_service_iam_member
from . import google_compute_backend_service_iam_policy
from . import google_compute_backend_service_signed_url_key
from . import google_compute_cross_site_network
from . import google_compute_disk
from . import google_compute_disk_async_replication
from . import google_compute_disk_iam_binding
from . import google_compute_disk_iam_member
from . import google_compute_disk_iam_policy
from . import google_compute_disk_resource_policy_attachment
from . import google_compute_external_vpn_gateway
from . import google_compute_firewall
from . import google_compute_firewall_policy
from . import google_compute_firewall_policy_association
from . import google_compute_firewall_policy_rule
from . import google_compute_firewall_policy_with_rules
from . import google_compute_forwarding_rule
from . import google_compute_future_reservation
from . import google_compute_global_address
from . import google_compute_global_forwarding_rule
from . import google_compute_global_network_endpoint
from . import google_compute_global_network_endpoint_group
from . import google_compute_ha_vpn_gateway
from . import google_compute_health_check
from . import google_compute_http_health_check
from . import google_compute_https_health_check
from . import google_compute_image
from . import google_compute_image_iam_binding
from . import google_compute_image_iam_member
from . import google_compute_image_iam_policy
from . import google_compute_instance
from . import google_compute_instance_from_machine_image
from . import google_compute_instance_from_template
from . import google_compute_instance_group
from . import google_compute_instance_group_manager
from . import google_compute_instance_group_membership
from . import google_compute_instance_group_named_port
from . import google_compute_instance_iam_binding
from . import google_compute_instance_iam_member
from . import google_compute_instance_iam_policy
from . import google_compute_instance_settings
from . import google_compute_instance_template
from . import google_compute_instance_template_iam_binding
from . import google_compute_instance_template_iam_member
from . import google_compute_instance_template_iam_policy
from . import google_compute_instant_snapshot
from . import google_compute_instant_snapshot_iam_binding
from . import google_compute_instant_snapshot_iam_member
from . import google_compute_instant_snapshot_iam_policy
from . import google_compute_interconnect
from . import google_compute_interconnect_attachment
from . import google_compute_interconnect_attachment_group
from . import google_compute_interconnect_group
from . import google_compute_machine_image
from . import google_compute_machine_image_iam_binding
from . import google_compute_machine_image_iam_member
from . import google_compute_machine_image_iam_policy
from . import google_compute_managed_ssl_certificate
from . import google_compute_network
from . import google_compute_network_attachment
from . import google_compute_network_edge_security_service
from . import google_compute_network_endpoint
from . import google_compute_network_endpoint_group
from . import google_compute_network_endpoints
from . import google_compute_network_firewall_policy
from . import google_compute_network_firewall_policy_association
from . import google_compute_network_firewall_policy_packet_mirroring_rule
from . import google_compute_network_firewall_policy_rule
from . import google_compute_network_firewall_policy_with_rules
from . import google_compute_network_peering
from . import google_compute_network_peering_routes_config
from . import google_compute_node_group
from . import google_compute_node_template
from . import google_compute_organization_security_policy
from . import google_compute_organization_security_policy_association
from . import google_compute_organization_security_policy_rule
from . import google_compute_packet_mirroring
from . import google_compute_per_instance_config
from . import google_compute_project_cloud_armor_tier
from . import google_compute_project_default_network_tier
from . import google_compute_project_metadata
from . import google_compute_project_metadata_item
from . import google_compute_public_advertised_prefix
from . import google_compute_public_delegated_prefix
from . import google_compute_region_autoscaler
from . import google_compute_region_backend_service
from . import google_compute_region_backend_service_iam_binding
from . import google_compute_region_backend_service_iam_member
from . import google_compute_region_backend_service_iam_policy
from . import google_compute_region_commitment
from . import google_compute_region_disk
from . import google_compute_region_disk_iam_binding
from . import google_compute_region_disk_iam_member
from . import google_compute_region_disk_iam_policy
from . import google_compute_region_disk_resource_policy_attachment
from . import google_compute_region_health_check
from . import google_compute_region_instance_group_manager
from . import google_compute_region_instance_template
from . import google_compute_region_network_endpoint
from . import google_compute_region_network_endpoint_group
from . import google_compute_region_network_firewall_policy
from . import google_compute_region_network_firewall_policy_association
from . import google_compute_region_network_firewall_policy_rule
from . import google_compute_region_network_firewall_policy_with_rules
from . import google_compute_region_per_instance_config
from . import google_compute_region_resize_request
from . import google_compute_region_security_policy
from . import google_compute_region_security_policy_rule
from . import google_compute_region_ssl_certificate
from . import google_compute_region_ssl_policy
from . import google_compute_region_target_http_proxy
from . import google_compute_region_target_https_proxy
from . import google_compute_region_target_tcp_proxy
from . import google_compute_region_url_map
from . import google_compute_reservation
from . import google_compute_resize_request
from . import google_compute_resource_policy
from . import google_compute_resource_policy_attachment
from . import google_compute_route
from . import google_compute_router
from . import google_compute_router_interface
from . import google_compute_router_nat
from . import google_compute_router_nat_address
from . import google_compute_router_peer
from . import google_compute_router_route_policy
from . import google_compute_security_policy
from . import google_compute_security_policy_rule
from . import google_compute_service_attachment
from . import google_compute_shared_vpc_host_project
from . import google_compute_shared_vpc_service_project
from . import google_compute_snapshot
from . import google_compute_snapshot_iam_binding
from . import google_compute_snapshot_iam_member
from . import google_compute_snapshot_iam_policy
from . import google_compute_snapshot_settings
from . import google_compute_ssl_certificate
from . import google_compute_ssl_policy
from . import google_compute_storage_pool
from . import google_compute_storage_pool_iam_binding
from . import google_compute_storage_pool_iam_member
from . import google_compute_storage_pool_iam_policy
from . import google_compute_subnetwork
from . import google_compute_subnetwork_iam_binding
from . import google_compute_subnetwork_iam_member
from . import google_compute_subnetwork_iam_policy
from . import google_compute_target_grpc_proxy
from . import google_compute_target_http_proxy
from . import google_compute_target_https_proxy
from . import google_compute_target_instance
from . import google_compute_target_pool
from . import google_compute_target_ssl_proxy
from . import google_compute_target_tcp_proxy
from . import google_compute_url_map
from . import google_compute_vpn_gateway
from . import google_compute_vpn_tunnel
from . import google_container_analysis_note
from . import google_container_analysis_note_iam_binding
from . import google_container_analysis_note_iam_member
from . import google_container_analysis_note_iam_policy
from . import google_container_analysis_occurrence
from . import google_container_attached_cluster
from . import google_container_aws_cluster
from . import google_container_aws_node_pool
from . import google_container_azure_client
from . import google_container_azure_cluster
from . import google_container_azure_node_pool
from . import google_container_cluster
from . import google_container_node_pool
from . import google_container_registry
from . import google_data_catalog_entry
from . import google_data_catalog_entry_group
from . import google_data_catalog_entry_group_iam_binding
from . import google_data_catalog_entry_group_iam_member
from . import google_data_catalog_entry_group_iam_policy
from . import google_data_catalog_policy_tag
from . import google_data_catalog_policy_tag_iam_binding
from . import google_data_catalog_policy_tag_iam_member
from . import google_data_catalog_policy_tag_iam_policy
from . import google_data_catalog_tag
from . import google_data_catalog_tag_template
from . import google_data_catalog_tag_template_iam_binding
from . import google_data_catalog_tag_template_iam_member
from . import google_data_catalog_tag_template_iam_policy
from . import google_data_catalog_taxonomy
from . import google_data_catalog_taxonomy_iam_binding
from . import google_data_catalog_taxonomy_iam_member
from . import google_data_catalog_taxonomy_iam_policy
from . import google_data_fusion_instance
from . import google_data_fusion_instance_iam_binding
from . import google_data_fusion_instance_iam_member
from . import google_data_fusion_instance_iam_policy
from . import google_data_loss_prevention_deidentify_template
from . import google_data_loss_prevention_discovery_config
from . import google_data_loss_prevention_inspect_template
from . import google_data_loss_prevention_job_trigger
from . import google_data_loss_prevention_stored_info_type
from . import google_data_pipeline_pipeline
from . import google_database_migration_service_connection_profile
from . import google_database_migration_service_migration_job
from . import google_database_migration_service_private_connection
from . import google_dataflow_flex_template_job
from . import google_dataflow_job
from . import google_dataform_repository
from . import google_dataform_repository_iam_binding
from . import google_dataform_repository_iam_member
from . import google_dataform_repository_iam_policy
from . import google_dataform_repository_release_config
from . import google_dataform_repository_workflow_config
from . import google_dataplex_aspect_type
from . import google_dataplex_aspect_type_iam_binding
from . import google_dataplex_aspect_type_iam_member
from . import google_dataplex_aspect_type_iam_policy
from . import google_dataplex_asset
from . import google_dataplex_asset_iam_binding
from . import google_dataplex_asset_iam_member
from . import google_dataplex_asset_iam_policy
from . import google_dataplex_datascan
from . import google_dataplex_datascan_iam_binding
from . import google_dataplex_datascan_iam_member
from . import google_dataplex_datascan_iam_policy
from . import google_dataplex_entry
from . import google_dataplex_entry_group
from . import google_dataplex_entry_group_iam_binding
from . import google_dataplex_entry_group_iam_member
from . import google_dataplex_entry_group_iam_policy
from . import google_dataplex_entry_type
from . import google_dataplex_entry_type_iam_binding
from . import google_dataplex_entry_type_iam_member
from . import google_dataplex_entry_type_iam_policy
from . import google_dataplex_glossary
from . import google_dataplex_glossary_category
from . import google_dataplex_glossary_iam_binding
from . import google_dataplex_glossary_iam_member
from . import google_dataplex_glossary_iam_policy
from . import google_dataplex_glossary_term
from . import google_dataplex_lake
from . import google_dataplex_lake_iam_binding
from . import google_dataplex_lake_iam_member
from . import google_dataplex_lake_iam_policy
from . import google_dataplex_task
from . import google_dataplex_task_iam_binding
from . import google_dataplex_task_iam_member
from . import google_dataplex_task_iam_policy
from . import google_dataplex_zone
from . import google_dataplex_zone_iam_binding
from . import google_dataplex_zone_iam_member
from . import google_dataplex_zone_iam_policy
from . import google_dataproc_autoscaling_policy
from . import google_dataproc_autoscaling_policy_iam_binding
from . import google_dataproc_autoscaling_policy_iam_member
from . import google_dataproc_autoscaling_policy_iam_policy
from . import google_dataproc_batch
from . import google_dataproc_cluster
from . import google_dataproc_cluster_iam_binding
from . import google_dataproc_cluster_iam_member
from . import google_dataproc_cluster_iam_policy
from . import google_dataproc_gdc_application_environment
from . import google_dataproc_gdc_service_instance
from . import google_dataproc_gdc_spark_application
from . import google_dataproc_job
from . import google_dataproc_job_iam_binding
from . import google_dataproc_job_iam_member
from . import google_dataproc_job_iam_policy
from . import google_dataproc_metastore_database_iam_binding
from . import google_dataproc_metastore_database_iam_member
from . import google_dataproc_metastore_database_iam_policy
from . import google_dataproc_metastore_federation
from . import google_dataproc_metastore_federation_iam_binding
from . import google_dataproc_metastore_federation_iam_member
from . import google_dataproc_metastore_federation_iam_policy
from . import google_dataproc_metastore_service
from . import google_dataproc_metastore_service_iam_binding
from . import google_dataproc_metastore_service_iam_member
from . import google_dataproc_metastore_service_iam_policy
from . import google_dataproc_metastore_table_iam_binding
from . import google_dataproc_metastore_table_iam_member
from . import google_dataproc_metastore_table_iam_policy
from . import google_dataproc_workflow_template
from . import google_datastream_connection_profile
from . import google_datastream_private_connection
from . import google_datastream_stream
from . import google_deployment_manager_deployment
from . import google_developer_connect_account_connector
from . import google_developer_connect_connection
from . import google_developer_connect_git_repository_link
from . import google_dialogflow_agent
from . import google_dialogflow_cx_agent
from . import google_dialogflow_cx_entity_type
from . import google_dialogflow_cx_environment
from . import google_dialogflow_cx_flow
from . import google_dialogflow_cx_intent
from . import google_dialogflow_cx_page
from . import google_dialogflow_cx_security_settings
from . import google_dialogflow_cx_test_case
from . import google_dialogflow_cx_version
from . import google_dialogflow_cx_webhook
from . import google_dialogflow_entity_type
from . import google_dialogflow_fulfillment
from . import google_dialogflow_intent
from . import google_discovery_engine_chat_engine
from . import google_discovery_engine_data_store
from . import google_discovery_engine_schema
from . import google_discovery_engine_search_engine
from . import google_discovery_engine_sitemap
from . import google_discovery_engine_target_site
from . import google_dns_managed_zone
from . import google_dns_managed_zone_iam_binding
from . import google_dns_managed_zone_iam_member
from . import google_dns_managed_zone_iam_policy
from . import google_dns_policy
from . import google_dns_record_set
from . import google_dns_response_policy
from . import google_dns_response_policy_rule
from . import google_document_ai_processor
from . import google_document_ai_processor_default_version
from . import google_document_ai_warehouse_document_schema
from . import google_document_ai_warehouse_location
from . import google_edgecontainer_cluster
from . import google_edgecontainer_node_pool
from . import google_edgecontainer_vpn_connection
from . import google_edgenetwork_interconnect_attachment
from . import google_edgenetwork_network
from . import google_edgenetwork_subnet
from . import google_endpoints_service
from . import google_endpoints_service_consumers_iam_binding
from . import google_endpoints_service_consumers_iam_member
from . import google_endpoints_service_consumers_iam_policy
from . import google_endpoints_service_iam_binding
from . import google_endpoints_service_iam_member
from . import google_endpoints_service_iam_policy
from . import google_essential_contacts_contact
from . import google_eventarc_channel
from . import google_eventarc_enrollment
from . import google_eventarc_google_api_source
from . import google_eventarc_google_channel_config
from . import google_eventarc_message_bus
from . import google_eventarc_pipeline
from . import google_eventarc_trigger
from . import google_filestore_backup
from . import google_filestore_instance
from . import google_filestore_snapshot
from . import google_firebase_android_app
from . import google_firebase_app_check_app_attest_config
from . import google_firebase_app_check_debug_token
from . import google_firebase_app_check_device_check_config
from . import google_firebase_app_check_play_integrity_config
from . import google_firebase_app_check_recaptcha_enterprise_config
from . import google_firebase_app_check_recaptcha_v3_config
from . import google_firebase_app_check_service_config
from . import google_firebase_app_hosting_backend
from . import google_firebase_app_hosting_build
from . import google_firebase_app_hosting_default_domain
from . import google_firebase_app_hosting_domain
from . import google_firebase_app_hosting_traffic
from . import google_firebase_apple_app
from . import google_firebase_data_connect_service
from . import google_firebase_database_instance
from . import google_firebase_extensions_instance
from . import google_firebase_hosting_channel
from . import google_firebase_hosting_custom_domain
from . import google_firebase_hosting_release
from . import google_firebase_hosting_site
from . import google_firebase_hosting_version
from . import google_firebase_project
from . import google_firebase_storage_bucket
from . import google_firebase_web_app
from . import google_firebaserules_release
from . import google_firebaserules_ruleset
from . import google_firestore_backup_schedule
from . import google_firestore_database
from . import google_firestore_document
from . import google_firestore_field
from . import google_firestore_index
from . import google_folder
from . import google_folder_access_approval_settings
from . import google_folder_iam_audit_config
from . import google_folder_iam_binding
from . import google_folder_iam_member
from . import google_folder_iam_policy
from . import google_folder_organization_policy
from . import google_folder_service_identity
from . import google_gemini_code_repository_index
from . import google_gemini_code_tools_setting
from . import google_gemini_code_tools_setting_binding
from . import google_gemini_data_sharing_with_google_setting
from . import google_gemini_data_sharing_with_google_setting_binding
from . import google_gemini_gemini_gcp_enablement_setting
from . import google_gemini_gemini_gcp_enablement_setting_binding
from . import google_gemini_logging_setting
from . import google_gemini_logging_setting_binding
from . import google_gemini_release_channel_setting
from . import google_gemini_release_channel_setting_binding
from . import google_gemini_repository_group
from . import google_gemini_repository_group_iam_binding
from . import google_gemini_repository_group_iam_member
from . import google_gemini_repository_group_iam_policy
from . import google_gke_backup_backup_channel
from . import google_gke_backup_backup_plan
from . import google_gke_backup_backup_plan_iam_binding
from . import google_gke_backup_backup_plan_iam_member
from . import google_gke_backup_backup_plan_iam_policy
from . import google_gke_backup_restore_channel
from . import google_gke_backup_restore_plan
from . import google_gke_backup_restore_plan_iam_binding
from . import google_gke_backup_restore_plan_iam_member
from . import google_gke_backup_restore_plan_iam_policy
from . import google_gke_hub_feature
from . import google_gke_hub_feature_iam_binding
from . import google_gke_hub_feature_iam_member
from . import google_gke_hub_feature_iam_policy
from . import google_gke_hub_feature_membership
from . import google_gke_hub_fleet
from . import google_gke_hub_membership
from . import google_gke_hub_membership_binding
from . import google_gke_hub_membership_iam_binding
from . import google_gke_hub_membership_iam_member
from . import google_gke_hub_membership_iam_policy
from . import google_gke_hub_membership_rbac_role_binding
from . import google_gke_hub_namespace
from . import google_gke_hub_scope
from . import google_gke_hub_scope_iam_binding
from . import google_gke_hub_scope_iam_member
from . import google_gke_hub_scope_iam_policy
from . import google_gke_hub_scope_rbac_role_binding
from . import google_gkeonprem_bare_metal_admin_cluster
from . import google_gkeonprem_bare_metal_cluster
from . import google_gkeonprem_bare_metal_node_pool
from . import google_gkeonprem_vmware_admin_cluster
from . import google_gkeonprem_vmware_cluster
from . import google_gkeonprem_vmware_node_pool
from . import google_healthcare_consent_store
from . import google_healthcare_consent_store_iam_binding
from . import google_healthcare_consent_store_iam_member
from . import google_healthcare_consent_store_iam_policy
from . import google_healthcare_dataset
from . import google_healthcare_dataset_iam_binding
from . import google_healthcare_dataset_iam_member
from . import google_healthcare_dataset_iam_policy
from . import google_healthcare_dicom_store
from . import google_healthcare_dicom_store_iam_binding
from . import google_healthcare_dicom_store_iam_member
from . import google_healthcare_dicom_store_iam_policy
from . import google_healthcare_fhir_store
from . import google_healthcare_fhir_store_iam_binding
from . import google_healthcare_fhir_store_iam_member
from . import google_healthcare_fhir_store_iam_policy
from . import google_healthcare_hl7_v2_store
from . import google_healthcare_hl7_v2_store_iam_binding
from . import google_healthcare_hl7_v2_store_iam_member
from . import google_healthcare_hl7_v2_store_iam_policy
from . import google_healthcare_pipeline_job
from . import google_healthcare_workspace
from . import google_iam_access_boundary_policy
from . import google_iam_deny_policy
from . import google_iam_folders_policy_binding
from . import google_iam_oauth_client
from . import google_iam_oauth_client_credential
from . import google_iam_organizations_policy_binding
from . import google_iam_principal_access_boundary_policy
from . import google_iam_projects_policy_binding
from . import google_iam_workforce_pool
from . import google_iam_workforce_pool_provider
from . import google_iam_workforce_pool_provider_key
from . import google_iam_workload_identity_pool
from . import google_iam_workload_identity_pool_iam_binding
from . import google_iam_workload_identity_pool_iam_member
from . import google_iam_workload_identity_pool_iam_policy
from . import google_iam_workload_identity_pool_managed_identity
from . import google_iam_workload_identity_pool_namespace
from . import google_iam_workload_identity_pool_provider
from . import google_iap_app_engine_service_iam_binding
from . import google_iap_app_engine_service_iam_member
from . import google_iap_app_engine_service_iam_policy
from . import google_iap_app_engine_version_iam_binding
from . import google_iap_app_engine_version_iam_member
from . import google_iap_app_engine_version_iam_policy
from . import google_iap_brand
from . import google_iap_client
from . import google_iap_settings
from . import google_iap_tunnel_dest_group
from . import google_iap_tunnel_dest_group_iam_binding
from . import google_iap_tunnel_dest_group_iam_member
from . import google_iap_tunnel_dest_group_iam_policy
from . import google_iap_tunnel_iam_binding
from . import google_iap_tunnel_iam_member
from . import google_iap_tunnel_iam_policy
from . import google_iap_tunnel_instance_iam_binding
from . import google_iap_tunnel_instance_iam_member
from . import google_iap_tunnel_instance_iam_policy
from . import google_iap_web_backend_service_iam_binding
from . import google_iap_web_backend_service_iam_member
from . import google_iap_web_backend_service_iam_policy
from . import google_iap_web_cloud_run_service_iam_binding
from . import google_iap_web_cloud_run_service_iam_member
from . import google_iap_web_cloud_run_service_iam_policy
from . import google_iap_web_iam_binding
from . import google_iap_web_iam_member
from . import google_iap_web_iam_policy
from . import google_iap_web_region_backend_service_iam_binding
from . import google_iap_web_region_backend_service_iam_member
from . import google_iap_web_region_backend_service_iam_policy
from . import google_iap_web_type_app_engine_iam_binding
from . import google_iap_web_type_app_engine_iam_member
from . import google_iap_web_type_app_engine_iam_policy
from . import google_iap_web_type_compute_iam_binding
from . import google_iap_web_type_compute_iam_member
from . import google_iap_web_type_compute_iam_policy
from . import google_identity_platform_config
from . import google_identity_platform_default_supported_idp_config
from . import google_identity_platform_inbound_saml_config
from . import google_identity_platform_oauth_idp_config
from . import google_identity_platform_tenant
from . import google_identity_platform_tenant_default_supported_idp_config
from . import google_identity_platform_tenant_inbound_saml_config
from . import google_identity_platform_tenant_oauth_idp_config
from . import google_integration_connectors_connection
from . import google_integration_connectors_endpoint_attachment
from . import google_integration_connectors_managed_zone
from . import google_integrations_auth_config
from . import google_integrations_client
from . import google_kms_autokey_config
from . import google_kms_crypto_key
from . import google_kms_crypto_key_iam_binding
from . import google_kms_crypto_key_iam_member
from . import google_kms_crypto_key_iam_policy
from . import google_kms_crypto_key_version
from . import google_kms_ekm_connection
from . import google_kms_ekm_connection_iam_binding
from . import google_kms_ekm_connection_iam_member
from . import google_kms_ekm_connection_iam_policy
from . import google_kms_key_handle
from . import google_kms_key_ring
from . import google_kms_key_ring_iam_binding
from . import google_kms_key_ring_iam_member
from . import google_kms_key_ring_iam_policy
from . import google_kms_key_ring_import_job
from . import google_kms_secret_ciphertext
from . import google_logging_billing_account_bucket_config
from . import google_logging_billing_account_exclusion
from . import google_logging_billing_account_sink
from . import google_logging_folder_bucket_config
from . import google_logging_folder_exclusion
from . import google_logging_folder_settings
from . import google_logging_folder_sink
from . import google_logging_linked_dataset
from . import google_logging_log_scope
from . import google_logging_log_view
from . import google_logging_log_view_iam_binding
from . import google_logging_log_view_iam_member
from . import google_logging_log_view_iam_policy
from . import google_logging_metric
from . import google_logging_organization_bucket_config
from . import google_logging_organization_exclusion
from . import google_logging_organization_settings
from . import google_logging_organization_sink
from . import google_logging_project_bucket_config
from . import google_logging_project_exclusion
from . import google_logging_project_sink
from . import google_looker_instance
from . import google_lustre_instance
from . import google_managed_kafka_acl
from . import google_managed_kafka_cluster
from . import google_managed_kafka_connect_cluster
from . import google_managed_kafka_connector
from . import google_managed_kafka_topic
from . import google_memcache_instance
from . import google_memorystore_instance
from . import google_memorystore_instance_desired_user_created_endpoints
from . import google_migration_center_group
from . import google_migration_center_preference_set
from . import google_ml_engine_model
from . import google_monitoring_alert_policy
from . import google_monitoring_custom_service
from . import google_monitoring_dashboard
from . import google_monitoring_group
from . import google_monitoring_metric_descriptor
from . import google_monitoring_monitored_project
from . import google_monitoring_notification_channel
from . import google_monitoring_service
from . import google_monitoring_slo
from . import google_monitoring_uptime_check_config
from . import google_netapp_active_directory
from . import google_netapp_backup
from . import google_netapp_backup_policy
from . import google_netapp_backup_vault
from . import google_netapp_kmsconfig
from . import google_netapp_storage_pool
from . import google_netapp_volume
from . import google_netapp_volume_quota_rule
from . import google_netapp_volume_replication
from . import google_netapp_volume_snapshot
from . import google_network_connectivity_group
from . import google_network_connectivity_hub
from . import google_network_connectivity_internal_range
from . import google_network_connectivity_policy_based_route
from . import google_network_connectivity_regional_endpoint
from . import google_network_connectivity_service_connection_policy
from . import google_network_connectivity_spoke
from . import google_network_management_connectivity_test
from . import google_network_management_vpc_flow_logs_config
from . import google_network_security_address_group
from . import google_network_security_address_group_iam_binding
from . import google_network_security_address_group_iam_member
from . import google_network_security_address_group_iam_policy
from . import google_network_security_authorization_policy
from . import google_network_security_authz_policy
from . import google_network_security_backend_authentication_config
from . import google_network_security_client_tls_policy
from . import google_network_security_firewall_endpoint
from . import google_network_security_firewall_endpoint_association
from . import google_network_security_gateway_security_policy
from . import google_network_security_gateway_security_policy_rule
from . import google_network_security_intercept_deployment
from . import google_network_security_intercept_deployment_group
from . import google_network_security_intercept_endpoint_group
from . import google_network_security_intercept_endpoint_group_association
from . import google_network_security_mirroring_deployment
from . import google_network_security_mirroring_deployment_group
from . import google_network_security_mirroring_endpoint_group
from . import google_network_security_mirroring_endpoint_group_association
from . import google_network_security_security_profile
from . import google_network_security_security_profile_group
from . import google_network_security_server_tls_policy
from . import google_network_security_tls_inspection_policy
from . import google_network_security_url_lists
from . import google_network_services_authz_extension
from . import google_network_services_edge_cache_keyset
from . import google_network_services_edge_cache_origin
from . import google_network_services_edge_cache_service
from . import google_network_services_endpoint_policy
from . import google_network_services_gateway
from . import google_network_services_grpc_route
from . import google_network_services_http_route
from . import google_network_services_lb_route_extension
from . import google_network_services_lb_traffic_extension
from . import google_network_services_mesh
from . import google_network_services_service_binding
from . import google_network_services_service_lb_policies
from . import google_network_services_tcp_route
from . import google_network_services_tls_route
from . import google_notebooks_environment
from . import google_notebooks_instance
from . import google_notebooks_instance_iam_binding
from . import google_notebooks_instance_iam_member
from . import google_notebooks_instance_iam_policy
from . import google_notebooks_location
from . import google_notebooks_runtime
from . import google_notebooks_runtime_iam_binding
from . import google_notebooks_runtime_iam_member
from . import google_notebooks_runtime_iam_policy
from . import google_oracle_database_autonomous_database
from . import google_oracle_database_cloud_exadata_infrastructure
from . import google_oracle_database_cloud_vm_cluster
from . import google_org_policy_custom_constraint
from . import google_org_policy_policy
from . import google_organization_access_approval_settings
from . import google_organization_iam_audit_config
from . import google_organization_iam_binding
from . import google_organization_iam_custom_role
from . import google_organization_iam_member
from . import google_organization_iam_policy
from . import google_organization_policy
from . import google_os_config_guest_policies
from . import google_os_config_os_policy_assignment
from . import google_os_config_patch_deployment
from . import google_os_config_v2_policy_orchestrator
from . import google_os_config_v2_policy_orchestrator_for_folder
from . import google_os_config_v2_policy_orchestrator_for_organization
from . import google_os_login_ssh_public_key
from . import google_parallelstore_instance
from . import google_parameter_manager_parameter
from . import google_parameter_manager_parameter_version
from . import google_parameter_manager_regional_parameter
from . import google_parameter_manager_regional_parameter_version
from . import google_privateca_ca_pool
from . import google_privateca_ca_pool_iam_binding
from . import google_privateca_ca_pool_iam_member
from . import google_privateca_ca_pool_iam_policy
from . import google_privateca_certificate
from . import google_privateca_certificate_authority
from . import google_privateca_certificate_template
from . import google_privateca_certificate_template_iam_binding
from . import google_privateca_certificate_template_iam_member
from . import google_privateca_certificate_template_iam_policy
from . import google_privileged_access_manager_entitlement
from . import google_project
from . import google_project_access_approval_settings
from . import google_project_default_service_accounts
from . import google_project_iam_audit_config
from . import google_project_iam_binding
from . import google_project_iam_custom_role
from . import google_project_iam_member
from . import google_project_iam_member_remove
from . import google_project_iam_policy
from . import google_project_organization_policy
from . import google_project_service
from . import google_project_service_identity
from . import google_project_usage_export_bucket
from . import google_public_ca_external_account_key
from . import google_pubsub_lite_reservation
from . import google_pubsub_lite_subscription
from . import google_pubsub_lite_topic
from . import google_pubsub_schema
from . import google_pubsub_schema_iam_binding
from . import google_pubsub_schema_iam_member
from . import google_pubsub_schema_iam_policy
from . import google_pubsub_subscription
from . import google_pubsub_subscription_iam_binding
from . import google_pubsub_subscription_iam_member
from . import google_pubsub_subscription_iam_policy
from . import google_pubsub_topic
from . import google_pubsub_topic_iam_binding
from . import google_pubsub_topic_iam_member
from . import google_pubsub_topic_iam_policy
from . import google_recaptcha_enterprise_key
from . import google_redis_cluster
from . import google_redis_cluster_user_created_connections
from . import google_redis_instance
from . import google_resource_manager_capability
from . import google_resource_manager_lien
from . import google_runtimeconfig_config
from . import google_runtimeconfig_config_iam_binding
from . import google_runtimeconfig_config_iam_member
from . import google_runtimeconfig_config_iam_policy
from . import google_runtimeconfig_variable
from . import google_scc_event_threat_detection_custom_module
from . import google_scc_folder_custom_module
from . import google_scc_folder_notification_config
from . import google_scc_folder_scc_big_query_export
from . import google_scc_management_folder_security_health_analytics_custom_module
from . import google_scc_management_organization_event_threat_detection_custom_module
from . import google_scc_management_organization_security_health_analytics_custom_module
from . import google_scc_management_project_security_health_analytics_custom_module
from . import google_scc_mute_config
from . import google_scc_notification_config
from . import google_scc_organization_custom_module
from . import google_scc_organization_scc_big_query_export
from . import google_scc_project_custom_module
from . import google_scc_project_notification_config
from . import google_scc_project_scc_big_query_export
from . import google_scc_source
from . import google_scc_source_iam_binding
from . import google_scc_source_iam_member
from . import google_scc_source_iam_policy
from . import google_scc_v2_folder_mute_config
from . import google_scc_v2_folder_notification_config
from . import google_scc_v2_folder_scc_big_query_export
from . import google_scc_v2_organization_mute_config
from . import google_scc_v2_organization_notification_config
from . import google_scc_v2_organization_scc_big_query_export
from . import google_scc_v2_organization_scc_big_query_exports
from . import google_scc_v2_organization_source
from . import google_scc_v2_organization_source_iam_binding
from . import google_scc_v2_organization_source_iam_member
from . import google_scc_v2_organization_source_iam_policy
from . import google_scc_v2_project_mute_config
from . import google_scc_v2_project_notification_config
from . import google_scc_v2_project_scc_big_query_export
from . import google_secret_manager_regional_secret
from . import google_secret_manager_regional_secret_iam_binding
from . import google_secret_manager_regional_secret_iam_member
from . import google_secret_manager_regional_secret_iam_policy
from . import google_secret_manager_regional_secret_version
from . import google_secret_manager_secret
from . import google_secret_manager_secret_iam_binding
from . import google_secret_manager_secret_iam_member
from . import google_secret_manager_secret_iam_policy
from . import google_secret_manager_secret_version
from . import google_secure_source_manager_branch_rule
from . import google_secure_source_manager_instance
from . import google_secure_source_manager_instance_iam_binding
from . import google_secure_source_manager_instance_iam_member
from . import google_secure_source_manager_instance_iam_policy
from . import google_secure_source_manager_repository
from . import google_secure_source_manager_repository_iam_binding
from . import google_secure_source_manager_repository_iam_member
from . import google_secure_source_manager_repository_iam_policy
from . import google_security_scanner_scan_config
from . import google_securityposture_posture
from . import google_securityposture_posture_deployment
from . import google_service_account
from . import google_service_account_iam_binding
from . import google_service_account_iam_member
from . import google_service_account_iam_policy
from . import google_service_account_key
from . import google_service_directory_endpoint
from . import google_service_directory_namespace
from . import google_service_directory_namespace_iam_binding
from . import google_service_directory_namespace_iam_member
from . import google_service_directory_namespace_iam_policy
from . import google_service_directory_service
from . import google_service_directory_service_iam_binding
from . import google_service_directory_service_iam_member
from . import google_service_directory_service_iam_policy
from . import google_service_networking_connection
from . import google_service_networking_peered_dns_domain
from . import google_service_networking_vpc_service_controls
from . import google_service_usage_consumer_quota_override
from . import google_site_verification_owner
from . import google_site_verification_web_resource
from . import google_sourcerepo_repository
from . import google_sourcerepo_repository_iam_binding
from . import google_sourcerepo_repository_iam_member
from . import google_sourcerepo_repository_iam_policy
from . import google_spanner_backup_schedule
from . import google_spanner_database
from . import google_spanner_database_iam_binding
from . import google_spanner_database_iam_member
from . import google_spanner_database_iam_policy
from . import google_spanner_instance
from . import google_spanner_instance_config
from . import google_spanner_instance_iam_binding
from . import google_spanner_instance_iam_member
from . import google_spanner_instance_iam_policy
from . import google_spanner_instance_partition
from . import google_sql_database
from . import google_sql_database_instance
from . import google_sql_source_representation_instance
from . import google_sql_ssl_cert
from . import google_sql_user
from . import google_storage_anywhere_cache
from . import google_storage_batch_operations_job
from . import google_storage_bucket
from . import google_storage_bucket_access_control
from . import google_storage_bucket_acl
from . import google_storage_bucket_iam_binding
from . import google_storage_bucket_iam_member
from . import google_storage_bucket_iam_policy
from . import google_storage_bucket_object
from . import google_storage_control_folder_intelligence_config
from . import google_storage_control_organization_intelligence_config
from . import google_storage_control_project_intelligence_config
from . import google_storage_default_object_access_control
from . import google_storage_default_object_acl
from . import google_storage_folder
from . import google_storage_hmac_key
from . import google_storage_insights_report_config
from . import google_storage_managed_folder
from . import google_storage_managed_folder_iam_binding
from . import google_storage_managed_folder_iam_member
from . import google_storage_managed_folder_iam_policy
from . import google_storage_notification
from . import google_storage_object_access_control
from . import google_storage_object_acl
from . import google_storage_transfer_agent_pool
from . import google_storage_transfer_job
from . import google_tags_location_tag_binding
from . import google_tags_tag_binding
from . import google_tags_tag_key
from . import google_tags_tag_key_iam_binding
from . import google_tags_tag_key_iam_member
from . import google_tags_tag_key_iam_policy
from . import google_tags_tag_value
from . import google_tags_tag_value_iam_binding
from . import google_tags_tag_value_iam_member
from . import google_tags_tag_value_iam_policy
from . import google_tpu_node
from . import google_tpu_v2_queued_resource
from . import google_tpu_v2_vm
from . import google_transcoder_job
from . import google_transcoder_job_template
from . import google_vertex_ai_dataset
from . import google_vertex_ai_deployment_resource_pool
from . import google_vertex_ai_endpoint
from . import google_vertex_ai_endpoint_iam_binding
from . import google_vertex_ai_endpoint_iam_member
from . import google_vertex_ai_endpoint_iam_policy
from . import google_vertex_ai_feature_group
from . import google_vertex_ai_feature_group_feature
from . import google_vertex_ai_feature_group_iam_binding
from . import google_vertex_ai_feature_group_iam_member
from . import google_vertex_ai_feature_group_iam_policy
from . import google_vertex_ai_feature_online_store
from . import google_vertex_ai_feature_online_store_featureview
from . import google_vertex_ai_feature_online_store_featureview_iam_binding
from . import google_vertex_ai_feature_online_store_featureview_iam_member
from . import google_vertex_ai_feature_online_store_featureview_iam_policy
from . import google_vertex_ai_feature_online_store_iam_binding
from . import google_vertex_ai_feature_online_store_iam_member
from . import google_vertex_ai_feature_online_store_iam_policy
from . import google_vertex_ai_featurestore
from . import google_vertex_ai_featurestore_entitytype
from . import google_vertex_ai_featurestore_entitytype_feature
from . import google_vertex_ai_featurestore_entitytype_iam_binding
from . import google_vertex_ai_featurestore_entitytype_iam_member
from . import google_vertex_ai_featurestore_entitytype_iam_policy
from . import google_vertex_ai_featurestore_iam_binding
from . import google_vertex_ai_featurestore_iam_member
from . import google_vertex_ai_featurestore_iam_policy
from . import google_vertex_ai_index
from . import google_vertex_ai_index_endpoint
from . import google_vertex_ai_index_endpoint_deployed_index
from . import google_vertex_ai_metadata_store
from . import google_vertex_ai_tensorboard
from . import google_vmwareengine_cluster
from . import google_vmwareengine_external_access_rule
from . import google_vmwareengine_external_address
from . import google_vmwareengine_network
from . import google_vmwareengine_network_peering
from . import google_vmwareengine_network_policy
from . import google_vmwareengine_private_cloud
from . import google_vmwareengine_subnet
from . import google_vpc_access_connector
from . import google_workbench_instance
from . import google_workbench_instance_iam_binding
from . import google_workbench_instance_iam_member
from . import google_workbench_instance_iam_policy
from . import google_workflows_workflow
from . import google_workstations_workstation
from . import google_workstations_workstation_cluster
from . import google_workstations_workstation_config
from . import google_workstations_workstation_config_iam_binding
from . import google_workstations_workstation_config_iam_member
from . import google_workstations_workstation_config_iam_policy
from . import google_workstations_workstation_iam_binding
from . import google_workstations_workstation_iam_member
from . import google_workstations_workstation_iam_policy
from . import provider
