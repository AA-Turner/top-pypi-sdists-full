r'''
# CDKTF prebuilt bindings for opentelekomcloud/opentelekomcloud provider version 1.36.44

This repo builds and publishes the [Terraform opentelekomcloud provider](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-opentelekomcloud](https://www.npmjs.com/package/@cdktf/provider-opentelekomcloud).

`npm install @cdktf/provider-opentelekomcloud`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-opentelekomcloud](https://pypi.org/project/cdktf-cdktf-provider-opentelekomcloud).

`pipenv install cdktf-cdktf-provider-opentelekomcloud`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Opentelekomcloud](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Opentelekomcloud).

`dotnet add package HashiCorp.Cdktf.Providers.Opentelekomcloud`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-opentelekomcloud](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-opentelekomcloud).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-opentelekomcloud</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-opentelekomcloud-go`](https://github.com/cdktf/cdktf-provider-opentelekomcloud-go) package.

`go get github.com/cdktf/cdktf-provider-opentelekomcloud-go/opentelekomcloud/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-opentelekomcloud-go/blob/main/opentelekomcloud/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-opentelekomcloud).

## Versioning

This project is explicitly not tracking the Terraform opentelekomcloud provider version 1:1. In fact, it always tracks `latest` of `~> 1.26` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform opentelekomcloud provider](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44)
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
    "antiddos_v1",
    "apigw_acl_policy_associate_v2",
    "apigw_acl_policy_v2",
    "apigw_api_publishment_v2",
    "apigw_api_v2",
    "apigw_appcode_v2",
    "apigw_application_authorization_v2",
    "apigw_application_v2",
    "apigw_certificate_v2",
    "apigw_custom_authorizer_v2",
    "apigw_environment_v2",
    "apigw_environment_variable_v2",
    "apigw_gateway_feature_v2",
    "apigw_gateway_routes_v2",
    "apigw_gateway_v2",
    "apigw_group_v2",
    "apigw_response_v2",
    "apigw_signature_associate_v2",
    "apigw_signature_v2",
    "apigw_throttling_policy_associate_v2",
    "apigw_throttling_policy_v2",
    "apigw_vpc_channel_v2",
    "as_configuration_v1",
    "as_group_v1",
    "as_lifecycle_hook_v1",
    "as_policy_v1",
    "as_policy_v2",
    "blockstorage_volume_v2",
    "cbr_policy_v3",
    "cbr_vault_v3",
    "cce_addon_v3",
    "cce_cluster_v3",
    "cce_node_attach_v3",
    "cce_node_pool_v3",
    "cce_node_v3",
    "cci_namespace_v2",
    "ces_alarmrule",
    "ces_event_report_v1",
    "ces_metric_data_v1",
    "cfw_acl_rule_v1",
    "cfw_address_group_member_v1",
    "cfw_address_group_v1",
    "cfw_blacklist_whitelist_rule_v1",
    "cfw_domain_name_group_v1",
    "cfw_eip_protection_v1",
    "cfw_firewall_v1",
    "cfw_ips_protection_v1",
    "cfw_service_group_member_v1",
    "cfw_service_group_v1",
    "compute_bms_server_v2",
    "compute_bms_tags_v2",
    "compute_floatingip_associate_v2",
    "compute_floatingip_v2",
    "compute_instance_v2",
    "compute_keypair_v2",
    "compute_secgroup_v2",
    "compute_servergroup_v2",
    "compute_volume_attach_v2",
    "csbs_backup_policy_v1",
    "csbs_backup_v1",
    "css_cluster_restart_v1",
    "css_cluster_v1",
    "css_configuration_v1",
    "css_snapshot_configuration_v1",
    "cts_event_notification_v3",
    "cts_tracker_v1",
    "cts_tracker_v3",
    "data_opentelekomcloud_antiddos_v1",
    "data_opentelekomcloud_apigw_api_history_v2",
    "data_opentelekomcloud_apigw_gateway_features_v2",
    "data_opentelekomcloud_cbr_backup_ids_v3",
    "data_opentelekomcloud_cbr_backup_v3",
    "data_opentelekomcloud_cce_addon_template_v3",
    "data_opentelekomcloud_cce_addon_templates_v3",
    "data_opentelekomcloud_cce_cluster_kubeconfig_v3",
    "data_opentelekomcloud_cce_cluster_v3",
    "data_opentelekomcloud_cce_clusters_v3",
    "data_opentelekomcloud_cce_node_ids_v3",
    "data_opentelekomcloud_cce_node_v3",
    "data_opentelekomcloud_ces_event_details_v1",
    "data_opentelekomcloud_ces_events_v1",
    "data_opentelekomcloud_ces_metric_data_v1",
    "data_opentelekomcloud_ces_metrics_v1",
    "data_opentelekomcloud_ces_multiple_metric_data_v1",
    "data_opentelekomcloud_ces_quotas_v1",
    "data_opentelekomcloud_cfw_firewall_v1",
    "data_opentelekomcloud_compute_availability_zones_v2",
    "data_opentelekomcloud_compute_bms_flavors_v2",
    "data_opentelekomcloud_compute_bms_keypairs_v2",
    "data_opentelekomcloud_compute_bms_nic_v2",
    "data_opentelekomcloud_compute_bms_server_v2",
    "data_opentelekomcloud_compute_flavor_v2",
    "data_opentelekomcloud_compute_instance_v2",
    "data_opentelekomcloud_compute_instances_v2",
    "data_opentelekomcloud_compute_keypair_v2",
    "data_opentelekomcloud_csbs_backup_policy_v1",
    "data_opentelekomcloud_csbs_backup_v1",
    "data_opentelekomcloud_css_certificate_v1",
    "data_opentelekomcloud_css_flavor_v1",
    "data_opentelekomcloud_cts_tracker_v1",
    "data_opentelekomcloud_dcs_az_v1",
    "data_opentelekomcloud_dcs_certificate_v2",
    "data_opentelekomcloud_dcs_maintainwindow_v1",
    "data_opentelekomcloud_dcs_product_v1",
    "data_opentelekomcloud_ddm_engines_v1",
    "data_opentelekomcloud_ddm_flavors_v1",
    "data_opentelekomcloud_ddm_instance_v1",
    "data_opentelekomcloud_dds_flavors_v3",
    "data_opentelekomcloud_dds_instance_v3",
    "data_opentelekomcloud_deh_host_v1",
    "data_opentelekomcloud_deh_server_v1",
    "data_opentelekomcloud_direct_connect_v2",
    "data_opentelekomcloud_dms_az_v1",
    "data_opentelekomcloud_dms_flavor_v2",
    "data_opentelekomcloud_dms_maintainwindow_v1",
    "data_opentelekomcloud_dms_product_v1",
    "data_opentelekomcloud_dns_nameservers_v2",
    "data_opentelekomcloud_dns_zone_v2",
    "data_opentelekomcloud_dws_flavors_v2",
    "data_opentelekomcloud_enterprise_vpn_connection_v5",
    "data_opentelekomcloud_enterprise_vpn_customer_gateway_v5",
    "data_opentelekomcloud_enterprise_vpn_gateway_v5",
    "data_opentelekomcloud_er_associations_v3",
    "data_opentelekomcloud_er_availability_zones_v3",
    "data_opentelekomcloud_er_flow_logs_v3",
    "data_opentelekomcloud_er_instances_v3",
    "data_opentelekomcloud_er_propagations_v3",
    "data_opentelekomcloud_er_quotas_v3",
    "data_opentelekomcloud_er_route_tables_v3",
    "data_opentelekomcloud_evs_volumes_v2",
    "data_opentelekomcloud_hss_host_groups_v5",
    "data_opentelekomcloud_hss_hosts_v5",
    "data_opentelekomcloud_hss_intrusion_events_v5",
    "data_opentelekomcloud_hss_quotas_v5",
    "data_opentelekomcloud_identity_agency_v3",
    "data_opentelekomcloud_identity_auth_scope_v3",
    "data_opentelekomcloud_identity_credential_v3",
    "data_opentelekomcloud_identity_group_v3",
    "data_opentelekomcloud_identity_project_v3",
    "data_opentelekomcloud_identity_projects_v3",
    "data_opentelekomcloud_identity_role_custom_v3",
    "data_opentelekomcloud_identity_role_v3",
    "data_opentelekomcloud_identity_user_v3",
    "data_opentelekomcloud_images_image_v2",
    "data_opentelekomcloud_kms_data_key_v1",
    "data_opentelekomcloud_kms_key_material_parameters_v1",
    "data_opentelekomcloud_kms_key_v1",
    "data_opentelekomcloud_lb_certificate_v3",
    "data_opentelekomcloud_lb_flavor_v3",
    "data_opentelekomcloud_lb_flavors_v3",
    "data_opentelekomcloud_lb_listener_v3",
    "data_opentelekomcloud_lb_loadbalancer_v3",
    "data_opentelekomcloud_lb_member_ids_v2",
    "data_opentelekomcloud_lts_groups_v2",
    "data_opentelekomcloud_lts_streams_v2",
    "data_opentelekomcloud_nat_dnat_rules_v2",
    "data_opentelekomcloud_nat_gateway_v2",
    "data_opentelekomcloud_nat_snat_rules_v2",
    "data_opentelekomcloud_networking_network_v2",
    "data_opentelekomcloud_networking_port_ids_v2",
    "data_opentelekomcloud_networking_port_v2",
    "data_opentelekomcloud_networking_secgroup_rule_ids_v2",
    "data_opentelekomcloud_networking_secgroup_v2",
    "data_opentelekomcloud_obs_bucket",
    "data_opentelekomcloud_obs_bucket_object",
    "data_opentelekomcloud_rds_backup_v3",
    "data_opentelekomcloud_rds_flavors_v1",
    "data_opentelekomcloud_rds_flavors_v3",
    "data_opentelekomcloud_rds_instance_v3",
    "data_opentelekomcloud_rds_versions_v3",
    "data_opentelekomcloud_rms_advanced_queries_v1",
    "data_opentelekomcloud_rms_advanced_query_schemas_v1",
    "data_opentelekomcloud_rms_advanced_query_v1",
    "data_opentelekomcloud_rms_policy_definitions_v1",
    "data_opentelekomcloud_rms_policy_states_v1",
    "data_opentelekomcloud_rms_regions_v1",
    "data_opentelekomcloud_rts_software_config_v1",
    "data_opentelekomcloud_rts_software_deployment_v1",
    "data_opentelekomcloud_rts_stack_resource_v1",
    "data_opentelekomcloud_rts_stack_v1",
    "data_opentelekomcloud_s3_bucket_object",
    "data_opentelekomcloud_sdrs_domain_v1",
    "data_opentelekomcloud_sfs_file_system_v2",
    "data_opentelekomcloud_sfs_turbo_share_v1",
    "data_opentelekomcloud_smn_message_templates_v2",
    "data_opentelekomcloud_smn_subscription_v2",
    "data_opentelekomcloud_smn_topic_subscription_v2",
    "data_opentelekomcloud_smn_topic_v2",
    "data_opentelekomcloud_tms_tags_v1",
    "data_opentelekomcloud_vbs_backup_policy_v2",
    "data_opentelekomcloud_vbs_backup_v2",
    "data_opentelekomcloud_vpc_bandwidth",
    "data_opentelekomcloud_vpc_bandwidth_v2",
    "data_opentelekomcloud_vpc_eip_v1",
    "data_opentelekomcloud_vpc_peering_connection_v2",
    "data_opentelekomcloud_vpc_route_ids_v2",
    "data_opentelekomcloud_vpc_route_table_v1",
    "data_opentelekomcloud_vpc_route_tables_v1",
    "data_opentelekomcloud_vpc_route_v2",
    "data_opentelekomcloud_vpc_subnet_ids_v1",
    "data_opentelekomcloud_vpc_subnet_v1",
    "data_opentelekomcloud_vpc_v1",
    "data_opentelekomcloud_vpcep_public_service_v1",
    "data_opentelekomcloud_vpcep_service_v1",
    "data_opentelekomcloud_vpnaas_service_v2",
    "data_opentelekomcloud_waf_dedicated_reference_tables_v1",
    "dc_endpoint_group_v2",
    "dc_hosted_connect_v3",
    "dc_virtual_gateway_v2",
    "dc_virtual_gateway_v3",
    "dc_virtual_interface_peer_v3",
    "dc_virtual_interface_v2",
    "dc_virtual_interface_v3",
    "dcs_instance_v1",
    "dcs_instance_v2",
    "ddm_instance_v1",
    "ddm_schema_v1",
    "dds_backup_v3",
    "dds_instance_v3",
    "dds_lts_log_v3",
    "deh_host_v1",
    "direct_connect_v2",
    "dis_app_v2",
    "dis_checkpoint_v2",
    "dis_dump_task_v2",
    "dis_stream_v2",
    "dms_consumer_group_v2",
    "dms_dedicated_instance_v2",
    "dms_instance_v1",
    "dms_instance_v2",
    "dms_reassign_partitions_v2",
    "dms_smart_connect_task_action_v2",
    "dms_smart_connect_task_v2",
    "dms_smart_connect_v2",
    "dms_topic_v1",
    "dms_topic_v2",
    "dms_user_permission_v1",
    "dms_user_v2",
    "dns_ptrrecord_v2",
    "dns_recordset_v2",
    "dns_zone_v2",
    "drs_task_v3",
    "dws_cluster_v1",
    "ecs_instance_v1",
    "enterprise_vpn_connection_monitor_v5",
    "enterprise_vpn_connection_v5",
    "enterprise_vpn_customer_gateway_v5",
    "enterprise_vpn_gateway_v5",
    "er_association_v3",
    "er_flow_log_v3",
    "er_instance_v3",
    "er_propagation_v3",
    "er_route_table_v3",
    "er_static_route_v3",
    "er_vpc_attachment_v3",
    "evs_volume_v3",
    "fgs_async_invoke_config_v2",
    "fgs_dependency_version_v2",
    "fgs_event_v2",
    "fgs_function_v2",
    "fgs_trigger_v2",
    "fw_firewall_group_v2",
    "fw_policy_v2",
    "fw_rule_v2",
    "gaussdb_mysql_instance_v3",
    "hss_host_group_v5",
    "hss_host_protection_v5",
    "identity_acl_v3",
    "identity_agency_v3",
    "identity_credential_v3",
    "identity_group_membership_v3",
    "identity_group_v3",
    "identity_login_policy_v3",
    "identity_mapping_v3",
    "identity_password_policy_v3",
    "identity_project_v3",
    "identity_protection_policy_v3",
    "identity_protocol_v3",
    "identity_provider",
    "identity_provider_v3",
    "identity_role_assignment_v3",
    "identity_role_v3",
    "identity_user_group_membership_v3",
    "identity_user_v3",
    "images_image_access_accept_v2",
    "images_image_access_v2",
    "images_image_v2",
    "ims_data_image_v2",
    "ims_image_share_accept_v1",
    "ims_image_share_v1",
    "ims_image_v2",
    "kms_grant_v1",
    "kms_key_material_v1",
    "kms_key_v1",
    "lb_certificate_v2",
    "lb_certificate_v3",
    "lb_ipgroup_v3",
    "lb_l7_policy_v2",
    "lb_l7_rule_v2",
    "lb_listener_v2",
    "lb_listener_v3",
    "lb_loadbalancer_v2",
    "lb_loadbalancer_v3",
    "lb_lts_log_v3",
    "lb_member_v2",
    "lb_member_v3",
    "lb_monitor_v2",
    "lb_monitor_v3",
    "lb_policy_v3",
    "lb_pool_v2",
    "lb_pool_v3",
    "lb_rule_v3",
    "lb_security_policy_v3",
    "lb_whitelist_v2",
    "logtank_group_v2",
    "logtank_topic_v2",
    "logtank_transfer_v2",
    "lts_cce_access_v3",
    "lts_cross_account_access_v2",
    "lts_group_v2",
    "lts_host_access_v3",
    "lts_host_group_v3",
    "lts_keywords_alarm_rule_v2",
    "lts_notification_template_v2",
    "lts_quick_search_criteria_v1",
    "lts_stream_v2",
    "lts_transfer_v2",
    "mrs_cluster_v1",
    "mrs_job_v1",
    "nat_dnat_rule_v2",
    "nat_gateway_v2",
    "nat_snat_rule_v2",
    "networking_floatingip_associate_v2",
    "networking_floatingip_v2",
    "networking_network_v2",
    "networking_port_secgroup_associate_v2",
    "networking_port_v2",
    "networking_router_interface_v2",
    "networking_router_route_v2",
    "networking_router_v2",
    "networking_secgroup_rule_v2",
    "networking_secgroup_v2",
    "networking_subnet_v2",
    "networking_vip_associate_v2",
    "networking_vip_v2",
    "obs_bucket",
    "obs_bucket_acl",
    "obs_bucket_inventory",
    "obs_bucket_object",
    "obs_bucket_object_acl",
    "obs_bucket_policy",
    "obs_bucket_replication",
    "provider",
    "rds_backup_v3",
    "rds_instance_v1",
    "rds_instance_v3",
    "rds_maintenance_v3",
    "rds_parametergroup_v3",
    "rds_public_ip_associate_v3",
    "rds_read_replica_v3",
    "rms_advanced_query_v1",
    "rms_policy_assignment_evaluate_v1",
    "rms_policy_assignment_v1",
    "rms_resource_recorder_v1",
    "rts_software_config_v1",
    "rts_software_deployment_v1",
    "rts_stack_v1",
    "s3_bucket",
    "s3_bucket_object",
    "s3_bucket_policy",
    "sdrs_protected_instance_v1",
    "sdrs_protectiongroup_v1",
    "sdrs_replication_attach_v1",
    "sdrs_replication_pair_v1",
    "sfs_file_system_v2",
    "sfs_share_access_rules_v2",
    "sfs_turbo_share_v1",
    "smn_message_template_v2",
    "smn_subscription_v2",
    "smn_topic_attribute_v2",
    "smn_topic_v2",
    "swr_domain_v2",
    "swr_organization_permissions_v2",
    "swr_organization_v2",
    "swr_repository_v2",
    "tms_tags_v1",
    "vbs_backup_policy_v2",
    "vbs_backup_share_v2",
    "vbs_backup_v2",
    "vpc_bandwidth_associate_v2",
    "vpc_bandwidth_v2",
    "vpc_eip_v1",
    "vpc_flow_log_v1",
    "vpc_peering_connection_accepter_v2",
    "vpc_peering_connection_v2",
    "vpc_route_table_v1",
    "vpc_route_v2",
    "vpc_subnet_v1",
    "vpc_v1",
    "vpcep_approval_v1",
    "vpcep_endpoint_v1",
    "vpcep_service_v1",
    "vpnaas_endpoint_group_v2",
    "vpnaas_ike_policy_v2",
    "vpnaas_ipsec_policy_v2",
    "vpnaas_service_v2",
    "vpnaas_site_connection_v2",
    "waf_alarm_notification_v1",
    "waf_ccattackprotection_rule_v1",
    "waf_certificate_v1",
    "waf_datamasking_rule_v1",
    "waf_dedicated_alarm_masking_rule_v1",
    "waf_dedicated_anti_crawler_rule_v1",
    "waf_dedicated_anti_leakage_rule_v1",
    "waf_dedicated_blacklist_rule_v1",
    "waf_dedicated_cc_rule_v1",
    "waf_dedicated_certificate_v1",
    "waf_dedicated_data_masking_rule_v1",
    "waf_dedicated_domain_v1",
    "waf_dedicated_geo_ip_rule_v1",
    "waf_dedicated_instance_v1",
    "waf_dedicated_known_attack_source_rule_v1",
    "waf_dedicated_policy_v1",
    "waf_dedicated_precise_protection_rule_v1",
    "waf_dedicated_reference_table_v1",
    "waf_dedicated_web_tamper_rule_v1",
    "waf_domain_v1",
    "waf_falsealarmmasking_rule_v1",
    "waf_policy_v1",
    "waf_preciseprotection_rule_v1",
    "waf_webtamperprotection_rule_v1",
    "waf_whiteblackip_rule_v1",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import antiddos_v1
from . import apigw_acl_policy_associate_v2
from . import apigw_acl_policy_v2
from . import apigw_api_publishment_v2
from . import apigw_api_v2
from . import apigw_appcode_v2
from . import apigw_application_authorization_v2
from . import apigw_application_v2
from . import apigw_certificate_v2
from . import apigw_custom_authorizer_v2
from . import apigw_environment_v2
from . import apigw_environment_variable_v2
from . import apigw_gateway_feature_v2
from . import apigw_gateway_routes_v2
from . import apigw_gateway_v2
from . import apigw_group_v2
from . import apigw_response_v2
from . import apigw_signature_associate_v2
from . import apigw_signature_v2
from . import apigw_throttling_policy_associate_v2
from . import apigw_throttling_policy_v2
from . import apigw_vpc_channel_v2
from . import as_configuration_v1
from . import as_group_v1
from . import as_lifecycle_hook_v1
from . import as_policy_v1
from . import as_policy_v2
from . import blockstorage_volume_v2
from . import cbr_policy_v3
from . import cbr_vault_v3
from . import cce_addon_v3
from . import cce_cluster_v3
from . import cce_node_attach_v3
from . import cce_node_pool_v3
from . import cce_node_v3
from . import cci_namespace_v2
from . import ces_alarmrule
from . import ces_event_report_v1
from . import ces_metric_data_v1
from . import cfw_acl_rule_v1
from . import cfw_address_group_member_v1
from . import cfw_address_group_v1
from . import cfw_blacklist_whitelist_rule_v1
from . import cfw_domain_name_group_v1
from . import cfw_eip_protection_v1
from . import cfw_firewall_v1
from . import cfw_ips_protection_v1
from . import cfw_service_group_member_v1
from . import cfw_service_group_v1
from . import compute_bms_server_v2
from . import compute_bms_tags_v2
from . import compute_floatingip_associate_v2
from . import compute_floatingip_v2
from . import compute_instance_v2
from . import compute_keypair_v2
from . import compute_secgroup_v2
from . import compute_servergroup_v2
from . import compute_volume_attach_v2
from . import csbs_backup_policy_v1
from . import csbs_backup_v1
from . import css_cluster_restart_v1
from . import css_cluster_v1
from . import css_configuration_v1
from . import css_snapshot_configuration_v1
from . import cts_event_notification_v3
from . import cts_tracker_v1
from . import cts_tracker_v3
from . import data_opentelekomcloud_antiddos_v1
from . import data_opentelekomcloud_apigw_api_history_v2
from . import data_opentelekomcloud_apigw_gateway_features_v2
from . import data_opentelekomcloud_cbr_backup_ids_v3
from . import data_opentelekomcloud_cbr_backup_v3
from . import data_opentelekomcloud_cce_addon_template_v3
from . import data_opentelekomcloud_cce_addon_templates_v3
from . import data_opentelekomcloud_cce_cluster_kubeconfig_v3
from . import data_opentelekomcloud_cce_cluster_v3
from . import data_opentelekomcloud_cce_clusters_v3
from . import data_opentelekomcloud_cce_node_ids_v3
from . import data_opentelekomcloud_cce_node_v3
from . import data_opentelekomcloud_ces_event_details_v1
from . import data_opentelekomcloud_ces_events_v1
from . import data_opentelekomcloud_ces_metric_data_v1
from . import data_opentelekomcloud_ces_metrics_v1
from . import data_opentelekomcloud_ces_multiple_metric_data_v1
from . import data_opentelekomcloud_ces_quotas_v1
from . import data_opentelekomcloud_cfw_firewall_v1
from . import data_opentelekomcloud_compute_availability_zones_v2
from . import data_opentelekomcloud_compute_bms_flavors_v2
from . import data_opentelekomcloud_compute_bms_keypairs_v2
from . import data_opentelekomcloud_compute_bms_nic_v2
from . import data_opentelekomcloud_compute_bms_server_v2
from . import data_opentelekomcloud_compute_flavor_v2
from . import data_opentelekomcloud_compute_instance_v2
from . import data_opentelekomcloud_compute_instances_v2
from . import data_opentelekomcloud_compute_keypair_v2
from . import data_opentelekomcloud_csbs_backup_policy_v1
from . import data_opentelekomcloud_csbs_backup_v1
from . import data_opentelekomcloud_css_certificate_v1
from . import data_opentelekomcloud_css_flavor_v1
from . import data_opentelekomcloud_cts_tracker_v1
from . import data_opentelekomcloud_dcs_az_v1
from . import data_opentelekomcloud_dcs_certificate_v2
from . import data_opentelekomcloud_dcs_maintainwindow_v1
from . import data_opentelekomcloud_dcs_product_v1
from . import data_opentelekomcloud_ddm_engines_v1
from . import data_opentelekomcloud_ddm_flavors_v1
from . import data_opentelekomcloud_ddm_instance_v1
from . import data_opentelekomcloud_dds_flavors_v3
from . import data_opentelekomcloud_dds_instance_v3
from . import data_opentelekomcloud_deh_host_v1
from . import data_opentelekomcloud_deh_server_v1
from . import data_opentelekomcloud_direct_connect_v2
from . import data_opentelekomcloud_dms_az_v1
from . import data_opentelekomcloud_dms_flavor_v2
from . import data_opentelekomcloud_dms_maintainwindow_v1
from . import data_opentelekomcloud_dms_product_v1
from . import data_opentelekomcloud_dns_nameservers_v2
from . import data_opentelekomcloud_dns_zone_v2
from . import data_opentelekomcloud_dws_flavors_v2
from . import data_opentelekomcloud_enterprise_vpn_connection_v5
from . import data_opentelekomcloud_enterprise_vpn_customer_gateway_v5
from . import data_opentelekomcloud_enterprise_vpn_gateway_v5
from . import data_opentelekomcloud_er_associations_v3
from . import data_opentelekomcloud_er_availability_zones_v3
from . import data_opentelekomcloud_er_flow_logs_v3
from . import data_opentelekomcloud_er_instances_v3
from . import data_opentelekomcloud_er_propagations_v3
from . import data_opentelekomcloud_er_quotas_v3
from . import data_opentelekomcloud_er_route_tables_v3
from . import data_opentelekomcloud_evs_volumes_v2
from . import data_opentelekomcloud_hss_host_groups_v5
from . import data_opentelekomcloud_hss_hosts_v5
from . import data_opentelekomcloud_hss_intrusion_events_v5
from . import data_opentelekomcloud_hss_quotas_v5
from . import data_opentelekomcloud_identity_agency_v3
from . import data_opentelekomcloud_identity_auth_scope_v3
from . import data_opentelekomcloud_identity_credential_v3
from . import data_opentelekomcloud_identity_group_v3
from . import data_opentelekomcloud_identity_project_v3
from . import data_opentelekomcloud_identity_projects_v3
from . import data_opentelekomcloud_identity_role_custom_v3
from . import data_opentelekomcloud_identity_role_v3
from . import data_opentelekomcloud_identity_user_v3
from . import data_opentelekomcloud_images_image_v2
from . import data_opentelekomcloud_kms_data_key_v1
from . import data_opentelekomcloud_kms_key_material_parameters_v1
from . import data_opentelekomcloud_kms_key_v1
from . import data_opentelekomcloud_lb_certificate_v3
from . import data_opentelekomcloud_lb_flavor_v3
from . import data_opentelekomcloud_lb_flavors_v3
from . import data_opentelekomcloud_lb_listener_v3
from . import data_opentelekomcloud_lb_loadbalancer_v3
from . import data_opentelekomcloud_lb_member_ids_v2
from . import data_opentelekomcloud_lts_groups_v2
from . import data_opentelekomcloud_lts_streams_v2
from . import data_opentelekomcloud_nat_dnat_rules_v2
from . import data_opentelekomcloud_nat_gateway_v2
from . import data_opentelekomcloud_nat_snat_rules_v2
from . import data_opentelekomcloud_networking_network_v2
from . import data_opentelekomcloud_networking_port_ids_v2
from . import data_opentelekomcloud_networking_port_v2
from . import data_opentelekomcloud_networking_secgroup_rule_ids_v2
from . import data_opentelekomcloud_networking_secgroup_v2
from . import data_opentelekomcloud_obs_bucket
from . import data_opentelekomcloud_obs_bucket_object
from . import data_opentelekomcloud_rds_backup_v3
from . import data_opentelekomcloud_rds_flavors_v1
from . import data_opentelekomcloud_rds_flavors_v3
from . import data_opentelekomcloud_rds_instance_v3
from . import data_opentelekomcloud_rds_versions_v3
from . import data_opentelekomcloud_rms_advanced_queries_v1
from . import data_opentelekomcloud_rms_advanced_query_schemas_v1
from . import data_opentelekomcloud_rms_advanced_query_v1
from . import data_opentelekomcloud_rms_policy_definitions_v1
from . import data_opentelekomcloud_rms_policy_states_v1
from . import data_opentelekomcloud_rms_regions_v1
from . import data_opentelekomcloud_rts_software_config_v1
from . import data_opentelekomcloud_rts_software_deployment_v1
from . import data_opentelekomcloud_rts_stack_resource_v1
from . import data_opentelekomcloud_rts_stack_v1
from . import data_opentelekomcloud_s3_bucket_object
from . import data_opentelekomcloud_sdrs_domain_v1
from . import data_opentelekomcloud_sfs_file_system_v2
from . import data_opentelekomcloud_sfs_turbo_share_v1
from . import data_opentelekomcloud_smn_message_templates_v2
from . import data_opentelekomcloud_smn_subscription_v2
from . import data_opentelekomcloud_smn_topic_subscription_v2
from . import data_opentelekomcloud_smn_topic_v2
from . import data_opentelekomcloud_tms_tags_v1
from . import data_opentelekomcloud_vbs_backup_policy_v2
from . import data_opentelekomcloud_vbs_backup_v2
from . import data_opentelekomcloud_vpc_bandwidth
from . import data_opentelekomcloud_vpc_bandwidth_v2
from . import data_opentelekomcloud_vpc_eip_v1
from . import data_opentelekomcloud_vpc_peering_connection_v2
from . import data_opentelekomcloud_vpc_route_ids_v2
from . import data_opentelekomcloud_vpc_route_table_v1
from . import data_opentelekomcloud_vpc_route_tables_v1
from . import data_opentelekomcloud_vpc_route_v2
from . import data_opentelekomcloud_vpc_subnet_ids_v1
from . import data_opentelekomcloud_vpc_subnet_v1
from . import data_opentelekomcloud_vpc_v1
from . import data_opentelekomcloud_vpcep_public_service_v1
from . import data_opentelekomcloud_vpcep_service_v1
from . import data_opentelekomcloud_vpnaas_service_v2
from . import data_opentelekomcloud_waf_dedicated_reference_tables_v1
from . import dc_endpoint_group_v2
from . import dc_hosted_connect_v3
from . import dc_virtual_gateway_v2
from . import dc_virtual_gateway_v3
from . import dc_virtual_interface_peer_v3
from . import dc_virtual_interface_v2
from . import dc_virtual_interface_v3
from . import dcs_instance_v1
from . import dcs_instance_v2
from . import ddm_instance_v1
from . import ddm_schema_v1
from . import dds_backup_v3
from . import dds_instance_v3
from . import dds_lts_log_v3
from . import deh_host_v1
from . import direct_connect_v2
from . import dis_app_v2
from . import dis_checkpoint_v2
from . import dis_dump_task_v2
from . import dis_stream_v2
from . import dms_consumer_group_v2
from . import dms_dedicated_instance_v2
from . import dms_instance_v1
from . import dms_instance_v2
from . import dms_reassign_partitions_v2
from . import dms_smart_connect_task_action_v2
from . import dms_smart_connect_task_v2
from . import dms_smart_connect_v2
from . import dms_topic_v1
from . import dms_topic_v2
from . import dms_user_permission_v1
from . import dms_user_v2
from . import dns_ptrrecord_v2
from . import dns_recordset_v2
from . import dns_zone_v2
from . import drs_task_v3
from . import dws_cluster_v1
from . import ecs_instance_v1
from . import enterprise_vpn_connection_monitor_v5
from . import enterprise_vpn_connection_v5
from . import enterprise_vpn_customer_gateway_v5
from . import enterprise_vpn_gateway_v5
from . import er_association_v3
from . import er_flow_log_v3
from . import er_instance_v3
from . import er_propagation_v3
from . import er_route_table_v3
from . import er_static_route_v3
from . import er_vpc_attachment_v3
from . import evs_volume_v3
from . import fgs_async_invoke_config_v2
from . import fgs_dependency_version_v2
from . import fgs_event_v2
from . import fgs_function_v2
from . import fgs_trigger_v2
from . import fw_firewall_group_v2
from . import fw_policy_v2
from . import fw_rule_v2
from . import gaussdb_mysql_instance_v3
from . import hss_host_group_v5
from . import hss_host_protection_v5
from . import identity_acl_v3
from . import identity_agency_v3
from . import identity_credential_v3
from . import identity_group_membership_v3
from . import identity_group_v3
from . import identity_login_policy_v3
from . import identity_mapping_v3
from . import identity_password_policy_v3
from . import identity_project_v3
from . import identity_protection_policy_v3
from . import identity_protocol_v3
from . import identity_provider
from . import identity_provider_v3
from . import identity_role_assignment_v3
from . import identity_role_v3
from . import identity_user_group_membership_v3
from . import identity_user_v3
from . import images_image_access_accept_v2
from . import images_image_access_v2
from . import images_image_v2
from . import ims_data_image_v2
from . import ims_image_share_accept_v1
from . import ims_image_share_v1
from . import ims_image_v2
from . import kms_grant_v1
from . import kms_key_material_v1
from . import kms_key_v1
from . import lb_certificate_v2
from . import lb_certificate_v3
from . import lb_ipgroup_v3
from . import lb_l7_policy_v2
from . import lb_l7_rule_v2
from . import lb_listener_v2
from . import lb_listener_v3
from . import lb_loadbalancer_v2
from . import lb_loadbalancer_v3
from . import lb_lts_log_v3
from . import lb_member_v2
from . import lb_member_v3
from . import lb_monitor_v2
from . import lb_monitor_v3
from . import lb_policy_v3
from . import lb_pool_v2
from . import lb_pool_v3
from . import lb_rule_v3
from . import lb_security_policy_v3
from . import lb_whitelist_v2
from . import logtank_group_v2
from . import logtank_topic_v2
from . import logtank_transfer_v2
from . import lts_cce_access_v3
from . import lts_cross_account_access_v2
from . import lts_group_v2
from . import lts_host_access_v3
from . import lts_host_group_v3
from . import lts_keywords_alarm_rule_v2
from . import lts_notification_template_v2
from . import lts_quick_search_criteria_v1
from . import lts_stream_v2
from . import lts_transfer_v2
from . import mrs_cluster_v1
from . import mrs_job_v1
from . import nat_dnat_rule_v2
from . import nat_gateway_v2
from . import nat_snat_rule_v2
from . import networking_floatingip_associate_v2
from . import networking_floatingip_v2
from . import networking_network_v2
from . import networking_port_secgroup_associate_v2
from . import networking_port_v2
from . import networking_router_interface_v2
from . import networking_router_route_v2
from . import networking_router_v2
from . import networking_secgroup_rule_v2
from . import networking_secgroup_v2
from . import networking_subnet_v2
from . import networking_vip_associate_v2
from . import networking_vip_v2
from . import obs_bucket
from . import obs_bucket_acl
from . import obs_bucket_inventory
from . import obs_bucket_object
from . import obs_bucket_object_acl
from . import obs_bucket_policy
from . import obs_bucket_replication
from . import provider
from . import rds_backup_v3
from . import rds_instance_v1
from . import rds_instance_v3
from . import rds_maintenance_v3
from . import rds_parametergroup_v3
from . import rds_public_ip_associate_v3
from . import rds_read_replica_v3
from . import rms_advanced_query_v1
from . import rms_policy_assignment_evaluate_v1
from . import rms_policy_assignment_v1
from . import rms_resource_recorder_v1
from . import rts_software_config_v1
from . import rts_software_deployment_v1
from . import rts_stack_v1
from . import s3_bucket
from . import s3_bucket_object
from . import s3_bucket_policy
from . import sdrs_protected_instance_v1
from . import sdrs_protectiongroup_v1
from . import sdrs_replication_attach_v1
from . import sdrs_replication_pair_v1
from . import sfs_file_system_v2
from . import sfs_share_access_rules_v2
from . import sfs_turbo_share_v1
from . import smn_message_template_v2
from . import smn_subscription_v2
from . import smn_topic_attribute_v2
from . import smn_topic_v2
from . import swr_domain_v2
from . import swr_organization_permissions_v2
from . import swr_organization_v2
from . import swr_repository_v2
from . import tms_tags_v1
from . import vbs_backup_policy_v2
from . import vbs_backup_share_v2
from . import vbs_backup_v2
from . import vpc_bandwidth_associate_v2
from . import vpc_bandwidth_v2
from . import vpc_eip_v1
from . import vpc_flow_log_v1
from . import vpc_peering_connection_accepter_v2
from . import vpc_peering_connection_v2
from . import vpc_route_table_v1
from . import vpc_route_v2
from . import vpc_subnet_v1
from . import vpc_v1
from . import vpcep_approval_v1
from . import vpcep_endpoint_v1
from . import vpcep_service_v1
from . import vpnaas_endpoint_group_v2
from . import vpnaas_ike_policy_v2
from . import vpnaas_ipsec_policy_v2
from . import vpnaas_service_v2
from . import vpnaas_site_connection_v2
from . import waf_alarm_notification_v1
from . import waf_ccattackprotection_rule_v1
from . import waf_certificate_v1
from . import waf_datamasking_rule_v1
from . import waf_dedicated_alarm_masking_rule_v1
from . import waf_dedicated_anti_crawler_rule_v1
from . import waf_dedicated_anti_leakage_rule_v1
from . import waf_dedicated_blacklist_rule_v1
from . import waf_dedicated_cc_rule_v1
from . import waf_dedicated_certificate_v1
from . import waf_dedicated_data_masking_rule_v1
from . import waf_dedicated_domain_v1
from . import waf_dedicated_geo_ip_rule_v1
from . import waf_dedicated_instance_v1
from . import waf_dedicated_known_attack_source_rule_v1
from . import waf_dedicated_policy_v1
from . import waf_dedicated_precise_protection_rule_v1
from . import waf_dedicated_reference_table_v1
from . import waf_dedicated_web_tamper_rule_v1
from . import waf_domain_v1
from . import waf_falsealarmmasking_rule_v1
from . import waf_policy_v1
from . import waf_preciseprotection_rule_v1
from . import waf_webtamperprotection_rule_v1
from . import waf_whiteblackip_rule_v1
