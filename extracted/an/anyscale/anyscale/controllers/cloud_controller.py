"""
Fetches data required and formats output for `anyscale cloud` commands.
"""

import copy
from datetime import datetime, timedelta
import difflib
import json
from os import getenv
import pathlib
import re
import secrets
import time
from typing import Any, Dict, List, MutableSequence, Optional, Tuple
import uuid

import boto3
from boto3.resources.base import ServiceResource as Boto3Resource
from botocore.exceptions import ClientError, NoCredentialsError
import click
from click import Abort, ClickException
import colorama
from rich.progress import Progress, track
import yaml

from anyscale import __version__ as anyscale_version
from anyscale.aws_iam_policies import get_anyscale_iam_permissions_ec2_restricted
from anyscale.cli_logger import CloudSetupLogger
from anyscale.client.openapi_client.models import (
    AWSConfig,
    AWSMemoryDBClusterConfig,
    CloudAnalyticsEventCloudResource,
    CloudAnalyticsEventCommandName,
    CloudAnalyticsEventName,
    CloudDeployment,
    CloudDeploymentConfig,
    CloudProviders,
    CloudState,
    CloudWithCloudResource,
    CloudWithCloudResourceGCP,
    ClusterManagementStackVersions,
    ComputeStack,
    CreateCloudResource,
    CreateCloudResourceGCP,
    EditableCloudResource,
    EditableCloudResourceGCP,
    FileStorage,
    GCPConfig,
    NFSMountTarget,
    SubnetIdWithAvailabilityZoneAWS,
    UpdateCloudWithCloudResource,
    UpdateCloudWithCloudResourceGCP,
    WriteCloud,
)
from anyscale.client.openapi_client.models.gcp_file_store_config import (
    GCPFileStoreConfig,
)
from anyscale.cloud_resource import (
    associate_aws_subnets_with_azs,
    GCS_STORAGE_PREFIX,
    S3_ARN_PREFIX,
    S3_STORAGE_PREFIX,
    verify_aws_cloudformation_stack,
    verify_aws_efs,
    verify_aws_iam_roles,
    verify_aws_memorydb_cluster,
    verify_aws_s3,
    verify_aws_security_groups,
    verify_aws_subnets,
    verify_aws_vpc,
)
from anyscale.cloud_utils import (
    get_cloud_id_and_name,
    get_cloud_resource_by_cloud_id,
    get_organization_id,
)
from anyscale.conf import ANYSCALE_IAM_ROLE_NAME
from anyscale.controllers.base_controller import BaseController
from anyscale.controllers.cloud_functional_verification_controller import (
    CloudFunctionalVerificationController,
    CloudFunctionalVerificationType,
)
from anyscale.formatters import clouds_formatter
from anyscale.job._private.job_sdk import (
    HA_JOB_STATE_TO_JOB_STATE,
    TERMINAL_HA_JOB_STATES,
)
from anyscale.shared_anyscale_utils.aws import AwsRoleArn
from anyscale.shared_anyscale_utils.conf import ANYSCALE_ENV, ANYSCALE_HOST
from anyscale.util import (  # pylint:disable=private-import
    _client,
    _get_aws_efs_mount_target_ip,
    _get_memorydb_cluster_config,
    _get_role,
    _update_external_ids_for_policy,
    confirm,
    GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS_LONG,
    get_anyscale_cross_account_iam_policies,
    get_available_regions,
    get_user_env_aws_account,
    prepare_cloudformation_template,
    REDIS_TLS_ADDRESS_PREFIX,
)
from anyscale.utils.cloud_update_utils import (
    CLOUDFORMATION_TIMEOUT_SECONDS_LONG,
    get_or_create_memorydb,
    MEMORYDB_REDIS_PORT,
    try_delete_customer_drifts_policy,
    update_iam_role,
)
from anyscale.utils.cloud_utils import (
    _unroll_resources_for_aws_list_call,
    CloudEventProducer,
    CloudSetupError,
    get_errored_resources_and_reasons,
    modify_memorydb_parameter_group,
    validate_aws_credentials,
    verify_anyscale_access,
    wait_for_gcp_lb_resource_termination,
)
from anyscale.utils.imports.gcp import (
    try_import_gcp_managed_setup_utils,
    try_import_gcp_utils,
    try_import_gcp_verify_lib,
)


ROLE_CREATION_RETRIES = 30
ROLE_CREATION_INTERVAL_SECONDS = 1

try:
    CLOUDFORMATION_TIMEOUT_SECONDS = int(getenv("CLOUDFORMATION_TIMEOUT_SECONDS", 300))
except ValueError:
    raise Exception(
        f"CLOUDFORMATION_TIMEOUT_SECONDS is set to {getenv('CLOUDFORMATION_TIMEOUT_SECONDS')}, which is not a valid integer."
    )


try:
    GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS = int(
        getenv("GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS", 600)
    )
except ValueError:
    raise Exception(
        f"GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS is set to {getenv('GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS')}, which is not a valid integer."
    )

IGNORE_CAPACITY_ERRORS = getenv("IGNORE_CAPACITY_ERRORS") is not None

# Constants forked from ray.autoscaler._private.aws.config
RAY = "ray-autoscaler"
DEFAULT_RAY_IAM_ROLE = RAY + "-v1"

# Only used in cloud edit.
BASE_ROLLBACK_COMMAND = "anyscale cloud edit --cloud-id={cloud_id}"


