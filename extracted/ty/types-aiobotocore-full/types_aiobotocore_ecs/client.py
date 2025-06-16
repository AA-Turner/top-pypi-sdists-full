"""
Type annotations for ecs service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ecs.client import ECSClient

    session = get_session()
    async with session.create_client("ecs") as client:
        client: ECSClient
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

from .paginator import (
    ListAccountSettingsPaginator,
    ListAttributesPaginator,
    ListClustersPaginator,
    ListContainerInstancesPaginator,
    ListServicesByNamespacePaginator,
    ListServicesPaginator,
    ListTaskDefinitionFamiliesPaginator,
    ListTaskDefinitionsPaginator,
    ListTasksPaginator,
)
from .type_defs import (
    CreateCapacityProviderRequestTypeDef,
    CreateCapacityProviderResponseTypeDef,
    CreateClusterRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateServiceRequestTypeDef,
    CreateServiceResponseTypeDef,
    CreateTaskSetRequestTypeDef,
    CreateTaskSetResponseTypeDef,
    DeleteAccountSettingRequestTypeDef,
    DeleteAccountSettingResponseTypeDef,
    DeleteAttributesRequestTypeDef,
    DeleteAttributesResponseTypeDef,
    DeleteCapacityProviderRequestTypeDef,
    DeleteCapacityProviderResponseTypeDef,
    DeleteClusterRequestTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteServiceRequestTypeDef,
    DeleteServiceResponseTypeDef,
    DeleteTaskDefinitionsRequestTypeDef,
    DeleteTaskDefinitionsResponseTypeDef,
    DeleteTaskSetRequestTypeDef,
    DeleteTaskSetResponseTypeDef,
    DeregisterContainerInstanceRequestTypeDef,
    DeregisterContainerInstanceResponseTypeDef,
    DeregisterTaskDefinitionRequestTypeDef,
    DeregisterTaskDefinitionResponseTypeDef,
    DescribeCapacityProvidersRequestTypeDef,
    DescribeCapacityProvidersResponseTypeDef,
    DescribeClustersRequestTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeContainerInstancesRequestTypeDef,
    DescribeContainerInstancesResponseTypeDef,
    DescribeServiceDeploymentsRequestTypeDef,
    DescribeServiceDeploymentsResponseTypeDef,
    DescribeServiceRevisionsRequestTypeDef,
    DescribeServiceRevisionsResponseTypeDef,
    DescribeServicesRequestTypeDef,
    DescribeServicesResponseTypeDef,
    DescribeTaskDefinitionRequestTypeDef,
    DescribeTaskDefinitionResponseTypeDef,
    DescribeTaskSetsRequestTypeDef,
    DescribeTaskSetsResponseTypeDef,
    DescribeTasksRequestTypeDef,
    DescribeTasksResponseTypeDef,
    DiscoverPollEndpointRequestTypeDef,
    DiscoverPollEndpointResponseTypeDef,
    ExecuteCommandRequestTypeDef,
    ExecuteCommandResponseTypeDef,
    GetTaskProtectionRequestTypeDef,
    GetTaskProtectionResponseTypeDef,
    ListAccountSettingsRequestTypeDef,
    ListAccountSettingsResponseTypeDef,
    ListAttributesRequestTypeDef,
    ListAttributesResponseTypeDef,
    ListClustersRequestTypeDef,
    ListClustersResponseTypeDef,
    ListContainerInstancesRequestTypeDef,
    ListContainerInstancesResponseTypeDef,
    ListServiceDeploymentsRequestTypeDef,
    ListServiceDeploymentsResponseTypeDef,
    ListServicesByNamespaceRequestTypeDef,
    ListServicesByNamespaceResponseTypeDef,
    ListServicesRequestTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTaskDefinitionFamiliesRequestTypeDef,
    ListTaskDefinitionFamiliesResponseTypeDef,
    ListTaskDefinitionsRequestTypeDef,
    ListTaskDefinitionsResponseTypeDef,
    ListTasksRequestTypeDef,
    ListTasksResponseTypeDef,
    PutAccountSettingDefaultRequestTypeDef,
    PutAccountSettingDefaultResponseTypeDef,
    PutAccountSettingRequestTypeDef,
    PutAccountSettingResponseTypeDef,
    PutAttributesRequestTypeDef,
    PutAttributesResponseTypeDef,
    PutClusterCapacityProvidersRequestTypeDef,
    PutClusterCapacityProvidersResponseTypeDef,
    RegisterContainerInstanceRequestTypeDef,
    RegisterContainerInstanceResponseTypeDef,
    RegisterTaskDefinitionRequestTypeDef,
    RegisterTaskDefinitionResponseTypeDef,
    RunTaskRequestTypeDef,
    RunTaskResponseTypeDef,
    StartTaskRequestTypeDef,
    StartTaskResponseTypeDef,
    StopServiceDeploymentRequestTypeDef,
    StopServiceDeploymentResponseTypeDef,
    StopTaskRequestTypeDef,
    StopTaskResponseTypeDef,
    SubmitAttachmentStateChangesRequestTypeDef,
    SubmitAttachmentStateChangesResponseTypeDef,
    SubmitContainerStateChangeRequestTypeDef,
    SubmitContainerStateChangeResponseTypeDef,
    SubmitTaskStateChangeRequestTypeDef,
    SubmitTaskStateChangeResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateCapacityProviderRequestTypeDef,
    UpdateCapacityProviderResponseTypeDef,
    UpdateClusterRequestTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateClusterSettingsRequestTypeDef,
    UpdateClusterSettingsResponseTypeDef,
    UpdateContainerAgentRequestTypeDef,
    UpdateContainerAgentResponseTypeDef,
    UpdateContainerInstancesStateRequestTypeDef,
    UpdateContainerInstancesStateResponseTypeDef,
    UpdateServicePrimaryTaskSetRequestTypeDef,
    UpdateServicePrimaryTaskSetResponseTypeDef,
    UpdateServiceRequestTypeDef,
    UpdateServiceResponseTypeDef,
    UpdateTaskProtectionRequestTypeDef,
    UpdateTaskProtectionResponseTypeDef,
    UpdateTaskSetRequestTypeDef,
    UpdateTaskSetResponseTypeDef,
)
from .waiter import (
    ServicesInactiveWaiter,
    ServicesStableWaiter,
    TasksRunningWaiter,
    TasksStoppedWaiter,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("ECSClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    AttributeLimitExceededException: Type[BotocoreClientError]
    BlockedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ClusterContainsContainerInstancesException: Type[BotocoreClientError]
    ClusterContainsServicesException: Type[BotocoreClientError]
    ClusterContainsTasksException: Type[BotocoreClientError]
    ClusterNotFoundException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MissingVersionException: Type[BotocoreClientError]
    NamespaceNotFoundException: Type[BotocoreClientError]
    NoUpdateAvailableException: Type[BotocoreClientError]
    PlatformTaskDefinitionIncompatibilityException: Type[BotocoreClientError]
    PlatformUnknownException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]
    ServiceDeploymentNotFoundException: Type[BotocoreClientError]
    ServiceNotActiveException: Type[BotocoreClientError]
    ServiceNotFoundException: Type[BotocoreClientError]
    TargetNotConnectedException: Type[BotocoreClientError]
    TargetNotFoundException: Type[BotocoreClientError]
    TaskSetNotFoundException: Type[BotocoreClientError]
    UnsupportedFeatureException: Type[BotocoreClientError]
    UpdateInProgressException: Type[BotocoreClientError]


class ECSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ECSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#generate_presigned_url)
        """

    async def create_capacity_provider(
        self, **kwargs: Unpack[CreateCapacityProviderRequestTypeDef]
    ) -> CreateCapacityProviderResponseTypeDef:
        """
        Creates a new capacity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/create_capacity_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#create_capacity_provider)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a new Amazon ECS cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/create_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#create_cluster)
        """

    async def create_service(
        self, **kwargs: Unpack[CreateServiceRequestTypeDef]
    ) -> CreateServiceResponseTypeDef:
        """
        Runs and maintains your desired number of tasks from a specified task
        definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/create_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#create_service)
        """

    async def create_task_set(
        self, **kwargs: Unpack[CreateTaskSetRequestTypeDef]
    ) -> CreateTaskSetResponseTypeDef:
        """
        Create a task set in the specified cluster and service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/create_task_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#create_task_set)
        """

    async def delete_account_setting(
        self, **kwargs: Unpack[DeleteAccountSettingRequestTypeDef]
    ) -> DeleteAccountSettingResponseTypeDef:
        """
        Disables an account setting for a specified user, role, or the root user for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_account_setting.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_account_setting)
        """

    async def delete_attributes(
        self, **kwargs: Unpack[DeleteAttributesRequestTypeDef]
    ) -> DeleteAttributesResponseTypeDef:
        """
        Deletes one or more custom attributes from an Amazon ECS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_attributes)
        """

    async def delete_capacity_provider(
        self, **kwargs: Unpack[DeleteCapacityProviderRequestTypeDef]
    ) -> DeleteCapacityProviderResponseTypeDef:
        """
        Deletes the specified capacity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_capacity_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_capacity_provider)
        """

    async def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterRequestTypeDef]
    ) -> DeleteClusterResponseTypeDef:
        """
        Deletes the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_cluster)
        """

    async def delete_service(
        self, **kwargs: Unpack[DeleteServiceRequestTypeDef]
    ) -> DeleteServiceResponseTypeDef:
        """
        Deletes a specified service within a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_service)
        """

    async def delete_task_definitions(
        self, **kwargs: Unpack[DeleteTaskDefinitionsRequestTypeDef]
    ) -> DeleteTaskDefinitionsResponseTypeDef:
        """
        Deletes one or more task definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_task_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_task_definitions)
        """

    async def delete_task_set(
        self, **kwargs: Unpack[DeleteTaskSetRequestTypeDef]
    ) -> DeleteTaskSetResponseTypeDef:
        """
        Deletes a specified task set within a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/delete_task_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_task_set)
        """

    async def deregister_container_instance(
        self, **kwargs: Unpack[DeregisterContainerInstanceRequestTypeDef]
    ) -> DeregisterContainerInstanceResponseTypeDef:
        """
        Deregisters an Amazon ECS container instance from the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/deregister_container_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#deregister_container_instance)
        """

    async def deregister_task_definition(
        self, **kwargs: Unpack[DeregisterTaskDefinitionRequestTypeDef]
    ) -> DeregisterTaskDefinitionResponseTypeDef:
        """
        Deregisters the specified task definition by family and revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/deregister_task_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#deregister_task_definition)
        """

    async def describe_capacity_providers(
        self, **kwargs: Unpack[DescribeCapacityProvidersRequestTypeDef]
    ) -> DescribeCapacityProvidersResponseTypeDef:
        """
        Describes one or more of your capacity providers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_capacity_providers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_capacity_providers)
        """

    async def describe_clusters(
        self, **kwargs: Unpack[DescribeClustersRequestTypeDef]
    ) -> DescribeClustersResponseTypeDef:
        """
        Describes one or more of your clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_clusters)
        """

    async def describe_container_instances(
        self, **kwargs: Unpack[DescribeContainerInstancesRequestTypeDef]
    ) -> DescribeContainerInstancesResponseTypeDef:
        """
        Describes one or more container instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_container_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_container_instances)
        """

    async def describe_service_deployments(
        self, **kwargs: Unpack[DescribeServiceDeploymentsRequestTypeDef]
    ) -> DescribeServiceDeploymentsResponseTypeDef:
        """
        Describes one or more of your service deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_service_deployments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_service_deployments)
        """

    async def describe_service_revisions(
        self, **kwargs: Unpack[DescribeServiceRevisionsRequestTypeDef]
    ) -> DescribeServiceRevisionsResponseTypeDef:
        """
        Describes one or more service revisions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_service_revisions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_service_revisions)
        """

    async def describe_services(
        self, **kwargs: Unpack[DescribeServicesRequestTypeDef]
    ) -> DescribeServicesResponseTypeDef:
        """
        Describes the specified services running in your cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_services)
        """

    async def describe_task_definition(
        self, **kwargs: Unpack[DescribeTaskDefinitionRequestTypeDef]
    ) -> DescribeTaskDefinitionResponseTypeDef:
        """
        Describes a task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_task_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_task_definition)
        """

    async def describe_task_sets(
        self, **kwargs: Unpack[DescribeTaskSetsRequestTypeDef]
    ) -> DescribeTaskSetsResponseTypeDef:
        """
        Describes the task sets in the specified cluster and service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_task_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_task_sets)
        """

    async def describe_tasks(
        self, **kwargs: Unpack[DescribeTasksRequestTypeDef]
    ) -> DescribeTasksResponseTypeDef:
        """
        Describes a specified task or tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/describe_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_tasks)
        """

    async def discover_poll_endpoint(
        self, **kwargs: Unpack[DiscoverPollEndpointRequestTypeDef]
    ) -> DiscoverPollEndpointResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/discover_poll_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#discover_poll_endpoint)
        """

    async def execute_command(
        self, **kwargs: Unpack[ExecuteCommandRequestTypeDef]
    ) -> ExecuteCommandResponseTypeDef:
        """
        Runs a command remotely on a container within a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/execute_command.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#execute_command)
        """

    async def get_task_protection(
        self, **kwargs: Unpack[GetTaskProtectionRequestTypeDef]
    ) -> GetTaskProtectionResponseTypeDef:
        """
        Retrieves the protection status of tasks in an Amazon ECS service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_task_protection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_task_protection)
        """

    async def list_account_settings(
        self, **kwargs: Unpack[ListAccountSettingsRequestTypeDef]
    ) -> ListAccountSettingsResponseTypeDef:
        """
        Lists the account settings for a specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_account_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_account_settings)
        """

    async def list_attributes(
        self, **kwargs: Unpack[ListAttributesRequestTypeDef]
    ) -> ListAttributesResponseTypeDef:
        """
        Lists the attributes for Amazon ECS resources within a specified target type
        and cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_attributes)
        """

    async def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestTypeDef]
    ) -> ListClustersResponseTypeDef:
        """
        Returns a list of existing clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_clusters)
        """

    async def list_container_instances(
        self, **kwargs: Unpack[ListContainerInstancesRequestTypeDef]
    ) -> ListContainerInstancesResponseTypeDef:
        """
        Returns a list of container instances in a specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_container_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_container_instances)
        """

    async def list_service_deployments(
        self, **kwargs: Unpack[ListServiceDeploymentsRequestTypeDef]
    ) -> ListServiceDeploymentsResponseTypeDef:
        """
        This operation lists all the service deployments that meet the specified filter
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_service_deployments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_service_deployments)
        """

    async def list_services(
        self, **kwargs: Unpack[ListServicesRequestTypeDef]
    ) -> ListServicesResponseTypeDef:
        """
        Returns a list of services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_services)
        """

    async def list_services_by_namespace(
        self, **kwargs: Unpack[ListServicesByNamespaceRequestTypeDef]
    ) -> ListServicesByNamespaceResponseTypeDef:
        """
        This operation lists all of the services that are associated with a Cloud Map
        namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_services_by_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_services_by_namespace)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for an Amazon ECS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_tags_for_resource)
        """

    async def list_task_definition_families(
        self, **kwargs: Unpack[ListTaskDefinitionFamiliesRequestTypeDef]
    ) -> ListTaskDefinitionFamiliesResponseTypeDef:
        """
        Returns a list of task definition families that are registered to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_task_definition_families.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_task_definition_families)
        """

    async def list_task_definitions(
        self, **kwargs: Unpack[ListTaskDefinitionsRequestTypeDef]
    ) -> ListTaskDefinitionsResponseTypeDef:
        """
        Returns a list of task definitions that are registered to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_task_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_task_definitions)
        """

    async def list_tasks(
        self, **kwargs: Unpack[ListTasksRequestTypeDef]
    ) -> ListTasksResponseTypeDef:
        """
        Returns a list of tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/list_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_tasks)
        """

    async def put_account_setting(
        self, **kwargs: Unpack[PutAccountSettingRequestTypeDef]
    ) -> PutAccountSettingResponseTypeDef:
        """
        Modifies an account setting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/put_account_setting.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#put_account_setting)
        """

    async def put_account_setting_default(
        self, **kwargs: Unpack[PutAccountSettingDefaultRequestTypeDef]
    ) -> PutAccountSettingDefaultResponseTypeDef:
        """
        Modifies an account setting for all users on an account for whom no individual
        account setting has been specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/put_account_setting_default.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#put_account_setting_default)
        """

    async def put_attributes(
        self, **kwargs: Unpack[PutAttributesRequestTypeDef]
    ) -> PutAttributesResponseTypeDef:
        """
        Create or update an attribute on an Amazon ECS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/put_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#put_attributes)
        """

    async def put_cluster_capacity_providers(
        self, **kwargs: Unpack[PutClusterCapacityProvidersRequestTypeDef]
    ) -> PutClusterCapacityProvidersResponseTypeDef:
        """
        Modifies the available capacity providers and the default capacity provider
        strategy for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/put_cluster_capacity_providers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#put_cluster_capacity_providers)
        """

    async def register_container_instance(
        self, **kwargs: Unpack[RegisterContainerInstanceRequestTypeDef]
    ) -> RegisterContainerInstanceResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/register_container_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#register_container_instance)
        """

    async def register_task_definition(
        self, **kwargs: Unpack[RegisterTaskDefinitionRequestTypeDef]
    ) -> RegisterTaskDefinitionResponseTypeDef:
        """
        Registers a new task definition from the supplied <code>family</code> and
        <code>containerDefinitions</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/register_task_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#register_task_definition)
        """

    async def run_task(self, **kwargs: Unpack[RunTaskRequestTypeDef]) -> RunTaskResponseTypeDef:
        """
        Starts a new task using the specified task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/run_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#run_task)
        """

    async def start_task(
        self, **kwargs: Unpack[StartTaskRequestTypeDef]
    ) -> StartTaskResponseTypeDef:
        """
        Starts a new task from the specified task definition on the specified container
        instance or instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/start_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#start_task)
        """

    async def stop_service_deployment(
        self, **kwargs: Unpack[StopServiceDeploymentRequestTypeDef]
    ) -> StopServiceDeploymentResponseTypeDef:
        """
        Stops an ongoing service deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/stop_service_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#stop_service_deployment)
        """

    async def stop_task(self, **kwargs: Unpack[StopTaskRequestTypeDef]) -> StopTaskResponseTypeDef:
        """
        Stops a running task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/stop_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#stop_task)
        """

    async def submit_attachment_state_changes(
        self, **kwargs: Unpack[SubmitAttachmentStateChangesRequestTypeDef]
    ) -> SubmitAttachmentStateChangesResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/submit_attachment_state_changes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#submit_attachment_state_changes)
        """

    async def submit_container_state_change(
        self, **kwargs: Unpack[SubmitContainerStateChangeRequestTypeDef]
    ) -> SubmitContainerStateChangeResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/submit_container_state_change.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#submit_container_state_change)
        """

    async def submit_task_state_change(
        self, **kwargs: Unpack[SubmitTaskStateChangeRequestTypeDef]
    ) -> SubmitTaskStateChangeResponseTypeDef:
        """
        This action is only used by the Amazon ECS agent, and it is not intended for
        use outside of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/submit_task_state_change.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#submit_task_state_change)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#untag_resource)
        """

    async def update_capacity_provider(
        self, **kwargs: Unpack[UpdateCapacityProviderRequestTypeDef]
    ) -> UpdateCapacityProviderResponseTypeDef:
        """
        Modifies the parameters for a capacity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_capacity_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_capacity_provider)
        """

    async def update_cluster(
        self, **kwargs: Unpack[UpdateClusterRequestTypeDef]
    ) -> UpdateClusterResponseTypeDef:
        """
        Updates the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_cluster)
        """

    async def update_cluster_settings(
        self, **kwargs: Unpack[UpdateClusterSettingsRequestTypeDef]
    ) -> UpdateClusterSettingsResponseTypeDef:
        """
        Modifies the settings to use for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_cluster_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_cluster_settings)
        """

    async def update_container_agent(
        self, **kwargs: Unpack[UpdateContainerAgentRequestTypeDef]
    ) -> UpdateContainerAgentResponseTypeDef:
        """
        Updates the Amazon ECS container agent on a specified container instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_container_agent.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_container_agent)
        """

    async def update_container_instances_state(
        self, **kwargs: Unpack[UpdateContainerInstancesStateRequestTypeDef]
    ) -> UpdateContainerInstancesStateResponseTypeDef:
        """
        Modifies the status of an Amazon ECS container instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_container_instances_state.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_container_instances_state)
        """

    async def update_service(
        self, **kwargs: Unpack[UpdateServiceRequestTypeDef]
    ) -> UpdateServiceResponseTypeDef:
        """
        Modifies the parameters of a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_service)
        """

    async def update_service_primary_task_set(
        self, **kwargs: Unpack[UpdateServicePrimaryTaskSetRequestTypeDef]
    ) -> UpdateServicePrimaryTaskSetResponseTypeDef:
        """
        Modifies which task set in a service is the primary task set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_service_primary_task_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_service_primary_task_set)
        """

    async def update_task_protection(
        self, **kwargs: Unpack[UpdateTaskProtectionRequestTypeDef]
    ) -> UpdateTaskProtectionResponseTypeDef:
        """
        Updates the protection status of a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_task_protection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_task_protection)
        """

    async def update_task_set(
        self, **kwargs: Unpack[UpdateTaskSetRequestTypeDef]
    ) -> UpdateTaskSetResponseTypeDef:
        """
        Modifies a task set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_task_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_task_set)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_account_settings"]
    ) -> ListAccountSettingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_attributes"]
    ) -> ListAttributesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_clusters"]
    ) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_container_instances"]
    ) -> ListContainerInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_services_by_namespace"]
    ) -> ListServicesByNamespacePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_services"]
    ) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_task_definition_families"]
    ) -> ListTaskDefinitionFamiliesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_task_definitions"]
    ) -> ListTaskDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tasks"]
    ) -> ListTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["services_inactive"]
    ) -> ServicesInactiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["services_stable"]
    ) -> ServicesStableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["tasks_running"]
    ) -> TasksRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["tasks_stopped"]
    ) -> TasksStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/)
        """
