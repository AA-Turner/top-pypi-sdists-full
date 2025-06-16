r'''
# `provider`

Refer to the Terraform Registry for docs: [`google-beta`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class GoogleBetaProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.provider.GoogleBetaProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs google-beta}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_approval_custom_endpoint: typing.Optional[builtins.str] = None,
        access_context_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        access_token: typing.Optional[builtins.str] = None,
        active_directory_custom_endpoint: typing.Optional[builtins.str] = None,
        add_terraform_attribution_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        alias: typing.Optional[builtins.str] = None,
        alloydb_custom_endpoint: typing.Optional[builtins.str] = None,
        api_gateway_custom_endpoint: typing.Optional[builtins.str] = None,
        apigee_custom_endpoint: typing.Optional[builtins.str] = None,
        apihub_custom_endpoint: typing.Optional[builtins.str] = None,
        apikeys_custom_endpoint: typing.Optional[builtins.str] = None,
        app_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        apphub_custom_endpoint: typing.Optional[builtins.str] = None,
        artifact_registry_custom_endpoint: typing.Optional[builtins.str] = None,
        assured_workloads_custom_endpoint: typing.Optional[builtins.str] = None,
        backup_dr_custom_endpoint: typing.Optional[builtins.str] = None,
        batching: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBetaProviderBatching", typing.Dict[builtins.str, typing.Any]]]]] = None,
        beyondcorp_custom_endpoint: typing.Optional[builtins.str] = None,
        biglake_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_analytics_hub_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_connection_custom_endpoint: typing.Optional[builtins.str] = None,
        big_query_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_datapolicy_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_data_transfer_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_reservation_custom_endpoint: typing.Optional[builtins.str] = None,
        bigtable_custom_endpoint: typing.Optional[builtins.str] = None,
        billing_custom_endpoint: typing.Optional[builtins.str] = None,
        billing_project: typing.Optional[builtins.str] = None,
        binary_authorization_custom_endpoint: typing.Optional[builtins.str] = None,
        blockchain_node_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        certificate_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        chronicle_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_asset_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_billing_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_build_custom_endpoint: typing.Optional[builtins.str] = None,
        cloudbuildv2_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_build_worker_pool_custom_endpoint: typing.Optional[builtins.str] = None,
        clouddeploy_custom_endpoint: typing.Optional[builtins.str] = None,
        clouddomains_custom_endpoint: typing.Optional[builtins.str] = None,
        cloudfunctions2_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_functions_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_identity_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_ids_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_quotas_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_run_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_run_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_scheduler_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_tasks_custom_endpoint: typing.Optional[builtins.str] = None,
        colab_custom_endpoint: typing.Optional[builtins.str] = None,
        composer_custom_endpoint: typing.Optional[builtins.str] = None,
        compute_custom_endpoint: typing.Optional[builtins.str] = None,
        container_analysis_custom_endpoint: typing.Optional[builtins.str] = None,
        container_attached_custom_endpoint: typing.Optional[builtins.str] = None,
        container_aws_custom_endpoint: typing.Optional[builtins.str] = None,
        container_azure_custom_endpoint: typing.Optional[builtins.str] = None,
        container_custom_endpoint: typing.Optional[builtins.str] = None,
        core_billing_custom_endpoint: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        database_migration_service_custom_endpoint: typing.Optional[builtins.str] = None,
        data_catalog_custom_endpoint: typing.Optional[builtins.str] = None,
        dataflow_custom_endpoint: typing.Optional[builtins.str] = None,
        dataform_custom_endpoint: typing.Optional[builtins.str] = None,
        data_fusion_custom_endpoint: typing.Optional[builtins.str] = None,
        data_loss_prevention_custom_endpoint: typing.Optional[builtins.str] = None,
        data_pipeline_custom_endpoint: typing.Optional[builtins.str] = None,
        dataplex_custom_endpoint: typing.Optional[builtins.str] = None,
        dataproc_custom_endpoint: typing.Optional[builtins.str] = None,
        dataproc_gdc_custom_endpoint: typing.Optional[builtins.str] = None,
        dataproc_metastore_custom_endpoint: typing.Optional[builtins.str] = None,
        datastream_custom_endpoint: typing.Optional[builtins.str] = None,
        default_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        deployment_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        developer_connect_custom_endpoint: typing.Optional[builtins.str] = None,
        dialogflow_custom_endpoint: typing.Optional[builtins.str] = None,
        dialogflow_cx_custom_endpoint: typing.Optional[builtins.str] = None,
        discovery_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        dns_custom_endpoint: typing.Optional[builtins.str] = None,
        document_ai_custom_endpoint: typing.Optional[builtins.str] = None,
        document_ai_warehouse_custom_endpoint: typing.Optional[builtins.str] = None,
        edgecontainer_custom_endpoint: typing.Optional[builtins.str] = None,
        edgenetwork_custom_endpoint: typing.Optional[builtins.str] = None,
        essential_contacts_custom_endpoint: typing.Optional[builtins.str] = None,
        eventarc_custom_endpoint: typing.Optional[builtins.str] = None,
        external_credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBetaProviderExternalCredentials", typing.Dict[builtins.str, typing.Any]]]]] = None,
        filestore_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_app_check_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_app_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_database_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_data_connect_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_extensions_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
        firebaserules_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_storage_custom_endpoint: typing.Optional[builtins.str] = None,
        firestore_custom_endpoint: typing.Optional[builtins.str] = None,
        gemini_custom_endpoint: typing.Optional[builtins.str] = None,
        gke_backup_custom_endpoint: typing.Optional[builtins.str] = None,
        gke_hub2_custom_endpoint: typing.Optional[builtins.str] = None,
        gke_hub_custom_endpoint: typing.Optional[builtins.str] = None,
        gkehub_feature_custom_endpoint: typing.Optional[builtins.str] = None,
        gkeonprem_custom_endpoint: typing.Optional[builtins.str] = None,
        healthcare_custom_endpoint: typing.Optional[builtins.str] = None,
        iam2_custom_endpoint: typing.Optional[builtins.str] = None,
        iam3_custom_endpoint: typing.Optional[builtins.str] = None,
        iam_beta_custom_endpoint: typing.Optional[builtins.str] = None,
        iam_credentials_custom_endpoint: typing.Optional[builtins.str] = None,
        iam_custom_endpoint: typing.Optional[builtins.str] = None,
        iam_workforce_pool_custom_endpoint: typing.Optional[builtins.str] = None,
        iap_custom_endpoint: typing.Optional[builtins.str] = None,
        identity_platform_custom_endpoint: typing.Optional[builtins.str] = None,
        impersonate_service_account: typing.Optional[builtins.str] = None,
        impersonate_service_account_delegates: typing.Optional[typing.Sequence[builtins.str]] = None,
        integration_connectors_custom_endpoint: typing.Optional[builtins.str] = None,
        integrations_custom_endpoint: typing.Optional[builtins.str] = None,
        kms_custom_endpoint: typing.Optional[builtins.str] = None,
        logging_custom_endpoint: typing.Optional[builtins.str] = None,
        looker_custom_endpoint: typing.Optional[builtins.str] = None,
        lustre_custom_endpoint: typing.Optional[builtins.str] = None,
        managed_kafka_custom_endpoint: typing.Optional[builtins.str] = None,
        memcache_custom_endpoint: typing.Optional[builtins.str] = None,
        memorystore_custom_endpoint: typing.Optional[builtins.str] = None,
        migration_center_custom_endpoint: typing.Optional[builtins.str] = None,
        ml_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        monitoring_custom_endpoint: typing.Optional[builtins.str] = None,
        netapp_custom_endpoint: typing.Optional[builtins.str] = None,
        network_connectivity_custom_endpoint: typing.Optional[builtins.str] = None,
        network_management_custom_endpoint: typing.Optional[builtins.str] = None,
        network_security_custom_endpoint: typing.Optional[builtins.str] = None,
        network_services_custom_endpoint: typing.Optional[builtins.str] = None,
        notebooks_custom_endpoint: typing.Optional[builtins.str] = None,
        oracle_database_custom_endpoint: typing.Optional[builtins.str] = None,
        org_policy_custom_endpoint: typing.Optional[builtins.str] = None,
        os_config_custom_endpoint: typing.Optional[builtins.str] = None,
        os_config_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        os_login_custom_endpoint: typing.Optional[builtins.str] = None,
        parallelstore_custom_endpoint: typing.Optional[builtins.str] = None,
        parameter_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        parameter_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
        privateca_custom_endpoint: typing.Optional[builtins.str] = None,
        privileged_access_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        public_ca_custom_endpoint: typing.Optional[builtins.str] = None,
        pubsub_custom_endpoint: typing.Optional[builtins.str] = None,
        pubsub_lite_custom_endpoint: typing.Optional[builtins.str] = None,
        recaptcha_enterprise_custom_endpoint: typing.Optional[builtins.str] = None,
        redis_custom_endpoint: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        request_reason: typing.Optional[builtins.str] = None,
        request_timeout: typing.Optional[builtins.str] = None,
        resource_manager3_custom_endpoint: typing.Optional[builtins.str] = None,
        resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        resource_manager_v3_custom_endpoint: typing.Optional[builtins.str] = None,
        runtimeconfig_custom_endpoint: typing.Optional[builtins.str] = None,
        runtime_config_custom_endpoint: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        secret_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
        secure_source_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_management_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        securityposture_custom_endpoint: typing.Optional[builtins.str] = None,
        security_scanner_custom_endpoint: typing.Optional[builtins.str] = None,
        service_directory_custom_endpoint: typing.Optional[builtins.str] = None,
        service_management_custom_endpoint: typing.Optional[builtins.str] = None,
        service_networking_custom_endpoint: typing.Optional[builtins.str] = None,
        service_usage_custom_endpoint: typing.Optional[builtins.str] = None,
        site_verification_custom_endpoint: typing.Optional[builtins.str] = None,
        source_repo_custom_endpoint: typing.Optional[builtins.str] = None,
        spanner_custom_endpoint: typing.Optional[builtins.str] = None,
        sql_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_batch_operations_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_control_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_insights_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_transfer_custom_endpoint: typing.Optional[builtins.str] = None,
        tags_custom_endpoint: typing.Optional[builtins.str] = None,
        tags_location_custom_endpoint: typing.Optional[builtins.str] = None,
        terraform_attribution_label_addition_strategy: typing.Optional[builtins.str] = None,
        tpu_custom_endpoint: typing.Optional[builtins.str] = None,
        tpu_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        transcoder_custom_endpoint: typing.Optional[builtins.str] = None,
        universe_domain: typing.Optional[builtins.str] = None,
        user_project_override: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vertex_ai_custom_endpoint: typing.Optional[builtins.str] = None,
        vmwareengine_custom_endpoint: typing.Optional[builtins.str] = None,
        vpc_access_custom_endpoint: typing.Optional[builtins.str] = None,
        workbench_custom_endpoint: typing.Optional[builtins.str] = None,
        workflows_custom_endpoint: typing.Optional[builtins.str] = None,
        workstations_custom_endpoint: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs google-beta} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_approval_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#access_approval_custom_endpoint GoogleBetaProvider#access_approval_custom_endpoint}.
        :param access_context_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#access_context_manager_custom_endpoint GoogleBetaProvider#access_context_manager_custom_endpoint}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#access_token GoogleBetaProvider#access_token}.
        :param active_directory_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#active_directory_custom_endpoint GoogleBetaProvider#active_directory_custom_endpoint}.
        :param add_terraform_attribution_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#add_terraform_attribution_label GoogleBetaProvider#add_terraform_attribution_label}.
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#alias GoogleBetaProvider#alias}
        :param alloydb_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#alloydb_custom_endpoint GoogleBetaProvider#alloydb_custom_endpoint}.
        :param api_gateway_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#api_gateway_custom_endpoint GoogleBetaProvider#api_gateway_custom_endpoint}.
        :param apigee_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apigee_custom_endpoint GoogleBetaProvider#apigee_custom_endpoint}.
        :param apihub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apihub_custom_endpoint GoogleBetaProvider#apihub_custom_endpoint}.
        :param apikeys_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apikeys_custom_endpoint GoogleBetaProvider#apikeys_custom_endpoint}.
        :param app_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#app_engine_custom_endpoint GoogleBetaProvider#app_engine_custom_endpoint}.
        :param apphub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apphub_custom_endpoint GoogleBetaProvider#apphub_custom_endpoint}.
        :param artifact_registry_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#artifact_registry_custom_endpoint GoogleBetaProvider#artifact_registry_custom_endpoint}.
        :param assured_workloads_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#assured_workloads_custom_endpoint GoogleBetaProvider#assured_workloads_custom_endpoint}.
        :param backup_dr_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#backup_dr_custom_endpoint GoogleBetaProvider#backup_dr_custom_endpoint}.
        :param batching: batching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#batching GoogleBetaProvider#batching}
        :param beyondcorp_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#beyondcorp_custom_endpoint GoogleBetaProvider#beyondcorp_custom_endpoint}.
        :param biglake_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#biglake_custom_endpoint GoogleBetaProvider#biglake_custom_endpoint}.
        :param bigquery_analytics_hub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_analytics_hub_custom_endpoint GoogleBetaProvider#bigquery_analytics_hub_custom_endpoint}.
        :param bigquery_connection_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_connection_custom_endpoint GoogleBetaProvider#bigquery_connection_custom_endpoint}.
        :param big_query_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#big_query_custom_endpoint GoogleBetaProvider#big_query_custom_endpoint}.
        :param bigquery_datapolicy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_datapolicy_custom_endpoint GoogleBetaProvider#bigquery_datapolicy_custom_endpoint}.
        :param bigquery_data_transfer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_data_transfer_custom_endpoint GoogleBetaProvider#bigquery_data_transfer_custom_endpoint}.
        :param bigquery_reservation_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_reservation_custom_endpoint GoogleBetaProvider#bigquery_reservation_custom_endpoint}.
        :param bigtable_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigtable_custom_endpoint GoogleBetaProvider#bigtable_custom_endpoint}.
        :param billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#billing_custom_endpoint GoogleBetaProvider#billing_custom_endpoint}.
        :param billing_project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#billing_project GoogleBetaProvider#billing_project}.
        :param binary_authorization_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#binary_authorization_custom_endpoint GoogleBetaProvider#binary_authorization_custom_endpoint}.
        :param blockchain_node_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#blockchain_node_engine_custom_endpoint GoogleBetaProvider#blockchain_node_engine_custom_endpoint}.
        :param certificate_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#certificate_manager_custom_endpoint GoogleBetaProvider#certificate_manager_custom_endpoint}.
        :param chronicle_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#chronicle_custom_endpoint GoogleBetaProvider#chronicle_custom_endpoint}.
        :param cloud_asset_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_asset_custom_endpoint GoogleBetaProvider#cloud_asset_custom_endpoint}.
        :param cloud_billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_billing_custom_endpoint GoogleBetaProvider#cloud_billing_custom_endpoint}.
        :param cloud_build_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_build_custom_endpoint GoogleBetaProvider#cloud_build_custom_endpoint}.
        :param cloudbuildv2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloudbuildv2_custom_endpoint GoogleBetaProvider#cloudbuildv2_custom_endpoint}.
        :param cloud_build_worker_pool_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_build_worker_pool_custom_endpoint GoogleBetaProvider#cloud_build_worker_pool_custom_endpoint}.
        :param clouddeploy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#clouddeploy_custom_endpoint GoogleBetaProvider#clouddeploy_custom_endpoint}.
        :param clouddomains_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#clouddomains_custom_endpoint GoogleBetaProvider#clouddomains_custom_endpoint}.
        :param cloudfunctions2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloudfunctions2_custom_endpoint GoogleBetaProvider#cloudfunctions2_custom_endpoint}.
        :param cloud_functions_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_functions_custom_endpoint GoogleBetaProvider#cloud_functions_custom_endpoint}.
        :param cloud_identity_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_identity_custom_endpoint GoogleBetaProvider#cloud_identity_custom_endpoint}.
        :param cloud_ids_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_ids_custom_endpoint GoogleBetaProvider#cloud_ids_custom_endpoint}.
        :param cloud_quotas_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_quotas_custom_endpoint GoogleBetaProvider#cloud_quotas_custom_endpoint}.
        :param cloud_resource_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_resource_manager_custom_endpoint GoogleBetaProvider#cloud_resource_manager_custom_endpoint}.
        :param cloud_run_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_run_custom_endpoint GoogleBetaProvider#cloud_run_custom_endpoint}.
        :param cloud_run_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_run_v2_custom_endpoint GoogleBetaProvider#cloud_run_v2_custom_endpoint}.
        :param cloud_scheduler_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_scheduler_custom_endpoint GoogleBetaProvider#cloud_scheduler_custom_endpoint}.
        :param cloud_tasks_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_tasks_custom_endpoint GoogleBetaProvider#cloud_tasks_custom_endpoint}.
        :param colab_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#colab_custom_endpoint GoogleBetaProvider#colab_custom_endpoint}.
        :param composer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#composer_custom_endpoint GoogleBetaProvider#composer_custom_endpoint}.
        :param compute_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#compute_custom_endpoint GoogleBetaProvider#compute_custom_endpoint}.
        :param container_analysis_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_analysis_custom_endpoint GoogleBetaProvider#container_analysis_custom_endpoint}.
        :param container_attached_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_attached_custom_endpoint GoogleBetaProvider#container_attached_custom_endpoint}.
        :param container_aws_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_aws_custom_endpoint GoogleBetaProvider#container_aws_custom_endpoint}.
        :param container_azure_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_azure_custom_endpoint GoogleBetaProvider#container_azure_custom_endpoint}.
        :param container_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_custom_endpoint GoogleBetaProvider#container_custom_endpoint}.
        :param core_billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#core_billing_custom_endpoint GoogleBetaProvider#core_billing_custom_endpoint}.
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#credentials GoogleBetaProvider#credentials}.
        :param database_migration_service_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#database_migration_service_custom_endpoint GoogleBetaProvider#database_migration_service_custom_endpoint}.
        :param data_catalog_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_catalog_custom_endpoint GoogleBetaProvider#data_catalog_custom_endpoint}.
        :param dataflow_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataflow_custom_endpoint GoogleBetaProvider#dataflow_custom_endpoint}.
        :param dataform_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataform_custom_endpoint GoogleBetaProvider#dataform_custom_endpoint}.
        :param data_fusion_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_fusion_custom_endpoint GoogleBetaProvider#data_fusion_custom_endpoint}.
        :param data_loss_prevention_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_loss_prevention_custom_endpoint GoogleBetaProvider#data_loss_prevention_custom_endpoint}.
        :param data_pipeline_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_pipeline_custom_endpoint GoogleBetaProvider#data_pipeline_custom_endpoint}.
        :param dataplex_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataplex_custom_endpoint GoogleBetaProvider#dataplex_custom_endpoint}.
        :param dataproc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataproc_custom_endpoint GoogleBetaProvider#dataproc_custom_endpoint}.
        :param dataproc_gdc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataproc_gdc_custom_endpoint GoogleBetaProvider#dataproc_gdc_custom_endpoint}.
        :param dataproc_metastore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataproc_metastore_custom_endpoint GoogleBetaProvider#dataproc_metastore_custom_endpoint}.
        :param datastream_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#datastream_custom_endpoint GoogleBetaProvider#datastream_custom_endpoint}.
        :param default_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#default_labels GoogleBetaProvider#default_labels}.
        :param deployment_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#deployment_manager_custom_endpoint GoogleBetaProvider#deployment_manager_custom_endpoint}.
        :param developer_connect_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#developer_connect_custom_endpoint GoogleBetaProvider#developer_connect_custom_endpoint}.
        :param dialogflow_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dialogflow_custom_endpoint GoogleBetaProvider#dialogflow_custom_endpoint}.
        :param dialogflow_cx_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dialogflow_cx_custom_endpoint GoogleBetaProvider#dialogflow_cx_custom_endpoint}.
        :param discovery_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#discovery_engine_custom_endpoint GoogleBetaProvider#discovery_engine_custom_endpoint}.
        :param dns_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dns_custom_endpoint GoogleBetaProvider#dns_custom_endpoint}.
        :param document_ai_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#document_ai_custom_endpoint GoogleBetaProvider#document_ai_custom_endpoint}.
        :param document_ai_warehouse_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#document_ai_warehouse_custom_endpoint GoogleBetaProvider#document_ai_warehouse_custom_endpoint}.
        :param edgecontainer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#edgecontainer_custom_endpoint GoogleBetaProvider#edgecontainer_custom_endpoint}.
        :param edgenetwork_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#edgenetwork_custom_endpoint GoogleBetaProvider#edgenetwork_custom_endpoint}.
        :param essential_contacts_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#essential_contacts_custom_endpoint GoogleBetaProvider#essential_contacts_custom_endpoint}.
        :param eventarc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#eventarc_custom_endpoint GoogleBetaProvider#eventarc_custom_endpoint}.
        :param external_credentials: external_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#external_credentials GoogleBetaProvider#external_credentials}
        :param filestore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#filestore_custom_endpoint GoogleBetaProvider#filestore_custom_endpoint}.
        :param firebase_app_check_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_app_check_custom_endpoint GoogleBetaProvider#firebase_app_check_custom_endpoint}.
        :param firebase_app_hosting_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_app_hosting_custom_endpoint GoogleBetaProvider#firebase_app_hosting_custom_endpoint}.
        :param firebase_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_custom_endpoint GoogleBetaProvider#firebase_custom_endpoint}.
        :param firebase_database_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_database_custom_endpoint GoogleBetaProvider#firebase_database_custom_endpoint}.
        :param firebase_data_connect_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_data_connect_custom_endpoint GoogleBetaProvider#firebase_data_connect_custom_endpoint}.
        :param firebase_extensions_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_extensions_custom_endpoint GoogleBetaProvider#firebase_extensions_custom_endpoint}.
        :param firebase_hosting_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_hosting_custom_endpoint GoogleBetaProvider#firebase_hosting_custom_endpoint}.
        :param firebaserules_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebaserules_custom_endpoint GoogleBetaProvider#firebaserules_custom_endpoint}.
        :param firebase_storage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_storage_custom_endpoint GoogleBetaProvider#firebase_storage_custom_endpoint}.
        :param firestore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firestore_custom_endpoint GoogleBetaProvider#firestore_custom_endpoint}.
        :param gemini_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gemini_custom_endpoint GoogleBetaProvider#gemini_custom_endpoint}.
        :param gke_backup_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gke_backup_custom_endpoint GoogleBetaProvider#gke_backup_custom_endpoint}.
        :param gke_hub2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gke_hub2_custom_endpoint GoogleBetaProvider#gke_hub2_custom_endpoint}.
        :param gke_hub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gke_hub_custom_endpoint GoogleBetaProvider#gke_hub_custom_endpoint}.
        :param gkehub_feature_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gkehub_feature_custom_endpoint GoogleBetaProvider#gkehub_feature_custom_endpoint}.
        :param gkeonprem_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gkeonprem_custom_endpoint GoogleBetaProvider#gkeonprem_custom_endpoint}.
        :param healthcare_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#healthcare_custom_endpoint GoogleBetaProvider#healthcare_custom_endpoint}.
        :param iam2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam2_custom_endpoint GoogleBetaProvider#iam2_custom_endpoint}.
        :param iam3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam3_custom_endpoint GoogleBetaProvider#iam3_custom_endpoint}.
        :param iam_beta_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_beta_custom_endpoint GoogleBetaProvider#iam_beta_custom_endpoint}.
        :param iam_credentials_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_credentials_custom_endpoint GoogleBetaProvider#iam_credentials_custom_endpoint}.
        :param iam_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_custom_endpoint GoogleBetaProvider#iam_custom_endpoint}.
        :param iam_workforce_pool_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_workforce_pool_custom_endpoint GoogleBetaProvider#iam_workforce_pool_custom_endpoint}.
        :param iap_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iap_custom_endpoint GoogleBetaProvider#iap_custom_endpoint}.
        :param identity_platform_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#identity_platform_custom_endpoint GoogleBetaProvider#identity_platform_custom_endpoint}.
        :param impersonate_service_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#impersonate_service_account GoogleBetaProvider#impersonate_service_account}.
        :param impersonate_service_account_delegates: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#impersonate_service_account_delegates GoogleBetaProvider#impersonate_service_account_delegates}.
        :param integration_connectors_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#integration_connectors_custom_endpoint GoogleBetaProvider#integration_connectors_custom_endpoint}.
        :param integrations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#integrations_custom_endpoint GoogleBetaProvider#integrations_custom_endpoint}.
        :param kms_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#kms_custom_endpoint GoogleBetaProvider#kms_custom_endpoint}.
        :param logging_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#logging_custom_endpoint GoogleBetaProvider#logging_custom_endpoint}.
        :param looker_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#looker_custom_endpoint GoogleBetaProvider#looker_custom_endpoint}.
        :param lustre_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#lustre_custom_endpoint GoogleBetaProvider#lustre_custom_endpoint}.
        :param managed_kafka_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#managed_kafka_custom_endpoint GoogleBetaProvider#managed_kafka_custom_endpoint}.
        :param memcache_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#memcache_custom_endpoint GoogleBetaProvider#memcache_custom_endpoint}.
        :param memorystore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#memorystore_custom_endpoint GoogleBetaProvider#memorystore_custom_endpoint}.
        :param migration_center_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#migration_center_custom_endpoint GoogleBetaProvider#migration_center_custom_endpoint}.
        :param ml_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#ml_engine_custom_endpoint GoogleBetaProvider#ml_engine_custom_endpoint}.
        :param monitoring_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#monitoring_custom_endpoint GoogleBetaProvider#monitoring_custom_endpoint}.
        :param netapp_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#netapp_custom_endpoint GoogleBetaProvider#netapp_custom_endpoint}.
        :param network_connectivity_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_connectivity_custom_endpoint GoogleBetaProvider#network_connectivity_custom_endpoint}.
        :param network_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_management_custom_endpoint GoogleBetaProvider#network_management_custom_endpoint}.
        :param network_security_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_security_custom_endpoint GoogleBetaProvider#network_security_custom_endpoint}.
        :param network_services_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_services_custom_endpoint GoogleBetaProvider#network_services_custom_endpoint}.
        :param notebooks_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#notebooks_custom_endpoint GoogleBetaProvider#notebooks_custom_endpoint}.
        :param oracle_database_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#oracle_database_custom_endpoint GoogleBetaProvider#oracle_database_custom_endpoint}.
        :param org_policy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#org_policy_custom_endpoint GoogleBetaProvider#org_policy_custom_endpoint}.
        :param os_config_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#os_config_custom_endpoint GoogleBetaProvider#os_config_custom_endpoint}.
        :param os_config_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#os_config_v2_custom_endpoint GoogleBetaProvider#os_config_v2_custom_endpoint}.
        :param os_login_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#os_login_custom_endpoint GoogleBetaProvider#os_login_custom_endpoint}.
        :param parallelstore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#parallelstore_custom_endpoint GoogleBetaProvider#parallelstore_custom_endpoint}.
        :param parameter_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#parameter_manager_custom_endpoint GoogleBetaProvider#parameter_manager_custom_endpoint}.
        :param parameter_manager_regional_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#parameter_manager_regional_custom_endpoint GoogleBetaProvider#parameter_manager_regional_custom_endpoint}.
        :param privateca_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#privateca_custom_endpoint GoogleBetaProvider#privateca_custom_endpoint}.
        :param privileged_access_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#privileged_access_manager_custom_endpoint GoogleBetaProvider#privileged_access_manager_custom_endpoint}.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#project GoogleBetaProvider#project}.
        :param public_ca_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#public_ca_custom_endpoint GoogleBetaProvider#public_ca_custom_endpoint}.
        :param pubsub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#pubsub_custom_endpoint GoogleBetaProvider#pubsub_custom_endpoint}.
        :param pubsub_lite_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#pubsub_lite_custom_endpoint GoogleBetaProvider#pubsub_lite_custom_endpoint}.
        :param recaptcha_enterprise_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#recaptcha_enterprise_custom_endpoint GoogleBetaProvider#recaptcha_enterprise_custom_endpoint}.
        :param redis_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#redis_custom_endpoint GoogleBetaProvider#redis_custom_endpoint}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#region GoogleBetaProvider#region}.
        :param request_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#request_reason GoogleBetaProvider#request_reason}.
        :param request_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#request_timeout GoogleBetaProvider#request_timeout}.
        :param resource_manager3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#resource_manager3_custom_endpoint GoogleBetaProvider#resource_manager3_custom_endpoint}.
        :param resource_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#resource_manager_custom_endpoint GoogleBetaProvider#resource_manager_custom_endpoint}.
        :param resource_manager_v3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#resource_manager_v3_custom_endpoint GoogleBetaProvider#resource_manager_v3_custom_endpoint}.
        :param runtimeconfig_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#runtimeconfig_custom_endpoint GoogleBetaProvider#runtimeconfig_custom_endpoint}.
        :param runtime_config_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#runtime_config_custom_endpoint GoogleBetaProvider#runtime_config_custom_endpoint}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#scopes GoogleBetaProvider#scopes}.
        :param secret_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#secret_manager_custom_endpoint GoogleBetaProvider#secret_manager_custom_endpoint}.
        :param secret_manager_regional_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#secret_manager_regional_custom_endpoint GoogleBetaProvider#secret_manager_regional_custom_endpoint}.
        :param secure_source_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#secure_source_manager_custom_endpoint GoogleBetaProvider#secure_source_manager_custom_endpoint}.
        :param security_center_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_center_custom_endpoint GoogleBetaProvider#security_center_custom_endpoint}.
        :param security_center_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_center_management_custom_endpoint GoogleBetaProvider#security_center_management_custom_endpoint}.
        :param security_center_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_center_v2_custom_endpoint GoogleBetaProvider#security_center_v2_custom_endpoint}.
        :param securityposture_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#securityposture_custom_endpoint GoogleBetaProvider#securityposture_custom_endpoint}.
        :param security_scanner_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_scanner_custom_endpoint GoogleBetaProvider#security_scanner_custom_endpoint}.
        :param service_directory_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_directory_custom_endpoint GoogleBetaProvider#service_directory_custom_endpoint}.
        :param service_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_management_custom_endpoint GoogleBetaProvider#service_management_custom_endpoint}.
        :param service_networking_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_networking_custom_endpoint GoogleBetaProvider#service_networking_custom_endpoint}.
        :param service_usage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_usage_custom_endpoint GoogleBetaProvider#service_usage_custom_endpoint}.
        :param site_verification_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#site_verification_custom_endpoint GoogleBetaProvider#site_verification_custom_endpoint}.
        :param source_repo_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#source_repo_custom_endpoint GoogleBetaProvider#source_repo_custom_endpoint}.
        :param spanner_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#spanner_custom_endpoint GoogleBetaProvider#spanner_custom_endpoint}.
        :param sql_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#sql_custom_endpoint GoogleBetaProvider#sql_custom_endpoint}.
        :param storage_batch_operations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_batch_operations_custom_endpoint GoogleBetaProvider#storage_batch_operations_custom_endpoint}.
        :param storage_control_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_control_custom_endpoint GoogleBetaProvider#storage_control_custom_endpoint}.
        :param storage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_custom_endpoint GoogleBetaProvider#storage_custom_endpoint}.
        :param storage_insights_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_insights_custom_endpoint GoogleBetaProvider#storage_insights_custom_endpoint}.
        :param storage_transfer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_transfer_custom_endpoint GoogleBetaProvider#storage_transfer_custom_endpoint}.
        :param tags_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tags_custom_endpoint GoogleBetaProvider#tags_custom_endpoint}.
        :param tags_location_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tags_location_custom_endpoint GoogleBetaProvider#tags_location_custom_endpoint}.
        :param terraform_attribution_label_addition_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#terraform_attribution_label_addition_strategy GoogleBetaProvider#terraform_attribution_label_addition_strategy}.
        :param tpu_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tpu_custom_endpoint GoogleBetaProvider#tpu_custom_endpoint}.
        :param tpu_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tpu_v2_custom_endpoint GoogleBetaProvider#tpu_v2_custom_endpoint}.
        :param transcoder_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#transcoder_custom_endpoint GoogleBetaProvider#transcoder_custom_endpoint}.
        :param universe_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#universe_domain GoogleBetaProvider#universe_domain}.
        :param user_project_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#user_project_override GoogleBetaProvider#user_project_override}.
        :param vertex_ai_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#vertex_ai_custom_endpoint GoogleBetaProvider#vertex_ai_custom_endpoint}.
        :param vmwareengine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#vmwareengine_custom_endpoint GoogleBetaProvider#vmwareengine_custom_endpoint}.
        :param vpc_access_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#vpc_access_custom_endpoint GoogleBetaProvider#vpc_access_custom_endpoint}.
        :param workbench_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#workbench_custom_endpoint GoogleBetaProvider#workbench_custom_endpoint}.
        :param workflows_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#workflows_custom_endpoint GoogleBetaProvider#workflows_custom_endpoint}.
        :param workstations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#workstations_custom_endpoint GoogleBetaProvider#workstations_custom_endpoint}.
        :param zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#zone GoogleBetaProvider#zone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd797056cd80150f775dd74b0137239361d8c3526785cfab58b0226d1185ff2b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = GoogleBetaProviderConfig(
            access_approval_custom_endpoint=access_approval_custom_endpoint,
            access_context_manager_custom_endpoint=access_context_manager_custom_endpoint,
            access_token=access_token,
            active_directory_custom_endpoint=active_directory_custom_endpoint,
            add_terraform_attribution_label=add_terraform_attribution_label,
            alias=alias,
            alloydb_custom_endpoint=alloydb_custom_endpoint,
            api_gateway_custom_endpoint=api_gateway_custom_endpoint,
            apigee_custom_endpoint=apigee_custom_endpoint,
            apihub_custom_endpoint=apihub_custom_endpoint,
            apikeys_custom_endpoint=apikeys_custom_endpoint,
            app_engine_custom_endpoint=app_engine_custom_endpoint,
            apphub_custom_endpoint=apphub_custom_endpoint,
            artifact_registry_custom_endpoint=artifact_registry_custom_endpoint,
            assured_workloads_custom_endpoint=assured_workloads_custom_endpoint,
            backup_dr_custom_endpoint=backup_dr_custom_endpoint,
            batching=batching,
            beyondcorp_custom_endpoint=beyondcorp_custom_endpoint,
            biglake_custom_endpoint=biglake_custom_endpoint,
            bigquery_analytics_hub_custom_endpoint=bigquery_analytics_hub_custom_endpoint,
            bigquery_connection_custom_endpoint=bigquery_connection_custom_endpoint,
            big_query_custom_endpoint=big_query_custom_endpoint,
            bigquery_datapolicy_custom_endpoint=bigquery_datapolicy_custom_endpoint,
            bigquery_data_transfer_custom_endpoint=bigquery_data_transfer_custom_endpoint,
            bigquery_reservation_custom_endpoint=bigquery_reservation_custom_endpoint,
            bigtable_custom_endpoint=bigtable_custom_endpoint,
            billing_custom_endpoint=billing_custom_endpoint,
            billing_project=billing_project,
            binary_authorization_custom_endpoint=binary_authorization_custom_endpoint,
            blockchain_node_engine_custom_endpoint=blockchain_node_engine_custom_endpoint,
            certificate_manager_custom_endpoint=certificate_manager_custom_endpoint,
            chronicle_custom_endpoint=chronicle_custom_endpoint,
            cloud_asset_custom_endpoint=cloud_asset_custom_endpoint,
            cloud_billing_custom_endpoint=cloud_billing_custom_endpoint,
            cloud_build_custom_endpoint=cloud_build_custom_endpoint,
            cloudbuildv2_custom_endpoint=cloudbuildv2_custom_endpoint,
            cloud_build_worker_pool_custom_endpoint=cloud_build_worker_pool_custom_endpoint,
            clouddeploy_custom_endpoint=clouddeploy_custom_endpoint,
            clouddomains_custom_endpoint=clouddomains_custom_endpoint,
            cloudfunctions2_custom_endpoint=cloudfunctions2_custom_endpoint,
            cloud_functions_custom_endpoint=cloud_functions_custom_endpoint,
            cloud_identity_custom_endpoint=cloud_identity_custom_endpoint,
            cloud_ids_custom_endpoint=cloud_ids_custom_endpoint,
            cloud_quotas_custom_endpoint=cloud_quotas_custom_endpoint,
            cloud_resource_manager_custom_endpoint=cloud_resource_manager_custom_endpoint,
            cloud_run_custom_endpoint=cloud_run_custom_endpoint,
            cloud_run_v2_custom_endpoint=cloud_run_v2_custom_endpoint,
            cloud_scheduler_custom_endpoint=cloud_scheduler_custom_endpoint,
            cloud_tasks_custom_endpoint=cloud_tasks_custom_endpoint,
            colab_custom_endpoint=colab_custom_endpoint,
            composer_custom_endpoint=composer_custom_endpoint,
            compute_custom_endpoint=compute_custom_endpoint,
            container_analysis_custom_endpoint=container_analysis_custom_endpoint,
            container_attached_custom_endpoint=container_attached_custom_endpoint,
            container_aws_custom_endpoint=container_aws_custom_endpoint,
            container_azure_custom_endpoint=container_azure_custom_endpoint,
            container_custom_endpoint=container_custom_endpoint,
            core_billing_custom_endpoint=core_billing_custom_endpoint,
            credentials=credentials,
            database_migration_service_custom_endpoint=database_migration_service_custom_endpoint,
            data_catalog_custom_endpoint=data_catalog_custom_endpoint,
            dataflow_custom_endpoint=dataflow_custom_endpoint,
            dataform_custom_endpoint=dataform_custom_endpoint,
            data_fusion_custom_endpoint=data_fusion_custom_endpoint,
            data_loss_prevention_custom_endpoint=data_loss_prevention_custom_endpoint,
            data_pipeline_custom_endpoint=data_pipeline_custom_endpoint,
            dataplex_custom_endpoint=dataplex_custom_endpoint,
            dataproc_custom_endpoint=dataproc_custom_endpoint,
            dataproc_gdc_custom_endpoint=dataproc_gdc_custom_endpoint,
            dataproc_metastore_custom_endpoint=dataproc_metastore_custom_endpoint,
            datastream_custom_endpoint=datastream_custom_endpoint,
            default_labels=default_labels,
            deployment_manager_custom_endpoint=deployment_manager_custom_endpoint,
            developer_connect_custom_endpoint=developer_connect_custom_endpoint,
            dialogflow_custom_endpoint=dialogflow_custom_endpoint,
            dialogflow_cx_custom_endpoint=dialogflow_cx_custom_endpoint,
            discovery_engine_custom_endpoint=discovery_engine_custom_endpoint,
            dns_custom_endpoint=dns_custom_endpoint,
            document_ai_custom_endpoint=document_ai_custom_endpoint,
            document_ai_warehouse_custom_endpoint=document_ai_warehouse_custom_endpoint,
            edgecontainer_custom_endpoint=edgecontainer_custom_endpoint,
            edgenetwork_custom_endpoint=edgenetwork_custom_endpoint,
            essential_contacts_custom_endpoint=essential_contacts_custom_endpoint,
            eventarc_custom_endpoint=eventarc_custom_endpoint,
            external_credentials=external_credentials,
            filestore_custom_endpoint=filestore_custom_endpoint,
            firebase_app_check_custom_endpoint=firebase_app_check_custom_endpoint,
            firebase_app_hosting_custom_endpoint=firebase_app_hosting_custom_endpoint,
            firebase_custom_endpoint=firebase_custom_endpoint,
            firebase_database_custom_endpoint=firebase_database_custom_endpoint,
            firebase_data_connect_custom_endpoint=firebase_data_connect_custom_endpoint,
            firebase_extensions_custom_endpoint=firebase_extensions_custom_endpoint,
            firebase_hosting_custom_endpoint=firebase_hosting_custom_endpoint,
            firebaserules_custom_endpoint=firebaserules_custom_endpoint,
            firebase_storage_custom_endpoint=firebase_storage_custom_endpoint,
            firestore_custom_endpoint=firestore_custom_endpoint,
            gemini_custom_endpoint=gemini_custom_endpoint,
            gke_backup_custom_endpoint=gke_backup_custom_endpoint,
            gke_hub2_custom_endpoint=gke_hub2_custom_endpoint,
            gke_hub_custom_endpoint=gke_hub_custom_endpoint,
            gkehub_feature_custom_endpoint=gkehub_feature_custom_endpoint,
            gkeonprem_custom_endpoint=gkeonprem_custom_endpoint,
            healthcare_custom_endpoint=healthcare_custom_endpoint,
            iam2_custom_endpoint=iam2_custom_endpoint,
            iam3_custom_endpoint=iam3_custom_endpoint,
            iam_beta_custom_endpoint=iam_beta_custom_endpoint,
            iam_credentials_custom_endpoint=iam_credentials_custom_endpoint,
            iam_custom_endpoint=iam_custom_endpoint,
            iam_workforce_pool_custom_endpoint=iam_workforce_pool_custom_endpoint,
            iap_custom_endpoint=iap_custom_endpoint,
            identity_platform_custom_endpoint=identity_platform_custom_endpoint,
            impersonate_service_account=impersonate_service_account,
            impersonate_service_account_delegates=impersonate_service_account_delegates,
            integration_connectors_custom_endpoint=integration_connectors_custom_endpoint,
            integrations_custom_endpoint=integrations_custom_endpoint,
            kms_custom_endpoint=kms_custom_endpoint,
            logging_custom_endpoint=logging_custom_endpoint,
            looker_custom_endpoint=looker_custom_endpoint,
            lustre_custom_endpoint=lustre_custom_endpoint,
            managed_kafka_custom_endpoint=managed_kafka_custom_endpoint,
            memcache_custom_endpoint=memcache_custom_endpoint,
            memorystore_custom_endpoint=memorystore_custom_endpoint,
            migration_center_custom_endpoint=migration_center_custom_endpoint,
            ml_engine_custom_endpoint=ml_engine_custom_endpoint,
            monitoring_custom_endpoint=monitoring_custom_endpoint,
            netapp_custom_endpoint=netapp_custom_endpoint,
            network_connectivity_custom_endpoint=network_connectivity_custom_endpoint,
            network_management_custom_endpoint=network_management_custom_endpoint,
            network_security_custom_endpoint=network_security_custom_endpoint,
            network_services_custom_endpoint=network_services_custom_endpoint,
            notebooks_custom_endpoint=notebooks_custom_endpoint,
            oracle_database_custom_endpoint=oracle_database_custom_endpoint,
            org_policy_custom_endpoint=org_policy_custom_endpoint,
            os_config_custom_endpoint=os_config_custom_endpoint,
            os_config_v2_custom_endpoint=os_config_v2_custom_endpoint,
            os_login_custom_endpoint=os_login_custom_endpoint,
            parallelstore_custom_endpoint=parallelstore_custom_endpoint,
            parameter_manager_custom_endpoint=parameter_manager_custom_endpoint,
            parameter_manager_regional_custom_endpoint=parameter_manager_regional_custom_endpoint,
            privateca_custom_endpoint=privateca_custom_endpoint,
            privileged_access_manager_custom_endpoint=privileged_access_manager_custom_endpoint,
            project=project,
            public_ca_custom_endpoint=public_ca_custom_endpoint,
            pubsub_custom_endpoint=pubsub_custom_endpoint,
            pubsub_lite_custom_endpoint=pubsub_lite_custom_endpoint,
            recaptcha_enterprise_custom_endpoint=recaptcha_enterprise_custom_endpoint,
            redis_custom_endpoint=redis_custom_endpoint,
            region=region,
            request_reason=request_reason,
            request_timeout=request_timeout,
            resource_manager3_custom_endpoint=resource_manager3_custom_endpoint,
            resource_manager_custom_endpoint=resource_manager_custom_endpoint,
            resource_manager_v3_custom_endpoint=resource_manager_v3_custom_endpoint,
            runtimeconfig_custom_endpoint=runtimeconfig_custom_endpoint,
            runtime_config_custom_endpoint=runtime_config_custom_endpoint,
            scopes=scopes,
            secret_manager_custom_endpoint=secret_manager_custom_endpoint,
            secret_manager_regional_custom_endpoint=secret_manager_regional_custom_endpoint,
            secure_source_manager_custom_endpoint=secure_source_manager_custom_endpoint,
            security_center_custom_endpoint=security_center_custom_endpoint,
            security_center_management_custom_endpoint=security_center_management_custom_endpoint,
            security_center_v2_custom_endpoint=security_center_v2_custom_endpoint,
            securityposture_custom_endpoint=securityposture_custom_endpoint,
            security_scanner_custom_endpoint=security_scanner_custom_endpoint,
            service_directory_custom_endpoint=service_directory_custom_endpoint,
            service_management_custom_endpoint=service_management_custom_endpoint,
            service_networking_custom_endpoint=service_networking_custom_endpoint,
            service_usage_custom_endpoint=service_usage_custom_endpoint,
            site_verification_custom_endpoint=site_verification_custom_endpoint,
            source_repo_custom_endpoint=source_repo_custom_endpoint,
            spanner_custom_endpoint=spanner_custom_endpoint,
            sql_custom_endpoint=sql_custom_endpoint,
            storage_batch_operations_custom_endpoint=storage_batch_operations_custom_endpoint,
            storage_control_custom_endpoint=storage_control_custom_endpoint,
            storage_custom_endpoint=storage_custom_endpoint,
            storage_insights_custom_endpoint=storage_insights_custom_endpoint,
            storage_transfer_custom_endpoint=storage_transfer_custom_endpoint,
            tags_custom_endpoint=tags_custom_endpoint,
            tags_location_custom_endpoint=tags_location_custom_endpoint,
            terraform_attribution_label_addition_strategy=terraform_attribution_label_addition_strategy,
            tpu_custom_endpoint=tpu_custom_endpoint,
            tpu_v2_custom_endpoint=tpu_v2_custom_endpoint,
            transcoder_custom_endpoint=transcoder_custom_endpoint,
            universe_domain=universe_domain,
            user_project_override=user_project_override,
            vertex_ai_custom_endpoint=vertex_ai_custom_endpoint,
            vmwareengine_custom_endpoint=vmwareengine_custom_endpoint,
            vpc_access_custom_endpoint=vpc_access_custom_endpoint,
            workbench_custom_endpoint=workbench_custom_endpoint,
            workflows_custom_endpoint=workflows_custom_endpoint,
            workstations_custom_endpoint=workstations_custom_endpoint,
            zone=zone,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a GoogleBetaProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBetaProvider to import.
        :param import_from_id: The id of the existing GoogleBetaProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBetaProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f0b89c806f84a1d7e9ffd2915f747abf710ac603560697f5b5b4ecf4a34620)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccessApprovalCustomEndpoint")
    def reset_access_approval_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessApprovalCustomEndpoint", []))

    @jsii.member(jsii_name="resetAccessContextManagerCustomEndpoint")
    def reset_access_context_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessContextManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetActiveDirectoryCustomEndpoint")
    def reset_active_directory_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryCustomEndpoint", []))

    @jsii.member(jsii_name="resetAddTerraformAttributionLabel")
    def reset_add_terraform_attribution_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddTerraformAttributionLabel", []))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAlloydbCustomEndpoint")
    def reset_alloydb_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlloydbCustomEndpoint", []))

    @jsii.member(jsii_name="resetApiGatewayCustomEndpoint")
    def reset_api_gateway_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiGatewayCustomEndpoint", []))

    @jsii.member(jsii_name="resetApigeeCustomEndpoint")
    def reset_apigee_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApigeeCustomEndpoint", []))

    @jsii.member(jsii_name="resetApihubCustomEndpoint")
    def reset_apihub_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApihubCustomEndpoint", []))

    @jsii.member(jsii_name="resetApikeysCustomEndpoint")
    def reset_apikeys_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApikeysCustomEndpoint", []))

    @jsii.member(jsii_name="resetAppEngineCustomEndpoint")
    def reset_app_engine_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngineCustomEndpoint", []))

    @jsii.member(jsii_name="resetApphubCustomEndpoint")
    def reset_apphub_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApphubCustomEndpoint", []))

    @jsii.member(jsii_name="resetArtifactRegistryCustomEndpoint")
    def reset_artifact_registry_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArtifactRegistryCustomEndpoint", []))

    @jsii.member(jsii_name="resetAssuredWorkloadsCustomEndpoint")
    def reset_assured_workloads_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssuredWorkloadsCustomEndpoint", []))

    @jsii.member(jsii_name="resetBackupDrCustomEndpoint")
    def reset_backup_dr_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupDrCustomEndpoint", []))

    @jsii.member(jsii_name="resetBatching")
    def reset_batching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatching", []))

    @jsii.member(jsii_name="resetBeyondcorpCustomEndpoint")
    def reset_beyondcorp_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBeyondcorpCustomEndpoint", []))

    @jsii.member(jsii_name="resetBiglakeCustomEndpoint")
    def reset_biglake_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBiglakeCustomEndpoint", []))

    @jsii.member(jsii_name="resetBigqueryAnalyticsHubCustomEndpoint")
    def reset_bigquery_analytics_hub_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryAnalyticsHubCustomEndpoint", []))

    @jsii.member(jsii_name="resetBigqueryConnectionCustomEndpoint")
    def reset_bigquery_connection_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryConnectionCustomEndpoint", []))

    @jsii.member(jsii_name="resetBigQueryCustomEndpoint")
    def reset_big_query_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigQueryCustomEndpoint", []))

    @jsii.member(jsii_name="resetBigqueryDatapolicyCustomEndpoint")
    def reset_bigquery_datapolicy_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryDatapolicyCustomEndpoint", []))

    @jsii.member(jsii_name="resetBigqueryDataTransferCustomEndpoint")
    def reset_bigquery_data_transfer_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryDataTransferCustomEndpoint", []))

    @jsii.member(jsii_name="resetBigqueryReservationCustomEndpoint")
    def reset_bigquery_reservation_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryReservationCustomEndpoint", []))

    @jsii.member(jsii_name="resetBigtableCustomEndpoint")
    def reset_bigtable_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigtableCustomEndpoint", []))

    @jsii.member(jsii_name="resetBillingCustomEndpoint")
    def reset_billing_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingCustomEndpoint", []))

    @jsii.member(jsii_name="resetBillingProject")
    def reset_billing_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingProject", []))

    @jsii.member(jsii_name="resetBinaryAuthorizationCustomEndpoint")
    def reset_binary_authorization_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAuthorizationCustomEndpoint", []))

    @jsii.member(jsii_name="resetBlockchainNodeEngineCustomEndpoint")
    def reset_blockchain_node_engine_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockchainNodeEngineCustomEndpoint", []))

    @jsii.member(jsii_name="resetCertificateManagerCustomEndpoint")
    def reset_certificate_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetChronicleCustomEndpoint")
    def reset_chronicle_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChronicleCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudAssetCustomEndpoint")
    def reset_cloud_asset_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudAssetCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudBillingCustomEndpoint")
    def reset_cloud_billing_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudBillingCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudBuildCustomEndpoint")
    def reset_cloud_build_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudBuildCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudbuildv2CustomEndpoint")
    def reset_cloudbuildv2_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudbuildv2CustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudBuildWorkerPoolCustomEndpoint")
    def reset_cloud_build_worker_pool_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudBuildWorkerPoolCustomEndpoint", []))

    @jsii.member(jsii_name="resetClouddeployCustomEndpoint")
    def reset_clouddeploy_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClouddeployCustomEndpoint", []))

    @jsii.member(jsii_name="resetClouddomainsCustomEndpoint")
    def reset_clouddomains_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClouddomainsCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudfunctions2CustomEndpoint")
    def reset_cloudfunctions2_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudfunctions2CustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudFunctionsCustomEndpoint")
    def reset_cloud_functions_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudFunctionsCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudIdentityCustomEndpoint")
    def reset_cloud_identity_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudIdentityCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudIdsCustomEndpoint")
    def reset_cloud_ids_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudIdsCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudQuotasCustomEndpoint")
    def reset_cloud_quotas_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudQuotasCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudResourceManagerCustomEndpoint")
    def reset_cloud_resource_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudResourceManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudRunCustomEndpoint")
    def reset_cloud_run_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudRunCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudRunV2CustomEndpoint")
    def reset_cloud_run_v2_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudRunV2CustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudSchedulerCustomEndpoint")
    def reset_cloud_scheduler_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSchedulerCustomEndpoint", []))

    @jsii.member(jsii_name="resetCloudTasksCustomEndpoint")
    def reset_cloud_tasks_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudTasksCustomEndpoint", []))

    @jsii.member(jsii_name="resetColabCustomEndpoint")
    def reset_colab_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColabCustomEndpoint", []))

    @jsii.member(jsii_name="resetComposerCustomEndpoint")
    def reset_composer_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComposerCustomEndpoint", []))

    @jsii.member(jsii_name="resetComputeCustomEndpoint")
    def reset_compute_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeCustomEndpoint", []))

    @jsii.member(jsii_name="resetContainerAnalysisCustomEndpoint")
    def reset_container_analysis_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerAnalysisCustomEndpoint", []))

    @jsii.member(jsii_name="resetContainerAttachedCustomEndpoint")
    def reset_container_attached_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerAttachedCustomEndpoint", []))

    @jsii.member(jsii_name="resetContainerAwsCustomEndpoint")
    def reset_container_aws_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerAwsCustomEndpoint", []))

    @jsii.member(jsii_name="resetContainerAzureCustomEndpoint")
    def reset_container_azure_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerAzureCustomEndpoint", []))

    @jsii.member(jsii_name="resetContainerCustomEndpoint")
    def reset_container_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerCustomEndpoint", []))

    @jsii.member(jsii_name="resetCoreBillingCustomEndpoint")
    def reset_core_billing_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreBillingCustomEndpoint", []))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetDatabaseMigrationServiceCustomEndpoint")
    def reset_database_migration_service_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseMigrationServiceCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataCatalogCustomEndpoint")
    def reset_data_catalog_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCatalogCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataflowCustomEndpoint")
    def reset_dataflow_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataflowCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataformCustomEndpoint")
    def reset_dataform_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataformCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataFusionCustomEndpoint")
    def reset_data_fusion_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataFusionCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataLossPreventionCustomEndpoint")
    def reset_data_loss_prevention_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataLossPreventionCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataPipelineCustomEndpoint")
    def reset_data_pipeline_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPipelineCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataplexCustomEndpoint")
    def reset_dataplex_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataplexCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataprocCustomEndpoint")
    def reset_dataproc_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataprocGdcCustomEndpoint")
    def reset_dataproc_gdc_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocGdcCustomEndpoint", []))

    @jsii.member(jsii_name="resetDataprocMetastoreCustomEndpoint")
    def reset_dataproc_metastore_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocMetastoreCustomEndpoint", []))

    @jsii.member(jsii_name="resetDatastreamCustomEndpoint")
    def reset_datastream_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatastreamCustomEndpoint", []))

    @jsii.member(jsii_name="resetDefaultLabels")
    def reset_default_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLabels", []))

    @jsii.member(jsii_name="resetDeploymentManagerCustomEndpoint")
    def reset_deployment_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetDeveloperConnectCustomEndpoint")
    def reset_developer_connect_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperConnectCustomEndpoint", []))

    @jsii.member(jsii_name="resetDialogflowCustomEndpoint")
    def reset_dialogflow_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDialogflowCustomEndpoint", []))

    @jsii.member(jsii_name="resetDialogflowCxCustomEndpoint")
    def reset_dialogflow_cx_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDialogflowCxCustomEndpoint", []))

    @jsii.member(jsii_name="resetDiscoveryEngineCustomEndpoint")
    def reset_discovery_engine_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscoveryEngineCustomEndpoint", []))

    @jsii.member(jsii_name="resetDnsCustomEndpoint")
    def reset_dns_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsCustomEndpoint", []))

    @jsii.member(jsii_name="resetDocumentAiCustomEndpoint")
    def reset_document_ai_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentAiCustomEndpoint", []))

    @jsii.member(jsii_name="resetDocumentAiWarehouseCustomEndpoint")
    def reset_document_ai_warehouse_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentAiWarehouseCustomEndpoint", []))

    @jsii.member(jsii_name="resetEdgecontainerCustomEndpoint")
    def reset_edgecontainer_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgecontainerCustomEndpoint", []))

    @jsii.member(jsii_name="resetEdgenetworkCustomEndpoint")
    def reset_edgenetwork_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgenetworkCustomEndpoint", []))

    @jsii.member(jsii_name="resetEssentialContactsCustomEndpoint")
    def reset_essential_contacts_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEssentialContactsCustomEndpoint", []))

    @jsii.member(jsii_name="resetEventarcCustomEndpoint")
    def reset_eventarc_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventarcCustomEndpoint", []))

    @jsii.member(jsii_name="resetExternalCredentials")
    def reset_external_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalCredentials", []))

    @jsii.member(jsii_name="resetFilestoreCustomEndpoint")
    def reset_filestore_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilestoreCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaseAppCheckCustomEndpoint")
    def reset_firebase_app_check_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaseAppCheckCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaseAppHostingCustomEndpoint")
    def reset_firebase_app_hosting_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaseAppHostingCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaseCustomEndpoint")
    def reset_firebase_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaseCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaseDatabaseCustomEndpoint")
    def reset_firebase_database_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaseDatabaseCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaseDataConnectCustomEndpoint")
    def reset_firebase_data_connect_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaseDataConnectCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaseExtensionsCustomEndpoint")
    def reset_firebase_extensions_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaseExtensionsCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaseHostingCustomEndpoint")
    def reset_firebase_hosting_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaseHostingCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaserulesCustomEndpoint")
    def reset_firebaserules_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaserulesCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaseStorageCustomEndpoint")
    def reset_firebase_storage_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaseStorageCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirestoreCustomEndpoint")
    def reset_firestore_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirestoreCustomEndpoint", []))

    @jsii.member(jsii_name="resetGeminiCustomEndpoint")
    def reset_gemini_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeminiCustomEndpoint", []))

    @jsii.member(jsii_name="resetGkeBackupCustomEndpoint")
    def reset_gke_backup_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeBackupCustomEndpoint", []))

    @jsii.member(jsii_name="resetGkeHub2CustomEndpoint")
    def reset_gke_hub2_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeHub2CustomEndpoint", []))

    @jsii.member(jsii_name="resetGkeHubCustomEndpoint")
    def reset_gke_hub_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeHubCustomEndpoint", []))

    @jsii.member(jsii_name="resetGkehubFeatureCustomEndpoint")
    def reset_gkehub_feature_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkehubFeatureCustomEndpoint", []))

    @jsii.member(jsii_name="resetGkeonpremCustomEndpoint")
    def reset_gkeonprem_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeonpremCustomEndpoint", []))

    @jsii.member(jsii_name="resetHealthcareCustomEndpoint")
    def reset_healthcare_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthcareCustomEndpoint", []))

    @jsii.member(jsii_name="resetIam2CustomEndpoint")
    def reset_iam2_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIam2CustomEndpoint", []))

    @jsii.member(jsii_name="resetIam3CustomEndpoint")
    def reset_iam3_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIam3CustomEndpoint", []))

    @jsii.member(jsii_name="resetIamBetaCustomEndpoint")
    def reset_iam_beta_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamBetaCustomEndpoint", []))

    @jsii.member(jsii_name="resetIamCredentialsCustomEndpoint")
    def reset_iam_credentials_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamCredentialsCustomEndpoint", []))

    @jsii.member(jsii_name="resetIamCustomEndpoint")
    def reset_iam_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamCustomEndpoint", []))

    @jsii.member(jsii_name="resetIamWorkforcePoolCustomEndpoint")
    def reset_iam_workforce_pool_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamWorkforcePoolCustomEndpoint", []))

    @jsii.member(jsii_name="resetIapCustomEndpoint")
    def reset_iap_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIapCustomEndpoint", []))

    @jsii.member(jsii_name="resetIdentityPlatformCustomEndpoint")
    def reset_identity_platform_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityPlatformCustomEndpoint", []))

    @jsii.member(jsii_name="resetImpersonateServiceAccount")
    def reset_impersonate_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImpersonateServiceAccount", []))

    @jsii.member(jsii_name="resetImpersonateServiceAccountDelegates")
    def reset_impersonate_service_account_delegates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImpersonateServiceAccountDelegates", []))

    @jsii.member(jsii_name="resetIntegrationConnectorsCustomEndpoint")
    def reset_integration_connectors_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationConnectorsCustomEndpoint", []))

    @jsii.member(jsii_name="resetIntegrationsCustomEndpoint")
    def reset_integrations_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationsCustomEndpoint", []))

    @jsii.member(jsii_name="resetKmsCustomEndpoint")
    def reset_kms_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsCustomEndpoint", []))

    @jsii.member(jsii_name="resetLoggingCustomEndpoint")
    def reset_logging_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingCustomEndpoint", []))

    @jsii.member(jsii_name="resetLookerCustomEndpoint")
    def reset_looker_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLookerCustomEndpoint", []))

    @jsii.member(jsii_name="resetLustreCustomEndpoint")
    def reset_lustre_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLustreCustomEndpoint", []))

    @jsii.member(jsii_name="resetManagedKafkaCustomEndpoint")
    def reset_managed_kafka_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedKafkaCustomEndpoint", []))

    @jsii.member(jsii_name="resetMemcacheCustomEndpoint")
    def reset_memcache_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemcacheCustomEndpoint", []))

    @jsii.member(jsii_name="resetMemorystoreCustomEndpoint")
    def reset_memorystore_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorystoreCustomEndpoint", []))

    @jsii.member(jsii_name="resetMigrationCenterCustomEndpoint")
    def reset_migration_center_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMigrationCenterCustomEndpoint", []))

    @jsii.member(jsii_name="resetMlEngineCustomEndpoint")
    def reset_ml_engine_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMlEngineCustomEndpoint", []))

    @jsii.member(jsii_name="resetMonitoringCustomEndpoint")
    def reset_monitoring_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringCustomEndpoint", []))

    @jsii.member(jsii_name="resetNetappCustomEndpoint")
    def reset_netapp_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetappCustomEndpoint", []))

    @jsii.member(jsii_name="resetNetworkConnectivityCustomEndpoint")
    def reset_network_connectivity_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConnectivityCustomEndpoint", []))

    @jsii.member(jsii_name="resetNetworkManagementCustomEndpoint")
    def reset_network_management_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkManagementCustomEndpoint", []))

    @jsii.member(jsii_name="resetNetworkSecurityCustomEndpoint")
    def reset_network_security_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkSecurityCustomEndpoint", []))

    @jsii.member(jsii_name="resetNetworkServicesCustomEndpoint")
    def reset_network_services_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkServicesCustomEndpoint", []))

    @jsii.member(jsii_name="resetNotebooksCustomEndpoint")
    def reset_notebooks_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotebooksCustomEndpoint", []))

    @jsii.member(jsii_name="resetOracleDatabaseCustomEndpoint")
    def reset_oracle_database_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleDatabaseCustomEndpoint", []))

    @jsii.member(jsii_name="resetOrgPolicyCustomEndpoint")
    def reset_org_policy_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgPolicyCustomEndpoint", []))

    @jsii.member(jsii_name="resetOsConfigCustomEndpoint")
    def reset_os_config_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsConfigCustomEndpoint", []))

    @jsii.member(jsii_name="resetOsConfigV2CustomEndpoint")
    def reset_os_config_v2_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsConfigV2CustomEndpoint", []))

    @jsii.member(jsii_name="resetOsLoginCustomEndpoint")
    def reset_os_login_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsLoginCustomEndpoint", []))

    @jsii.member(jsii_name="resetParallelstoreCustomEndpoint")
    def reset_parallelstore_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelstoreCustomEndpoint", []))

    @jsii.member(jsii_name="resetParameterManagerCustomEndpoint")
    def reset_parameter_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameterManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetParameterManagerRegionalCustomEndpoint")
    def reset_parameter_manager_regional_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameterManagerRegionalCustomEndpoint", []))

    @jsii.member(jsii_name="resetPrivatecaCustomEndpoint")
    def reset_privateca_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivatecaCustomEndpoint", []))

    @jsii.member(jsii_name="resetPrivilegedAccessManagerCustomEndpoint")
    def reset_privileged_access_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivilegedAccessManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublicCaCustomEndpoint")
    def reset_public_ca_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicCaCustomEndpoint", []))

    @jsii.member(jsii_name="resetPubsubCustomEndpoint")
    def reset_pubsub_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubCustomEndpoint", []))

    @jsii.member(jsii_name="resetPubsubLiteCustomEndpoint")
    def reset_pubsub_lite_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubLiteCustomEndpoint", []))

    @jsii.member(jsii_name="resetRecaptchaEnterpriseCustomEndpoint")
    def reset_recaptcha_enterprise_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecaptchaEnterpriseCustomEndpoint", []))

    @jsii.member(jsii_name="resetRedisCustomEndpoint")
    def reset_redis_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisCustomEndpoint", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRequestReason")
    def reset_request_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestReason", []))

    @jsii.member(jsii_name="resetRequestTimeout")
    def reset_request_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestTimeout", []))

    @jsii.member(jsii_name="resetResourceManager3CustomEndpoint")
    def reset_resource_manager3_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManager3CustomEndpoint", []))

    @jsii.member(jsii_name="resetResourceManagerCustomEndpoint")
    def reset_resource_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetResourceManagerV3CustomEndpoint")
    def reset_resource_manager_v3_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerV3CustomEndpoint", []))

    @jsii.member(jsii_name="resetRuntimeconfigCustomEndpoint")
    def reset_runtimeconfig_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeconfigCustomEndpoint", []))

    @jsii.member(jsii_name="resetRuntimeConfigCustomEndpoint")
    def reset_runtime_config_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeConfigCustomEndpoint", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetSecretManagerCustomEndpoint")
    def reset_secret_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetSecretManagerRegionalCustomEndpoint")
    def reset_secret_manager_regional_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerRegionalCustomEndpoint", []))

    @jsii.member(jsii_name="resetSecureSourceManagerCustomEndpoint")
    def reset_secure_source_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecureSourceManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetSecurityCenterCustomEndpoint")
    def reset_security_center_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityCenterCustomEndpoint", []))

    @jsii.member(jsii_name="resetSecurityCenterManagementCustomEndpoint")
    def reset_security_center_management_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityCenterManagementCustomEndpoint", []))

    @jsii.member(jsii_name="resetSecurityCenterV2CustomEndpoint")
    def reset_security_center_v2_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityCenterV2CustomEndpoint", []))

    @jsii.member(jsii_name="resetSecuritypostureCustomEndpoint")
    def reset_securityposture_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecuritypostureCustomEndpoint", []))

    @jsii.member(jsii_name="resetSecurityScannerCustomEndpoint")
    def reset_security_scanner_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityScannerCustomEndpoint", []))

    @jsii.member(jsii_name="resetServiceDirectoryCustomEndpoint")
    def reset_service_directory_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryCustomEndpoint", []))

    @jsii.member(jsii_name="resetServiceManagementCustomEndpoint")
    def reset_service_management_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceManagementCustomEndpoint", []))

    @jsii.member(jsii_name="resetServiceNetworkingCustomEndpoint")
    def reset_service_networking_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNetworkingCustomEndpoint", []))

    @jsii.member(jsii_name="resetServiceUsageCustomEndpoint")
    def reset_service_usage_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceUsageCustomEndpoint", []))

    @jsii.member(jsii_name="resetSiteVerificationCustomEndpoint")
    def reset_site_verification_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSiteVerificationCustomEndpoint", []))

    @jsii.member(jsii_name="resetSourceRepoCustomEndpoint")
    def reset_source_repo_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceRepoCustomEndpoint", []))

    @jsii.member(jsii_name="resetSpannerCustomEndpoint")
    def reset_spanner_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpannerCustomEndpoint", []))

    @jsii.member(jsii_name="resetSqlCustomEndpoint")
    def reset_sql_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlCustomEndpoint", []))

    @jsii.member(jsii_name="resetStorageBatchOperationsCustomEndpoint")
    def reset_storage_batch_operations_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageBatchOperationsCustomEndpoint", []))

    @jsii.member(jsii_name="resetStorageControlCustomEndpoint")
    def reset_storage_control_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageControlCustomEndpoint", []))

    @jsii.member(jsii_name="resetStorageCustomEndpoint")
    def reset_storage_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageCustomEndpoint", []))

    @jsii.member(jsii_name="resetStorageInsightsCustomEndpoint")
    def reset_storage_insights_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageInsightsCustomEndpoint", []))

    @jsii.member(jsii_name="resetStorageTransferCustomEndpoint")
    def reset_storage_transfer_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageTransferCustomEndpoint", []))

    @jsii.member(jsii_name="resetTagsCustomEndpoint")
    def reset_tags_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsCustomEndpoint", []))

    @jsii.member(jsii_name="resetTagsLocationCustomEndpoint")
    def reset_tags_location_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsLocationCustomEndpoint", []))

    @jsii.member(jsii_name="resetTerraformAttributionLabelAdditionStrategy")
    def reset_terraform_attribution_label_addition_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerraformAttributionLabelAdditionStrategy", []))

    @jsii.member(jsii_name="resetTpuCustomEndpoint")
    def reset_tpu_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpuCustomEndpoint", []))

    @jsii.member(jsii_name="resetTpuV2CustomEndpoint")
    def reset_tpu_v2_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpuV2CustomEndpoint", []))

    @jsii.member(jsii_name="resetTranscoderCustomEndpoint")
    def reset_transcoder_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTranscoderCustomEndpoint", []))

    @jsii.member(jsii_name="resetUniverseDomain")
    def reset_universe_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniverseDomain", []))

    @jsii.member(jsii_name="resetUserProjectOverride")
    def reset_user_project_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserProjectOverride", []))

    @jsii.member(jsii_name="resetVertexAiCustomEndpoint")
    def reset_vertex_ai_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVertexAiCustomEndpoint", []))

    @jsii.member(jsii_name="resetVmwareengineCustomEndpoint")
    def reset_vmwareengine_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmwareengineCustomEndpoint", []))

    @jsii.member(jsii_name="resetVpcAccessCustomEndpoint")
    def reset_vpc_access_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccessCustomEndpoint", []))

    @jsii.member(jsii_name="resetWorkbenchCustomEndpoint")
    def reset_workbench_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkbenchCustomEndpoint", []))

    @jsii.member(jsii_name="resetWorkflowsCustomEndpoint")
    def reset_workflows_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflowsCustomEndpoint", []))

    @jsii.member(jsii_name="resetWorkstationsCustomEndpoint")
    def reset_workstations_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkstationsCustomEndpoint", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accessApprovalCustomEndpointInput")
    def access_approval_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessApprovalCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="accessContextManagerCustomEndpointInput")
    def access_context_manager_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessContextManagerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryCustomEndpointInput")
    def active_directory_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeDirectoryCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="addTerraformAttributionLabelInput")
    def add_terraform_attribution_label_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "addTerraformAttributionLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="alloydbCustomEndpointInput")
    def alloydb_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alloydbCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayCustomEndpointInput")
    def api_gateway_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiGatewayCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="apigeeCustomEndpointInput")
    def apigee_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apigeeCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="apihubCustomEndpointInput")
    def apihub_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apihubCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="apikeysCustomEndpointInput")
    def apikeys_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apikeysCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="appEngineCustomEndpointInput")
    def app_engine_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appEngineCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="apphubCustomEndpointInput")
    def apphub_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apphubCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactRegistryCustomEndpointInput")
    def artifact_registry_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactRegistryCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="assuredWorkloadsCustomEndpointInput")
    def assured_workloads_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assuredWorkloadsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="backupDrCustomEndpointInput")
    def backup_dr_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupDrCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="batchingInput")
    def batching_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderBatching"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderBatching"]]], jsii.get(self, "batchingInput"))

    @builtins.property
    @jsii.member(jsii_name="beyondcorpCustomEndpointInput")
    def beyondcorp_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "beyondcorpCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="biglakeCustomEndpointInput")
    def biglake_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "biglakeCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryAnalyticsHubCustomEndpointInput")
    def bigquery_analytics_hub_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryAnalyticsHubCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryConnectionCustomEndpointInput")
    def bigquery_connection_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryConnectionCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="bigQueryCustomEndpointInput")
    def big_query_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigQueryCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDatapolicyCustomEndpointInput")
    def bigquery_datapolicy_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryDatapolicyCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDataTransferCustomEndpointInput")
    def bigquery_data_transfer_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryDataTransferCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryReservationCustomEndpointInput")
    def bigquery_reservation_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryReservationCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="bigtableCustomEndpointInput")
    def bigtable_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigtableCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="billingCustomEndpointInput")
    def billing_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="billingProjectInput")
    def billing_project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingProjectInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationCustomEndpointInput")
    def binary_authorization_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryAuthorizationCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="blockchainNodeEngineCustomEndpointInput")
    def blockchain_node_engine_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockchainNodeEngineCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateManagerCustomEndpointInput")
    def certificate_manager_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateManagerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="chronicleCustomEndpointInput")
    def chronicle_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chronicleCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudAssetCustomEndpointInput")
    def cloud_asset_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudAssetCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudBillingCustomEndpointInput")
    def cloud_billing_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudBillingCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudBuildCustomEndpointInput")
    def cloud_build_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudBuildCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudbuildv2CustomEndpointInput")
    def cloudbuildv2_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudbuildv2CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudBuildWorkerPoolCustomEndpointInput")
    def cloud_build_worker_pool_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudBuildWorkerPoolCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clouddeployCustomEndpointInput")
    def clouddeploy_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clouddeployCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clouddomainsCustomEndpointInput")
    def clouddomains_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clouddomainsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudfunctions2CustomEndpointInput")
    def cloudfunctions2_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudfunctions2CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudFunctionsCustomEndpointInput")
    def cloud_functions_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudFunctionsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudIdentityCustomEndpointInput")
    def cloud_identity_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudIdentityCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudIdsCustomEndpointInput")
    def cloud_ids_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudIdsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudQuotasCustomEndpointInput")
    def cloud_quotas_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudQuotasCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudResourceManagerCustomEndpointInput")
    def cloud_resource_manager_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudResourceManagerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunCustomEndpointInput")
    def cloud_run_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudRunCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunV2CustomEndpointInput")
    def cloud_run_v2_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudRunV2CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSchedulerCustomEndpointInput")
    def cloud_scheduler_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudSchedulerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudTasksCustomEndpointInput")
    def cloud_tasks_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudTasksCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="colabCustomEndpointInput")
    def colab_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "colabCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="composerCustomEndpointInput")
    def composer_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "composerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="computeCustomEndpointInput")
    def compute_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="containerAnalysisCustomEndpointInput")
    def container_analysis_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAnalysisCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="containerAttachedCustomEndpointInput")
    def container_attached_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAttachedCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="containerAwsCustomEndpointInput")
    def container_aws_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAwsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="containerAzureCustomEndpointInput")
    def container_azure_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAzureCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="containerCustomEndpointInput")
    def container_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="coreBillingCustomEndpointInput")
    def core_billing_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coreBillingCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseMigrationServiceCustomEndpointInput")
    def database_migration_service_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseMigrationServiceCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogCustomEndpointInput")
    def data_catalog_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataCatalogCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataflowCustomEndpointInput")
    def dataflow_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataflowCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataformCustomEndpointInput")
    def dataform_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataformCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFusionCustomEndpointInput")
    def data_fusion_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFusionCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataLossPreventionCustomEndpointInput")
    def data_loss_prevention_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataLossPreventionCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPipelineCustomEndpointInput")
    def data_pipeline_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataPipelineCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataplexCustomEndpointInput")
    def dataplex_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataplexCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocCustomEndpointInput")
    def dataproc_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocGdcCustomEndpointInput")
    def dataproc_gdc_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocGdcCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreCustomEndpointInput")
    def dataproc_metastore_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocMetastoreCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="datastreamCustomEndpointInput")
    def datastream_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datastreamCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLabelsInput")
    def default_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "defaultLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentManagerCustomEndpointInput")
    def deployment_manager_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentManagerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="developerConnectCustomEndpointInput")
    def developer_connect_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "developerConnectCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowCustomEndpointInput")
    def dialogflow_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dialogflowCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowCxCustomEndpointInput")
    def dialogflow_cx_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dialogflowCxCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="discoveryEngineCustomEndpointInput")
    def discovery_engine_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "discoveryEngineCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsCustomEndpointInput")
    def dns_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="documentAiCustomEndpointInput")
    def document_ai_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentAiCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="documentAiWarehouseCustomEndpointInput")
    def document_ai_warehouse_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentAiWarehouseCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="edgecontainerCustomEndpointInput")
    def edgecontainer_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgecontainerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="edgenetworkCustomEndpointInput")
    def edgenetwork_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgenetworkCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="essentialContactsCustomEndpointInput")
    def essential_contacts_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "essentialContactsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="eventarcCustomEndpointInput")
    def eventarc_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventarcCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="externalCredentialsInput")
    def external_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderExternalCredentials"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderExternalCredentials"]]], jsii.get(self, "externalCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="filestoreCustomEndpointInput")
    def filestore_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filestoreCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaseAppCheckCustomEndpointInput")
    def firebase_app_check_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseAppCheckCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaseAppHostingCustomEndpointInput")
    def firebase_app_hosting_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseAppHostingCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaseCustomEndpointInput")
    def firebase_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaseDatabaseCustomEndpointInput")
    def firebase_database_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseDatabaseCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaseDataConnectCustomEndpointInput")
    def firebase_data_connect_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseDataConnectCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaseExtensionsCustomEndpointInput")
    def firebase_extensions_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseExtensionsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaseHostingCustomEndpointInput")
    def firebase_hosting_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseHostingCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaserulesCustomEndpointInput")
    def firebaserules_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaserulesCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaseStorageCustomEndpointInput")
    def firebase_storage_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseStorageCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firestoreCustomEndpointInput")
    def firestore_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firestoreCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="geminiCustomEndpointInput")
    def gemini_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geminiCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeBackupCustomEndpointInput")
    def gke_backup_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeBackupCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeHub2CustomEndpointInput")
    def gke_hub2_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeHub2CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeHubCustomEndpointInput")
    def gke_hub_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeHubCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="gkehubFeatureCustomEndpointInput")
    def gkehub_feature_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkehubFeatureCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeonpremCustomEndpointInput")
    def gkeonprem_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeonpremCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="healthcareCustomEndpointInput")
    def healthcare_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthcareCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="iam2CustomEndpointInput")
    def iam2_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iam2CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="iam3CustomEndpointInput")
    def iam3_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iam3CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="iamBetaCustomEndpointInput")
    def iam_beta_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamBetaCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="iamCredentialsCustomEndpointInput")
    def iam_credentials_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamCredentialsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="iamCustomEndpointInput")
    def iam_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="iamWorkforcePoolCustomEndpointInput")
    def iam_workforce_pool_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamWorkforcePoolCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="iapCustomEndpointInput")
    def iap_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iapCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="identityPlatformCustomEndpointInput")
    def identity_platform_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityPlatformCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="impersonateServiceAccountDelegatesInput")
    def impersonate_service_account_delegates_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "impersonateServiceAccountDelegatesInput"))

    @builtins.property
    @jsii.member(jsii_name="impersonateServiceAccountInput")
    def impersonate_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "impersonateServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationConnectorsCustomEndpointInput")
    def integration_connectors_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationConnectorsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationsCustomEndpointInput")
    def integrations_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsCustomEndpointInput")
    def kms_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingCustomEndpointInput")
    def logging_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="lookerCustomEndpointInput")
    def looker_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lookerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="lustreCustomEndpointInput")
    def lustre_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lustreCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="managedKafkaCustomEndpointInput")
    def managed_kafka_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedKafkaCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="memcacheCustomEndpointInput")
    def memcache_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memcacheCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="memorystoreCustomEndpointInput")
    def memorystore_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memorystoreCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="migrationCenterCustomEndpointInput")
    def migration_center_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "migrationCenterCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="mlEngineCustomEndpointInput")
    def ml_engine_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mlEngineCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringCustomEndpointInput")
    def monitoring_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitoringCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="netappCustomEndpointInput")
    def netapp_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netappCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConnectivityCustomEndpointInput")
    def network_connectivity_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkConnectivityCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="networkManagementCustomEndpointInput")
    def network_management_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkManagementCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="networkSecurityCustomEndpointInput")
    def network_security_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkSecurityCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="networkServicesCustomEndpointInput")
    def network_services_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkServicesCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="notebooksCustomEndpointInput")
    def notebooks_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebooksCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleDatabaseCustomEndpointInput")
    def oracle_database_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oracleDatabaseCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="orgPolicyCustomEndpointInput")
    def org_policy_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgPolicyCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="osConfigCustomEndpointInput")
    def os_config_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osConfigCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="osConfigV2CustomEndpointInput")
    def os_config_v2_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osConfigV2CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="osLoginCustomEndpointInput")
    def os_login_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osLoginCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelstoreCustomEndpointInput")
    def parallelstore_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parallelstoreCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterManagerCustomEndpointInput")
    def parameter_manager_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterManagerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterManagerRegionalCustomEndpointInput")
    def parameter_manager_regional_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterManagerRegionalCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="privatecaCustomEndpointInput")
    def privateca_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privatecaCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegedAccessManagerCustomEndpointInput")
    def privileged_access_manager_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privilegedAccessManagerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="publicCaCustomEndpointInput")
    def public_ca_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicCaCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubCustomEndpointInput")
    def pubsub_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubLiteCustomEndpointInput")
    def pubsub_lite_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubLiteCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaEnterpriseCustomEndpointInput")
    def recaptcha_enterprise_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recaptchaEnterpriseCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="redisCustomEndpointInput")
    def redis_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestReasonInput")
    def request_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="requestTimeoutInput")
    def request_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceManager3CustomEndpointInput")
    def resource_manager3_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceManager3CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerCustomEndpointInput")
    def resource_manager_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceManagerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerV3CustomEndpointInput")
    def resource_manager_v3_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceManagerV3CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeconfigCustomEndpointInput")
    def runtimeconfig_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeconfigCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfigCustomEndpointInput")
    def runtime_config_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeConfigCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerCustomEndpointInput")
    def secret_manager_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerRegionalCustomEndpointInput")
    def secret_manager_regional_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerRegionalCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="secureSourceManagerCustomEndpointInput")
    def secure_source_manager_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secureSourceManagerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="securityCenterCustomEndpointInput")
    def security_center_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityCenterCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="securityCenterManagementCustomEndpointInput")
    def security_center_management_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityCenterManagementCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="securityCenterV2CustomEndpointInput")
    def security_center_v2_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityCenterV2CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="securitypostureCustomEndpointInput")
    def securityposture_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securitypostureCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="securityScannerCustomEndpointInput")
    def security_scanner_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityScannerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryCustomEndpointInput")
    def service_directory_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceDirectoryCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceManagementCustomEndpointInput")
    def service_management_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceManagementCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkingCustomEndpointInput")
    def service_networking_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNetworkingCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceUsageCustomEndpointInput")
    def service_usage_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceUsageCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="siteVerificationCustomEndpointInput")
    def site_verification_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteVerificationCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRepoCustomEndpointInput")
    def source_repo_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRepoCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="spannerCustomEndpointInput")
    def spanner_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spannerCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlCustomEndpointInput")
    def sql_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="storageBatchOperationsCustomEndpointInput")
    def storage_batch_operations_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageBatchOperationsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="storageControlCustomEndpointInput")
    def storage_control_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageControlCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="storageCustomEndpointInput")
    def storage_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInsightsCustomEndpointInput")
    def storage_insights_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageInsightsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="storageTransferCustomEndpointInput")
    def storage_transfer_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageTransferCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsCustomEndpointInput")
    def tags_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsLocationCustomEndpointInput")
    def tags_location_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagsLocationCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="terraformAttributionLabelAdditionStrategyInput")
    def terraform_attribution_label_addition_strategy_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformAttributionLabelAdditionStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="tpuCustomEndpointInput")
    def tpu_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpuCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="tpuV2CustomEndpointInput")
    def tpu_v2_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpuV2CustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="transcoderCustomEndpointInput")
    def transcoder_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transcoderCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="universeDomainInput")
    def universe_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "universeDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="userProjectOverrideInput")
    def user_project_override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userProjectOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="vertexAiCustomEndpointInput")
    def vertex_ai_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vertexAiCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="vmwareengineCustomEndpointInput")
    def vmwareengine_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmwareengineCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessCustomEndpointInput")
    def vpc_access_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcAccessCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="workbenchCustomEndpointInput")
    def workbench_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workbenchCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowsCustomEndpointInput")
    def workflows_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="workstationsCustomEndpointInput")
    def workstations_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workstationsCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="accessApprovalCustomEndpoint")
    def access_approval_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessApprovalCustomEndpoint"))

    @access_approval_custom_endpoint.setter
    def access_approval_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__277b135c45e1f36c53e3d6259bc2e9b67e398af621946044f49c76987759ac70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessApprovalCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessContextManagerCustomEndpoint")
    def access_context_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessContextManagerCustomEndpoint"))

    @access_context_manager_custom_endpoint.setter
    def access_context_manager_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a79e0eda73c39486edd2476fd0478aa96c302f7caeaa0237544255b31b955b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessContextManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279293696549d3620383fba86650deae2fbfd4e534270bb5546382da607f2519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryCustomEndpoint")
    def active_directory_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeDirectoryCustomEndpoint"))

    @active_directory_custom_endpoint.setter
    def active_directory_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c33ac2a832f17924fabe06c300baf587ef1d25ab9b65b7b2c03b14f61b1224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addTerraformAttributionLabel")
    def add_terraform_attribution_label(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "addTerraformAttributionLabel"))

    @add_terraform_attribution_label.setter
    def add_terraform_attribution_label(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06d16a0fb6e3bb74b6ac090679bb407db97981fe8b4afe346763c78f001ce6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addTerraformAttributionLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0787e4e3080f2ea5478f760a1ae96f889d67e334e927b487d33a54ecdd4b0bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alloydbCustomEndpoint")
    def alloydb_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alloydbCustomEndpoint"))

    @alloydb_custom_endpoint.setter
    def alloydb_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909a834d18cc31be72737093f6bbad3d0ddfccf4ccad73f8ed5d1470d84d6082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alloydbCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiGatewayCustomEndpoint")
    def api_gateway_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiGatewayCustomEndpoint"))

    @api_gateway_custom_endpoint.setter
    def api_gateway_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a4e3d94a7dc556f3aacca26f463f68696a64705f6356ba742a76d8f0d57037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiGatewayCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apigeeCustomEndpoint")
    def apigee_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apigeeCustomEndpoint"))

    @apigee_custom_endpoint.setter
    def apigee_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2f7f919a3d93f81392e9357777b83216485f80d731089aa76bfeff8333d24a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apigeeCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apihubCustomEndpoint")
    def apihub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apihubCustomEndpoint"))

    @apihub_custom_endpoint.setter
    def apihub_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78759a0e1be2766b57dea4cf8f34f853dc0a1790e861ddb0330709fda70af8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apihubCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apikeysCustomEndpoint")
    def apikeys_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apikeysCustomEndpoint"))

    @apikeys_custom_endpoint.setter
    def apikeys_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8d52d7c4b41479af7ce0d8cb9b5dc72eb8c5efe0dab27a78042b05034a4f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apikeysCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appEngineCustomEndpoint")
    def app_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appEngineCustomEndpoint"))

    @app_engine_custom_endpoint.setter
    def app_engine_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7403f0dc8519653edcf8eb699807d991bfa40fa013d9911aa8b0c4edcf417a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appEngineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apphubCustomEndpoint")
    def apphub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apphubCustomEndpoint"))

    @apphub_custom_endpoint.setter
    def apphub_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8bc16eee0e7e41e825c803ba456a5844215cafd87cd6d9ede0aff8270ad4ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apphubCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="artifactRegistryCustomEndpoint")
    def artifact_registry_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactRegistryCustomEndpoint"))

    @artifact_registry_custom_endpoint.setter
    def artifact_registry_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6403a296e73cd5c56d9e1b6f247494f9eece6a62884f5ad1f4b3e67d05e4a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactRegistryCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assuredWorkloadsCustomEndpoint")
    def assured_workloads_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assuredWorkloadsCustomEndpoint"))

    @assured_workloads_custom_endpoint.setter
    def assured_workloads_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09810854ef17d3dbaca0b75f5b72a4f874704681b0dc41c660a732d23c9b342a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assuredWorkloadsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupDrCustomEndpoint")
    def backup_dr_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupDrCustomEndpoint"))

    @backup_dr_custom_endpoint.setter
    def backup_dr_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12fee8a212f7bbc8e3d32ee0ce8bd27ae14fabe330887745b9ea581bf907d38f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupDrCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="batching")
    def batching(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderBatching"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderBatching"]]], jsii.get(self, "batching"))

    @batching.setter
    def batching(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderBatching"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3b319071259ceb02b77c72747b16e27fde115d7bbba257180f9ea390c0c8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="beyondcorpCustomEndpoint")
    def beyondcorp_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "beyondcorpCustomEndpoint"))

    @beyondcorp_custom_endpoint.setter
    def beyondcorp_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bec08d530be531b8494d0df258bb2a55c6f0763b522a8587b6f0f32f41f3e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beyondcorpCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="biglakeCustomEndpoint")
    def biglake_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "biglakeCustomEndpoint"))

    @biglake_custom_endpoint.setter
    def biglake_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d803a6adfc2857c900ad1b01cb82b1abb27fde87432ee66399d4f22f231ae1c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "biglakeCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bigqueryAnalyticsHubCustomEndpoint")
    def bigquery_analytics_hub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryAnalyticsHubCustomEndpoint"))

    @bigquery_analytics_hub_custom_endpoint.setter
    def bigquery_analytics_hub_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13223b4eddb793529314c142bc32f27f7cb1ce79b5ad68c64c7a0fdf969e1914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigqueryAnalyticsHubCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bigqueryConnectionCustomEndpoint")
    def bigquery_connection_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryConnectionCustomEndpoint"))

    @bigquery_connection_custom_endpoint.setter
    def bigquery_connection_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3efb8641cc3c55085ac1b4866d4284b129951f45f33d2c9e94b9116da19c99cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigqueryConnectionCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bigQueryCustomEndpoint")
    def big_query_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigQueryCustomEndpoint"))

    @big_query_custom_endpoint.setter
    def big_query_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8d2749a637080806771911f5123d8a726e8b3367dec0c6d58e693072528374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigQueryCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bigqueryDatapolicyCustomEndpoint")
    def bigquery_datapolicy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryDatapolicyCustomEndpoint"))

    @bigquery_datapolicy_custom_endpoint.setter
    def bigquery_datapolicy_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06c550df17c3e3bd9363ae923c9ad3e6e600f99acd1df7ae0274afa1d2f6d016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigqueryDatapolicyCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bigqueryDataTransferCustomEndpoint")
    def bigquery_data_transfer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryDataTransferCustomEndpoint"))

    @bigquery_data_transfer_custom_endpoint.setter
    def bigquery_data_transfer_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52690aa938c990a769452e4879075ea2e851b81e9ad2d5a9dd46c01038d1c0ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigqueryDataTransferCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bigqueryReservationCustomEndpoint")
    def bigquery_reservation_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigqueryReservationCustomEndpoint"))

    @bigquery_reservation_custom_endpoint.setter
    def bigquery_reservation_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19f0c25fd5890ebc21e1f5cf7b32927508352c17e219ff9551ab172049155e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigqueryReservationCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bigtableCustomEndpoint")
    def bigtable_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigtableCustomEndpoint"))

    @bigtable_custom_endpoint.setter
    def bigtable_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34bbaea14f860ae3ef73b5bde905679593cb2f59b439d04dd33aafc9d5174095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigtableCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingCustomEndpoint")
    def billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingCustomEndpoint"))

    @billing_custom_endpoint.setter
    def billing_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df62387c443e8b15d0e183156dcff070053a4cd00a2e5b550c044f3f54de4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingProject")
    def billing_project(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingProject"))

    @billing_project.setter
    def billing_project(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68068de88f171aa0ee628d7c916a1296349de9382dabf2056a9fc0fe0cc1621c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationCustomEndpoint")
    def binary_authorization_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryAuthorizationCustomEndpoint"))

    @binary_authorization_custom_endpoint.setter
    def binary_authorization_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bcbcafd8668702c903270203c5a7be030092062e8f9b13989f146f13be32f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryAuthorizationCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blockchainNodeEngineCustomEndpoint")
    def blockchain_node_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockchainNodeEngineCustomEndpoint"))

    @blockchain_node_engine_custom_endpoint.setter
    def blockchain_node_engine_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45350c75dd13c69b9b1254d6f3ff5268d2b599dc20e8fa079d4b98b914186119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockchainNodeEngineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateManagerCustomEndpoint")
    def certificate_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateManagerCustomEndpoint"))

    @certificate_manager_custom_endpoint.setter
    def certificate_manager_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c66f0e49843317abde0fe81934aedf593a0bfea9be63fce8de4884162578c8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="chronicleCustomEndpoint")
    def chronicle_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chronicleCustomEndpoint"))

    @chronicle_custom_endpoint.setter
    def chronicle_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8e221f1eada3611ca14ce9a5c5f9f3addbfadf062f07d1c193cc27a8ac3cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chronicleCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudAssetCustomEndpoint")
    def cloud_asset_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudAssetCustomEndpoint"))

    @cloud_asset_custom_endpoint.setter
    def cloud_asset_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a40176a1055e782aca6e3a4fcbfa6877196c24006915677f98bb4c52a5a0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudAssetCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudBillingCustomEndpoint")
    def cloud_billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudBillingCustomEndpoint"))

    @cloud_billing_custom_endpoint.setter
    def cloud_billing_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7799685f41ed1c973a6a1ddbdb95bcb810668b3a643ecb5e41f3a3794e421c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudBillingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudBuildCustomEndpoint")
    def cloud_build_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudBuildCustomEndpoint"))

    @cloud_build_custom_endpoint.setter
    def cloud_build_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65110ec7f849976770de17c3725ac57498276ff76b348a6d8568c66ef88c59e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudBuildCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudbuildv2CustomEndpoint")
    def cloudbuildv2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudbuildv2CustomEndpoint"))

    @cloudbuildv2_custom_endpoint.setter
    def cloudbuildv2_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9977b67c753f417d60971b0a883bbd9af092727c524e42ee479f50ccf46c8b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudbuildv2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudBuildWorkerPoolCustomEndpoint")
    def cloud_build_worker_pool_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudBuildWorkerPoolCustomEndpoint"))

    @cloud_build_worker_pool_custom_endpoint.setter
    def cloud_build_worker_pool_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edeb4ead8d80df25f1e99cbeddb63c5b32fed6f6a3cf254e4e8df32c074c042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudBuildWorkerPoolCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clouddeployCustomEndpoint")
    def clouddeploy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clouddeployCustomEndpoint"))

    @clouddeploy_custom_endpoint.setter
    def clouddeploy_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ad023dfd7b35fc0e60d201d987643b327f3dd0f678943bf2c5a84b489d7d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clouddeployCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clouddomainsCustomEndpoint")
    def clouddomains_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clouddomainsCustomEndpoint"))

    @clouddomains_custom_endpoint.setter
    def clouddomains_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fb7e943e788ad08a55ff0b9233e1bd183b0eda7b22835ee2641e89f1d11613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clouddomainsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudfunctions2CustomEndpoint")
    def cloudfunctions2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudfunctions2CustomEndpoint"))

    @cloudfunctions2_custom_endpoint.setter
    def cloudfunctions2_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297f475b1a6814835e1485081c685731da37a34461ee6708e3d2ecea1e2b27dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudfunctions2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudFunctionsCustomEndpoint")
    def cloud_functions_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudFunctionsCustomEndpoint"))

    @cloud_functions_custom_endpoint.setter
    def cloud_functions_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0483a0b3ca8290da1d2338a077bb80f1d3a6419f74255c90f110eb2c45b79e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudFunctionsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudIdentityCustomEndpoint")
    def cloud_identity_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudIdentityCustomEndpoint"))

    @cloud_identity_custom_endpoint.setter
    def cloud_identity_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d5ec9567f22107fa330d6412f3edaa076e4c5b25b880bf04282bed78ac4e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudIdentityCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudIdsCustomEndpoint")
    def cloud_ids_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudIdsCustomEndpoint"))

    @cloud_ids_custom_endpoint.setter
    def cloud_ids_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6144a72cd33c762d7300406419e5c43ebb579cb66a54a99114a3eb45c92ea44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudIdsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudQuotasCustomEndpoint")
    def cloud_quotas_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudQuotasCustomEndpoint"))

    @cloud_quotas_custom_endpoint.setter
    def cloud_quotas_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3b78732498d99005c6e8b86cb12da5fb5203bd31f6956b91372cd1d5d0be5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudQuotasCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudResourceManagerCustomEndpoint")
    def cloud_resource_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudResourceManagerCustomEndpoint"))

    @cloud_resource_manager_custom_endpoint.setter
    def cloud_resource_manager_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc03072cf715797626e6838106e765f8cf89fd21f4f69ced55a497cd7ba3f77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudResourceManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudRunCustomEndpoint")
    def cloud_run_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudRunCustomEndpoint"))

    @cloud_run_custom_endpoint.setter
    def cloud_run_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8336e6be0948f35cde26196545b7a68d472abcdb64e2dcff5e308a9ff28cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudRunCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudRunV2CustomEndpoint")
    def cloud_run_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudRunV2CustomEndpoint"))

    @cloud_run_v2_custom_endpoint.setter
    def cloud_run_v2_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0329c1f238b71f12159a8683cc307e3a73cb02e4e9e70aea1e5336509e9b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudRunV2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudSchedulerCustomEndpoint")
    def cloud_scheduler_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudSchedulerCustomEndpoint"))

    @cloud_scheduler_custom_endpoint.setter
    def cloud_scheduler_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f3d0c894c04fd73eeeb63656da3f257e2ce7f14fb887e0e8eb2ea0551e54c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSchedulerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudTasksCustomEndpoint")
    def cloud_tasks_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudTasksCustomEndpoint"))

    @cloud_tasks_custom_endpoint.setter
    def cloud_tasks_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae9575f69905842bd484785ba031751341873761039b3d860f7d03b8df9cded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudTasksCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="colabCustomEndpoint")
    def colab_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "colabCustomEndpoint"))

    @colab_custom_endpoint.setter
    def colab_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc05d7fc7b1900fd2b59712dc1db57f1d4684bd1eb9c79c965c991a0893c51d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "colabCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="composerCustomEndpoint")
    def composer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "composerCustomEndpoint"))

    @composer_custom_endpoint.setter
    def composer_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d70ee7d8597c2852b8eff5cef83fd5fe5871b9f2dc084bf77fb7b1e48e146b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "composerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computeCustomEndpoint")
    def compute_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeCustomEndpoint"))

    @compute_custom_endpoint.setter
    def compute_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c1440b8ee9049c44ba8d02175aed090087094a3aa2c20b136a723e7fc461cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerAnalysisCustomEndpoint")
    def container_analysis_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAnalysisCustomEndpoint"))

    @container_analysis_custom_endpoint.setter
    def container_analysis_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594165eb917f308076b1e8602000deef67cfc404b2b89c8ca928be8af9a0406b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerAnalysisCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerAttachedCustomEndpoint")
    def container_attached_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAttachedCustomEndpoint"))

    @container_attached_custom_endpoint.setter
    def container_attached_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6935387c545fc24e8db2891f466215342a0a7a3d7500a628afe1bb460a040954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerAttachedCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerAwsCustomEndpoint")
    def container_aws_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAwsCustomEndpoint"))

    @container_aws_custom_endpoint.setter
    def container_aws_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c587f4ba61fca0d303fa8dabcc98fa3e1fdea837feedfa441819cad3e266e9a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerAwsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerAzureCustomEndpoint")
    def container_azure_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAzureCustomEndpoint"))

    @container_azure_custom_endpoint.setter
    def container_azure_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dffe094183562a726716929cd7e7c180b2c836215cc926302dd49641545467e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerAzureCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerCustomEndpoint")
    def container_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerCustomEndpoint"))

    @container_custom_endpoint.setter
    def container_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f743a40befb7832cb0250b3a0fe6b1349f3559881382f290dcb30c15947a962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coreBillingCustomEndpoint")
    def core_billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coreBillingCustomEndpoint"))

    @core_billing_custom_endpoint.setter
    def core_billing_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf1f684d698662b953e89a568935ba91386b7467ce411da6053d7d4a6feabc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreBillingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781e7ef8949e8098e387633d67fe3ea0e798690d66a9547fe7e2c84d23ba2911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseMigrationServiceCustomEndpoint")
    def database_migration_service_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseMigrationServiceCustomEndpoint"))

    @database_migration_service_custom_endpoint.setter
    def database_migration_service_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e97b9d7ecce45bcceb5308ce2dddca5d875a47c3a1850b0c348a2e615c5946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseMigrationServiceCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataCatalogCustomEndpoint")
    def data_catalog_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataCatalogCustomEndpoint"))

    @data_catalog_custom_endpoint.setter
    def data_catalog_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e5e262cfcda61da75f224e0fa4b234505f11655afd720aae8e983dd55b81857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataCatalogCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataflowCustomEndpoint")
    def dataflow_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataflowCustomEndpoint"))

    @dataflow_custom_endpoint.setter
    def dataflow_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9f59207e5ced72d362a91ecbdcf2fa719804a4441440017931b697a4d7564e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataflowCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataformCustomEndpoint")
    def dataform_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataformCustomEndpoint"))

    @dataform_custom_endpoint.setter
    def dataform_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42454630398f7deeeec3e6a30b0f4d943966bce2f359c68149a0f736d47cd037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataformCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFusionCustomEndpoint")
    def data_fusion_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFusionCustomEndpoint"))

    @data_fusion_custom_endpoint.setter
    def data_fusion_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09dc72140c1d2be4b7e68c94742f86be552fb8da22beb10689429db0862e1d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFusionCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataLossPreventionCustomEndpoint")
    def data_loss_prevention_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataLossPreventionCustomEndpoint"))

    @data_loss_prevention_custom_endpoint.setter
    def data_loss_prevention_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee8e39386feb134041e2ef2f8445b0109466667f333debe7b0834caddacdf977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataLossPreventionCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataPipelineCustomEndpoint")
    def data_pipeline_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataPipelineCustomEndpoint"))

    @data_pipeline_custom_endpoint.setter
    def data_pipeline_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7509c970485e43d8484bfe5d58ccf088ce9fe33930b4a8972bf46af9baf6363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataPipelineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataplexCustomEndpoint")
    def dataplex_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataplexCustomEndpoint"))

    @dataplex_custom_endpoint.setter
    def dataplex_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7fa61e7bfc0ae8cfb8a1cc45d1ca9594a1bef25d07826650fae3f5c3e35023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataplexCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataprocCustomEndpoint")
    def dataproc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocCustomEndpoint"))

    @dataproc_custom_endpoint.setter
    def dataproc_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8557ec8b3ece3e7bd76e25650187e8cfd82199a763f67b2a4aa26e8c81b0df83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataprocGdcCustomEndpoint")
    def dataproc_gdc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocGdcCustomEndpoint"))

    @dataproc_gdc_custom_endpoint.setter
    def dataproc_gdc_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c50c5131b38a0d7065499c9b3cb8d8a469271e302fb8637a03b32328a1c5ecd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocGdcCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreCustomEndpoint")
    def dataproc_metastore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocMetastoreCustomEndpoint"))

    @dataproc_metastore_custom_endpoint.setter
    def dataproc_metastore_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1457ccece6aad860986e78c01e92241fca81167611c262e7922002ec6e88e90f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocMetastoreCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datastreamCustomEndpoint")
    def datastream_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datastreamCustomEndpoint"))

    @datastream_custom_endpoint.setter
    def datastream_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b538b3242e339a1fbc77a21eae8de2dc4d59af4510a17323d191b847240cc7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datastreamCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLabels")
    def default_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "defaultLabels"))

    @default_labels.setter
    def default_labels(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97cf3d7f96646d6f44c1dad3bd367a8425aa308b182e37c9e9593f513f4bf511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentManagerCustomEndpoint")
    def deployment_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentManagerCustomEndpoint"))

    @deployment_manager_custom_endpoint.setter
    def deployment_manager_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df36c62ace8e49cea320b1df34f8d5cc169f23a514bd7db4a8af8e9188f27160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developerConnectCustomEndpoint")
    def developer_connect_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "developerConnectCustomEndpoint"))

    @developer_connect_custom_endpoint.setter
    def developer_connect_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa14129fc70abb49b617075e323a8c92610d3bf8d64c3773f3b1068f005173f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developerConnectCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dialogflowCustomEndpoint")
    def dialogflow_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dialogflowCustomEndpoint"))

    @dialogflow_custom_endpoint.setter
    def dialogflow_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7383c42c5676e804c21625984129145d98af9eaed2afeea19137c3ad9eb6d765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dialogflowCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dialogflowCxCustomEndpoint")
    def dialogflow_cx_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dialogflowCxCustomEndpoint"))

    @dialogflow_cx_custom_endpoint.setter
    def dialogflow_cx_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55dbde4287441ca53b8364cb3eb1fb3d02002ea9078071a49ff674edec8b7d08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dialogflowCxCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="discoveryEngineCustomEndpoint")
    def discovery_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "discoveryEngineCustomEndpoint"))

    @discovery_engine_custom_endpoint.setter
    def discovery_engine_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70fd76c17a8571105fd3d2860f0a31f01527df3ebf6dfd657847914a8927160a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discoveryEngineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsCustomEndpoint")
    def dns_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsCustomEndpoint"))

    @dns_custom_endpoint.setter
    def dns_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f919ff2bcc878515f30894852650c0cc18d2c9b10a5e57115ea6166c15fb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentAiCustomEndpoint")
    def document_ai_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentAiCustomEndpoint"))

    @document_ai_custom_endpoint.setter
    def document_ai_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d08c038cbac78ce24f7e02d5588f46a08383d7f75a570ffecd63fffad7ad63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentAiCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentAiWarehouseCustomEndpoint")
    def document_ai_warehouse_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentAiWarehouseCustomEndpoint"))

    @document_ai_warehouse_custom_endpoint.setter
    def document_ai_warehouse_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2465f7590332147a3c0a6ad53241dfafcddc2f83e354c2007d4286a6434e139d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentAiWarehouseCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgecontainerCustomEndpoint")
    def edgecontainer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgecontainerCustomEndpoint"))

    @edgecontainer_custom_endpoint.setter
    def edgecontainer_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86faae4a5e206c1ba7ba0517c652774646e8ee885fd9e8cbebb226aa01e5aa6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgecontainerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgenetworkCustomEndpoint")
    def edgenetwork_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgenetworkCustomEndpoint"))

    @edgenetwork_custom_endpoint.setter
    def edgenetwork_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df40d7843585bd43698c2d9462672c223b28e16bd43552ecc793f6d5053fb694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgenetworkCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="essentialContactsCustomEndpoint")
    def essential_contacts_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "essentialContactsCustomEndpoint"))

    @essential_contacts_custom_endpoint.setter
    def essential_contacts_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ecb2a5f392b3275e436a6047dd9cc37455e22f70e50f95b4c47d14e24578f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "essentialContactsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventarcCustomEndpoint")
    def eventarc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventarcCustomEndpoint"))

    @eventarc_custom_endpoint.setter
    def eventarc_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0511b49e099f1d75cd08f6e3d9d0c5899beb9e5df4aecee1487beac9c3412e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventarcCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalCredentials")
    def external_credentials(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderExternalCredentials"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderExternalCredentials"]]], jsii.get(self, "externalCredentials"))

    @external_credentials.setter
    def external_credentials(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderExternalCredentials"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862ca0af72c2a59e81b74d34407ecf9798387a3e886a989861b40aca4f2e83c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filestoreCustomEndpoint")
    def filestore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filestoreCustomEndpoint"))

    @filestore_custom_endpoint.setter
    def filestore_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515578f0fa3414e1f587be77823d372563806bca4ba1a421f275af267cc22bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filestoreCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firebaseAppCheckCustomEndpoint")
    def firebase_app_check_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseAppCheckCustomEndpoint"))

    @firebase_app_check_custom_endpoint.setter
    def firebase_app_check_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c523080169447cf31f7704e572564aaa8977901dbb550e91fde62353a67425a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseAppCheckCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firebaseAppHostingCustomEndpoint")
    def firebase_app_hosting_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseAppHostingCustomEndpoint"))

    @firebase_app_hosting_custom_endpoint.setter
    def firebase_app_hosting_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ff4d6d7ca21691a78647262d00cf18031926338b90ff0f38be4a6897bad4e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseAppHostingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firebaseCustomEndpoint")
    def firebase_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseCustomEndpoint"))

    @firebase_custom_endpoint.setter
    def firebase_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37085d6d0c112005fb95b523fdd1f84b8faa41f7da1a546cd528fdfdce298b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firebaseDatabaseCustomEndpoint")
    def firebase_database_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseDatabaseCustomEndpoint"))

    @firebase_database_custom_endpoint.setter
    def firebase_database_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740b4ff1ccd145aa4815ca4594431c815aa6f3f53f88a227a97f6114563ec798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseDatabaseCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firebaseDataConnectCustomEndpoint")
    def firebase_data_connect_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseDataConnectCustomEndpoint"))

    @firebase_data_connect_custom_endpoint.setter
    def firebase_data_connect_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62f0d602ef39504e14219b727e18deaf689088d11c86a0851a19353f5287c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseDataConnectCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firebaseExtensionsCustomEndpoint")
    def firebase_extensions_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseExtensionsCustomEndpoint"))

    @firebase_extensions_custom_endpoint.setter
    def firebase_extensions_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac77163ad01854a6a13d786173be447d2380925669e156703b7a5e363ef5de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseExtensionsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firebaseHostingCustomEndpoint")
    def firebase_hosting_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseHostingCustomEndpoint"))

    @firebase_hosting_custom_endpoint.setter
    def firebase_hosting_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4c0d9d5a8225de17f54784604951f923074fda15e51e72d38d231771069c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseHostingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firebaserulesCustomEndpoint")
    def firebaserules_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaserulesCustomEndpoint"))

    @firebaserules_custom_endpoint.setter
    def firebaserules_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b980b19f58fb586745e89398640dd90281ee6252de9cc0b72c5efd86e2222b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaserulesCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firebaseStorageCustomEndpoint")
    def firebase_storage_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseStorageCustomEndpoint"))

    @firebase_storage_custom_endpoint.setter
    def firebase_storage_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61d658e7cdda012fb0d54ccb692c63fe773ed14856a151a097b1c5558d0093d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseStorageCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firestoreCustomEndpoint")
    def firestore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firestoreCustomEndpoint"))

    @firestore_custom_endpoint.setter
    def firestore_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e02c755630ad98326031533cc3f3ecdddb4629c6eec2cdbcf9d6b4dfd13e4fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firestoreCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geminiCustomEndpoint")
    def gemini_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geminiCustomEndpoint"))

    @gemini_custom_endpoint.setter
    def gemini_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8177d3e5b1630532f1e4e6bb33ea4d82398fcc40af1e34812fcb1b3f8f8bfad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geminiCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeBackupCustomEndpoint")
    def gke_backup_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeBackupCustomEndpoint"))

    @gke_backup_custom_endpoint.setter
    def gke_backup_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31af92754f7cccaf571e2a9de25c475277122680fd9bcc782004ab085cb82f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeBackupCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeHub2CustomEndpoint")
    def gke_hub2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeHub2CustomEndpoint"))

    @gke_hub2_custom_endpoint.setter
    def gke_hub2_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e9430b1003f8e02a77c781325da9e9f48db45addf49d7a2d152d5d8762618ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeHub2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeHubCustomEndpoint")
    def gke_hub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeHubCustomEndpoint"))

    @gke_hub_custom_endpoint.setter
    def gke_hub_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4bb05e0e27835248b17c226392bb99ff2ba32625fc9bdca51d0b285aea1b63f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeHubCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkehubFeatureCustomEndpoint")
    def gkehub_feature_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkehubFeatureCustomEndpoint"))

    @gkehub_feature_custom_endpoint.setter
    def gkehub_feature_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21951682d7460f4b766bd144c0a9d6e0027279da8cd0853a9ffd5921db0224d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkehubFeatureCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeonpremCustomEndpoint")
    def gkeonprem_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeonpremCustomEndpoint"))

    @gkeonprem_custom_endpoint.setter
    def gkeonprem_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2224e65c4c2baa326b676a4a5515ccfeb21b7a9ab7d2ed5bc8416c0c039d2c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeonpremCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthcareCustomEndpoint")
    def healthcare_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthcareCustomEndpoint"))

    @healthcare_custom_endpoint.setter
    def healthcare_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910c97876c8c450c429d36bbb9bee18ba4024bd93e23e01f4739eee29ccf93d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthcareCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iam2CustomEndpoint")
    def iam2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iam2CustomEndpoint"))

    @iam2_custom_endpoint.setter
    def iam2_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d40bcd0659a217e73c2d21f1151f7e26e38453a6315efa629752f72ac0d6aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iam2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iam3CustomEndpoint")
    def iam3_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iam3CustomEndpoint"))

    @iam3_custom_endpoint.setter
    def iam3_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e40f20576c2e4edb8ab56460d21a5fa3434a9f5b47526e62e3a0ffa58dffad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iam3CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamBetaCustomEndpoint")
    def iam_beta_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamBetaCustomEndpoint"))

    @iam_beta_custom_endpoint.setter
    def iam_beta_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deaac9b79a43ecbcc2bd353a085bc00385532ddb8bcd8270d8fdbdc811337b05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamBetaCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamCredentialsCustomEndpoint")
    def iam_credentials_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamCredentialsCustomEndpoint"))

    @iam_credentials_custom_endpoint.setter
    def iam_credentials_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c06e0c8ce729e984ef30354e151d4a3284ee05cb13addfc3c4d3d5890c9eee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamCredentialsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamCustomEndpoint")
    def iam_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamCustomEndpoint"))

    @iam_custom_endpoint.setter
    def iam_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c801f7a56bc9364ecb91d83c5edd4f8efb72eb76843fce749485bd25a5fbf14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamWorkforcePoolCustomEndpoint")
    def iam_workforce_pool_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamWorkforcePoolCustomEndpoint"))

    @iam_workforce_pool_custom_endpoint.setter
    def iam_workforce_pool_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66a59934fd4e2b04add1a8ead6662a2999905dc475159e45012365676b3ed9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamWorkforcePoolCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iapCustomEndpoint")
    def iap_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iapCustomEndpoint"))

    @iap_custom_endpoint.setter
    def iap_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ad2eea5652f568aba98083e76fa1417fb2db19c844a1660b1e4f34d6ada98c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iapCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityPlatformCustomEndpoint")
    def identity_platform_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityPlatformCustomEndpoint"))

    @identity_platform_custom_endpoint.setter
    def identity_platform_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109be11f9283c0efc33f0b423370fb012fff3a3938c4531b4e494b25733eb81f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityPlatformCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="impersonateServiceAccount")
    def impersonate_service_account(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "impersonateServiceAccount"))

    @impersonate_service_account.setter
    def impersonate_service_account(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f72aa0b243eadac1c7b1264ea0fbe21de31e132e7a45024864e90bb0017d2d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "impersonateServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="impersonateServiceAccountDelegates")
    def impersonate_service_account_delegates(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "impersonateServiceAccountDelegates"))

    @impersonate_service_account_delegates.setter
    def impersonate_service_account_delegates(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab17ec8e3c09a39cdcfacd377a16222fe714c4efce0a122b2de5a3c9242e66f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "impersonateServiceAccountDelegates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationConnectorsCustomEndpoint")
    def integration_connectors_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationConnectorsCustomEndpoint"))

    @integration_connectors_custom_endpoint.setter
    def integration_connectors_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf2b6106563398a7b1c503ac8bd10c8109c24e25f246db4bd05399ecb57e927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationConnectorsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationsCustomEndpoint")
    def integrations_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationsCustomEndpoint"))

    @integrations_custom_endpoint.setter
    def integrations_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ed388c8d0117d21f03dcfd603b2b9c5a66fbb069b4004b6fb6cae8fd4a9d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsCustomEndpoint")
    def kms_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsCustomEndpoint"))

    @kms_custom_endpoint.setter
    def kms_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee93361c464a963f37a9cdd87ad737b9bd5b749e4d1e708d57037c74cb190cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingCustomEndpoint")
    def logging_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingCustomEndpoint"))

    @logging_custom_endpoint.setter
    def logging_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc5cded5e87200af16b787f4673609997b55d3f44d341ac5a7c9f665dc8f828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lookerCustomEndpoint")
    def looker_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lookerCustomEndpoint"))

    @looker_custom_endpoint.setter
    def looker_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d2a33c841fab9d8bc06e2b9e2c2a253a32c61215de152451ee0aed447cb6d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lustreCustomEndpoint")
    def lustre_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lustreCustomEndpoint"))

    @lustre_custom_endpoint.setter
    def lustre_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d344f29e05f432b2310e2688e905b206cf1fa707287931cd9478bcc28fb5720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lustreCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedKafkaCustomEndpoint")
    def managed_kafka_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedKafkaCustomEndpoint"))

    @managed_kafka_custom_endpoint.setter
    def managed_kafka_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffcb605ec19a68cfd58da0cadc51f700cb7fcbc12b57c013ba3174e3e9b8c51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedKafkaCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memcacheCustomEndpoint")
    def memcache_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memcacheCustomEndpoint"))

    @memcache_custom_endpoint.setter
    def memcache_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e984b21a5ea66b82291a11675ff78c2bc1a7da7b4665b6a42f696d5b6ffc4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memcacheCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorystoreCustomEndpoint")
    def memorystore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memorystoreCustomEndpoint"))

    @memorystore_custom_endpoint.setter
    def memorystore_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3859959af1500e4aa158c9a41aded706a34980d32e90a6ce1b4ca8d75d750e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorystoreCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="migrationCenterCustomEndpoint")
    def migration_center_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "migrationCenterCustomEndpoint"))

    @migration_center_custom_endpoint.setter
    def migration_center_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9403e199a59b7e8ee9ff75e2a1c75b127c2a21d222740f3707011c81b80c755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "migrationCenterCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mlEngineCustomEndpoint")
    def ml_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mlEngineCustomEndpoint"))

    @ml_engine_custom_endpoint.setter
    def ml_engine_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8448496713fe8128a39ef3d6f429d4127aa6dad679d4ba74a60eaf05be5d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mlEngineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitoringCustomEndpoint")
    def monitoring_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitoringCustomEndpoint"))

    @monitoring_custom_endpoint.setter
    def monitoring_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b255fd005429e016ff919756701a95909c8ee9d08b94b882d15d42b42283e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoringCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netappCustomEndpoint")
    def netapp_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netappCustomEndpoint"))

    @netapp_custom_endpoint.setter
    def netapp_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c28c9e9ba68afddb6addc818073186c254b7a0f0da193de01a56f5d3ea7faa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netappCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkConnectivityCustomEndpoint")
    def network_connectivity_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkConnectivityCustomEndpoint"))

    @network_connectivity_custom_endpoint.setter
    def network_connectivity_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de47f9bed38abb9857acc1e96638144a74278ba6118111105dc93583fd4a52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConnectivityCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkManagementCustomEndpoint")
    def network_management_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkManagementCustomEndpoint"))

    @network_management_custom_endpoint.setter
    def network_management_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823b5f1f7247f7d28eaeecb4521e3527e5870c0bdc2c3aed2b8adfcce9b2fde6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkManagementCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkSecurityCustomEndpoint")
    def network_security_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkSecurityCustomEndpoint"))

    @network_security_custom_endpoint.setter
    def network_security_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d2b3b847a28032b27f16ccc9c0a21701fcc7c638f1fa03579a0160afbb1eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkSecurityCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkServicesCustomEndpoint")
    def network_services_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkServicesCustomEndpoint"))

    @network_services_custom_endpoint.setter
    def network_services_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a66c909ce893e25eafb470fd8d62a42844ebb278487880f25724d8adab916a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkServicesCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebooksCustomEndpoint")
    def notebooks_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebooksCustomEndpoint"))

    @notebooks_custom_endpoint.setter
    def notebooks_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70fecaf83f6ed1b664c993936be11418276188c26e45aeb326ff33ea49c23bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebooksCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oracleDatabaseCustomEndpoint")
    def oracle_database_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oracleDatabaseCustomEndpoint"))

    @oracle_database_custom_endpoint.setter
    def oracle_database_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8676c31fe795b16a2f10fc8954ad5c5bbb64158914c6af01a06712f5c43ee557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oracleDatabaseCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgPolicyCustomEndpoint")
    def org_policy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgPolicyCustomEndpoint"))

    @org_policy_custom_endpoint.setter
    def org_policy_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ceb6f6a579175ad8f20d614cb5a4b870f003b390eefc31d1a806e5126537cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgPolicyCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osConfigCustomEndpoint")
    def os_config_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osConfigCustomEndpoint"))

    @os_config_custom_endpoint.setter
    def os_config_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48976ef46d76eaefc8446cb8c3bad2786e89fa98a67afd69a682cbf0a3c31d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osConfigCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osConfigV2CustomEndpoint")
    def os_config_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osConfigV2CustomEndpoint"))

    @os_config_v2_custom_endpoint.setter
    def os_config_v2_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7743975c2b631af5789e25de57ade2faec5d2ddbb1cf02e79266749b42a458b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osConfigV2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osLoginCustomEndpoint")
    def os_login_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osLoginCustomEndpoint"))

    @os_login_custom_endpoint.setter
    def os_login_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3377f27f22de9c684a2207bce376bc4a3a77d594840566aece605617f9a8c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osLoginCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelstoreCustomEndpoint")
    def parallelstore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parallelstoreCustomEndpoint"))

    @parallelstore_custom_endpoint.setter
    def parallelstore_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90cf79df198f374b1c76da9b24feea72873f604a88e2b2491fa712041d770b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelstoreCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameterManagerCustomEndpoint")
    def parameter_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterManagerCustomEndpoint"))

    @parameter_manager_custom_endpoint.setter
    def parameter_manager_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ccc084c23d9bb77fc7b958db07de00f434fbf2b709b625a19a231b03b9d403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameterManagerRegionalCustomEndpoint")
    def parameter_manager_regional_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterManagerRegionalCustomEndpoint"))

    @parameter_manager_regional_custom_endpoint.setter
    def parameter_manager_regional_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d94229fe704baa7048f9ec79bea58ebe7555c1703a4cef0cfc730c0fda6ae84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterManagerRegionalCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privatecaCustomEndpoint")
    def privateca_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privatecaCustomEndpoint"))

    @privateca_custom_endpoint.setter
    def privateca_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee90dbc1b564cda0c55046efa24e318ffd04d12fddbe4b3cdad7b59b10027ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privatecaCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privilegedAccessManagerCustomEndpoint")
    def privileged_access_manager_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privilegedAccessManagerCustomEndpoint"))

    @privileged_access_manager_custom_endpoint.setter
    def privileged_access_manager_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab355394dea00a911ce2800dd38ed94a4599bcb15776c9120373be0c7b7f648c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privilegedAccessManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "project"))

    @project.setter
    def project(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b334230c30ac4befac0d3bc79dbf82960acd331bcf230c3c2b9702d71e9c407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicCaCustomEndpoint")
    def public_ca_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicCaCustomEndpoint"))

    @public_ca_custom_endpoint.setter
    def public_ca_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874597822d8c4e0a8dd18a417057332a575df04dda52f21a4d0fcd5e49c0f52c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicCaCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubCustomEndpoint")
    def pubsub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubCustomEndpoint"))

    @pubsub_custom_endpoint.setter
    def pubsub_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d35ae613dd14fc26ad932d9ae1c67074f2969f8525bb137e044fd748a9ed7df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubLiteCustomEndpoint")
    def pubsub_lite_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubLiteCustomEndpoint"))

    @pubsub_lite_custom_endpoint.setter
    def pubsub_lite_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78115d57ff065a810f35d72a2f1a765096a020dd518fae113fe34350d4c1df95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubLiteCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recaptchaEnterpriseCustomEndpoint")
    def recaptcha_enterprise_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recaptchaEnterpriseCustomEndpoint"))

    @recaptcha_enterprise_custom_endpoint.setter
    def recaptcha_enterprise_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220fc6edded0619e1e29d10866b002acd584deffe3edb29df8fac20d95ccbc5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recaptchaEnterpriseCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redisCustomEndpoint")
    def redis_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisCustomEndpoint"))

    @redis_custom_endpoint.setter
    def redis_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22979f69f872ef3fd8012b2d7311a92845dbdbf378ab73cd6688997ba83d4ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @region.setter
    def region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5656bfa8c680416ec6c8713075287a57c3e637737e432e6dc9222c46f0bb979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestReason")
    def request_reason(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestReason"))

    @request_reason.setter
    def request_reason(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa5847dc7e5a17fe5cd23545194315bb3db887ef43de22793c81a042ba05ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestTimeout")
    def request_timeout(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestTimeout"))

    @request_timeout.setter
    def request_timeout(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77ccc2a0cbf0c3f3d1df1da50f2e9839ae27b596f3c8c33246c833d706b01b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceManager3CustomEndpoint")
    def resource_manager3_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceManager3CustomEndpoint"))

    @resource_manager3_custom_endpoint.setter
    def resource_manager3_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b328e661fd71d34b2ee41f34edb7a22393c45d5cd3e6a016b10e8ab4ac3f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManager3CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceManagerCustomEndpoint")
    def resource_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceManagerCustomEndpoint"))

    @resource_manager_custom_endpoint.setter
    def resource_manager_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f95457ec2068c65c8e03df6aa22969d51170ff1430f2a27eda22a3f2ee07a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceManagerV3CustomEndpoint")
    def resource_manager_v3_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceManagerV3CustomEndpoint"))

    @resource_manager_v3_custom_endpoint.setter
    def resource_manager_v3_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72766b6852d67462c0f10240e60ad39737654eac6f9854f5e73cc2907620d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerV3CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeconfigCustomEndpoint")
    def runtimeconfig_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeconfigCustomEndpoint"))

    @runtimeconfig_custom_endpoint.setter
    def runtimeconfig_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d39a6c90d1382a85ab1bf4d9b615953c989437d10737dd581ac966a9cd462d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeconfigCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeConfigCustomEndpoint")
    def runtime_config_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeConfigCustomEndpoint"))

    @runtime_config_custom_endpoint.setter
    def runtime_config_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b692e627d68fbaeccb3aaf1f990c5adfca5c456293c06c56dc7b994220630b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeConfigCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f06b9d949684d96e3dc29a629a2fc0392c56e9199be04ae55a6bd3cd2eec64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerCustomEndpoint")
    def secret_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerCustomEndpoint"))

    @secret_manager_custom_endpoint.setter
    def secret_manager_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f42f7fb66a5f120818b1ec0074aa4ba4c9eb826d0a8b1c20f1bc96d55c5954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerRegionalCustomEndpoint")
    def secret_manager_regional_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerRegionalCustomEndpoint"))

    @secret_manager_regional_custom_endpoint.setter
    def secret_manager_regional_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d3b47d3918595d7250bd296be8640f1e8ab1e6e34b45cdb345d8250e249f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerRegionalCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secureSourceManagerCustomEndpoint")
    def secure_source_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secureSourceManagerCustomEndpoint"))

    @secure_source_manager_custom_endpoint.setter
    def secure_source_manager_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4bfde948d0c95558d502c922539cc931ff52ee9a77091bbc00694de80e068dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secureSourceManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityCenterCustomEndpoint")
    def security_center_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityCenterCustomEndpoint"))

    @security_center_custom_endpoint.setter
    def security_center_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f3ca0658d64f05cd29e8723d023814736f299cbf0463581232fcb789d4040b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityCenterCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityCenterManagementCustomEndpoint")
    def security_center_management_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityCenterManagementCustomEndpoint"))

    @security_center_management_custom_endpoint.setter
    def security_center_management_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652a124bea66968f564f7f12d970b577c1815a32d2033a416b40be0abd471bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityCenterManagementCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityCenterV2CustomEndpoint")
    def security_center_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityCenterV2CustomEndpoint"))

    @security_center_v2_custom_endpoint.setter
    def security_center_v2_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c2332d7ca2a5fc76f4f04ae3d24c23c4825ed5e9082e80ef3175c596b30161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityCenterV2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securitypostureCustomEndpoint")
    def securityposture_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securitypostureCustomEndpoint"))

    @securityposture_custom_endpoint.setter
    def securityposture_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5747ab24111cecc22440ecf90703e759694a07f8c6f5b8c26e78b4cbcca2fff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securitypostureCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityScannerCustomEndpoint")
    def security_scanner_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityScannerCustomEndpoint"))

    @security_scanner_custom_endpoint.setter
    def security_scanner_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83963070cf816c0423d08c1328940cd66194549ec5c3b0edd3de8da1e9a4a2c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityScannerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryCustomEndpoint")
    def service_directory_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceDirectoryCustomEndpoint"))

    @service_directory_custom_endpoint.setter
    def service_directory_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303feb20a504b2ae74d8a4ea27af5792bfd6305de510a98afef0ebe3dff49717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceDirectoryCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceManagementCustomEndpoint")
    def service_management_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceManagementCustomEndpoint"))

    @service_management_custom_endpoint.setter
    def service_management_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882e3fd626de4f7336d4e267de9450eb2b77d1ee956d0b74cc21c4f3fd45baf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceManagementCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkingCustomEndpoint")
    def service_networking_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNetworkingCustomEndpoint"))

    @service_networking_custom_endpoint.setter
    def service_networking_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ea784a23839f4e86ef3696dacef0d47c8971b746dc637cb1872195a6a6c0b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceNetworkingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceUsageCustomEndpoint")
    def service_usage_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceUsageCustomEndpoint"))

    @service_usage_custom_endpoint.setter
    def service_usage_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac207e9bbddfd545f61fab059e350c3a9f3c8f39ca9eda14994317e9af46749f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceUsageCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="siteVerificationCustomEndpoint")
    def site_verification_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteVerificationCustomEndpoint"))

    @site_verification_custom_endpoint.setter
    def site_verification_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f375707cf3dbd9c95b62a66777e045f03043ed75f80e3c245ae03bb27ce676f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteVerificationCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRepoCustomEndpoint")
    def source_repo_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRepoCustomEndpoint"))

    @source_repo_custom_endpoint.setter
    def source_repo_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3398fa4c6e6fe464fd5263786d2b898c6923760fb5ea42d4c01639247a3938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRepoCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spannerCustomEndpoint")
    def spanner_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spannerCustomEndpoint"))

    @spanner_custom_endpoint.setter
    def spanner_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7e9a387bf7818c118bfa8c3c014273fa47053af35b5485792c3ed4831c9d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spannerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlCustomEndpoint")
    def sql_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlCustomEndpoint"))

    @sql_custom_endpoint.setter
    def sql_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccd63d441134893f54f211021b17f1e92571fe3f72a5c90108cee2046d4d3ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageBatchOperationsCustomEndpoint")
    def storage_batch_operations_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageBatchOperationsCustomEndpoint"))

    @storage_batch_operations_custom_endpoint.setter
    def storage_batch_operations_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59de503556316a3ca64baba8587e021d747e0f5b43f661a0347f59ecb1908d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageBatchOperationsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageControlCustomEndpoint")
    def storage_control_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageControlCustomEndpoint"))

    @storage_control_custom_endpoint.setter
    def storage_control_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada3fb034878a8679fda6dd9e593d31618f5ebe594785dcd247aa8eaf2d78645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageControlCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageCustomEndpoint")
    def storage_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageCustomEndpoint"))

    @storage_custom_endpoint.setter
    def storage_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d4fb1ec219b71accd2cc2a764fed5bfd02cce21c134985b4fd24868cd71504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageInsightsCustomEndpoint")
    def storage_insights_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageInsightsCustomEndpoint"))

    @storage_insights_custom_endpoint.setter
    def storage_insights_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f6bcfe20b7ef31aa902ecc563c998182d11ed7dbb60a97eac286afe83a43c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageInsightsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageTransferCustomEndpoint")
    def storage_transfer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageTransferCustomEndpoint"))

    @storage_transfer_custom_endpoint.setter
    def storage_transfer_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a93bae96dd736c3e267dc9906134bc87ff9aae22f6e03dbae592493b5d74f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageTransferCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsCustomEndpoint")
    def tags_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagsCustomEndpoint"))

    @tags_custom_endpoint.setter
    def tags_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1514eeaa8dc1ec783e5f6b7ebd57ee508d494172ace1d89c9b7f89c75e7f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsLocationCustomEndpoint")
    def tags_location_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagsLocationCustomEndpoint"))

    @tags_location_custom_endpoint.setter
    def tags_location_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d8e65c04f5d3a3478be640d1792a2376e5aad4c7f821baff338337ab8a1391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsLocationCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformAttributionLabelAdditionStrategy")
    def terraform_attribution_label_addition_strategy(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformAttributionLabelAdditionStrategy"))

    @terraform_attribution_label_addition_strategy.setter
    def terraform_attribution_label_addition_strategy(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a2f23d31c7b9451edef4a206a49656d22da08d1f015ec89ea004aa13e4fdcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttributionLabelAdditionStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tpuCustomEndpoint")
    def tpu_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpuCustomEndpoint"))

    @tpu_custom_endpoint.setter
    def tpu_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c842aede83001afeec71bd444e796b2566d761862872837f56f33b11bd98738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpuCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tpuV2CustomEndpoint")
    def tpu_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpuV2CustomEndpoint"))

    @tpu_v2_custom_endpoint.setter
    def tpu_v2_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d247ccbd9491e52988522264f6fcdbbee22d9593c7cb1721870e3ef8a9cddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpuV2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transcoderCustomEndpoint")
    def transcoder_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transcoderCustomEndpoint"))

    @transcoder_custom_endpoint.setter
    def transcoder_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ce0a9288408970f20561dc13833c63464947b18b210f1ece263604218c641b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transcoderCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="universeDomain")
    def universe_domain(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "universeDomain"))

    @universe_domain.setter
    def universe_domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239b5b453ec987bfd51773776fdbe35524d94410a888bfddb0d982610e8fd371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "universeDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userProjectOverride")
    def user_project_override(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userProjectOverride"))

    @user_project_override.setter
    def user_project_override(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23917ccd6c2d6e2a8db5f7d71fad4bebe11f77fca71623a4fb270c56908fe97d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userProjectOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vertexAiCustomEndpoint")
    def vertex_ai_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vertexAiCustomEndpoint"))

    @vertex_ai_custom_endpoint.setter
    def vertex_ai_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3163d7f484f936d6a7f275f62e778d20e0a91533a9e3533b7a3e225bcb09c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vertexAiCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmwareengineCustomEndpoint")
    def vmwareengine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmwareengineCustomEndpoint"))

    @vmwareengine_custom_endpoint.setter
    def vmwareengine_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5a1ab2f5a12bd704ecdb36629bdaec68b5a3ff60961590a1396d0406ffb2c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmwareengineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcAccessCustomEndpoint")
    def vpc_access_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcAccessCustomEndpoint"))

    @vpc_access_custom_endpoint.setter
    def vpc_access_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6940e4bff6e9e8667cf2a4feb08ad070232db20d09ac892aedb750f07425d75a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcAccessCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workbenchCustomEndpoint")
    def workbench_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workbenchCustomEndpoint"))

    @workbench_custom_endpoint.setter
    def workbench_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdedc88d0e55b82d0d0a9735fb84b61b86a05db71fc1cca08a91cbdbf34d5463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workbenchCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflowsCustomEndpoint")
    def workflows_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowsCustomEndpoint"))

    @workflows_custom_endpoint.setter
    def workflows_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8263ee3354fc1599c11af3e1847de81bf4d0a754c9a52d739383294224858e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflowsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workstationsCustomEndpoint")
    def workstations_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workstationsCustomEndpoint"))

    @workstations_custom_endpoint.setter
    def workstations_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0a272deed4287035bbaf36aa494e4409e2ca6627f5de4aa58cd84158148328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workstationsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4a318fadbee5551187cdb78b3cf3e8ee27cbe311ccecdeabf64b86641c8024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.provider.GoogleBetaProviderBatching",
    jsii_struct_bases=[],
    name_mapping={"enable_batching": "enableBatching", "send_after": "sendAfter"},
)
class GoogleBetaProviderBatching:
    def __init__(
        self,
        *,
        enable_batching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_after: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_batching: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#enable_batching GoogleBetaProvider#enable_batching}.
        :param send_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#send_after GoogleBetaProvider#send_after}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbf2bb8f37e1971fc512e090f309f883c17935d206ab19907c44b1932a0f917)
            check_type(argname="argument enable_batching", value=enable_batching, expected_type=type_hints["enable_batching"])
            check_type(argname="argument send_after", value=send_after, expected_type=type_hints["send_after"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_batching is not None:
            self._values["enable_batching"] = enable_batching
        if send_after is not None:
            self._values["send_after"] = send_after

    @builtins.property
    def enable_batching(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#enable_batching GoogleBetaProvider#enable_batching}.'''
        result = self._values.get("enable_batching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_after(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#send_after GoogleBetaProvider#send_after}.'''
        result = self._values.get("send_after")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBetaProviderBatching(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.provider.GoogleBetaProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_approval_custom_endpoint": "accessApprovalCustomEndpoint",
        "access_context_manager_custom_endpoint": "accessContextManagerCustomEndpoint",
        "access_token": "accessToken",
        "active_directory_custom_endpoint": "activeDirectoryCustomEndpoint",
        "add_terraform_attribution_label": "addTerraformAttributionLabel",
        "alias": "alias",
        "alloydb_custom_endpoint": "alloydbCustomEndpoint",
        "api_gateway_custom_endpoint": "apiGatewayCustomEndpoint",
        "apigee_custom_endpoint": "apigeeCustomEndpoint",
        "apihub_custom_endpoint": "apihubCustomEndpoint",
        "apikeys_custom_endpoint": "apikeysCustomEndpoint",
        "app_engine_custom_endpoint": "appEngineCustomEndpoint",
        "apphub_custom_endpoint": "apphubCustomEndpoint",
        "artifact_registry_custom_endpoint": "artifactRegistryCustomEndpoint",
        "assured_workloads_custom_endpoint": "assuredWorkloadsCustomEndpoint",
        "backup_dr_custom_endpoint": "backupDrCustomEndpoint",
        "batching": "batching",
        "beyondcorp_custom_endpoint": "beyondcorpCustomEndpoint",
        "biglake_custom_endpoint": "biglakeCustomEndpoint",
        "bigquery_analytics_hub_custom_endpoint": "bigqueryAnalyticsHubCustomEndpoint",
        "bigquery_connection_custom_endpoint": "bigqueryConnectionCustomEndpoint",
        "big_query_custom_endpoint": "bigQueryCustomEndpoint",
        "bigquery_datapolicy_custom_endpoint": "bigqueryDatapolicyCustomEndpoint",
        "bigquery_data_transfer_custom_endpoint": "bigqueryDataTransferCustomEndpoint",
        "bigquery_reservation_custom_endpoint": "bigqueryReservationCustomEndpoint",
        "bigtable_custom_endpoint": "bigtableCustomEndpoint",
        "billing_custom_endpoint": "billingCustomEndpoint",
        "billing_project": "billingProject",
        "binary_authorization_custom_endpoint": "binaryAuthorizationCustomEndpoint",
        "blockchain_node_engine_custom_endpoint": "blockchainNodeEngineCustomEndpoint",
        "certificate_manager_custom_endpoint": "certificateManagerCustomEndpoint",
        "chronicle_custom_endpoint": "chronicleCustomEndpoint",
        "cloud_asset_custom_endpoint": "cloudAssetCustomEndpoint",
        "cloud_billing_custom_endpoint": "cloudBillingCustomEndpoint",
        "cloud_build_custom_endpoint": "cloudBuildCustomEndpoint",
        "cloudbuildv2_custom_endpoint": "cloudbuildv2CustomEndpoint",
        "cloud_build_worker_pool_custom_endpoint": "cloudBuildWorkerPoolCustomEndpoint",
        "clouddeploy_custom_endpoint": "clouddeployCustomEndpoint",
        "clouddomains_custom_endpoint": "clouddomainsCustomEndpoint",
        "cloudfunctions2_custom_endpoint": "cloudfunctions2CustomEndpoint",
        "cloud_functions_custom_endpoint": "cloudFunctionsCustomEndpoint",
        "cloud_identity_custom_endpoint": "cloudIdentityCustomEndpoint",
        "cloud_ids_custom_endpoint": "cloudIdsCustomEndpoint",
        "cloud_quotas_custom_endpoint": "cloudQuotasCustomEndpoint",
        "cloud_resource_manager_custom_endpoint": "cloudResourceManagerCustomEndpoint",
        "cloud_run_custom_endpoint": "cloudRunCustomEndpoint",
        "cloud_run_v2_custom_endpoint": "cloudRunV2CustomEndpoint",
        "cloud_scheduler_custom_endpoint": "cloudSchedulerCustomEndpoint",
        "cloud_tasks_custom_endpoint": "cloudTasksCustomEndpoint",
        "colab_custom_endpoint": "colabCustomEndpoint",
        "composer_custom_endpoint": "composerCustomEndpoint",
        "compute_custom_endpoint": "computeCustomEndpoint",
        "container_analysis_custom_endpoint": "containerAnalysisCustomEndpoint",
        "container_attached_custom_endpoint": "containerAttachedCustomEndpoint",
        "container_aws_custom_endpoint": "containerAwsCustomEndpoint",
        "container_azure_custom_endpoint": "containerAzureCustomEndpoint",
        "container_custom_endpoint": "containerCustomEndpoint",
        "core_billing_custom_endpoint": "coreBillingCustomEndpoint",
        "credentials": "credentials",
        "database_migration_service_custom_endpoint": "databaseMigrationServiceCustomEndpoint",
        "data_catalog_custom_endpoint": "dataCatalogCustomEndpoint",
        "dataflow_custom_endpoint": "dataflowCustomEndpoint",
        "dataform_custom_endpoint": "dataformCustomEndpoint",
        "data_fusion_custom_endpoint": "dataFusionCustomEndpoint",
        "data_loss_prevention_custom_endpoint": "dataLossPreventionCustomEndpoint",
        "data_pipeline_custom_endpoint": "dataPipelineCustomEndpoint",
        "dataplex_custom_endpoint": "dataplexCustomEndpoint",
        "dataproc_custom_endpoint": "dataprocCustomEndpoint",
        "dataproc_gdc_custom_endpoint": "dataprocGdcCustomEndpoint",
        "dataproc_metastore_custom_endpoint": "dataprocMetastoreCustomEndpoint",
        "datastream_custom_endpoint": "datastreamCustomEndpoint",
        "default_labels": "defaultLabels",
        "deployment_manager_custom_endpoint": "deploymentManagerCustomEndpoint",
        "developer_connect_custom_endpoint": "developerConnectCustomEndpoint",
        "dialogflow_custom_endpoint": "dialogflowCustomEndpoint",
        "dialogflow_cx_custom_endpoint": "dialogflowCxCustomEndpoint",
        "discovery_engine_custom_endpoint": "discoveryEngineCustomEndpoint",
        "dns_custom_endpoint": "dnsCustomEndpoint",
        "document_ai_custom_endpoint": "documentAiCustomEndpoint",
        "document_ai_warehouse_custom_endpoint": "documentAiWarehouseCustomEndpoint",
        "edgecontainer_custom_endpoint": "edgecontainerCustomEndpoint",
        "edgenetwork_custom_endpoint": "edgenetworkCustomEndpoint",
        "essential_contacts_custom_endpoint": "essentialContactsCustomEndpoint",
        "eventarc_custom_endpoint": "eventarcCustomEndpoint",
        "external_credentials": "externalCredentials",
        "filestore_custom_endpoint": "filestoreCustomEndpoint",
        "firebase_app_check_custom_endpoint": "firebaseAppCheckCustomEndpoint",
        "firebase_app_hosting_custom_endpoint": "firebaseAppHostingCustomEndpoint",
        "firebase_custom_endpoint": "firebaseCustomEndpoint",
        "firebase_database_custom_endpoint": "firebaseDatabaseCustomEndpoint",
        "firebase_data_connect_custom_endpoint": "firebaseDataConnectCustomEndpoint",
        "firebase_extensions_custom_endpoint": "firebaseExtensionsCustomEndpoint",
        "firebase_hosting_custom_endpoint": "firebaseHostingCustomEndpoint",
        "firebaserules_custom_endpoint": "firebaserulesCustomEndpoint",
        "firebase_storage_custom_endpoint": "firebaseStorageCustomEndpoint",
        "firestore_custom_endpoint": "firestoreCustomEndpoint",
        "gemini_custom_endpoint": "geminiCustomEndpoint",
        "gke_backup_custom_endpoint": "gkeBackupCustomEndpoint",
        "gke_hub2_custom_endpoint": "gkeHub2CustomEndpoint",
        "gke_hub_custom_endpoint": "gkeHubCustomEndpoint",
        "gkehub_feature_custom_endpoint": "gkehubFeatureCustomEndpoint",
        "gkeonprem_custom_endpoint": "gkeonpremCustomEndpoint",
        "healthcare_custom_endpoint": "healthcareCustomEndpoint",
        "iam2_custom_endpoint": "iam2CustomEndpoint",
        "iam3_custom_endpoint": "iam3CustomEndpoint",
        "iam_beta_custom_endpoint": "iamBetaCustomEndpoint",
        "iam_credentials_custom_endpoint": "iamCredentialsCustomEndpoint",
        "iam_custom_endpoint": "iamCustomEndpoint",
        "iam_workforce_pool_custom_endpoint": "iamWorkforcePoolCustomEndpoint",
        "iap_custom_endpoint": "iapCustomEndpoint",
        "identity_platform_custom_endpoint": "identityPlatformCustomEndpoint",
        "impersonate_service_account": "impersonateServiceAccount",
        "impersonate_service_account_delegates": "impersonateServiceAccountDelegates",
        "integration_connectors_custom_endpoint": "integrationConnectorsCustomEndpoint",
        "integrations_custom_endpoint": "integrationsCustomEndpoint",
        "kms_custom_endpoint": "kmsCustomEndpoint",
        "logging_custom_endpoint": "loggingCustomEndpoint",
        "looker_custom_endpoint": "lookerCustomEndpoint",
        "lustre_custom_endpoint": "lustreCustomEndpoint",
        "managed_kafka_custom_endpoint": "managedKafkaCustomEndpoint",
        "memcache_custom_endpoint": "memcacheCustomEndpoint",
        "memorystore_custom_endpoint": "memorystoreCustomEndpoint",
        "migration_center_custom_endpoint": "migrationCenterCustomEndpoint",
        "ml_engine_custom_endpoint": "mlEngineCustomEndpoint",
        "monitoring_custom_endpoint": "monitoringCustomEndpoint",
        "netapp_custom_endpoint": "netappCustomEndpoint",
        "network_connectivity_custom_endpoint": "networkConnectivityCustomEndpoint",
        "network_management_custom_endpoint": "networkManagementCustomEndpoint",
        "network_security_custom_endpoint": "networkSecurityCustomEndpoint",
        "network_services_custom_endpoint": "networkServicesCustomEndpoint",
        "notebooks_custom_endpoint": "notebooksCustomEndpoint",
        "oracle_database_custom_endpoint": "oracleDatabaseCustomEndpoint",
        "org_policy_custom_endpoint": "orgPolicyCustomEndpoint",
        "os_config_custom_endpoint": "osConfigCustomEndpoint",
        "os_config_v2_custom_endpoint": "osConfigV2CustomEndpoint",
        "os_login_custom_endpoint": "osLoginCustomEndpoint",
        "parallelstore_custom_endpoint": "parallelstoreCustomEndpoint",
        "parameter_manager_custom_endpoint": "parameterManagerCustomEndpoint",
        "parameter_manager_regional_custom_endpoint": "parameterManagerRegionalCustomEndpoint",
        "privateca_custom_endpoint": "privatecaCustomEndpoint",
        "privileged_access_manager_custom_endpoint": "privilegedAccessManagerCustomEndpoint",
        "project": "project",
        "public_ca_custom_endpoint": "publicCaCustomEndpoint",
        "pubsub_custom_endpoint": "pubsubCustomEndpoint",
        "pubsub_lite_custom_endpoint": "pubsubLiteCustomEndpoint",
        "recaptcha_enterprise_custom_endpoint": "recaptchaEnterpriseCustomEndpoint",
        "redis_custom_endpoint": "redisCustomEndpoint",
        "region": "region",
        "request_reason": "requestReason",
        "request_timeout": "requestTimeout",
        "resource_manager3_custom_endpoint": "resourceManager3CustomEndpoint",
        "resource_manager_custom_endpoint": "resourceManagerCustomEndpoint",
        "resource_manager_v3_custom_endpoint": "resourceManagerV3CustomEndpoint",
        "runtimeconfig_custom_endpoint": "runtimeconfigCustomEndpoint",
        "runtime_config_custom_endpoint": "runtimeConfigCustomEndpoint",
        "scopes": "scopes",
        "secret_manager_custom_endpoint": "secretManagerCustomEndpoint",
        "secret_manager_regional_custom_endpoint": "secretManagerRegionalCustomEndpoint",
        "secure_source_manager_custom_endpoint": "secureSourceManagerCustomEndpoint",
        "security_center_custom_endpoint": "securityCenterCustomEndpoint",
        "security_center_management_custom_endpoint": "securityCenterManagementCustomEndpoint",
        "security_center_v2_custom_endpoint": "securityCenterV2CustomEndpoint",
        "securityposture_custom_endpoint": "securitypostureCustomEndpoint",
        "security_scanner_custom_endpoint": "securityScannerCustomEndpoint",
        "service_directory_custom_endpoint": "serviceDirectoryCustomEndpoint",
        "service_management_custom_endpoint": "serviceManagementCustomEndpoint",
        "service_networking_custom_endpoint": "serviceNetworkingCustomEndpoint",
        "service_usage_custom_endpoint": "serviceUsageCustomEndpoint",
        "site_verification_custom_endpoint": "siteVerificationCustomEndpoint",
        "source_repo_custom_endpoint": "sourceRepoCustomEndpoint",
        "spanner_custom_endpoint": "spannerCustomEndpoint",
        "sql_custom_endpoint": "sqlCustomEndpoint",
        "storage_batch_operations_custom_endpoint": "storageBatchOperationsCustomEndpoint",
        "storage_control_custom_endpoint": "storageControlCustomEndpoint",
        "storage_custom_endpoint": "storageCustomEndpoint",
        "storage_insights_custom_endpoint": "storageInsightsCustomEndpoint",
        "storage_transfer_custom_endpoint": "storageTransferCustomEndpoint",
        "tags_custom_endpoint": "tagsCustomEndpoint",
        "tags_location_custom_endpoint": "tagsLocationCustomEndpoint",
        "terraform_attribution_label_addition_strategy": "terraformAttributionLabelAdditionStrategy",
        "tpu_custom_endpoint": "tpuCustomEndpoint",
        "tpu_v2_custom_endpoint": "tpuV2CustomEndpoint",
        "transcoder_custom_endpoint": "transcoderCustomEndpoint",
        "universe_domain": "universeDomain",
        "user_project_override": "userProjectOverride",
        "vertex_ai_custom_endpoint": "vertexAiCustomEndpoint",
        "vmwareengine_custom_endpoint": "vmwareengineCustomEndpoint",
        "vpc_access_custom_endpoint": "vpcAccessCustomEndpoint",
        "workbench_custom_endpoint": "workbenchCustomEndpoint",
        "workflows_custom_endpoint": "workflowsCustomEndpoint",
        "workstations_custom_endpoint": "workstationsCustomEndpoint",
        "zone": "zone",
    },
)
class GoogleBetaProviderConfig:
    def __init__(
        self,
        *,
        access_approval_custom_endpoint: typing.Optional[builtins.str] = None,
        access_context_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        access_token: typing.Optional[builtins.str] = None,
        active_directory_custom_endpoint: typing.Optional[builtins.str] = None,
        add_terraform_attribution_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        alias: typing.Optional[builtins.str] = None,
        alloydb_custom_endpoint: typing.Optional[builtins.str] = None,
        api_gateway_custom_endpoint: typing.Optional[builtins.str] = None,
        apigee_custom_endpoint: typing.Optional[builtins.str] = None,
        apihub_custom_endpoint: typing.Optional[builtins.str] = None,
        apikeys_custom_endpoint: typing.Optional[builtins.str] = None,
        app_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        apphub_custom_endpoint: typing.Optional[builtins.str] = None,
        artifact_registry_custom_endpoint: typing.Optional[builtins.str] = None,
        assured_workloads_custom_endpoint: typing.Optional[builtins.str] = None,
        backup_dr_custom_endpoint: typing.Optional[builtins.str] = None,
        batching: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBetaProviderBatching, typing.Dict[builtins.str, typing.Any]]]]] = None,
        beyondcorp_custom_endpoint: typing.Optional[builtins.str] = None,
        biglake_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_analytics_hub_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_connection_custom_endpoint: typing.Optional[builtins.str] = None,
        big_query_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_datapolicy_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_data_transfer_custom_endpoint: typing.Optional[builtins.str] = None,
        bigquery_reservation_custom_endpoint: typing.Optional[builtins.str] = None,
        bigtable_custom_endpoint: typing.Optional[builtins.str] = None,
        billing_custom_endpoint: typing.Optional[builtins.str] = None,
        billing_project: typing.Optional[builtins.str] = None,
        binary_authorization_custom_endpoint: typing.Optional[builtins.str] = None,
        blockchain_node_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        certificate_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        chronicle_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_asset_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_billing_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_build_custom_endpoint: typing.Optional[builtins.str] = None,
        cloudbuildv2_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_build_worker_pool_custom_endpoint: typing.Optional[builtins.str] = None,
        clouddeploy_custom_endpoint: typing.Optional[builtins.str] = None,
        clouddomains_custom_endpoint: typing.Optional[builtins.str] = None,
        cloudfunctions2_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_functions_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_identity_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_ids_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_quotas_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_run_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_run_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_scheduler_custom_endpoint: typing.Optional[builtins.str] = None,
        cloud_tasks_custom_endpoint: typing.Optional[builtins.str] = None,
        colab_custom_endpoint: typing.Optional[builtins.str] = None,
        composer_custom_endpoint: typing.Optional[builtins.str] = None,
        compute_custom_endpoint: typing.Optional[builtins.str] = None,
        container_analysis_custom_endpoint: typing.Optional[builtins.str] = None,
        container_attached_custom_endpoint: typing.Optional[builtins.str] = None,
        container_aws_custom_endpoint: typing.Optional[builtins.str] = None,
        container_azure_custom_endpoint: typing.Optional[builtins.str] = None,
        container_custom_endpoint: typing.Optional[builtins.str] = None,
        core_billing_custom_endpoint: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[builtins.str] = None,
        database_migration_service_custom_endpoint: typing.Optional[builtins.str] = None,
        data_catalog_custom_endpoint: typing.Optional[builtins.str] = None,
        dataflow_custom_endpoint: typing.Optional[builtins.str] = None,
        dataform_custom_endpoint: typing.Optional[builtins.str] = None,
        data_fusion_custom_endpoint: typing.Optional[builtins.str] = None,
        data_loss_prevention_custom_endpoint: typing.Optional[builtins.str] = None,
        data_pipeline_custom_endpoint: typing.Optional[builtins.str] = None,
        dataplex_custom_endpoint: typing.Optional[builtins.str] = None,
        dataproc_custom_endpoint: typing.Optional[builtins.str] = None,
        dataproc_gdc_custom_endpoint: typing.Optional[builtins.str] = None,
        dataproc_metastore_custom_endpoint: typing.Optional[builtins.str] = None,
        datastream_custom_endpoint: typing.Optional[builtins.str] = None,
        default_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        deployment_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        developer_connect_custom_endpoint: typing.Optional[builtins.str] = None,
        dialogflow_custom_endpoint: typing.Optional[builtins.str] = None,
        dialogflow_cx_custom_endpoint: typing.Optional[builtins.str] = None,
        discovery_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        dns_custom_endpoint: typing.Optional[builtins.str] = None,
        document_ai_custom_endpoint: typing.Optional[builtins.str] = None,
        document_ai_warehouse_custom_endpoint: typing.Optional[builtins.str] = None,
        edgecontainer_custom_endpoint: typing.Optional[builtins.str] = None,
        edgenetwork_custom_endpoint: typing.Optional[builtins.str] = None,
        essential_contacts_custom_endpoint: typing.Optional[builtins.str] = None,
        eventarc_custom_endpoint: typing.Optional[builtins.str] = None,
        external_credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBetaProviderExternalCredentials", typing.Dict[builtins.str, typing.Any]]]]] = None,
        filestore_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_app_check_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_app_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_database_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_data_connect_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_extensions_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
        firebaserules_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_storage_custom_endpoint: typing.Optional[builtins.str] = None,
        firestore_custom_endpoint: typing.Optional[builtins.str] = None,
        gemini_custom_endpoint: typing.Optional[builtins.str] = None,
        gke_backup_custom_endpoint: typing.Optional[builtins.str] = None,
        gke_hub2_custom_endpoint: typing.Optional[builtins.str] = None,
        gke_hub_custom_endpoint: typing.Optional[builtins.str] = None,
        gkehub_feature_custom_endpoint: typing.Optional[builtins.str] = None,
        gkeonprem_custom_endpoint: typing.Optional[builtins.str] = None,
        healthcare_custom_endpoint: typing.Optional[builtins.str] = None,
        iam2_custom_endpoint: typing.Optional[builtins.str] = None,
        iam3_custom_endpoint: typing.Optional[builtins.str] = None,
        iam_beta_custom_endpoint: typing.Optional[builtins.str] = None,
        iam_credentials_custom_endpoint: typing.Optional[builtins.str] = None,
        iam_custom_endpoint: typing.Optional[builtins.str] = None,
        iam_workforce_pool_custom_endpoint: typing.Optional[builtins.str] = None,
        iap_custom_endpoint: typing.Optional[builtins.str] = None,
        identity_platform_custom_endpoint: typing.Optional[builtins.str] = None,
        impersonate_service_account: typing.Optional[builtins.str] = None,
        impersonate_service_account_delegates: typing.Optional[typing.Sequence[builtins.str]] = None,
        integration_connectors_custom_endpoint: typing.Optional[builtins.str] = None,
        integrations_custom_endpoint: typing.Optional[builtins.str] = None,
        kms_custom_endpoint: typing.Optional[builtins.str] = None,
        logging_custom_endpoint: typing.Optional[builtins.str] = None,
        looker_custom_endpoint: typing.Optional[builtins.str] = None,
        lustre_custom_endpoint: typing.Optional[builtins.str] = None,
        managed_kafka_custom_endpoint: typing.Optional[builtins.str] = None,
        memcache_custom_endpoint: typing.Optional[builtins.str] = None,
        memorystore_custom_endpoint: typing.Optional[builtins.str] = None,
        migration_center_custom_endpoint: typing.Optional[builtins.str] = None,
        ml_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        monitoring_custom_endpoint: typing.Optional[builtins.str] = None,
        netapp_custom_endpoint: typing.Optional[builtins.str] = None,
        network_connectivity_custom_endpoint: typing.Optional[builtins.str] = None,
        network_management_custom_endpoint: typing.Optional[builtins.str] = None,
        network_security_custom_endpoint: typing.Optional[builtins.str] = None,
        network_services_custom_endpoint: typing.Optional[builtins.str] = None,
        notebooks_custom_endpoint: typing.Optional[builtins.str] = None,
        oracle_database_custom_endpoint: typing.Optional[builtins.str] = None,
        org_policy_custom_endpoint: typing.Optional[builtins.str] = None,
        os_config_custom_endpoint: typing.Optional[builtins.str] = None,
        os_config_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        os_login_custom_endpoint: typing.Optional[builtins.str] = None,
        parallelstore_custom_endpoint: typing.Optional[builtins.str] = None,
        parameter_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        parameter_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
        privateca_custom_endpoint: typing.Optional[builtins.str] = None,
        privileged_access_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        public_ca_custom_endpoint: typing.Optional[builtins.str] = None,
        pubsub_custom_endpoint: typing.Optional[builtins.str] = None,
        pubsub_lite_custom_endpoint: typing.Optional[builtins.str] = None,
        recaptcha_enterprise_custom_endpoint: typing.Optional[builtins.str] = None,
        redis_custom_endpoint: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        request_reason: typing.Optional[builtins.str] = None,
        request_timeout: typing.Optional[builtins.str] = None,
        resource_manager3_custom_endpoint: typing.Optional[builtins.str] = None,
        resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        resource_manager_v3_custom_endpoint: typing.Optional[builtins.str] = None,
        runtimeconfig_custom_endpoint: typing.Optional[builtins.str] = None,
        runtime_config_custom_endpoint: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        secret_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
        secure_source_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_management_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        securityposture_custom_endpoint: typing.Optional[builtins.str] = None,
        security_scanner_custom_endpoint: typing.Optional[builtins.str] = None,
        service_directory_custom_endpoint: typing.Optional[builtins.str] = None,
        service_management_custom_endpoint: typing.Optional[builtins.str] = None,
        service_networking_custom_endpoint: typing.Optional[builtins.str] = None,
        service_usage_custom_endpoint: typing.Optional[builtins.str] = None,
        site_verification_custom_endpoint: typing.Optional[builtins.str] = None,
        source_repo_custom_endpoint: typing.Optional[builtins.str] = None,
        spanner_custom_endpoint: typing.Optional[builtins.str] = None,
        sql_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_batch_operations_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_control_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_insights_custom_endpoint: typing.Optional[builtins.str] = None,
        storage_transfer_custom_endpoint: typing.Optional[builtins.str] = None,
        tags_custom_endpoint: typing.Optional[builtins.str] = None,
        tags_location_custom_endpoint: typing.Optional[builtins.str] = None,
        terraform_attribution_label_addition_strategy: typing.Optional[builtins.str] = None,
        tpu_custom_endpoint: typing.Optional[builtins.str] = None,
        tpu_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        transcoder_custom_endpoint: typing.Optional[builtins.str] = None,
        universe_domain: typing.Optional[builtins.str] = None,
        user_project_override: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vertex_ai_custom_endpoint: typing.Optional[builtins.str] = None,
        vmwareengine_custom_endpoint: typing.Optional[builtins.str] = None,
        vpc_access_custom_endpoint: typing.Optional[builtins.str] = None,
        workbench_custom_endpoint: typing.Optional[builtins.str] = None,
        workflows_custom_endpoint: typing.Optional[builtins.str] = None,
        workstations_custom_endpoint: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_approval_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#access_approval_custom_endpoint GoogleBetaProvider#access_approval_custom_endpoint}.
        :param access_context_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#access_context_manager_custom_endpoint GoogleBetaProvider#access_context_manager_custom_endpoint}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#access_token GoogleBetaProvider#access_token}.
        :param active_directory_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#active_directory_custom_endpoint GoogleBetaProvider#active_directory_custom_endpoint}.
        :param add_terraform_attribution_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#add_terraform_attribution_label GoogleBetaProvider#add_terraform_attribution_label}.
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#alias GoogleBetaProvider#alias}
        :param alloydb_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#alloydb_custom_endpoint GoogleBetaProvider#alloydb_custom_endpoint}.
        :param api_gateway_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#api_gateway_custom_endpoint GoogleBetaProvider#api_gateway_custom_endpoint}.
        :param apigee_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apigee_custom_endpoint GoogleBetaProvider#apigee_custom_endpoint}.
        :param apihub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apihub_custom_endpoint GoogleBetaProvider#apihub_custom_endpoint}.
        :param apikeys_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apikeys_custom_endpoint GoogleBetaProvider#apikeys_custom_endpoint}.
        :param app_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#app_engine_custom_endpoint GoogleBetaProvider#app_engine_custom_endpoint}.
        :param apphub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apphub_custom_endpoint GoogleBetaProvider#apphub_custom_endpoint}.
        :param artifact_registry_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#artifact_registry_custom_endpoint GoogleBetaProvider#artifact_registry_custom_endpoint}.
        :param assured_workloads_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#assured_workloads_custom_endpoint GoogleBetaProvider#assured_workloads_custom_endpoint}.
        :param backup_dr_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#backup_dr_custom_endpoint GoogleBetaProvider#backup_dr_custom_endpoint}.
        :param batching: batching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#batching GoogleBetaProvider#batching}
        :param beyondcorp_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#beyondcorp_custom_endpoint GoogleBetaProvider#beyondcorp_custom_endpoint}.
        :param biglake_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#biglake_custom_endpoint GoogleBetaProvider#biglake_custom_endpoint}.
        :param bigquery_analytics_hub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_analytics_hub_custom_endpoint GoogleBetaProvider#bigquery_analytics_hub_custom_endpoint}.
        :param bigquery_connection_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_connection_custom_endpoint GoogleBetaProvider#bigquery_connection_custom_endpoint}.
        :param big_query_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#big_query_custom_endpoint GoogleBetaProvider#big_query_custom_endpoint}.
        :param bigquery_datapolicy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_datapolicy_custom_endpoint GoogleBetaProvider#bigquery_datapolicy_custom_endpoint}.
        :param bigquery_data_transfer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_data_transfer_custom_endpoint GoogleBetaProvider#bigquery_data_transfer_custom_endpoint}.
        :param bigquery_reservation_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_reservation_custom_endpoint GoogleBetaProvider#bigquery_reservation_custom_endpoint}.
        :param bigtable_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigtable_custom_endpoint GoogleBetaProvider#bigtable_custom_endpoint}.
        :param billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#billing_custom_endpoint GoogleBetaProvider#billing_custom_endpoint}.
        :param billing_project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#billing_project GoogleBetaProvider#billing_project}.
        :param binary_authorization_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#binary_authorization_custom_endpoint GoogleBetaProvider#binary_authorization_custom_endpoint}.
        :param blockchain_node_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#blockchain_node_engine_custom_endpoint GoogleBetaProvider#blockchain_node_engine_custom_endpoint}.
        :param certificate_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#certificate_manager_custom_endpoint GoogleBetaProvider#certificate_manager_custom_endpoint}.
        :param chronicle_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#chronicle_custom_endpoint GoogleBetaProvider#chronicle_custom_endpoint}.
        :param cloud_asset_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_asset_custom_endpoint GoogleBetaProvider#cloud_asset_custom_endpoint}.
        :param cloud_billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_billing_custom_endpoint GoogleBetaProvider#cloud_billing_custom_endpoint}.
        :param cloud_build_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_build_custom_endpoint GoogleBetaProvider#cloud_build_custom_endpoint}.
        :param cloudbuildv2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloudbuildv2_custom_endpoint GoogleBetaProvider#cloudbuildv2_custom_endpoint}.
        :param cloud_build_worker_pool_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_build_worker_pool_custom_endpoint GoogleBetaProvider#cloud_build_worker_pool_custom_endpoint}.
        :param clouddeploy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#clouddeploy_custom_endpoint GoogleBetaProvider#clouddeploy_custom_endpoint}.
        :param clouddomains_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#clouddomains_custom_endpoint GoogleBetaProvider#clouddomains_custom_endpoint}.
        :param cloudfunctions2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloudfunctions2_custom_endpoint GoogleBetaProvider#cloudfunctions2_custom_endpoint}.
        :param cloud_functions_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_functions_custom_endpoint GoogleBetaProvider#cloud_functions_custom_endpoint}.
        :param cloud_identity_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_identity_custom_endpoint GoogleBetaProvider#cloud_identity_custom_endpoint}.
        :param cloud_ids_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_ids_custom_endpoint GoogleBetaProvider#cloud_ids_custom_endpoint}.
        :param cloud_quotas_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_quotas_custom_endpoint GoogleBetaProvider#cloud_quotas_custom_endpoint}.
        :param cloud_resource_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_resource_manager_custom_endpoint GoogleBetaProvider#cloud_resource_manager_custom_endpoint}.
        :param cloud_run_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_run_custom_endpoint GoogleBetaProvider#cloud_run_custom_endpoint}.
        :param cloud_run_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_run_v2_custom_endpoint GoogleBetaProvider#cloud_run_v2_custom_endpoint}.
        :param cloud_scheduler_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_scheduler_custom_endpoint GoogleBetaProvider#cloud_scheduler_custom_endpoint}.
        :param cloud_tasks_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_tasks_custom_endpoint GoogleBetaProvider#cloud_tasks_custom_endpoint}.
        :param colab_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#colab_custom_endpoint GoogleBetaProvider#colab_custom_endpoint}.
        :param composer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#composer_custom_endpoint GoogleBetaProvider#composer_custom_endpoint}.
        :param compute_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#compute_custom_endpoint GoogleBetaProvider#compute_custom_endpoint}.
        :param container_analysis_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_analysis_custom_endpoint GoogleBetaProvider#container_analysis_custom_endpoint}.
        :param container_attached_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_attached_custom_endpoint GoogleBetaProvider#container_attached_custom_endpoint}.
        :param container_aws_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_aws_custom_endpoint GoogleBetaProvider#container_aws_custom_endpoint}.
        :param container_azure_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_azure_custom_endpoint GoogleBetaProvider#container_azure_custom_endpoint}.
        :param container_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_custom_endpoint GoogleBetaProvider#container_custom_endpoint}.
        :param core_billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#core_billing_custom_endpoint GoogleBetaProvider#core_billing_custom_endpoint}.
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#credentials GoogleBetaProvider#credentials}.
        :param database_migration_service_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#database_migration_service_custom_endpoint GoogleBetaProvider#database_migration_service_custom_endpoint}.
        :param data_catalog_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_catalog_custom_endpoint GoogleBetaProvider#data_catalog_custom_endpoint}.
        :param dataflow_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataflow_custom_endpoint GoogleBetaProvider#dataflow_custom_endpoint}.
        :param dataform_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataform_custom_endpoint GoogleBetaProvider#dataform_custom_endpoint}.
        :param data_fusion_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_fusion_custom_endpoint GoogleBetaProvider#data_fusion_custom_endpoint}.
        :param data_loss_prevention_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_loss_prevention_custom_endpoint GoogleBetaProvider#data_loss_prevention_custom_endpoint}.
        :param data_pipeline_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_pipeline_custom_endpoint GoogleBetaProvider#data_pipeline_custom_endpoint}.
        :param dataplex_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataplex_custom_endpoint GoogleBetaProvider#dataplex_custom_endpoint}.
        :param dataproc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataproc_custom_endpoint GoogleBetaProvider#dataproc_custom_endpoint}.
        :param dataproc_gdc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataproc_gdc_custom_endpoint GoogleBetaProvider#dataproc_gdc_custom_endpoint}.
        :param dataproc_metastore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataproc_metastore_custom_endpoint GoogleBetaProvider#dataproc_metastore_custom_endpoint}.
        :param datastream_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#datastream_custom_endpoint GoogleBetaProvider#datastream_custom_endpoint}.
        :param default_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#default_labels GoogleBetaProvider#default_labels}.
        :param deployment_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#deployment_manager_custom_endpoint GoogleBetaProvider#deployment_manager_custom_endpoint}.
        :param developer_connect_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#developer_connect_custom_endpoint GoogleBetaProvider#developer_connect_custom_endpoint}.
        :param dialogflow_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dialogflow_custom_endpoint GoogleBetaProvider#dialogflow_custom_endpoint}.
        :param dialogflow_cx_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dialogflow_cx_custom_endpoint GoogleBetaProvider#dialogflow_cx_custom_endpoint}.
        :param discovery_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#discovery_engine_custom_endpoint GoogleBetaProvider#discovery_engine_custom_endpoint}.
        :param dns_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dns_custom_endpoint GoogleBetaProvider#dns_custom_endpoint}.
        :param document_ai_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#document_ai_custom_endpoint GoogleBetaProvider#document_ai_custom_endpoint}.
        :param document_ai_warehouse_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#document_ai_warehouse_custom_endpoint GoogleBetaProvider#document_ai_warehouse_custom_endpoint}.
        :param edgecontainer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#edgecontainer_custom_endpoint GoogleBetaProvider#edgecontainer_custom_endpoint}.
        :param edgenetwork_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#edgenetwork_custom_endpoint GoogleBetaProvider#edgenetwork_custom_endpoint}.
        :param essential_contacts_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#essential_contacts_custom_endpoint GoogleBetaProvider#essential_contacts_custom_endpoint}.
        :param eventarc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#eventarc_custom_endpoint GoogleBetaProvider#eventarc_custom_endpoint}.
        :param external_credentials: external_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#external_credentials GoogleBetaProvider#external_credentials}
        :param filestore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#filestore_custom_endpoint GoogleBetaProvider#filestore_custom_endpoint}.
        :param firebase_app_check_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_app_check_custom_endpoint GoogleBetaProvider#firebase_app_check_custom_endpoint}.
        :param firebase_app_hosting_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_app_hosting_custom_endpoint GoogleBetaProvider#firebase_app_hosting_custom_endpoint}.
        :param firebase_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_custom_endpoint GoogleBetaProvider#firebase_custom_endpoint}.
        :param firebase_database_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_database_custom_endpoint GoogleBetaProvider#firebase_database_custom_endpoint}.
        :param firebase_data_connect_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_data_connect_custom_endpoint GoogleBetaProvider#firebase_data_connect_custom_endpoint}.
        :param firebase_extensions_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_extensions_custom_endpoint GoogleBetaProvider#firebase_extensions_custom_endpoint}.
        :param firebase_hosting_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_hosting_custom_endpoint GoogleBetaProvider#firebase_hosting_custom_endpoint}.
        :param firebaserules_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebaserules_custom_endpoint GoogleBetaProvider#firebaserules_custom_endpoint}.
        :param firebase_storage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_storage_custom_endpoint GoogleBetaProvider#firebase_storage_custom_endpoint}.
        :param firestore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firestore_custom_endpoint GoogleBetaProvider#firestore_custom_endpoint}.
        :param gemini_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gemini_custom_endpoint GoogleBetaProvider#gemini_custom_endpoint}.
        :param gke_backup_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gke_backup_custom_endpoint GoogleBetaProvider#gke_backup_custom_endpoint}.
        :param gke_hub2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gke_hub2_custom_endpoint GoogleBetaProvider#gke_hub2_custom_endpoint}.
        :param gke_hub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gke_hub_custom_endpoint GoogleBetaProvider#gke_hub_custom_endpoint}.
        :param gkehub_feature_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gkehub_feature_custom_endpoint GoogleBetaProvider#gkehub_feature_custom_endpoint}.
        :param gkeonprem_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gkeonprem_custom_endpoint GoogleBetaProvider#gkeonprem_custom_endpoint}.
        :param healthcare_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#healthcare_custom_endpoint GoogleBetaProvider#healthcare_custom_endpoint}.
        :param iam2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam2_custom_endpoint GoogleBetaProvider#iam2_custom_endpoint}.
        :param iam3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam3_custom_endpoint GoogleBetaProvider#iam3_custom_endpoint}.
        :param iam_beta_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_beta_custom_endpoint GoogleBetaProvider#iam_beta_custom_endpoint}.
        :param iam_credentials_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_credentials_custom_endpoint GoogleBetaProvider#iam_credentials_custom_endpoint}.
        :param iam_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_custom_endpoint GoogleBetaProvider#iam_custom_endpoint}.
        :param iam_workforce_pool_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_workforce_pool_custom_endpoint GoogleBetaProvider#iam_workforce_pool_custom_endpoint}.
        :param iap_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iap_custom_endpoint GoogleBetaProvider#iap_custom_endpoint}.
        :param identity_platform_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#identity_platform_custom_endpoint GoogleBetaProvider#identity_platform_custom_endpoint}.
        :param impersonate_service_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#impersonate_service_account GoogleBetaProvider#impersonate_service_account}.
        :param impersonate_service_account_delegates: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#impersonate_service_account_delegates GoogleBetaProvider#impersonate_service_account_delegates}.
        :param integration_connectors_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#integration_connectors_custom_endpoint GoogleBetaProvider#integration_connectors_custom_endpoint}.
        :param integrations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#integrations_custom_endpoint GoogleBetaProvider#integrations_custom_endpoint}.
        :param kms_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#kms_custom_endpoint GoogleBetaProvider#kms_custom_endpoint}.
        :param logging_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#logging_custom_endpoint GoogleBetaProvider#logging_custom_endpoint}.
        :param looker_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#looker_custom_endpoint GoogleBetaProvider#looker_custom_endpoint}.
        :param lustre_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#lustre_custom_endpoint GoogleBetaProvider#lustre_custom_endpoint}.
        :param managed_kafka_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#managed_kafka_custom_endpoint GoogleBetaProvider#managed_kafka_custom_endpoint}.
        :param memcache_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#memcache_custom_endpoint GoogleBetaProvider#memcache_custom_endpoint}.
        :param memorystore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#memorystore_custom_endpoint GoogleBetaProvider#memorystore_custom_endpoint}.
        :param migration_center_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#migration_center_custom_endpoint GoogleBetaProvider#migration_center_custom_endpoint}.
        :param ml_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#ml_engine_custom_endpoint GoogleBetaProvider#ml_engine_custom_endpoint}.
        :param monitoring_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#monitoring_custom_endpoint GoogleBetaProvider#monitoring_custom_endpoint}.
        :param netapp_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#netapp_custom_endpoint GoogleBetaProvider#netapp_custom_endpoint}.
        :param network_connectivity_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_connectivity_custom_endpoint GoogleBetaProvider#network_connectivity_custom_endpoint}.
        :param network_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_management_custom_endpoint GoogleBetaProvider#network_management_custom_endpoint}.
        :param network_security_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_security_custom_endpoint GoogleBetaProvider#network_security_custom_endpoint}.
        :param network_services_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_services_custom_endpoint GoogleBetaProvider#network_services_custom_endpoint}.
        :param notebooks_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#notebooks_custom_endpoint GoogleBetaProvider#notebooks_custom_endpoint}.
        :param oracle_database_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#oracle_database_custom_endpoint GoogleBetaProvider#oracle_database_custom_endpoint}.
        :param org_policy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#org_policy_custom_endpoint GoogleBetaProvider#org_policy_custom_endpoint}.
        :param os_config_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#os_config_custom_endpoint GoogleBetaProvider#os_config_custom_endpoint}.
        :param os_config_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#os_config_v2_custom_endpoint GoogleBetaProvider#os_config_v2_custom_endpoint}.
        :param os_login_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#os_login_custom_endpoint GoogleBetaProvider#os_login_custom_endpoint}.
        :param parallelstore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#parallelstore_custom_endpoint GoogleBetaProvider#parallelstore_custom_endpoint}.
        :param parameter_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#parameter_manager_custom_endpoint GoogleBetaProvider#parameter_manager_custom_endpoint}.
        :param parameter_manager_regional_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#parameter_manager_regional_custom_endpoint GoogleBetaProvider#parameter_manager_regional_custom_endpoint}.
        :param privateca_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#privateca_custom_endpoint GoogleBetaProvider#privateca_custom_endpoint}.
        :param privileged_access_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#privileged_access_manager_custom_endpoint GoogleBetaProvider#privileged_access_manager_custom_endpoint}.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#project GoogleBetaProvider#project}.
        :param public_ca_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#public_ca_custom_endpoint GoogleBetaProvider#public_ca_custom_endpoint}.
        :param pubsub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#pubsub_custom_endpoint GoogleBetaProvider#pubsub_custom_endpoint}.
        :param pubsub_lite_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#pubsub_lite_custom_endpoint GoogleBetaProvider#pubsub_lite_custom_endpoint}.
        :param recaptcha_enterprise_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#recaptcha_enterprise_custom_endpoint GoogleBetaProvider#recaptcha_enterprise_custom_endpoint}.
        :param redis_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#redis_custom_endpoint GoogleBetaProvider#redis_custom_endpoint}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#region GoogleBetaProvider#region}.
        :param request_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#request_reason GoogleBetaProvider#request_reason}.
        :param request_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#request_timeout GoogleBetaProvider#request_timeout}.
        :param resource_manager3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#resource_manager3_custom_endpoint GoogleBetaProvider#resource_manager3_custom_endpoint}.
        :param resource_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#resource_manager_custom_endpoint GoogleBetaProvider#resource_manager_custom_endpoint}.
        :param resource_manager_v3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#resource_manager_v3_custom_endpoint GoogleBetaProvider#resource_manager_v3_custom_endpoint}.
        :param runtimeconfig_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#runtimeconfig_custom_endpoint GoogleBetaProvider#runtimeconfig_custom_endpoint}.
        :param runtime_config_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#runtime_config_custom_endpoint GoogleBetaProvider#runtime_config_custom_endpoint}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#scopes GoogleBetaProvider#scopes}.
        :param secret_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#secret_manager_custom_endpoint GoogleBetaProvider#secret_manager_custom_endpoint}.
        :param secret_manager_regional_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#secret_manager_regional_custom_endpoint GoogleBetaProvider#secret_manager_regional_custom_endpoint}.
        :param secure_source_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#secure_source_manager_custom_endpoint GoogleBetaProvider#secure_source_manager_custom_endpoint}.
        :param security_center_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_center_custom_endpoint GoogleBetaProvider#security_center_custom_endpoint}.
        :param security_center_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_center_management_custom_endpoint GoogleBetaProvider#security_center_management_custom_endpoint}.
        :param security_center_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_center_v2_custom_endpoint GoogleBetaProvider#security_center_v2_custom_endpoint}.
        :param securityposture_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#securityposture_custom_endpoint GoogleBetaProvider#securityposture_custom_endpoint}.
        :param security_scanner_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_scanner_custom_endpoint GoogleBetaProvider#security_scanner_custom_endpoint}.
        :param service_directory_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_directory_custom_endpoint GoogleBetaProvider#service_directory_custom_endpoint}.
        :param service_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_management_custom_endpoint GoogleBetaProvider#service_management_custom_endpoint}.
        :param service_networking_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_networking_custom_endpoint GoogleBetaProvider#service_networking_custom_endpoint}.
        :param service_usage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_usage_custom_endpoint GoogleBetaProvider#service_usage_custom_endpoint}.
        :param site_verification_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#site_verification_custom_endpoint GoogleBetaProvider#site_verification_custom_endpoint}.
        :param source_repo_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#source_repo_custom_endpoint GoogleBetaProvider#source_repo_custom_endpoint}.
        :param spanner_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#spanner_custom_endpoint GoogleBetaProvider#spanner_custom_endpoint}.
        :param sql_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#sql_custom_endpoint GoogleBetaProvider#sql_custom_endpoint}.
        :param storage_batch_operations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_batch_operations_custom_endpoint GoogleBetaProvider#storage_batch_operations_custom_endpoint}.
        :param storage_control_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_control_custom_endpoint GoogleBetaProvider#storage_control_custom_endpoint}.
        :param storage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_custom_endpoint GoogleBetaProvider#storage_custom_endpoint}.
        :param storage_insights_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_insights_custom_endpoint GoogleBetaProvider#storage_insights_custom_endpoint}.
        :param storage_transfer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_transfer_custom_endpoint GoogleBetaProvider#storage_transfer_custom_endpoint}.
        :param tags_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tags_custom_endpoint GoogleBetaProvider#tags_custom_endpoint}.
        :param tags_location_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tags_location_custom_endpoint GoogleBetaProvider#tags_location_custom_endpoint}.
        :param terraform_attribution_label_addition_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#terraform_attribution_label_addition_strategy GoogleBetaProvider#terraform_attribution_label_addition_strategy}.
        :param tpu_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tpu_custom_endpoint GoogleBetaProvider#tpu_custom_endpoint}.
        :param tpu_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tpu_v2_custom_endpoint GoogleBetaProvider#tpu_v2_custom_endpoint}.
        :param transcoder_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#transcoder_custom_endpoint GoogleBetaProvider#transcoder_custom_endpoint}.
        :param universe_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#universe_domain GoogleBetaProvider#universe_domain}.
        :param user_project_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#user_project_override GoogleBetaProvider#user_project_override}.
        :param vertex_ai_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#vertex_ai_custom_endpoint GoogleBetaProvider#vertex_ai_custom_endpoint}.
        :param vmwareengine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#vmwareengine_custom_endpoint GoogleBetaProvider#vmwareengine_custom_endpoint}.
        :param vpc_access_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#vpc_access_custom_endpoint GoogleBetaProvider#vpc_access_custom_endpoint}.
        :param workbench_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#workbench_custom_endpoint GoogleBetaProvider#workbench_custom_endpoint}.
        :param workflows_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#workflows_custom_endpoint GoogleBetaProvider#workflows_custom_endpoint}.
        :param workstations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#workstations_custom_endpoint GoogleBetaProvider#workstations_custom_endpoint}.
        :param zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#zone GoogleBetaProvider#zone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0888201207876e3240f2c01d78947ebd8ad730c84b80d6e77c356836c1f801)
            check_type(argname="argument access_approval_custom_endpoint", value=access_approval_custom_endpoint, expected_type=type_hints["access_approval_custom_endpoint"])
            check_type(argname="argument access_context_manager_custom_endpoint", value=access_context_manager_custom_endpoint, expected_type=type_hints["access_context_manager_custom_endpoint"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument active_directory_custom_endpoint", value=active_directory_custom_endpoint, expected_type=type_hints["active_directory_custom_endpoint"])
            check_type(argname="argument add_terraform_attribution_label", value=add_terraform_attribution_label, expected_type=type_hints["add_terraform_attribution_label"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument alloydb_custom_endpoint", value=alloydb_custom_endpoint, expected_type=type_hints["alloydb_custom_endpoint"])
            check_type(argname="argument api_gateway_custom_endpoint", value=api_gateway_custom_endpoint, expected_type=type_hints["api_gateway_custom_endpoint"])
            check_type(argname="argument apigee_custom_endpoint", value=apigee_custom_endpoint, expected_type=type_hints["apigee_custom_endpoint"])
            check_type(argname="argument apihub_custom_endpoint", value=apihub_custom_endpoint, expected_type=type_hints["apihub_custom_endpoint"])
            check_type(argname="argument apikeys_custom_endpoint", value=apikeys_custom_endpoint, expected_type=type_hints["apikeys_custom_endpoint"])
            check_type(argname="argument app_engine_custom_endpoint", value=app_engine_custom_endpoint, expected_type=type_hints["app_engine_custom_endpoint"])
            check_type(argname="argument apphub_custom_endpoint", value=apphub_custom_endpoint, expected_type=type_hints["apphub_custom_endpoint"])
            check_type(argname="argument artifact_registry_custom_endpoint", value=artifact_registry_custom_endpoint, expected_type=type_hints["artifact_registry_custom_endpoint"])
            check_type(argname="argument assured_workloads_custom_endpoint", value=assured_workloads_custom_endpoint, expected_type=type_hints["assured_workloads_custom_endpoint"])
            check_type(argname="argument backup_dr_custom_endpoint", value=backup_dr_custom_endpoint, expected_type=type_hints["backup_dr_custom_endpoint"])
            check_type(argname="argument batching", value=batching, expected_type=type_hints["batching"])
            check_type(argname="argument beyondcorp_custom_endpoint", value=beyondcorp_custom_endpoint, expected_type=type_hints["beyondcorp_custom_endpoint"])
            check_type(argname="argument biglake_custom_endpoint", value=biglake_custom_endpoint, expected_type=type_hints["biglake_custom_endpoint"])
            check_type(argname="argument bigquery_analytics_hub_custom_endpoint", value=bigquery_analytics_hub_custom_endpoint, expected_type=type_hints["bigquery_analytics_hub_custom_endpoint"])
            check_type(argname="argument bigquery_connection_custom_endpoint", value=bigquery_connection_custom_endpoint, expected_type=type_hints["bigquery_connection_custom_endpoint"])
            check_type(argname="argument big_query_custom_endpoint", value=big_query_custom_endpoint, expected_type=type_hints["big_query_custom_endpoint"])
            check_type(argname="argument bigquery_datapolicy_custom_endpoint", value=bigquery_datapolicy_custom_endpoint, expected_type=type_hints["bigquery_datapolicy_custom_endpoint"])
            check_type(argname="argument bigquery_data_transfer_custom_endpoint", value=bigquery_data_transfer_custom_endpoint, expected_type=type_hints["bigquery_data_transfer_custom_endpoint"])
            check_type(argname="argument bigquery_reservation_custom_endpoint", value=bigquery_reservation_custom_endpoint, expected_type=type_hints["bigquery_reservation_custom_endpoint"])
            check_type(argname="argument bigtable_custom_endpoint", value=bigtable_custom_endpoint, expected_type=type_hints["bigtable_custom_endpoint"])
            check_type(argname="argument billing_custom_endpoint", value=billing_custom_endpoint, expected_type=type_hints["billing_custom_endpoint"])
            check_type(argname="argument billing_project", value=billing_project, expected_type=type_hints["billing_project"])
            check_type(argname="argument binary_authorization_custom_endpoint", value=binary_authorization_custom_endpoint, expected_type=type_hints["binary_authorization_custom_endpoint"])
            check_type(argname="argument blockchain_node_engine_custom_endpoint", value=blockchain_node_engine_custom_endpoint, expected_type=type_hints["blockchain_node_engine_custom_endpoint"])
            check_type(argname="argument certificate_manager_custom_endpoint", value=certificate_manager_custom_endpoint, expected_type=type_hints["certificate_manager_custom_endpoint"])
            check_type(argname="argument chronicle_custom_endpoint", value=chronicle_custom_endpoint, expected_type=type_hints["chronicle_custom_endpoint"])
            check_type(argname="argument cloud_asset_custom_endpoint", value=cloud_asset_custom_endpoint, expected_type=type_hints["cloud_asset_custom_endpoint"])
            check_type(argname="argument cloud_billing_custom_endpoint", value=cloud_billing_custom_endpoint, expected_type=type_hints["cloud_billing_custom_endpoint"])
            check_type(argname="argument cloud_build_custom_endpoint", value=cloud_build_custom_endpoint, expected_type=type_hints["cloud_build_custom_endpoint"])
            check_type(argname="argument cloudbuildv2_custom_endpoint", value=cloudbuildv2_custom_endpoint, expected_type=type_hints["cloudbuildv2_custom_endpoint"])
            check_type(argname="argument cloud_build_worker_pool_custom_endpoint", value=cloud_build_worker_pool_custom_endpoint, expected_type=type_hints["cloud_build_worker_pool_custom_endpoint"])
            check_type(argname="argument clouddeploy_custom_endpoint", value=clouddeploy_custom_endpoint, expected_type=type_hints["clouddeploy_custom_endpoint"])
            check_type(argname="argument clouddomains_custom_endpoint", value=clouddomains_custom_endpoint, expected_type=type_hints["clouddomains_custom_endpoint"])
            check_type(argname="argument cloudfunctions2_custom_endpoint", value=cloudfunctions2_custom_endpoint, expected_type=type_hints["cloudfunctions2_custom_endpoint"])
            check_type(argname="argument cloud_functions_custom_endpoint", value=cloud_functions_custom_endpoint, expected_type=type_hints["cloud_functions_custom_endpoint"])
            check_type(argname="argument cloud_identity_custom_endpoint", value=cloud_identity_custom_endpoint, expected_type=type_hints["cloud_identity_custom_endpoint"])
            check_type(argname="argument cloud_ids_custom_endpoint", value=cloud_ids_custom_endpoint, expected_type=type_hints["cloud_ids_custom_endpoint"])
            check_type(argname="argument cloud_quotas_custom_endpoint", value=cloud_quotas_custom_endpoint, expected_type=type_hints["cloud_quotas_custom_endpoint"])
            check_type(argname="argument cloud_resource_manager_custom_endpoint", value=cloud_resource_manager_custom_endpoint, expected_type=type_hints["cloud_resource_manager_custom_endpoint"])
            check_type(argname="argument cloud_run_custom_endpoint", value=cloud_run_custom_endpoint, expected_type=type_hints["cloud_run_custom_endpoint"])
            check_type(argname="argument cloud_run_v2_custom_endpoint", value=cloud_run_v2_custom_endpoint, expected_type=type_hints["cloud_run_v2_custom_endpoint"])
            check_type(argname="argument cloud_scheduler_custom_endpoint", value=cloud_scheduler_custom_endpoint, expected_type=type_hints["cloud_scheduler_custom_endpoint"])
            check_type(argname="argument cloud_tasks_custom_endpoint", value=cloud_tasks_custom_endpoint, expected_type=type_hints["cloud_tasks_custom_endpoint"])
            check_type(argname="argument colab_custom_endpoint", value=colab_custom_endpoint, expected_type=type_hints["colab_custom_endpoint"])
            check_type(argname="argument composer_custom_endpoint", value=composer_custom_endpoint, expected_type=type_hints["composer_custom_endpoint"])
            check_type(argname="argument compute_custom_endpoint", value=compute_custom_endpoint, expected_type=type_hints["compute_custom_endpoint"])
            check_type(argname="argument container_analysis_custom_endpoint", value=container_analysis_custom_endpoint, expected_type=type_hints["container_analysis_custom_endpoint"])
            check_type(argname="argument container_attached_custom_endpoint", value=container_attached_custom_endpoint, expected_type=type_hints["container_attached_custom_endpoint"])
            check_type(argname="argument container_aws_custom_endpoint", value=container_aws_custom_endpoint, expected_type=type_hints["container_aws_custom_endpoint"])
            check_type(argname="argument container_azure_custom_endpoint", value=container_azure_custom_endpoint, expected_type=type_hints["container_azure_custom_endpoint"])
            check_type(argname="argument container_custom_endpoint", value=container_custom_endpoint, expected_type=type_hints["container_custom_endpoint"])
            check_type(argname="argument core_billing_custom_endpoint", value=core_billing_custom_endpoint, expected_type=type_hints["core_billing_custom_endpoint"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument database_migration_service_custom_endpoint", value=database_migration_service_custom_endpoint, expected_type=type_hints["database_migration_service_custom_endpoint"])
            check_type(argname="argument data_catalog_custom_endpoint", value=data_catalog_custom_endpoint, expected_type=type_hints["data_catalog_custom_endpoint"])
            check_type(argname="argument dataflow_custom_endpoint", value=dataflow_custom_endpoint, expected_type=type_hints["dataflow_custom_endpoint"])
            check_type(argname="argument dataform_custom_endpoint", value=dataform_custom_endpoint, expected_type=type_hints["dataform_custom_endpoint"])
            check_type(argname="argument data_fusion_custom_endpoint", value=data_fusion_custom_endpoint, expected_type=type_hints["data_fusion_custom_endpoint"])
            check_type(argname="argument data_loss_prevention_custom_endpoint", value=data_loss_prevention_custom_endpoint, expected_type=type_hints["data_loss_prevention_custom_endpoint"])
            check_type(argname="argument data_pipeline_custom_endpoint", value=data_pipeline_custom_endpoint, expected_type=type_hints["data_pipeline_custom_endpoint"])
            check_type(argname="argument dataplex_custom_endpoint", value=dataplex_custom_endpoint, expected_type=type_hints["dataplex_custom_endpoint"])
            check_type(argname="argument dataproc_custom_endpoint", value=dataproc_custom_endpoint, expected_type=type_hints["dataproc_custom_endpoint"])
            check_type(argname="argument dataproc_gdc_custom_endpoint", value=dataproc_gdc_custom_endpoint, expected_type=type_hints["dataproc_gdc_custom_endpoint"])
            check_type(argname="argument dataproc_metastore_custom_endpoint", value=dataproc_metastore_custom_endpoint, expected_type=type_hints["dataproc_metastore_custom_endpoint"])
            check_type(argname="argument datastream_custom_endpoint", value=datastream_custom_endpoint, expected_type=type_hints["datastream_custom_endpoint"])
            check_type(argname="argument default_labels", value=default_labels, expected_type=type_hints["default_labels"])
            check_type(argname="argument deployment_manager_custom_endpoint", value=deployment_manager_custom_endpoint, expected_type=type_hints["deployment_manager_custom_endpoint"])
            check_type(argname="argument developer_connect_custom_endpoint", value=developer_connect_custom_endpoint, expected_type=type_hints["developer_connect_custom_endpoint"])
            check_type(argname="argument dialogflow_custom_endpoint", value=dialogflow_custom_endpoint, expected_type=type_hints["dialogflow_custom_endpoint"])
            check_type(argname="argument dialogflow_cx_custom_endpoint", value=dialogflow_cx_custom_endpoint, expected_type=type_hints["dialogflow_cx_custom_endpoint"])
            check_type(argname="argument discovery_engine_custom_endpoint", value=discovery_engine_custom_endpoint, expected_type=type_hints["discovery_engine_custom_endpoint"])
            check_type(argname="argument dns_custom_endpoint", value=dns_custom_endpoint, expected_type=type_hints["dns_custom_endpoint"])
            check_type(argname="argument document_ai_custom_endpoint", value=document_ai_custom_endpoint, expected_type=type_hints["document_ai_custom_endpoint"])
            check_type(argname="argument document_ai_warehouse_custom_endpoint", value=document_ai_warehouse_custom_endpoint, expected_type=type_hints["document_ai_warehouse_custom_endpoint"])
            check_type(argname="argument edgecontainer_custom_endpoint", value=edgecontainer_custom_endpoint, expected_type=type_hints["edgecontainer_custom_endpoint"])
            check_type(argname="argument edgenetwork_custom_endpoint", value=edgenetwork_custom_endpoint, expected_type=type_hints["edgenetwork_custom_endpoint"])
            check_type(argname="argument essential_contacts_custom_endpoint", value=essential_contacts_custom_endpoint, expected_type=type_hints["essential_contacts_custom_endpoint"])
            check_type(argname="argument eventarc_custom_endpoint", value=eventarc_custom_endpoint, expected_type=type_hints["eventarc_custom_endpoint"])
            check_type(argname="argument external_credentials", value=external_credentials, expected_type=type_hints["external_credentials"])
            check_type(argname="argument filestore_custom_endpoint", value=filestore_custom_endpoint, expected_type=type_hints["filestore_custom_endpoint"])
            check_type(argname="argument firebase_app_check_custom_endpoint", value=firebase_app_check_custom_endpoint, expected_type=type_hints["firebase_app_check_custom_endpoint"])
            check_type(argname="argument firebase_app_hosting_custom_endpoint", value=firebase_app_hosting_custom_endpoint, expected_type=type_hints["firebase_app_hosting_custom_endpoint"])
            check_type(argname="argument firebase_custom_endpoint", value=firebase_custom_endpoint, expected_type=type_hints["firebase_custom_endpoint"])
            check_type(argname="argument firebase_database_custom_endpoint", value=firebase_database_custom_endpoint, expected_type=type_hints["firebase_database_custom_endpoint"])
            check_type(argname="argument firebase_data_connect_custom_endpoint", value=firebase_data_connect_custom_endpoint, expected_type=type_hints["firebase_data_connect_custom_endpoint"])
            check_type(argname="argument firebase_extensions_custom_endpoint", value=firebase_extensions_custom_endpoint, expected_type=type_hints["firebase_extensions_custom_endpoint"])
            check_type(argname="argument firebase_hosting_custom_endpoint", value=firebase_hosting_custom_endpoint, expected_type=type_hints["firebase_hosting_custom_endpoint"])
            check_type(argname="argument firebaserules_custom_endpoint", value=firebaserules_custom_endpoint, expected_type=type_hints["firebaserules_custom_endpoint"])
            check_type(argname="argument firebase_storage_custom_endpoint", value=firebase_storage_custom_endpoint, expected_type=type_hints["firebase_storage_custom_endpoint"])
            check_type(argname="argument firestore_custom_endpoint", value=firestore_custom_endpoint, expected_type=type_hints["firestore_custom_endpoint"])
            check_type(argname="argument gemini_custom_endpoint", value=gemini_custom_endpoint, expected_type=type_hints["gemini_custom_endpoint"])
            check_type(argname="argument gke_backup_custom_endpoint", value=gke_backup_custom_endpoint, expected_type=type_hints["gke_backup_custom_endpoint"])
            check_type(argname="argument gke_hub2_custom_endpoint", value=gke_hub2_custom_endpoint, expected_type=type_hints["gke_hub2_custom_endpoint"])
            check_type(argname="argument gke_hub_custom_endpoint", value=gke_hub_custom_endpoint, expected_type=type_hints["gke_hub_custom_endpoint"])
            check_type(argname="argument gkehub_feature_custom_endpoint", value=gkehub_feature_custom_endpoint, expected_type=type_hints["gkehub_feature_custom_endpoint"])
            check_type(argname="argument gkeonprem_custom_endpoint", value=gkeonprem_custom_endpoint, expected_type=type_hints["gkeonprem_custom_endpoint"])
            check_type(argname="argument healthcare_custom_endpoint", value=healthcare_custom_endpoint, expected_type=type_hints["healthcare_custom_endpoint"])
            check_type(argname="argument iam2_custom_endpoint", value=iam2_custom_endpoint, expected_type=type_hints["iam2_custom_endpoint"])
            check_type(argname="argument iam3_custom_endpoint", value=iam3_custom_endpoint, expected_type=type_hints["iam3_custom_endpoint"])
            check_type(argname="argument iam_beta_custom_endpoint", value=iam_beta_custom_endpoint, expected_type=type_hints["iam_beta_custom_endpoint"])
            check_type(argname="argument iam_credentials_custom_endpoint", value=iam_credentials_custom_endpoint, expected_type=type_hints["iam_credentials_custom_endpoint"])
            check_type(argname="argument iam_custom_endpoint", value=iam_custom_endpoint, expected_type=type_hints["iam_custom_endpoint"])
            check_type(argname="argument iam_workforce_pool_custom_endpoint", value=iam_workforce_pool_custom_endpoint, expected_type=type_hints["iam_workforce_pool_custom_endpoint"])
            check_type(argname="argument iap_custom_endpoint", value=iap_custom_endpoint, expected_type=type_hints["iap_custom_endpoint"])
            check_type(argname="argument identity_platform_custom_endpoint", value=identity_platform_custom_endpoint, expected_type=type_hints["identity_platform_custom_endpoint"])
            check_type(argname="argument impersonate_service_account", value=impersonate_service_account, expected_type=type_hints["impersonate_service_account"])
            check_type(argname="argument impersonate_service_account_delegates", value=impersonate_service_account_delegates, expected_type=type_hints["impersonate_service_account_delegates"])
            check_type(argname="argument integration_connectors_custom_endpoint", value=integration_connectors_custom_endpoint, expected_type=type_hints["integration_connectors_custom_endpoint"])
            check_type(argname="argument integrations_custom_endpoint", value=integrations_custom_endpoint, expected_type=type_hints["integrations_custom_endpoint"])
            check_type(argname="argument kms_custom_endpoint", value=kms_custom_endpoint, expected_type=type_hints["kms_custom_endpoint"])
            check_type(argname="argument logging_custom_endpoint", value=logging_custom_endpoint, expected_type=type_hints["logging_custom_endpoint"])
            check_type(argname="argument looker_custom_endpoint", value=looker_custom_endpoint, expected_type=type_hints["looker_custom_endpoint"])
            check_type(argname="argument lustre_custom_endpoint", value=lustre_custom_endpoint, expected_type=type_hints["lustre_custom_endpoint"])
            check_type(argname="argument managed_kafka_custom_endpoint", value=managed_kafka_custom_endpoint, expected_type=type_hints["managed_kafka_custom_endpoint"])
            check_type(argname="argument memcache_custom_endpoint", value=memcache_custom_endpoint, expected_type=type_hints["memcache_custom_endpoint"])
            check_type(argname="argument memorystore_custom_endpoint", value=memorystore_custom_endpoint, expected_type=type_hints["memorystore_custom_endpoint"])
            check_type(argname="argument migration_center_custom_endpoint", value=migration_center_custom_endpoint, expected_type=type_hints["migration_center_custom_endpoint"])
            check_type(argname="argument ml_engine_custom_endpoint", value=ml_engine_custom_endpoint, expected_type=type_hints["ml_engine_custom_endpoint"])
            check_type(argname="argument monitoring_custom_endpoint", value=monitoring_custom_endpoint, expected_type=type_hints["monitoring_custom_endpoint"])
            check_type(argname="argument netapp_custom_endpoint", value=netapp_custom_endpoint, expected_type=type_hints["netapp_custom_endpoint"])
            check_type(argname="argument network_connectivity_custom_endpoint", value=network_connectivity_custom_endpoint, expected_type=type_hints["network_connectivity_custom_endpoint"])
            check_type(argname="argument network_management_custom_endpoint", value=network_management_custom_endpoint, expected_type=type_hints["network_management_custom_endpoint"])
            check_type(argname="argument network_security_custom_endpoint", value=network_security_custom_endpoint, expected_type=type_hints["network_security_custom_endpoint"])
            check_type(argname="argument network_services_custom_endpoint", value=network_services_custom_endpoint, expected_type=type_hints["network_services_custom_endpoint"])
            check_type(argname="argument notebooks_custom_endpoint", value=notebooks_custom_endpoint, expected_type=type_hints["notebooks_custom_endpoint"])
            check_type(argname="argument oracle_database_custom_endpoint", value=oracle_database_custom_endpoint, expected_type=type_hints["oracle_database_custom_endpoint"])
            check_type(argname="argument org_policy_custom_endpoint", value=org_policy_custom_endpoint, expected_type=type_hints["org_policy_custom_endpoint"])
            check_type(argname="argument os_config_custom_endpoint", value=os_config_custom_endpoint, expected_type=type_hints["os_config_custom_endpoint"])
            check_type(argname="argument os_config_v2_custom_endpoint", value=os_config_v2_custom_endpoint, expected_type=type_hints["os_config_v2_custom_endpoint"])
            check_type(argname="argument os_login_custom_endpoint", value=os_login_custom_endpoint, expected_type=type_hints["os_login_custom_endpoint"])
            check_type(argname="argument parallelstore_custom_endpoint", value=parallelstore_custom_endpoint, expected_type=type_hints["parallelstore_custom_endpoint"])
            check_type(argname="argument parameter_manager_custom_endpoint", value=parameter_manager_custom_endpoint, expected_type=type_hints["parameter_manager_custom_endpoint"])
            check_type(argname="argument parameter_manager_regional_custom_endpoint", value=parameter_manager_regional_custom_endpoint, expected_type=type_hints["parameter_manager_regional_custom_endpoint"])
            check_type(argname="argument privateca_custom_endpoint", value=privateca_custom_endpoint, expected_type=type_hints["privateca_custom_endpoint"])
            check_type(argname="argument privileged_access_manager_custom_endpoint", value=privileged_access_manager_custom_endpoint, expected_type=type_hints["privileged_access_manager_custom_endpoint"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument public_ca_custom_endpoint", value=public_ca_custom_endpoint, expected_type=type_hints["public_ca_custom_endpoint"])
            check_type(argname="argument pubsub_custom_endpoint", value=pubsub_custom_endpoint, expected_type=type_hints["pubsub_custom_endpoint"])
            check_type(argname="argument pubsub_lite_custom_endpoint", value=pubsub_lite_custom_endpoint, expected_type=type_hints["pubsub_lite_custom_endpoint"])
            check_type(argname="argument recaptcha_enterprise_custom_endpoint", value=recaptcha_enterprise_custom_endpoint, expected_type=type_hints["recaptcha_enterprise_custom_endpoint"])
            check_type(argname="argument redis_custom_endpoint", value=redis_custom_endpoint, expected_type=type_hints["redis_custom_endpoint"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument request_reason", value=request_reason, expected_type=type_hints["request_reason"])
            check_type(argname="argument request_timeout", value=request_timeout, expected_type=type_hints["request_timeout"])
            check_type(argname="argument resource_manager3_custom_endpoint", value=resource_manager3_custom_endpoint, expected_type=type_hints["resource_manager3_custom_endpoint"])
            check_type(argname="argument resource_manager_custom_endpoint", value=resource_manager_custom_endpoint, expected_type=type_hints["resource_manager_custom_endpoint"])
            check_type(argname="argument resource_manager_v3_custom_endpoint", value=resource_manager_v3_custom_endpoint, expected_type=type_hints["resource_manager_v3_custom_endpoint"])
            check_type(argname="argument runtimeconfig_custom_endpoint", value=runtimeconfig_custom_endpoint, expected_type=type_hints["runtimeconfig_custom_endpoint"])
            check_type(argname="argument runtime_config_custom_endpoint", value=runtime_config_custom_endpoint, expected_type=type_hints["runtime_config_custom_endpoint"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument secret_manager_custom_endpoint", value=secret_manager_custom_endpoint, expected_type=type_hints["secret_manager_custom_endpoint"])
            check_type(argname="argument secret_manager_regional_custom_endpoint", value=secret_manager_regional_custom_endpoint, expected_type=type_hints["secret_manager_regional_custom_endpoint"])
            check_type(argname="argument secure_source_manager_custom_endpoint", value=secure_source_manager_custom_endpoint, expected_type=type_hints["secure_source_manager_custom_endpoint"])
            check_type(argname="argument security_center_custom_endpoint", value=security_center_custom_endpoint, expected_type=type_hints["security_center_custom_endpoint"])
            check_type(argname="argument security_center_management_custom_endpoint", value=security_center_management_custom_endpoint, expected_type=type_hints["security_center_management_custom_endpoint"])
            check_type(argname="argument security_center_v2_custom_endpoint", value=security_center_v2_custom_endpoint, expected_type=type_hints["security_center_v2_custom_endpoint"])
            check_type(argname="argument securityposture_custom_endpoint", value=securityposture_custom_endpoint, expected_type=type_hints["securityposture_custom_endpoint"])
            check_type(argname="argument security_scanner_custom_endpoint", value=security_scanner_custom_endpoint, expected_type=type_hints["security_scanner_custom_endpoint"])
            check_type(argname="argument service_directory_custom_endpoint", value=service_directory_custom_endpoint, expected_type=type_hints["service_directory_custom_endpoint"])
            check_type(argname="argument service_management_custom_endpoint", value=service_management_custom_endpoint, expected_type=type_hints["service_management_custom_endpoint"])
            check_type(argname="argument service_networking_custom_endpoint", value=service_networking_custom_endpoint, expected_type=type_hints["service_networking_custom_endpoint"])
            check_type(argname="argument service_usage_custom_endpoint", value=service_usage_custom_endpoint, expected_type=type_hints["service_usage_custom_endpoint"])
            check_type(argname="argument site_verification_custom_endpoint", value=site_verification_custom_endpoint, expected_type=type_hints["site_verification_custom_endpoint"])
            check_type(argname="argument source_repo_custom_endpoint", value=source_repo_custom_endpoint, expected_type=type_hints["source_repo_custom_endpoint"])
            check_type(argname="argument spanner_custom_endpoint", value=spanner_custom_endpoint, expected_type=type_hints["spanner_custom_endpoint"])
            check_type(argname="argument sql_custom_endpoint", value=sql_custom_endpoint, expected_type=type_hints["sql_custom_endpoint"])
            check_type(argname="argument storage_batch_operations_custom_endpoint", value=storage_batch_operations_custom_endpoint, expected_type=type_hints["storage_batch_operations_custom_endpoint"])
            check_type(argname="argument storage_control_custom_endpoint", value=storage_control_custom_endpoint, expected_type=type_hints["storage_control_custom_endpoint"])
            check_type(argname="argument storage_custom_endpoint", value=storage_custom_endpoint, expected_type=type_hints["storage_custom_endpoint"])
            check_type(argname="argument storage_insights_custom_endpoint", value=storage_insights_custom_endpoint, expected_type=type_hints["storage_insights_custom_endpoint"])
            check_type(argname="argument storage_transfer_custom_endpoint", value=storage_transfer_custom_endpoint, expected_type=type_hints["storage_transfer_custom_endpoint"])
            check_type(argname="argument tags_custom_endpoint", value=tags_custom_endpoint, expected_type=type_hints["tags_custom_endpoint"])
            check_type(argname="argument tags_location_custom_endpoint", value=tags_location_custom_endpoint, expected_type=type_hints["tags_location_custom_endpoint"])
            check_type(argname="argument terraform_attribution_label_addition_strategy", value=terraform_attribution_label_addition_strategy, expected_type=type_hints["terraform_attribution_label_addition_strategy"])
            check_type(argname="argument tpu_custom_endpoint", value=tpu_custom_endpoint, expected_type=type_hints["tpu_custom_endpoint"])
            check_type(argname="argument tpu_v2_custom_endpoint", value=tpu_v2_custom_endpoint, expected_type=type_hints["tpu_v2_custom_endpoint"])
            check_type(argname="argument transcoder_custom_endpoint", value=transcoder_custom_endpoint, expected_type=type_hints["transcoder_custom_endpoint"])
            check_type(argname="argument universe_domain", value=universe_domain, expected_type=type_hints["universe_domain"])
            check_type(argname="argument user_project_override", value=user_project_override, expected_type=type_hints["user_project_override"])
            check_type(argname="argument vertex_ai_custom_endpoint", value=vertex_ai_custom_endpoint, expected_type=type_hints["vertex_ai_custom_endpoint"])
            check_type(argname="argument vmwareengine_custom_endpoint", value=vmwareengine_custom_endpoint, expected_type=type_hints["vmwareengine_custom_endpoint"])
            check_type(argname="argument vpc_access_custom_endpoint", value=vpc_access_custom_endpoint, expected_type=type_hints["vpc_access_custom_endpoint"])
            check_type(argname="argument workbench_custom_endpoint", value=workbench_custom_endpoint, expected_type=type_hints["workbench_custom_endpoint"])
            check_type(argname="argument workflows_custom_endpoint", value=workflows_custom_endpoint, expected_type=type_hints["workflows_custom_endpoint"])
            check_type(argname="argument workstations_custom_endpoint", value=workstations_custom_endpoint, expected_type=type_hints["workstations_custom_endpoint"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_approval_custom_endpoint is not None:
            self._values["access_approval_custom_endpoint"] = access_approval_custom_endpoint
        if access_context_manager_custom_endpoint is not None:
            self._values["access_context_manager_custom_endpoint"] = access_context_manager_custom_endpoint
        if access_token is not None:
            self._values["access_token"] = access_token
        if active_directory_custom_endpoint is not None:
            self._values["active_directory_custom_endpoint"] = active_directory_custom_endpoint
        if add_terraform_attribution_label is not None:
            self._values["add_terraform_attribution_label"] = add_terraform_attribution_label
        if alias is not None:
            self._values["alias"] = alias
        if alloydb_custom_endpoint is not None:
            self._values["alloydb_custom_endpoint"] = alloydb_custom_endpoint
        if api_gateway_custom_endpoint is not None:
            self._values["api_gateway_custom_endpoint"] = api_gateway_custom_endpoint
        if apigee_custom_endpoint is not None:
            self._values["apigee_custom_endpoint"] = apigee_custom_endpoint
        if apihub_custom_endpoint is not None:
            self._values["apihub_custom_endpoint"] = apihub_custom_endpoint
        if apikeys_custom_endpoint is not None:
            self._values["apikeys_custom_endpoint"] = apikeys_custom_endpoint
        if app_engine_custom_endpoint is not None:
            self._values["app_engine_custom_endpoint"] = app_engine_custom_endpoint
        if apphub_custom_endpoint is not None:
            self._values["apphub_custom_endpoint"] = apphub_custom_endpoint
        if artifact_registry_custom_endpoint is not None:
            self._values["artifact_registry_custom_endpoint"] = artifact_registry_custom_endpoint
        if assured_workloads_custom_endpoint is not None:
            self._values["assured_workloads_custom_endpoint"] = assured_workloads_custom_endpoint
        if backup_dr_custom_endpoint is not None:
            self._values["backup_dr_custom_endpoint"] = backup_dr_custom_endpoint
        if batching is not None:
            self._values["batching"] = batching
        if beyondcorp_custom_endpoint is not None:
            self._values["beyondcorp_custom_endpoint"] = beyondcorp_custom_endpoint
        if biglake_custom_endpoint is not None:
            self._values["biglake_custom_endpoint"] = biglake_custom_endpoint
        if bigquery_analytics_hub_custom_endpoint is not None:
            self._values["bigquery_analytics_hub_custom_endpoint"] = bigquery_analytics_hub_custom_endpoint
        if bigquery_connection_custom_endpoint is not None:
            self._values["bigquery_connection_custom_endpoint"] = bigquery_connection_custom_endpoint
        if big_query_custom_endpoint is not None:
            self._values["big_query_custom_endpoint"] = big_query_custom_endpoint
        if bigquery_datapolicy_custom_endpoint is not None:
            self._values["bigquery_datapolicy_custom_endpoint"] = bigquery_datapolicy_custom_endpoint
        if bigquery_data_transfer_custom_endpoint is not None:
            self._values["bigquery_data_transfer_custom_endpoint"] = bigquery_data_transfer_custom_endpoint
        if bigquery_reservation_custom_endpoint is not None:
            self._values["bigquery_reservation_custom_endpoint"] = bigquery_reservation_custom_endpoint
        if bigtable_custom_endpoint is not None:
            self._values["bigtable_custom_endpoint"] = bigtable_custom_endpoint
        if billing_custom_endpoint is not None:
            self._values["billing_custom_endpoint"] = billing_custom_endpoint
        if billing_project is not None:
            self._values["billing_project"] = billing_project
        if binary_authorization_custom_endpoint is not None:
            self._values["binary_authorization_custom_endpoint"] = binary_authorization_custom_endpoint
        if blockchain_node_engine_custom_endpoint is not None:
            self._values["blockchain_node_engine_custom_endpoint"] = blockchain_node_engine_custom_endpoint
        if certificate_manager_custom_endpoint is not None:
            self._values["certificate_manager_custom_endpoint"] = certificate_manager_custom_endpoint
        if chronicle_custom_endpoint is not None:
            self._values["chronicle_custom_endpoint"] = chronicle_custom_endpoint
        if cloud_asset_custom_endpoint is not None:
            self._values["cloud_asset_custom_endpoint"] = cloud_asset_custom_endpoint
        if cloud_billing_custom_endpoint is not None:
            self._values["cloud_billing_custom_endpoint"] = cloud_billing_custom_endpoint
        if cloud_build_custom_endpoint is not None:
            self._values["cloud_build_custom_endpoint"] = cloud_build_custom_endpoint
        if cloudbuildv2_custom_endpoint is not None:
            self._values["cloudbuildv2_custom_endpoint"] = cloudbuildv2_custom_endpoint
        if cloud_build_worker_pool_custom_endpoint is not None:
            self._values["cloud_build_worker_pool_custom_endpoint"] = cloud_build_worker_pool_custom_endpoint
        if clouddeploy_custom_endpoint is not None:
            self._values["clouddeploy_custom_endpoint"] = clouddeploy_custom_endpoint
        if clouddomains_custom_endpoint is not None:
            self._values["clouddomains_custom_endpoint"] = clouddomains_custom_endpoint
        if cloudfunctions2_custom_endpoint is not None:
            self._values["cloudfunctions2_custom_endpoint"] = cloudfunctions2_custom_endpoint
        if cloud_functions_custom_endpoint is not None:
            self._values["cloud_functions_custom_endpoint"] = cloud_functions_custom_endpoint
        if cloud_identity_custom_endpoint is not None:
            self._values["cloud_identity_custom_endpoint"] = cloud_identity_custom_endpoint
        if cloud_ids_custom_endpoint is not None:
            self._values["cloud_ids_custom_endpoint"] = cloud_ids_custom_endpoint
        if cloud_quotas_custom_endpoint is not None:
            self._values["cloud_quotas_custom_endpoint"] = cloud_quotas_custom_endpoint
        if cloud_resource_manager_custom_endpoint is not None:
            self._values["cloud_resource_manager_custom_endpoint"] = cloud_resource_manager_custom_endpoint
        if cloud_run_custom_endpoint is not None:
            self._values["cloud_run_custom_endpoint"] = cloud_run_custom_endpoint
        if cloud_run_v2_custom_endpoint is not None:
            self._values["cloud_run_v2_custom_endpoint"] = cloud_run_v2_custom_endpoint
        if cloud_scheduler_custom_endpoint is not None:
            self._values["cloud_scheduler_custom_endpoint"] = cloud_scheduler_custom_endpoint
        if cloud_tasks_custom_endpoint is not None:
            self._values["cloud_tasks_custom_endpoint"] = cloud_tasks_custom_endpoint
        if colab_custom_endpoint is not None:
            self._values["colab_custom_endpoint"] = colab_custom_endpoint
        if composer_custom_endpoint is not None:
            self._values["composer_custom_endpoint"] = composer_custom_endpoint
        if compute_custom_endpoint is not None:
            self._values["compute_custom_endpoint"] = compute_custom_endpoint
        if container_analysis_custom_endpoint is not None:
            self._values["container_analysis_custom_endpoint"] = container_analysis_custom_endpoint
        if container_attached_custom_endpoint is not None:
            self._values["container_attached_custom_endpoint"] = container_attached_custom_endpoint
        if container_aws_custom_endpoint is not None:
            self._values["container_aws_custom_endpoint"] = container_aws_custom_endpoint
        if container_azure_custom_endpoint is not None:
            self._values["container_azure_custom_endpoint"] = container_azure_custom_endpoint
        if container_custom_endpoint is not None:
            self._values["container_custom_endpoint"] = container_custom_endpoint
        if core_billing_custom_endpoint is not None:
            self._values["core_billing_custom_endpoint"] = core_billing_custom_endpoint
        if credentials is not None:
            self._values["credentials"] = credentials
        if database_migration_service_custom_endpoint is not None:
            self._values["database_migration_service_custom_endpoint"] = database_migration_service_custom_endpoint
        if data_catalog_custom_endpoint is not None:
            self._values["data_catalog_custom_endpoint"] = data_catalog_custom_endpoint
        if dataflow_custom_endpoint is not None:
            self._values["dataflow_custom_endpoint"] = dataflow_custom_endpoint
        if dataform_custom_endpoint is not None:
            self._values["dataform_custom_endpoint"] = dataform_custom_endpoint
        if data_fusion_custom_endpoint is not None:
            self._values["data_fusion_custom_endpoint"] = data_fusion_custom_endpoint
        if data_loss_prevention_custom_endpoint is not None:
            self._values["data_loss_prevention_custom_endpoint"] = data_loss_prevention_custom_endpoint
        if data_pipeline_custom_endpoint is not None:
            self._values["data_pipeline_custom_endpoint"] = data_pipeline_custom_endpoint
        if dataplex_custom_endpoint is not None:
            self._values["dataplex_custom_endpoint"] = dataplex_custom_endpoint
        if dataproc_custom_endpoint is not None:
            self._values["dataproc_custom_endpoint"] = dataproc_custom_endpoint
        if dataproc_gdc_custom_endpoint is not None:
            self._values["dataproc_gdc_custom_endpoint"] = dataproc_gdc_custom_endpoint
        if dataproc_metastore_custom_endpoint is not None:
            self._values["dataproc_metastore_custom_endpoint"] = dataproc_metastore_custom_endpoint
        if datastream_custom_endpoint is not None:
            self._values["datastream_custom_endpoint"] = datastream_custom_endpoint
        if default_labels is not None:
            self._values["default_labels"] = default_labels
        if deployment_manager_custom_endpoint is not None:
            self._values["deployment_manager_custom_endpoint"] = deployment_manager_custom_endpoint
        if developer_connect_custom_endpoint is not None:
            self._values["developer_connect_custom_endpoint"] = developer_connect_custom_endpoint
        if dialogflow_custom_endpoint is not None:
            self._values["dialogflow_custom_endpoint"] = dialogflow_custom_endpoint
        if dialogflow_cx_custom_endpoint is not None:
            self._values["dialogflow_cx_custom_endpoint"] = dialogflow_cx_custom_endpoint
        if discovery_engine_custom_endpoint is not None:
            self._values["discovery_engine_custom_endpoint"] = discovery_engine_custom_endpoint
        if dns_custom_endpoint is not None:
            self._values["dns_custom_endpoint"] = dns_custom_endpoint
        if document_ai_custom_endpoint is not None:
            self._values["document_ai_custom_endpoint"] = document_ai_custom_endpoint
        if document_ai_warehouse_custom_endpoint is not None:
            self._values["document_ai_warehouse_custom_endpoint"] = document_ai_warehouse_custom_endpoint
        if edgecontainer_custom_endpoint is not None:
            self._values["edgecontainer_custom_endpoint"] = edgecontainer_custom_endpoint
        if edgenetwork_custom_endpoint is not None:
            self._values["edgenetwork_custom_endpoint"] = edgenetwork_custom_endpoint
        if essential_contacts_custom_endpoint is not None:
            self._values["essential_contacts_custom_endpoint"] = essential_contacts_custom_endpoint
        if eventarc_custom_endpoint is not None:
            self._values["eventarc_custom_endpoint"] = eventarc_custom_endpoint
        if external_credentials is not None:
            self._values["external_credentials"] = external_credentials
        if filestore_custom_endpoint is not None:
            self._values["filestore_custom_endpoint"] = filestore_custom_endpoint
        if firebase_app_check_custom_endpoint is not None:
            self._values["firebase_app_check_custom_endpoint"] = firebase_app_check_custom_endpoint
        if firebase_app_hosting_custom_endpoint is not None:
            self._values["firebase_app_hosting_custom_endpoint"] = firebase_app_hosting_custom_endpoint
        if firebase_custom_endpoint is not None:
            self._values["firebase_custom_endpoint"] = firebase_custom_endpoint
        if firebase_database_custom_endpoint is not None:
            self._values["firebase_database_custom_endpoint"] = firebase_database_custom_endpoint
        if firebase_data_connect_custom_endpoint is not None:
            self._values["firebase_data_connect_custom_endpoint"] = firebase_data_connect_custom_endpoint
        if firebase_extensions_custom_endpoint is not None:
            self._values["firebase_extensions_custom_endpoint"] = firebase_extensions_custom_endpoint
        if firebase_hosting_custom_endpoint is not None:
            self._values["firebase_hosting_custom_endpoint"] = firebase_hosting_custom_endpoint
        if firebaserules_custom_endpoint is not None:
            self._values["firebaserules_custom_endpoint"] = firebaserules_custom_endpoint
        if firebase_storage_custom_endpoint is not None:
            self._values["firebase_storage_custom_endpoint"] = firebase_storage_custom_endpoint
        if firestore_custom_endpoint is not None:
            self._values["firestore_custom_endpoint"] = firestore_custom_endpoint
        if gemini_custom_endpoint is not None:
            self._values["gemini_custom_endpoint"] = gemini_custom_endpoint
        if gke_backup_custom_endpoint is not None:
            self._values["gke_backup_custom_endpoint"] = gke_backup_custom_endpoint
        if gke_hub2_custom_endpoint is not None:
            self._values["gke_hub2_custom_endpoint"] = gke_hub2_custom_endpoint
        if gke_hub_custom_endpoint is not None:
            self._values["gke_hub_custom_endpoint"] = gke_hub_custom_endpoint
        if gkehub_feature_custom_endpoint is not None:
            self._values["gkehub_feature_custom_endpoint"] = gkehub_feature_custom_endpoint
        if gkeonprem_custom_endpoint is not None:
            self._values["gkeonprem_custom_endpoint"] = gkeonprem_custom_endpoint
        if healthcare_custom_endpoint is not None:
            self._values["healthcare_custom_endpoint"] = healthcare_custom_endpoint
        if iam2_custom_endpoint is not None:
            self._values["iam2_custom_endpoint"] = iam2_custom_endpoint
        if iam3_custom_endpoint is not None:
            self._values["iam3_custom_endpoint"] = iam3_custom_endpoint
        if iam_beta_custom_endpoint is not None:
            self._values["iam_beta_custom_endpoint"] = iam_beta_custom_endpoint
        if iam_credentials_custom_endpoint is not None:
            self._values["iam_credentials_custom_endpoint"] = iam_credentials_custom_endpoint
        if iam_custom_endpoint is not None:
            self._values["iam_custom_endpoint"] = iam_custom_endpoint
        if iam_workforce_pool_custom_endpoint is not None:
            self._values["iam_workforce_pool_custom_endpoint"] = iam_workforce_pool_custom_endpoint
        if iap_custom_endpoint is not None:
            self._values["iap_custom_endpoint"] = iap_custom_endpoint
        if identity_platform_custom_endpoint is not None:
            self._values["identity_platform_custom_endpoint"] = identity_platform_custom_endpoint
        if impersonate_service_account is not None:
            self._values["impersonate_service_account"] = impersonate_service_account
        if impersonate_service_account_delegates is not None:
            self._values["impersonate_service_account_delegates"] = impersonate_service_account_delegates
        if integration_connectors_custom_endpoint is not None:
            self._values["integration_connectors_custom_endpoint"] = integration_connectors_custom_endpoint
        if integrations_custom_endpoint is not None:
            self._values["integrations_custom_endpoint"] = integrations_custom_endpoint
        if kms_custom_endpoint is not None:
            self._values["kms_custom_endpoint"] = kms_custom_endpoint
        if logging_custom_endpoint is not None:
            self._values["logging_custom_endpoint"] = logging_custom_endpoint
        if looker_custom_endpoint is not None:
            self._values["looker_custom_endpoint"] = looker_custom_endpoint
        if lustre_custom_endpoint is not None:
            self._values["lustre_custom_endpoint"] = lustre_custom_endpoint
        if managed_kafka_custom_endpoint is not None:
            self._values["managed_kafka_custom_endpoint"] = managed_kafka_custom_endpoint
        if memcache_custom_endpoint is not None:
            self._values["memcache_custom_endpoint"] = memcache_custom_endpoint
        if memorystore_custom_endpoint is not None:
            self._values["memorystore_custom_endpoint"] = memorystore_custom_endpoint
        if migration_center_custom_endpoint is not None:
            self._values["migration_center_custom_endpoint"] = migration_center_custom_endpoint
        if ml_engine_custom_endpoint is not None:
            self._values["ml_engine_custom_endpoint"] = ml_engine_custom_endpoint
        if monitoring_custom_endpoint is not None:
            self._values["monitoring_custom_endpoint"] = monitoring_custom_endpoint
        if netapp_custom_endpoint is not None:
            self._values["netapp_custom_endpoint"] = netapp_custom_endpoint
        if network_connectivity_custom_endpoint is not None:
            self._values["network_connectivity_custom_endpoint"] = network_connectivity_custom_endpoint
        if network_management_custom_endpoint is not None:
            self._values["network_management_custom_endpoint"] = network_management_custom_endpoint
        if network_security_custom_endpoint is not None:
            self._values["network_security_custom_endpoint"] = network_security_custom_endpoint
        if network_services_custom_endpoint is not None:
            self._values["network_services_custom_endpoint"] = network_services_custom_endpoint
        if notebooks_custom_endpoint is not None:
            self._values["notebooks_custom_endpoint"] = notebooks_custom_endpoint
        if oracle_database_custom_endpoint is not None:
            self._values["oracle_database_custom_endpoint"] = oracle_database_custom_endpoint
        if org_policy_custom_endpoint is not None:
            self._values["org_policy_custom_endpoint"] = org_policy_custom_endpoint
        if os_config_custom_endpoint is not None:
            self._values["os_config_custom_endpoint"] = os_config_custom_endpoint
        if os_config_v2_custom_endpoint is not None:
            self._values["os_config_v2_custom_endpoint"] = os_config_v2_custom_endpoint
        if os_login_custom_endpoint is not None:
            self._values["os_login_custom_endpoint"] = os_login_custom_endpoint
        if parallelstore_custom_endpoint is not None:
            self._values["parallelstore_custom_endpoint"] = parallelstore_custom_endpoint
        if parameter_manager_custom_endpoint is not None:
            self._values["parameter_manager_custom_endpoint"] = parameter_manager_custom_endpoint
        if parameter_manager_regional_custom_endpoint is not None:
            self._values["parameter_manager_regional_custom_endpoint"] = parameter_manager_regional_custom_endpoint
        if privateca_custom_endpoint is not None:
            self._values["privateca_custom_endpoint"] = privateca_custom_endpoint
        if privileged_access_manager_custom_endpoint is not None:
            self._values["privileged_access_manager_custom_endpoint"] = privileged_access_manager_custom_endpoint
        if project is not None:
            self._values["project"] = project
        if public_ca_custom_endpoint is not None:
            self._values["public_ca_custom_endpoint"] = public_ca_custom_endpoint
        if pubsub_custom_endpoint is not None:
            self._values["pubsub_custom_endpoint"] = pubsub_custom_endpoint
        if pubsub_lite_custom_endpoint is not None:
            self._values["pubsub_lite_custom_endpoint"] = pubsub_lite_custom_endpoint
        if recaptcha_enterprise_custom_endpoint is not None:
            self._values["recaptcha_enterprise_custom_endpoint"] = recaptcha_enterprise_custom_endpoint
        if redis_custom_endpoint is not None:
            self._values["redis_custom_endpoint"] = redis_custom_endpoint
        if region is not None:
            self._values["region"] = region
        if request_reason is not None:
            self._values["request_reason"] = request_reason
        if request_timeout is not None:
            self._values["request_timeout"] = request_timeout
        if resource_manager3_custom_endpoint is not None:
            self._values["resource_manager3_custom_endpoint"] = resource_manager3_custom_endpoint
        if resource_manager_custom_endpoint is not None:
            self._values["resource_manager_custom_endpoint"] = resource_manager_custom_endpoint
        if resource_manager_v3_custom_endpoint is not None:
            self._values["resource_manager_v3_custom_endpoint"] = resource_manager_v3_custom_endpoint
        if runtimeconfig_custom_endpoint is not None:
            self._values["runtimeconfig_custom_endpoint"] = runtimeconfig_custom_endpoint
        if runtime_config_custom_endpoint is not None:
            self._values["runtime_config_custom_endpoint"] = runtime_config_custom_endpoint
        if scopes is not None:
            self._values["scopes"] = scopes
        if secret_manager_custom_endpoint is not None:
            self._values["secret_manager_custom_endpoint"] = secret_manager_custom_endpoint
        if secret_manager_regional_custom_endpoint is not None:
            self._values["secret_manager_regional_custom_endpoint"] = secret_manager_regional_custom_endpoint
        if secure_source_manager_custom_endpoint is not None:
            self._values["secure_source_manager_custom_endpoint"] = secure_source_manager_custom_endpoint
        if security_center_custom_endpoint is not None:
            self._values["security_center_custom_endpoint"] = security_center_custom_endpoint
        if security_center_management_custom_endpoint is not None:
            self._values["security_center_management_custom_endpoint"] = security_center_management_custom_endpoint
        if security_center_v2_custom_endpoint is not None:
            self._values["security_center_v2_custom_endpoint"] = security_center_v2_custom_endpoint
        if securityposture_custom_endpoint is not None:
            self._values["securityposture_custom_endpoint"] = securityposture_custom_endpoint
        if security_scanner_custom_endpoint is not None:
            self._values["security_scanner_custom_endpoint"] = security_scanner_custom_endpoint
        if service_directory_custom_endpoint is not None:
            self._values["service_directory_custom_endpoint"] = service_directory_custom_endpoint
        if service_management_custom_endpoint is not None:
            self._values["service_management_custom_endpoint"] = service_management_custom_endpoint
        if service_networking_custom_endpoint is not None:
            self._values["service_networking_custom_endpoint"] = service_networking_custom_endpoint
        if service_usage_custom_endpoint is not None:
            self._values["service_usage_custom_endpoint"] = service_usage_custom_endpoint
        if site_verification_custom_endpoint is not None:
            self._values["site_verification_custom_endpoint"] = site_verification_custom_endpoint
        if source_repo_custom_endpoint is not None:
            self._values["source_repo_custom_endpoint"] = source_repo_custom_endpoint
        if spanner_custom_endpoint is not None:
            self._values["spanner_custom_endpoint"] = spanner_custom_endpoint
        if sql_custom_endpoint is not None:
            self._values["sql_custom_endpoint"] = sql_custom_endpoint
        if storage_batch_operations_custom_endpoint is not None:
            self._values["storage_batch_operations_custom_endpoint"] = storage_batch_operations_custom_endpoint
        if storage_control_custom_endpoint is not None:
            self._values["storage_control_custom_endpoint"] = storage_control_custom_endpoint
        if storage_custom_endpoint is not None:
            self._values["storage_custom_endpoint"] = storage_custom_endpoint
        if storage_insights_custom_endpoint is not None:
            self._values["storage_insights_custom_endpoint"] = storage_insights_custom_endpoint
        if storage_transfer_custom_endpoint is not None:
            self._values["storage_transfer_custom_endpoint"] = storage_transfer_custom_endpoint
        if tags_custom_endpoint is not None:
            self._values["tags_custom_endpoint"] = tags_custom_endpoint
        if tags_location_custom_endpoint is not None:
            self._values["tags_location_custom_endpoint"] = tags_location_custom_endpoint
        if terraform_attribution_label_addition_strategy is not None:
            self._values["terraform_attribution_label_addition_strategy"] = terraform_attribution_label_addition_strategy
        if tpu_custom_endpoint is not None:
            self._values["tpu_custom_endpoint"] = tpu_custom_endpoint
        if tpu_v2_custom_endpoint is not None:
            self._values["tpu_v2_custom_endpoint"] = tpu_v2_custom_endpoint
        if transcoder_custom_endpoint is not None:
            self._values["transcoder_custom_endpoint"] = transcoder_custom_endpoint
        if universe_domain is not None:
            self._values["universe_domain"] = universe_domain
        if user_project_override is not None:
            self._values["user_project_override"] = user_project_override
        if vertex_ai_custom_endpoint is not None:
            self._values["vertex_ai_custom_endpoint"] = vertex_ai_custom_endpoint
        if vmwareengine_custom_endpoint is not None:
            self._values["vmwareengine_custom_endpoint"] = vmwareengine_custom_endpoint
        if vpc_access_custom_endpoint is not None:
            self._values["vpc_access_custom_endpoint"] = vpc_access_custom_endpoint
        if workbench_custom_endpoint is not None:
            self._values["workbench_custom_endpoint"] = workbench_custom_endpoint
        if workflows_custom_endpoint is not None:
            self._values["workflows_custom_endpoint"] = workflows_custom_endpoint
        if workstations_custom_endpoint is not None:
            self._values["workstations_custom_endpoint"] = workstations_custom_endpoint
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def access_approval_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#access_approval_custom_endpoint GoogleBetaProvider#access_approval_custom_endpoint}.'''
        result = self._values.get("access_approval_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_context_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#access_context_manager_custom_endpoint GoogleBetaProvider#access_context_manager_custom_endpoint}.'''
        result = self._values.get("access_context_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#access_token GoogleBetaProvider#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def active_directory_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#active_directory_custom_endpoint GoogleBetaProvider#active_directory_custom_endpoint}.'''
        result = self._values.get("active_directory_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def add_terraform_attribution_label(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#add_terraform_attribution_label GoogleBetaProvider#add_terraform_attribution_label}.'''
        result = self._values.get("add_terraform_attribution_label")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#alias GoogleBetaProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alloydb_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#alloydb_custom_endpoint GoogleBetaProvider#alloydb_custom_endpoint}.'''
        result = self._values.get("alloydb_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_gateway_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#api_gateway_custom_endpoint GoogleBetaProvider#api_gateway_custom_endpoint}.'''
        result = self._values.get("api_gateway_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apigee_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apigee_custom_endpoint GoogleBetaProvider#apigee_custom_endpoint}.'''
        result = self._values.get("apigee_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apihub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apihub_custom_endpoint GoogleBetaProvider#apihub_custom_endpoint}.'''
        result = self._values.get("apihub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apikeys_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apikeys_custom_endpoint GoogleBetaProvider#apikeys_custom_endpoint}.'''
        result = self._values.get("apikeys_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#app_engine_custom_endpoint GoogleBetaProvider#app_engine_custom_endpoint}.'''
        result = self._values.get("app_engine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apphub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#apphub_custom_endpoint GoogleBetaProvider#apphub_custom_endpoint}.'''
        result = self._values.get("apphub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def artifact_registry_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#artifact_registry_custom_endpoint GoogleBetaProvider#artifact_registry_custom_endpoint}.'''
        result = self._values.get("artifact_registry_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assured_workloads_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#assured_workloads_custom_endpoint GoogleBetaProvider#assured_workloads_custom_endpoint}.'''
        result = self._values.get("assured_workloads_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_dr_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#backup_dr_custom_endpoint GoogleBetaProvider#backup_dr_custom_endpoint}.'''
        result = self._values.get("backup_dr_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def batching(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBetaProviderBatching]]]:
        '''batching block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#batching GoogleBetaProvider#batching}
        '''
        result = self._values.get("batching")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBetaProviderBatching]]], result)

    @builtins.property
    def beyondcorp_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#beyondcorp_custom_endpoint GoogleBetaProvider#beyondcorp_custom_endpoint}.'''
        result = self._values.get("beyondcorp_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def biglake_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#biglake_custom_endpoint GoogleBetaProvider#biglake_custom_endpoint}.'''
        result = self._values.get("biglake_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_analytics_hub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_analytics_hub_custom_endpoint GoogleBetaProvider#bigquery_analytics_hub_custom_endpoint}.'''
        result = self._values.get("bigquery_analytics_hub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_connection_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_connection_custom_endpoint GoogleBetaProvider#bigquery_connection_custom_endpoint}.'''
        result = self._values.get("bigquery_connection_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def big_query_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#big_query_custom_endpoint GoogleBetaProvider#big_query_custom_endpoint}.'''
        result = self._values.get("big_query_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_datapolicy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_datapolicy_custom_endpoint GoogleBetaProvider#bigquery_datapolicy_custom_endpoint}.'''
        result = self._values.get("bigquery_datapolicy_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_data_transfer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_data_transfer_custom_endpoint GoogleBetaProvider#bigquery_data_transfer_custom_endpoint}.'''
        result = self._values.get("bigquery_data_transfer_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_reservation_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigquery_reservation_custom_endpoint GoogleBetaProvider#bigquery_reservation_custom_endpoint}.'''
        result = self._values.get("bigquery_reservation_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigtable_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#bigtable_custom_endpoint GoogleBetaProvider#bigtable_custom_endpoint}.'''
        result = self._values.get("bigtable_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#billing_custom_endpoint GoogleBetaProvider#billing_custom_endpoint}.'''
        result = self._values.get("billing_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#billing_project GoogleBetaProvider#billing_project}.'''
        result = self._values.get("billing_project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_authorization_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#binary_authorization_custom_endpoint GoogleBetaProvider#binary_authorization_custom_endpoint}.'''
        result = self._values.get("binary_authorization_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def blockchain_node_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#blockchain_node_engine_custom_endpoint GoogleBetaProvider#blockchain_node_engine_custom_endpoint}.'''
        result = self._values.get("blockchain_node_engine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#certificate_manager_custom_endpoint GoogleBetaProvider#certificate_manager_custom_endpoint}.'''
        result = self._values.get("certificate_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chronicle_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#chronicle_custom_endpoint GoogleBetaProvider#chronicle_custom_endpoint}.'''
        result = self._values.get("chronicle_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_asset_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_asset_custom_endpoint GoogleBetaProvider#cloud_asset_custom_endpoint}.'''
        result = self._values.get("cloud_asset_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_billing_custom_endpoint GoogleBetaProvider#cloud_billing_custom_endpoint}.'''
        result = self._values.get("cloud_billing_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_build_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_build_custom_endpoint GoogleBetaProvider#cloud_build_custom_endpoint}.'''
        result = self._values.get("cloud_build_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudbuildv2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloudbuildv2_custom_endpoint GoogleBetaProvider#cloudbuildv2_custom_endpoint}.'''
        result = self._values.get("cloudbuildv2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_build_worker_pool_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_build_worker_pool_custom_endpoint GoogleBetaProvider#cloud_build_worker_pool_custom_endpoint}.'''
        result = self._values.get("cloud_build_worker_pool_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clouddeploy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#clouddeploy_custom_endpoint GoogleBetaProvider#clouddeploy_custom_endpoint}.'''
        result = self._values.get("clouddeploy_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clouddomains_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#clouddomains_custom_endpoint GoogleBetaProvider#clouddomains_custom_endpoint}.'''
        result = self._values.get("clouddomains_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfunctions2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloudfunctions2_custom_endpoint GoogleBetaProvider#cloudfunctions2_custom_endpoint}.'''
        result = self._values.get("cloudfunctions2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_functions_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_functions_custom_endpoint GoogleBetaProvider#cloud_functions_custom_endpoint}.'''
        result = self._values.get("cloud_functions_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_identity_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_identity_custom_endpoint GoogleBetaProvider#cloud_identity_custom_endpoint}.'''
        result = self._values.get("cloud_identity_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_ids_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_ids_custom_endpoint GoogleBetaProvider#cloud_ids_custom_endpoint}.'''
        result = self._values.get("cloud_ids_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_quotas_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_quotas_custom_endpoint GoogleBetaProvider#cloud_quotas_custom_endpoint}.'''
        result = self._values.get("cloud_quotas_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_resource_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_resource_manager_custom_endpoint GoogleBetaProvider#cloud_resource_manager_custom_endpoint}.'''
        result = self._values.get("cloud_resource_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_run_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_run_custom_endpoint GoogleBetaProvider#cloud_run_custom_endpoint}.'''
        result = self._values.get("cloud_run_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_run_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_run_v2_custom_endpoint GoogleBetaProvider#cloud_run_v2_custom_endpoint}.'''
        result = self._values.get("cloud_run_v2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_scheduler_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_scheduler_custom_endpoint GoogleBetaProvider#cloud_scheduler_custom_endpoint}.'''
        result = self._values.get("cloud_scheduler_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_tasks_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#cloud_tasks_custom_endpoint GoogleBetaProvider#cloud_tasks_custom_endpoint}.'''
        result = self._values.get("cloud_tasks_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def colab_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#colab_custom_endpoint GoogleBetaProvider#colab_custom_endpoint}.'''
        result = self._values.get("colab_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def composer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#composer_custom_endpoint GoogleBetaProvider#composer_custom_endpoint}.'''
        result = self._values.get("composer_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#compute_custom_endpoint GoogleBetaProvider#compute_custom_endpoint}.'''
        result = self._values.get("compute_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_analysis_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_analysis_custom_endpoint GoogleBetaProvider#container_analysis_custom_endpoint}.'''
        result = self._values.get("container_analysis_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_attached_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_attached_custom_endpoint GoogleBetaProvider#container_attached_custom_endpoint}.'''
        result = self._values.get("container_attached_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_aws_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_aws_custom_endpoint GoogleBetaProvider#container_aws_custom_endpoint}.'''
        result = self._values.get("container_aws_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_azure_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_azure_custom_endpoint GoogleBetaProvider#container_azure_custom_endpoint}.'''
        result = self._values.get("container_azure_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#container_custom_endpoint GoogleBetaProvider#container_custom_endpoint}.'''
        result = self._values.get("container_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def core_billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#core_billing_custom_endpoint GoogleBetaProvider#core_billing_custom_endpoint}.'''
        result = self._values.get("core_billing_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#credentials GoogleBetaProvider#credentials}.'''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_migration_service_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#database_migration_service_custom_endpoint GoogleBetaProvider#database_migration_service_custom_endpoint}.'''
        result = self._values.get("database_migration_service_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_catalog_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_catalog_custom_endpoint GoogleBetaProvider#data_catalog_custom_endpoint}.'''
        result = self._values.get("data_catalog_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataflow_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataflow_custom_endpoint GoogleBetaProvider#dataflow_custom_endpoint}.'''
        result = self._values.get("dataflow_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataform_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataform_custom_endpoint GoogleBetaProvider#dataform_custom_endpoint}.'''
        result = self._values.get("dataform_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_fusion_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_fusion_custom_endpoint GoogleBetaProvider#data_fusion_custom_endpoint}.'''
        result = self._values.get("data_fusion_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_loss_prevention_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_loss_prevention_custom_endpoint GoogleBetaProvider#data_loss_prevention_custom_endpoint}.'''
        result = self._values.get("data_loss_prevention_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_pipeline_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#data_pipeline_custom_endpoint GoogleBetaProvider#data_pipeline_custom_endpoint}.'''
        result = self._values.get("data_pipeline_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataplex_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataplex_custom_endpoint GoogleBetaProvider#dataplex_custom_endpoint}.'''
        result = self._values.get("dataplex_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataproc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataproc_custom_endpoint GoogleBetaProvider#dataproc_custom_endpoint}.'''
        result = self._values.get("dataproc_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataproc_gdc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataproc_gdc_custom_endpoint GoogleBetaProvider#dataproc_gdc_custom_endpoint}.'''
        result = self._values.get("dataproc_gdc_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataproc_metastore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dataproc_metastore_custom_endpoint GoogleBetaProvider#dataproc_metastore_custom_endpoint}.'''
        result = self._values.get("dataproc_metastore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datastream_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#datastream_custom_endpoint GoogleBetaProvider#datastream_custom_endpoint}.'''
        result = self._values.get("datastream_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#default_labels GoogleBetaProvider#default_labels}.'''
        result = self._values.get("default_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def deployment_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#deployment_manager_custom_endpoint GoogleBetaProvider#deployment_manager_custom_endpoint}.'''
        result = self._values.get("deployment_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def developer_connect_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#developer_connect_custom_endpoint GoogleBetaProvider#developer_connect_custom_endpoint}.'''
        result = self._values.get("developer_connect_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dialogflow_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dialogflow_custom_endpoint GoogleBetaProvider#dialogflow_custom_endpoint}.'''
        result = self._values.get("dialogflow_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dialogflow_cx_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dialogflow_cx_custom_endpoint GoogleBetaProvider#dialogflow_cx_custom_endpoint}.'''
        result = self._values.get("dialogflow_cx_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def discovery_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#discovery_engine_custom_endpoint GoogleBetaProvider#discovery_engine_custom_endpoint}.'''
        result = self._values.get("discovery_engine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#dns_custom_endpoint GoogleBetaProvider#dns_custom_endpoint}.'''
        result = self._values.get("dns_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_ai_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#document_ai_custom_endpoint GoogleBetaProvider#document_ai_custom_endpoint}.'''
        result = self._values.get("document_ai_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_ai_warehouse_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#document_ai_warehouse_custom_endpoint GoogleBetaProvider#document_ai_warehouse_custom_endpoint}.'''
        result = self._values.get("document_ai_warehouse_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edgecontainer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#edgecontainer_custom_endpoint GoogleBetaProvider#edgecontainer_custom_endpoint}.'''
        result = self._values.get("edgecontainer_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edgenetwork_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#edgenetwork_custom_endpoint GoogleBetaProvider#edgenetwork_custom_endpoint}.'''
        result = self._values.get("edgenetwork_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def essential_contacts_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#essential_contacts_custom_endpoint GoogleBetaProvider#essential_contacts_custom_endpoint}.'''
        result = self._values.get("essential_contacts_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventarc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#eventarc_custom_endpoint GoogleBetaProvider#eventarc_custom_endpoint}.'''
        result = self._values.get("eventarc_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_credentials(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderExternalCredentials"]]]:
        '''external_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#external_credentials GoogleBetaProvider#external_credentials}
        '''
        result = self._values.get("external_credentials")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBetaProviderExternalCredentials"]]], result)

    @builtins.property
    def filestore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#filestore_custom_endpoint GoogleBetaProvider#filestore_custom_endpoint}.'''
        result = self._values.get("filestore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_app_check_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_app_check_custom_endpoint GoogleBetaProvider#firebase_app_check_custom_endpoint}.'''
        result = self._values.get("firebase_app_check_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_app_hosting_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_app_hosting_custom_endpoint GoogleBetaProvider#firebase_app_hosting_custom_endpoint}.'''
        result = self._values.get("firebase_app_hosting_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_custom_endpoint GoogleBetaProvider#firebase_custom_endpoint}.'''
        result = self._values.get("firebase_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_database_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_database_custom_endpoint GoogleBetaProvider#firebase_database_custom_endpoint}.'''
        result = self._values.get("firebase_database_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_data_connect_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_data_connect_custom_endpoint GoogleBetaProvider#firebase_data_connect_custom_endpoint}.'''
        result = self._values.get("firebase_data_connect_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_extensions_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_extensions_custom_endpoint GoogleBetaProvider#firebase_extensions_custom_endpoint}.'''
        result = self._values.get("firebase_extensions_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_hosting_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_hosting_custom_endpoint GoogleBetaProvider#firebase_hosting_custom_endpoint}.'''
        result = self._values.get("firebase_hosting_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebaserules_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebaserules_custom_endpoint GoogleBetaProvider#firebaserules_custom_endpoint}.'''
        result = self._values.get("firebaserules_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_storage_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firebase_storage_custom_endpoint GoogleBetaProvider#firebase_storage_custom_endpoint}.'''
        result = self._values.get("firebase_storage_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firestore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#firestore_custom_endpoint GoogleBetaProvider#firestore_custom_endpoint}.'''
        result = self._values.get("firestore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gemini_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gemini_custom_endpoint GoogleBetaProvider#gemini_custom_endpoint}.'''
        result = self._values.get("gemini_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gke_backup_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gke_backup_custom_endpoint GoogleBetaProvider#gke_backup_custom_endpoint}.'''
        result = self._values.get("gke_backup_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gke_hub2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gke_hub2_custom_endpoint GoogleBetaProvider#gke_hub2_custom_endpoint}.'''
        result = self._values.get("gke_hub2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gke_hub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gke_hub_custom_endpoint GoogleBetaProvider#gke_hub_custom_endpoint}.'''
        result = self._values.get("gke_hub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gkehub_feature_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gkehub_feature_custom_endpoint GoogleBetaProvider#gkehub_feature_custom_endpoint}.'''
        result = self._values.get("gkehub_feature_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gkeonprem_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#gkeonprem_custom_endpoint GoogleBetaProvider#gkeonprem_custom_endpoint}.'''
        result = self._values.get("gkeonprem_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def healthcare_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#healthcare_custom_endpoint GoogleBetaProvider#healthcare_custom_endpoint}.'''
        result = self._values.get("healthcare_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam2_custom_endpoint GoogleBetaProvider#iam2_custom_endpoint}.'''
        result = self._values.get("iam2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam3_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam3_custom_endpoint GoogleBetaProvider#iam3_custom_endpoint}.'''
        result = self._values.get("iam3_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_beta_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_beta_custom_endpoint GoogleBetaProvider#iam_beta_custom_endpoint}.'''
        result = self._values.get("iam_beta_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_credentials_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_credentials_custom_endpoint GoogleBetaProvider#iam_credentials_custom_endpoint}.'''
        result = self._values.get("iam_credentials_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_custom_endpoint GoogleBetaProvider#iam_custom_endpoint}.'''
        result = self._values.get("iam_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_workforce_pool_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iam_workforce_pool_custom_endpoint GoogleBetaProvider#iam_workforce_pool_custom_endpoint}.'''
        result = self._values.get("iam_workforce_pool_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iap_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#iap_custom_endpoint GoogleBetaProvider#iap_custom_endpoint}.'''
        result = self._values.get("iap_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_platform_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#identity_platform_custom_endpoint GoogleBetaProvider#identity_platform_custom_endpoint}.'''
        result = self._values.get("identity_platform_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def impersonate_service_account(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#impersonate_service_account GoogleBetaProvider#impersonate_service_account}.'''
        result = self._values.get("impersonate_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def impersonate_service_account_delegates(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#impersonate_service_account_delegates GoogleBetaProvider#impersonate_service_account_delegates}.'''
        result = self._values.get("impersonate_service_account_delegates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def integration_connectors_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#integration_connectors_custom_endpoint GoogleBetaProvider#integration_connectors_custom_endpoint}.'''
        result = self._values.get("integration_connectors_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integrations_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#integrations_custom_endpoint GoogleBetaProvider#integrations_custom_endpoint}.'''
        result = self._values.get("integrations_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#kms_custom_endpoint GoogleBetaProvider#kms_custom_endpoint}.'''
        result = self._values.get("kms_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#logging_custom_endpoint GoogleBetaProvider#logging_custom_endpoint}.'''
        result = self._values.get("logging_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def looker_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#looker_custom_endpoint GoogleBetaProvider#looker_custom_endpoint}.'''
        result = self._values.get("looker_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lustre_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#lustre_custom_endpoint GoogleBetaProvider#lustre_custom_endpoint}.'''
        result = self._values.get("lustre_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_kafka_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#managed_kafka_custom_endpoint GoogleBetaProvider#managed_kafka_custom_endpoint}.'''
        result = self._values.get("managed_kafka_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memcache_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#memcache_custom_endpoint GoogleBetaProvider#memcache_custom_endpoint}.'''
        result = self._values.get("memcache_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memorystore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#memorystore_custom_endpoint GoogleBetaProvider#memorystore_custom_endpoint}.'''
        result = self._values.get("memorystore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def migration_center_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#migration_center_custom_endpoint GoogleBetaProvider#migration_center_custom_endpoint}.'''
        result = self._values.get("migration_center_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ml_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#ml_engine_custom_endpoint GoogleBetaProvider#ml_engine_custom_endpoint}.'''
        result = self._values.get("ml_engine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitoring_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#monitoring_custom_endpoint GoogleBetaProvider#monitoring_custom_endpoint}.'''
        result = self._values.get("monitoring_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netapp_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#netapp_custom_endpoint GoogleBetaProvider#netapp_custom_endpoint}.'''
        result = self._values.get("netapp_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_connectivity_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_connectivity_custom_endpoint GoogleBetaProvider#network_connectivity_custom_endpoint}.'''
        result = self._values.get("network_connectivity_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_management_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_management_custom_endpoint GoogleBetaProvider#network_management_custom_endpoint}.'''
        result = self._values.get("network_management_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_security_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_security_custom_endpoint GoogleBetaProvider#network_security_custom_endpoint}.'''
        result = self._values.get("network_security_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_services_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#network_services_custom_endpoint GoogleBetaProvider#network_services_custom_endpoint}.'''
        result = self._values.get("network_services_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notebooks_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#notebooks_custom_endpoint GoogleBetaProvider#notebooks_custom_endpoint}.'''
        result = self._values.get("notebooks_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oracle_database_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#oracle_database_custom_endpoint GoogleBetaProvider#oracle_database_custom_endpoint}.'''
        result = self._values.get("oracle_database_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org_policy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#org_policy_custom_endpoint GoogleBetaProvider#org_policy_custom_endpoint}.'''
        result = self._values.get("org_policy_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_config_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#os_config_custom_endpoint GoogleBetaProvider#os_config_custom_endpoint}.'''
        result = self._values.get("os_config_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_config_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#os_config_v2_custom_endpoint GoogleBetaProvider#os_config_v2_custom_endpoint}.'''
        result = self._values.get("os_config_v2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_login_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#os_login_custom_endpoint GoogleBetaProvider#os_login_custom_endpoint}.'''
        result = self._values.get("os_login_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelstore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#parallelstore_custom_endpoint GoogleBetaProvider#parallelstore_custom_endpoint}.'''
        result = self._values.get("parallelstore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#parameter_manager_custom_endpoint GoogleBetaProvider#parameter_manager_custom_endpoint}.'''
        result = self._values.get("parameter_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_manager_regional_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#parameter_manager_regional_custom_endpoint GoogleBetaProvider#parameter_manager_regional_custom_endpoint}.'''
        result = self._values.get("parameter_manager_regional_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privateca_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#privateca_custom_endpoint GoogleBetaProvider#privateca_custom_endpoint}.'''
        result = self._values.get("privateca_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privileged_access_manager_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#privileged_access_manager_custom_endpoint GoogleBetaProvider#privileged_access_manager_custom_endpoint}.'''
        result = self._values.get("privileged_access_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#project GoogleBetaProvider#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ca_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#public_ca_custom_endpoint GoogleBetaProvider#public_ca_custom_endpoint}.'''
        result = self._values.get("public_ca_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#pubsub_custom_endpoint GoogleBetaProvider#pubsub_custom_endpoint}.'''
        result = self._values.get("pubsub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_lite_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#pubsub_lite_custom_endpoint GoogleBetaProvider#pubsub_lite_custom_endpoint}.'''
        result = self._values.get("pubsub_lite_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recaptcha_enterprise_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#recaptcha_enterprise_custom_endpoint GoogleBetaProvider#recaptcha_enterprise_custom_endpoint}.'''
        result = self._values.get("recaptcha_enterprise_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#redis_custom_endpoint GoogleBetaProvider#redis_custom_endpoint}.'''
        result = self._values.get("redis_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#region GoogleBetaProvider#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_reason(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#request_reason GoogleBetaProvider#request_reason}.'''
        result = self._values.get("request_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#request_timeout GoogleBetaProvider#request_timeout}.'''
        result = self._values.get("request_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_manager3_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#resource_manager3_custom_endpoint GoogleBetaProvider#resource_manager3_custom_endpoint}.'''
        result = self._values.get("resource_manager3_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#resource_manager_custom_endpoint GoogleBetaProvider#resource_manager_custom_endpoint}.'''
        result = self._values.get("resource_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_manager_v3_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#resource_manager_v3_custom_endpoint GoogleBetaProvider#resource_manager_v3_custom_endpoint}.'''
        result = self._values.get("resource_manager_v3_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtimeconfig_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#runtimeconfig_custom_endpoint GoogleBetaProvider#runtimeconfig_custom_endpoint}.'''
        result = self._values.get("runtimeconfig_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_config_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#runtime_config_custom_endpoint GoogleBetaProvider#runtime_config_custom_endpoint}.'''
        result = self._values.get("runtime_config_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#scopes GoogleBetaProvider#scopes}.'''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#secret_manager_custom_endpoint GoogleBetaProvider#secret_manager_custom_endpoint}.'''
        result = self._values.get("secret_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_manager_regional_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#secret_manager_regional_custom_endpoint GoogleBetaProvider#secret_manager_regional_custom_endpoint}.'''
        result = self._values.get("secret_manager_regional_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secure_source_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#secure_source_manager_custom_endpoint GoogleBetaProvider#secure_source_manager_custom_endpoint}.'''
        result = self._values.get("secure_source_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_center_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_center_custom_endpoint GoogleBetaProvider#security_center_custom_endpoint}.'''
        result = self._values.get("security_center_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_center_management_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_center_management_custom_endpoint GoogleBetaProvider#security_center_management_custom_endpoint}.'''
        result = self._values.get("security_center_management_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_center_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_center_v2_custom_endpoint GoogleBetaProvider#security_center_v2_custom_endpoint}.'''
        result = self._values.get("security_center_v2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def securityposture_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#securityposture_custom_endpoint GoogleBetaProvider#securityposture_custom_endpoint}.'''
        result = self._values.get("securityposture_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_scanner_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#security_scanner_custom_endpoint GoogleBetaProvider#security_scanner_custom_endpoint}.'''
        result = self._values.get("security_scanner_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_directory_custom_endpoint GoogleBetaProvider#service_directory_custom_endpoint}.'''
        result = self._values.get("service_directory_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_management_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_management_custom_endpoint GoogleBetaProvider#service_management_custom_endpoint}.'''
        result = self._values.get("service_management_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_networking_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_networking_custom_endpoint GoogleBetaProvider#service_networking_custom_endpoint}.'''
        result = self._values.get("service_networking_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_usage_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_usage_custom_endpoint GoogleBetaProvider#service_usage_custom_endpoint}.'''
        result = self._values.get("service_usage_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site_verification_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#site_verification_custom_endpoint GoogleBetaProvider#site_verification_custom_endpoint}.'''
        result = self._values.get("site_verification_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_repo_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#source_repo_custom_endpoint GoogleBetaProvider#source_repo_custom_endpoint}.'''
        result = self._values.get("source_repo_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spanner_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#spanner_custom_endpoint GoogleBetaProvider#spanner_custom_endpoint}.'''
        result = self._values.get("spanner_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#sql_custom_endpoint GoogleBetaProvider#sql_custom_endpoint}.'''
        result = self._values.get("sql_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_batch_operations_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_batch_operations_custom_endpoint GoogleBetaProvider#storage_batch_operations_custom_endpoint}.'''
        result = self._values.get("storage_batch_operations_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_control_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_control_custom_endpoint GoogleBetaProvider#storage_control_custom_endpoint}.'''
        result = self._values.get("storage_control_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_custom_endpoint GoogleBetaProvider#storage_custom_endpoint}.'''
        result = self._values.get("storage_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_insights_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_insights_custom_endpoint GoogleBetaProvider#storage_insights_custom_endpoint}.'''
        result = self._values.get("storage_insights_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_transfer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#storage_transfer_custom_endpoint GoogleBetaProvider#storage_transfer_custom_endpoint}.'''
        result = self._values.get("storage_transfer_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tags_custom_endpoint GoogleBetaProvider#tags_custom_endpoint}.'''
        result = self._values.get("tags_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags_location_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tags_location_custom_endpoint GoogleBetaProvider#tags_location_custom_endpoint}.'''
        result = self._values.get("tags_location_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terraform_attribution_label_addition_strategy(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#terraform_attribution_label_addition_strategy GoogleBetaProvider#terraform_attribution_label_addition_strategy}.'''
        result = self._values.get("terraform_attribution_label_addition_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpu_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tpu_custom_endpoint GoogleBetaProvider#tpu_custom_endpoint}.'''
        result = self._values.get("tpu_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpu_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#tpu_v2_custom_endpoint GoogleBetaProvider#tpu_v2_custom_endpoint}.'''
        result = self._values.get("tpu_v2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transcoder_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#transcoder_custom_endpoint GoogleBetaProvider#transcoder_custom_endpoint}.'''
        result = self._values.get("transcoder_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def universe_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#universe_domain GoogleBetaProvider#universe_domain}.'''
        result = self._values.get("universe_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_project_override(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#user_project_override GoogleBetaProvider#user_project_override}.'''
        result = self._values.get("user_project_override")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vertex_ai_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#vertex_ai_custom_endpoint GoogleBetaProvider#vertex_ai_custom_endpoint}.'''
        result = self._values.get("vertex_ai_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vmwareengine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#vmwareengine_custom_endpoint GoogleBetaProvider#vmwareengine_custom_endpoint}.'''
        result = self._values.get("vmwareengine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_access_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#vpc_access_custom_endpoint GoogleBetaProvider#vpc_access_custom_endpoint}.'''
        result = self._values.get("vpc_access_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workbench_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#workbench_custom_endpoint GoogleBetaProvider#workbench_custom_endpoint}.'''
        result = self._values.get("workbench_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflows_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#workflows_custom_endpoint GoogleBetaProvider#workflows_custom_endpoint}.'''
        result = self._values.get("workflows_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workstations_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#workstations_custom_endpoint GoogleBetaProvider#workstations_custom_endpoint}.'''
        result = self._values.get("workstations_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#zone GoogleBetaProvider#zone}.'''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBetaProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.provider.GoogleBetaProviderExternalCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "audience": "audience",
        "identity_token": "identityToken",
        "service_account_email": "serviceAccountEmail",
    },
)
class GoogleBetaProviderExternalCredentials:
    def __init__(
        self,
        *,
        audience: builtins.str,
        identity_token: builtins.str,
        service_account_email: builtins.str,
    ) -> None:
        '''
        :param audience: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#audience GoogleBetaProvider#audience}.
        :param identity_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#identity_token GoogleBetaProvider#identity_token}.
        :param service_account_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_account_email GoogleBetaProvider#service_account_email}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17130effea28cfff8a6ced91a439f095c6fbbbc7a6bc18c0788218d199d61ad6)
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument identity_token", value=identity_token, expected_type=type_hints["identity_token"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audience": audience,
            "identity_token": identity_token,
            "service_account_email": service_account_email,
        }

    @builtins.property
    def audience(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#audience GoogleBetaProvider#audience}.'''
        result = self._values.get("audience")
        assert result is not None, "Required property 'audience' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#identity_token GoogleBetaProvider#identity_token}.'''
        result = self._values.get("identity_token")
        assert result is not None, "Required property 'identity_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs#service_account_email GoogleBetaProvider#service_account_email}.'''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBetaProviderExternalCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GoogleBetaProvider",
    "GoogleBetaProviderBatching",
    "GoogleBetaProviderConfig",
    "GoogleBetaProviderExternalCredentials",
]

publication.publish()

def _typecheckingstub__dd797056cd80150f775dd74b0137239361d8c3526785cfab58b0226d1185ff2b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_approval_custom_endpoint: typing.Optional[builtins.str] = None,
    access_context_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    access_token: typing.Optional[builtins.str] = None,
    active_directory_custom_endpoint: typing.Optional[builtins.str] = None,
    add_terraform_attribution_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alias: typing.Optional[builtins.str] = None,
    alloydb_custom_endpoint: typing.Optional[builtins.str] = None,
    api_gateway_custom_endpoint: typing.Optional[builtins.str] = None,
    apigee_custom_endpoint: typing.Optional[builtins.str] = None,
    apihub_custom_endpoint: typing.Optional[builtins.str] = None,
    apikeys_custom_endpoint: typing.Optional[builtins.str] = None,
    app_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    apphub_custom_endpoint: typing.Optional[builtins.str] = None,
    artifact_registry_custom_endpoint: typing.Optional[builtins.str] = None,
    assured_workloads_custom_endpoint: typing.Optional[builtins.str] = None,
    backup_dr_custom_endpoint: typing.Optional[builtins.str] = None,
    batching: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBetaProviderBatching, typing.Dict[builtins.str, typing.Any]]]]] = None,
    beyondcorp_custom_endpoint: typing.Optional[builtins.str] = None,
    biglake_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_analytics_hub_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_connection_custom_endpoint: typing.Optional[builtins.str] = None,
    big_query_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_datapolicy_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_data_transfer_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_reservation_custom_endpoint: typing.Optional[builtins.str] = None,
    bigtable_custom_endpoint: typing.Optional[builtins.str] = None,
    billing_custom_endpoint: typing.Optional[builtins.str] = None,
    billing_project: typing.Optional[builtins.str] = None,
    binary_authorization_custom_endpoint: typing.Optional[builtins.str] = None,
    blockchain_node_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    certificate_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    chronicle_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_asset_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_billing_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_build_custom_endpoint: typing.Optional[builtins.str] = None,
    cloudbuildv2_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_build_worker_pool_custom_endpoint: typing.Optional[builtins.str] = None,
    clouddeploy_custom_endpoint: typing.Optional[builtins.str] = None,
    clouddomains_custom_endpoint: typing.Optional[builtins.str] = None,
    cloudfunctions2_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_functions_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_identity_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_ids_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_quotas_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_run_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_run_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_scheduler_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_tasks_custom_endpoint: typing.Optional[builtins.str] = None,
    colab_custom_endpoint: typing.Optional[builtins.str] = None,
    composer_custom_endpoint: typing.Optional[builtins.str] = None,
    compute_custom_endpoint: typing.Optional[builtins.str] = None,
    container_analysis_custom_endpoint: typing.Optional[builtins.str] = None,
    container_attached_custom_endpoint: typing.Optional[builtins.str] = None,
    container_aws_custom_endpoint: typing.Optional[builtins.str] = None,
    container_azure_custom_endpoint: typing.Optional[builtins.str] = None,
    container_custom_endpoint: typing.Optional[builtins.str] = None,
    core_billing_custom_endpoint: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[builtins.str] = None,
    database_migration_service_custom_endpoint: typing.Optional[builtins.str] = None,
    data_catalog_custom_endpoint: typing.Optional[builtins.str] = None,
    dataflow_custom_endpoint: typing.Optional[builtins.str] = None,
    dataform_custom_endpoint: typing.Optional[builtins.str] = None,
    data_fusion_custom_endpoint: typing.Optional[builtins.str] = None,
    data_loss_prevention_custom_endpoint: typing.Optional[builtins.str] = None,
    data_pipeline_custom_endpoint: typing.Optional[builtins.str] = None,
    dataplex_custom_endpoint: typing.Optional[builtins.str] = None,
    dataproc_custom_endpoint: typing.Optional[builtins.str] = None,
    dataproc_gdc_custom_endpoint: typing.Optional[builtins.str] = None,
    dataproc_metastore_custom_endpoint: typing.Optional[builtins.str] = None,
    datastream_custom_endpoint: typing.Optional[builtins.str] = None,
    default_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    deployment_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    developer_connect_custom_endpoint: typing.Optional[builtins.str] = None,
    dialogflow_custom_endpoint: typing.Optional[builtins.str] = None,
    dialogflow_cx_custom_endpoint: typing.Optional[builtins.str] = None,
    discovery_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    dns_custom_endpoint: typing.Optional[builtins.str] = None,
    document_ai_custom_endpoint: typing.Optional[builtins.str] = None,
    document_ai_warehouse_custom_endpoint: typing.Optional[builtins.str] = None,
    edgecontainer_custom_endpoint: typing.Optional[builtins.str] = None,
    edgenetwork_custom_endpoint: typing.Optional[builtins.str] = None,
    essential_contacts_custom_endpoint: typing.Optional[builtins.str] = None,
    eventarc_custom_endpoint: typing.Optional[builtins.str] = None,
    external_credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBetaProviderExternalCredentials, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filestore_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_app_check_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_app_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_database_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_data_connect_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_extensions_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
    firebaserules_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_storage_custom_endpoint: typing.Optional[builtins.str] = None,
    firestore_custom_endpoint: typing.Optional[builtins.str] = None,
    gemini_custom_endpoint: typing.Optional[builtins.str] = None,
    gke_backup_custom_endpoint: typing.Optional[builtins.str] = None,
    gke_hub2_custom_endpoint: typing.Optional[builtins.str] = None,
    gke_hub_custom_endpoint: typing.Optional[builtins.str] = None,
    gkehub_feature_custom_endpoint: typing.Optional[builtins.str] = None,
    gkeonprem_custom_endpoint: typing.Optional[builtins.str] = None,
    healthcare_custom_endpoint: typing.Optional[builtins.str] = None,
    iam2_custom_endpoint: typing.Optional[builtins.str] = None,
    iam3_custom_endpoint: typing.Optional[builtins.str] = None,
    iam_beta_custom_endpoint: typing.Optional[builtins.str] = None,
    iam_credentials_custom_endpoint: typing.Optional[builtins.str] = None,
    iam_custom_endpoint: typing.Optional[builtins.str] = None,
    iam_workforce_pool_custom_endpoint: typing.Optional[builtins.str] = None,
    iap_custom_endpoint: typing.Optional[builtins.str] = None,
    identity_platform_custom_endpoint: typing.Optional[builtins.str] = None,
    impersonate_service_account: typing.Optional[builtins.str] = None,
    impersonate_service_account_delegates: typing.Optional[typing.Sequence[builtins.str]] = None,
    integration_connectors_custom_endpoint: typing.Optional[builtins.str] = None,
    integrations_custom_endpoint: typing.Optional[builtins.str] = None,
    kms_custom_endpoint: typing.Optional[builtins.str] = None,
    logging_custom_endpoint: typing.Optional[builtins.str] = None,
    looker_custom_endpoint: typing.Optional[builtins.str] = None,
    lustre_custom_endpoint: typing.Optional[builtins.str] = None,
    managed_kafka_custom_endpoint: typing.Optional[builtins.str] = None,
    memcache_custom_endpoint: typing.Optional[builtins.str] = None,
    memorystore_custom_endpoint: typing.Optional[builtins.str] = None,
    migration_center_custom_endpoint: typing.Optional[builtins.str] = None,
    ml_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    monitoring_custom_endpoint: typing.Optional[builtins.str] = None,
    netapp_custom_endpoint: typing.Optional[builtins.str] = None,
    network_connectivity_custom_endpoint: typing.Optional[builtins.str] = None,
    network_management_custom_endpoint: typing.Optional[builtins.str] = None,
    network_security_custom_endpoint: typing.Optional[builtins.str] = None,
    network_services_custom_endpoint: typing.Optional[builtins.str] = None,
    notebooks_custom_endpoint: typing.Optional[builtins.str] = None,
    oracle_database_custom_endpoint: typing.Optional[builtins.str] = None,
    org_policy_custom_endpoint: typing.Optional[builtins.str] = None,
    os_config_custom_endpoint: typing.Optional[builtins.str] = None,
    os_config_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    os_login_custom_endpoint: typing.Optional[builtins.str] = None,
    parallelstore_custom_endpoint: typing.Optional[builtins.str] = None,
    parameter_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    parameter_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
    privateca_custom_endpoint: typing.Optional[builtins.str] = None,
    privileged_access_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    public_ca_custom_endpoint: typing.Optional[builtins.str] = None,
    pubsub_custom_endpoint: typing.Optional[builtins.str] = None,
    pubsub_lite_custom_endpoint: typing.Optional[builtins.str] = None,
    recaptcha_enterprise_custom_endpoint: typing.Optional[builtins.str] = None,
    redis_custom_endpoint: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    request_reason: typing.Optional[builtins.str] = None,
    request_timeout: typing.Optional[builtins.str] = None,
    resource_manager3_custom_endpoint: typing.Optional[builtins.str] = None,
    resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    resource_manager_v3_custom_endpoint: typing.Optional[builtins.str] = None,
    runtimeconfig_custom_endpoint: typing.Optional[builtins.str] = None,
    runtime_config_custom_endpoint: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    secret_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
    secure_source_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_management_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    securityposture_custom_endpoint: typing.Optional[builtins.str] = None,
    security_scanner_custom_endpoint: typing.Optional[builtins.str] = None,
    service_directory_custom_endpoint: typing.Optional[builtins.str] = None,
    service_management_custom_endpoint: typing.Optional[builtins.str] = None,
    service_networking_custom_endpoint: typing.Optional[builtins.str] = None,
    service_usage_custom_endpoint: typing.Optional[builtins.str] = None,
    site_verification_custom_endpoint: typing.Optional[builtins.str] = None,
    source_repo_custom_endpoint: typing.Optional[builtins.str] = None,
    spanner_custom_endpoint: typing.Optional[builtins.str] = None,
    sql_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_batch_operations_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_control_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_insights_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_transfer_custom_endpoint: typing.Optional[builtins.str] = None,
    tags_custom_endpoint: typing.Optional[builtins.str] = None,
    tags_location_custom_endpoint: typing.Optional[builtins.str] = None,
    terraform_attribution_label_addition_strategy: typing.Optional[builtins.str] = None,
    tpu_custom_endpoint: typing.Optional[builtins.str] = None,
    tpu_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    transcoder_custom_endpoint: typing.Optional[builtins.str] = None,
    universe_domain: typing.Optional[builtins.str] = None,
    user_project_override: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vertex_ai_custom_endpoint: typing.Optional[builtins.str] = None,
    vmwareengine_custom_endpoint: typing.Optional[builtins.str] = None,
    vpc_access_custom_endpoint: typing.Optional[builtins.str] = None,
    workbench_custom_endpoint: typing.Optional[builtins.str] = None,
    workflows_custom_endpoint: typing.Optional[builtins.str] = None,
    workstations_custom_endpoint: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f0b89c806f84a1d7e9ffd2915f747abf710ac603560697f5b5b4ecf4a34620(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277b135c45e1f36c53e3d6259bc2e9b67e398af621946044f49c76987759ac70(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79e0eda73c39486edd2476fd0478aa96c302f7caeaa0237544255b31b955b81(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279293696549d3620383fba86650deae2fbfd4e534270bb5546382da607f2519(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c33ac2a832f17924fabe06c300baf587ef1d25ab9b65b7b2c03b14f61b1224(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06d16a0fb6e3bb74b6ac090679bb407db97981fe8b4afe346763c78f001ce6f(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0787e4e3080f2ea5478f760a1ae96f889d67e334e927b487d33a54ecdd4b0bf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909a834d18cc31be72737093f6bbad3d0ddfccf4ccad73f8ed5d1470d84d6082(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a4e3d94a7dc556f3aacca26f463f68696a64705f6356ba742a76d8f0d57037(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2f7f919a3d93f81392e9357777b83216485f80d731089aa76bfeff8333d24a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78759a0e1be2766b57dea4cf8f34f853dc0a1790e861ddb0330709fda70af8f5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8d52d7c4b41479af7ce0d8cb9b5dc72eb8c5efe0dab27a78042b05034a4f2c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7403f0dc8519653edcf8eb699807d991bfa40fa013d9911aa8b0c4edcf417a2b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8bc16eee0e7e41e825c803ba456a5844215cafd87cd6d9ede0aff8270ad4ea(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6403a296e73cd5c56d9e1b6f247494f9eece6a62884f5ad1f4b3e67d05e4a47(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09810854ef17d3dbaca0b75f5b72a4f874704681b0dc41c660a732d23c9b342a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fee8a212f7bbc8e3d32ee0ce8bd27ae14fabe330887745b9ea581bf907d38f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3b319071259ceb02b77c72747b16e27fde115d7bbba257180f9ea390c0c8bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBetaProviderBatching]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bec08d530be531b8494d0df258bb2a55c6f0763b522a8587b6f0f32f41f3e41(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d803a6adfc2857c900ad1b01cb82b1abb27fde87432ee66399d4f22f231ae1c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13223b4eddb793529314c142bc32f27f7cb1ce79b5ad68c64c7a0fdf969e1914(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efb8641cc3c55085ac1b4866d4284b129951f45f33d2c9e94b9116da19c99cd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8d2749a637080806771911f5123d8a726e8b3367dec0c6d58e693072528374(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c550df17c3e3bd9363ae923c9ad3e6e600f99acd1df7ae0274afa1d2f6d016(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52690aa938c990a769452e4879075ea2e851b81e9ad2d5a9dd46c01038d1c0ca(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19f0c25fd5890ebc21e1f5cf7b32927508352c17e219ff9551ab172049155e6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34bbaea14f860ae3ef73b5bde905679593cb2f59b439d04dd33aafc9d5174095(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df62387c443e8b15d0e183156dcff070053a4cd00a2e5b550c044f3f54de4bc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68068de88f171aa0ee628d7c916a1296349de9382dabf2056a9fc0fe0cc1621c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bcbcafd8668702c903270203c5a7be030092062e8f9b13989f146f13be32f34(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45350c75dd13c69b9b1254d6f3ff5268d2b599dc20e8fa079d4b98b914186119(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c66f0e49843317abde0fe81934aedf593a0bfea9be63fce8de4884162578c8a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8e221f1eada3611ca14ce9a5c5f9f3addbfadf062f07d1c193cc27a8ac3cb4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a40176a1055e782aca6e3a4fcbfa6877196c24006915677f98bb4c52a5a0c8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7799685f41ed1c973a6a1ddbdb95bcb810668b3a643ecb5e41f3a3794e421c2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65110ec7f849976770de17c3725ac57498276ff76b348a6d8568c66ef88c59e9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9977b67c753f417d60971b0a883bbd9af092727c524e42ee479f50ccf46c8b53(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edeb4ead8d80df25f1e99cbeddb63c5b32fed6f6a3cf254e4e8df32c074c042(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ad023dfd7b35fc0e60d201d987643b327f3dd0f678943bf2c5a84b489d7d66(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fb7e943e788ad08a55ff0b9233e1bd183b0eda7b22835ee2641e89f1d11613(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297f475b1a6814835e1485081c685731da37a34461ee6708e3d2ecea1e2b27dd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0483a0b3ca8290da1d2338a077bb80f1d3a6419f74255c90f110eb2c45b79e9f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d5ec9567f22107fa330d6412f3edaa076e4c5b25b880bf04282bed78ac4e83(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6144a72cd33c762d7300406419e5c43ebb579cb66a54a99114a3eb45c92ea44(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3b78732498d99005c6e8b86cb12da5fb5203bd31f6956b91372cd1d5d0be5e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc03072cf715797626e6838106e765f8cf89fd21f4f69ced55a497cd7ba3f77b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8336e6be0948f35cde26196545b7a68d472abcdb64e2dcff5e308a9ff28cfd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0329c1f238b71f12159a8683cc307e3a73cb02e4e9e70aea1e5336509e9b46(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f3d0c894c04fd73eeeb63656da3f257e2ce7f14fb887e0e8eb2ea0551e54c8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae9575f69905842bd484785ba031751341873761039b3d860f7d03b8df9cded(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc05d7fc7b1900fd2b59712dc1db57f1d4684bd1eb9c79c965c991a0893c51d0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d70ee7d8597c2852b8eff5cef83fd5fe5871b9f2dc084bf77fb7b1e48e146b06(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c1440b8ee9049c44ba8d02175aed090087094a3aa2c20b136a723e7fc461cf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594165eb917f308076b1e8602000deef67cfc404b2b89c8ca928be8af9a0406b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6935387c545fc24e8db2891f466215342a0a7a3d7500a628afe1bb460a040954(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c587f4ba61fca0d303fa8dabcc98fa3e1fdea837feedfa441819cad3e266e9a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dffe094183562a726716929cd7e7c180b2c836215cc926302dd49641545467e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f743a40befb7832cb0250b3a0fe6b1349f3559881382f290dcb30c15947a962(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf1f684d698662b953e89a568935ba91386b7467ce411da6053d7d4a6feabc8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781e7ef8949e8098e387633d67fe3ea0e798690d66a9547fe7e2c84d23ba2911(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e97b9d7ecce45bcceb5308ce2dddca5d875a47c3a1850b0c348a2e615c5946(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5e262cfcda61da75f224e0fa4b234505f11655afd720aae8e983dd55b81857(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9f59207e5ced72d362a91ecbdcf2fa719804a4441440017931b697a4d7564e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42454630398f7deeeec3e6a30b0f4d943966bce2f359c68149a0f736d47cd037(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09dc72140c1d2be4b7e68c94742f86be552fb8da22beb10689429db0862e1d36(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8e39386feb134041e2ef2f8445b0109466667f333debe7b0834caddacdf977(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7509c970485e43d8484bfe5d58ccf088ce9fe33930b4a8972bf46af9baf6363(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7fa61e7bfc0ae8cfb8a1cc45d1ca9594a1bef25d07826650fae3f5c3e35023(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8557ec8b3ece3e7bd76e25650187e8cfd82199a763f67b2a4aa26e8c81b0df83(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c50c5131b38a0d7065499c9b3cb8d8a469271e302fb8637a03b32328a1c5ecd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1457ccece6aad860986e78c01e92241fca81167611c262e7922002ec6e88e90f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b538b3242e339a1fbc77a21eae8de2dc4d59af4510a17323d191b847240cc7b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97cf3d7f96646d6f44c1dad3bd367a8425aa308b182e37c9e9593f513f4bf511(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df36c62ace8e49cea320b1df34f8d5cc169f23a514bd7db4a8af8e9188f27160(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa14129fc70abb49b617075e323a8c92610d3bf8d64c3773f3b1068f005173f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7383c42c5676e804c21625984129145d98af9eaed2afeea19137c3ad9eb6d765(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55dbde4287441ca53b8364cb3eb1fb3d02002ea9078071a49ff674edec8b7d08(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70fd76c17a8571105fd3d2860f0a31f01527df3ebf6dfd657847914a8927160a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f919ff2bcc878515f30894852650c0cc18d2c9b10a5e57115ea6166c15fb36(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d08c038cbac78ce24f7e02d5588f46a08383d7f75a570ffecd63fffad7ad63(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2465f7590332147a3c0a6ad53241dfafcddc2f83e354c2007d4286a6434e139d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86faae4a5e206c1ba7ba0517c652774646e8ee885fd9e8cbebb226aa01e5aa6e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df40d7843585bd43698c2d9462672c223b28e16bd43552ecc793f6d5053fb694(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ecb2a5f392b3275e436a6047dd9cc37455e22f70e50f95b4c47d14e24578f38(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0511b49e099f1d75cd08f6e3d9d0c5899beb9e5df4aecee1487beac9c3412e2b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862ca0af72c2a59e81b74d34407ecf9798387a3e886a989861b40aca4f2e83c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBetaProviderExternalCredentials]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515578f0fa3414e1f587be77823d372563806bca4ba1a421f275af267cc22bab(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c523080169447cf31f7704e572564aaa8977901dbb550e91fde62353a67425a5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ff4d6d7ca21691a78647262d00cf18031926338b90ff0f38be4a6897bad4e8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37085d6d0c112005fb95b523fdd1f84b8faa41f7da1a546cd528fdfdce298b54(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740b4ff1ccd145aa4815ca4594431c815aa6f3f53f88a227a97f6114563ec798(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62f0d602ef39504e14219b727e18deaf689088d11c86a0851a19353f5287c86(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac77163ad01854a6a13d786173be447d2380925669e156703b7a5e363ef5de0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4c0d9d5a8225de17f54784604951f923074fda15e51e72d38d231771069c10(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b980b19f58fb586745e89398640dd90281ee6252de9cc0b72c5efd86e2222b93(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61d658e7cdda012fb0d54ccb692c63fe773ed14856a151a097b1c5558d0093d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e02c755630ad98326031533cc3f3ecdddb4629c6eec2cdbcf9d6b4dfd13e4fa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8177d3e5b1630532f1e4e6bb33ea4d82398fcc40af1e34812fcb1b3f8f8bfad2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31af92754f7cccaf571e2a9de25c475277122680fd9bcc782004ab085cb82f0d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9430b1003f8e02a77c781325da9e9f48db45addf49d7a2d152d5d8762618ef(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4bb05e0e27835248b17c226392bb99ff2ba32625fc9bdca51d0b285aea1b63f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21951682d7460f4b766bd144c0a9d6e0027279da8cd0853a9ffd5921db0224d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2224e65c4c2baa326b676a4a5515ccfeb21b7a9ab7d2ed5bc8416c0c039d2c7f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910c97876c8c450c429d36bbb9bee18ba4024bd93e23e01f4739eee29ccf93d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d40bcd0659a217e73c2d21f1151f7e26e38453a6315efa629752f72ac0d6aa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e40f20576c2e4edb8ab56460d21a5fa3434a9f5b47526e62e3a0ffa58dffad5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deaac9b79a43ecbcc2bd353a085bc00385532ddb8bcd8270d8fdbdc811337b05(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c06e0c8ce729e984ef30354e151d4a3284ee05cb13addfc3c4d3d5890c9eee4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c801f7a56bc9364ecb91d83c5edd4f8efb72eb76843fce749485bd25a5fbf14c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66a59934fd4e2b04add1a8ead6662a2999905dc475159e45012365676b3ed9d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ad2eea5652f568aba98083e76fa1417fb2db19c844a1660b1e4f34d6ada98c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109be11f9283c0efc33f0b423370fb012fff3a3938c4531b4e494b25733eb81f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f72aa0b243eadac1c7b1264ea0fbe21de31e132e7a45024864e90bb0017d2d8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab17ec8e3c09a39cdcfacd377a16222fe714c4efce0a122b2de5a3c9242e66f(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf2b6106563398a7b1c503ac8bd10c8109c24e25f246db4bd05399ecb57e927(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ed388c8d0117d21f03dcfd603b2b9c5a66fbb069b4004b6fb6cae8fd4a9d1a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee93361c464a963f37a9cdd87ad737b9bd5b749e4d1e708d57037c74cb190cc1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc5cded5e87200af16b787f4673609997b55d3f44d341ac5a7c9f665dc8f828(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d2a33c841fab9d8bc06e2b9e2c2a253a32c61215de152451ee0aed447cb6d2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d344f29e05f432b2310e2688e905b206cf1fa707287931cd9478bcc28fb5720(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffcb605ec19a68cfd58da0cadc51f700cb7fcbc12b57c013ba3174e3e9b8c51c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e984b21a5ea66b82291a11675ff78c2bc1a7da7b4665b6a42f696d5b6ffc4d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3859959af1500e4aa158c9a41aded706a34980d32e90a6ce1b4ca8d75d750e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9403e199a59b7e8ee9ff75e2a1c75b127c2a21d222740f3707011c81b80c755(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8448496713fe8128a39ef3d6f429d4127aa6dad679d4ba74a60eaf05be5d89(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b255fd005429e016ff919756701a95909c8ee9d08b94b882d15d42b42283e6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c28c9e9ba68afddb6addc818073186c254b7a0f0da193de01a56f5d3ea7faa5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de47f9bed38abb9857acc1e96638144a74278ba6118111105dc93583fd4a52a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823b5f1f7247f7d28eaeecb4521e3527e5870c0bdc2c3aed2b8adfcce9b2fde6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d2b3b847a28032b27f16ccc9c0a21701fcc7c638f1fa03579a0160afbb1eeb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a66c909ce893e25eafb470fd8d62a42844ebb278487880f25724d8adab916a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70fecaf83f6ed1b664c993936be11418276188c26e45aeb326ff33ea49c23bcd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8676c31fe795b16a2f10fc8954ad5c5bbb64158914c6af01a06712f5c43ee557(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ceb6f6a579175ad8f20d614cb5a4b870f003b390eefc31d1a806e5126537cf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48976ef46d76eaefc8446cb8c3bad2786e89fa98a67afd69a682cbf0a3c31d8b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7743975c2b631af5789e25de57ade2faec5d2ddbb1cf02e79266749b42a458b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3377f27f22de9c684a2207bce376bc4a3a77d594840566aece605617f9a8c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90cf79df198f374b1c76da9b24feea72873f604a88e2b2491fa712041d770b4c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ccc084c23d9bb77fc7b958db07de00f434fbf2b709b625a19a231b03b9d403(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d94229fe704baa7048f9ec79bea58ebe7555c1703a4cef0cfc730c0fda6ae84(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee90dbc1b564cda0c55046efa24e318ffd04d12fddbe4b3cdad7b59b10027ab1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab355394dea00a911ce2800dd38ed94a4599bcb15776c9120373be0c7b7f648c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b334230c30ac4befac0d3bc79dbf82960acd331bcf230c3c2b9702d71e9c407(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874597822d8c4e0a8dd18a417057332a575df04dda52f21a4d0fcd5e49c0f52c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d35ae613dd14fc26ad932d9ae1c67074f2969f8525bb137e044fd748a9ed7df(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78115d57ff065a810f35d72a2f1a765096a020dd518fae113fe34350d4c1df95(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220fc6edded0619e1e29d10866b002acd584deffe3edb29df8fac20d95ccbc5f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22979f69f872ef3fd8012b2d7311a92845dbdbf378ab73cd6688997ba83d4ce5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5656bfa8c680416ec6c8713075287a57c3e637737e432e6dc9222c46f0bb979(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa5847dc7e5a17fe5cd23545194315bb3db887ef43de22793c81a042ba05ed5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77ccc2a0cbf0c3f3d1df1da50f2e9839ae27b596f3c8c33246c833d706b01b3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b328e661fd71d34b2ee41f34edb7a22393c45d5cd3e6a016b10e8ab4ac3f0a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f95457ec2068c65c8e03df6aa22969d51170ff1430f2a27eda22a3f2ee07a2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72766b6852d67462c0f10240e60ad39737654eac6f9854f5e73cc2907620d5c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d39a6c90d1382a85ab1bf4d9b615953c989437d10737dd581ac966a9cd462d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b692e627d68fbaeccb3aaf1f990c5adfca5c456293c06c56dc7b994220630b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f06b9d949684d96e3dc29a629a2fc0392c56e9199be04ae55a6bd3cd2eec64c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f42f7fb66a5f120818b1ec0074aa4ba4c9eb826d0a8b1c20f1bc96d55c5954(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d3b47d3918595d7250bd296be8640f1e8ab1e6e34b45cdb345d8250e249f74(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bfde948d0c95558d502c922539cc931ff52ee9a77091bbc00694de80e068dc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f3ca0658d64f05cd29e8723d023814736f299cbf0463581232fcb789d4040b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652a124bea66968f564f7f12d970b577c1815a32d2033a416b40be0abd471bcf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c2332d7ca2a5fc76f4f04ae3d24c23c4825ed5e9082e80ef3175c596b30161(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5747ab24111cecc22440ecf90703e759694a07f8c6f5b8c26e78b4cbcca2fff3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83963070cf816c0423d08c1328940cd66194549ec5c3b0edd3de8da1e9a4a2c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303feb20a504b2ae74d8a4ea27af5792bfd6305de510a98afef0ebe3dff49717(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882e3fd626de4f7336d4e267de9450eb2b77d1ee956d0b74cc21c4f3fd45baf4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ea784a23839f4e86ef3696dacef0d47c8971b746dc637cb1872195a6a6c0b0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac207e9bbddfd545f61fab059e350c3a9f3c8f39ca9eda14994317e9af46749f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f375707cf3dbd9c95b62a66777e045f03043ed75f80e3c245ae03bb27ce676f6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3398fa4c6e6fe464fd5263786d2b898c6923760fb5ea42d4c01639247a3938(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7e9a387bf7818c118bfa8c3c014273fa47053af35b5485792c3ed4831c9d97(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccd63d441134893f54f211021b17f1e92571fe3f72a5c90108cee2046d4d3ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59de503556316a3ca64baba8587e021d747e0f5b43f661a0347f59ecb1908d5c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada3fb034878a8679fda6dd9e593d31618f5ebe594785dcd247aa8eaf2d78645(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d4fb1ec219b71accd2cc2a764fed5bfd02cce21c134985b4fd24868cd71504(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f6bcfe20b7ef31aa902ecc563c998182d11ed7dbb60a97eac286afe83a43c2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a93bae96dd736c3e267dc9906134bc87ff9aae22f6e03dbae592493b5d74f47(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1514eeaa8dc1ec783e5f6b7ebd57ee508d494172ace1d89c9b7f89c75e7f63(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d8e65c04f5d3a3478be640d1792a2376e5aad4c7f821baff338337ab8a1391(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a2f23d31c7b9451edef4a206a49656d22da08d1f015ec89ea004aa13e4fdcc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c842aede83001afeec71bd444e796b2566d761862872837f56f33b11bd98738(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d247ccbd9491e52988522264f6fcdbbee22d9593c7cb1721870e3ef8a9cddf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ce0a9288408970f20561dc13833c63464947b18b210f1ece263604218c641b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239b5b453ec987bfd51773776fdbe35524d94410a888bfddb0d982610e8fd371(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23917ccd6c2d6e2a8db5f7d71fad4bebe11f77fca71623a4fb270c56908fe97d(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3163d7f484f936d6a7f275f62e778d20e0a91533a9e3533b7a3e225bcb09c7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5a1ab2f5a12bd704ecdb36629bdaec68b5a3ff60961590a1396d0406ffb2c1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6940e4bff6e9e8667cf2a4feb08ad070232db20d09ac892aedb750f07425d75a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdedc88d0e55b82d0d0a9735fb84b61b86a05db71fc1cca08a91cbdbf34d5463(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8263ee3354fc1599c11af3e1847de81bf4d0a754c9a52d739383294224858e7e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0a272deed4287035bbaf36aa494e4409e2ca6627f5de4aa58cd84158148328(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4a318fadbee5551187cdb78b3cf3e8ee27cbe311ccecdeabf64b86641c8024(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbf2bb8f37e1971fc512e090f309f883c17935d206ab19907c44b1932a0f917(
    *,
    enable_batching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_after: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0888201207876e3240f2c01d78947ebd8ad730c84b80d6e77c356836c1f801(
    *,
    access_approval_custom_endpoint: typing.Optional[builtins.str] = None,
    access_context_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    access_token: typing.Optional[builtins.str] = None,
    active_directory_custom_endpoint: typing.Optional[builtins.str] = None,
    add_terraform_attribution_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alias: typing.Optional[builtins.str] = None,
    alloydb_custom_endpoint: typing.Optional[builtins.str] = None,
    api_gateway_custom_endpoint: typing.Optional[builtins.str] = None,
    apigee_custom_endpoint: typing.Optional[builtins.str] = None,
    apihub_custom_endpoint: typing.Optional[builtins.str] = None,
    apikeys_custom_endpoint: typing.Optional[builtins.str] = None,
    app_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    apphub_custom_endpoint: typing.Optional[builtins.str] = None,
    artifact_registry_custom_endpoint: typing.Optional[builtins.str] = None,
    assured_workloads_custom_endpoint: typing.Optional[builtins.str] = None,
    backup_dr_custom_endpoint: typing.Optional[builtins.str] = None,
    batching: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBetaProviderBatching, typing.Dict[builtins.str, typing.Any]]]]] = None,
    beyondcorp_custom_endpoint: typing.Optional[builtins.str] = None,
    biglake_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_analytics_hub_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_connection_custom_endpoint: typing.Optional[builtins.str] = None,
    big_query_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_datapolicy_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_data_transfer_custom_endpoint: typing.Optional[builtins.str] = None,
    bigquery_reservation_custom_endpoint: typing.Optional[builtins.str] = None,
    bigtable_custom_endpoint: typing.Optional[builtins.str] = None,
    billing_custom_endpoint: typing.Optional[builtins.str] = None,
    billing_project: typing.Optional[builtins.str] = None,
    binary_authorization_custom_endpoint: typing.Optional[builtins.str] = None,
    blockchain_node_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    certificate_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    chronicle_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_asset_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_billing_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_build_custom_endpoint: typing.Optional[builtins.str] = None,
    cloudbuildv2_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_build_worker_pool_custom_endpoint: typing.Optional[builtins.str] = None,
    clouddeploy_custom_endpoint: typing.Optional[builtins.str] = None,
    clouddomains_custom_endpoint: typing.Optional[builtins.str] = None,
    cloudfunctions2_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_functions_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_identity_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_ids_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_quotas_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_run_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_run_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_scheduler_custom_endpoint: typing.Optional[builtins.str] = None,
    cloud_tasks_custom_endpoint: typing.Optional[builtins.str] = None,
    colab_custom_endpoint: typing.Optional[builtins.str] = None,
    composer_custom_endpoint: typing.Optional[builtins.str] = None,
    compute_custom_endpoint: typing.Optional[builtins.str] = None,
    container_analysis_custom_endpoint: typing.Optional[builtins.str] = None,
    container_attached_custom_endpoint: typing.Optional[builtins.str] = None,
    container_aws_custom_endpoint: typing.Optional[builtins.str] = None,
    container_azure_custom_endpoint: typing.Optional[builtins.str] = None,
    container_custom_endpoint: typing.Optional[builtins.str] = None,
    core_billing_custom_endpoint: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[builtins.str] = None,
    database_migration_service_custom_endpoint: typing.Optional[builtins.str] = None,
    data_catalog_custom_endpoint: typing.Optional[builtins.str] = None,
    dataflow_custom_endpoint: typing.Optional[builtins.str] = None,
    dataform_custom_endpoint: typing.Optional[builtins.str] = None,
    data_fusion_custom_endpoint: typing.Optional[builtins.str] = None,
    data_loss_prevention_custom_endpoint: typing.Optional[builtins.str] = None,
    data_pipeline_custom_endpoint: typing.Optional[builtins.str] = None,
    dataplex_custom_endpoint: typing.Optional[builtins.str] = None,
    dataproc_custom_endpoint: typing.Optional[builtins.str] = None,
    dataproc_gdc_custom_endpoint: typing.Optional[builtins.str] = None,
    dataproc_metastore_custom_endpoint: typing.Optional[builtins.str] = None,
    datastream_custom_endpoint: typing.Optional[builtins.str] = None,
    default_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    deployment_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    developer_connect_custom_endpoint: typing.Optional[builtins.str] = None,
    dialogflow_custom_endpoint: typing.Optional[builtins.str] = None,
    dialogflow_cx_custom_endpoint: typing.Optional[builtins.str] = None,
    discovery_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    dns_custom_endpoint: typing.Optional[builtins.str] = None,
    document_ai_custom_endpoint: typing.Optional[builtins.str] = None,
    document_ai_warehouse_custom_endpoint: typing.Optional[builtins.str] = None,
    edgecontainer_custom_endpoint: typing.Optional[builtins.str] = None,
    edgenetwork_custom_endpoint: typing.Optional[builtins.str] = None,
    essential_contacts_custom_endpoint: typing.Optional[builtins.str] = None,
    eventarc_custom_endpoint: typing.Optional[builtins.str] = None,
    external_credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBetaProviderExternalCredentials, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filestore_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_app_check_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_app_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_database_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_data_connect_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_extensions_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
    firebaserules_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_storage_custom_endpoint: typing.Optional[builtins.str] = None,
    firestore_custom_endpoint: typing.Optional[builtins.str] = None,
    gemini_custom_endpoint: typing.Optional[builtins.str] = None,
    gke_backup_custom_endpoint: typing.Optional[builtins.str] = None,
    gke_hub2_custom_endpoint: typing.Optional[builtins.str] = None,
    gke_hub_custom_endpoint: typing.Optional[builtins.str] = None,
    gkehub_feature_custom_endpoint: typing.Optional[builtins.str] = None,
    gkeonprem_custom_endpoint: typing.Optional[builtins.str] = None,
    healthcare_custom_endpoint: typing.Optional[builtins.str] = None,
    iam2_custom_endpoint: typing.Optional[builtins.str] = None,
    iam3_custom_endpoint: typing.Optional[builtins.str] = None,
    iam_beta_custom_endpoint: typing.Optional[builtins.str] = None,
    iam_credentials_custom_endpoint: typing.Optional[builtins.str] = None,
    iam_custom_endpoint: typing.Optional[builtins.str] = None,
    iam_workforce_pool_custom_endpoint: typing.Optional[builtins.str] = None,
    iap_custom_endpoint: typing.Optional[builtins.str] = None,
    identity_platform_custom_endpoint: typing.Optional[builtins.str] = None,
    impersonate_service_account: typing.Optional[builtins.str] = None,
    impersonate_service_account_delegates: typing.Optional[typing.Sequence[builtins.str]] = None,
    integration_connectors_custom_endpoint: typing.Optional[builtins.str] = None,
    integrations_custom_endpoint: typing.Optional[builtins.str] = None,
    kms_custom_endpoint: typing.Optional[builtins.str] = None,
    logging_custom_endpoint: typing.Optional[builtins.str] = None,
    looker_custom_endpoint: typing.Optional[builtins.str] = None,
    lustre_custom_endpoint: typing.Optional[builtins.str] = None,
    managed_kafka_custom_endpoint: typing.Optional[builtins.str] = None,
    memcache_custom_endpoint: typing.Optional[builtins.str] = None,
    memorystore_custom_endpoint: typing.Optional[builtins.str] = None,
    migration_center_custom_endpoint: typing.Optional[builtins.str] = None,
    ml_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    monitoring_custom_endpoint: typing.Optional[builtins.str] = None,
    netapp_custom_endpoint: typing.Optional[builtins.str] = None,
    network_connectivity_custom_endpoint: typing.Optional[builtins.str] = None,
    network_management_custom_endpoint: typing.Optional[builtins.str] = None,
    network_security_custom_endpoint: typing.Optional[builtins.str] = None,
    network_services_custom_endpoint: typing.Optional[builtins.str] = None,
    notebooks_custom_endpoint: typing.Optional[builtins.str] = None,
    oracle_database_custom_endpoint: typing.Optional[builtins.str] = None,
    org_policy_custom_endpoint: typing.Optional[builtins.str] = None,
    os_config_custom_endpoint: typing.Optional[builtins.str] = None,
    os_config_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    os_login_custom_endpoint: typing.Optional[builtins.str] = None,
    parallelstore_custom_endpoint: typing.Optional[builtins.str] = None,
    parameter_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    parameter_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
    privateca_custom_endpoint: typing.Optional[builtins.str] = None,
    privileged_access_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    public_ca_custom_endpoint: typing.Optional[builtins.str] = None,
    pubsub_custom_endpoint: typing.Optional[builtins.str] = None,
    pubsub_lite_custom_endpoint: typing.Optional[builtins.str] = None,
    recaptcha_enterprise_custom_endpoint: typing.Optional[builtins.str] = None,
    redis_custom_endpoint: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    request_reason: typing.Optional[builtins.str] = None,
    request_timeout: typing.Optional[builtins.str] = None,
    resource_manager3_custom_endpoint: typing.Optional[builtins.str] = None,
    resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    resource_manager_v3_custom_endpoint: typing.Optional[builtins.str] = None,
    runtimeconfig_custom_endpoint: typing.Optional[builtins.str] = None,
    runtime_config_custom_endpoint: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    secret_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
    secure_source_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_management_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    securityposture_custom_endpoint: typing.Optional[builtins.str] = None,
    security_scanner_custom_endpoint: typing.Optional[builtins.str] = None,
    service_directory_custom_endpoint: typing.Optional[builtins.str] = None,
    service_management_custom_endpoint: typing.Optional[builtins.str] = None,
    service_networking_custom_endpoint: typing.Optional[builtins.str] = None,
    service_usage_custom_endpoint: typing.Optional[builtins.str] = None,
    site_verification_custom_endpoint: typing.Optional[builtins.str] = None,
    source_repo_custom_endpoint: typing.Optional[builtins.str] = None,
    spanner_custom_endpoint: typing.Optional[builtins.str] = None,
    sql_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_batch_operations_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_control_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_insights_custom_endpoint: typing.Optional[builtins.str] = None,
    storage_transfer_custom_endpoint: typing.Optional[builtins.str] = None,
    tags_custom_endpoint: typing.Optional[builtins.str] = None,
    tags_location_custom_endpoint: typing.Optional[builtins.str] = None,
    terraform_attribution_label_addition_strategy: typing.Optional[builtins.str] = None,
    tpu_custom_endpoint: typing.Optional[builtins.str] = None,
    tpu_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    transcoder_custom_endpoint: typing.Optional[builtins.str] = None,
    universe_domain: typing.Optional[builtins.str] = None,
    user_project_override: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vertex_ai_custom_endpoint: typing.Optional[builtins.str] = None,
    vmwareengine_custom_endpoint: typing.Optional[builtins.str] = None,
    vpc_access_custom_endpoint: typing.Optional[builtins.str] = None,
    workbench_custom_endpoint: typing.Optional[builtins.str] = None,
    workflows_custom_endpoint: typing.Optional[builtins.str] = None,
    workstations_custom_endpoint: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17130effea28cfff8a6ced91a439f095c6fbbbc7a6bc18c0788218d199d61ad6(
    *,
    audience: builtins.str,
    identity_token: builtins.str,
    service_account_email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