class CloudController(BaseController):
    def __init__(
        self,
        log: Optional[CloudSetupLogger] = None,
        initialize_auth_api_client: bool = True,
        cli_token: Optional[str] = None,
    ):
        """
        :param log: The logger to use for this controller. If not provided, a new logger will be created.
        :param initialize_auth_api_client: Whether to initialize the auth api client.
        :param cli_token: The CLI token to use for this controller. If provided, the CLI token will be used instead
        of the one in the config file or the one in the environment variable. This is for setting up AIOA clouds only.
        """
        if log is None:
            log = CloudSetupLogger()

        super().__init__(
            initialize_auth_api_client=initialize_auth_api_client, cli_token=cli_token,
        )

        self.log = log
        self.log.open_block("Output")
        if self.initialize_auth_api_client:
            self.cloud_event_producer = CloudEventProducer(
                cli_version=anyscale_version, api_client=self.api_client
            )

    def list_clouds(
        self, cloud_name: Optional[str], cloud_id: Optional[str], max_items: int
    ) -> str:
        if cloud_id is not None:
            clouds = [
                self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result
            ]
        elif cloud_name is not None:
            clouds = [
                self.api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post(
                    {"name": cloud_name}
                ).result
            ]
        else:
            clouds = self.api_client.list_clouds_api_v2_clouds_get().results
        clouds_output = clouds[:max_items]
        output = clouds_formatter.format_clouds_output(
            clouds=clouds_output, json_format=False
        )
        return str(output)

    def _get_anyscale_cross_account_iam_policies(
        self, cloud_id: str, _use_strict_iam_permissions: bool,
    ) -> List[Dict[str, str]]:
        iam_policy_parameters = get_anyscale_cross_account_iam_policies()
        if _use_strict_iam_permissions:
            anyscale_iam_permissions_ec2 = get_anyscale_iam_permissions_ec2_restricted(
                cloud_id
            )
            for parameter in iam_policy_parameters:
                if (
                    parameter["ParameterKey"]
                    == "AnyscaleCrossAccountIAMPolicySteadyState"
                ):
                    parameter["ParameterValue"] = json.dumps(
                        anyscale_iam_permissions_ec2
                    )
                    break
        return iam_policy_parameters

    def create_cloudformation_stack(  # noqa: PLR0913
        self,
        region: str,
        cloud_id: str,
        anyscale_iam_role_name: str,
        cluster_node_iam_role_name: str,
        enable_head_node_fault_tolerance: bool,
        anyscale_aws_account: str,
        _use_strict_iam_permissions: bool = False,  # This should only be used in testing.
        boto3_session: Optional[boto3.Session] = None,
        is_anyscale_hosted: bool = False,
        anyscale_hosted_network_info: Optional[Dict[str, Any]] = None,
    ):
        if boto3_session is None:
            boto3_session = boto3.Session(region_name=region)

        cfn_client = boto3_session.client("cloudformation", region_name=region)
        cfn_stack_name = cloud_id.replace("_", "-").lower()

        cfn_template_body = prepare_cloudformation_template(
            region,
            cfn_stack_name,
            cloud_id,
            enable_head_node_fault_tolerance,
            boto3_session,
            is_anyscale_hosted=is_anyscale_hosted,
        )

        parameters = [
            {"ParameterKey": "EnvironmentName", "ParameterValue": ANYSCALE_ENV},
            {"ParameterKey": "AnyscaleCLIVersion", "ParameterValue": anyscale_version},
            {"ParameterKey": "CloudID", "ParameterValue": cloud_id},
            {
                "ParameterKey": "AnyscaleAWSAccountID",
                "ParameterValue": anyscale_aws_account,
            },
            {
                "ParameterKey": "ClusterNodeIAMRoleName",
                "ParameterValue": cluster_node_iam_role_name,
            },
            {
                "ParameterKey": "MemoryDBRedisPort",
                "ParameterValue": MEMORYDB_REDIS_PORT,
            },
        ]
        if not is_anyscale_hosted:
            parameters.append(
                {
                    "ParameterKey": "AnyscaleCrossAccountIAMRoleName",
                    "ParameterValue": anyscale_iam_role_name,
                }
            )
            cross_account_iam_policies = self._get_anyscale_cross_account_iam_policies(
                cloud_id, _use_strict_iam_permissions
            )
            for parameter in cross_account_iam_policies:
                parameters.append(parameter)

        tags: MutableSequence[Any] = []
        if is_anyscale_hosted:
            # Add is-anyscale-hosted tag to the cloudformation stack which
            # the reconcile process will use to determine if the use the
            # shared resources.
            tags.append({"Key": "anyscale:cloud-id", "Value": cloud_id},)
            tags.append({"Key": "anyscale:is-anyscale-hosted", "Value": "true"},)

            # VPC ID are needed for creating security groups and subnets
            # are needed for mount targets in shared VPC clouds.
            if anyscale_hosted_network_info is not None:
                parameters.append(
                    {
                        "ParameterKey": "VpcId",
                        "ParameterValue": anyscale_hosted_network_info["vpc_id"],
                    },
                )

        cfn_client.create_stack(
            StackName=cfn_stack_name,
            TemplateBody=cfn_template_body,
            Parameters=parameters,  # type: ignore
            Capabilities=["CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND"],
            Tags=tags,
        )

    def run_cloudformation(  # noqa: PLR0913
        self,
        region: str,
        cloud_id: str,
        anyscale_iam_role_name: str,
        cluster_node_iam_role_name: str,
        enable_head_node_fault_tolerance: bool,
        anyscale_aws_account: str,
        _use_strict_iam_permissions: bool = False,  # This should only be used in testing.
        boto3_session: Optional[boto3.Session] = None,
    ) -> Dict[str, Any]:
        """
        Run cloudformation to create the AWS resources for a cloud.

        When enable_head_node_fault_tolerance is set to True, a memorydb cluster will be created.
        """
        if boto3_session is None:
            boto3_session = boto3.Session(region_name=region)

        cfn_client = boto3_session.client("cloudformation", region_name=region)
        cfn_stack_name = cloud_id.replace("_", "-").lower()

        cfn_template_body = prepare_cloudformation_template(
            region,
            cfn_stack_name,
            cloud_id,
            enable_head_node_fault_tolerance,
            boto3_session,
        )

        cross_account_iam_policies = self._get_anyscale_cross_account_iam_policies(
            cloud_id, _use_strict_iam_permissions
        )

        parameters = [
            {"ParameterKey": "EnvironmentName", "ParameterValue": ANYSCALE_ENV},
            {"ParameterKey": "AnyscaleCLIVersion", "ParameterValue": anyscale_version},
            {"ParameterKey": "CloudID", "ParameterValue": cloud_id},
            {
                "ParameterKey": "AnyscaleAWSAccountID",
                "ParameterValue": anyscale_aws_account,
            },
            {
                "ParameterKey": "AnyscaleCrossAccountIAMRoleName",
                "ParameterValue": anyscale_iam_role_name,
            },
            {
                "ParameterKey": "ClusterNodeIAMRoleName",
                "ParameterValue": cluster_node_iam_role_name,
            },
            {
                "ParameterKey": "MemoryDBRedisPort",
                "ParameterValue": MEMORYDB_REDIS_PORT,
            },
        ]
        for parameter in cross_account_iam_policies:
            parameters.append(parameter)

        self.log.debug("cloudformation body:")
        self.log.debug(cfn_template_body)

        cfn_client.create_stack(
            StackName=cfn_stack_name,
            TemplateBody=cfn_template_body,
            Parameters=parameters,  # type: ignore
            Capabilities=["CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND"],
        )

        stacks = cfn_client.describe_stacks(StackName=cfn_stack_name)
        cfn_stack = stacks["Stacks"][0]
        cfn_stack_url = f"https://{region}.console.aws.amazon.com/cloudformation/home?region={region}#/stacks/stackinfo?stackId={cfn_stack['StackId']}"
        self.log.info(f"\nTrack progress of cloudformation at {cfn_stack_url}")
        with self.log.spinner("Creating cloud resources through cloudformation..."):
            start_time = time.time()
            end_time = (
                start_time + CLOUDFORMATION_TIMEOUT_SECONDS_LONG
                if enable_head_node_fault_tolerance
                else start_time + CLOUDFORMATION_TIMEOUT_SECONDS
            )
            while time.time() < end_time:
                stacks = cfn_client.describe_stacks(StackName=cfn_stack_name)
                cfn_stack = stacks["Stacks"][0]
                if cfn_stack["StackStatus"] in (
                    "CREATE_FAILED",
                    "ROLLBACK_COMPLETE",
                    "ROLLBACK_IN_PROGRESS",
                ):
                    bucket_name = f"anyscale-{ANYSCALE_ENV}-data-{cfn_stack_name}"
                    try:
                        boto3_session.client("s3", region_name=region).delete_bucket(
                            Bucket=bucket_name
                        )
                        self.log.info(f"Successfully deleted {bucket_name}")
                    except Exception as e:  # noqa: BLE001
                        if not (
                            isinstance(e, ClientError)
                            and e.response["Error"]["Code"] == "NoSuchBucket"
                        ):
                            self.log.error(
                                f"Unable to delete the S3 bucket created by the cloud formation stack, please manually delete {bucket_name}"
                            )

                    # Describe events to get error reason
                    error_details = get_errored_resources_and_reasons(
                        cfn_client, cfn_stack_name
                    )
                    self.log.log_resource_error(
                        CloudAnalyticsEventCloudResource.AWS_CLOUDFORMATION,
                        f"Cloudformation stack failed to deploy. Detailed errors: {error_details}",
                    )
                    # Provide link to cloudformation
                    raise ClickException(
                        f"Failed to set up cloud resources. Please check your cloudformation stack for errors and to ensure that all resources created in this cloudformation stack were deleted: {cfn_stack_url}"
                    )
                if cfn_stack["StackStatus"] == "CREATE_COMPLETE":
                    if enable_head_node_fault_tolerance:
                        modify_memorydb_parameter_group(
                            cfn_stack_name, region, boto3_session
                        )
                    self.log.info(
                        f"Cloudformation stack {cfn_stack['StackId']} Completed"
                    )
                    break

                time.sleep(1)

            if time.time() > end_time:
                self.log.log_resource_error(
                    CloudAnalyticsEventCloudResource.AWS_CLOUDFORMATION,
                    "Cloudformation timed out.",
                )
                raise ClickException(
                    f"Timed out creating AWS resources. Please check your cloudformation stack for errors. {cfn_stack['StackId']}"
                )
        return cfn_stack  # type: ignore

    def run_deployment_manager(  # noqa: PLR0913
        self,
        factory: Any,
        deployment_name: str,
        cloud_id: str,
        project_id: str,
        region: str,
        anyscale_access_service_account: str,
        workload_identity_pool_name: str,
        anyscale_aws_account: str,
        organization_id: str,
        enable_head_node_fault_tolerance: bool,
    ):
        setup_utils = try_import_gcp_managed_setup_utils()

        anyscale_access_service_account_name = anyscale_access_service_account.split(
            "@"
        )[0]
        deployment_config = setup_utils.generate_deployment_manager_config(
            region,
            project_id,
            cloud_id,
            anyscale_access_service_account_name,
            workload_identity_pool_name,
            anyscale_aws_account,
            organization_id,
            enable_head_node_fault_tolerance,
        )

        self.log.debug("GCP Deployment Manager resource config:")
        self.log.debug(deployment_config)

        deployment = {
            "name": deployment_name,
            "target": {"config": {"content": deployment_config,},},
            "labels": [{"key": "anyscale-cloud-id", "value": cloud_id},],
        }

        deployment_client = factory.build("deploymentmanager", "v2")
        response = (
            deployment_client.deployments()
            .insert(project=project_id, body=deployment)
            .execute()
        )
        deployment_url = f"https://console.cloud.google.com/dm/deployments/details/{deployment_name}?project={project_id}"

        timeout_seconds = (
            GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS_LONG
            if enable_head_node_fault_tolerance
            else GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS
        )
        self.log.info(
            f"Note that it may take up to {int(timeout_seconds / 60)} minutes to create resources on GCP."
        )
        self.log.info(f"Track progress of Deployment Manager at {deployment_url}")
        with self.log.spinner("Creating cloud resources through Deployment Manager..."):
            start_time = time.time()
            end_time = start_time + timeout_seconds
            while time.time() < end_time:
                current_operation = (
                    deployment_client.operations()
                    .get(operation=response["name"], project=project_id)
                    .execute()
                )
                if current_operation.get("status", None) == "DONE":
                    if "error" in current_operation:
                        self.log.error(f"Error: {current_operation['error']}")
                        self.log.log_resource_error(
                            CloudAnalyticsEventCloudResource.GCP_DEPLOYMENT,
                            current_operation["error"],
                        )
                        raise ClickException(
                            f"Failed to set up cloud resources. Please check your Deployment Manager for errors and delete all resources created in this deployment: {deployment_url}"
                        )
                    # happy path
                    self.log.info("Deployment succeeded.")
                    return True
                time.sleep(1)
            # timeout
            self.log.log_resource_error(
                CloudAnalyticsEventCloudResource.GCP_DEPLOYMENT, "Deployment timed out."
            )
            raise ClickException(
                f"Timed out creating GCP resources. Please check your deployment for errors and delete all resources created in this deployment: {deployment_url}"
            )

    def get_create_cloud_resource_from_cfn_stack(
        self,
        cfn_stack: Dict[str, Any],
        enable_head_node_fault_tolerance: bool,
        anyscale_hosted_network_info: Optional[Dict[str, Any]] = None,
        anyscale_control_plane_role_arn: str = "",
    ) -> CreateCloudResource:
        if "Outputs" not in cfn_stack:
            raise ClickException(
                f"Timed out setting up cloud resources. Please check your cloudformation stack for errors. {cfn_stack['StackId']}"
            )

        cfn_resources = {}
        for resource in cfn_stack["Outputs"]:
            resource_type = resource["OutputKey"]
            resource_value = resource["OutputValue"]
            assert (
                resource_value is not None
            ), f"{resource_type} is not created properly. Please delete the cloud and try creating agian."
            cfn_resources[resource_type] = resource_value

        aws_subnets_with_availability_zones = (
            json.loads(cfn_resources["SubnetsWithAvailabilityZones"])
            if not anyscale_hosted_network_info
            else anyscale_hosted_network_info["subnet_ids"]
        )
        aws_vpc_id = (
            cfn_resources["VPC"]
            if not anyscale_hosted_network_info
            else anyscale_hosted_network_info["vpc_id"]
        )
        aws_security_groups = [cfn_resources["AnyscaleSecurityGroup"]]

        aws_efs_id = cfn_resources.get("EFS", None)
        aws_efs_mount_target_ip = cfn_resources.get("EFSMountTargetIP", None)
        anyscale_iam_role_arn = cfn_resources.get(
            "AnyscaleIAMRole", anyscale_control_plane_role_arn
        )
        cluster_node_iam_role_arn = cfn_resources["NodeIamRole"]

        if enable_head_node_fault_tolerance:
            memorydb = json.loads(cfn_resources["MemoryDB"])
            memorydb_cluster_config = AWSMemoryDBClusterConfig(
                id=memorydb["arn"],
                endpoint=f'{REDIS_TLS_ADDRESS_PREFIX}{memorydb["ClusterEndpointAddress"]}:{MEMORYDB_REDIS_PORT}',
            )
        else:
            memorydb_cluster_config = None

        bucket_name = cfn_resources.get("S3Bucket", "")
        if bucket_name.startswith(S3_ARN_PREFIX):
            bucket_name = bucket_name[len(S3_ARN_PREFIX) :]

        return CreateCloudResource(
            aws_vpc_id=aws_vpc_id,
            aws_subnet_ids_with_availability_zones=[
                SubnetIdWithAvailabilityZoneAWS(
                    subnet_id=subnet_with_az["subnet_id"],
                    availability_zone=subnet_with_az["availability_zone"],
                )
                for subnet_with_az in aws_subnets_with_availability_zones
            ],
            aws_iam_role_arns=[anyscale_iam_role_arn, cluster_node_iam_role_arn],
            aws_security_groups=aws_security_groups,
            aws_s3_id=bucket_name,
            aws_efs_id=aws_efs_id,
            aws_efs_mount_target_ip=aws_efs_mount_target_ip,
            aws_cloudformation_stack_id=cfn_stack["StackId"],
            memorydb_cluster_config=memorydb_cluster_config,
            cloud_storage_bucket_name=S3_STORAGE_PREFIX + bucket_name,
        )

    def update_cloud_with_resources(
        self,
        cfn_stack: Dict[str, Any],
        cloud_id: str,
        enable_head_node_fault_tolerance: bool,
    ):
        create_cloud_resource = self.get_create_cloud_resource_from_cfn_stack(
            cfn_stack, enable_head_node_fault_tolerance
        )
        with self.log.spinner("Updating Anyscale cloud with cloud resources..."):
            self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
                cloud_id=cloud_id,
                update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                    cloud_resource_to_update=create_cloud_resource
                ),
            )

    def update_cloud_with_resources_gcp(
        self,
        factory: Any,
        deployment_name: str,
        cloud_id: str,
        project_id: str,
        anyscale_access_service_account: str,
    ):
        setup_utils = try_import_gcp_managed_setup_utils()
        gcp_utils = try_import_gcp_utils()
        anyscale_access_service_account_name = anyscale_access_service_account.split(
            "@"
        )[0]

        cloud_resources = setup_utils.get_deployment_resources(
            factory, deployment_name, project_id, anyscale_access_service_account_name
        )
        gcp_vpc_id = cloud_resources["compute.v1.network"]
        gcp_subnet_ids = [cloud_resources["compute.v1.subnetwork"]]
        gcp_cluster_node_service_account_email = f'{cloud_resources["iam.v1.serviceAccount"]}@{anyscale_access_service_account.split("@")[-1]}'
        gcp_anyscale_iam_service_account_email = anyscale_access_service_account
        gcp_firewall_policy = cloud_resources[
            "gcp-types/compute-v1:networkFirewallPolicies"
        ]
        gcp_firewall_policy_ids = [gcp_firewall_policy]
        gcp_cloud_storage_bucket_id = cloud_resources["storage.v1.bucket"]
        gcp_deployment_manager_id = deployment_name

        gcp_filestore_config = None
        if cloud_resources.get("filestore_location") and cloud_resources.get(
            "filestore_instance"
        ):
            gcp_filestore_config = gcp_utils.get_gcp_filestore_config(
                factory,
                project_id,
                gcp_vpc_id,
                cloud_resources["filestore_location"],
                cloud_resources["filestore_instance"],
                self.log,
            )
        memorystore_instance_config = gcp_utils.get_gcp_memorystore_config(
            factory, cloud_resources.get("memorystore_name"),
        )
        try:
            setup_utils.configure_firewall_policy(
                factory, gcp_vpc_id, project_id, gcp_firewall_policy
            )

            create_cloud_resource_gcp = CreateCloudResourceGCP(
                gcp_vpc_id=gcp_vpc_id,
                gcp_subnet_ids=gcp_subnet_ids,
                gcp_cluster_node_service_account_email=gcp_cluster_node_service_account_email,
                gcp_anyscale_iam_service_account_email=gcp_anyscale_iam_service_account_email,
                gcp_filestore_config=gcp_filestore_config,
                gcp_firewall_policy_ids=gcp_firewall_policy_ids,
                gcp_cloud_storage_bucket_id=gcp_cloud_storage_bucket_id,
                gcp_deployment_manager_id=gcp_deployment_manager_id,
                memorystore_instance_config=memorystore_instance_config,
                cloud_storage_bucket_name=GCS_STORAGE_PREFIX
                + gcp_cloud_storage_bucket_id,
            )
            self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put(
                cloud_id=cloud_id,
                update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                    cloud_resource_to_update=create_cloud_resource_gcp,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            for firewall_policy_name in gcp_firewall_policy_ids:
                setup_utils.remove_firewall_policy_associations(
                    factory, project_id, firewall_policy_name
                )
            raise ClickException(
                f"Error occurred when updating resources for the cloud {cloud_id}."
            )

    def prepare_for_managed_cloud_setup(
        self,
        region: str,
        cloud_name: str,
        cluster_management_stack_version: ClusterManagementStackVersions,
        auto_add_user: bool,
        is_aioa: bool = False,
        boto3_session: Optional[boto3.Session] = None,
    ) -> Tuple[str, str]:
        regions_available = get_available_regions(boto3_session)
        if region not in regions_available:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                succeeded=False,
                internal_error=f"Region '{region}' is not available.",
            )
            raise ClickException(
                f"Region '{region}' is not available. Regions available are: "
                f"{', '.join(map(repr, regions_available))}"
            )

        for _ in range(5):
            anyscale_iam_role_name = "{}-{}".format(
                ANYSCALE_IAM_ROLE_NAME, secrets.token_hex(4)
            )
            try:
                role = _get_role(anyscale_iam_role_name, region, boto3_session)
            except Exception as e:  # noqa: BLE001
                if isinstance(e, NoCredentialsError):
                    # Rewrite the error message to be more user friendly
                    self.cloud_event_producer.produce(
                        CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                        succeeded=False,
                        internal_error="Unable to locate AWS credentials.",
                    )
                    raise ClickException(
                        "Unable to locate AWS credentials. Please make sure you have AWS credentials configured."
                    )
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                    succeeded=False,
                    internal_error=str(e),
                )
                raise ClickException(f"Failed to get IAM role: {e}")
            if role is None:
                break
        else:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                succeeded=False,
                internal_error="Unable to find an available AWS IAM Role name",
            )
            raise ClickException(
                "We weren't able to connect your account with the Anyscale because we weren't able to find an available IAM Role name in your account. Please reach out to support or your SA for assistance."
            )

        user_aws_account_id = get_user_env_aws_account(region)
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.PREPROCESS_COMPLETE, succeeded=True,
        )
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="AWS",
                    region=region,
                    credentials=AwsRoleArn.from_role_name(
                        user_aws_account_id, anyscale_iam_role_name
                    ).to_string(),
                    name=cloud_name,
                    is_bring_your_own_resource=False,
                    cluster_management_stack_version=cluster_management_stack_version,
                    auto_add_user=auto_add_user,
                    is_aioa=is_aioa,
                )
            ).result
            self.cloud_event_producer.set_cloud_id(created_cloud.id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED, succeeded=True,
            )
        except ClickException as e:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED,
                succeeded=False,
                internal_error=str(e),
            )
            raise

        return anyscale_iam_role_name, created_cloud.id

    def prepare_for_managed_cloud_setup_gcp(  # noqa: PLR0913
        self,
        project_id: str,
        region: str,
        cloud_name: str,
        factory: Any,
        cluster_management_stack_version: ClusterManagementStackVersions,
        auto_add_user: bool,
        is_aioa: bool = False,
    ) -> Tuple[str, str, str]:
        setup_utils = try_import_gcp_managed_setup_utils()

        # choose an service account name and create a provider pool
        for _ in range(5):
            token = secrets.token_hex(4)
            anyscale_access_service_account = (
                f"anyscale-access-{token}@{project_id}.iam.gserviceaccount.com"
            )
            service_account = setup_utils.get_anyscale_gcp_access_service_acount(
                factory, anyscale_access_service_account
            )
            if service_account is not None:
                continue
            pool_id = f"anyscale-provider-pool-{token}"
            wordload_identity_pool = setup_utils.get_workload_identity_pool(
                factory, project_id, pool_id
            )
            if wordload_identity_pool is None:
                break
        else:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                succeeded=False,
                internal_error="Unable to find an available GCP service account name and create a provider pool.",
            )
            raise ClickException(
                "We weren't able to connect your account with the Anyscale because we weren't able to find an available service account name and create a provider pool in your GCP project. Please reach out to support or your SA for assistance."
            )

        # build credentials
        project_number = setup_utils.get_project_number(factory, project_id)
        provider_id = "anyscale-access"
        pool_name = f"{project_number}/locations/global/workloadIdentityPools/{pool_id}"
        provider_name = f"{pool_name}/providers/{provider_id}"
        credentials = json.dumps(
            {
                "project_id": project_id,
                "provider_id": provider_name,
                "service_account_email": anyscale_access_service_account,
            }
        )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.PREPROCESS_COMPLETE, succeeded=True,
        )

        # create a cloud
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="GCP",
                    region=region,
                    credentials=credentials,
                    name=cloud_name,
                    is_bring_your_own_resource=False,
                    cluster_management_stack_version=cluster_management_stack_version,
                    auto_add_user=auto_add_user,
                    is_aioa=is_aioa,
                )
            ).result
            self.cloud_event_producer.set_cloud_id(created_cloud.id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED, succeeded=True,
            )
        except ClickException as e:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED,
                succeeded=False,
                internal_error=str(e),
            )
            raise
        return anyscale_access_service_account, pool_name, created_cloud.id

    def create_workload_identity_federation_provider(
        self,
        factory: Any,
        project_id: str,
        pool_id: str,
        anyscale_access_service_account: str,
    ):
        setup_utils = try_import_gcp_managed_setup_utils()
        # create provider pool
        pool_display_name = "Anyscale provider pool"
        pool_description = f"Workload Identity Provider Pool for Anyscale access service account {anyscale_access_service_account}"

        wordload_identity_pool = setup_utils.create_workload_identity_pool(
            factory, project_id, pool_id, self.log, pool_display_name, pool_description,
        )
        try:
            # create provider
            provider_display_name = "Anyscale Access"
            provider_id = "anyscale-access"
            anyscale_aws_account = (
                self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
            )
            organization_id = get_organization_id(self.api_client)
            setup_utils.create_anyscale_aws_provider(
                factory,
                organization_id,
                wordload_identity_pool,
                provider_id,
                anyscale_aws_account,
                provider_display_name,
                self.log,
            )
        except ClickException as e:
            # delete provider pool if there's an exception
            setup_utils.delete_workload_identity_pool(
                factory, wordload_identity_pool, self.log
            )
            raise ClickException(
                f"Error occurred when trying to set up workload identity federation: {e}"
            )

    def wait_for_cloud_to_be_active(
        self, cloud_id: str, cloud_provider: CloudProviders
    ) -> None:
        """
        Waits for the cloud to be active
        """
        with self.log.spinner("Setting up resources on Anyscale for your new cloud..."):
            try:
                # The ingress for cloud admin zone may not be ready yet, so we need to wait for it to be active.
                # We use the cloud functional verification controller to create a cluster compute config to wait
                # for the cloud admin zone to be active.
                if self.initialize_auth_api_client:
                    CloudFunctionalVerificationController(
                        self.cloud_event_producer, self.log
                    ).get_or_create_cluster_compute(cloud_id, cloud_provider)
            except Exception:  # noqa: BLE001
                self.log.error(
                    "Timed out waiting for cloud admin zone to be active. Your cloud may not be set up properly. Please reach out to Anyscale support for assistance."
                )

    def setup_managed_cloud(  # noqa: PLR0912
        self,
        *,
        provider: str,
        region: str,
        name: str,
        functional_verify: Optional[str],
        cluster_management_stack_version: ClusterManagementStackVersions,
        enable_head_node_fault_tolerance: bool,
        project_id: Optional[str] = None,
        is_aioa: bool = False,
        yes: bool = False,
        boto3_session: Optional[
            boto3.Session
        ] = None,  # This is used by AIOA cloud setup
        _use_strict_iam_permissions: bool = False,  # This should only be used in testing.
        auto_add_user: bool = True,
    ) -> None:
        """
        Sets up a cloud provider
        """
        # TODO (congding): split this function into smaller functions per cloud provider
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        if provider == "aws":
            if boto3_session is None:
                # If boto3_session is not provided, we will create a new session with the given region.
                boto3_session = boto3.Session(region_name=region)
            if not validate_aws_credentials(self.log, boto3_session):
                raise ClickException(
                    "Cloud setup requires valid AWS credentials to be set locally. Learn more: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html"
                )
            self.cloud_event_producer.init_trace_context(
                CloudAnalyticsEventCommandName.SETUP, CloudProviders.AWS
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.COMMAND_START, succeeded=True,
            )
            with self.log.spinner("Preparing environment for cloud setup..."):
                (
                    anyscale_iam_role_name,
                    cloud_id,
                ) = self.prepare_for_managed_cloud_setup(
                    region,
                    name,
                    cluster_management_stack_version,
                    auto_add_user,
                    is_aioa,
                    boto3_session,
                )

            try:
                anyscale_aws_account = (
                    self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
                )
                cfn_stack = self.run_cloudformation(
                    region,
                    cloud_id,
                    anyscale_iam_role_name,
                    f"{cloud_id}-cluster_node_role",
                    enable_head_node_fault_tolerance,
                    anyscale_aws_account,
                    _use_strict_iam_permissions=_use_strict_iam_permissions,
                    boto3_session=boto3_session,
                )
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_CREATED, succeeded=True,
                )
            except Exception as e:  # noqa: BLE001
                self.log.error(str(e))
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_CREATED,
                    succeeded=False,
                    logger=self.log,
                    internal_error=str(e),
                )
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
                raise ClickException("Cloud setup failed!")

            try:
                self.update_cloud_with_resources(
                    cfn_stack, cloud_id, enable_head_node_fault_tolerance
                )
                self.wait_for_cloud_to_be_active(cloud_id, CloudProviders.AWS)
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.INFRA_SETUP_COMPLETE, succeeded=True,
                )
            except Exception as e:  # noqa: BLE001
                self.log.error(str(e))
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.INFRA_SETUP_COMPLETE,
                    succeeded=False,
                    internal_error=str(e),
                )
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
                raise ClickException("Cloud setup failed!")

            self.verify_aws_cloud_quotas(region=region, boto3_session=boto3_session)

            self.log.info(f"Successfully created cloud {name}, and it's ready to use.")
        elif provider == "gcp":
            if project_id is None:
                raise click.ClickException("Please provide a value for --project-id")
            gcp_utils = try_import_gcp_utils()
            setup_utils = try_import_gcp_managed_setup_utils()
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
            self.cloud_event_producer.init_trace_context(
                CloudAnalyticsEventCommandName.SETUP, CloudProviders.GCP
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.COMMAND_START, succeeded=True,
            )
            with self.log.spinner("Preparing environment for cloud setup..."):
                try:
                    organization_id = get_organization_id(self.api_client)
                    anyscale_aws_account = (
                        self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
                    )
                    # Enable APIs in the given GCP project
                    setup_utils.enable_project_apis(
                        factory, project_id, self.log, enable_head_node_fault_tolerance
                    )
                    # We need the Google APIs Service Agent to have security admin permissions on the project
                    # so that we can set IAM policy on Anyscale access service account
                    project_number = setup_utils.get_project_number(
                        factory, project_id
                    ).split("/")[-1]
                    google_api_service_agent = f"serviceAccount:{project_number}@cloudservices.gserviceaccount.com"
                    setup_utils.append_project_iam_policy(
                        factory,
                        project_id,
                        "roles/iam.securityAdmin",
                        google_api_service_agent,
                    )

                except ClickException as e:
                    self.cloud_event_producer.produce(
                        CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                        succeeded=False,
                        logger=self.log,
                        internal_error=str(e),
                    )
                    self.log.error(str(e))
                    raise ClickException("Cloud setup failed!")

                (
                    anyscale_access_service_account,
                    pool_name,
                    cloud_id,
                ) = self.prepare_for_managed_cloud_setup_gcp(
                    project_id,
                    region,
                    name,
                    factory,
                    cluster_management_stack_version,
                    auto_add_user,
                    is_aioa,
                )

            pool_id = pool_name.split("/")[-1]
            deployment_name = cloud_id.replace("_", "-").lower()
            deployment_succeed = False
            try:
                with self.log.spinner(
                    "Creating workload identity federation provider for Anyscale access..."
                ):
                    self.create_workload_identity_federation_provider(
                        factory, project_id, pool_id, anyscale_access_service_account
                    )
                deployment_succeed = self.run_deployment_manager(
                    factory,
                    deployment_name,
                    cloud_id,
                    project_id,
                    region,
                    anyscale_access_service_account,
                    pool_name,
                    anyscale_aws_account,
                    organization_id,
                    enable_head_node_fault_tolerance,
                )
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_CREATED, succeeded=True,
                )
            except Exception as e:  # noqa: BLE001
                self.log.error(str(e))
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_CREATED,
                    succeeded=False,
                    internal_error=str(e),
                    logger=self.log,
                )
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
                setup_utils.delete_workload_identity_pool(factory, pool_name, self.log)
                raise ClickException("Cloud setup failed!")

            try:
                with self.log.spinner(
                    "Updating Anyscale cloud with cloud resources..."
                ):
                    self.update_cloud_with_resources_gcp(
                        factory,
                        deployment_name,
                        cloud_id,
                        project_id,
                        anyscale_access_service_account,
                    )
                self.wait_for_cloud_to_be_active(cloud_id, CloudProviders.GCP)
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.INFRA_SETUP_COMPLETE, succeeded=True,
                )
            except Exception as e:  # noqa: BLE001
                self.log.error(str(e))
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.INFRA_SETUP_COMPLETE,
                    succeeded=False,
                    internal_error=str(e),
                )
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
                if deployment_succeed:
                    # only clean up deployment if it's created successfully
                    # otherwise keep the deployment for customers to check the errors
                    setup_utils.delete_gcp_deployment(
                        factory, project_id, deployment_name
                    )
                setup_utils.delete_workload_identity_pool(factory, pool_name, self.log)
                raise ClickException("Cloud setup failed!")

            self.log.info(f"Successfully created cloud {name}, and it's ready to use.")
        else:
            raise ClickException(
                f"Invalid Cloud provider: {provider}. Available providers are [aws, gcp]."
            )

        if len(functions_to_verify) > 0:
            CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(
                cloud_id,
                self._get_cloud_provider_from_str(provider),
                functions_to_verify,
                yes,
            )

    def _add_redis_cluster_aws(
        self, cloud: Any, cloud_resource: CreateCloudResource, yes: bool = False
    ):
        # Check if memorydb cluster already exists
        if cloud_resource.memorydb_cluster_config is not None:
            memorydb_name = cloud_resource.memorydb_cluster_config.id
            self.log.info(f"AWS memorydb {memorydb_name} already exists. ")
            return

        # Get or create memorydb cluster
        try:
            memorydb_cluster_id = get_or_create_memorydb(
                cloud.region, cloud_resource.aws_cloudformation_stack_id, self.log, yes,
            )
            memorydb_cluster_config = _get_memorydb_cluster_config(
                memorydb_cluster_id, cloud.region, self.log
            )
        except Exception as e:  # noqa: BLE001
            raise ClickException(f"Failed to create memorydb cluster: {e}")

        # Edit cloud resource record
        try:
            self.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_patch(
                cloud_id=cloud.id,
                editable_cloud_resource=EditableCloudResource(
                    memorydb_cluster_config=memorydb_cluster_config,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                "Failed to update resources on Anyscale. Please reach out to Anyscale support or your SA for assistance."
            )

    def _add_redis_cluster_gcp(
        self, cloud: Any, cloud_resource: CreateCloudResourceGCP, yes: bool = False
    ):
        if cloud_resource.memorystore_instance_config is not None:
            memorystore_name = cloud_resource.memorystore_instance_config.name
            self.log.info(f"GCP memorystore {memorystore_name} already exists. ")
            return

        gcp_utils = try_import_gcp_utils()
        managed_setup_utils = try_import_gcp_managed_setup_utils()
        project_id = self._get_project_id(cloud, cloud.name, cloud.id)
        factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
        deployment_name = cloud_resource.gcp_deployment_manager_id
        try:
            memorystore_instance_name = managed_setup_utils.get_or_create_memorystore_gcp(
                factory,
                cloud.id,
                deployment_name,
                project_id,
                cloud.region,
                self.log,
                yes,
            )
            memorystore_instance_config = gcp_utils.get_gcp_memorystore_config(
                factory, memorystore_instance_name
            )
        except Exception as e:  # noqa: BLE001
            raise ClickException(f"Failed to create GCP memorystore. Error: {e}")
        try:
            self.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_patch(
                cloud_id=cloud.id,
                editable_cloud_resource_gcp=EditableCloudResourceGCP(
                    memorystore_instance_config=memorystore_instance_config,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                "Cloud update failed! Please reach out to Anyscale support or your SA for assistance."
            )

    def _update_auto_add_user_field(self, auto_add_user: bool, cloud) -> None:
        if cloud.auto_add_user == auto_add_user:
            self.log.info(
                f"No updated required to the auto add user value. Cloud {cloud.name}({cloud.id}) "
                f"has auto add user {'enabled' if auto_add_user else 'disabled'}."
            )
        else:
            self.api_client.update_cloud_auto_add_user_api_v2_clouds_cloud_id_auto_add_user_put(
                cloud.id, auto_add_user=auto_add_user
            )
            if auto_add_user:
                self.log.info(
                    f"Auto add user for cloud {cloud.name}({cloud.id}) has been successfully enabled. Note: There may be up to 30 "
                    "sec delay for all users to be granted permissions after this feature is enabled."
                )
            else:
                self.log.info(
                    f"Auto add user for cloud {cloud.name}({cloud.id}) has been successfully disabled. No existing "
                    "cloud permissions were altered by this flag. Users added to the organization in the future will not "
                    "automatically be added to this cloud."
                )

    def _update_customer_aggregated_logs_config(self, cloud_id: str, is_enabled: bool):
        self.api_client.update_customer_aggregated_logs_config_api_v2_clouds_cloud_id_update_customer_aggregated_logs_config_put(
            cloud_id=cloud_id, is_enabled=is_enabled,
        )

    def update_managed_cloud(  # noqa: PLR0912, C901
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        enable_head_node_fault_tolerance: bool,
        functional_verify: Optional[str],
        yes: bool = False,
        auto_add_user: Optional[bool] = None,
    ) -> None:
        """
        Updates managed cloud.

        If `enable_head_node_fault_tolerance` is set to True, we will add redis clusters to the cloud.
        Otherwise it only updates the inline IAM policies associated with the cross account IAM role for AWS clouds.
        """
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )
        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result
        if cloud.is_bring_your_own_resource or cloud.is_bring_your_own_resource is None:
            # If cloud.is_bring_your_own_resource is None, we couldn't tell it's a registered cloud or a managed cloud.
            # But it should be an old cloud so that we could just abort.
            raise ClickException(
                "Cannot update cloud with customer defined resources. Please modify the resources by `anyscale cloud edit`"
            )
        cloud_resource = get_cloud_resource_by_cloud_id(
            cloud_id, cloud.provider, self.api_client
        )
        if cloud_resource is None:
            raise ClickException(
                f"This cloud {cloud_name}({cloud_id}) does not contain resource records. Please delete this cloud and create a new one."
            )
        if anyscale_version == "0.0.0-dev":
            confirm(
                "You are using a development version of Anyscale CLI. Still want to update the cloud?",
                yes,
            )
        if auto_add_user is not None:
            self._update_auto_add_user_field(auto_add_user, cloud)
            msg = ""
            if cloud.provider == CloudProviders.AWS:
                msg = (
                    " Note: The inline IAM policies associated with the cross account IAM role of this AWS cloud "
                    f"were not updated because {'--enable-auto-add-user' if auto_add_user else '--disable-auto-add-user'} "
                    "was specified. Please re-run `anyscale cloud update` if you want to update these IAM policies."
                )
            self.log.info("Cloud update completed." + msg)
            return

        self.cloud_event_producer.init_trace_context(
            CloudAnalyticsEventCommandName.UPDATE, cloud.provider, cloud_id
        )
        if enable_head_node_fault_tolerance:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.COMMAND_START, succeeded=True,
            )
            try:
                if cloud.provider == CloudProviders.AWS:
                    self._add_redis_cluster_aws(cloud, cloud_resource, yes)
                elif cloud.provider == CloudProviders.GCP:
                    self._add_redis_cluster_gcp(cloud, cloud_resource, yes)
                else:
                    raise ClickException(
                        f"Unsupported cloud provider {cloud.provider}. Only AWS and GCP are supported for fault tolerance."
                    )
            except Exception as e:  # noqa: BLE001
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.REDIS_CLUSTER_ADDED,
                    succeeded=False,
                    internal_error=str(e),
                )
                raise ClickException(f"Cloud update failed! {e}")
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.REDIS_CLUSTER_ADDED, succeeded=True
            )
        else:
            # Update IAM permissions
            if cloud.provider != CloudProviders.AWS:
                raise ClickException(
                    f"Unsupported cloud provider {cloud.provider}. Only AWS is supported for updating."
                )
            aws_cloudformation_stack_id = cloud_resource.aws_cloudformation_stack_id
            if aws_cloudformation_stack_id is None:
                raise ClickException(
                    f"This cloud {cloud.name}({cloud.id}) does not have an associated cloudformation stack. Please contact Anyscale support."
                )

            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.COMMAND_START, succeeded=True,
            )
            try:
                update_iam_role(
                    cloud.region, aws_cloudformation_stack_id, self.log, yes
                )
            except Exception as e:  # noqa: BLE001
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.IAM_ROLE_UPDATED,
                    succeeded=False,
                    internal_error=str(e),
                )
                raise ClickException(f"Cloud update failed! {e}")
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.IAM_ROLE_UPDATED, succeeded=True,
            )

        self.log.info("Cloud update completed.")

        if len(functions_to_verify) > 0:
            CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(
                cloud_id, CloudProviders.AWS, functions_to_verify, yes,
            )

    def get_cloud_deployments(self, cloud_id: str) -> Dict[str, Any]:
        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(
            cloud_id=cloud_id,
        ).result

        if cloud.is_aioa:
            raise ValueError(
                "Listing cloud deployments is only supported for customer-hosted clouds."
            )

        try:
            deployments = self.api_client.get_cloud_deployments_api_v2_clouds_cloud_id_deployments_get(
                cloud_id=cloud_id,
            ).results
        except Exception as e:  # noqa: BLE001
            raise ClickException(
                f"Failed to get cloud deployments for cloud {cloud.name} ({cloud_id}). Error: {e}"
            )

        # Avoid displaying fields with empty values (since the values for optional fields default to None).
        def remove_empty_values(d):
            if isinstance(d, dict):
                return {
                    k: remove_empty_values(v)
                    for k, v in d.items()
                    if remove_empty_values(v)
                }
            return d

        return {
            "id": cloud_id,
            "name": cloud.name,
            "deployments": [
                remove_empty_values(deployment.to_dict()) for deployment in deployments
            ],
        }

    def update_aws_anyscale_iam_role(
        self,
        cloud_id: str,
        region: str,
        anyscale_iam_role_id: Optional[str],
        external_id: Optional[str],
    ) -> Tuple[Optional[Boto3Resource], Optional[str]]:
        """
        Updates the Anyscale IAM role's assume policy to include the cloud ID as the external ID.
        Returns the role and the original policy document.
        """
        if not anyscale_iam_role_id:
            # anyscale_iam_role_id is optional for k8s
            return None, None

        organization_id = get_organization_id(self.api_client)
        if external_id and not external_id.startswith(organization_id):
            raise ClickException(
                f"Invalid external ID: external ID must start with the organization ID: {organization_id}"
            )

        # Update anyscale IAM role's assume policy to include the cloud id as the external ID
        role = _get_role(
            AwsRoleArn.from_string(anyscale_iam_role_id).to_role_name(), region
        )
        if role is None:
            self.log.log_resource_error(
                CloudAnalyticsEventCloudResource.AWS_IAM_ROLE,
                CloudSetupError.RESOURCE_NOT_FOUND,
            )
            raise ClickException(f"Failed to access IAM role {anyscale_iam_role_id}.")

        iam_role_original_policy = role.assume_role_policy_document  # type: ignore
        if external_id is None:
            try:
                new_policy = _update_external_ids_for_policy(
                    iam_role_original_policy, cloud_id
                )
                role.AssumeRolePolicy().update(PolicyDocument=json.dumps(new_policy))  # type: ignore
            except ClientError as e:
                self.log.log_resource_exception(
                    CloudAnalyticsEventCloudResource.AWS_IAM_ROLE, e
                )
                raise e
        else:
            fetched_external_ids = [
                statement.setdefault("Condition", {})
                .setdefault("StringEquals", {})
                .setdefault("sts:ExternalId", [])
                for statement in iam_role_original_policy.get("Statement", [])  # type: ignore
            ]
            external_id_in_policy = all(
                external_id == fetched_external_id
                if isinstance(fetched_external_id, str)
                else external_id in fetched_external_id
                for fetched_external_id in fetched_external_ids
            )
            if not external_id_in_policy:
                raise ClickException(
                    f"External ID {external_id} is not in the assume role policy of {anyscale_iam_role_id}."
                )

        return role, iam_role_original_policy

    def _generate_diff(self, existing: Dict[str, Any], new: Dict[str, Any]) -> str:
        """
        Generates a diff between the existing and new dicts.
        """

        diff = difflib.unified_diff(
            yaml.dump(existing).splitlines(keepends=True),
            yaml.dump(new).splitlines(keepends=True),
            lineterm="",
        )

        formatted_diff = ""
        for d in diff:
            if d.startswith("+") and not d.startswith("+++"):
                formatted_diff += "{}{}{}".format(
                    colorama.Fore.GREEN, d, colorama.Style.RESET_ALL
                )
            elif d.startswith("-") and not d.startswith("---"):
                formatted_diff += "{}{}{}".format(
                    colorama.Fore.RED, d, colorama.Style.RESET_ALL
                )
            else:
                formatted_diff += d

        return formatted_diff.strip()

    def _compare_cloud_deployments(
        self,
        deployments: List[CloudDeployment],
        existing_deployments: Dict[str, CloudDeployment],
    ) -> List[CloudDeployment]:
        """
        Compares the new deployments with the existing deployments and returns a list of updated/added deployments.
        """

        deployment_ids = {
            deployment.cloud_deployment_id
            for deployment in deployments
            if deployment.cloud_deployment_id
        }

        if existing_deployments.keys() - deployment_ids:
            raise ClickException("Deleting cloud deployments is not supported.")

        unknown_deployments = deployment_ids - existing_deployments.keys()
        if unknown_deployments:
            raise ClickException(
                f"Cloud deployment(s) {unknown_deployments} do not exist. Do not include a deployment ID when adding a new deployment."
            )

        updated_deployments: List[CloudDeployment] = []
        for d in deployments:
            if d.cloud_deployment_id:
                if d == existing_deployments[d.cloud_deployment_id]:
                    continue
                if d.provider == CloudProviders.PCP:
                    raise ClickException(
                        "Updating machine pool deployments is not supported."
                    )
            else:
                if d.provider == CloudProviders.PCP:
                    raise ClickException(
                        "Please use `anyscale machine-pool attach` to attach a machine pool to a cloud."
                    )
            updated_deployments.append(d)

        return updated_deployments

    def _preprocess_aws(self, cloud_id: str, deployment: CloudDeployment,) -> None:
        if not deployment.aws_config and not deployment.file_storage:
            return

        if not validate_aws_credentials(self.log):
            raise ClickException(
                "Updating cloud deployments requires valid AWS credentials to be set locally. Learn more: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html"
            )

        # Get EFS mount target IP.
        if deployment.file_storage:
            file_storage = FileStorage(**deployment.file_storage)
            assert file_storage.file_storage_id

            try:
                boto3_session = boto3.Session(region_name=deployment.region)
                efs_mount_target_ip = _get_aws_efs_mount_target_ip(
                    boto3_session, file_storage.file_storage_id,
                )
                if not efs_mount_target_ip:
                    raise ClickException(
                        f"EFS mount target IP not found for {file_storage.file_storage_id}."
                    )
                file_storage.mount_targets = [
                    NFSMountTarget(address=efs_mount_target_ip)
                ]
            except ClientError as e:
                self.log.log_resource_exception(
                    CloudAnalyticsEventCloudResource.AWS_EFS, e
                )
                raise e

            deployment.file_storage = file_storage

        if deployment.aws_config:
            aws_config = AWSConfig(**deployment.aws_config)
            assert deployment.region

            # Update Anyscale IAM role's assume policy to include the cloud ID as the external ID.
            self.update_aws_anyscale_iam_role(
                cloud_id,
                deployment.region,
                aws_config.anyscale_iam_role_id,
                aws_config.external_id,
            )
            if aws_config.external_id is None:
                aws_config.external_id = cloud_id

            # Get zones corresponding to subnet IDs.
            if aws_config.subnet_ids:
                subnets_with_azs = associate_aws_subnets_with_azs(
                    aws_config.subnet_ids, deployment.region, self.log
                )
                aws_config.zones = [s.availability_zone for s in subnets_with_azs]

            # Get memorydb config.
            if aws_config.memorydb_cluster_name:
                memorydb_cluster_config = _get_memorydb_cluster_config(
                    aws_config.memorydb_cluster_name, deployment.region, self.log,
                )
                assert memorydb_cluster_config
                aws_config.memorydb_cluster_arn = memorydb_cluster_config.id
                aws_config.memorydb_cluster_endpoint = memorydb_cluster_config.endpoint

            deployment.aws_config = aws_config

    def _preprocess_gcp(
        self, deployment: CloudDeployment,
    ):
        if not deployment.gcp_config:
            return

        gcp_config = GCPConfig(**deployment.gcp_config)
        if not deployment.file_storage and not gcp_config.memorystore_instance_name:
            return

        if not gcp_config.project_id:
            raise ClickException(
                '"project_id" is required to configure filestore or memorystore'
            )

        gcp_utils = try_import_gcp_utils()
        factory = gcp_utils.get_google_cloud_client_factory(
            self.log, gcp_config.project_id
        )

        # Get Filestore mount target IP and root dir.
        if deployment.file_storage:
            fs = FileStorage(**deployment.file_storage)
            if fs.file_storage_id:
                if not gcp_config.vpc_name:
                    raise ClickException(
                        '"vpc_name" is required to configure filestore'
                    )
                filestore_config = gcp_utils.get_gcp_filestore_config_from_full_name(
                    factory, gcp_config.vpc_name, fs.file_storage_id, self.log,
                )
                if not filestore_config:
                    raise ClickException(
                        f"Filestore config not found for {fs.file_storage_id}."
                    )
                fs.mount_path = filestore_config.root_dir
                fs.mount_targets = [
                    NFSMountTarget(address=filestore_config.mount_target_ip)
                ]

                deployment.file_storage = fs

        # Get Memorystore config.
        if gcp_config.memorystore_instance_name:
            memorystore_config = gcp_utils.get_gcp_memorystore_config(
                factory, gcp_config.memorystore_instance_name
            )
            assert memorystore_config
            gcp_config.memorystore_endpoint = memorystore_config.endpoint

            deployment.gcp_config = gcp_config

    def update_cloud_deployments(  # noqa: PLR0912
        self, spec_file: str, yes: bool = False,
    ):
        # Read the spec file.
        path = pathlib.Path(spec_file)
        if not path.exists():
            raise ClickException(f"{spec_file} does not exist.")
        if not path.is_file():
            raise ClickException(f"{spec_file} is not a file.")

        spec = yaml.safe_load(path.read_text())
        if not all(k in spec for k in ["id", "name", "deployments"]):
            raise ClickException(
                "Cloud ID, name, and deployments must be specified in the spec file."
            )

        # Get the existing spec.
        existing_spec = self.get_cloud_deployments(cloud_id=spec["id"],)
        if existing_spec["name"] != spec["name"]:
            raise ClickException("Changing the name of a cloud is not supported.")

        # Diff the existing and new specs
        diff = self._generate_diff(existing_spec, spec)
        if not diff:
            self.log.info("No changes detected.")
            return

        # Get updated/new deployments.
        try:
            deployments = [CloudDeployment(**d) for d in spec["deployments"]]
        except Exception as e:  # noqa: BLE001
            raise ClickException(f"Failed to parse deployments: {e}")

        existing_deployments = {
            deployment["cloud_deployment_id"]: CloudDeployment(**deployment)
            for deployment in existing_spec["deployments"]
        }

        # Figure out which deployments have been updated/added.
        updated_deployments = self._compare_cloud_deployments(
            deployments, existing_deployments,
        )

        # Log the diff and confirm.
        self.log.info(f"Detected the following changes:\n{diff}")

        existing_deployment_ids = {
            d.cloud_deployment_id for d in updated_deployments if d.cloud_deployment_id
        }
        if len(updated_deployments) - len(existing_deployment_ids):
            self.log.info(
                f"{len(updated_deployments) - len(existing_deployment_ids)} new deployment(s) will be added."
            )
        if existing_deployment_ids:
            self.log.info(
                f"{len(existing_deployment_ids)} existing deployment(s) will be updated ({', '.join(existing_deployment_ids)})"
            )

        # Log an additional warning if a new deployment is being added but a deployment with the same AWS/GCP region already exists.
        existing_stack_provider_regions = {
            (d.compute_stack, d.provider, d.region)
            for d in existing_deployments.values()
            if d.provider in (CloudProviders.AWS, CloudProviders.GCP)
        }
        for d in updated_deployments:
            if (
                not d.cloud_deployment_id
                and (d.compute_stack, d.provider, d.region)
                in existing_stack_provider_regions
            ):
                self.log.warning(
                    f"A {d.provider} {d.compute_stack} deployment in region {d.region} already exists."
                )

        confirm("Would you like to proceed with updating this cloud?", yes)

        # Preprocess the deployments if necessary.
        for deployment in updated_deployments:
            if deployment.provider == CloudProviders.AWS:
                self._preprocess_aws(cloud_id=spec["id"], deployment=deployment)
            elif deployment.provider == CloudProviders.GCP:
                self._preprocess_gcp(deployment=deployment)

        # Update the deployments.
        try:
            self.api_client.update_cloud_deployments_api_v2_clouds_cloud_id_deployments_put(
                cloud_id=spec["id"], cloud_deployment=updated_deployments,
            )
        except Exception as e:  # noqa: BLE001
            raise ClickException(f"Failed to update cloud deployments: {e}")

        self.log.info(f"Successfully updated cloud {spec['name']}!")

    def get_cloud_config(
        self, cloud_name: Optional[str] = None, cloud_id: Optional[str] = None,
    ) -> CloudDeploymentConfig:
        """Get a cloud's current JSON configuration."""

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        # In the future we will expose cloud_deployment id as a parameter, for now, it's just a placeholder.
        config: CloudDeploymentConfig = self.api_client.get_cloud_deployment_config_api_v2_clouds_cloud_id_deployment_cloud_deployment_id_config_get(
            cloud_id=cloud_id, cloud_deployment_id="default"
        ).result

        return config

    def update_cloud_config(
        self,
        cloud_name: Optional[str] = None,
        cloud_id: Optional[str] = None,
        enable_log_ingestion: Optional[bool] = None,
        spec_file: Optional[str] = None,
    ):
        """Update a cloud's configuration."""
        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )
        if enable_log_ingestion is not None:
            self._update_customer_aggregated_logs_config(
                cloud_id=cloud_id, is_enabled=enable_log_ingestion,  # type: ignore
            )
            self.log.info(
                f"Successfully updated log ingestion configuration for cloud, "
                f"{cloud_id} to {enable_log_ingestion}"
            )
        elif spec_file is not None:
            path = pathlib.Path(spec_file)
            if not path.exists():
                raise FileNotFoundError(f"File {spec_file} does not exist.")

            if not path.is_file():
                raise ValueError(f"File {spec_file} is not a file.")

            spec = yaml.safe_load(path.read_text())
            config = CloudDeploymentConfig(spec=spec)
            self.api_client.update_cloud_deployment_config_api_v2_clouds_cloud_id_deployment_cloud_deployment_id_config_put(
                cloud_id=cloud_id,
                cloud_deployment_id="default",
                cloud_deployment_config=config,
            )
            self.log.info(
                f"Successfully updated cloud configuration for cloud {cloud_name}"
            )

    def set_default_cloud(
        self, cloud_name: Optional[str], cloud_id: Optional[str],
    ) -> None:
        """
        Sets default cloud for caller's organization. This operation can only be performed
        by organization admins, and the default cloud must have organization level
        permissions.
        """

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        self.api_client.update_default_cloud_api_v2_organizations_update_default_cloud_post(
            cloud_id=cloud_id
        )

        self.log.info(f"Updated default cloud to {cloud_name}")

    def _passed_or_failed_str_from_bool(self, is_passing: bool) -> str:
        return "PASSED" if is_passing else "FAILED"

    @staticmethod
    def _get_cloud_provider_from_str(provider: str) -> CloudProviders:
        if provider.lower() == "aws":
            return CloudProviders.AWS
        elif provider.lower() == "gcp":
            return CloudProviders.GCP
        else:
            raise ClickException(
                f"Unsupported provider {provider}. Supported providers are [aws, gcp]."
            )

    def _validate_functional_verification_args(
        self, functional_verify: Optional[str]
    ) -> List[CloudFunctionalVerificationType]:
        if functional_verify is None:
            return []
        # validate functional_verify
        functions_to_verify = set()
        for function in functional_verify.split(","):
            fn = getattr(CloudFunctionalVerificationType, function.upper(), None)
            if fn is None:
                raise ClickException(
                    f"Unsupported function {function} for --functional-verify. "
                    f"Supported functions: {[function.lower() for function in CloudFunctionalVerificationType]}"
                )
            functions_to_verify.add(fn)
        return list(functions_to_verify)

    def verify_cloud(  # noqa: PLR0911
        self,
        *,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        functional_verify: Optional[str],
        boto3_session: Optional[Any] = None,
        strict: bool = False,
        _use_strict_iam_permissions: bool = False,  # This should only be used in testing.
        yes: bool = False,
    ) -> bool:
        """
        Verifies a cloud by name or id.

        Note: If your changes involve operations that may require additional permissions
        (for example, `boto3_session.client("efs").describe_backup_policy`), it's important
        to run the end-to-end test `bk_e2e/test_cloud.py` locally before pushing the changes.
        This way, you can ensure that your changes will not break the tests.
        """
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result

        if cloud.compute_stack == ComputeStack.K8S:
            self.log.error(
                "The cloud verify command is not supported for Kubernetes clouds."
            )
            return False

        if cloud.state in (CloudState.DELETING, CloudState.DELETED):
            self.log.info(
                f"This cloud {cloud_name}({cloud_id}) is either during deletion or deleted. Skipping verification."
            )
            return False

        cloud_resource = get_cloud_resource_by_cloud_id(
            cloud_id, cloud.provider, self.api_client
        )
        if cloud_resource is None:
            self.log.error(
                f"This cloud {cloud_name}({cloud_id}) does not contain resource records. Please delete this cloud and create a new one."
            )
            return False

        self.cloud_event_producer.init_trace_context(
            CloudAnalyticsEventCommandName.VERIFY,
            cloud_provider=cloud.provider,
            cloud_id=cloud_id,
        )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.COMMAND_START, succeeded=True
        )

        if cloud.provider == "AWS":
            if boto3_session is None:
                boto3_session = boto3.Session(region_name=cloud.region)
            if not self.verify_aws_cloud_resources(
                cloud_resource=cloud_resource,
                boto3_session=boto3_session,
                region=cloud.region,
                cloud_id=cloud_id,  # type: ignore
                is_bring_your_own_resource=cloud.is_bring_your_own_resource,
                is_private_network=cloud.is_private_cloud
                if cloud.is_private_cloud
                else False,
                strict=strict,
                _use_strict_iam_permissions=_use_strict_iam_permissions,
            ):
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_VERIFIED,
                    succeeded=False,
                    logger=self.log,
                )
                return False
        elif cloud.provider == "GCP":
            credentials_dict = json.loads(cloud.credentials)
            project_id = credentials_dict["project_id"]
            host_project_id = credentials_dict.get("host_project_id")
            if not self.verify_gcp_cloud_resources(
                cloud_resource=cloud_resource,
                project_id=project_id,
                host_project_id=host_project_id,
                region=cloud.region,
                cloud_id=cloud_id,  # type: ignore
                yes=False,
                strict=strict,
                is_private_service_cloud=cloud.is_private_service_cloud,
            ):
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_VERIFIED,
                    succeeded=False,
                    logger=self.log,
                )
                return False
        else:
            self.log.error(
                f"This cloud {cloud_name}({cloud_id}) does not have a valid cloud provider."
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.RESOURCES_VERIFIED,
                succeeded=False,
                internal_error="invalid cloud provider",
            )
            return False

        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.RESOURCES_VERIFIED, succeeded=True
        )

        if len(functions_to_verify) == 0:
            return True

        return CloudFunctionalVerificationController(
            self.cloud_event_producer, self.log
        ).start_verification(cloud_id, cloud.provider, functions_to_verify, yes=yes)

    def verify_aws_cloud_resources(
        self,
        *,
        cloud_resource: CreateCloudResource,
        boto3_session: boto3.Session,
        region: str,
        is_private_network: bool,
        cloud_id: str,
        is_bring_your_own_resource: bool = False,
        ignore_capacity_errors: bool = IGNORE_CAPACITY_ERRORS,
        logger: CloudSetupLogger = None,
        strict: bool = False,
        _use_strict_iam_permissions: bool = False,  # This should only be used in testing.
    ):
        if not logger:
            logger = self.log

        verify_aws_vpc_result = verify_aws_vpc(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            logger=logger,
            ignore_capacity_errors=ignore_capacity_errors,
            strict=strict,
        )
        verify_aws_subnets_result = verify_aws_subnets(
            cloud_resource=cloud_resource,
            region=region,
            logger=logger,
            ignore_capacity_errors=ignore_capacity_errors,
            is_private_network=is_private_network,
            strict=strict,
        )

        anyscale_aws_account = (
            self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
        )
        verify_aws_iam_roles_result = verify_aws_iam_roles(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            anyscale_aws_account=anyscale_aws_account,
            logger=logger,
            strict=strict,
            cloud_id=cloud_id,
            _use_strict_iam_permissions=_use_strict_iam_permissions,
        )
        verify_aws_security_groups_result = verify_aws_security_groups(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            logger=logger,
            strict=strict,
        )
        verify_aws_s3_result = verify_aws_s3(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            region=region,
            logger=logger,
            strict=strict,
        )
        verify_aws_efs_result = True
        if cloud_resource.aws_efs_id:
            verify_aws_efs_result = verify_aws_efs(
                cloud_resource=cloud_resource,
                boto3_session=boto3_session,
                logger=logger,
                strict=strict,
            )
        # Cloudformation is only used in managed cloud setup. Set to True in BYOR case because it's not used.
        verify_aws_cloudformation_stack_result = True
        if not is_bring_your_own_resource:
            verify_aws_cloudformation_stack_result = verify_aws_cloudformation_stack(
                cloud_resource=cloud_resource,
                boto3_session=boto3_session,
                logger=logger,
                strict=strict,
            )
        if cloud_resource.memorydb_cluster_config is not None:
            verify_aws_memorydb_cluster_result = verify_aws_memorydb_cluster(
                cloud_resource=cloud_resource,
                boto3_session=boto3_session,
                logger=logger,
                strict=strict,
            )

        verify_anyscale_access_result = verify_anyscale_access(
            self.api_client, cloud_id, CloudProviders.AWS, logger
        )

        verification_result_summary = [
            "Verification result:",
            f"anyscale access: {self._passed_or_failed_str_from_bool(verify_anyscale_access_result)}",
            f"vpc: {self._passed_or_failed_str_from_bool(verify_aws_vpc_result)}",
            f"subnets: {self._passed_or_failed_str_from_bool(verify_aws_subnets_result)}",
            f"iam roles: {self._passed_or_failed_str_from_bool(verify_aws_iam_roles_result)}",
            f"security groups: {self._passed_or_failed_str_from_bool(verify_aws_security_groups_result)}",
            f"s3: {self._passed_or_failed_str_from_bool(verify_aws_s3_result)}",
            f"cloudformation stack: {self._passed_or_failed_str_from_bool(verify_aws_cloudformation_stack_result) if not is_bring_your_own_resource else 'N/A'}",
        ]
        if cloud_resource.aws_efs_id:
            verification_result_summary.append(
                f"efs: {self._passed_or_failed_str_from_bool(verify_aws_efs_result)}"
            )
        if cloud_resource.memorydb_cluster_config is not None:
            verification_result_summary.append(
                f"memorydb cluster: {self._passed_or_failed_str_from_bool(verify_aws_memorydb_cluster_result)}"
            )

        logger.info("\n".join(verification_result_summary))

        self.verify_aws_cloud_quotas(region=region, boto3_session=boto3_session)

        return all(
            [
                verify_anyscale_access_result,
                verify_aws_vpc_result,
                verify_aws_subnets_result,
                verify_aws_iam_roles_result,
                verify_aws_security_groups_result,
                verify_aws_s3_result,
                verify_aws_efs_result,
                verify_aws_cloudformation_stack_result
                if not is_bring_your_own_resource
                else True,
            ]
        )

    def verify_aws_cloud_quotas(
        self, *, region: str, boto3_session: Optional[Any] = None
    ):
        """
        Checks the AWS EC2 instance quotas and warns users if they are not good enough
        to support LLM workloads
        """
        if boto3_session is None:
            boto3_session = boto3.Session(region_name=region)

        QUOTAS_CONFIG = {
            "L-3819A6DF": {
                "description": "All G and VT Spot Instance Requests",
                "min": 512,
            },
            "L-34B43A08": {
                "description": "All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests",
                "min": 512,
            },
            "L-7212CCBC": {
                "description": "All P4, P3 and P2 Spot Instance Requests",
                "min": 224,
            },
            "L-DB2E81BA": {
                "description": "Running On-Demand G and VT instances",
                "min": 512,
            },
            "L-1216C47A": {
                "description": "Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances",
                "min": 544,
            },
            "L-417A185B": {"description": "Running On-Demand P instances", "min": 224,},
        }

        quota_client = boto3_session.client("service-quotas", region_name=region)

        self.log.info("Checking quota values...")
        # List of tuples of quota code, current quota value
        invalid_quotas = []
        for quota_code, config in QUOTAS_CONFIG.items():
            quota = quota_client.get_service_quota(
                ServiceCode="ec2", QuotaCode=quota_code
            )
            if quota["Quota"]["Value"] < config["min"]:
                invalid_quotas.append((quota_code, quota["Quota"]["Value"]))

        if len(invalid_quotas):
            quota_errors = [
                f"- \"{QUOTAS_CONFIG[quota_code]['description']}\" should be at least {QUOTAS_CONFIG[quota_code]['min']} (curr: {value})"
                for quota_code, value in invalid_quotas
            ]
            quota_error_str = "\n".join(quota_errors)
            self.log.warning(
                "Your AWS account does not have enough quota to support LLM workloads. "
                "Please request quota increases for the following quotas:\n"
                f"{quota_error_str}\n\nFor instructions on how to increase quotas, visit this link: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html#request-increase"
            )

    def register_azure_or_generic_cloud(  # noqa: PLR0913
        self,
        name: str,
        provider: str,
        auto_add_user: bool = False,
        # Optional cloud-resource-scoped parameters.
        # Some of these are conditionally required.
        region: Optional[str] = "default",
        cloud_storage_bucket_name: Optional[str] = None,
        cloud_storage_bucket_endpoint: Optional[str] = None,
        cloud_storage_bucket_region: Optional[str] = None,
        nfs_mount_targets: Optional[List[str]] = None,
        nfs_mount_path: Optional[str] = None,
        kubernetes_zones: Optional[List[str]] = None,
    ) -> None:
        cloud_provider = (
            CloudProviders.AZURE if provider == "azure" else CloudProviders.GENERIC
        )
        self.cloud_event_producer.init_trace_context(
            CloudAnalyticsEventCommandName.REGISTER, cloud_provider,
        )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.COMMAND_START, succeeded=True
        )

        # Handle parsing / conversion of nfs_mount_targets.
        mount_targets: List[NFSMountTarget] = []
        for target in nfs_mount_targets or []:
            parts = [part.strip() for part in target.split(",")]
            if len(parts) == 1:
                mount_targets.append(NFSMountTarget(address=parts[0]))
            elif len(parts) == 2:
                mount_targets.append(NFSMountTarget(address=parts[1], zone=parts[0]))
            else:
                raise ClickException(
                    f"Invalid mount target {target}; expected (zone,address) tuple or a singular address."
                )

        # Handle defaulting of region.
        if not region:
            region = "default"

        # Attempt to create the cloud.
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    name=name,
                    region=region,
                    provider=cloud_provider,
                    is_bring_your_own_resource=True,
                    cluster_management_stack_version=ClusterManagementStackVersions.V2,
                    auto_add_user=auto_add_user,
                    credentials="",
                )
            )
            cloud_id = created_cloud.result.id
            self.cloud_event_producer.set_cloud_id(cloud_id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED, succeeded=True
            )
        except ClickException as e:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED,
                succeeded=False,
                internal_error=str(e),
            )
            raise

        # Attempt to create the cloud resource.
        try:
            with self.log.spinner("Registering Anyscale cloud resources..."):
                cloud_resource = self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
                    cloud_id=cloud_id,
                    update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                        cloud_resource_to_update=CreateCloudResource(
                            compute_stack=ComputeStack.K8S,
                            kubernetes_zones=kubernetes_zones,
                            cloud_storage_bucket_name=cloud_storage_bucket_name,
                            cloud_storage_bucket_endpoint=cloud_storage_bucket_endpoint,
                            cloud_storage_bucket_region=cloud_storage_bucket_region
                            or region,
                            nfs_mount_targets=mount_targets,
                            nfs_mount_path=nfs_mount_path,
                        ),
                    ),
                )

            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE, succeeded=True
            )

        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE,
                succeeded=False,
                internal_error=str(e),
            )

            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            raise ClickException(f"Cloud registration failed! {e}")

        # TODO (shomilj): Fetch & optionally run the Helm installation here.
        cloud_resource_id = cloud_resource.result.cloud_resource.id
        self.log.info(
            f"Cloud registration complete! When installing this cloud's Kubernetes Manager, use cloud deployment ID '{cloud_resource_id}'."
        )

    def register_aws_cloud(  # noqa: PLR0913, PLR0912, C901
        self,
        *,
        region: str,
        name: str,
        vpc_id: str,
        subnet_ids: List[str],
        efs_id: Optional[str],
        anyscale_iam_role_id: str,
        instance_iam_role_id: str,
        security_group_ids: List[str],
        cloud_storage_bucket_name: str,
        memorydb_cluster_id: Optional[str],
        functional_verify: Optional[str],
        private_network: bool,
        cluster_management_stack_version: ClusterManagementStackVersions,
        yes: bool = False,
        skip_verifications: bool = False,
        auto_add_user: bool = False,
        external_id: Optional[str] = None,
        # Default to ComputeStack.VM for backwards compatibility
        # for SDK users who do not specify a compute stack here.
        compute_stack: ComputeStack = ComputeStack.VM,
        kubernetes_zones: Optional[List[str]] = None,
        anyscale_operator_iam_identity: Optional[str] = None,
    ):
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        if not validate_aws_credentials(self.log):
            raise ClickException(
                "Cloud registration requires valid AWS credentials to be set locally. Learn more: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html"
            )

        # We accept both the full ARN and the bucket name as input
        # but we unify it to the bucket name here
        if cloud_storage_bucket_name.startswith(S3_ARN_PREFIX):
            cloud_storage_bucket_name = cloud_storage_bucket_name[len(S3_ARN_PREFIX) :]
        if not cloud_storage_bucket_name.startswith(S3_STORAGE_PREFIX):
            cloud_storage_bucket_name = S3_STORAGE_PREFIX + cloud_storage_bucket_name

        self.cloud_event_producer.init_trace_context(
            CloudAnalyticsEventCommandName.REGISTER, CloudProviders.AWS
        )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.COMMAND_START, succeeded=True
        )

        credentials = anyscale_iam_role_id
        if compute_stack == ComputeStack.K8S:
            # On K8S, we don't need to collect credentials;
            # instead, write a random value into this field
            # to maintain the property that each cloud's
            # credentials are unique.
            credentials = uuid.uuid4().hex

        # Create a cloud without cloud resources first
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="AWS",
                    region=region,
                    credentials=credentials,
                    name=name,
                    is_bring_your_own_resource=True,
                    is_private_cloud=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                    auto_add_user=auto_add_user,
                    external_id=external_id,
                )
            )
            cloud_id = created_cloud.result.id
            self.cloud_event_producer.set_cloud_id(cloud_id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED, succeeded=True
            )
        except ClickException as e:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED,
                succeeded=False,
                internal_error=str(e),
            )
            raise

        try:
            # The Anyscale IAM role is optional for the K8s stack.
            has_anyscale_iam_role = compute_stack == ComputeStack.VM or (
                compute_stack == ComputeStack.K8S and anyscale_iam_role_id
            )

            iam_role_original_policy = None
            if has_anyscale_iam_role:
                # Update anyscale IAM role's assume policy to include the cloud id as the external ID
                role, iam_role_original_policy = self.update_aws_anyscale_iam_role(
                    cloud_id=cloud_id,
                    region=region,
                    anyscale_iam_role_id=anyscale_iam_role_id,
                    external_id=external_id,
                )

            # When running on the VM compute stack, validate and retrieve the EFS mount target IP.
            # When running on the K8S compute stack, EFS is optional; if efs_id is provided, then
            # validate and retrieve the EFS mount target IP.
            if efs_id:
                try:
                    boto3_session = boto3.Session(region_name=region)
                    aws_efs_mount_target_ip = _get_aws_efs_mount_target_ip(
                        boto3_session, efs_id
                    )
                except ClientError as e:
                    self.log.log_resource_exception(
                        CloudAnalyticsEventCloudResource.AWS_EFS, e
                    )
                    raise e
            else:
                boto3_session = None
                aws_efs_mount_target_ip = None

            # When running on the VM compute stack, associate the AWS subnets with their availability zones.
            if compute_stack == ComputeStack.VM:
                aws_subnet_ids_with_availability_zones = associate_aws_subnets_with_azs(
                    subnet_ids, region, self.log
                )
            else:
                aws_subnet_ids_with_availability_zones = None

            # If memorydb cluster is provided, get the memorydb cluster config.
            if memorydb_cluster_id is not None:
                memorydb_cluster_config = _get_memorydb_cluster_config(
                    memorydb_cluster_id, region, self.log
                )
            else:
                memorydb_cluster_config = None

            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE, succeeded=True
            )
        except Exception as e:  # noqa: BLE001
            error = str(e)
            self.log.error(error)
            error_msg_for_event = str(e)
            if isinstance(e, NoCredentialsError):
                # If it is a credentials error, rewrite the error to be more clear
                error = "Unable to locate AWS credentials. Cloud registration requires valid AWS credentials to be set locally. Learn more: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html"
                error_msg_for_event = "Unable to locate AWS credentials."
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                succeeded=False,
                logger=self.log,
                internal_error=error_msg_for_event,
            )
            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            try:
                if iam_role_original_policy is not None and external_id is None:
                    # Revert the assume policy back to the original policy
                    role.AssumeRolePolicy().update(  # type: ignore
                        PolicyDocument=json.dumps(iam_role_original_policy)
                    )
            except Exception as revert_error:  # noqa: BLE001
                raise ClickException(
                    f"Cloud registration failed! {error}. Failed to revert the trust policy back to the original policy. {revert_error}"
                )
            raise ClickException(f"Cloud registration failed! {error}")

        aws_iam_role_arns = None
        if compute_stack == ComputeStack.VM:
            aws_iam_role_arns = [anyscale_iam_role_id, instance_iam_role_id]
        elif compute_stack == ComputeStack.K8S and anyscale_iam_role_id:
            aws_iam_role_arns = [anyscale_iam_role_id]

        try:
            # Verify cloud resources meet our requirement
            create_cloud_resource = CreateCloudResource(
                aws_vpc_id=vpc_id,
                aws_subnet_ids_with_availability_zones=aws_subnet_ids_with_availability_zones,
                aws_iam_role_arns=aws_iam_role_arns,
                aws_security_groups=security_group_ids,
                aws_s3_id=cloud_storage_bucket_name[len(S3_STORAGE_PREFIX) :],
                aws_efs_id=efs_id,
                aws_efs_mount_target_ip=aws_efs_mount_target_ip,
                memorydb_cluster_config=memorydb_cluster_config,
                compute_stack=compute_stack,
                kubernetes_zones=kubernetes_zones,
                kubernetes_dataplane_identity=anyscale_operator_iam_identity,
                cloud_storage_bucket_name=cloud_storage_bucket_name,
            )

            # Verification is only performed for VM compute stack.
            # TODO (shomilj): Add verification to the K8S compute stack as well.
            if compute_stack == ComputeStack.VM:
                with self.log.spinner("Verifying cloud resources...") as spinner:
                    if boto3_session is None:
                        boto3_session = boto3.Session(region_name=region)
                    if not skip_verifications and not self.verify_aws_cloud_resources(
                        cloud_resource=create_cloud_resource,
                        boto3_session=boto3_session,
                        region=region,
                        is_bring_your_own_resource=True,
                        is_private_network=private_network,
                        cloud_id=cloud_id,
                        logger=CloudSetupLogger(spinner_manager=spinner),
                    ):
                        raise ClickException(
                            "Please make sure all the resources provided meet the requirements and try again."
                        )

                confirm(
                    "Please review the output from verification for any warnings. Would you like to proceed with cloud creation?",
                    yes,
                )
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_VERIFIED, succeeded=True
                )
        # Since the verify runs for a while, it's possible the user aborts the process, which throws a KeyboardInterrupt.
        except (Exception, KeyboardInterrupt) as e:  # noqa: BLE001
            self.log.error(str(e))
            internal_error = str(e)
            if isinstance(e, Abort):
                internal_error = "User aborted."
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.RESOURCES_VERIFIED,
                succeeded=False,
                logger=self.log,
                internal_error=internal_error,
            )
            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            try:
                if iam_role_original_policy is not None and external_id is None:
                    # Revert the assume policy back to the original policy
                    role.AssumeRolePolicy().update(  # type: ignore
                        PolicyDocument=json.dumps(iam_role_original_policy)
                    )
            except Exception as revert_error:  # noqa: BLE001
                raise ClickException(
                    f"Cloud registration failed! {e}. Failed to revert the trust policy back to the original policy. {revert_error}"
                )

            raise ClickException(f"Cloud registration failed! {e}")

        try:
            with self.log.spinner(
                "Updating Anyscale cloud with cloud resource..."
            ) as spinner:
                # update cloud with verified cloud resources
                cloud_resource = self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
                    cloud_id=cloud_id,
                    update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                        cloud_resource_to_update=create_cloud_resource,
                    ),
                )
            # For now, only wait for the cloud to be active if the compute stack is VM.
            # TODO (shomilj): support this fully for Kubernetes after provider metadata
            # checks are removed.
            if compute_stack == ComputeStack.VM:
                self.wait_for_cloud_to_be_active(cloud_id, CloudProviders.AWS)
            if compute_stack == ComputeStack.K8S:
                cloud_resource_id = cloud_resource.result.cloud_resource.id
                self.log.info(
                    f"For registering this cloud's Kubernetes Manager, use cloud deployment ID '{cloud_resource_id}'."
                )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE, succeeded=True
            )
        # Since the update runs for a while, it's possible the user aborts the process, which throws a KeyboardInterrupt.
        except (Exception, KeyboardInterrupt) as e:  # noqa: BLE001
            # Delete the cloud if registering the cloud fails
            self.log.error(str(e))
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE,
                succeeded=False,
                internal_error=str(e),
            )
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            try:
                if iam_role_original_policy is not None and external_id is None:
                    # Revert the assume policy back to the original policy
                    role.AssumeRolePolicy().update(  # type: ignore
                        PolicyDocument=json.dumps(iam_role_original_policy)
                    )
            except Exception as revert_error:  # noqa: BLE001
                raise ClickException(
                    f"Cloud registration failed! {e}. Failed to revert the trust policy back to the original policy. {revert_error}"
                )

            raise ClickException(f"Cloud registration failed! {e}")

        self.log.info(f"Successfully created cloud {name}, and it's ready to use.")

        if len(functions_to_verify) > 0:
            CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(cloud_id, CloudProviders.AWS, functions_to_verify, yes)

    def verify_gcp_cloud_resources(
        self,
        *,
        cloud_resource: CreateCloudResourceGCP,
        project_id: str,
        region: str,
        cloud_id: str,
        yes: bool,
        host_project_id: Optional[str] = None,
        factory: Any = None,
        strict: bool = False,
        is_private_service_cloud: bool = False,
    ) -> bool:
        gcp_utils = try_import_gcp_utils()
        if not factory:
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
        GCPLogger = gcp_utils.GCPLogger
        verify_lib = try_import_gcp_verify_lib()

        network_project_id = host_project_id if host_project_id else project_id
        use_shared_vpc = bool(host_project_id)

        with self.log.spinner("Verifying cloud resources...") as spinner:
            gcp_logger = GCPLogger(self.log, project_id, spinner, yes)
            verify_gcp_project_result = verify_lib.verify_gcp_project(
                factory, cloud_resource, project_id, gcp_logger, strict=strict
            )
            verify_gcp_access_service_account_result = verify_lib.verify_gcp_access_service_account(
                factory, cloud_resource, project_id, gcp_logger
            )
            verify_gcp_dataplane_service_account_result = verify_lib.verify_gcp_dataplane_service_account(
                factory, cloud_resource, project_id, gcp_logger, strict=strict
            )
            verify_gcp_networking_result = verify_lib.verify_gcp_networking(
                factory,
                cloud_resource,
                network_project_id,
                region,
                gcp_logger,
                strict=strict,
                is_private_service_cloud=is_private_service_cloud,
            )
            verify_firewall_policy_result = verify_lib.verify_firewall_policy(
                factory,
                cloud_resource,
                network_project_id,
                region,
                use_shared_vpc,
                is_private_service_cloud,
                gcp_logger,
                strict=strict,
            )
            verify_cloud_storage_result = verify_lib.verify_cloud_storage(
                factory, cloud_resource, project_id, region, gcp_logger, strict=strict,
            )
            verify_anyscale_access_result = verify_anyscale_access(
                self.api_client, cloud_id, CloudProviders.GCP, self.log
            )
            verify_filestore_result = True
            if cloud_resource.gcp_filestore_config.instance_name:
                verify_filestore_result = verify_lib.verify_filestore(
                    factory, cloud_resource, region, gcp_logger, strict=strict
                )
            verify_memorystore_result = True
            if cloud_resource.memorystore_instance_config is not None:
                verify_memorystore_result = verify_lib.verify_memorystore(
                    factory, cloud_resource, gcp_logger, strict=strict,
                )

        verification_results = [
            "Verification result:",
            f"anyscale access: {self._passed_or_failed_str_from_bool(verify_anyscale_access_result)}",
            f"project: {self._passed_or_failed_str_from_bool(verify_gcp_project_result)}",
            f"vpc and subnet: {self._passed_or_failed_str_from_bool(verify_gcp_networking_result)}",
            f"anyscale iam service account: {self._passed_or_failed_str_from_bool(verify_gcp_access_service_account_result)}",
            f"cluster node service account: {self._passed_or_failed_str_from_bool(verify_gcp_dataplane_service_account_result)}",
            f"firewall policy: {self._passed_or_failed_str_from_bool(verify_firewall_policy_result)}",
            f"cloud storage: {self._passed_or_failed_str_from_bool(verify_cloud_storage_result)}",
        ]

        if cloud_resource.gcp_filestore_config.instance_name:
            verification_results.append(
                f"filestore: {self._passed_or_failed_str_from_bool(verify_filestore_result)}"
            )
        if cloud_resource.memorystore_instance_config is not None:
            verification_results.append(
                f"memorystore: {self._passed_or_failed_str_from_bool(verify_memorystore_result)}"
            )

        self.log.info("\n".join(verification_results))

        return all(
            [
                verify_anyscale_access_result,
                verify_gcp_project_result,
                verify_gcp_access_service_account_result,
                verify_gcp_dataplane_service_account_result,
                verify_gcp_networking_result,
                verify_firewall_policy_result,
                verify_filestore_result,
                verify_cloud_storage_result,
                verify_memorystore_result,
            ]
        )

    def register_gcp_cloud(  # noqa: PLR0913, PLR0912, C901
        self,
        *,
        region: str,
        name: str,
        project_id: str,
        vpc_name: str,
        subnet_names: List[str],
        filestore_instance_id: str,
        filestore_location: str,
        anyscale_service_account_email: str,
        instance_service_account_email: str,
        provider_id: str,
        firewall_policy_names: List[str],
        cloud_storage_bucket_name: str,
        memorystore_instance_name: Optional[str],
        functional_verify: Optional[str],
        private_network: bool,
        cluster_management_stack_version: ClusterManagementStackVersions,
        host_project_id: Optional[str] = None,
        yes: bool = False,
        skip_verifications: bool = False,
        auto_add_user: bool = False,
        # Default to ComputeStack.VM for backwards compatibility
        # for SDK users who do not specify a compute stack here.
        compute_stack: ComputeStack = ComputeStack.VM,
        kubernetes_zones: Optional[List[str]] = None,
        anyscale_operator_iam_identity: Optional[str] = None,
    ):
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        gcp_utils = try_import_gcp_utils()

        # Create a cloud without cloud resources first
        # Provider ID is optional for K8s clouds.
        if compute_stack != ComputeStack.K8S:
            provider_id_re_result = re.search(
                "projects\\/[0-9]*\\/locations\\/global\\/workloadIdentityPools\\/.+\\/providers\\/[a-z0-9-]*$",
                provider_id,
            )
            if provider_id_re_result is None:
                raise ClickException(
                    f"Invalid provider_id {provider_id}. Only lowercase letters, numbers, and dashes are allowed."
                )

        self.cloud_event_producer.init_trace_context(
            CloudAnalyticsEventCommandName.REGISTER, CloudProviders.GCP
        )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.COMMAND_START, succeeded=True
        )

        try:
            credentials_dict = {
                "project_id": project_id or "",
                "provider_id": provider_id or "",
                "service_account_email": anyscale_service_account_email or "",
            }
            if host_project_id:
                credentials_dict["host_project_id"] = host_project_id
            credentials = json.dumps(credentials_dict)

            if compute_stack == ComputeStack.K8S:
                # On K8S, we don't need to collect credentials;
                # instead, write a random trace_id into this field
                # to maintain the property that each cloud's
                # credentials are unique.
                random_id = uuid.uuid4().hex
                credentials = json.dumps(
                    {
                        "provider_id": "",
                        "project_id": random_id,
                        "service_account_email": random_id,
                    }
                )

            # NOTE: For now we set the is_private_service_cloud to be the same as is_private_cloud
            # We don't expose this to the user yet since it's not recommended.
            is_private_service_cloud = private_network

            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="GCP",
                    region=region,
                    credentials=credentials,
                    name=name,
                    is_bring_your_own_resource=True,
                    is_private_cloud=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                    is_private_service_cloud=is_private_service_cloud,
                    auto_add_user=auto_add_user,
                )
            )
            cloud_id = created_cloud.result.id
            self.cloud_event_producer.set_cloud_id(cloud_id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED, succeeded=True
            )
        except ClickException as e:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED,
                succeeded=False,
                internal_error=str(e),
            )
            raise

        try:
            # Set defaults for Kubernetes clouds.
            if compute_stack == ComputeStack.K8S:
                instance_service_account_email = ""
                subnet_names = []

            enable_filestore = filestore_location and filestore_instance_id

            # Normally, for Kubernetes clouds, we don't need a VPC name, since networking is managed by Kubernetes.
            # For Kubernetes clouds on GCP where Filestore is enabled, we require the VPC name, since it is needed
            # to look up the relevant Mount Target IP for Filestore in the VPC.
            if compute_stack == ComputeStack.K8S:
                if enable_filestore and not vpc_name:
                    raise ClickException(
                        "Please provide the name of the VPC that your Kubernetes cluster is running inside of."
                    )
                if (enable_filestore or memorystore_instance_name) and not project_id:
                    raise ClickException("Please provide a project ID.")

            if project_id:
                factory = gcp_utils.get_google_cloud_client_factory(
                    self.log, project_id
                )

            if enable_filestore:
                filestore_config = gcp_utils.get_gcp_filestore_config(
                    factory,
                    project_id,
                    vpc_name,
                    filestore_location,
                    filestore_instance_id,
                    self.log,
                )
            else:
                filestore_config = GCPFileStoreConfig(
                    instance_name="", mount_target_ip="", root_dir=""
                )
                if compute_stack == ComputeStack.K8S:
                    # Set vpc_name to empty string for Kubernetes clouds
                    vpc_name = ""

            if memorystore_instance_name:
                memorystore_instance_config = gcp_utils.get_gcp_memorystore_config(
                    factory, memorystore_instance_name
                )
            else:
                memorystore_instance_config = None

            if not cloud_storage_bucket_name.startswith(GCS_STORAGE_PREFIX):
                cloud_storage_bucket_name = (
                    GCS_STORAGE_PREFIX + cloud_storage_bucket_name
                )

            # Verify cloud resources meet our requirement
            create_cloud_resource_gcp = CreateCloudResourceGCP(
                gcp_vpc_id=vpc_name,
                gcp_subnet_ids=subnet_names,
                gcp_cluster_node_service_account_email=instance_service_account_email,
                gcp_anyscale_iam_service_account_email=anyscale_service_account_email
                or "",
                gcp_filestore_config=filestore_config,
                gcp_firewall_policy_ids=firewall_policy_names,
                gcp_cloud_storage_bucket_id=cloud_storage_bucket_name[
                    len(GCS_STORAGE_PREFIX) :
                ],
                memorystore_instance_config=memorystore_instance_config,
                compute_stack=compute_stack,
                kubernetes_zones=kubernetes_zones,
                kubernetes_dataplane_identity=anyscale_operator_iam_identity,
                cloud_storage_bucket_name=cloud_storage_bucket_name,
            )

            # Verification is only performed for VM compute stack.
            # TODO (shomilj): Add verification to the K8S compute stack as well.
            if compute_stack == ComputeStack.VM:
                if not skip_verifications and not self.verify_gcp_cloud_resources(
                    cloud_resource=create_cloud_resource_gcp,
                    project_id=project_id,
                    host_project_id=host_project_id,
                    region=region,
                    cloud_id=cloud_id,
                    yes=yes,
                    factory=factory,
                    is_private_service_cloud=is_private_service_cloud,
                ):
                    raise ClickException(
                        "Please make sure all the resources provided meet the requirements and try again."
                    )

                confirm(
                    "Please review the output from verification for any warnings. Would you like to proceed with cloud creation?",
                    yes,
                )
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_VERIFIED, succeeded=True
                )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            internal_error = str(e)
            if isinstance(e, Abort):
                internal_error = "User aborted."
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.RESOURCES_VERIFIED,
                succeeded=False,
                logger=self.log,
                internal_error=internal_error,
            )

            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            raise ClickException(f"Cloud registration failed! {e}")

        try:
            # update cloud with verified cloud resources
            with self.log.spinner("Updating Anyscale cloud with cloud resources..."):
                cloud_resource = self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put(
                    cloud_id=cloud_id,
                    update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                        cloud_resource_to_update=create_cloud_resource_gcp,
                    ),
                )
            # For now, only wait for the cloud to be active if the compute stack is VM.
            # TODO (shomilj): support this fully for Kubernetes after provider metadata
            # checks are removed.
            if compute_stack == ComputeStack.VM:
                self.wait_for_cloud_to_be_active(cloud_id, CloudProviders.GCP)
            if compute_stack == ComputeStack.K8S:
                cloud_resource_id = cloud_resource.result.cloud_resource.id
                self.log.info(
                    f"For registering this cloud's Kubernetes Manager, use cloud deployment ID '{cloud_resource_id}'."
                )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE, succeeded=True
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE,
                succeeded=False,
                internal_error=str(e),
            )
            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            raise ClickException(f"Cloud registration failed! {e}")

        self.log.info(f"Successfully created cloud {name}, and it's ready to use.")

        if len(functions_to_verify) > 0:
            CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(cloud_id, CloudProviders.GCP, functions_to_verify, yes)

    def delete_cloud(  # noqa: PLR0912, C901
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        skip_confirmation: bool,
    ) -> bool:
        """
        Deletes a cloud by name or id.
        TODO Delete all GCE resources on cloud delete
        Including: Anyscale maanged resources, ALB resources, and TLS certs
        """
        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        # get cloud
        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(
            cloud_id=cloud_id
        ).result

        cloud_provider = cloud.provider
        assert cloud_provider in (
            CloudProviders.AWS,
            CloudProviders.GCP,
            CloudProviders.AZURE,
            CloudProviders.GENERIC,
        ), f"Cloud provider {cloud_provider} not supported yet"

        cloud_resource = get_cloud_resource_by_cloud_id(
            cloud_id, cloud.provider, self.api_client
        )
        if cloud_resource is None:
            # no cloud resource found, directly delete the cloud
            try:
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
            except ClickException as e:
                self.log.error(e)
                raise ClickException(f"Failed to delete cloud with name {cloud_name}.")

            self.log.info(f"Deleted cloud with name {cloud_name}.")
            return True

        confirmation_msg = f"\nIf the cloud {cloud_id} is deleted, you will not be able to access existing clusters of this cloud.\n"
        if cloud.is_bring_your_own_resource:
            confirmation_msg += "Note that Anyscale does not delete any of the cloud provider resources created by you.\n"

        confirmation_msg += "For more information, refer to the documentation "
        if cloud_provider == CloudProviders.AWS:
            confirmation_msg += "https://docs.anyscale.com/administration/cloud-deployment/manage-aws-cloud#delete-an-anyscale-cloud\n"
        elif cloud_provider == CloudProviders.GCP:
            confirmation_msg += "https://docs.anyscale.com/administration/cloud-deployment/manage-gcp-cloud#delete-an-anyscale-cloud\n"

        confirmation_msg += "Continue?"
        confirm(confirmation_msg, skip_confirmation)

        # set cloud state to DELETING
        try:
            if cloud_provider in (
                CloudProviders.AWS,
                CloudProviders.AZURE,
                CloudProviders.GENERIC,
            ):
                with self.log.spinner("Preparing to delete Anyscale cloud..."):
                    response = self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
                        cloud_id=cloud_id,
                        update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                            state=CloudState.DELETING
                        ),
                    )
            elif cloud_provider == CloudProviders.GCP:
                with self.log.spinner("Preparing to delete Anyscale cloud..."):
                    response = self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put(
                        cloud_id=cloud_id,
                        update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                            state=CloudState.DELETING
                        ),
                    )

            cloud = response.result
        except ClickException as e:
            raise ClickException(
                f"Failed to update cloud state to deleting for cloud {cloud_name}: {e}"
            )

        # Clean up cloud resources
        try:
            if cloud_provider == CloudProviders.AWS:
                self.delete_all_aws_resources(cloud)
            elif cloud_provider == CloudProviders.GCP:
                with self.log.spinner("Deleting load balancing resources..."):
                    wait_for_gcp_lb_resource_termination(
                        api_client=self.api_client, cloud_id=cloud_id
                    )
                self.delete_all_gcp_resources(cloud)
        except Exception as e:  # noqa: BLE001
            confirm(
                f"Error while trying to clean up {cloud_provider} resources:\n{e}\n"
                f"Please check your {cloud_provider} account for relevant errors.\n"
                "Do you want to force delete this cloud? You will need to clean up any associated resources on your own.\n"
                "Continue with force deletion?",
                skip_confirmation,
            )

        # Tear down admin zone and mark cloud as deleted
        with self.log.spinner("Deleting Anyscale cloud..."):
            try:
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
            except ClickException as e:
                self.log.error(e)
                raise ClickException(f"Failed to delete cloud with name {cloud_name}.")

        self.log.info(f"Deleted cloud with name {cloud_name}.")
        return True

    def delete_all_gcp_resources(self, cloud: CloudWithCloudResource):
        if cloud.is_aioa or cloud.compute_stack == ComputeStack.K8S:
            # No resources to delete for hosted and k8s clouds
            return True

        setup_utils = try_import_gcp_managed_setup_utils()
        gcp_utils = try_import_gcp_utils()
        credentials = json.loads(cloud.credentials)
        provider = credentials["gcp_workload_identity_pool_id"]
        service_account = credentials["service_account_email"]
        project_id = credentials["project_id"]
        factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)

        # Delete services resources
        setup_utils.delete_gcp_tls_certificates(factory, project_id, cloud.id)

        # Clean up cloud resources
        if cloud.is_bring_your_own_resource is False:  # managed cloud
            self.delete_gcp_managed_cloud(cloud=cloud)
        else:
            self.log.warning(
                f"The workload identity federation provider pool {provider} and service account {service_account} that allows Anyscale to access your GCP account is still in place. Please delete it manually if you no longer wish anyscale to have access."
            )

        return True

    def delete_all_aws_resources(self, cloud: CloudWithCloudResource) -> bool:
        if cloud.is_aioa or cloud.compute_stack == ComputeStack.K8S:
            # No resources to delete for hosted and k8s clouds
            return True

        # Delete services resources
        self.delete_aws_lb_cfn_stack(cloud=cloud)
        self.delete_aws_tls_certificates(cloud=cloud)

        # Clean up cloud resources
        if cloud.is_bring_your_own_resource is False:  # managed cloud
            # Delete AWS cloud resources by deleting the cfn stack
            self.delete_aws_managed_cloud(cloud=cloud)
        else:  # registered cloud
            self.log.warning(
                f"The trust policy that allows Anyscale to assume {cloud.credentials} is still in place. Please delete it manually if you no longer wish anyscale to have access."
            )

        return True

    def delete_aws_lb_cfn_stack(self, cloud: CloudWithCloudResource) -> bool:

        tag_name = "anyscale-cloud-id"
        key_name = cloud.id

        cfn_client = _client("cloudformation", cloud.region)
        # Get a list of all the CloudFormation stacks with the specified tag
        stacks = cfn_client.list_stacks()

        stacks = _unroll_resources_for_aws_list_call(
            cfn_client.list_stacks, "StackSummaries"
        )

        resources_to_cleanup = []

        for stack in stacks:
            if "StackName" in stack and "StackId" in stack:
                cfn_stack_arn = stack["StackId"]
                stack_description = cfn_client.describe_stacks(StackName=cfn_stack_arn)

                # Extract the tags from the response
                if (
                    "Stacks" in stack_description
                    and stack_description["Stacks"]
                    and "Tags" in stack_description["Stacks"][0]
                ):
                    tags = stack_description["Stacks"][0]["Tags"]
                    for tag in tags:
                        if (
                            "Key" in tag
                            and tag["Key"] == tag_name
                            and "Value" in tag
                            and tag["Value"] == key_name
                        ):
                            resources_to_cleanup.append(cfn_stack_arn)

        resource_delete_status = []
        for cfn_stack_arn in resources_to_cleanup:
            resource_delete_status.append(
                self.delete_aws_cloudformation_stack(
                    cfn_stack_arn=cfn_stack_arn, cloud=cloud
                )
            )

        return all(resource_delete_status)

    def delete_aws_tls_certificates(self, cloud: CloudWithCloudResource) -> bool:
        tag_name = "anyscale-cloud-id"
        key_name = cloud.id

        acm = boto3.client("acm", cloud.region)

        certificates = _unroll_resources_for_aws_list_call(
            acm.list_certificates, "CertificateSummaryList"
        )

        matching_certs = []

        for certificate in certificates:
            if "CertificateArn" in certificate:

                certificate_arn = certificate["CertificateArn"]
                response = acm.list_tags_for_certificate(CertificateArn=certificate_arn)

                if "Tags" in response:
                    tags = response["Tags"]
                    for tag in tags:
                        if (
                            "Key" in tag
                            and tag["Key"] == tag_name
                            and "Value" in tag
                            and tag["Value"] == key_name
                        ):
                            matching_certs.append(certificate_arn)

        resource_delete_status = []
        for certificate_arn in matching_certs:
            resource_delete_status.append(self.delete_tls_cert(certificate_arn, cloud))
        return all(resource_delete_status)

    def delete_aws_managed_cloud(self, cloud: CloudWithCloudResource) -> bool:
        if (
            not cloud.cloud_resource
            or not cloud.cloud_resource.aws_cloudformation_stack_id
        ):
            raise ClickException(
                f"This cloud {cloud.id} does not have a cloudformation stack."
            )

        cfn_stack_arn = cloud.cloud_resource.aws_cloudformation_stack_id

        # If the cloud is updated, the cross account IAM role might have an inline policy for customer drifts
        # We delete the inline policy first otherwise cfn stack deletion would fail
        try_delete_customer_drifts_policy(cloud=cloud)

        self.log.info(
            f"\nThe S3 bucket ({cloud.cloud_resource.aws_s3_id}) associated with this cloud still exists."
            "\nIf you no longer need the data associated with this bucket, please delete it."
        )

        return self.delete_aws_cloudformation_stack(
            cfn_stack_arn=cfn_stack_arn, cloud=cloud
        )

    def delete_aws_cloudformation_stack(
        self, cfn_stack_arn: str, cloud: CloudWithCloudResource
    ) -> bool:
        cfn_client = _client("cloudformation", cloud.region)

        cfn_stack_url = f"https://{cloud.region}.console.aws.amazon.com/cloudformation/home?region={cloud.region}#/stacks/stackinfo?stackId={cfn_stack_arn}"

        try:
            cfn_client.delete_stack(StackName=cfn_stack_arn)
        except ClientError:
            raise ClickException(
                f"Failed to delete cloudformation stack {cfn_stack_arn}.\nPlease view it at {cfn_stack_url}"
            ) from None

        self.log.info(f"\nTrack progress of cloudformation at {cfn_stack_url}")
        with self.log.spinner(
            f"Deleting cloud resource {cfn_stack_arn} through cloudformation..."
        ):
            end_time = time.time() + CLOUDFORMATION_TIMEOUT_SECONDS_LONG
            while time.time() < end_time:
                try:
                    cfn_stack = cfn_client.describe_stacks(StackName=cfn_stack_arn)[
                        "Stacks"
                    ][0]
                except ClientError as e:
                    raise ClickException(
                        f"Failed to fetch the cloudformation stack {cfn_stack_arn}. Please check you have the right AWS credentials and the cloudformation stack still exists. Error details: {e}"
                    ) from None

                if cfn_stack["StackStatus"] == "DELETE_COMPLETE":
                    self.log.info(
                        f"Cloudformation stack {cfn_stack['StackId']} is deleted."
                    )
                    break

                if cfn_stack["StackStatus"] in ("DELETE_FAILED"):
                    # Provide link to cloudformation
                    raise ClickException(
                        f"Failed to delete cloud resources. Please check your cloudformation stack for errors. {cfn_stack_url}"
                    )
                time.sleep(1)

            if time.time() > end_time:
                raise ClickException(
                    f"Timed out deleting AWS resources. Please check your cloudformation stack for errors. {cfn_stack['StackId']}"
                )

        return True

    def delete_tls_cert(
        self, certificate_arn: str, cloud: CloudWithCloudResource
    ) -> bool:
        acm = boto3.client("acm", cloud.region)

        try:
            acm.delete_certificate(CertificateArn=certificate_arn)
        except ClientError as e:
            raise ClickException(
                f"Failed to delete TLS certificate {certificate_arn}: {e}"
            ) from None

        return True

    def delete_gcp_managed_cloud(self, cloud: CloudWithCloudResourceGCP) -> bool:
        if (
            not cloud.cloud_resource
            or not cloud.cloud_resource.gcp_deployment_manager_id
        ):
            raise ClickException(
                f"This cloud {cloud.id} does not have a deployment in GCP deployment manager."
            )
        setup_utils = try_import_gcp_managed_setup_utils()
        gcp_utils = try_import_gcp_utils()

        project_id = json.loads(cloud.credentials)["project_id"]
        factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
        deployment_name = cloud.cloud_resource.gcp_deployment_manager_id
        deployment_url = f"https://console.cloud.google.com/dm/deployments/details/{deployment_name}?project={project_id}"

        self.log.info(f"\nTrack progress of Deployment Manager at {deployment_url}")

        with self.log.spinner("Deleting cloud resources through Deployment Manager..."):

            # Remove firewall policy ids
            if cloud.cloud_resource.gcp_firewall_policy_ids:
                for firewall_policy in cloud.cloud_resource.gcp_firewall_policy_ids:
                    # try delete the associations
                    setup_utils.remove_firewall_policy_associations(
                        factory, project_id, firewall_policy
                    )

            # Delete the deployment
            setup_utils.update_deployment_with_bucket_only(
                factory, project_id, deployment_name
            )

        self.log.info(
            f"\nThe cloud bucket ({cloud.cloud_resource.gcp_cloud_storage_bucket_id}) associated with this cloud still exists."
            "\nIf you no longer need the data associated with this bucket, please delete it."
        )
        return True

    ### Edit cloud ###
    def _get_cloud_resource_value(self, cloud_resource: Any, resource_type: str) -> Any:
        # Special case -- memorydb_cluster_id
        if resource_type == "memorydb_cluster_id":
            memorydb_cluster_config = getattr(
                cloud_resource, "memorydb_cluster_config", None
            )
            if memorydb_cluster_config is None:
                return None
            else:
                # memorydb_cluster_config.id has format "arn:aws:memorydb:us-east-2:815664363732:cluster/cloud-edit-test".
                value = memorydb_cluster_config.id.split("/")[-1]
                return value

        # Special case -- memorystore_instance_name
        if resource_type == "memorystore_instance_name":
            memorystore_instance_config = getattr(
                cloud_resource, "memorystore_instance_config", None
            )
            if memorystore_instance_config is None:
                return None
            else:
                value = memorystore_instance_config.name
                return value

        # Normal cases.
        value = getattr(cloud_resource, resource_type, None)
        if value is None:
            self.log.warning(f"Old value of {resource_type} is None.")
            return None
        return value

    def _generate_edit_details_logs(
        self, cloud_resource: Any, edit_details: Dict[str, Optional[str]]
    ) -> List[str]:
        details_logs = []
        for resource_type, value in edit_details.items():
            if value:
                old_value = self._get_cloud_resource_value(
                    cloud_resource, resource_type
                )
                if old_value == value:
                    raise ClickException(
                        f"Specified resource is the same as existed resource -- {resource_type}: {value}"
                    )
                details_logs.append(f"{resource_type}: from {old_value} -> {value}")
        return details_logs

    def _generate_rollback_command(
        self, cloud_id: str, cloud_resource: Any, edit_details: Dict[str, Optional[str]]
    ) -> str:
        rollback_command = BASE_ROLLBACK_COMMAND.format(cloud_id=cloud_id)
        for resource_type, value in edit_details.items():
            if value:
                old_value = self._get_cloud_resource_value(
                    cloud_resource, resource_type
                )
                if old_value is not None:
                    # The resource type names are in CreateCloudResource (backend/server/api/product/models/clouds.py).
                    # The cli command names are in cloud_edit (frontend/cli/anyscale/commands:cloud_commands).
                    # The relationship between their names are cli_command_name = resource_type_name.replace("_", "-").
                    # e.g. cli_command_name: aws-s3-id & resource_type_name: aws_s3_id.
                    formatted_resource_type = resource_type.replace("_", "-")
                    rollback_command += f" --{formatted_resource_type}={old_value}"
        # If the only edit field is redis and it was None originally, rollback_command didn't appened any args, reset the rollback command to be empty.
        if rollback_command == BASE_ROLLBACK_COMMAND.format(cloud_id=cloud_id):
            rollback_command = ""
        return rollback_command

    def _edit_aws_cloud(  # noqa: PLR0912
        self,
        *,
        cloud_id: str,
        cloud_name: str,
        cloud: Any,
        cloud_resource: Any,
        aws_s3_id: Optional[str],
        aws_efs_id: Optional[str],
        aws_efs_mount_target_ip: Optional[str],
        memorydb_cluster_id: Optional[str],
        yes: bool = False,
    ):
        # Log edit details.
        self.log.open_block("EditDetail", "\nEdit details...")
        edit_details = {
            "aws_s3_id": aws_s3_id,
            "aws_efs_id": aws_efs_id,
            "aws_efs_mount_target_ip": aws_efs_mount_target_ip,
            "memorydb_cluster_id": memorydb_cluster_id,
        }
        details_logs = self._generate_edit_details_logs(cloud_resource, edit_details)
        self.log.info(
            self.log.highlight(
                "Cloud {} ({}) edit details: \n{}".format(
                    cloud_name, cloud_id, "; \n".join(details_logs)
                )
            )
        )
        self.log.close_block("EditDetail")

        try:
            boto3_session = boto3.Session(region_name=cloud.region)
            if aws_efs_id and not aws_efs_mount_target_ip:
                # Get the mount target IP for new aws_efs_ip (consistent with cloud register).
                aws_efs_mount_target_ip = _get_aws_efs_mount_target_ip(
                    boto3_session, aws_efs_id
                )
                if not aws_efs_mount_target_ip:
                    raise ClickException(
                        f"Failed to get the mount target IP for new aws_efs_ip {aws_efs_id}, please make sure the aws_efs_ip exists and it has mount targets."
                    )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                f"Failed to get the mount target IP for new aws_efs_ip {aws_efs_id}, please make sure it has mount targets."
            )
        try:
            memorydb_cluster_config = None
            if memorydb_cluster_id:
                memorydb_cluster_config = _get_memorydb_cluster_config(
                    memorydb_cluster_id, cloud.region, self.log
                )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                f"Failed to get the memorydb cluster config for new memorydb_cluster_id {memorydb_cluster_id}, please make sure it's created."
            )

        # Static Verify.
        self.log.open_block(
            "Verify", "Start cloud static verification on the specified resources..."
        )
        new_cloud_resource = copy.deepcopy(cloud_resource)
        if aws_s3_id:
            new_cloud_resource.aws_s3_id = aws_s3_id
        if aws_efs_id:
            new_cloud_resource.aws_efs_id = aws_efs_id
        if aws_efs_mount_target_ip:
            new_cloud_resource.aws_efs_mount_target_ip = aws_efs_mount_target_ip
        if memorydb_cluster_id:
            new_cloud_resource.memorydb_cluster_config = memorydb_cluster_config

        if not self.verify_aws_cloud_resources(
            cloud_resource=new_cloud_resource,
            boto3_session=boto3_session,
            region=cloud.region,
            cloud_id=cloud_id,
            is_bring_your_own_resource=cloud.is_bring_your_own_resource,
            is_private_network=cloud.is_private_cloud
            if cloud.is_private_cloud
            else False,
        ):
            raise ClickException(
                "Cloud edit failed because resource failed verification. Please check the verification results above, fix them, and try again."
            )

        self.log.info(
            self.log.highlight(
                "Please make sure you checked the warnings from above verification results."
            )
        )
        self.log.close_block("Verify")

        self.log.open_block(
            "Reminder", "Please read the following reminder carefully..."
        )
        self.log.info(
            self.log.highlight(
                "If there are running workloads utilizing the old resources, you may want to retain them. Please note that this edit will not automatically remove any old resources. If you wish to delete them, you'll need to handle it."
            )
        )
        self.log.info(
            self.log.highlight(
                "The cloud resources we are going to edit {} ({}): \n{}".format(
                    cloud_name, cloud_id, "; \n".join(details_logs)
                )
            )
        )
        self.log.close_block("Reminder")

        confirm(
            "Are you sure you want to edit these cloud resource? ", yes,
        )

        # Execute edit cloud.
        self.log.open_block("Edit", "Start editing cloud...")
        try:
            self.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_patch(
                cloud_id=cloud_id,
                editable_cloud_resource=EditableCloudResource(
                    aws_s3_id=aws_s3_id,
                    aws_efs_id=aws_efs_id,
                    aws_efs_mount_target_ip=aws_efs_mount_target_ip,
                    memorydb_cluster_config=memorydb_cluster_config,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                "Edit cloud resource failed! The backend server might be under maintainance right now, please reach out to support or your SA for assistance."
            )

        # Hint customer rollback command.
        rollback_command = self._generate_rollback_command(
            cloud_id, cloud_resource, edit_details
        )
        self.log.info(
            self.log.highlight(
                f"Cloud {cloud_name}({cloud_id}) is successfully edited."
            )
        )
        if rollback_command:
            self.log.info(
                self.log.highlight(
                    f"If you want to revert the edit, you can edit it back to the original cloud with: `{rollback_command}`"
                )
            )
        self.log.close_block("Edit")

    def _get_project_id(self, cloud: Any, cloud_name: str, cloud_id: str) -> str:
        try:
            return json.loads(cloud.credentials)["project_id"]
        except Exception:  # noqa: BLE001
            raise ClickException(
                f"Failed to get project id for cloud {cloud_name}({cloud_id}). Please ensure the provided cloud_name/cloud_id exists."
            )

    def _get_host_project_id(
        self, cloud: Any, cloud_name: str, cloud_id: str
    ) -> Optional[str]:
        try:
            credentials = json.loads(cloud.credentials)
            return credentials.get("host_project_id")
        except Exception:  # noqa: BLE001
            raise ClickException(
                f"Failed to get host project id for cloud {cloud_name}({cloud_id}). Please ensure the provided cloud_name/cloud_id exists."
            )

    def _get_gcp_filestore_config(
        self,
        gcp_filestore_instance_id: str,
        gcp_filestore_location: str,
        project_id: str,
        cloud_resource: Any,
        gcp_utils,
    ) -> GCPFileStoreConfig:
        try:
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
            return gcp_utils.get_gcp_filestore_config(
                factory,
                project_id,
                cloud_resource.gcp_vpc_id,
                gcp_filestore_location,
                gcp_filestore_instance_id,
                self.log,
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                f"Failed to construct the gcp_filestore_config from project {project_id}, please double check the provided filestore_location {gcp_filestore_location} and filestore_instance_id {gcp_filestore_instance_id}."
            )

    def _get_gcp_edit_details(
        self,
        *,
        cloud_resource: Any,
        edit_details: Dict[str, Optional[str]],
        gcp_filestore_config: Optional[GCPFileStoreConfig],
        gcp_filestore_instance_id: Optional[str],
        gcp_filestore_location: Optional[str],
        gcp_utils,
    ) -> List[str]:
        details_logs = self._generate_edit_details_logs(cloud_resource, edit_details)
        if gcp_filestore_config:
            (
                old_filestore_location,
                old_filestore_instance_id,
            ) = gcp_utils.get_filestore_location_and_instance_id(
                cloud_resource.gcp_filestore_config
            )
            if (
                old_filestore_instance_id == gcp_filestore_instance_id
                and old_filestore_location == gcp_filestore_location
            ):
                raise ClickException(
                    f"Specified resource is the same as existed resource -- gcp_filestore_instance_id: {gcp_filestore_instance_id}; gcp_filestore_location: {gcp_filestore_location}"
                )
            details_logs.append(
                f"filestore_instance_id: from {old_filestore_instance_id} -> {gcp_filestore_instance_id}"
            )
            details_logs.append(
                f"filestore_location: from {old_filestore_location} -> {gcp_filestore_location}"
            )
        return details_logs

    def _generate_rollback_command_for_gcp(
        self,
        cloud_id: str,
        cloud_resource: Any,
        edit_details: Dict[str, Optional[str]],
        gcp_filestore_config: Optional[GCPFileStoreConfig],
        gcp_utils,
    ):
        rollback_cmd = self._generate_rollback_command(
            cloud_id, cloud_resource, edit_details
        )
        if gcp_filestore_config:
            (
                old_filestore_location,
                old_filestore_instance_id,
            ) = gcp_utils.get_filestore_location_and_instance_id(
                cloud_resource.gcp_filestore_config
            )
            rollback_cmd += f" --gcp-filestore-instance-id={old_filestore_instance_id}"
            rollback_cmd += f" --gcp-filestore-location={old_filestore_location}"
        rollback_cmd = rollback_cmd.replace(
            "gcp-cloud-storage-bucket-id", "gcp-cloud-storage-bucket-name"
        )
        return rollback_cmd

    def _edit_gcp_cloud(  # noqa: PLR0912
        self,
        *,
        cloud_id: str,
        cloud_name: str,
        cloud: Any,
        cloud_resource: Any,
        gcp_filestore_instance_id: Optional[str],
        gcp_filestore_location: Optional[str],
        gcp_cloud_storage_bucket_name: Optional[str],
        memorystore_instance_name: Optional[str],
        yes: bool = False,
    ):
        project_id = self._get_project_id(cloud, cloud_name, cloud_id)
        host_project_id = self._get_host_project_id(cloud, cloud_name, cloud_id)
        gcp_utils = try_import_gcp_utils()

        gcp_filestore_config = None
        if gcp_filestore_instance_id and gcp_filestore_location:
            gcp_filestore_config = self._get_gcp_filestore_config(
                gcp_filestore_instance_id,
                gcp_filestore_location,
                project_id,
                cloud_resource,
                gcp_utils,
            )

        memorystore_instance_config = None
        if memorystore_instance_name:
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
            memorystore_instance_config = gcp_utils.get_gcp_memorystore_config(
                factory, memorystore_instance_name
            )

        # Log edit details.
        self.log.open_block("EditDetail", "\nEdit details...")
        edit_details = {
            "gcp_cloud_storage_bucket_id": gcp_cloud_storage_bucket_name,
            "memorystore_instance_name": memorystore_instance_name,
        }
        details_logs = self._get_gcp_edit_details(
            cloud_resource=cloud_resource,
            edit_details=edit_details,
            gcp_filestore_config=gcp_filestore_config,
            gcp_filestore_instance_id=gcp_filestore_instance_id,
            gcp_filestore_location=gcp_filestore_location,
            gcp_utils=gcp_utils,
        )
        self.log.info(
            self.log.highlight(
                "Cloud edit details {} ({}): \n{}".format(
                    cloud_name, cloud_id, "; \n".join(details_logs)
                )
            )
        )
        self.log.close_block("EditDetail")

        # Static Verify.
        self.log.open_block(
            "Verify", "Start cloud static verification on the specified resources..."
        )
        new_cloud_resource = copy.deepcopy(cloud_resource)
        if gcp_filestore_config:
            new_cloud_resource.gcp_filestore_config = gcp_filestore_config
        if gcp_cloud_storage_bucket_name:
            new_cloud_resource.gcp_cloud_storage_bucket_id = (
                gcp_cloud_storage_bucket_name
            )
        if memorystore_instance_config:
            new_cloud_resource.memorystore_instance_config = memorystore_instance_config
        if not self.verify_gcp_cloud_resources(
            cloud_resource=new_cloud_resource,
            project_id=project_id,
            host_project_id=host_project_id,
            region=cloud.region,
            cloud_id=cloud_id,
            yes=False,
        ):
            raise ClickException(
                "Cloud edit failed because resource failed verification. Please check the verification results above, fix them, and try again."
            )

        self.log.info(
            self.log.highlight(
                "Please make sure you checked the warnings from above verification results."
            )
        )
        self.log.close_block("Verify")

        self.log.open_block(
            "Reminder", "Please read the following reminder carefully..."
        )
        self.log.info(
            self.log.highlight(
                "If there are running workloads utilizing the old resources, you may want to retain them. Please note that this edit will not automatically remove any old resources. If you wish to delete them, you'll need to handle it."
            )
        )
        self.log.info(
            self.log.highlight(
                "The cloud resources we are going to edit {} ({}): \n{}".format(
                    cloud_name, cloud_id, "; \n".join(details_logs)
                )
            )
        )
        self.log.close_block("Reminder")

        confirm(
            "Are you sure you want to edit these cloud resource? ", yes,
        )

        # Execute edit cloud.
        self.log.open_block("Edit", "Start editing cloud...")
        try:
            self.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_patch(
                cloud_id=cloud_id,
                editable_cloud_resource_gcp=EditableCloudResourceGCP(
                    gcp_filestore_config=gcp_filestore_config,
                    gcp_cloud_storage_bucket_id=gcp_cloud_storage_bucket_name,
                    memorystore_instance_config=memorystore_instance_config,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                "Edit cloud resource failed! The backend server might be under maintainance right now, please reach out to support or your SA for assistance."
            )

        # Hint customer rollback command.
        rollback_command = self._generate_rollback_command_for_gcp(
            cloud_id, cloud_resource, edit_details, gcp_filestore_config, gcp_utils,
        )
        self.log.info(
            self.log.highlight(
                f"Cloud {cloud_name}({cloud_id}) is successfully edited."
            )
        )
        if rollback_command:
            self.log.info(
                self.log.highlight(
                    f"If you want to revert the edit, you can edit it back to the original cloud with: `{rollback_command}`"
                )
            )
        self.log.close_block("Edit")

    def edit_cloud(  # noqa: PLR0912,PLR0913
        self,
        *,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        aws_s3_id: Optional[str],
        aws_efs_id: Optional[str],
        aws_efs_mount_target_ip: Optional[str],
        memorydb_cluster_id: Optional[str],
        gcp_filestore_instance_id: Optional[str],
        gcp_filestore_location: Optional[str],
        gcp_cloud_storage_bucket_name: Optional[str],
        memorystore_instance_name: Optional[str],
        functional_verify: Optional[str],
        yes: bool = False,
        auto_add_user: Optional[bool] = None,
    ):
        """Edit aws cloud.

        The editable fields are in EditableCloudResource (AWS) /EditableCloudResourceGCP (GCP).
        Steps:
        1. Log the edits (from old to new values).
        2. Static verify cloud resources with updated values.
        3. Prompt the customer for confirmation based on verification results.
        4. Update the cloud resource (calls backend API to modify the database).
        5. Conduct a functional verification, if specified.
        """
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )
        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result

        if not cloud.is_bring_your_own_resource:
            raise ClickException(
                f"Cloud {cloud_name}({cloud_id}) is not a cloud with customer defined resources, currently we don't support editing cloud resource values of managed clouds."
            )

        cloud_resource = get_cloud_resource_by_cloud_id(
            cloud_id, cloud.provider, self.api_client
        )
        if cloud_resource is None:
            raise ClickException(
                f"Cloud {cloud_name}({cloud_id}) does not contain resource records."
            )

        if auto_add_user is not None:
            self._update_auto_add_user_field(auto_add_user, cloud)

        if any(
            [
                aws_s3_id,
                aws_efs_id,
                aws_efs_mount_target_ip,
                memorydb_cluster_id,
                gcp_filestore_instance_id,
                gcp_filestore_location,
                gcp_cloud_storage_bucket_name,
                memorystore_instance_name,
            ]
        ):
            if cloud.provider == "AWS":
                self.cloud_event_producer.init_trace_context(
                    CloudAnalyticsEventCommandName.EDIT,
                    CloudProviders.AWS,
                    cloud_id=cloud_id,
                )
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.COMMAND_START, succeeded=True
                )
                if (
                    not any(
                        [
                            aws_s3_id,
                            aws_efs_id,
                            aws_efs_mount_target_ip,
                            memorydb_cluster_id,
                        ]
                    )
                ) or any(
                    [
                        gcp_filestore_instance_id,
                        gcp_filestore_location,
                        gcp_cloud_storage_bucket_name,
                        memorystore_instance_name,
                    ]
                ):
                    self.cloud_event_producer.produce(
                        CloudAnalyticsEventName.RESOURCES_EDITED,
                        succeeded=False,
                        internal_error="specified resource and provider mismatch",
                    )
                    raise ClickException(
                        "Specified resource and provider mismatch -- the cloud's provider is AWS, please make sure all the resource you want to edit is for AWS as well."
                    )
                try:
                    self._edit_aws_cloud(
                        cloud_id=cloud_id,  # type: ignore
                        cloud_name=cloud_name,  # type: ignore
                        cloud=cloud,
                        cloud_resource=cloud_resource,
                        aws_s3_id=aws_s3_id,
                        aws_efs_id=aws_efs_id,
                        aws_efs_mount_target_ip=aws_efs_mount_target_ip,
                        memorydb_cluster_id=memorydb_cluster_id,
                        yes=yes,
                    )
                except Exception as e:  # noqa: BLE001
                    self.cloud_event_producer.produce(
                        CloudAnalyticsEventName.RESOURCES_EDITED,
                        succeeded=False,
                        logger=self.log,
                        internal_error=str(e),
                    )
                    raise e
            elif cloud.provider == "GCP":
                self.cloud_event_producer.init_trace_context(
                    CloudAnalyticsEventCommandName.EDIT,
                    CloudProviders.GCP,
                    cloud_id=cloud_id,
                )
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.COMMAND_START, succeeded=True
                )
                if (
                    not any(
                        [
                            gcp_filestore_instance_id,
                            gcp_filestore_location,
                            gcp_cloud_storage_bucket_name,
                            memorystore_instance_name,
                        ]
                    )
                ) or any(
                    [
                        aws_s3_id,
                        aws_efs_id,
                        aws_efs_mount_target_ip,
                        memorydb_cluster_id,
                    ]
                ):
                    self.cloud_event_producer.produce(
                        CloudAnalyticsEventName.RESOURCES_EDITED,
                        succeeded=False,
                        internal_error="specified resource and provider mismatch",
                    )
                    raise ClickException(
                        "Specified resource and provider mismatch -- the cloud's provider is GCP, please make sure all the resource you want to edit is for GCP as well."
                    )
                try:
                    self._edit_gcp_cloud(
                        cloud_id=cloud_id,  # type: ignore
                        cloud_name=cloud_name,  # type: ignore
                        cloud=cloud,
                        cloud_resource=cloud_resource,
                        gcp_filestore_instance_id=gcp_filestore_instance_id,
                        gcp_filestore_location=gcp_filestore_location,
                        gcp_cloud_storage_bucket_name=gcp_cloud_storage_bucket_name,
                        memorystore_instance_name=memorystore_instance_name,
                        yes=yes,
                    )
                except Exception as e:  # noqa: BLE001
                    self.cloud_event_producer.produce(
                        CloudAnalyticsEventName.RESOURCES_EDITED,
                        succeeded=False,
                        logger=self.log,
                        internal_error=str(e),
                    )
                    raise e
            else:
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_EDITED,
                    succeeded=False,
                    internal_error="invalid cloud provider",
                )
                raise ClickException(
                    f"Unsupported cloud provider {cloud.provider} for cloud edit!"
                )

        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.RESOURCES_EDITED, succeeded=True
        )
        # Functional verify.
        if len(functions_to_verify) > 0:
            functional_verify_succeed = CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(
                cloud_id,
                self._get_cloud_provider_from_str(cloud.provider),
                functions_to_verify,
                yes,
            )
            if not functional_verify_succeed:
                raise ClickException(
                    "Cloud functional verification failed. Please consider the following options:\n"
                    "1. Create a new cloud (we recommend)\n"
                    "2. Double-check the resources specified in the edit details, and the verification results, modify the resource if necessary, run `anyscale cloud verify (optional with functional-verify)` to verify again.\n"
                    "3. Edit the resource back to original if you still want to use this cloud.\n"
                )

    ### End of edit cloud ###

    def generate_jobs_report(
        self, cloud_id: str, csv: bool, out_path: str, sort: str, sort_order_asc: bool
    ) -> None:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)

        full_results = []
        paging_token: Optional[str] = None
        count_per_page = 20
        curr_page_results = None
        total_jobs: Optional[int] = None

        with Progress() as progress:
            download_task = progress.add_task("Downloading jobs...", total=None)

            while curr_page_results is None or len(curr_page_results) == count_per_page:
                response = self.api_client.list_job_reports_api_v2_job_reports_get(
                    cloud_id,
                    start_time=start_time,
                    end_time=end_time,
                    paging_token=paging_token,
                    count=count_per_page,
                )
                curr_page_results = response.results
                full_results.extend(curr_page_results)
                paging_token = response.metadata.next_paging_token
                total_jobs = response.metadata.total
                progress.update(
                    download_task, total=total_jobs, advance=len(curr_page_results)
                )

            progress.update(download_task, completed=total_jobs)

        if not full_results:
            self.log.info("No jobs found in the last 7 days.")
            return

        filtered_results = [
            job
            for job in full_results
            if job.job_state in TERMINAL_HA_JOB_STATES and job.job_report is not None
        ]
        if sort == "created_at":
            filtered_results.sort(
                key=lambda x: x.created_at, reverse=not sort_order_asc
            )
        elif sort == "gpu":
            filtered_results.sort(
                key=lambda x: x.job_report.unused_gpu_hours or 0,
                reverse=not sort_order_asc,
            )
        elif sort == "cpu":
            filtered_results.sort(
                key=lambda x: x.job_report.unused_cpu_hours or 0,
                reverse=not sort_order_asc,
            )
        elif sort == "instances":
            filtered_results.sort(
                key=lambda x: x.job_report.max_instances_launched or 0,
                reverse=not sort_order_asc,
            )

        with open(out_path, "w") as out_file:
            if csv:
                out_file.write(
                    "Job ID,Job name,Job state,Created at,Finished at,Duration,Unused CPU hours,Unused GPU hours,Max concurrent instances\n"
                )
                for job in track(filtered_results, description="Generating report..."):
                    job_state = HA_JOB_STATE_TO_JOB_STATE[job.job_state]
                    if job.finished_at is not None:
                        duration = str(job.finished_at - job.created_at)
                        finished_at = str(job.finished_at)
                    else:
                        duration = ""
                        finished_at = ""
                    unused_cpu_hours = job.job_report.unused_cpu_hours or ""
                    unused_gpu_hours = job.job_report.unused_gpu_hours or ""
                    max_instances_launched = job.job_report.max_instances_launched or ""

                    out_file.write(
                        f'"{job.job_id}","{job.job_name}","{job_state}","{str(job.created_at)}","{finished_at}","{duration}","{unused_cpu_hours}","{unused_gpu_hours}","{max_instances_launched}"\n'
                    )
            else:
                out_file.write(
                    f"""
<html>
<head>
<title>Jobs Report - {str(end_time)}</title>
<style>
    table {{
        border: 1px solid black;
        border-collapse: collapse;
    }}
    th, td {{
        border: 1px solid black;
        border-collapse: collapse;
        padding: 8px;
    }}
</style>
</head>
<body>
<h1>Job Report - {str(end_time)}</h1>
<p>Total jobs reported (finished jobs): {len(filtered_results)}</p>
<p>Total jobs in the last 7 days: {total_jobs}</p>
<table>
<thead>
<tr>
<th>Job ID</th>
<th>Job name</th>
<th>Job state</th>
<th>Created at</th>
<th>Finished at</th>
<th>Duration</th>
<th>Unused CPU hours</th>
<th>Unused GPU hours</th>
<th>Max concurrent instances</th>
</tr>
</thead>
<tbody>
"""
                )

                for job in track(filtered_results, description="Generating report..."):
                    job_state = HA_JOB_STATE_TO_JOB_STATE[job.job_state]
                    if job.finished_at is not None:
                        duration = str(job.finished_at - job.created_at)
                        finished_at = str(job.finished_at)
                    else:
                        duration = ""
                        finished_at = ""
                    unused_cpu_hours = job.job_report.unused_cpu_hours or ""
                    unused_gpu_hours = job.job_report.unused_gpu_hours or ""
                    max_instances_launched = job.job_report.max_instances_launched or ""

                    out_file.write(
                        f"""
<tr>
<td><a target="_blank" rel="noreferrer" href="{ANYSCALE_HOST}/jobs/{job.job_id}">{job.job_id}</a></td>
<td>{job.job_name}</td>
<td>{job_state}</td>
<td>{str(job.created_at)}</td>
<td>{finished_at}</td>
<td>{duration}</td>
<td>{unused_cpu_hours}</td>
<td>{unused_gpu_hours}</td>
<td>{max_instances_launched}</td>
</tr>
"""
                    )

                out_file.write(
                    """
</tbody>
</table>
"""
                )
