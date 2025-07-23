r'''
# `provider`

Refer to the Terraform Registry for docs: [`google`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs).
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


class GoogleProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.provider.GoogleProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs google}.'''

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
        apigee_custom_endpoint: typing.Optional[builtins.str] = None,
        apihub_custom_endpoint: typing.Optional[builtins.str] = None,
        apikeys_custom_endpoint: typing.Optional[builtins.str] = None,
        app_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        apphub_custom_endpoint: typing.Optional[builtins.str] = None,
        artifact_registry_custom_endpoint: typing.Optional[builtins.str] = None,
        assured_workloads_custom_endpoint: typing.Optional[builtins.str] = None,
        backup_dr_custom_endpoint: typing.Optional[builtins.str] = None,
        batching: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleProviderBatching", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        contact_center_insights_custom_endpoint: typing.Optional[builtins.str] = None,
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
        external_credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleProviderExternalCredentials", typing.Dict[builtins.str, typing.Any]]]]] = None,
        filestore_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_app_check_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_app_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_data_connect_custom_endpoint: typing.Optional[builtins.str] = None,
        firebaserules_custom_endpoint: typing.Optional[builtins.str] = None,
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
        model_armor_custom_endpoint: typing.Optional[builtins.str] = None,
        model_armor_global_custom_endpoint: typing.Optional[builtins.str] = None,
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
        resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        resource_manager_v3_custom_endpoint: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        secret_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
        secure_source_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_management_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        securityposture_custom_endpoint: typing.Optional[builtins.str] = None,
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
        transcoder_custom_endpoint: typing.Optional[builtins.str] = None,
        universe_domain: typing.Optional[builtins.str] = None,
        user_project_override: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vertex_ai_custom_endpoint: typing.Optional[builtins.str] = None,
        vmwareengine_custom_endpoint: typing.Optional[builtins.str] = None,
        vpc_access_custom_endpoint: typing.Optional[builtins.str] = None,
        workbench_custom_endpoint: typing.Optional[builtins.str] = None,
        workflows_custom_endpoint: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs google} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_approval_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#access_approval_custom_endpoint GoogleProvider#access_approval_custom_endpoint}.
        :param access_context_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#access_context_manager_custom_endpoint GoogleProvider#access_context_manager_custom_endpoint}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#access_token GoogleProvider#access_token}.
        :param active_directory_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#active_directory_custom_endpoint GoogleProvider#active_directory_custom_endpoint}.
        :param add_terraform_attribution_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#add_terraform_attribution_label GoogleProvider#add_terraform_attribution_label}.
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#alias GoogleProvider#alias}
        :param alloydb_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#alloydb_custom_endpoint GoogleProvider#alloydb_custom_endpoint}.
        :param apigee_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apigee_custom_endpoint GoogleProvider#apigee_custom_endpoint}.
        :param apihub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apihub_custom_endpoint GoogleProvider#apihub_custom_endpoint}.
        :param apikeys_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apikeys_custom_endpoint GoogleProvider#apikeys_custom_endpoint}.
        :param app_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#app_engine_custom_endpoint GoogleProvider#app_engine_custom_endpoint}.
        :param apphub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apphub_custom_endpoint GoogleProvider#apphub_custom_endpoint}.
        :param artifact_registry_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#artifact_registry_custom_endpoint GoogleProvider#artifact_registry_custom_endpoint}.
        :param assured_workloads_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#assured_workloads_custom_endpoint GoogleProvider#assured_workloads_custom_endpoint}.
        :param backup_dr_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#backup_dr_custom_endpoint GoogleProvider#backup_dr_custom_endpoint}.
        :param batching: batching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#batching GoogleProvider#batching}
        :param beyondcorp_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#beyondcorp_custom_endpoint GoogleProvider#beyondcorp_custom_endpoint}.
        :param biglake_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#biglake_custom_endpoint GoogleProvider#biglake_custom_endpoint}.
        :param bigquery_analytics_hub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_analytics_hub_custom_endpoint GoogleProvider#bigquery_analytics_hub_custom_endpoint}.
        :param bigquery_connection_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_connection_custom_endpoint GoogleProvider#bigquery_connection_custom_endpoint}.
        :param big_query_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#big_query_custom_endpoint GoogleProvider#big_query_custom_endpoint}.
        :param bigquery_datapolicy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_datapolicy_custom_endpoint GoogleProvider#bigquery_datapolicy_custom_endpoint}.
        :param bigquery_data_transfer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_data_transfer_custom_endpoint GoogleProvider#bigquery_data_transfer_custom_endpoint}.
        :param bigquery_reservation_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_reservation_custom_endpoint GoogleProvider#bigquery_reservation_custom_endpoint}.
        :param bigtable_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigtable_custom_endpoint GoogleProvider#bigtable_custom_endpoint}.
        :param billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#billing_custom_endpoint GoogleProvider#billing_custom_endpoint}.
        :param billing_project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#billing_project GoogleProvider#billing_project}.
        :param binary_authorization_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#binary_authorization_custom_endpoint GoogleProvider#binary_authorization_custom_endpoint}.
        :param blockchain_node_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#blockchain_node_engine_custom_endpoint GoogleProvider#blockchain_node_engine_custom_endpoint}.
        :param certificate_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#certificate_manager_custom_endpoint GoogleProvider#certificate_manager_custom_endpoint}.
        :param chronicle_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#chronicle_custom_endpoint GoogleProvider#chronicle_custom_endpoint}.
        :param cloud_asset_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_asset_custom_endpoint GoogleProvider#cloud_asset_custom_endpoint}.
        :param cloud_billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_billing_custom_endpoint GoogleProvider#cloud_billing_custom_endpoint}.
        :param cloud_build_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_build_custom_endpoint GoogleProvider#cloud_build_custom_endpoint}.
        :param cloudbuildv2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloudbuildv2_custom_endpoint GoogleProvider#cloudbuildv2_custom_endpoint}.
        :param cloud_build_worker_pool_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_build_worker_pool_custom_endpoint GoogleProvider#cloud_build_worker_pool_custom_endpoint}.
        :param clouddeploy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#clouddeploy_custom_endpoint GoogleProvider#clouddeploy_custom_endpoint}.
        :param clouddomains_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#clouddomains_custom_endpoint GoogleProvider#clouddomains_custom_endpoint}.
        :param cloudfunctions2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloudfunctions2_custom_endpoint GoogleProvider#cloudfunctions2_custom_endpoint}.
        :param cloud_functions_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_functions_custom_endpoint GoogleProvider#cloud_functions_custom_endpoint}.
        :param cloud_identity_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_identity_custom_endpoint GoogleProvider#cloud_identity_custom_endpoint}.
        :param cloud_ids_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_ids_custom_endpoint GoogleProvider#cloud_ids_custom_endpoint}.
        :param cloud_quotas_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_quotas_custom_endpoint GoogleProvider#cloud_quotas_custom_endpoint}.
        :param cloud_resource_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_resource_manager_custom_endpoint GoogleProvider#cloud_resource_manager_custom_endpoint}.
        :param cloud_run_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_run_custom_endpoint GoogleProvider#cloud_run_custom_endpoint}.
        :param cloud_run_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_run_v2_custom_endpoint GoogleProvider#cloud_run_v2_custom_endpoint}.
        :param cloud_scheduler_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_scheduler_custom_endpoint GoogleProvider#cloud_scheduler_custom_endpoint}.
        :param cloud_tasks_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_tasks_custom_endpoint GoogleProvider#cloud_tasks_custom_endpoint}.
        :param colab_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#colab_custom_endpoint GoogleProvider#colab_custom_endpoint}.
        :param composer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#composer_custom_endpoint GoogleProvider#composer_custom_endpoint}.
        :param compute_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#compute_custom_endpoint GoogleProvider#compute_custom_endpoint}.
        :param contact_center_insights_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#contact_center_insights_custom_endpoint GoogleProvider#contact_center_insights_custom_endpoint}.
        :param container_analysis_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_analysis_custom_endpoint GoogleProvider#container_analysis_custom_endpoint}.
        :param container_attached_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_attached_custom_endpoint GoogleProvider#container_attached_custom_endpoint}.
        :param container_aws_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_aws_custom_endpoint GoogleProvider#container_aws_custom_endpoint}.
        :param container_azure_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_azure_custom_endpoint GoogleProvider#container_azure_custom_endpoint}.
        :param container_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_custom_endpoint GoogleProvider#container_custom_endpoint}.
        :param core_billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#core_billing_custom_endpoint GoogleProvider#core_billing_custom_endpoint}.
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#credentials GoogleProvider#credentials}.
        :param database_migration_service_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#database_migration_service_custom_endpoint GoogleProvider#database_migration_service_custom_endpoint}.
        :param data_catalog_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_catalog_custom_endpoint GoogleProvider#data_catalog_custom_endpoint}.
        :param dataflow_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataflow_custom_endpoint GoogleProvider#dataflow_custom_endpoint}.
        :param data_fusion_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_fusion_custom_endpoint GoogleProvider#data_fusion_custom_endpoint}.
        :param data_loss_prevention_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_loss_prevention_custom_endpoint GoogleProvider#data_loss_prevention_custom_endpoint}.
        :param data_pipeline_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_pipeline_custom_endpoint GoogleProvider#data_pipeline_custom_endpoint}.
        :param dataplex_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataplex_custom_endpoint GoogleProvider#dataplex_custom_endpoint}.
        :param dataproc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataproc_custom_endpoint GoogleProvider#dataproc_custom_endpoint}.
        :param dataproc_gdc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataproc_gdc_custom_endpoint GoogleProvider#dataproc_gdc_custom_endpoint}.
        :param dataproc_metastore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataproc_metastore_custom_endpoint GoogleProvider#dataproc_metastore_custom_endpoint}.
        :param datastream_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#datastream_custom_endpoint GoogleProvider#datastream_custom_endpoint}.
        :param default_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#default_labels GoogleProvider#default_labels}.
        :param deployment_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#deployment_manager_custom_endpoint GoogleProvider#deployment_manager_custom_endpoint}.
        :param developer_connect_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#developer_connect_custom_endpoint GoogleProvider#developer_connect_custom_endpoint}.
        :param dialogflow_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dialogflow_custom_endpoint GoogleProvider#dialogflow_custom_endpoint}.
        :param dialogflow_cx_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dialogflow_cx_custom_endpoint GoogleProvider#dialogflow_cx_custom_endpoint}.
        :param discovery_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#discovery_engine_custom_endpoint GoogleProvider#discovery_engine_custom_endpoint}.
        :param dns_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dns_custom_endpoint GoogleProvider#dns_custom_endpoint}.
        :param document_ai_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#document_ai_custom_endpoint GoogleProvider#document_ai_custom_endpoint}.
        :param document_ai_warehouse_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#document_ai_warehouse_custom_endpoint GoogleProvider#document_ai_warehouse_custom_endpoint}.
        :param edgecontainer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#edgecontainer_custom_endpoint GoogleProvider#edgecontainer_custom_endpoint}.
        :param edgenetwork_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#edgenetwork_custom_endpoint GoogleProvider#edgenetwork_custom_endpoint}.
        :param essential_contacts_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#essential_contacts_custom_endpoint GoogleProvider#essential_contacts_custom_endpoint}.
        :param eventarc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#eventarc_custom_endpoint GoogleProvider#eventarc_custom_endpoint}.
        :param external_credentials: external_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#external_credentials GoogleProvider#external_credentials}
        :param filestore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#filestore_custom_endpoint GoogleProvider#filestore_custom_endpoint}.
        :param firebase_app_check_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebase_app_check_custom_endpoint GoogleProvider#firebase_app_check_custom_endpoint}.
        :param firebase_app_hosting_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebase_app_hosting_custom_endpoint GoogleProvider#firebase_app_hosting_custom_endpoint}.
        :param firebase_data_connect_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebase_data_connect_custom_endpoint GoogleProvider#firebase_data_connect_custom_endpoint}.
        :param firebaserules_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebaserules_custom_endpoint GoogleProvider#firebaserules_custom_endpoint}.
        :param firestore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firestore_custom_endpoint GoogleProvider#firestore_custom_endpoint}.
        :param gemini_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gemini_custom_endpoint GoogleProvider#gemini_custom_endpoint}.
        :param gke_backup_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gke_backup_custom_endpoint GoogleProvider#gke_backup_custom_endpoint}.
        :param gke_hub2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gke_hub2_custom_endpoint GoogleProvider#gke_hub2_custom_endpoint}.
        :param gke_hub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gke_hub_custom_endpoint GoogleProvider#gke_hub_custom_endpoint}.
        :param gkehub_feature_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gkehub_feature_custom_endpoint GoogleProvider#gkehub_feature_custom_endpoint}.
        :param gkeonprem_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gkeonprem_custom_endpoint GoogleProvider#gkeonprem_custom_endpoint}.
        :param healthcare_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#healthcare_custom_endpoint GoogleProvider#healthcare_custom_endpoint}.
        :param iam2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam2_custom_endpoint GoogleProvider#iam2_custom_endpoint}.
        :param iam3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam3_custom_endpoint GoogleProvider#iam3_custom_endpoint}.
        :param iam_beta_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_beta_custom_endpoint GoogleProvider#iam_beta_custom_endpoint}.
        :param iam_credentials_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_credentials_custom_endpoint GoogleProvider#iam_credentials_custom_endpoint}.
        :param iam_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_custom_endpoint GoogleProvider#iam_custom_endpoint}.
        :param iam_workforce_pool_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_workforce_pool_custom_endpoint GoogleProvider#iam_workforce_pool_custom_endpoint}.
        :param iap_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iap_custom_endpoint GoogleProvider#iap_custom_endpoint}.
        :param identity_platform_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#identity_platform_custom_endpoint GoogleProvider#identity_platform_custom_endpoint}.
        :param impersonate_service_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#impersonate_service_account GoogleProvider#impersonate_service_account}.
        :param impersonate_service_account_delegates: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#impersonate_service_account_delegates GoogleProvider#impersonate_service_account_delegates}.
        :param integration_connectors_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#integration_connectors_custom_endpoint GoogleProvider#integration_connectors_custom_endpoint}.
        :param integrations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#integrations_custom_endpoint GoogleProvider#integrations_custom_endpoint}.
        :param kms_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#kms_custom_endpoint GoogleProvider#kms_custom_endpoint}.
        :param logging_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#logging_custom_endpoint GoogleProvider#logging_custom_endpoint}.
        :param looker_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#looker_custom_endpoint GoogleProvider#looker_custom_endpoint}.
        :param lustre_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#lustre_custom_endpoint GoogleProvider#lustre_custom_endpoint}.
        :param managed_kafka_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#managed_kafka_custom_endpoint GoogleProvider#managed_kafka_custom_endpoint}.
        :param memcache_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#memcache_custom_endpoint GoogleProvider#memcache_custom_endpoint}.
        :param memorystore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#memorystore_custom_endpoint GoogleProvider#memorystore_custom_endpoint}.
        :param migration_center_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#migration_center_custom_endpoint GoogleProvider#migration_center_custom_endpoint}.
        :param ml_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#ml_engine_custom_endpoint GoogleProvider#ml_engine_custom_endpoint}.
        :param model_armor_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#model_armor_custom_endpoint GoogleProvider#model_armor_custom_endpoint}.
        :param model_armor_global_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#model_armor_global_custom_endpoint GoogleProvider#model_armor_global_custom_endpoint}.
        :param monitoring_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#monitoring_custom_endpoint GoogleProvider#monitoring_custom_endpoint}.
        :param netapp_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#netapp_custom_endpoint GoogleProvider#netapp_custom_endpoint}.
        :param network_connectivity_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_connectivity_custom_endpoint GoogleProvider#network_connectivity_custom_endpoint}.
        :param network_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_management_custom_endpoint GoogleProvider#network_management_custom_endpoint}.
        :param network_security_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_security_custom_endpoint GoogleProvider#network_security_custom_endpoint}.
        :param network_services_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_services_custom_endpoint GoogleProvider#network_services_custom_endpoint}.
        :param notebooks_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#notebooks_custom_endpoint GoogleProvider#notebooks_custom_endpoint}.
        :param oracle_database_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#oracle_database_custom_endpoint GoogleProvider#oracle_database_custom_endpoint}.
        :param org_policy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#org_policy_custom_endpoint GoogleProvider#org_policy_custom_endpoint}.
        :param os_config_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#os_config_custom_endpoint GoogleProvider#os_config_custom_endpoint}.
        :param os_config_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#os_config_v2_custom_endpoint GoogleProvider#os_config_v2_custom_endpoint}.
        :param os_login_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#os_login_custom_endpoint GoogleProvider#os_login_custom_endpoint}.
        :param parallelstore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#parallelstore_custom_endpoint GoogleProvider#parallelstore_custom_endpoint}.
        :param parameter_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#parameter_manager_custom_endpoint GoogleProvider#parameter_manager_custom_endpoint}.
        :param parameter_manager_regional_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#parameter_manager_regional_custom_endpoint GoogleProvider#parameter_manager_regional_custom_endpoint}.
        :param privateca_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#privateca_custom_endpoint GoogleProvider#privateca_custom_endpoint}.
        :param privileged_access_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#privileged_access_manager_custom_endpoint GoogleProvider#privileged_access_manager_custom_endpoint}.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#project GoogleProvider#project}.
        :param public_ca_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#public_ca_custom_endpoint GoogleProvider#public_ca_custom_endpoint}.
        :param pubsub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#pubsub_custom_endpoint GoogleProvider#pubsub_custom_endpoint}.
        :param pubsub_lite_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#pubsub_lite_custom_endpoint GoogleProvider#pubsub_lite_custom_endpoint}.
        :param recaptcha_enterprise_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#recaptcha_enterprise_custom_endpoint GoogleProvider#recaptcha_enterprise_custom_endpoint}.
        :param redis_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#redis_custom_endpoint GoogleProvider#redis_custom_endpoint}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#region GoogleProvider#region}.
        :param request_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#request_reason GoogleProvider#request_reason}.
        :param request_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#request_timeout GoogleProvider#request_timeout}.
        :param resource_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#resource_manager_custom_endpoint GoogleProvider#resource_manager_custom_endpoint}.
        :param resource_manager_v3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#resource_manager_v3_custom_endpoint GoogleProvider#resource_manager_v3_custom_endpoint}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#scopes GoogleProvider#scopes}.
        :param secret_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#secret_manager_custom_endpoint GoogleProvider#secret_manager_custom_endpoint}.
        :param secret_manager_regional_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#secret_manager_regional_custom_endpoint GoogleProvider#secret_manager_regional_custom_endpoint}.
        :param secure_source_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#secure_source_manager_custom_endpoint GoogleProvider#secure_source_manager_custom_endpoint}.
        :param security_center_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#security_center_custom_endpoint GoogleProvider#security_center_custom_endpoint}.
        :param security_center_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#security_center_management_custom_endpoint GoogleProvider#security_center_management_custom_endpoint}.
        :param security_center_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#security_center_v2_custom_endpoint GoogleProvider#security_center_v2_custom_endpoint}.
        :param securityposture_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#securityposture_custom_endpoint GoogleProvider#securityposture_custom_endpoint}.
        :param service_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_management_custom_endpoint GoogleProvider#service_management_custom_endpoint}.
        :param service_networking_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_networking_custom_endpoint GoogleProvider#service_networking_custom_endpoint}.
        :param service_usage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_usage_custom_endpoint GoogleProvider#service_usage_custom_endpoint}.
        :param site_verification_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#site_verification_custom_endpoint GoogleProvider#site_verification_custom_endpoint}.
        :param source_repo_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#source_repo_custom_endpoint GoogleProvider#source_repo_custom_endpoint}.
        :param spanner_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#spanner_custom_endpoint GoogleProvider#spanner_custom_endpoint}.
        :param sql_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#sql_custom_endpoint GoogleProvider#sql_custom_endpoint}.
        :param storage_batch_operations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_batch_operations_custom_endpoint GoogleProvider#storage_batch_operations_custom_endpoint}.
        :param storage_control_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_control_custom_endpoint GoogleProvider#storage_control_custom_endpoint}.
        :param storage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_custom_endpoint GoogleProvider#storage_custom_endpoint}.
        :param storage_insights_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_insights_custom_endpoint GoogleProvider#storage_insights_custom_endpoint}.
        :param storage_transfer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_transfer_custom_endpoint GoogleProvider#storage_transfer_custom_endpoint}.
        :param tags_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#tags_custom_endpoint GoogleProvider#tags_custom_endpoint}.
        :param tags_location_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#tags_location_custom_endpoint GoogleProvider#tags_location_custom_endpoint}.
        :param terraform_attribution_label_addition_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#terraform_attribution_label_addition_strategy GoogleProvider#terraform_attribution_label_addition_strategy}.
        :param tpu_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#tpu_custom_endpoint GoogleProvider#tpu_custom_endpoint}.
        :param transcoder_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#transcoder_custom_endpoint GoogleProvider#transcoder_custom_endpoint}.
        :param universe_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#universe_domain GoogleProvider#universe_domain}.
        :param user_project_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#user_project_override GoogleProvider#user_project_override}.
        :param vertex_ai_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#vertex_ai_custom_endpoint GoogleProvider#vertex_ai_custom_endpoint}.
        :param vmwareengine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#vmwareengine_custom_endpoint GoogleProvider#vmwareengine_custom_endpoint}.
        :param vpc_access_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#vpc_access_custom_endpoint GoogleProvider#vpc_access_custom_endpoint}.
        :param workbench_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#workbench_custom_endpoint GoogleProvider#workbench_custom_endpoint}.
        :param workflows_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#workflows_custom_endpoint GoogleProvider#workflows_custom_endpoint}.
        :param zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#zone GoogleProvider#zone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9c9a462b0aa745ad035967b873d8ce6f7e44eb4d193e40fd943d1eb67b81e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = GoogleProviderConfig(
            access_approval_custom_endpoint=access_approval_custom_endpoint,
            access_context_manager_custom_endpoint=access_context_manager_custom_endpoint,
            access_token=access_token,
            active_directory_custom_endpoint=active_directory_custom_endpoint,
            add_terraform_attribution_label=add_terraform_attribution_label,
            alias=alias,
            alloydb_custom_endpoint=alloydb_custom_endpoint,
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
            contact_center_insights_custom_endpoint=contact_center_insights_custom_endpoint,
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
            firebase_data_connect_custom_endpoint=firebase_data_connect_custom_endpoint,
            firebaserules_custom_endpoint=firebaserules_custom_endpoint,
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
            model_armor_custom_endpoint=model_armor_custom_endpoint,
            model_armor_global_custom_endpoint=model_armor_global_custom_endpoint,
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
            resource_manager_custom_endpoint=resource_manager_custom_endpoint,
            resource_manager_v3_custom_endpoint=resource_manager_v3_custom_endpoint,
            scopes=scopes,
            secret_manager_custom_endpoint=secret_manager_custom_endpoint,
            secret_manager_regional_custom_endpoint=secret_manager_regional_custom_endpoint,
            secure_source_manager_custom_endpoint=secure_source_manager_custom_endpoint,
            security_center_custom_endpoint=security_center_custom_endpoint,
            security_center_management_custom_endpoint=security_center_management_custom_endpoint,
            security_center_v2_custom_endpoint=security_center_v2_custom_endpoint,
            securityposture_custom_endpoint=securityposture_custom_endpoint,
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
            transcoder_custom_endpoint=transcoder_custom_endpoint,
            universe_domain=universe_domain,
            user_project_override=user_project_override,
            vertex_ai_custom_endpoint=vertex_ai_custom_endpoint,
            vmwareengine_custom_endpoint=vmwareengine_custom_endpoint,
            vpc_access_custom_endpoint=vpc_access_custom_endpoint,
            workbench_custom_endpoint=workbench_custom_endpoint,
            workflows_custom_endpoint=workflows_custom_endpoint,
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
        '''Generates CDKTF code for importing a GoogleProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleProvider to import.
        :param import_from_id: The id of the existing GoogleProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e12059e57117a071bd42280927cce199ca1837d7c061b36cad0524aa493938)
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

    @jsii.member(jsii_name="resetContactCenterInsightsCustomEndpoint")
    def reset_contact_center_insights_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContactCenterInsightsCustomEndpoint", []))

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

    @jsii.member(jsii_name="resetFirebaseDataConnectCustomEndpoint")
    def reset_firebase_data_connect_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaseDataConnectCustomEndpoint", []))

    @jsii.member(jsii_name="resetFirebaserulesCustomEndpoint")
    def reset_firebaserules_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirebaserulesCustomEndpoint", []))

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

    @jsii.member(jsii_name="resetModelArmorCustomEndpoint")
    def reset_model_armor_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelArmorCustomEndpoint", []))

    @jsii.member(jsii_name="resetModelArmorGlobalCustomEndpoint")
    def reset_model_armor_global_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelArmorGlobalCustomEndpoint", []))

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

    @jsii.member(jsii_name="resetResourceManagerCustomEndpoint")
    def reset_resource_manager_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerCustomEndpoint", []))

    @jsii.member(jsii_name="resetResourceManagerV3CustomEndpoint")
    def reset_resource_manager_v3_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerV3CustomEndpoint", []))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderBatching"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderBatching"]]], jsii.get(self, "batchingInput"))

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
    @jsii.member(jsii_name="contactCenterInsightsCustomEndpointInput")
    def contact_center_insights_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactCenterInsightsCustomEndpointInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderExternalCredentials"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderExternalCredentials"]]], jsii.get(self, "externalCredentialsInput"))

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
    @jsii.member(jsii_name="firebaseDataConnectCustomEndpointInput")
    def firebase_data_connect_custom_endpoint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaseDataConnectCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="firebaserulesCustomEndpointInput")
    def firebaserules_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firebaserulesCustomEndpointInput"))

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
    @jsii.member(jsii_name="modelArmorCustomEndpointInput")
    def model_armor_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelArmorCustomEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="modelArmorGlobalCustomEndpointInput")
    def model_armor_global_custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelArmorGlobalCustomEndpointInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1a5c0adeec5de750c28add2a691b4ab7cb2f3e95e6488613d444fe55e6364d5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__015d2d431258e890010396e2cf315ef61276700a821d468f2afd05e8563c98d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessContextManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7638d43620391b024d55e540d69cbff6e41b8e48ef1237ee48d59927379e12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbac66b8848648dac2eb689252587ef2214ba3b79abdd0051854380846f4d4f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a9cae4ac1d3ffebb6c3aed6ab7d1552cb22650bfcef5254b2844ceded00b9ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addTerraformAttributionLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b5742bd7375a5efff231915d7f0e43c0856eecfb0e7a42d3f372e99fc34dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alloydbCustomEndpoint")
    def alloydb_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alloydbCustomEndpoint"))

    @alloydb_custom_endpoint.setter
    def alloydb_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e327a82a5adefc5195b48cd138c55f5bd06ceea3576cd7fef33e6464a261976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alloydbCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apigeeCustomEndpoint")
    def apigee_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apigeeCustomEndpoint"))

    @apigee_custom_endpoint.setter
    def apigee_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3cbfb662564ab3bcfd475ab8b074bdf09599c87ba3ab9cc682c3c21d709acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apigeeCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apihubCustomEndpoint")
    def apihub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apihubCustomEndpoint"))

    @apihub_custom_endpoint.setter
    def apihub_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee61df982220a8a44083010f2cded616f878f06b5f07dcb580189a375e532847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apihubCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apikeysCustomEndpoint")
    def apikeys_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apikeysCustomEndpoint"))

    @apikeys_custom_endpoint.setter
    def apikeys_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a98f3b7926c58a33cf0aa43f49ebe3cf6586638ebe6f621ef14dbcff5d397f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apikeysCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appEngineCustomEndpoint")
    def app_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appEngineCustomEndpoint"))

    @app_engine_custom_endpoint.setter
    def app_engine_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae9a98a94813329995757ec2600a43e8be3b12033b6d87b6699e88ed0b95724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appEngineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apphubCustomEndpoint")
    def apphub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apphubCustomEndpoint"))

    @apphub_custom_endpoint.setter
    def apphub_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c368d7994d3692a90cdeda59bdf3445c90a7bd462a53dd37e3c1b523ba85f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a14b55c4d9f184f418ee32b83a64466f9050331eec158b1d955848f035fd27d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89b6aa6c515b171800dd45441384f56ec577c3a79aa022df882d9dd922b88379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assuredWorkloadsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupDrCustomEndpoint")
    def backup_dr_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupDrCustomEndpoint"))

    @backup_dr_custom_endpoint.setter
    def backup_dr_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ba90efbb1e513e996feaa3aa39bfea2dffd001dff4fb52e54ed0ef03bf52a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupDrCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="batching")
    def batching(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderBatching"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderBatching"]]], jsii.get(self, "batching"))

    @batching.setter
    def batching(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderBatching"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83e36d866048786690a2c35886681b601c9e69aaad464c598d6eb7f6dc7b5ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="beyondcorpCustomEndpoint")
    def beyondcorp_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "beyondcorpCustomEndpoint"))

    @beyondcorp_custom_endpoint.setter
    def beyondcorp_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4d22b736f37213cc90cf0e8f962c13701762ffc4622195db3021eb5183e201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beyondcorpCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="biglakeCustomEndpoint")
    def biglake_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "biglakeCustomEndpoint"))

    @biglake_custom_endpoint.setter
    def biglake_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e832964c7789e90b2cfb9044c4e11069b0ca063a9f2412253197247ee3fac007)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1b504597e5425abf3440e942a2f94ec780ab7ad48355636e27ae605f9095824)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7961d901ebeddef40efe7b7dac34515d0aa4ef5d3b3ac423f7f43cbbbf90c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigqueryConnectionCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bigQueryCustomEndpoint")
    def big_query_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigQueryCustomEndpoint"))

    @big_query_custom_endpoint.setter
    def big_query_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d8b794072e370274ca7f8155047fdc15d74070a5e3704580e3ce4d73d1e639)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90671a4a892c98cc587328a8b5d42fcae2b29edc7209cdb893330b2a3f4953ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76a3ea9bfe743dd2a03c3fbf586fa13f8c8775661037ee44a01accaac84720e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a45f096e0b8dfcd471be3b1ab2f3e54046d34454374c29ffac5ff87270a431b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigqueryReservationCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bigtableCustomEndpoint")
    def bigtable_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bigtableCustomEndpoint"))

    @bigtable_custom_endpoint.setter
    def bigtable_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99cd8eceb26f3af475fcfadec2636d108c0523d2e1f3aa5867bb798734037284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bigtableCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingCustomEndpoint")
    def billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingCustomEndpoint"))

    @billing_custom_endpoint.setter
    def billing_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d47470ca7241ee9d4a0b73c87355bbcd9b95d36fe18896ddb8fe740c149527c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingProject")
    def billing_project(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingProject"))

    @billing_project.setter
    def billing_project(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa59053ee275d153b2e30d7d1c60dc51e1bdfcbf05e35111d5458ad424d64f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6fe93b9b505727a7e90189486be50f257fe4f743f6545b031ef2da715725290)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f07f0e1ba7c9afe93103041dcf9895dcc2ef5314b7bf1cf763c65ee803d3a46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__665011469859bd6c1a74abfb67ce4795061391e510bd79f72d769a305064b36e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="chronicleCustomEndpoint")
    def chronicle_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chronicleCustomEndpoint"))

    @chronicle_custom_endpoint.setter
    def chronicle_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a880df48ff11bc33c76ba0b2ee6d43649cb5ce3c010fa03ff1cc381e2100989d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chronicleCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudAssetCustomEndpoint")
    def cloud_asset_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudAssetCustomEndpoint"))

    @cloud_asset_custom_endpoint.setter
    def cloud_asset_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a744b835514d2f6ab428c376d0cd4054ddf6bdb1762cfc0e7fd1628f9f9e202)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab3b1d1bff2ac93dd75e2118219a364309450befa835605b3dddef0a471b6710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudBillingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudBuildCustomEndpoint")
    def cloud_build_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudBuildCustomEndpoint"))

    @cloud_build_custom_endpoint.setter
    def cloud_build_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b012c5c1b7b020f5c18d6a02543d6267853f7f892f4ac6961022378ed53773)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fc29988ebc5a48de273d8a3d4dca69faa6d716d6176aebc69244761acd57e68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdb06ef9f40d3ed363a8d1f1129bea2076189ad1a2d3a74d95650c6cf89f4861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudBuildWorkerPoolCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clouddeployCustomEndpoint")
    def clouddeploy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clouddeployCustomEndpoint"))

    @clouddeploy_custom_endpoint.setter
    def clouddeploy_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e1ebd675816a832a25d3fd917b7cfb67031f4a23296a92d153426ad3167356)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac7d8d5019969e564cc44b0467d0f8b07a3bc654e8553150149bdb38ae00e077)
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
            type_hints = typing.get_type_hints(_typecheckingstub__712bda9c3547471e6974d396cccb5badb0875aba0b40721fdfeb4874726cc475)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13011133ed46f8e7db78260a78c6d57b976c28fe87e47278c2813cbc9e166f80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2712e4e6ad6b2a71b3898570e9e8d17393cfa26f6f9f1f193b9bb3f3bc1c4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudIdentityCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudIdsCustomEndpoint")
    def cloud_ids_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudIdsCustomEndpoint"))

    @cloud_ids_custom_endpoint.setter
    def cloud_ids_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7407abeb13cdbd92caeca1c6f3d8ecc9ce935dfe6fbd66ddbb54a5b8aa616ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ba7e7065ec66ae3a85fa557249f3b7a7e151ca4a45c434cee7fb3b7b186e54a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15a6779183376badb7fb68aa3b671c81d0595c00c7470e0f781b2a3118751b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudResourceManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudRunCustomEndpoint")
    def cloud_run_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudRunCustomEndpoint"))

    @cloud_run_custom_endpoint.setter
    def cloud_run_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b28954f903a9da29ea29137b4d5da03123029dab0a29b7f1113957afc077eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d0791a599c39393da130e47dd364bbb69bd6358d6c18f3156396e4ddabff545)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecdb62174497b029aaec3b2eba50d435ea1a34b509c57f4079aa898349d06575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSchedulerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudTasksCustomEndpoint")
    def cloud_tasks_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudTasksCustomEndpoint"))

    @cloud_tasks_custom_endpoint.setter
    def cloud_tasks_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da2a1b1e6ee13147ce4cc9f0b07cb155ba1a5eb7f2225ac052dc74a7bada22fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudTasksCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="colabCustomEndpoint")
    def colab_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "colabCustomEndpoint"))

    @colab_custom_endpoint.setter
    def colab_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddcad339c3411726ea9b6f441802663f22e7f4b03e28598464653b8da9d36700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "colabCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="composerCustomEndpoint")
    def composer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "composerCustomEndpoint"))

    @composer_custom_endpoint.setter
    def composer_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9087460f92db4604c0d3b0f469733144dbe1154eed14dead87f6e7af07f160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "composerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computeCustomEndpoint")
    def compute_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeCustomEndpoint"))

    @compute_custom_endpoint.setter
    def compute_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e6f61e2368c7d162d1b8374ccf259b4b99e7880f864f18d2187c15caa8b852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contactCenterInsightsCustomEndpoint")
    def contact_center_insights_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactCenterInsightsCustomEndpoint"))

    @contact_center_insights_custom_endpoint.setter
    def contact_center_insights_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0265109bb4aac70755830fb08348d90e7de58f7e9b9c74146ba6001740803dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactCenterInsightsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__522176c0806e7e8066d071f7ffb3537aa5cfb0b70e3b5216daf2a4ded9f4f5b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__076fdca6833b704682b86bebe74630155f60b7204d0045bdf15fc7ac2f52c8f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1180a66777f400fa458db866a0e8c16ab180ab409a6e93e1607896bb5ee4717)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b86bb78dea946f6067c0307e3b96d84ec87f3940d21e651413b5c361da5c41ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerAzureCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerCustomEndpoint")
    def container_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerCustomEndpoint"))

    @container_custom_endpoint.setter
    def container_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d041736f02803f109e96ba7c4a82f4721b53c9b0d6e27f5dcc779681c9083a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df9abb92094f9bf1bcce5efd8202a087b9f16de2578a0655ad5311e5dce74bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreBillingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09248dab6ce94044e6bafa4fd7c402e7bfd17b15d8c72668ea1871db5269d827)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40feaa91b82dcfbbf3c8fd113255ac6ab570e4ea9d2fc3ae7fc3466f63e740ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__619e71adfabec4d4492249d8a32aad64d7c27e69f326636f82b79cb91c6cc891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataCatalogCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataflowCustomEndpoint")
    def dataflow_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataflowCustomEndpoint"))

    @dataflow_custom_endpoint.setter
    def dataflow_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df3ac65dec3328ed80e81fdf5315a7c13417e5a77488e6593b51c2eb12dfbff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataflowCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFusionCustomEndpoint")
    def data_fusion_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFusionCustomEndpoint"))

    @data_fusion_custom_endpoint.setter
    def data_fusion_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391641acc421be6f8021ba8d6e952b672b3212b0ee32b15d68d072bf9ebadb6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c6f81f61ac78a9cbebf178d6db637370e7501e9d699d111245a0400c6e22285)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74fceefeee935a2375eb957491952f05085ff61b8dffd123eef32bc53c4d71dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataPipelineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataplexCustomEndpoint")
    def dataplex_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataplexCustomEndpoint"))

    @dataplex_custom_endpoint.setter
    def dataplex_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3faf38f30bbdfe9f381489bb4008915f29d60a8f6a728180e930afdd9bdd3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataplexCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataprocCustomEndpoint")
    def dataproc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocCustomEndpoint"))

    @dataproc_custom_endpoint.setter
    def dataproc_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3528437c1bbcb2144d8c5ea59b0e35ec0f6073e397e5469ced79a9de4b0f8bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9ba6747f8a38483d609c25f942dea439e0bc5f4c4cd4d224941e8430dcac82b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b9035dac9bcb2912016af684886d2fe6c662ea57a69a84b780909090bb0c63e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocMetastoreCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datastreamCustomEndpoint")
    def datastream_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datastreamCustomEndpoint"))

    @datastream_custom_endpoint.setter
    def datastream_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8001af4c89858bf318038e47ffd1808cb8e77528efc966cd9438e33f7eebc99f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71c7380e3793eb0577f1f3a0e57ddb9625fc13cea75eef00c62f83129dd49327)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0cfd2529237ec1c053ad3ca52ace8bb213c6401075ee99e95fead89d1be39d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__675d323b83f5eb76d03096ec8459a6959cc4f4276d02b1f1c788269a4845ecb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developerConnectCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dialogflowCustomEndpoint")
    def dialogflow_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dialogflowCustomEndpoint"))

    @dialogflow_custom_endpoint.setter
    def dialogflow_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2b2448205898541fe606c44189a648fc5da67d471dcfcfa2f8c85e2f9e0099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e77285d7604904c73c72143c4382154f849a10552f8f040c19650327535f423a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bb1732d2de0c1ad24c0967ec9feb89b40a45987e5e540c841bc4a333567e552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discoveryEngineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsCustomEndpoint")
    def dns_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsCustomEndpoint"))

    @dns_custom_endpoint.setter
    def dns_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7534d48fcb48096aa9d64c1a4a813ba4986bb226ca4722faa786a752fa7f9987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentAiCustomEndpoint")
    def document_ai_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentAiCustomEndpoint"))

    @document_ai_custom_endpoint.setter
    def document_ai_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f3e42f3a1181b3709d477443e501ddf376abc27a2d5b33fe24a8c8ede78ccd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a359f3bd78e05fdd16e941f2c9ffc63e2227aa1d0ac03d47a280e9a555d8e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__871090028ccd9e4e77e4fb29de74b41d90caaf9631caef9cfe31a3b256266531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgecontainerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgenetworkCustomEndpoint")
    def edgenetwork_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgenetworkCustomEndpoint"))

    @edgenetwork_custom_endpoint.setter
    def edgenetwork_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51bcd247d127d5329e160ccaaa8082bd27c48ae70778c377570495a2760f9cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51e94722796e7de48e9cec699d7b62841736683f0203599f2086dfd5d8e95673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "essentialContactsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventarcCustomEndpoint")
    def eventarc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventarcCustomEndpoint"))

    @eventarc_custom_endpoint.setter
    def eventarc_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf6b8ee1ac57d9f73e270560d3374673df2d9b5682a2d69151f98d47f662359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventarcCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalCredentials")
    def external_credentials(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderExternalCredentials"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderExternalCredentials"]]], jsii.get(self, "externalCredentials"))

    @external_credentials.setter
    def external_credentials(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderExternalCredentials"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f2cf2bebbaf5f57ec28eaa324895d1714a39e2bc62426b729e69da11e6bad9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filestoreCustomEndpoint")
    def filestore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filestoreCustomEndpoint"))

    @filestore_custom_endpoint.setter
    def filestore_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f8081f7f042d9b185fedcd6eda325eb348c42541231f447aa1a01057ed04cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb55fb7ffb701e5847aeae055ab4166c529af64eac6ac162e1a42daa5b10f53f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__006126d4b1929d76173ffe0c3662e8b52d3de536cd9057ccf853f9a491c0d9f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseAppHostingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__a5a8b538b225e3f6b01686039c118c744872f140cc631a3ef73cf808298ea578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaseDataConnectCustomEndpoint", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0089ea10e48efb5cf6c87c39eb3ba3fb28bd98bb315cc2226338cbd8cedece8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firebaserulesCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firestoreCustomEndpoint")
    def firestore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firestoreCustomEndpoint"))

    @firestore_custom_endpoint.setter
    def firestore_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5aceffbff7a2a626aa463dd3219bbea8ade3cc12f09fd8a33d9b74414062b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firestoreCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geminiCustomEndpoint")
    def gemini_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geminiCustomEndpoint"))

    @gemini_custom_endpoint.setter
    def gemini_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f48706c44ec50fe94a481cdd9cbce32fcb3bf00ea90de0e29616a1e9958f1dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geminiCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeBackupCustomEndpoint")
    def gke_backup_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeBackupCustomEndpoint"))

    @gke_backup_custom_endpoint.setter
    def gke_backup_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a04ff8ad54bb3804c09695b20e20a671d5ffd94b3c1adae7b992048abb5625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeBackupCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeHub2CustomEndpoint")
    def gke_hub2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeHub2CustomEndpoint"))

    @gke_hub2_custom_endpoint.setter
    def gke_hub2_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4928ddf1b51286a8d198d94a645c5a8d67f55a6bdfcb8906942c041a1098e344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeHub2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeHubCustomEndpoint")
    def gke_hub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeHubCustomEndpoint"))

    @gke_hub_custom_endpoint.setter
    def gke_hub_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28aa3645f33c06e0f54f95637f8ecaaea04e267bf3a91a8c0dee07f8b41d7c96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aefbaa2f7b10493075a5133e27774ea3ddfff27775a5fd85e2fd661b9399ea5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkehubFeatureCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeonpremCustomEndpoint")
    def gkeonprem_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeonpremCustomEndpoint"))

    @gkeonprem_custom_endpoint.setter
    def gkeonprem_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e76c30954749804826b4e29ae01fb32e276e766a82fa1b5bed31dba4752c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeonpremCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthcareCustomEndpoint")
    def healthcare_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthcareCustomEndpoint"))

    @healthcare_custom_endpoint.setter
    def healthcare_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c20f4794b1722b4fc53caf935b1406b157d1549af3db010f15d2b258eef642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthcareCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iam2CustomEndpoint")
    def iam2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iam2CustomEndpoint"))

    @iam2_custom_endpoint.setter
    def iam2_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58e429e2630752cf97b74243523a313d21a8a54815bbb48badf69f11a9a9c17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iam2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iam3CustomEndpoint")
    def iam3_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iam3CustomEndpoint"))

    @iam3_custom_endpoint.setter
    def iam3_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da82c4bd1e2111eb7f19616d468b2bb8278497e8a549de56eb339b9ed34b003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iam3CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamBetaCustomEndpoint")
    def iam_beta_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamBetaCustomEndpoint"))

    @iam_beta_custom_endpoint.setter
    def iam_beta_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52c049e83201a4750f222474eefce4fcdaada014c812a436ebce3b82b8fc345)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5fc5fb6135530545bbce339ecae493adc95b5de067ac7ace1a7b75c973c5467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamCredentialsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamCustomEndpoint")
    def iam_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamCustomEndpoint"))

    @iam_custom_endpoint.setter
    def iam_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9478fed36fbf22f7a44247c1feb4087038be0d4fd6d030608ef86c5686672788)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35a91cdf0add467e75b877fd1f39db09a9608d3faba6405c1120224f28c6063d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamWorkforcePoolCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iapCustomEndpoint")
    def iap_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iapCustomEndpoint"))

    @iap_custom_endpoint.setter
    def iap_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d4c6e1ca836c04d10a290089103d93aabbae66b0deb3c23a8158b8dd140b1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d468e61d57002257de6c6a08668e53527861d7bddac55da9084fa95cc06dd45b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityPlatformCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="impersonateServiceAccount")
    def impersonate_service_account(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "impersonateServiceAccount"))

    @impersonate_service_account.setter
    def impersonate_service_account(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568ada9920b0bfce948c0da6826a420d3f7a74956a21673ac7d6479c5ac6885d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1be1fc705df36f6e49b32b17ef0814acd804821447ae5b496b792610e47af71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e68cc01615a8434b089a3b480d8b1c76322eb381bf8263487bc00007398ebee0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76abd832ed695cf5d1412e48c20593d9c2a564ba29f1ac265377cf7747a7708b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsCustomEndpoint")
    def kms_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsCustomEndpoint"))

    @kms_custom_endpoint.setter
    def kms_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3139a9d40cb619878fbfe2fcb47485f53f84841e51d28ae3bc8f13eea1dffac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingCustomEndpoint")
    def logging_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingCustomEndpoint"))

    @logging_custom_endpoint.setter
    def logging_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7731c0d4060e2ca44156636f3f3970c5811f552d1d2834c16d5239b780c6d43a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lookerCustomEndpoint")
    def looker_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lookerCustomEndpoint"))

    @looker_custom_endpoint.setter
    def looker_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57cf7387c16897db7f45328c505270aef993cfe2be4d0c1822894648a7a0b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lustreCustomEndpoint")
    def lustre_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lustreCustomEndpoint"))

    @lustre_custom_endpoint.setter
    def lustre_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b887ae5391a7ed74a6adf51a7d0b55f26422ed3b400a57c6db3df9d0e851c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95e2fe0591708aa50224b35bbf119421239eeb99a7b1031098c75dc29f4fa792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedKafkaCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memcacheCustomEndpoint")
    def memcache_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memcacheCustomEndpoint"))

    @memcache_custom_endpoint.setter
    def memcache_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa59586f46e9143e1f0199911a4b00fbbc8b63e5a0b95b7f9328653f7fb81d82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memcacheCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorystoreCustomEndpoint")
    def memorystore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memorystoreCustomEndpoint"))

    @memorystore_custom_endpoint.setter
    def memorystore_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99eafbfbcecbc80f3e5730b7111f11bc141a7d1db93e46865e811a65cda285b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eba1150671085cd70dea78679985498e6792b89421e0dfcae8ff0d4d401e7f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "migrationCenterCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mlEngineCustomEndpoint")
    def ml_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mlEngineCustomEndpoint"))

    @ml_engine_custom_endpoint.setter
    def ml_engine_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29eed68ed05f67b6986d852e1645eab423fa4edfa5f833074edd2cd8ae9c231a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mlEngineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelArmorCustomEndpoint")
    def model_armor_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelArmorCustomEndpoint"))

    @model_armor_custom_endpoint.setter
    def model_armor_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0ee5315298bbb87e8a8323ddd20b8e0af65d6b3b9d71d1c1d603012a331398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelArmorCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelArmorGlobalCustomEndpoint")
    def model_armor_global_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelArmorGlobalCustomEndpoint"))

    @model_armor_global_custom_endpoint.setter
    def model_armor_global_custom_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea3fad4627a7fd80135c9a5fe4b92448802bc64323f89b523a31c76c17710d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelArmorGlobalCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitoringCustomEndpoint")
    def monitoring_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitoringCustomEndpoint"))

    @monitoring_custom_endpoint.setter
    def monitoring_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d719e90211c978316d9872d02c04242550051a1f29289e224747017524cbf8b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoringCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netappCustomEndpoint")
    def netapp_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netappCustomEndpoint"))

    @netapp_custom_endpoint.setter
    def netapp_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941fd8a6b3a88916ebe4156c48b5723da6cace555f27f0e4d19c31f29d51c46c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13135ac3e35dbb874a13fc79d607d6d11384cfc54b7f1630a808a0e08352e331)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a9387b6b59f9cafb8c4638d6a660666cf94bbabaf9db0a453bbb49d4cb0fb33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f200096e548e00c0c02c77845b4879afb7aac3ee15ac04a643135fec855ad3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7439d289ae5d1f92fa0f52bb378302e5b40a0db13f2d20859e25dbef25980ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkServicesCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebooksCustomEndpoint")
    def notebooks_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebooksCustomEndpoint"))

    @notebooks_custom_endpoint.setter
    def notebooks_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf2a4afc85ca8cf2eb2932ed85dce47dbeaa0b03904b8ffcf9458012cc86c04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23749ed50f4c62f332bb5351b3648296006c57adeb02944bcc01bdf3944d3134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oracleDatabaseCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgPolicyCustomEndpoint")
    def org_policy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgPolicyCustomEndpoint"))

    @org_policy_custom_endpoint.setter
    def org_policy_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d28fde2e261d6c0cb07afb0c412f5d040260e5ea2007dc0a8f2019938185cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgPolicyCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osConfigCustomEndpoint")
    def os_config_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osConfigCustomEndpoint"))

    @os_config_custom_endpoint.setter
    def os_config_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b08b69f26b387eeb22b91d23cc47e8ed978a7da353ad776e1917c2d66da4806)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78eb7ad5f06712d9564748d04e3efa29352fed51ece6051737d9049de98aea04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osConfigV2CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osLoginCustomEndpoint")
    def os_login_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osLoginCustomEndpoint"))

    @os_login_custom_endpoint.setter
    def os_login_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3f44f9d990a27d03bfce2e5e7fef851ab7ac55aea35512fa7cea8710635c9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe4529d157143410240ce0a48077901da70c9418b167d0654d1795e205c2e1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53cfce5d62d084bc1890ee051bda67988ce1c9e413c32a7cc17c22f74c833010)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5c4d458b5ec6bb315d1a545eca7f349330a467846e429645397d0712f4b472e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterManagerRegionalCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privatecaCustomEndpoint")
    def privateca_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privatecaCustomEndpoint"))

    @privateca_custom_endpoint.setter
    def privateca_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3f0734c5f8bd154845a06db218dc5b58b1f83bf46dad778b648a52f58c3d01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff501d0d66a8eea80c4be567217a15bb5f907eaf2a9bc6cf0233ec70d509b69f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privilegedAccessManagerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "project"))

    @project.setter
    def project(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9f9ac025c9d8905713d1fb6002b96da1db5674e5e76f7d797ae8ea7ed40b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicCaCustomEndpoint")
    def public_ca_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicCaCustomEndpoint"))

    @public_ca_custom_endpoint.setter
    def public_ca_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85493ad87918295a9b34818e76f60d3de86c87d501c07287fc522bda13ebb89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicCaCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubCustomEndpoint")
    def pubsub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubCustomEndpoint"))

    @pubsub_custom_endpoint.setter
    def pubsub_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfcc682bbdbd95dca76e4af07ce9695bb27043a232e61dd4e109b58d031860f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubLiteCustomEndpoint")
    def pubsub_lite_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubLiteCustomEndpoint"))

    @pubsub_lite_custom_endpoint.setter
    def pubsub_lite_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5326db7210f292d6ae8495808ff6a8fa569c3d34108dc242fbeb69375a00c5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb745ced4d24320d9a2087477c10be8f6729eba2d1aeec402151743c6e717386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recaptchaEnterpriseCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redisCustomEndpoint")
    def redis_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisCustomEndpoint"))

    @redis_custom_endpoint.setter
    def redis_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac62be79a428868d52f7451d398261c22d1b201c35ee90b141db961de426c56b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @region.setter
    def region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d40b4cbd3ef1cff0c73baefeda79a5665a0942ab0bc1dc4f32cb4fa51190a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestReason")
    def request_reason(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestReason"))

    @request_reason.setter
    def request_reason(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3105209a782ca83ea40369e72ba8b48da281e77be0b94d5cb2ecd792d818ad38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestTimeout")
    def request_timeout(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestTimeout"))

    @request_timeout.setter
    def request_timeout(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e836f7bca51071f5f8efe393ec9aa4a91419126f6e2275f13f06e5a48bfe118a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestTimeout", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__806d04f231bf3ea05dd54c78bff1be61b3a0a130068bb5cff0b89aca87fff4c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f84e7555494d51a38353b2867373a5cc6306935cb538ad35c91321ac31d3f48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerV3CustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa487fd257ff1e1516ada743f366a2a884f633bc42debadee158f8632cdd857)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ba81ae96e33c174eb1e23b05805f13249f90cbb56de48578e3c9add7ebffb51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0af85b4f306a918c8435a7be2f360d1cb4852a5da77c75acf9c6bbef4ef03ad5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4be5aef0fe1bc14407f10f8ccc3440991676c092a973c4e4f68aad6df4b32615)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c7cf001c57b4df72acf38ab2c03892e7458841e76be009d9d9bc62b07766902)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce7ca9563a58043e4cd5148f94d7822fac438ee00249ae01b5a15ad37b585202)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45da06525905cfb679f6389b8e8de3dbccee22ed08781223a783db9e7e25a1a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d80ceb9f8dddab2adbee6158cbade2aa7f626691f736e7bd8aed27bffde1f862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securitypostureCustomEndpoint", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__1093c258b75a9133610048d4f99f8a047ac789d01e27788e428d7723f2a79e98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48b4938055764d3c2be71cdab4e434385656bb5e4b8e1698a952bf1faab468f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42bcb649cc59102425c20a123669a2f5da7104de071c7b4ea0ff53db8ad24673)
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
            type_hints = typing.get_type_hints(_typecheckingstub__126d55833b48dfaba45f164fcf19ef314011d2a3e945639da122a240d249c414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteVerificationCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRepoCustomEndpoint")
    def source_repo_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRepoCustomEndpoint"))

    @source_repo_custom_endpoint.setter
    def source_repo_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de3815d6d66cdc511904c846ca718c9d7b43e60e3c806967bf732ca16f89f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRepoCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spannerCustomEndpoint")
    def spanner_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spannerCustomEndpoint"))

    @spanner_custom_endpoint.setter
    def spanner_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28064a67f72a7aa1b54559f681d2bf48d5cbfecf85ebb753bb54e016d449eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spannerCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlCustomEndpoint")
    def sql_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlCustomEndpoint"))

    @sql_custom_endpoint.setter
    def sql_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d838260ea73128cc4d5f9a1e9e5bd4c99fef65af703ba52f338de1fe168dab0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ae3d16359ce356e5a84c8c896b4e85560dc4b567df63d136b46b7654d346110)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4baa66f16e5ba74871553d8a9674036208e1fb256c65cbdb141b79294168d480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageControlCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageCustomEndpoint")
    def storage_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageCustomEndpoint"))

    @storage_custom_endpoint.setter
    def storage_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a31e83b9623c1f365445ae8d8669516b7b64a0fd3ac89464142505d6d80aaa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc21283e39e3971327a5e8014bdec0157a7cc4fa5fd2fef8d455d4a124ec924b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9e17f3e33ac5b1685c8e27a5d617ac8798056892e7ab860964be96d7545dcea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageTransferCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsCustomEndpoint")
    def tags_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagsCustomEndpoint"))

    @tags_custom_endpoint.setter
    def tags_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1256a9557712bfd0ce3e07ca962b7057b4676a649fdae8f2f5fa0543fcd1e461)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91b413ca8a9edc6d38ddb72add779c618b03c531b6aa989b8529bfe74ef7adb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6133d4127c14311988f68fbf1dbe99efa3d4216063c3ea926b794f9400d3b2e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttributionLabelAdditionStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tpuCustomEndpoint")
    def tpu_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpuCustomEndpoint"))

    @tpu_custom_endpoint.setter
    def tpu_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49794f801e9500da11330bfeafe13807f17c98fff9961ee43290951ed01878c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpuCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transcoderCustomEndpoint")
    def transcoder_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transcoderCustomEndpoint"))

    @transcoder_custom_endpoint.setter
    def transcoder_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ec2c45cdf665b34c663fa359efb82bc5121e938042c0dedf8284d235bebe28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transcoderCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="universeDomain")
    def universe_domain(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "universeDomain"))

    @universe_domain.setter
    def universe_domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc0cef22329f2de38915eaa47dbbb49692444a7ef410d58cb19f3850a16a882)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3ecdeb22e978c397b4e226d79b6bcad8aa325840214c2426b4b05e91490bf0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userProjectOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vertexAiCustomEndpoint")
    def vertex_ai_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vertexAiCustomEndpoint"))

    @vertex_ai_custom_endpoint.setter
    def vertex_ai_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea2883d4937f94b4f36339087606fa726253d0ff9913e85205c5b342d096cd9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a6e517ee6458896d38d4faac90e73aeaf0d490a9cc3d6914f93b64d8031983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmwareengineCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcAccessCustomEndpoint")
    def vpc_access_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcAccessCustomEndpoint"))

    @vpc_access_custom_endpoint.setter
    def vpc_access_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88234b92931a104d47c6cf5c02ffecc7f049229430994128bc4b2728b750237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcAccessCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workbenchCustomEndpoint")
    def workbench_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workbenchCustomEndpoint"))

    @workbench_custom_endpoint.setter
    def workbench_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176398c41aee01e6ad94b0b6dfa63ad6b99602dc0434be5363fc5c5854832590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workbenchCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workflowsCustomEndpoint")
    def workflows_custom_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowsCustomEndpoint"))

    @workflows_custom_endpoint.setter
    def workflows_custom_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ea2d953395eaa15371d19df3e4449ac4bf2cf63e2806cf30667b70950845ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflowsCustomEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f97ccc5e86abdcbc07d3f426b0c7ed9e4510476fd420a978f3884ab31230f8b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.provider.GoogleProviderBatching",
    jsii_struct_bases=[],
    name_mapping={"enable_batching": "enableBatching", "send_after": "sendAfter"},
)
class GoogleProviderBatching:
    def __init__(
        self,
        *,
        enable_batching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_after: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_batching: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#enable_batching GoogleProvider#enable_batching}.
        :param send_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#send_after GoogleProvider#send_after}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3956bddf410c41cab7d5dc93225b07c0b6a12cc9a13b463c21d4d2453de874f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#enable_batching GoogleProvider#enable_batching}.'''
        result = self._values.get("enable_batching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_after(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#send_after GoogleProvider#send_after}.'''
        result = self._values.get("send_after")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleProviderBatching(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.provider.GoogleProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_approval_custom_endpoint": "accessApprovalCustomEndpoint",
        "access_context_manager_custom_endpoint": "accessContextManagerCustomEndpoint",
        "access_token": "accessToken",
        "active_directory_custom_endpoint": "activeDirectoryCustomEndpoint",
        "add_terraform_attribution_label": "addTerraformAttributionLabel",
        "alias": "alias",
        "alloydb_custom_endpoint": "alloydbCustomEndpoint",
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
        "contact_center_insights_custom_endpoint": "contactCenterInsightsCustomEndpoint",
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
        "firebase_data_connect_custom_endpoint": "firebaseDataConnectCustomEndpoint",
        "firebaserules_custom_endpoint": "firebaserulesCustomEndpoint",
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
        "model_armor_custom_endpoint": "modelArmorCustomEndpoint",
        "model_armor_global_custom_endpoint": "modelArmorGlobalCustomEndpoint",
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
        "resource_manager_custom_endpoint": "resourceManagerCustomEndpoint",
        "resource_manager_v3_custom_endpoint": "resourceManagerV3CustomEndpoint",
        "scopes": "scopes",
        "secret_manager_custom_endpoint": "secretManagerCustomEndpoint",
        "secret_manager_regional_custom_endpoint": "secretManagerRegionalCustomEndpoint",
        "secure_source_manager_custom_endpoint": "secureSourceManagerCustomEndpoint",
        "security_center_custom_endpoint": "securityCenterCustomEndpoint",
        "security_center_management_custom_endpoint": "securityCenterManagementCustomEndpoint",
        "security_center_v2_custom_endpoint": "securityCenterV2CustomEndpoint",
        "securityposture_custom_endpoint": "securitypostureCustomEndpoint",
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
        "transcoder_custom_endpoint": "transcoderCustomEndpoint",
        "universe_domain": "universeDomain",
        "user_project_override": "userProjectOverride",
        "vertex_ai_custom_endpoint": "vertexAiCustomEndpoint",
        "vmwareengine_custom_endpoint": "vmwareengineCustomEndpoint",
        "vpc_access_custom_endpoint": "vpcAccessCustomEndpoint",
        "workbench_custom_endpoint": "workbenchCustomEndpoint",
        "workflows_custom_endpoint": "workflowsCustomEndpoint",
        "zone": "zone",
    },
)
class GoogleProviderConfig:
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
        apigee_custom_endpoint: typing.Optional[builtins.str] = None,
        apihub_custom_endpoint: typing.Optional[builtins.str] = None,
        apikeys_custom_endpoint: typing.Optional[builtins.str] = None,
        app_engine_custom_endpoint: typing.Optional[builtins.str] = None,
        apphub_custom_endpoint: typing.Optional[builtins.str] = None,
        artifact_registry_custom_endpoint: typing.Optional[builtins.str] = None,
        assured_workloads_custom_endpoint: typing.Optional[builtins.str] = None,
        backup_dr_custom_endpoint: typing.Optional[builtins.str] = None,
        batching: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleProviderBatching, typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        contact_center_insights_custom_endpoint: typing.Optional[builtins.str] = None,
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
        external_credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleProviderExternalCredentials", typing.Dict[builtins.str, typing.Any]]]]] = None,
        filestore_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_app_check_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_app_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
        firebase_data_connect_custom_endpoint: typing.Optional[builtins.str] = None,
        firebaserules_custom_endpoint: typing.Optional[builtins.str] = None,
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
        model_armor_custom_endpoint: typing.Optional[builtins.str] = None,
        model_armor_global_custom_endpoint: typing.Optional[builtins.str] = None,
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
        resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        resource_manager_v3_custom_endpoint: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        secret_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
        secure_source_manager_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_management_custom_endpoint: typing.Optional[builtins.str] = None,
        security_center_v2_custom_endpoint: typing.Optional[builtins.str] = None,
        securityposture_custom_endpoint: typing.Optional[builtins.str] = None,
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
        transcoder_custom_endpoint: typing.Optional[builtins.str] = None,
        universe_domain: typing.Optional[builtins.str] = None,
        user_project_override: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vertex_ai_custom_endpoint: typing.Optional[builtins.str] = None,
        vmwareengine_custom_endpoint: typing.Optional[builtins.str] = None,
        vpc_access_custom_endpoint: typing.Optional[builtins.str] = None,
        workbench_custom_endpoint: typing.Optional[builtins.str] = None,
        workflows_custom_endpoint: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_approval_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#access_approval_custom_endpoint GoogleProvider#access_approval_custom_endpoint}.
        :param access_context_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#access_context_manager_custom_endpoint GoogleProvider#access_context_manager_custom_endpoint}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#access_token GoogleProvider#access_token}.
        :param active_directory_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#active_directory_custom_endpoint GoogleProvider#active_directory_custom_endpoint}.
        :param add_terraform_attribution_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#add_terraform_attribution_label GoogleProvider#add_terraform_attribution_label}.
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#alias GoogleProvider#alias}
        :param alloydb_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#alloydb_custom_endpoint GoogleProvider#alloydb_custom_endpoint}.
        :param apigee_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apigee_custom_endpoint GoogleProvider#apigee_custom_endpoint}.
        :param apihub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apihub_custom_endpoint GoogleProvider#apihub_custom_endpoint}.
        :param apikeys_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apikeys_custom_endpoint GoogleProvider#apikeys_custom_endpoint}.
        :param app_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#app_engine_custom_endpoint GoogleProvider#app_engine_custom_endpoint}.
        :param apphub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apphub_custom_endpoint GoogleProvider#apphub_custom_endpoint}.
        :param artifact_registry_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#artifact_registry_custom_endpoint GoogleProvider#artifact_registry_custom_endpoint}.
        :param assured_workloads_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#assured_workloads_custom_endpoint GoogleProvider#assured_workloads_custom_endpoint}.
        :param backup_dr_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#backup_dr_custom_endpoint GoogleProvider#backup_dr_custom_endpoint}.
        :param batching: batching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#batching GoogleProvider#batching}
        :param beyondcorp_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#beyondcorp_custom_endpoint GoogleProvider#beyondcorp_custom_endpoint}.
        :param biglake_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#biglake_custom_endpoint GoogleProvider#biglake_custom_endpoint}.
        :param bigquery_analytics_hub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_analytics_hub_custom_endpoint GoogleProvider#bigquery_analytics_hub_custom_endpoint}.
        :param bigquery_connection_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_connection_custom_endpoint GoogleProvider#bigquery_connection_custom_endpoint}.
        :param big_query_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#big_query_custom_endpoint GoogleProvider#big_query_custom_endpoint}.
        :param bigquery_datapolicy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_datapolicy_custom_endpoint GoogleProvider#bigquery_datapolicy_custom_endpoint}.
        :param bigquery_data_transfer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_data_transfer_custom_endpoint GoogleProvider#bigquery_data_transfer_custom_endpoint}.
        :param bigquery_reservation_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_reservation_custom_endpoint GoogleProvider#bigquery_reservation_custom_endpoint}.
        :param bigtable_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigtable_custom_endpoint GoogleProvider#bigtable_custom_endpoint}.
        :param billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#billing_custom_endpoint GoogleProvider#billing_custom_endpoint}.
        :param billing_project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#billing_project GoogleProvider#billing_project}.
        :param binary_authorization_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#binary_authorization_custom_endpoint GoogleProvider#binary_authorization_custom_endpoint}.
        :param blockchain_node_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#blockchain_node_engine_custom_endpoint GoogleProvider#blockchain_node_engine_custom_endpoint}.
        :param certificate_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#certificate_manager_custom_endpoint GoogleProvider#certificate_manager_custom_endpoint}.
        :param chronicle_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#chronicle_custom_endpoint GoogleProvider#chronicle_custom_endpoint}.
        :param cloud_asset_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_asset_custom_endpoint GoogleProvider#cloud_asset_custom_endpoint}.
        :param cloud_billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_billing_custom_endpoint GoogleProvider#cloud_billing_custom_endpoint}.
        :param cloud_build_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_build_custom_endpoint GoogleProvider#cloud_build_custom_endpoint}.
        :param cloudbuildv2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloudbuildv2_custom_endpoint GoogleProvider#cloudbuildv2_custom_endpoint}.
        :param cloud_build_worker_pool_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_build_worker_pool_custom_endpoint GoogleProvider#cloud_build_worker_pool_custom_endpoint}.
        :param clouddeploy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#clouddeploy_custom_endpoint GoogleProvider#clouddeploy_custom_endpoint}.
        :param clouddomains_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#clouddomains_custom_endpoint GoogleProvider#clouddomains_custom_endpoint}.
        :param cloudfunctions2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloudfunctions2_custom_endpoint GoogleProvider#cloudfunctions2_custom_endpoint}.
        :param cloud_functions_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_functions_custom_endpoint GoogleProvider#cloud_functions_custom_endpoint}.
        :param cloud_identity_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_identity_custom_endpoint GoogleProvider#cloud_identity_custom_endpoint}.
        :param cloud_ids_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_ids_custom_endpoint GoogleProvider#cloud_ids_custom_endpoint}.
        :param cloud_quotas_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_quotas_custom_endpoint GoogleProvider#cloud_quotas_custom_endpoint}.
        :param cloud_resource_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_resource_manager_custom_endpoint GoogleProvider#cloud_resource_manager_custom_endpoint}.
        :param cloud_run_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_run_custom_endpoint GoogleProvider#cloud_run_custom_endpoint}.
        :param cloud_run_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_run_v2_custom_endpoint GoogleProvider#cloud_run_v2_custom_endpoint}.
        :param cloud_scheduler_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_scheduler_custom_endpoint GoogleProvider#cloud_scheduler_custom_endpoint}.
        :param cloud_tasks_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_tasks_custom_endpoint GoogleProvider#cloud_tasks_custom_endpoint}.
        :param colab_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#colab_custom_endpoint GoogleProvider#colab_custom_endpoint}.
        :param composer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#composer_custom_endpoint GoogleProvider#composer_custom_endpoint}.
        :param compute_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#compute_custom_endpoint GoogleProvider#compute_custom_endpoint}.
        :param contact_center_insights_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#contact_center_insights_custom_endpoint GoogleProvider#contact_center_insights_custom_endpoint}.
        :param container_analysis_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_analysis_custom_endpoint GoogleProvider#container_analysis_custom_endpoint}.
        :param container_attached_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_attached_custom_endpoint GoogleProvider#container_attached_custom_endpoint}.
        :param container_aws_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_aws_custom_endpoint GoogleProvider#container_aws_custom_endpoint}.
        :param container_azure_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_azure_custom_endpoint GoogleProvider#container_azure_custom_endpoint}.
        :param container_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_custom_endpoint GoogleProvider#container_custom_endpoint}.
        :param core_billing_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#core_billing_custom_endpoint GoogleProvider#core_billing_custom_endpoint}.
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#credentials GoogleProvider#credentials}.
        :param database_migration_service_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#database_migration_service_custom_endpoint GoogleProvider#database_migration_service_custom_endpoint}.
        :param data_catalog_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_catalog_custom_endpoint GoogleProvider#data_catalog_custom_endpoint}.
        :param dataflow_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataflow_custom_endpoint GoogleProvider#dataflow_custom_endpoint}.
        :param data_fusion_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_fusion_custom_endpoint GoogleProvider#data_fusion_custom_endpoint}.
        :param data_loss_prevention_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_loss_prevention_custom_endpoint GoogleProvider#data_loss_prevention_custom_endpoint}.
        :param data_pipeline_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_pipeline_custom_endpoint GoogleProvider#data_pipeline_custom_endpoint}.
        :param dataplex_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataplex_custom_endpoint GoogleProvider#dataplex_custom_endpoint}.
        :param dataproc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataproc_custom_endpoint GoogleProvider#dataproc_custom_endpoint}.
        :param dataproc_gdc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataproc_gdc_custom_endpoint GoogleProvider#dataproc_gdc_custom_endpoint}.
        :param dataproc_metastore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataproc_metastore_custom_endpoint GoogleProvider#dataproc_metastore_custom_endpoint}.
        :param datastream_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#datastream_custom_endpoint GoogleProvider#datastream_custom_endpoint}.
        :param default_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#default_labels GoogleProvider#default_labels}.
        :param deployment_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#deployment_manager_custom_endpoint GoogleProvider#deployment_manager_custom_endpoint}.
        :param developer_connect_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#developer_connect_custom_endpoint GoogleProvider#developer_connect_custom_endpoint}.
        :param dialogflow_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dialogflow_custom_endpoint GoogleProvider#dialogflow_custom_endpoint}.
        :param dialogflow_cx_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dialogflow_cx_custom_endpoint GoogleProvider#dialogflow_cx_custom_endpoint}.
        :param discovery_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#discovery_engine_custom_endpoint GoogleProvider#discovery_engine_custom_endpoint}.
        :param dns_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dns_custom_endpoint GoogleProvider#dns_custom_endpoint}.
        :param document_ai_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#document_ai_custom_endpoint GoogleProvider#document_ai_custom_endpoint}.
        :param document_ai_warehouse_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#document_ai_warehouse_custom_endpoint GoogleProvider#document_ai_warehouse_custom_endpoint}.
        :param edgecontainer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#edgecontainer_custom_endpoint GoogleProvider#edgecontainer_custom_endpoint}.
        :param edgenetwork_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#edgenetwork_custom_endpoint GoogleProvider#edgenetwork_custom_endpoint}.
        :param essential_contacts_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#essential_contacts_custom_endpoint GoogleProvider#essential_contacts_custom_endpoint}.
        :param eventarc_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#eventarc_custom_endpoint GoogleProvider#eventarc_custom_endpoint}.
        :param external_credentials: external_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#external_credentials GoogleProvider#external_credentials}
        :param filestore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#filestore_custom_endpoint GoogleProvider#filestore_custom_endpoint}.
        :param firebase_app_check_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebase_app_check_custom_endpoint GoogleProvider#firebase_app_check_custom_endpoint}.
        :param firebase_app_hosting_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebase_app_hosting_custom_endpoint GoogleProvider#firebase_app_hosting_custom_endpoint}.
        :param firebase_data_connect_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebase_data_connect_custom_endpoint GoogleProvider#firebase_data_connect_custom_endpoint}.
        :param firebaserules_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebaserules_custom_endpoint GoogleProvider#firebaserules_custom_endpoint}.
        :param firestore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firestore_custom_endpoint GoogleProvider#firestore_custom_endpoint}.
        :param gemini_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gemini_custom_endpoint GoogleProvider#gemini_custom_endpoint}.
        :param gke_backup_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gke_backup_custom_endpoint GoogleProvider#gke_backup_custom_endpoint}.
        :param gke_hub2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gke_hub2_custom_endpoint GoogleProvider#gke_hub2_custom_endpoint}.
        :param gke_hub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gke_hub_custom_endpoint GoogleProvider#gke_hub_custom_endpoint}.
        :param gkehub_feature_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gkehub_feature_custom_endpoint GoogleProvider#gkehub_feature_custom_endpoint}.
        :param gkeonprem_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gkeonprem_custom_endpoint GoogleProvider#gkeonprem_custom_endpoint}.
        :param healthcare_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#healthcare_custom_endpoint GoogleProvider#healthcare_custom_endpoint}.
        :param iam2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam2_custom_endpoint GoogleProvider#iam2_custom_endpoint}.
        :param iam3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam3_custom_endpoint GoogleProvider#iam3_custom_endpoint}.
        :param iam_beta_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_beta_custom_endpoint GoogleProvider#iam_beta_custom_endpoint}.
        :param iam_credentials_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_credentials_custom_endpoint GoogleProvider#iam_credentials_custom_endpoint}.
        :param iam_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_custom_endpoint GoogleProvider#iam_custom_endpoint}.
        :param iam_workforce_pool_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_workforce_pool_custom_endpoint GoogleProvider#iam_workforce_pool_custom_endpoint}.
        :param iap_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iap_custom_endpoint GoogleProvider#iap_custom_endpoint}.
        :param identity_platform_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#identity_platform_custom_endpoint GoogleProvider#identity_platform_custom_endpoint}.
        :param impersonate_service_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#impersonate_service_account GoogleProvider#impersonate_service_account}.
        :param impersonate_service_account_delegates: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#impersonate_service_account_delegates GoogleProvider#impersonate_service_account_delegates}.
        :param integration_connectors_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#integration_connectors_custom_endpoint GoogleProvider#integration_connectors_custom_endpoint}.
        :param integrations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#integrations_custom_endpoint GoogleProvider#integrations_custom_endpoint}.
        :param kms_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#kms_custom_endpoint GoogleProvider#kms_custom_endpoint}.
        :param logging_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#logging_custom_endpoint GoogleProvider#logging_custom_endpoint}.
        :param looker_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#looker_custom_endpoint GoogleProvider#looker_custom_endpoint}.
        :param lustre_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#lustre_custom_endpoint GoogleProvider#lustre_custom_endpoint}.
        :param managed_kafka_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#managed_kafka_custom_endpoint GoogleProvider#managed_kafka_custom_endpoint}.
        :param memcache_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#memcache_custom_endpoint GoogleProvider#memcache_custom_endpoint}.
        :param memorystore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#memorystore_custom_endpoint GoogleProvider#memorystore_custom_endpoint}.
        :param migration_center_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#migration_center_custom_endpoint GoogleProvider#migration_center_custom_endpoint}.
        :param ml_engine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#ml_engine_custom_endpoint GoogleProvider#ml_engine_custom_endpoint}.
        :param model_armor_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#model_armor_custom_endpoint GoogleProvider#model_armor_custom_endpoint}.
        :param model_armor_global_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#model_armor_global_custom_endpoint GoogleProvider#model_armor_global_custom_endpoint}.
        :param monitoring_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#monitoring_custom_endpoint GoogleProvider#monitoring_custom_endpoint}.
        :param netapp_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#netapp_custom_endpoint GoogleProvider#netapp_custom_endpoint}.
        :param network_connectivity_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_connectivity_custom_endpoint GoogleProvider#network_connectivity_custom_endpoint}.
        :param network_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_management_custom_endpoint GoogleProvider#network_management_custom_endpoint}.
        :param network_security_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_security_custom_endpoint GoogleProvider#network_security_custom_endpoint}.
        :param network_services_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_services_custom_endpoint GoogleProvider#network_services_custom_endpoint}.
        :param notebooks_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#notebooks_custom_endpoint GoogleProvider#notebooks_custom_endpoint}.
        :param oracle_database_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#oracle_database_custom_endpoint GoogleProvider#oracle_database_custom_endpoint}.
        :param org_policy_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#org_policy_custom_endpoint GoogleProvider#org_policy_custom_endpoint}.
        :param os_config_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#os_config_custom_endpoint GoogleProvider#os_config_custom_endpoint}.
        :param os_config_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#os_config_v2_custom_endpoint GoogleProvider#os_config_v2_custom_endpoint}.
        :param os_login_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#os_login_custom_endpoint GoogleProvider#os_login_custom_endpoint}.
        :param parallelstore_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#parallelstore_custom_endpoint GoogleProvider#parallelstore_custom_endpoint}.
        :param parameter_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#parameter_manager_custom_endpoint GoogleProvider#parameter_manager_custom_endpoint}.
        :param parameter_manager_regional_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#parameter_manager_regional_custom_endpoint GoogleProvider#parameter_manager_regional_custom_endpoint}.
        :param privateca_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#privateca_custom_endpoint GoogleProvider#privateca_custom_endpoint}.
        :param privileged_access_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#privileged_access_manager_custom_endpoint GoogleProvider#privileged_access_manager_custom_endpoint}.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#project GoogleProvider#project}.
        :param public_ca_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#public_ca_custom_endpoint GoogleProvider#public_ca_custom_endpoint}.
        :param pubsub_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#pubsub_custom_endpoint GoogleProvider#pubsub_custom_endpoint}.
        :param pubsub_lite_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#pubsub_lite_custom_endpoint GoogleProvider#pubsub_lite_custom_endpoint}.
        :param recaptcha_enterprise_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#recaptcha_enterprise_custom_endpoint GoogleProvider#recaptcha_enterprise_custom_endpoint}.
        :param redis_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#redis_custom_endpoint GoogleProvider#redis_custom_endpoint}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#region GoogleProvider#region}.
        :param request_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#request_reason GoogleProvider#request_reason}.
        :param request_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#request_timeout GoogleProvider#request_timeout}.
        :param resource_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#resource_manager_custom_endpoint GoogleProvider#resource_manager_custom_endpoint}.
        :param resource_manager_v3_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#resource_manager_v3_custom_endpoint GoogleProvider#resource_manager_v3_custom_endpoint}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#scopes GoogleProvider#scopes}.
        :param secret_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#secret_manager_custom_endpoint GoogleProvider#secret_manager_custom_endpoint}.
        :param secret_manager_regional_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#secret_manager_regional_custom_endpoint GoogleProvider#secret_manager_regional_custom_endpoint}.
        :param secure_source_manager_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#secure_source_manager_custom_endpoint GoogleProvider#secure_source_manager_custom_endpoint}.
        :param security_center_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#security_center_custom_endpoint GoogleProvider#security_center_custom_endpoint}.
        :param security_center_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#security_center_management_custom_endpoint GoogleProvider#security_center_management_custom_endpoint}.
        :param security_center_v2_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#security_center_v2_custom_endpoint GoogleProvider#security_center_v2_custom_endpoint}.
        :param securityposture_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#securityposture_custom_endpoint GoogleProvider#securityposture_custom_endpoint}.
        :param service_management_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_management_custom_endpoint GoogleProvider#service_management_custom_endpoint}.
        :param service_networking_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_networking_custom_endpoint GoogleProvider#service_networking_custom_endpoint}.
        :param service_usage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_usage_custom_endpoint GoogleProvider#service_usage_custom_endpoint}.
        :param site_verification_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#site_verification_custom_endpoint GoogleProvider#site_verification_custom_endpoint}.
        :param source_repo_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#source_repo_custom_endpoint GoogleProvider#source_repo_custom_endpoint}.
        :param spanner_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#spanner_custom_endpoint GoogleProvider#spanner_custom_endpoint}.
        :param sql_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#sql_custom_endpoint GoogleProvider#sql_custom_endpoint}.
        :param storage_batch_operations_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_batch_operations_custom_endpoint GoogleProvider#storage_batch_operations_custom_endpoint}.
        :param storage_control_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_control_custom_endpoint GoogleProvider#storage_control_custom_endpoint}.
        :param storage_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_custom_endpoint GoogleProvider#storage_custom_endpoint}.
        :param storage_insights_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_insights_custom_endpoint GoogleProvider#storage_insights_custom_endpoint}.
        :param storage_transfer_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_transfer_custom_endpoint GoogleProvider#storage_transfer_custom_endpoint}.
        :param tags_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#tags_custom_endpoint GoogleProvider#tags_custom_endpoint}.
        :param tags_location_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#tags_location_custom_endpoint GoogleProvider#tags_location_custom_endpoint}.
        :param terraform_attribution_label_addition_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#terraform_attribution_label_addition_strategy GoogleProvider#terraform_attribution_label_addition_strategy}.
        :param tpu_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#tpu_custom_endpoint GoogleProvider#tpu_custom_endpoint}.
        :param transcoder_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#transcoder_custom_endpoint GoogleProvider#transcoder_custom_endpoint}.
        :param universe_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#universe_domain GoogleProvider#universe_domain}.
        :param user_project_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#user_project_override GoogleProvider#user_project_override}.
        :param vertex_ai_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#vertex_ai_custom_endpoint GoogleProvider#vertex_ai_custom_endpoint}.
        :param vmwareengine_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#vmwareengine_custom_endpoint GoogleProvider#vmwareengine_custom_endpoint}.
        :param vpc_access_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#vpc_access_custom_endpoint GoogleProvider#vpc_access_custom_endpoint}.
        :param workbench_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#workbench_custom_endpoint GoogleProvider#workbench_custom_endpoint}.
        :param workflows_custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#workflows_custom_endpoint GoogleProvider#workflows_custom_endpoint}.
        :param zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#zone GoogleProvider#zone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9129c5feceef1a0d065989f96f621f2f6ce8c9a329998493f7b7a7b6ff4f6f0)
            check_type(argname="argument access_approval_custom_endpoint", value=access_approval_custom_endpoint, expected_type=type_hints["access_approval_custom_endpoint"])
            check_type(argname="argument access_context_manager_custom_endpoint", value=access_context_manager_custom_endpoint, expected_type=type_hints["access_context_manager_custom_endpoint"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument active_directory_custom_endpoint", value=active_directory_custom_endpoint, expected_type=type_hints["active_directory_custom_endpoint"])
            check_type(argname="argument add_terraform_attribution_label", value=add_terraform_attribution_label, expected_type=type_hints["add_terraform_attribution_label"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument alloydb_custom_endpoint", value=alloydb_custom_endpoint, expected_type=type_hints["alloydb_custom_endpoint"])
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
            check_type(argname="argument contact_center_insights_custom_endpoint", value=contact_center_insights_custom_endpoint, expected_type=type_hints["contact_center_insights_custom_endpoint"])
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
            check_type(argname="argument firebase_data_connect_custom_endpoint", value=firebase_data_connect_custom_endpoint, expected_type=type_hints["firebase_data_connect_custom_endpoint"])
            check_type(argname="argument firebaserules_custom_endpoint", value=firebaserules_custom_endpoint, expected_type=type_hints["firebaserules_custom_endpoint"])
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
            check_type(argname="argument model_armor_custom_endpoint", value=model_armor_custom_endpoint, expected_type=type_hints["model_armor_custom_endpoint"])
            check_type(argname="argument model_armor_global_custom_endpoint", value=model_armor_global_custom_endpoint, expected_type=type_hints["model_armor_global_custom_endpoint"])
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
            check_type(argname="argument resource_manager_custom_endpoint", value=resource_manager_custom_endpoint, expected_type=type_hints["resource_manager_custom_endpoint"])
            check_type(argname="argument resource_manager_v3_custom_endpoint", value=resource_manager_v3_custom_endpoint, expected_type=type_hints["resource_manager_v3_custom_endpoint"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument secret_manager_custom_endpoint", value=secret_manager_custom_endpoint, expected_type=type_hints["secret_manager_custom_endpoint"])
            check_type(argname="argument secret_manager_regional_custom_endpoint", value=secret_manager_regional_custom_endpoint, expected_type=type_hints["secret_manager_regional_custom_endpoint"])
            check_type(argname="argument secure_source_manager_custom_endpoint", value=secure_source_manager_custom_endpoint, expected_type=type_hints["secure_source_manager_custom_endpoint"])
            check_type(argname="argument security_center_custom_endpoint", value=security_center_custom_endpoint, expected_type=type_hints["security_center_custom_endpoint"])
            check_type(argname="argument security_center_management_custom_endpoint", value=security_center_management_custom_endpoint, expected_type=type_hints["security_center_management_custom_endpoint"])
            check_type(argname="argument security_center_v2_custom_endpoint", value=security_center_v2_custom_endpoint, expected_type=type_hints["security_center_v2_custom_endpoint"])
            check_type(argname="argument securityposture_custom_endpoint", value=securityposture_custom_endpoint, expected_type=type_hints["securityposture_custom_endpoint"])
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
            check_type(argname="argument transcoder_custom_endpoint", value=transcoder_custom_endpoint, expected_type=type_hints["transcoder_custom_endpoint"])
            check_type(argname="argument universe_domain", value=universe_domain, expected_type=type_hints["universe_domain"])
            check_type(argname="argument user_project_override", value=user_project_override, expected_type=type_hints["user_project_override"])
            check_type(argname="argument vertex_ai_custom_endpoint", value=vertex_ai_custom_endpoint, expected_type=type_hints["vertex_ai_custom_endpoint"])
            check_type(argname="argument vmwareengine_custom_endpoint", value=vmwareengine_custom_endpoint, expected_type=type_hints["vmwareengine_custom_endpoint"])
            check_type(argname="argument vpc_access_custom_endpoint", value=vpc_access_custom_endpoint, expected_type=type_hints["vpc_access_custom_endpoint"])
            check_type(argname="argument workbench_custom_endpoint", value=workbench_custom_endpoint, expected_type=type_hints["workbench_custom_endpoint"])
            check_type(argname="argument workflows_custom_endpoint", value=workflows_custom_endpoint, expected_type=type_hints["workflows_custom_endpoint"])
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
        if contact_center_insights_custom_endpoint is not None:
            self._values["contact_center_insights_custom_endpoint"] = contact_center_insights_custom_endpoint
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
        if firebase_data_connect_custom_endpoint is not None:
            self._values["firebase_data_connect_custom_endpoint"] = firebase_data_connect_custom_endpoint
        if firebaserules_custom_endpoint is not None:
            self._values["firebaserules_custom_endpoint"] = firebaserules_custom_endpoint
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
        if model_armor_custom_endpoint is not None:
            self._values["model_armor_custom_endpoint"] = model_armor_custom_endpoint
        if model_armor_global_custom_endpoint is not None:
            self._values["model_armor_global_custom_endpoint"] = model_armor_global_custom_endpoint
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
        if resource_manager_custom_endpoint is not None:
            self._values["resource_manager_custom_endpoint"] = resource_manager_custom_endpoint
        if resource_manager_v3_custom_endpoint is not None:
            self._values["resource_manager_v3_custom_endpoint"] = resource_manager_v3_custom_endpoint
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
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def access_approval_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#access_approval_custom_endpoint GoogleProvider#access_approval_custom_endpoint}.'''
        result = self._values.get("access_approval_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_context_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#access_context_manager_custom_endpoint GoogleProvider#access_context_manager_custom_endpoint}.'''
        result = self._values.get("access_context_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#access_token GoogleProvider#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def active_directory_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#active_directory_custom_endpoint GoogleProvider#active_directory_custom_endpoint}.'''
        result = self._values.get("active_directory_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def add_terraform_attribution_label(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#add_terraform_attribution_label GoogleProvider#add_terraform_attribution_label}.'''
        result = self._values.get("add_terraform_attribution_label")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#alias GoogleProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alloydb_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#alloydb_custom_endpoint GoogleProvider#alloydb_custom_endpoint}.'''
        result = self._values.get("alloydb_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apigee_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apigee_custom_endpoint GoogleProvider#apigee_custom_endpoint}.'''
        result = self._values.get("apigee_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apihub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apihub_custom_endpoint GoogleProvider#apihub_custom_endpoint}.'''
        result = self._values.get("apihub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apikeys_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apikeys_custom_endpoint GoogleProvider#apikeys_custom_endpoint}.'''
        result = self._values.get("apikeys_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#app_engine_custom_endpoint GoogleProvider#app_engine_custom_endpoint}.'''
        result = self._values.get("app_engine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apphub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#apphub_custom_endpoint GoogleProvider#apphub_custom_endpoint}.'''
        result = self._values.get("apphub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def artifact_registry_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#artifact_registry_custom_endpoint GoogleProvider#artifact_registry_custom_endpoint}.'''
        result = self._values.get("artifact_registry_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assured_workloads_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#assured_workloads_custom_endpoint GoogleProvider#assured_workloads_custom_endpoint}.'''
        result = self._values.get("assured_workloads_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_dr_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#backup_dr_custom_endpoint GoogleProvider#backup_dr_custom_endpoint}.'''
        result = self._values.get("backup_dr_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def batching(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleProviderBatching]]]:
        '''batching block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#batching GoogleProvider#batching}
        '''
        result = self._values.get("batching")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleProviderBatching]]], result)

    @builtins.property
    def beyondcorp_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#beyondcorp_custom_endpoint GoogleProvider#beyondcorp_custom_endpoint}.'''
        result = self._values.get("beyondcorp_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def biglake_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#biglake_custom_endpoint GoogleProvider#biglake_custom_endpoint}.'''
        result = self._values.get("biglake_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_analytics_hub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_analytics_hub_custom_endpoint GoogleProvider#bigquery_analytics_hub_custom_endpoint}.'''
        result = self._values.get("bigquery_analytics_hub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_connection_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_connection_custom_endpoint GoogleProvider#bigquery_connection_custom_endpoint}.'''
        result = self._values.get("bigquery_connection_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def big_query_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#big_query_custom_endpoint GoogleProvider#big_query_custom_endpoint}.'''
        result = self._values.get("big_query_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_datapolicy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_datapolicy_custom_endpoint GoogleProvider#bigquery_datapolicy_custom_endpoint}.'''
        result = self._values.get("bigquery_datapolicy_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_data_transfer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_data_transfer_custom_endpoint GoogleProvider#bigquery_data_transfer_custom_endpoint}.'''
        result = self._values.get("bigquery_data_transfer_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigquery_reservation_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigquery_reservation_custom_endpoint GoogleProvider#bigquery_reservation_custom_endpoint}.'''
        result = self._values.get("bigquery_reservation_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bigtable_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#bigtable_custom_endpoint GoogleProvider#bigtable_custom_endpoint}.'''
        result = self._values.get("bigtable_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#billing_custom_endpoint GoogleProvider#billing_custom_endpoint}.'''
        result = self._values.get("billing_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#billing_project GoogleProvider#billing_project}.'''
        result = self._values.get("billing_project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_authorization_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#binary_authorization_custom_endpoint GoogleProvider#binary_authorization_custom_endpoint}.'''
        result = self._values.get("binary_authorization_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def blockchain_node_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#blockchain_node_engine_custom_endpoint GoogleProvider#blockchain_node_engine_custom_endpoint}.'''
        result = self._values.get("blockchain_node_engine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#certificate_manager_custom_endpoint GoogleProvider#certificate_manager_custom_endpoint}.'''
        result = self._values.get("certificate_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chronicle_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#chronicle_custom_endpoint GoogleProvider#chronicle_custom_endpoint}.'''
        result = self._values.get("chronicle_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_asset_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_asset_custom_endpoint GoogleProvider#cloud_asset_custom_endpoint}.'''
        result = self._values.get("cloud_asset_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_billing_custom_endpoint GoogleProvider#cloud_billing_custom_endpoint}.'''
        result = self._values.get("cloud_billing_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_build_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_build_custom_endpoint GoogleProvider#cloud_build_custom_endpoint}.'''
        result = self._values.get("cloud_build_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudbuildv2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloudbuildv2_custom_endpoint GoogleProvider#cloudbuildv2_custom_endpoint}.'''
        result = self._values.get("cloudbuildv2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_build_worker_pool_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_build_worker_pool_custom_endpoint GoogleProvider#cloud_build_worker_pool_custom_endpoint}.'''
        result = self._values.get("cloud_build_worker_pool_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clouddeploy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#clouddeploy_custom_endpoint GoogleProvider#clouddeploy_custom_endpoint}.'''
        result = self._values.get("clouddeploy_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clouddomains_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#clouddomains_custom_endpoint GoogleProvider#clouddomains_custom_endpoint}.'''
        result = self._values.get("clouddomains_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfunctions2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloudfunctions2_custom_endpoint GoogleProvider#cloudfunctions2_custom_endpoint}.'''
        result = self._values.get("cloudfunctions2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_functions_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_functions_custom_endpoint GoogleProvider#cloud_functions_custom_endpoint}.'''
        result = self._values.get("cloud_functions_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_identity_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_identity_custom_endpoint GoogleProvider#cloud_identity_custom_endpoint}.'''
        result = self._values.get("cloud_identity_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_ids_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_ids_custom_endpoint GoogleProvider#cloud_ids_custom_endpoint}.'''
        result = self._values.get("cloud_ids_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_quotas_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_quotas_custom_endpoint GoogleProvider#cloud_quotas_custom_endpoint}.'''
        result = self._values.get("cloud_quotas_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_resource_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_resource_manager_custom_endpoint GoogleProvider#cloud_resource_manager_custom_endpoint}.'''
        result = self._values.get("cloud_resource_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_run_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_run_custom_endpoint GoogleProvider#cloud_run_custom_endpoint}.'''
        result = self._values.get("cloud_run_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_run_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_run_v2_custom_endpoint GoogleProvider#cloud_run_v2_custom_endpoint}.'''
        result = self._values.get("cloud_run_v2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_scheduler_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_scheduler_custom_endpoint GoogleProvider#cloud_scheduler_custom_endpoint}.'''
        result = self._values.get("cloud_scheduler_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_tasks_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#cloud_tasks_custom_endpoint GoogleProvider#cloud_tasks_custom_endpoint}.'''
        result = self._values.get("cloud_tasks_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def colab_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#colab_custom_endpoint GoogleProvider#colab_custom_endpoint}.'''
        result = self._values.get("colab_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def composer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#composer_custom_endpoint GoogleProvider#composer_custom_endpoint}.'''
        result = self._values.get("composer_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#compute_custom_endpoint GoogleProvider#compute_custom_endpoint}.'''
        result = self._values.get("compute_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contact_center_insights_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#contact_center_insights_custom_endpoint GoogleProvider#contact_center_insights_custom_endpoint}.'''
        result = self._values.get("contact_center_insights_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_analysis_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_analysis_custom_endpoint GoogleProvider#container_analysis_custom_endpoint}.'''
        result = self._values.get("container_analysis_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_attached_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_attached_custom_endpoint GoogleProvider#container_attached_custom_endpoint}.'''
        result = self._values.get("container_attached_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_aws_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_aws_custom_endpoint GoogleProvider#container_aws_custom_endpoint}.'''
        result = self._values.get("container_aws_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_azure_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_azure_custom_endpoint GoogleProvider#container_azure_custom_endpoint}.'''
        result = self._values.get("container_azure_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#container_custom_endpoint GoogleProvider#container_custom_endpoint}.'''
        result = self._values.get("container_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def core_billing_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#core_billing_custom_endpoint GoogleProvider#core_billing_custom_endpoint}.'''
        result = self._values.get("core_billing_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#credentials GoogleProvider#credentials}.'''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_migration_service_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#database_migration_service_custom_endpoint GoogleProvider#database_migration_service_custom_endpoint}.'''
        result = self._values.get("database_migration_service_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_catalog_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_catalog_custom_endpoint GoogleProvider#data_catalog_custom_endpoint}.'''
        result = self._values.get("data_catalog_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataflow_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataflow_custom_endpoint GoogleProvider#dataflow_custom_endpoint}.'''
        result = self._values.get("dataflow_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_fusion_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_fusion_custom_endpoint GoogleProvider#data_fusion_custom_endpoint}.'''
        result = self._values.get("data_fusion_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_loss_prevention_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_loss_prevention_custom_endpoint GoogleProvider#data_loss_prevention_custom_endpoint}.'''
        result = self._values.get("data_loss_prevention_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_pipeline_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#data_pipeline_custom_endpoint GoogleProvider#data_pipeline_custom_endpoint}.'''
        result = self._values.get("data_pipeline_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataplex_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataplex_custom_endpoint GoogleProvider#dataplex_custom_endpoint}.'''
        result = self._values.get("dataplex_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataproc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataproc_custom_endpoint GoogleProvider#dataproc_custom_endpoint}.'''
        result = self._values.get("dataproc_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataproc_gdc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataproc_gdc_custom_endpoint GoogleProvider#dataproc_gdc_custom_endpoint}.'''
        result = self._values.get("dataproc_gdc_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataproc_metastore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dataproc_metastore_custom_endpoint GoogleProvider#dataproc_metastore_custom_endpoint}.'''
        result = self._values.get("dataproc_metastore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datastream_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#datastream_custom_endpoint GoogleProvider#datastream_custom_endpoint}.'''
        result = self._values.get("datastream_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#default_labels GoogleProvider#default_labels}.'''
        result = self._values.get("default_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def deployment_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#deployment_manager_custom_endpoint GoogleProvider#deployment_manager_custom_endpoint}.'''
        result = self._values.get("deployment_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def developer_connect_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#developer_connect_custom_endpoint GoogleProvider#developer_connect_custom_endpoint}.'''
        result = self._values.get("developer_connect_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dialogflow_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dialogflow_custom_endpoint GoogleProvider#dialogflow_custom_endpoint}.'''
        result = self._values.get("dialogflow_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dialogflow_cx_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dialogflow_cx_custom_endpoint GoogleProvider#dialogflow_cx_custom_endpoint}.'''
        result = self._values.get("dialogflow_cx_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def discovery_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#discovery_engine_custom_endpoint GoogleProvider#discovery_engine_custom_endpoint}.'''
        result = self._values.get("discovery_engine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#dns_custom_endpoint GoogleProvider#dns_custom_endpoint}.'''
        result = self._values.get("dns_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_ai_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#document_ai_custom_endpoint GoogleProvider#document_ai_custom_endpoint}.'''
        result = self._values.get("document_ai_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_ai_warehouse_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#document_ai_warehouse_custom_endpoint GoogleProvider#document_ai_warehouse_custom_endpoint}.'''
        result = self._values.get("document_ai_warehouse_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edgecontainer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#edgecontainer_custom_endpoint GoogleProvider#edgecontainer_custom_endpoint}.'''
        result = self._values.get("edgecontainer_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edgenetwork_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#edgenetwork_custom_endpoint GoogleProvider#edgenetwork_custom_endpoint}.'''
        result = self._values.get("edgenetwork_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def essential_contacts_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#essential_contacts_custom_endpoint GoogleProvider#essential_contacts_custom_endpoint}.'''
        result = self._values.get("essential_contacts_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventarc_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#eventarc_custom_endpoint GoogleProvider#eventarc_custom_endpoint}.'''
        result = self._values.get("eventarc_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_credentials(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderExternalCredentials"]]]:
        '''external_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#external_credentials GoogleProvider#external_credentials}
        '''
        result = self._values.get("external_credentials")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleProviderExternalCredentials"]]], result)

    @builtins.property
    def filestore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#filestore_custom_endpoint GoogleProvider#filestore_custom_endpoint}.'''
        result = self._values.get("filestore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_app_check_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebase_app_check_custom_endpoint GoogleProvider#firebase_app_check_custom_endpoint}.'''
        result = self._values.get("firebase_app_check_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_app_hosting_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebase_app_hosting_custom_endpoint GoogleProvider#firebase_app_hosting_custom_endpoint}.'''
        result = self._values.get("firebase_app_hosting_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebase_data_connect_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebase_data_connect_custom_endpoint GoogleProvider#firebase_data_connect_custom_endpoint}.'''
        result = self._values.get("firebase_data_connect_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firebaserules_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firebaserules_custom_endpoint GoogleProvider#firebaserules_custom_endpoint}.'''
        result = self._values.get("firebaserules_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firestore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#firestore_custom_endpoint GoogleProvider#firestore_custom_endpoint}.'''
        result = self._values.get("firestore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gemini_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gemini_custom_endpoint GoogleProvider#gemini_custom_endpoint}.'''
        result = self._values.get("gemini_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gke_backup_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gke_backup_custom_endpoint GoogleProvider#gke_backup_custom_endpoint}.'''
        result = self._values.get("gke_backup_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gke_hub2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gke_hub2_custom_endpoint GoogleProvider#gke_hub2_custom_endpoint}.'''
        result = self._values.get("gke_hub2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gke_hub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gke_hub_custom_endpoint GoogleProvider#gke_hub_custom_endpoint}.'''
        result = self._values.get("gke_hub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gkehub_feature_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gkehub_feature_custom_endpoint GoogleProvider#gkehub_feature_custom_endpoint}.'''
        result = self._values.get("gkehub_feature_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gkeonprem_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#gkeonprem_custom_endpoint GoogleProvider#gkeonprem_custom_endpoint}.'''
        result = self._values.get("gkeonprem_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def healthcare_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#healthcare_custom_endpoint GoogleProvider#healthcare_custom_endpoint}.'''
        result = self._values.get("healthcare_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam2_custom_endpoint GoogleProvider#iam2_custom_endpoint}.'''
        result = self._values.get("iam2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam3_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam3_custom_endpoint GoogleProvider#iam3_custom_endpoint}.'''
        result = self._values.get("iam3_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_beta_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_beta_custom_endpoint GoogleProvider#iam_beta_custom_endpoint}.'''
        result = self._values.get("iam_beta_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_credentials_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_credentials_custom_endpoint GoogleProvider#iam_credentials_custom_endpoint}.'''
        result = self._values.get("iam_credentials_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_custom_endpoint GoogleProvider#iam_custom_endpoint}.'''
        result = self._values.get("iam_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_workforce_pool_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iam_workforce_pool_custom_endpoint GoogleProvider#iam_workforce_pool_custom_endpoint}.'''
        result = self._values.get("iam_workforce_pool_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iap_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#iap_custom_endpoint GoogleProvider#iap_custom_endpoint}.'''
        result = self._values.get("iap_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_platform_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#identity_platform_custom_endpoint GoogleProvider#identity_platform_custom_endpoint}.'''
        result = self._values.get("identity_platform_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def impersonate_service_account(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#impersonate_service_account GoogleProvider#impersonate_service_account}.'''
        result = self._values.get("impersonate_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def impersonate_service_account_delegates(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#impersonate_service_account_delegates GoogleProvider#impersonate_service_account_delegates}.'''
        result = self._values.get("impersonate_service_account_delegates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def integration_connectors_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#integration_connectors_custom_endpoint GoogleProvider#integration_connectors_custom_endpoint}.'''
        result = self._values.get("integration_connectors_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integrations_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#integrations_custom_endpoint GoogleProvider#integrations_custom_endpoint}.'''
        result = self._values.get("integrations_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#kms_custom_endpoint GoogleProvider#kms_custom_endpoint}.'''
        result = self._values.get("kms_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#logging_custom_endpoint GoogleProvider#logging_custom_endpoint}.'''
        result = self._values.get("logging_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def looker_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#looker_custom_endpoint GoogleProvider#looker_custom_endpoint}.'''
        result = self._values.get("looker_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lustre_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#lustre_custom_endpoint GoogleProvider#lustre_custom_endpoint}.'''
        result = self._values.get("lustre_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_kafka_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#managed_kafka_custom_endpoint GoogleProvider#managed_kafka_custom_endpoint}.'''
        result = self._values.get("managed_kafka_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memcache_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#memcache_custom_endpoint GoogleProvider#memcache_custom_endpoint}.'''
        result = self._values.get("memcache_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memorystore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#memorystore_custom_endpoint GoogleProvider#memorystore_custom_endpoint}.'''
        result = self._values.get("memorystore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def migration_center_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#migration_center_custom_endpoint GoogleProvider#migration_center_custom_endpoint}.'''
        result = self._values.get("migration_center_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ml_engine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#ml_engine_custom_endpoint GoogleProvider#ml_engine_custom_endpoint}.'''
        result = self._values.get("ml_engine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_armor_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#model_armor_custom_endpoint GoogleProvider#model_armor_custom_endpoint}.'''
        result = self._values.get("model_armor_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_armor_global_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#model_armor_global_custom_endpoint GoogleProvider#model_armor_global_custom_endpoint}.'''
        result = self._values.get("model_armor_global_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitoring_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#monitoring_custom_endpoint GoogleProvider#monitoring_custom_endpoint}.'''
        result = self._values.get("monitoring_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netapp_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#netapp_custom_endpoint GoogleProvider#netapp_custom_endpoint}.'''
        result = self._values.get("netapp_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_connectivity_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_connectivity_custom_endpoint GoogleProvider#network_connectivity_custom_endpoint}.'''
        result = self._values.get("network_connectivity_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_management_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_management_custom_endpoint GoogleProvider#network_management_custom_endpoint}.'''
        result = self._values.get("network_management_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_security_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_security_custom_endpoint GoogleProvider#network_security_custom_endpoint}.'''
        result = self._values.get("network_security_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_services_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#network_services_custom_endpoint GoogleProvider#network_services_custom_endpoint}.'''
        result = self._values.get("network_services_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notebooks_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#notebooks_custom_endpoint GoogleProvider#notebooks_custom_endpoint}.'''
        result = self._values.get("notebooks_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oracle_database_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#oracle_database_custom_endpoint GoogleProvider#oracle_database_custom_endpoint}.'''
        result = self._values.get("oracle_database_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org_policy_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#org_policy_custom_endpoint GoogleProvider#org_policy_custom_endpoint}.'''
        result = self._values.get("org_policy_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_config_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#os_config_custom_endpoint GoogleProvider#os_config_custom_endpoint}.'''
        result = self._values.get("os_config_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_config_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#os_config_v2_custom_endpoint GoogleProvider#os_config_v2_custom_endpoint}.'''
        result = self._values.get("os_config_v2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_login_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#os_login_custom_endpoint GoogleProvider#os_login_custom_endpoint}.'''
        result = self._values.get("os_login_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelstore_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#parallelstore_custom_endpoint GoogleProvider#parallelstore_custom_endpoint}.'''
        result = self._values.get("parallelstore_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#parameter_manager_custom_endpoint GoogleProvider#parameter_manager_custom_endpoint}.'''
        result = self._values.get("parameter_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_manager_regional_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#parameter_manager_regional_custom_endpoint GoogleProvider#parameter_manager_regional_custom_endpoint}.'''
        result = self._values.get("parameter_manager_regional_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privateca_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#privateca_custom_endpoint GoogleProvider#privateca_custom_endpoint}.'''
        result = self._values.get("privateca_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privileged_access_manager_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#privileged_access_manager_custom_endpoint GoogleProvider#privileged_access_manager_custom_endpoint}.'''
        result = self._values.get("privileged_access_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#project GoogleProvider#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ca_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#public_ca_custom_endpoint GoogleProvider#public_ca_custom_endpoint}.'''
        result = self._values.get("public_ca_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#pubsub_custom_endpoint GoogleProvider#pubsub_custom_endpoint}.'''
        result = self._values.get("pubsub_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_lite_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#pubsub_lite_custom_endpoint GoogleProvider#pubsub_lite_custom_endpoint}.'''
        result = self._values.get("pubsub_lite_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recaptcha_enterprise_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#recaptcha_enterprise_custom_endpoint GoogleProvider#recaptcha_enterprise_custom_endpoint}.'''
        result = self._values.get("recaptcha_enterprise_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#redis_custom_endpoint GoogleProvider#redis_custom_endpoint}.'''
        result = self._values.get("redis_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#region GoogleProvider#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_reason(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#request_reason GoogleProvider#request_reason}.'''
        result = self._values.get("request_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#request_timeout GoogleProvider#request_timeout}.'''
        result = self._values.get("request_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#resource_manager_custom_endpoint GoogleProvider#resource_manager_custom_endpoint}.'''
        result = self._values.get("resource_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_manager_v3_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#resource_manager_v3_custom_endpoint GoogleProvider#resource_manager_v3_custom_endpoint}.'''
        result = self._values.get("resource_manager_v3_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#scopes GoogleProvider#scopes}.'''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#secret_manager_custom_endpoint GoogleProvider#secret_manager_custom_endpoint}.'''
        result = self._values.get("secret_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_manager_regional_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#secret_manager_regional_custom_endpoint GoogleProvider#secret_manager_regional_custom_endpoint}.'''
        result = self._values.get("secret_manager_regional_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secure_source_manager_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#secure_source_manager_custom_endpoint GoogleProvider#secure_source_manager_custom_endpoint}.'''
        result = self._values.get("secure_source_manager_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_center_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#security_center_custom_endpoint GoogleProvider#security_center_custom_endpoint}.'''
        result = self._values.get("security_center_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_center_management_custom_endpoint(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#security_center_management_custom_endpoint GoogleProvider#security_center_management_custom_endpoint}.'''
        result = self._values.get("security_center_management_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_center_v2_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#security_center_v2_custom_endpoint GoogleProvider#security_center_v2_custom_endpoint}.'''
        result = self._values.get("security_center_v2_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def securityposture_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#securityposture_custom_endpoint GoogleProvider#securityposture_custom_endpoint}.'''
        result = self._values.get("securityposture_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_management_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_management_custom_endpoint GoogleProvider#service_management_custom_endpoint}.'''
        result = self._values.get("service_management_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_networking_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_networking_custom_endpoint GoogleProvider#service_networking_custom_endpoint}.'''
        result = self._values.get("service_networking_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_usage_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_usage_custom_endpoint GoogleProvider#service_usage_custom_endpoint}.'''
        result = self._values.get("service_usage_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site_verification_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#site_verification_custom_endpoint GoogleProvider#site_verification_custom_endpoint}.'''
        result = self._values.get("site_verification_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_repo_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#source_repo_custom_endpoint GoogleProvider#source_repo_custom_endpoint}.'''
        result = self._values.get("source_repo_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spanner_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#spanner_custom_endpoint GoogleProvider#spanner_custom_endpoint}.'''
        result = self._values.get("spanner_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#sql_custom_endpoint GoogleProvider#sql_custom_endpoint}.'''
        result = self._values.get("sql_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_batch_operations_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_batch_operations_custom_endpoint GoogleProvider#storage_batch_operations_custom_endpoint}.'''
        result = self._values.get("storage_batch_operations_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_control_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_control_custom_endpoint GoogleProvider#storage_control_custom_endpoint}.'''
        result = self._values.get("storage_control_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_custom_endpoint GoogleProvider#storage_custom_endpoint}.'''
        result = self._values.get("storage_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_insights_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_insights_custom_endpoint GoogleProvider#storage_insights_custom_endpoint}.'''
        result = self._values.get("storage_insights_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_transfer_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#storage_transfer_custom_endpoint GoogleProvider#storage_transfer_custom_endpoint}.'''
        result = self._values.get("storage_transfer_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#tags_custom_endpoint GoogleProvider#tags_custom_endpoint}.'''
        result = self._values.get("tags_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags_location_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#tags_location_custom_endpoint GoogleProvider#tags_location_custom_endpoint}.'''
        result = self._values.get("tags_location_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terraform_attribution_label_addition_strategy(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#terraform_attribution_label_addition_strategy GoogleProvider#terraform_attribution_label_addition_strategy}.'''
        result = self._values.get("terraform_attribution_label_addition_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpu_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#tpu_custom_endpoint GoogleProvider#tpu_custom_endpoint}.'''
        result = self._values.get("tpu_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transcoder_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#transcoder_custom_endpoint GoogleProvider#transcoder_custom_endpoint}.'''
        result = self._values.get("transcoder_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def universe_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#universe_domain GoogleProvider#universe_domain}.'''
        result = self._values.get("universe_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_project_override(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#user_project_override GoogleProvider#user_project_override}.'''
        result = self._values.get("user_project_override")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vertex_ai_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#vertex_ai_custom_endpoint GoogleProvider#vertex_ai_custom_endpoint}.'''
        result = self._values.get("vertex_ai_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vmwareengine_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#vmwareengine_custom_endpoint GoogleProvider#vmwareengine_custom_endpoint}.'''
        result = self._values.get("vmwareengine_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_access_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#vpc_access_custom_endpoint GoogleProvider#vpc_access_custom_endpoint}.'''
        result = self._values.get("vpc_access_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workbench_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#workbench_custom_endpoint GoogleProvider#workbench_custom_endpoint}.'''
        result = self._values.get("workbench_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflows_custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#workflows_custom_endpoint GoogleProvider#workflows_custom_endpoint}.'''
        result = self._values.get("workflows_custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#zone GoogleProvider#zone}.'''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.provider.GoogleProviderExternalCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "audience": "audience",
        "identity_token": "identityToken",
        "service_account_email": "serviceAccountEmail",
    },
)
class GoogleProviderExternalCredentials:
    def __init__(
        self,
        *,
        audience: builtins.str,
        identity_token: builtins.str,
        service_account_email: builtins.str,
    ) -> None:
        '''
        :param audience: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#audience GoogleProvider#audience}.
        :param identity_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#identity_token GoogleProvider#identity_token}.
        :param service_account_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_account_email GoogleProvider#service_account_email}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331f41525a02c8ff5015cb8d7e4f172be58cb05a8f174b1dd1d6005af02b0c90)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#audience GoogleProvider#audience}.'''
        result = self._values.get("audience")
        assert result is not None, "Required property 'audience' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#identity_token GoogleProvider#identity_token}.'''
        result = self._values.get("identity_token")
        assert result is not None, "Required property 'identity_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs#service_account_email GoogleProvider#service_account_email}.'''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleProviderExternalCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GoogleProvider",
    "GoogleProviderBatching",
    "GoogleProviderConfig",
    "GoogleProviderExternalCredentials",
]

publication.publish()

def _typecheckingstub__2b9c9a462b0aa745ad035967b873d8ce6f7e44eb4d193e40fd943d1eb67b81e4(
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
    apigee_custom_endpoint: typing.Optional[builtins.str] = None,
    apihub_custom_endpoint: typing.Optional[builtins.str] = None,
    apikeys_custom_endpoint: typing.Optional[builtins.str] = None,
    app_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    apphub_custom_endpoint: typing.Optional[builtins.str] = None,
    artifact_registry_custom_endpoint: typing.Optional[builtins.str] = None,
    assured_workloads_custom_endpoint: typing.Optional[builtins.str] = None,
    backup_dr_custom_endpoint: typing.Optional[builtins.str] = None,
    batching: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleProviderBatching, typing.Dict[builtins.str, typing.Any]]]]] = None,
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
    contact_center_insights_custom_endpoint: typing.Optional[builtins.str] = None,
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
    external_credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleProviderExternalCredentials, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filestore_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_app_check_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_app_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_data_connect_custom_endpoint: typing.Optional[builtins.str] = None,
    firebaserules_custom_endpoint: typing.Optional[builtins.str] = None,
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
    model_armor_custom_endpoint: typing.Optional[builtins.str] = None,
    model_armor_global_custom_endpoint: typing.Optional[builtins.str] = None,
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
    resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    resource_manager_v3_custom_endpoint: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    secret_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
    secure_source_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_management_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    securityposture_custom_endpoint: typing.Optional[builtins.str] = None,
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
    transcoder_custom_endpoint: typing.Optional[builtins.str] = None,
    universe_domain: typing.Optional[builtins.str] = None,
    user_project_override: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vertex_ai_custom_endpoint: typing.Optional[builtins.str] = None,
    vmwareengine_custom_endpoint: typing.Optional[builtins.str] = None,
    vpc_access_custom_endpoint: typing.Optional[builtins.str] = None,
    workbench_custom_endpoint: typing.Optional[builtins.str] = None,
    workflows_custom_endpoint: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e12059e57117a071bd42280927cce199ca1837d7c061b36cad0524aa493938(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5c0adeec5de750c28add2a691b4ab7cb2f3e95e6488613d444fe55e6364d5f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015d2d431258e890010396e2cf315ef61276700a821d468f2afd05e8563c98d9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7638d43620391b024d55e540d69cbff6e41b8e48ef1237ee48d59927379e12(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbac66b8848648dac2eb689252587ef2214ba3b79abdd0051854380846f4d4f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9cae4ac1d3ffebb6c3aed6ab7d1552cb22650bfcef5254b2844ceded00b9ad(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b5742bd7375a5efff231915d7f0e43c0856eecfb0e7a42d3f372e99fc34dc8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e327a82a5adefc5195b48cd138c55f5bd06ceea3576cd7fef33e6464a261976(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3cbfb662564ab3bcfd475ab8b074bdf09599c87ba3ab9cc682c3c21d709acf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee61df982220a8a44083010f2cded616f878f06b5f07dcb580189a375e532847(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a98f3b7926c58a33cf0aa43f49ebe3cf6586638ebe6f621ef14dbcff5d397f9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae9a98a94813329995757ec2600a43e8be3b12033b6d87b6699e88ed0b95724(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c368d7994d3692a90cdeda59bdf3445c90a7bd462a53dd37e3c1b523ba85f3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14b55c4d9f184f418ee32b83a64466f9050331eec158b1d955848f035fd27d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b6aa6c515b171800dd45441384f56ec577c3a79aa022df882d9dd922b88379(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ba90efbb1e513e996feaa3aa39bfea2dffd001dff4fb52e54ed0ef03bf52a8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83e36d866048786690a2c35886681b601c9e69aaad464c598d6eb7f6dc7b5ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleProviderBatching]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4d22b736f37213cc90cf0e8f962c13701762ffc4622195db3021eb5183e201(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e832964c7789e90b2cfb9044c4e11069b0ca063a9f2412253197247ee3fac007(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b504597e5425abf3440e942a2f94ec780ab7ad48355636e27ae605f9095824(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7961d901ebeddef40efe7b7dac34515d0aa4ef5d3b3ac423f7f43cbbbf90c83(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d8b794072e370274ca7f8155047fdc15d74070a5e3704580e3ce4d73d1e639(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90671a4a892c98cc587328a8b5d42fcae2b29edc7209cdb893330b2a3f4953ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a3ea9bfe743dd2a03c3fbf586fa13f8c8775661037ee44a01accaac84720e7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45f096e0b8dfcd471be3b1ab2f3e54046d34454374c29ffac5ff87270a431b1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99cd8eceb26f3af475fcfadec2636d108c0523d2e1f3aa5867bb798734037284(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d47470ca7241ee9d4a0b73c87355bbcd9b95d36fe18896ddb8fe740c149527c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa59053ee275d153b2e30d7d1c60dc51e1bdfcbf05e35111d5458ad424d64f5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fe93b9b505727a7e90189486be50f257fe4f743f6545b031ef2da715725290(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f07f0e1ba7c9afe93103041dcf9895dcc2ef5314b7bf1cf763c65ee803d3a46(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665011469859bd6c1a74abfb67ce4795061391e510bd79f72d769a305064b36e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a880df48ff11bc33c76ba0b2ee6d43649cb5ce3c010fa03ff1cc381e2100989d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a744b835514d2f6ab428c376d0cd4054ddf6bdb1762cfc0e7fd1628f9f9e202(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3b1d1bff2ac93dd75e2118219a364309450befa835605b3dddef0a471b6710(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b012c5c1b7b020f5c18d6a02543d6267853f7f892f4ac6961022378ed53773(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc29988ebc5a48de273d8a3d4dca69faa6d716d6176aebc69244761acd57e68(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb06ef9f40d3ed363a8d1f1129bea2076189ad1a2d3a74d95650c6cf89f4861(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e1ebd675816a832a25d3fd917b7cfb67031f4a23296a92d153426ad3167356(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7d8d5019969e564cc44b0467d0f8b07a3bc654e8553150149bdb38ae00e077(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712bda9c3547471e6974d396cccb5badb0875aba0b40721fdfeb4874726cc475(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13011133ed46f8e7db78260a78c6d57b976c28fe87e47278c2813cbc9e166f80(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2712e4e6ad6b2a71b3898570e9e8d17393cfa26f6f9f1f193b9bb3f3bc1c4f3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7407abeb13cdbd92caeca1c6f3d8ecc9ce935dfe6fbd66ddbb54a5b8aa616ba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba7e7065ec66ae3a85fa557249f3b7a7e151ca4a45c434cee7fb3b7b186e54a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a6779183376badb7fb68aa3b671c81d0595c00c7470e0f781b2a3118751b52(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b28954f903a9da29ea29137b4d5da03123029dab0a29b7f1113957afc077eb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0791a599c39393da130e47dd364bbb69bd6358d6c18f3156396e4ddabff545(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecdb62174497b029aaec3b2eba50d435ea1a34b509c57f4079aa898349d06575(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2a1b1e6ee13147ce4cc9f0b07cb155ba1a5eb7f2225ac052dc74a7bada22fe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcad339c3411726ea9b6f441802663f22e7f4b03e28598464653b8da9d36700(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9087460f92db4604c0d3b0f469733144dbe1154eed14dead87f6e7af07f160(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e6f61e2368c7d162d1b8374ccf259b4b99e7880f864f18d2187c15caa8b852(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0265109bb4aac70755830fb08348d90e7de58f7e9b9c74146ba6001740803dd9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522176c0806e7e8066d071f7ffb3537aa5cfb0b70e3b5216daf2a4ded9f4f5b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076fdca6833b704682b86bebe74630155f60b7204d0045bdf15fc7ac2f52c8f5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1180a66777f400fa458db866a0e8c16ab180ab409a6e93e1607896bb5ee4717(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86bb78dea946f6067c0307e3b96d84ec87f3940d21e651413b5c361da5c41ce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d041736f02803f109e96ba7c4a82f4721b53c9b0d6e27f5dcc779681c9083a3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9abb92094f9bf1bcce5efd8202a087b9f16de2578a0655ad5311e5dce74bfd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09248dab6ce94044e6bafa4fd7c402e7bfd17b15d8c72668ea1871db5269d827(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40feaa91b82dcfbbf3c8fd113255ac6ab570e4ea9d2fc3ae7fc3466f63e740ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619e71adfabec4d4492249d8a32aad64d7c27e69f326636f82b79cb91c6cc891(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df3ac65dec3328ed80e81fdf5315a7c13417e5a77488e6593b51c2eb12dfbff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391641acc421be6f8021ba8d6e952b672b3212b0ee32b15d68d072bf9ebadb6b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6f81f61ac78a9cbebf178d6db637370e7501e9d699d111245a0400c6e22285(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fceefeee935a2375eb957491952f05085ff61b8dffd123eef32bc53c4d71dc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3faf38f30bbdfe9f381489bb4008915f29d60a8f6a728180e930afdd9bdd3b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3528437c1bbcb2144d8c5ea59b0e35ec0f6073e397e5469ced79a9de4b0f8bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ba6747f8a38483d609c25f942dea439e0bc5f4c4cd4d224941e8430dcac82b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9035dac9bcb2912016af684886d2fe6c662ea57a69a84b780909090bb0c63e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8001af4c89858bf318038e47ffd1808cb8e77528efc966cd9438e33f7eebc99f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c7380e3793eb0577f1f3a0e57ddb9625fc13cea75eef00c62f83129dd49327(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0cfd2529237ec1c053ad3ca52ace8bb213c6401075ee99e95fead89d1be39d0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675d323b83f5eb76d03096ec8459a6959cc4f4276d02b1f1c788269a4845ecb4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2b2448205898541fe606c44189a648fc5da67d471dcfcfa2f8c85e2f9e0099(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77285d7604904c73c72143c4382154f849a10552f8f040c19650327535f423a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb1732d2de0c1ad24c0967ec9feb89b40a45987e5e540c841bc4a333567e552(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7534d48fcb48096aa9d64c1a4a813ba4986bb226ca4722faa786a752fa7f9987(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f3e42f3a1181b3709d477443e501ddf376abc27a2d5b33fe24a8c8ede78ccd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a359f3bd78e05fdd16e941f2c9ffc63e2227aa1d0ac03d47a280e9a555d8e1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871090028ccd9e4e77e4fb29de74b41d90caaf9631caef9cfe31a3b256266531(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51bcd247d127d5329e160ccaaa8082bd27c48ae70778c377570495a2760f9cf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e94722796e7de48e9cec699d7b62841736683f0203599f2086dfd5d8e95673(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf6b8ee1ac57d9f73e270560d3374673df2d9b5682a2d69151f98d47f662359(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2cf2bebbaf5f57ec28eaa324895d1714a39e2bc62426b729e69da11e6bad9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleProviderExternalCredentials]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f8081f7f042d9b185fedcd6eda325eb348c42541231f447aa1a01057ed04cc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb55fb7ffb701e5847aeae055ab4166c529af64eac6ac162e1a42daa5b10f53f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006126d4b1929d76173ffe0c3662e8b52d3de536cd9057ccf853f9a491c0d9f2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a8b538b225e3f6b01686039c118c744872f140cc631a3ef73cf808298ea578(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0089ea10e48efb5cf6c87c39eb3ba3fb28bd98bb315cc2226338cbd8cedece8a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5aceffbff7a2a626aa463dd3219bbea8ade3cc12f09fd8a33d9b74414062b8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f48706c44ec50fe94a481cdd9cbce32fcb3bf00ea90de0e29616a1e9958f1dd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a04ff8ad54bb3804c09695b20e20a671d5ffd94b3c1adae7b992048abb5625(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4928ddf1b51286a8d198d94a645c5a8d67f55a6bdfcb8906942c041a1098e344(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28aa3645f33c06e0f54f95637f8ecaaea04e267bf3a91a8c0dee07f8b41d7c96(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefbaa2f7b10493075a5133e27774ea3ddfff27775a5fd85e2fd661b9399ea5d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e76c30954749804826b4e29ae01fb32e276e766a82fa1b5bed31dba4752c9f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c20f4794b1722b4fc53caf935b1406b157d1549af3db010f15d2b258eef642(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58e429e2630752cf97b74243523a313d21a8a54815bbb48badf69f11a9a9c17(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da82c4bd1e2111eb7f19616d468b2bb8278497e8a549de56eb339b9ed34b003(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52c049e83201a4750f222474eefce4fcdaada014c812a436ebce3b82b8fc345(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fc5fb6135530545bbce339ecae493adc95b5de067ac7ace1a7b75c973c5467(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9478fed36fbf22f7a44247c1feb4087038be0d4fd6d030608ef86c5686672788(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a91cdf0add467e75b877fd1f39db09a9608d3faba6405c1120224f28c6063d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d4c6e1ca836c04d10a290089103d93aabbae66b0deb3c23a8158b8dd140b1f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d468e61d57002257de6c6a08668e53527861d7bddac55da9084fa95cc06dd45b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568ada9920b0bfce948c0da6826a420d3f7a74956a21673ac7d6479c5ac6885d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1be1fc705df36f6e49b32b17ef0814acd804821447ae5b496b792610e47af71(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68cc01615a8434b089a3b480d8b1c76322eb381bf8263487bc00007398ebee0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76abd832ed695cf5d1412e48c20593d9c2a564ba29f1ac265377cf7747a7708b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3139a9d40cb619878fbfe2fcb47485f53f84841e51d28ae3bc8f13eea1dffac6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7731c0d4060e2ca44156636f3f3970c5811f552d1d2834c16d5239b780c6d43a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57cf7387c16897db7f45328c505270aef993cfe2be4d0c1822894648a7a0b7f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b887ae5391a7ed74a6adf51a7d0b55f26422ed3b400a57c6db3df9d0e851c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e2fe0591708aa50224b35bbf119421239eeb99a7b1031098c75dc29f4fa792(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa59586f46e9143e1f0199911a4b00fbbc8b63e5a0b95b7f9328653f7fb81d82(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99eafbfbcecbc80f3e5730b7111f11bc141a7d1db93e46865e811a65cda285b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba1150671085cd70dea78679985498e6792b89421e0dfcae8ff0d4d401e7f97(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29eed68ed05f67b6986d852e1645eab423fa4edfa5f833074edd2cd8ae9c231a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0ee5315298bbb87e8a8323ddd20b8e0af65d6b3b9d71d1c1d603012a331398(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea3fad4627a7fd80135c9a5fe4b92448802bc64323f89b523a31c76c17710d9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d719e90211c978316d9872d02c04242550051a1f29289e224747017524cbf8b8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941fd8a6b3a88916ebe4156c48b5723da6cace555f27f0e4d19c31f29d51c46c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13135ac3e35dbb874a13fc79d607d6d11384cfc54b7f1630a808a0e08352e331(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9387b6b59f9cafb8c4638d6a660666cf94bbabaf9db0a453bbb49d4cb0fb33(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f200096e548e00c0c02c77845b4879afb7aac3ee15ac04a643135fec855ad3a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7439d289ae5d1f92fa0f52bb378302e5b40a0db13f2d20859e25dbef25980ce6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf2a4afc85ca8cf2eb2932ed85dce47dbeaa0b03904b8ffcf9458012cc86c04(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23749ed50f4c62f332bb5351b3648296006c57adeb02944bcc01bdf3944d3134(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d28fde2e261d6c0cb07afb0c412f5d040260e5ea2007dc0a8f2019938185cce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b08b69f26b387eeb22b91d23cc47e8ed978a7da353ad776e1917c2d66da4806(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78eb7ad5f06712d9564748d04e3efa29352fed51ece6051737d9049de98aea04(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3f44f9d990a27d03bfce2e5e7fef851ab7ac55aea35512fa7cea8710635c9e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe4529d157143410240ce0a48077901da70c9418b167d0654d1795e205c2e1c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53cfce5d62d084bc1890ee051bda67988ce1c9e413c32a7cc17c22f74c833010(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c4d458b5ec6bb315d1a545eca7f349330a467846e429645397d0712f4b472e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3f0734c5f8bd154845a06db218dc5b58b1f83bf46dad778b648a52f58c3d01(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff501d0d66a8eea80c4be567217a15bb5f907eaf2a9bc6cf0233ec70d509b69f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9f9ac025c9d8905713d1fb6002b96da1db5674e5e76f7d797ae8ea7ed40b15(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85493ad87918295a9b34818e76f60d3de86c87d501c07287fc522bda13ebb89e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfcc682bbdbd95dca76e4af07ce9695bb27043a232e61dd4e109b58d031860f3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5326db7210f292d6ae8495808ff6a8fa569c3d34108dc242fbeb69375a00c5b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb745ced4d24320d9a2087477c10be8f6729eba2d1aeec402151743c6e717386(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac62be79a428868d52f7451d398261c22d1b201c35ee90b141db961de426c56b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d40b4cbd3ef1cff0c73baefeda79a5665a0942ab0bc1dc4f32cb4fa51190a0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3105209a782ca83ea40369e72ba8b48da281e77be0b94d5cb2ecd792d818ad38(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e836f7bca51071f5f8efe393ec9aa4a91419126f6e2275f13f06e5a48bfe118a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806d04f231bf3ea05dd54c78bff1be61b3a0a130068bb5cff0b89aca87fff4c4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84e7555494d51a38353b2867373a5cc6306935cb538ad35c91321ac31d3f48f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa487fd257ff1e1516ada743f366a2a884f633bc42debadee158f8632cdd857(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba81ae96e33c174eb1e23b05805f13249f90cbb56de48578e3c9add7ebffb51(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af85b4f306a918c8435a7be2f360d1cb4852a5da77c75acf9c6bbef4ef03ad5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be5aef0fe1bc14407f10f8ccc3440991676c092a973c4e4f68aad6df4b32615(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7cf001c57b4df72acf38ab2c03892e7458841e76be009d9d9bc62b07766902(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7ca9563a58043e4cd5148f94d7822fac438ee00249ae01b5a15ad37b585202(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45da06525905cfb679f6389b8e8de3dbccee22ed08781223a783db9e7e25a1a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80ceb9f8dddab2adbee6158cbade2aa7f626691f736e7bd8aed27bffde1f862(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1093c258b75a9133610048d4f99f8a047ac789d01e27788e428d7723f2a79e98(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b4938055764d3c2be71cdab4e434385656bb5e4b8e1698a952bf1faab468f5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42bcb649cc59102425c20a123669a2f5da7104de071c7b4ea0ff53db8ad24673(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126d55833b48dfaba45f164fcf19ef314011d2a3e945639da122a240d249c414(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de3815d6d66cdc511904c846ca718c9d7b43e60e3c806967bf732ca16f89f52(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28064a67f72a7aa1b54559f681d2bf48d5cbfecf85ebb753bb54e016d449eb9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d838260ea73128cc4d5f9a1e9e5bd4c99fef65af703ba52f338de1fe168dab0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae3d16359ce356e5a84c8c896b4e85560dc4b567df63d136b46b7654d346110(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4baa66f16e5ba74871553d8a9674036208e1fb256c65cbdb141b79294168d480(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a31e83b9623c1f365445ae8d8669516b7b64a0fd3ac89464142505d6d80aaa2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc21283e39e3971327a5e8014bdec0157a7cc4fa5fd2fef8d455d4a124ec924b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e17f3e33ac5b1685c8e27a5d617ac8798056892e7ab860964be96d7545dcea(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1256a9557712bfd0ce3e07ca962b7057b4676a649fdae8f2f5fa0543fcd1e461(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b413ca8a9edc6d38ddb72add779c618b03c531b6aa989b8529bfe74ef7adb2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6133d4127c14311988f68fbf1dbe99efa3d4216063c3ea926b794f9400d3b2e6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49794f801e9500da11330bfeafe13807f17c98fff9961ee43290951ed01878c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ec2c45cdf665b34c663fa359efb82bc5121e938042c0dedf8284d235bebe28(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc0cef22329f2de38915eaa47dbbb49692444a7ef410d58cb19f3850a16a882(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ecdeb22e978c397b4e226d79b6bcad8aa325840214c2426b4b05e91490bf0a(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea2883d4937f94b4f36339087606fa726253d0ff9913e85205c5b342d096cd9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a6e517ee6458896d38d4faac90e73aeaf0d490a9cc3d6914f93b64d8031983(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88234b92931a104d47c6cf5c02ffecc7f049229430994128bc4b2728b750237(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176398c41aee01e6ad94b0b6dfa63ad6b99602dc0434be5363fc5c5854832590(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ea2d953395eaa15371d19df3e4449ac4bf2cf63e2806cf30667b70950845ce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97ccc5e86abdcbc07d3f426b0c7ed9e4510476fd420a978f3884ab31230f8b6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3956bddf410c41cab7d5dc93225b07c0b6a12cc9a13b463c21d4d2453de874f(
    *,
    enable_batching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_after: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9129c5feceef1a0d065989f96f621f2f6ce8c9a329998493f7b7a7b6ff4f6f0(
    *,
    access_approval_custom_endpoint: typing.Optional[builtins.str] = None,
    access_context_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    access_token: typing.Optional[builtins.str] = None,
    active_directory_custom_endpoint: typing.Optional[builtins.str] = None,
    add_terraform_attribution_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alias: typing.Optional[builtins.str] = None,
    alloydb_custom_endpoint: typing.Optional[builtins.str] = None,
    apigee_custom_endpoint: typing.Optional[builtins.str] = None,
    apihub_custom_endpoint: typing.Optional[builtins.str] = None,
    apikeys_custom_endpoint: typing.Optional[builtins.str] = None,
    app_engine_custom_endpoint: typing.Optional[builtins.str] = None,
    apphub_custom_endpoint: typing.Optional[builtins.str] = None,
    artifact_registry_custom_endpoint: typing.Optional[builtins.str] = None,
    assured_workloads_custom_endpoint: typing.Optional[builtins.str] = None,
    backup_dr_custom_endpoint: typing.Optional[builtins.str] = None,
    batching: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleProviderBatching, typing.Dict[builtins.str, typing.Any]]]]] = None,
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
    contact_center_insights_custom_endpoint: typing.Optional[builtins.str] = None,
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
    external_credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleProviderExternalCredentials, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filestore_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_app_check_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_app_hosting_custom_endpoint: typing.Optional[builtins.str] = None,
    firebase_data_connect_custom_endpoint: typing.Optional[builtins.str] = None,
    firebaserules_custom_endpoint: typing.Optional[builtins.str] = None,
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
    model_armor_custom_endpoint: typing.Optional[builtins.str] = None,
    model_armor_global_custom_endpoint: typing.Optional[builtins.str] = None,
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
    resource_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    resource_manager_v3_custom_endpoint: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    secret_manager_regional_custom_endpoint: typing.Optional[builtins.str] = None,
    secure_source_manager_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_management_custom_endpoint: typing.Optional[builtins.str] = None,
    security_center_v2_custom_endpoint: typing.Optional[builtins.str] = None,
    securityposture_custom_endpoint: typing.Optional[builtins.str] = None,
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
    transcoder_custom_endpoint: typing.Optional[builtins.str] = None,
    universe_domain: typing.Optional[builtins.str] = None,
    user_project_override: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vertex_ai_custom_endpoint: typing.Optional[builtins.str] = None,
    vmwareengine_custom_endpoint: typing.Optional[builtins.str] = None,
    vpc_access_custom_endpoint: typing.Optional[builtins.str] = None,
    workbench_custom_endpoint: typing.Optional[builtins.str] = None,
    workflows_custom_endpoint: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331f41525a02c8ff5015cb8d7e4f172be58cb05a8f174b1dd1d6005af02b0c90(
    *,
    audience: builtins.str,
    identity_token: builtins.str,
    service_account_email: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
