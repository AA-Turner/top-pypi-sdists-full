"""
Type annotations for servicediscovery service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_servicediscovery.client import ServiceDiscoveryClient

    session = get_session()
    async with session.create_client("servicediscovery") as client:
        client: ServiceDiscoveryClient
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
    ListInstancesPaginator,
    ListNamespacesPaginator,
    ListOperationsPaginator,
    ListServicesPaginator,
)
from .type_defs import (
    CreateHttpNamespaceRequestTypeDef,
    CreateHttpNamespaceResponseTypeDef,
    CreatePrivateDnsNamespaceRequestTypeDef,
    CreatePrivateDnsNamespaceResponseTypeDef,
    CreatePublicDnsNamespaceRequestTypeDef,
    CreatePublicDnsNamespaceResponseTypeDef,
    CreateServiceRequestTypeDef,
    CreateServiceResponseTypeDef,
    DeleteNamespaceRequestTypeDef,
    DeleteNamespaceResponseTypeDef,
    DeleteServiceAttributesRequestTypeDef,
    DeleteServiceRequestTypeDef,
    DeregisterInstanceRequestTypeDef,
    DeregisterInstanceResponseTypeDef,
    DiscoverInstancesRequestTypeDef,
    DiscoverInstancesResponseTypeDef,
    DiscoverInstancesRevisionRequestTypeDef,
    DiscoverInstancesRevisionResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetInstanceRequestTypeDef,
    GetInstanceResponseTypeDef,
    GetInstancesHealthStatusRequestTypeDef,
    GetInstancesHealthStatusResponseTypeDef,
    GetNamespaceRequestTypeDef,
    GetNamespaceResponseTypeDef,
    GetOperationRequestTypeDef,
    GetOperationResponseTypeDef,
    GetServiceAttributesRequestTypeDef,
    GetServiceAttributesResponseTypeDef,
    GetServiceRequestTypeDef,
    GetServiceResponseTypeDef,
    ListInstancesRequestTypeDef,
    ListInstancesResponseTypeDef,
    ListNamespacesRequestTypeDef,
    ListNamespacesResponseTypeDef,
    ListOperationsRequestTypeDef,
    ListOperationsResponseTypeDef,
    ListServicesRequestTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterInstanceRequestTypeDef,
    RegisterInstanceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateHttpNamespaceRequestTypeDef,
    UpdateHttpNamespaceResponseTypeDef,
    UpdateInstanceCustomHealthStatusRequestTypeDef,
    UpdatePrivateDnsNamespaceRequestTypeDef,
    UpdatePrivateDnsNamespaceResponseTypeDef,
    UpdatePublicDnsNamespaceRequestTypeDef,
    UpdatePublicDnsNamespaceResponseTypeDef,
    UpdateServiceAttributesRequestTypeDef,
    UpdateServiceRequestTypeDef,
    UpdateServiceResponseTypeDef,
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


__all__ = ("ServiceDiscoveryClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    CustomHealthNotFound: Type[BotocoreClientError]
    DuplicateRequest: Type[BotocoreClientError]
    InstanceNotFound: Type[BotocoreClientError]
    InvalidInput: Type[BotocoreClientError]
    NamespaceAlreadyExists: Type[BotocoreClientError]
    NamespaceNotFound: Type[BotocoreClientError]
    OperationNotFound: Type[BotocoreClientError]
    RequestLimitExceeded: Type[BotocoreClientError]
    ResourceInUse: Type[BotocoreClientError]
    ResourceLimitExceeded: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceAlreadyExists: Type[BotocoreClientError]
    ServiceAttributesLimitExceededException: Type[BotocoreClientError]
    ServiceNotFound: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class ServiceDiscoveryClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ServiceDiscoveryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#generate_presigned_url)
        """

    async def create_http_namespace(
        self, **kwargs: Unpack[CreateHttpNamespaceRequestTypeDef]
    ) -> CreateHttpNamespaceResponseTypeDef:
        """
        Creates an HTTP namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/create_http_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#create_http_namespace)
        """

    async def create_private_dns_namespace(
        self, **kwargs: Unpack[CreatePrivateDnsNamespaceRequestTypeDef]
    ) -> CreatePrivateDnsNamespaceResponseTypeDef:
        """
        Creates a private namespace based on DNS, which is visible only inside a
        specified Amazon VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/create_private_dns_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#create_private_dns_namespace)
        """

    async def create_public_dns_namespace(
        self, **kwargs: Unpack[CreatePublicDnsNamespaceRequestTypeDef]
    ) -> CreatePublicDnsNamespaceResponseTypeDef:
        """
        Creates a public namespace based on DNS, which is visible on the internet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/create_public_dns_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#create_public_dns_namespace)
        """

    async def create_service(
        self, **kwargs: Unpack[CreateServiceRequestTypeDef]
    ) -> CreateServiceResponseTypeDef:
        """
        Creates a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/create_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#create_service)
        """

    async def delete_namespace(
        self, **kwargs: Unpack[DeleteNamespaceRequestTypeDef]
    ) -> DeleteNamespaceResponseTypeDef:
        """
        Deletes a namespace from the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/delete_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#delete_namespace)
        """

    async def delete_service(self, **kwargs: Unpack[DeleteServiceRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a specified service and all associated service attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/delete_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#delete_service)
        """

    async def delete_service_attributes(
        self, **kwargs: Unpack[DeleteServiceAttributesRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes specific attributes associated with a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/delete_service_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#delete_service_attributes)
        """

    async def deregister_instance(
        self, **kwargs: Unpack[DeregisterInstanceRequestTypeDef]
    ) -> DeregisterInstanceResponseTypeDef:
        """
        Deletes the Amazon Route 53 DNS records and health check, if any, that Cloud
        Map created for the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/deregister_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#deregister_instance)
        """

    async def discover_instances(
        self, **kwargs: Unpack[DiscoverInstancesRequestTypeDef]
    ) -> DiscoverInstancesResponseTypeDef:
        """
        Discovers registered instances for a specified namespace and service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/discover_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#discover_instances)
        """

    async def discover_instances_revision(
        self, **kwargs: Unpack[DiscoverInstancesRevisionRequestTypeDef]
    ) -> DiscoverInstancesRevisionResponseTypeDef:
        """
        Discovers the increasing revision associated with an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/discover_instances_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#discover_instances_revision)
        """

    async def get_instance(
        self, **kwargs: Unpack[GetInstanceRequestTypeDef]
    ) -> GetInstanceResponseTypeDef:
        """
        Gets information about a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_instance)
        """

    async def get_instances_health_status(
        self, **kwargs: Unpack[GetInstancesHealthStatusRequestTypeDef]
    ) -> GetInstancesHealthStatusResponseTypeDef:
        """
        Gets the current health status (<code>Healthy</code>, <code>Unhealthy</code>,
        or <code>Unknown</code>) of one or more instances that are associated with a
        specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_instances_health_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_instances_health_status)
        """

    async def get_namespace(
        self, **kwargs: Unpack[GetNamespaceRequestTypeDef]
    ) -> GetNamespaceResponseTypeDef:
        """
        Gets information about a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_namespace)
        """

    async def get_operation(
        self, **kwargs: Unpack[GetOperationRequestTypeDef]
    ) -> GetOperationResponseTypeDef:
        """
        Gets information about any operation that returns an operation ID in the
        response, such as a <code>CreateHttpNamespace</code> request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_operation)
        """

    async def get_service(
        self, **kwargs: Unpack[GetServiceRequestTypeDef]
    ) -> GetServiceResponseTypeDef:
        """
        Gets the settings for a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_service)
        """

    async def get_service_attributes(
        self, **kwargs: Unpack[GetServiceAttributesRequestTypeDef]
    ) -> GetServiceAttributesResponseTypeDef:
        """
        Returns the attributes associated with a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_service_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_service_attributes)
        """

    async def list_instances(
        self, **kwargs: Unpack[ListInstancesRequestTypeDef]
    ) -> ListInstancesResponseTypeDef:
        """
        Lists summary information about the instances that you registered by using a
        specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#list_instances)
        """

    async def list_namespaces(
        self, **kwargs: Unpack[ListNamespacesRequestTypeDef]
    ) -> ListNamespacesResponseTypeDef:
        """
        Lists summary information about the namespaces that were created by the current
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_namespaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#list_namespaces)
        """

    async def list_operations(
        self, **kwargs: Unpack[ListOperationsRequestTypeDef]
    ) -> ListOperationsResponseTypeDef:
        """
        Lists operations that match the criteria that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_operations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#list_operations)
        """

    async def list_services(
        self, **kwargs: Unpack[ListServicesRequestTypeDef]
    ) -> ListServicesResponseTypeDef:
        """
        Lists summary information for all the services that are associated with one or
        more namespaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#list_services)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#list_tags_for_resource)
        """

    async def register_instance(
        self, **kwargs: Unpack[RegisterInstanceRequestTypeDef]
    ) -> RegisterInstanceResponseTypeDef:
        """
        Creates or updates one or more records and, optionally, creates a health check
        based on the settings in a specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/register_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#register_instance)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#untag_resource)
        """

    async def update_http_namespace(
        self, **kwargs: Unpack[UpdateHttpNamespaceRequestTypeDef]
    ) -> UpdateHttpNamespaceResponseTypeDef:
        """
        Updates an HTTP namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_http_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#update_http_namespace)
        """

    async def update_instance_custom_health_status(
        self, **kwargs: Unpack[UpdateInstanceCustomHealthStatusRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Submits a request to change the health status of a custom health check to
        healthy or unhealthy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_instance_custom_health_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#update_instance_custom_health_status)
        """

    async def update_private_dns_namespace(
        self, **kwargs: Unpack[UpdatePrivateDnsNamespaceRequestTypeDef]
    ) -> UpdatePrivateDnsNamespaceResponseTypeDef:
        """
        Updates a private DNS namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_private_dns_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#update_private_dns_namespace)
        """

    async def update_public_dns_namespace(
        self, **kwargs: Unpack[UpdatePublicDnsNamespaceRequestTypeDef]
    ) -> UpdatePublicDnsNamespaceResponseTypeDef:
        """
        Updates a public DNS namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_public_dns_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#update_public_dns_namespace)
        """

    async def update_service(
        self, **kwargs: Unpack[UpdateServiceRequestTypeDef]
    ) -> UpdateServiceResponseTypeDef:
        """
        Submits a request to perform the following operations:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#update_service)
        """

    async def update_service_attributes(
        self, **kwargs: Unpack[UpdateServiceAttributesRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Submits a request to update a specified service to add service-level attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/update_service_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#update_service_attributes)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_instances"]
    ) -> ListInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_namespaces"]
    ) -> ListNamespacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_operations"]
    ) -> ListOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_services"]
    ) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicediscovery/client/)
        """
