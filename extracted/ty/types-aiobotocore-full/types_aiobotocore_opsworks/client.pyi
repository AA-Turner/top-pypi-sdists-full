"""
Type annotations for opsworks service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_opsworks.client import OpsWorksClient

    session = get_session()
    async with session.create_client("opsworks") as client:
        client: OpsWorksClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import DescribeEcsClustersPaginator
from .type_defs import (
    AssignInstanceRequestTypeDef,
    AssignVolumeRequestTypeDef,
    AssociateElasticIpRequestTypeDef,
    AttachElasticLoadBalancerRequestTypeDef,
    CloneStackRequestTypeDef,
    CloneStackResultTypeDef,
    CreateAppRequestTypeDef,
    CreateAppResultTypeDef,
    CreateDeploymentRequestTypeDef,
    CreateDeploymentResultTypeDef,
    CreateInstanceRequestTypeDef,
    CreateInstanceResultTypeDef,
    CreateLayerRequestTypeDef,
    CreateLayerResultTypeDef,
    CreateStackRequestTypeDef,
    CreateStackResultTypeDef,
    CreateUserProfileRequestTypeDef,
    CreateUserProfileResultTypeDef,
    DeleteAppRequestTypeDef,
    DeleteInstanceRequestTypeDef,
    DeleteLayerRequestTypeDef,
    DeleteStackRequestTypeDef,
    DeleteUserProfileRequestTypeDef,
    DeregisterEcsClusterRequestTypeDef,
    DeregisterElasticIpRequestTypeDef,
    DeregisterInstanceRequestTypeDef,
    DeregisterRdsDbInstanceRequestTypeDef,
    DeregisterVolumeRequestTypeDef,
    DescribeAgentVersionsRequestTypeDef,
    DescribeAgentVersionsResultTypeDef,
    DescribeAppsRequestTypeDef,
    DescribeAppsResultTypeDef,
    DescribeCommandsRequestTypeDef,
    DescribeCommandsResultTypeDef,
    DescribeDeploymentsRequestTypeDef,
    DescribeDeploymentsResultTypeDef,
    DescribeEcsClustersRequestTypeDef,
    DescribeEcsClustersResultTypeDef,
    DescribeElasticIpsRequestTypeDef,
    DescribeElasticIpsResultTypeDef,
    DescribeElasticLoadBalancersRequestTypeDef,
    DescribeElasticLoadBalancersResultTypeDef,
    DescribeInstancesRequestTypeDef,
    DescribeInstancesResultTypeDef,
    DescribeLayersRequestTypeDef,
    DescribeLayersResultTypeDef,
    DescribeLoadBasedAutoScalingRequestTypeDef,
    DescribeLoadBasedAutoScalingResultTypeDef,
    DescribeMyUserProfileResultTypeDef,
    DescribeOperatingSystemsResponseTypeDef,
    DescribePermissionsRequestTypeDef,
    DescribePermissionsResultTypeDef,
    DescribeRaidArraysRequestTypeDef,
    DescribeRaidArraysResultTypeDef,
    DescribeRdsDbInstancesRequestTypeDef,
    DescribeRdsDbInstancesResultTypeDef,
    DescribeServiceErrorsRequestTypeDef,
    DescribeServiceErrorsResultTypeDef,
    DescribeStackProvisioningParametersRequestTypeDef,
    DescribeStackProvisioningParametersResultTypeDef,
    DescribeStacksRequestTypeDef,
    DescribeStacksResultTypeDef,
    DescribeStackSummaryRequestTypeDef,
    DescribeStackSummaryResultTypeDef,
    DescribeTimeBasedAutoScalingRequestTypeDef,
    DescribeTimeBasedAutoScalingResultTypeDef,
    DescribeUserProfilesRequestTypeDef,
    DescribeUserProfilesResultTypeDef,
    DescribeVolumesRequestTypeDef,
    DescribeVolumesResultTypeDef,
    DetachElasticLoadBalancerRequestTypeDef,
    DisassociateElasticIpRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetHostnameSuggestionRequestTypeDef,
    GetHostnameSuggestionResultTypeDef,
    GrantAccessRequestTypeDef,
    GrantAccessResultTypeDef,
    ListTagsRequestTypeDef,
    ListTagsResultTypeDef,
    RebootInstanceRequestTypeDef,
    RegisterEcsClusterRequestTypeDef,
    RegisterEcsClusterResultTypeDef,
    RegisterElasticIpRequestTypeDef,
    RegisterElasticIpResultTypeDef,
    RegisterInstanceRequestTypeDef,
    RegisterInstanceResultTypeDef,
    RegisterRdsDbInstanceRequestTypeDef,
    RegisterVolumeRequestTypeDef,
    RegisterVolumeResultTypeDef,
    SetLoadBasedAutoScalingRequestTypeDef,
    SetPermissionRequestTypeDef,
    SetTimeBasedAutoScalingRequestTypeDef,
    StartInstanceRequestTypeDef,
    StartStackRequestTypeDef,
    StopInstanceRequestTypeDef,
    StopStackRequestTypeDef,
    TagResourceRequestTypeDef,
    UnassignInstanceRequestTypeDef,
    UnassignVolumeRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAppRequestTypeDef,
    UpdateElasticIpRequestTypeDef,
    UpdateInstanceRequestTypeDef,
    UpdateLayerRequestTypeDef,
    UpdateMyUserProfileRequestTypeDef,
    UpdateRdsDbInstanceRequestTypeDef,
    UpdateStackRequestTypeDef,
    UpdateUserProfileRequestTypeDef,
    UpdateVolumeRequestTypeDef,
)
from .waiter import (
    AppExistsWaiter,
    DeploymentSuccessfulWaiter,
    InstanceOnlineWaiter,
    InstanceRegisteredWaiter,
    InstanceStoppedWaiter,
    InstanceTerminatedWaiter,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("OpsWorksClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class OpsWorksClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OpsWorksClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#generate_presigned_url)
        """

    async def assign_instance(
        self, **kwargs: Unpack[AssignInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assign a registered instance to a layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/assign_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#assign_instance)
        """

    async def assign_volume(
        self, **kwargs: Unpack[AssignVolumeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns one of the stack's registered Amazon EBS volumes to a specified
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/assign_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#assign_volume)
        """

    async def associate_elastic_ip(
        self, **kwargs: Unpack[AssociateElasticIpRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates one of the stack's registered Elastic IP addresses with a specified
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/associate_elastic_ip.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#associate_elastic_ip)
        """

    async def attach_elastic_load_balancer(
        self, **kwargs: Unpack[AttachElasticLoadBalancerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches an Elastic Load Balancing load balancer to a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/attach_elastic_load_balancer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#attach_elastic_load_balancer)
        """

    async def clone_stack(
        self, **kwargs: Unpack[CloneStackRequestTypeDef]
    ) -> CloneStackResultTypeDef:
        """
        Creates a clone of a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/clone_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#clone_stack)
        """

    async def create_app(self, **kwargs: Unpack[CreateAppRequestTypeDef]) -> CreateAppResultTypeDef:
        """
        Creates an app for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#create_app)
        """

    async def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentRequestTypeDef]
    ) -> CreateDeploymentResultTypeDef:
        """
        Runs deployment or stack commands.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#create_deployment)
        """

    async def create_instance(
        self, **kwargs: Unpack[CreateInstanceRequestTypeDef]
    ) -> CreateInstanceResultTypeDef:
        """
        Creates an instance in a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#create_instance)
        """

    async def create_layer(
        self, **kwargs: Unpack[CreateLayerRequestTypeDef]
    ) -> CreateLayerResultTypeDef:
        """
        Creates a layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_layer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#create_layer)
        """

    async def create_stack(
        self, **kwargs: Unpack[CreateStackRequestTypeDef]
    ) -> CreateStackResultTypeDef:
        """
        Creates a new stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#create_stack)
        """

    async def create_user_profile(
        self, **kwargs: Unpack[CreateUserProfileRequestTypeDef]
    ) -> CreateUserProfileResultTypeDef:
        """
        Creates a new user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_user_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#create_user_profile)
        """

    async def delete_app(
        self, **kwargs: Unpack[DeleteAppRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#delete_app)
        """

    async def delete_instance(
        self, **kwargs: Unpack[DeleteInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified instance, which terminates the associated Amazon EC2
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#delete_instance)
        """

    async def delete_layer(
        self, **kwargs: Unpack[DeleteLayerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_layer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#delete_layer)
        """

    async def delete_stack(
        self, **kwargs: Unpack[DeleteStackRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#delete_stack)
        """

    async def delete_user_profile(
        self, **kwargs: Unpack[DeleteUserProfileRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_user_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#delete_user_profile)
        """

    async def deregister_ecs_cluster(
        self, **kwargs: Unpack[DeregisterEcsClusterRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters a specified Amazon ECS cluster from a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_ecs_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#deregister_ecs_cluster)
        """

    async def deregister_elastic_ip(
        self, **kwargs: Unpack[DeregisterElasticIpRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters a specified Elastic IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_elastic_ip.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#deregister_elastic_ip)
        """

    async def deregister_instance(
        self, **kwargs: Unpack[DeregisterInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregister an instance from OpsWorks Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#deregister_instance)
        """

    async def deregister_rds_db_instance(
        self, **kwargs: Unpack[DeregisterRdsDbInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters an Amazon RDS instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_rds_db_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#deregister_rds_db_instance)
        """

    async def deregister_volume(
        self, **kwargs: Unpack[DeregisterVolumeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters an Amazon EBS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#deregister_volume)
        """

    async def describe_agent_versions(
        self, **kwargs: Unpack[DescribeAgentVersionsRequestTypeDef]
    ) -> DescribeAgentVersionsResultTypeDef:
        """
        Describes the available OpsWorks Stacks agent versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_agent_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_agent_versions)
        """

    async def describe_apps(
        self, **kwargs: Unpack[DescribeAppsRequestTypeDef]
    ) -> DescribeAppsResultTypeDef:
        """
        Requests a description of a specified set of apps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_apps.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_apps)
        """

    async def describe_commands(
        self, **kwargs: Unpack[DescribeCommandsRequestTypeDef]
    ) -> DescribeCommandsResultTypeDef:
        """
        Describes the results of specified commands.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_commands.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_commands)
        """

    async def describe_deployments(
        self, **kwargs: Unpack[DescribeDeploymentsRequestTypeDef]
    ) -> DescribeDeploymentsResultTypeDef:
        """
        Requests a description of a specified set of deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_deployments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_deployments)
        """

    async def describe_ecs_clusters(
        self, **kwargs: Unpack[DescribeEcsClustersRequestTypeDef]
    ) -> DescribeEcsClustersResultTypeDef:
        """
        Describes Amazon ECS clusters that are registered with a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_ecs_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_ecs_clusters)
        """

    async def describe_elastic_ips(
        self, **kwargs: Unpack[DescribeElasticIpsRequestTypeDef]
    ) -> DescribeElasticIpsResultTypeDef:
        """
        Describes <a
        href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html">Elastic
        IP addresses</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_elastic_ips.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_elastic_ips)
        """

    async def describe_elastic_load_balancers(
        self, **kwargs: Unpack[DescribeElasticLoadBalancersRequestTypeDef]
    ) -> DescribeElasticLoadBalancersResultTypeDef:
        """
        Describes a stack's Elastic Load Balancing instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_elastic_load_balancers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_elastic_load_balancers)
        """

    async def describe_instances(
        self, **kwargs: Unpack[DescribeInstancesRequestTypeDef]
    ) -> DescribeInstancesResultTypeDef:
        """
        Requests a description of a set of instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_instances)
        """

    async def describe_layers(
        self, **kwargs: Unpack[DescribeLayersRequestTypeDef]
    ) -> DescribeLayersResultTypeDef:
        """
        Requests a description of one or more layers in a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_layers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_layers)
        """

    async def describe_load_based_auto_scaling(
        self, **kwargs: Unpack[DescribeLoadBasedAutoScalingRequestTypeDef]
    ) -> DescribeLoadBasedAutoScalingResultTypeDef:
        """
        Describes load-based auto scaling configurations for specified layers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_load_based_auto_scaling.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_load_based_auto_scaling)
        """

    async def describe_my_user_profile(self) -> DescribeMyUserProfileResultTypeDef:
        """
        Describes a user's SSH information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_my_user_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_my_user_profile)
        """

    async def describe_operating_systems(self) -> DescribeOperatingSystemsResponseTypeDef:
        """
        Describes the operating systems that are supported by OpsWorks Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_operating_systems.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_operating_systems)
        """

    async def describe_permissions(
        self, **kwargs: Unpack[DescribePermissionsRequestTypeDef]
    ) -> DescribePermissionsResultTypeDef:
        """
        Describes the permissions for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_permissions)
        """

    async def describe_raid_arrays(
        self, **kwargs: Unpack[DescribeRaidArraysRequestTypeDef]
    ) -> DescribeRaidArraysResultTypeDef:
        """
        Describe an instance's RAID arrays.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_raid_arrays.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_raid_arrays)
        """

    async def describe_rds_db_instances(
        self, **kwargs: Unpack[DescribeRdsDbInstancesRequestTypeDef]
    ) -> DescribeRdsDbInstancesResultTypeDef:
        """
        Describes Amazon RDS instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_rds_db_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_rds_db_instances)
        """

    async def describe_service_errors(
        self, **kwargs: Unpack[DescribeServiceErrorsRequestTypeDef]
    ) -> DescribeServiceErrorsResultTypeDef:
        """
        Describes OpsWorks Stacks service errors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_service_errors.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_service_errors)
        """

    async def describe_stack_provisioning_parameters(
        self, **kwargs: Unpack[DescribeStackProvisioningParametersRequestTypeDef]
    ) -> DescribeStackProvisioningParametersResultTypeDef:
        """
        Requests a description of a stack's provisioning parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_stack_provisioning_parameters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_stack_provisioning_parameters)
        """

    async def describe_stack_summary(
        self, **kwargs: Unpack[DescribeStackSummaryRequestTypeDef]
    ) -> DescribeStackSummaryResultTypeDef:
        """
        Describes the number of layers and apps in a specified stack, and the number of
        instances in each state, such as <code>running_setup</code> or
        <code>online</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_stack_summary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_stack_summary)
        """

    async def describe_stacks(
        self, **kwargs: Unpack[DescribeStacksRequestTypeDef]
    ) -> DescribeStacksResultTypeDef:
        """
        Requests a description of one or more stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_stacks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_stacks)
        """

    async def describe_time_based_auto_scaling(
        self, **kwargs: Unpack[DescribeTimeBasedAutoScalingRequestTypeDef]
    ) -> DescribeTimeBasedAutoScalingResultTypeDef:
        """
        Describes time-based auto scaling configurations for specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_time_based_auto_scaling.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_time_based_auto_scaling)
        """

    async def describe_user_profiles(
        self, **kwargs: Unpack[DescribeUserProfilesRequestTypeDef]
    ) -> DescribeUserProfilesResultTypeDef:
        """
        Describe specified users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_user_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_user_profiles)
        """

    async def describe_volumes(
        self, **kwargs: Unpack[DescribeVolumesRequestTypeDef]
    ) -> DescribeVolumesResultTypeDef:
        """
        Describes an instance's Amazon EBS volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_volumes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#describe_volumes)
        """

    async def detach_elastic_load_balancer(
        self, **kwargs: Unpack[DetachElasticLoadBalancerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a specified Elastic Load Balancing instance from its layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/detach_elastic_load_balancer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#detach_elastic_load_balancer)
        """

    async def disassociate_elastic_ip(
        self, **kwargs: Unpack[DisassociateElasticIpRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates an Elastic IP address from its instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/disassociate_elastic_ip.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#disassociate_elastic_ip)
        """

    async def get_hostname_suggestion(
        self, **kwargs: Unpack[GetHostnameSuggestionRequestTypeDef]
    ) -> GetHostnameSuggestionResultTypeDef:
        """
        Gets a generated host name for the specified layer, based on the current host
        name theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_hostname_suggestion.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#get_hostname_suggestion)
        """

    async def grant_access(
        self, **kwargs: Unpack[GrantAccessRequestTypeDef]
    ) -> GrantAccessResultTypeDef:
        """
        This action can be used only with Windows stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/grant_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#grant_access)
        """

    async def list_tags(self, **kwargs: Unpack[ListTagsRequestTypeDef]) -> ListTagsResultTypeDef:
        """
        Returns a list of tags that are applied to the specified stack or layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/list_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#list_tags)
        """

    async def reboot_instance(
        self, **kwargs: Unpack[RebootInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Reboots a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/reboot_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#reboot_instance)
        """

    async def register_ecs_cluster(
        self, **kwargs: Unpack[RegisterEcsClusterRequestTypeDef]
    ) -> RegisterEcsClusterResultTypeDef:
        """
        Registers a specified Amazon ECS cluster with a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_ecs_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#register_ecs_cluster)
        """

    async def register_elastic_ip(
        self, **kwargs: Unpack[RegisterElasticIpRequestTypeDef]
    ) -> RegisterElasticIpResultTypeDef:
        """
        Registers an Elastic IP address with a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_elastic_ip.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#register_elastic_ip)
        """

    async def register_instance(
        self, **kwargs: Unpack[RegisterInstanceRequestTypeDef]
    ) -> RegisterInstanceResultTypeDef:
        """
        Registers instances that were created outside of OpsWorks Stacks with a
        specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#register_instance)
        """

    async def register_rds_db_instance(
        self, **kwargs: Unpack[RegisterRdsDbInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers an Amazon RDS instance with a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_rds_db_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#register_rds_db_instance)
        """

    async def register_volume(
        self, **kwargs: Unpack[RegisterVolumeRequestTypeDef]
    ) -> RegisterVolumeResultTypeDef:
        """
        Registers an Amazon EBS volume with a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#register_volume)
        """

    async def set_load_based_auto_scaling(
        self, **kwargs: Unpack[SetLoadBasedAutoScalingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the load-based auto scaling configuration for a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/set_load_based_auto_scaling.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#set_load_based_auto_scaling)
        """

    async def set_permission(
        self, **kwargs: Unpack[SetPermissionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specifies a user's permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/set_permission.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#set_permission)
        """

    async def set_time_based_auto_scaling(
        self, **kwargs: Unpack[SetTimeBasedAutoScalingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the time-based auto scaling configuration for a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/set_time_based_auto_scaling.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#set_time_based_auto_scaling)
        """

    async def start_instance(
        self, **kwargs: Unpack[StartInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/start_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#start_instance)
        """

    async def start_stack(
        self, **kwargs: Unpack[StartStackRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a stack's instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/start_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#start_stack)
        """

    async def stop_instance(
        self, **kwargs: Unpack[StopInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/stop_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#stop_instance)
        """

    async def stop_stack(
        self, **kwargs: Unpack[StopStackRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/stop_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#stop_stack)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Apply cost-allocation tags to a specified stack or layer in OpsWorks Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#tag_resource)
        """

    async def unassign_instance(
        self, **kwargs: Unpack[UnassignInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Unassigns a registered instance from all layers that are using the instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/unassign_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#unassign_instance)
        """

    async def unassign_volume(
        self, **kwargs: Unpack[UnassignVolumeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Unassigns an assigned Amazon EBS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/unassign_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#unassign_volume)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from a specified stack or layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#untag_resource)
        """

    async def update_app(
        self, **kwargs: Unpack[UpdateAppRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#update_app)
        """

    async def update_elastic_ip(
        self, **kwargs: Unpack[UpdateElasticIpRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a registered Elastic IP address's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_elastic_ip.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#update_elastic_ip)
        """

    async def update_instance(
        self, **kwargs: Unpack[UpdateInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#update_instance)
        """

    async def update_layer(
        self, **kwargs: Unpack[UpdateLayerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_layer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#update_layer)
        """

    async def update_my_user_profile(
        self, **kwargs: Unpack[UpdateMyUserProfileRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a user's SSH public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_my_user_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#update_my_user_profile)
        """

    async def update_rds_db_instance(
        self, **kwargs: Unpack[UpdateRdsDbInstanceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon RDS instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_rds_db_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#update_rds_db_instance)
        """

    async def update_stack(
        self, **kwargs: Unpack[UpdateStackRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#update_stack)
        """

    async def update_user_profile(
        self, **kwargs: Unpack[UpdateUserProfileRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_user_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#update_user_profile)
        """

    async def update_volume(
        self, **kwargs: Unpack[UpdateVolumeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon EBS volume's name or mount point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#update_volume)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_ecs_clusters"]
    ) -> DescribeEcsClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["app_exists"]
    ) -> AppExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["deployment_successful"]
    ) -> DeploymentSuccessfulWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["instance_online"]
    ) -> InstanceOnlineWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["instance_registered"]
    ) -> InstanceRegisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["instance_stopped"]
    ) -> InstanceStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["instance_terminated"]
    ) -> InstanceTerminatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/client/)
        """
