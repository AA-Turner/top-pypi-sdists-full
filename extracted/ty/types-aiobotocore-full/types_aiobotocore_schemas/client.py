"""
Type annotations for schemas service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_schemas.client import SchemasClient

    session = get_session()
    async with session.create_client("schemas") as client:
        client: SchemasClient
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
    ListDiscoverersPaginator,
    ListRegistriesPaginator,
    ListSchemasPaginator,
    ListSchemaVersionsPaginator,
    SearchSchemasPaginator,
)
from .type_defs import (
    CreateDiscovererRequestTypeDef,
    CreateDiscovererResponseTypeDef,
    CreateRegistryRequestTypeDef,
    CreateRegistryResponseTypeDef,
    CreateSchemaRequestTypeDef,
    CreateSchemaResponseTypeDef,
    DeleteDiscovererRequestTypeDef,
    DeleteRegistryRequestTypeDef,
    DeleteResourcePolicyRequestTypeDef,
    DeleteSchemaRequestTypeDef,
    DeleteSchemaVersionRequestTypeDef,
    DescribeCodeBindingRequestTypeDef,
    DescribeCodeBindingResponseTypeDef,
    DescribeDiscovererRequestTypeDef,
    DescribeDiscovererResponseTypeDef,
    DescribeRegistryRequestTypeDef,
    DescribeRegistryResponseTypeDef,
    DescribeSchemaRequestTypeDef,
    DescribeSchemaResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportSchemaRequestTypeDef,
    ExportSchemaResponseTypeDef,
    GetCodeBindingSourceRequestTypeDef,
    GetCodeBindingSourceResponseTypeDef,
    GetDiscoveredSchemaRequestTypeDef,
    GetDiscoveredSchemaResponseTypeDef,
    GetResourcePolicyRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    ListDiscoverersRequestTypeDef,
    ListDiscoverersResponseTypeDef,
    ListRegistriesRequestTypeDef,
    ListRegistriesResponseTypeDef,
    ListSchemasRequestTypeDef,
    ListSchemasResponseTypeDef,
    ListSchemaVersionsRequestTypeDef,
    ListSchemaVersionsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutCodeBindingRequestTypeDef,
    PutCodeBindingResponseTypeDef,
    PutResourcePolicyRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    SearchSchemasRequestTypeDef,
    SearchSchemasResponseTypeDef,
    StartDiscovererRequestTypeDef,
    StartDiscovererResponseTypeDef,
    StopDiscovererRequestTypeDef,
    StopDiscovererResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDiscovererRequestTypeDef,
    UpdateDiscovererResponseTypeDef,
    UpdateRegistryRequestTypeDef,
    UpdateRegistryResponseTypeDef,
    UpdateSchemaRequestTypeDef,
    UpdateSchemaResponseTypeDef,
)
from .waiter import CodeBindingExistsWaiter

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("SchemasClient",)


class Exceptions(BaseClientExceptions):
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    GoneException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    PreconditionFailedException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class SchemasClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas.html#Schemas.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SchemasClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas.html#Schemas.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#generate_presigned_url)
        """

    async def create_discoverer(
        self, **kwargs: Unpack[CreateDiscovererRequestTypeDef]
    ) -> CreateDiscovererResponseTypeDef:
        """
        Creates a discoverer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/create_discoverer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#create_discoverer)
        """

    async def create_registry(
        self, **kwargs: Unpack[CreateRegistryRequestTypeDef]
    ) -> CreateRegistryResponseTypeDef:
        """
        Creates a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/create_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#create_registry)
        """

    async def create_schema(
        self, **kwargs: Unpack[CreateSchemaRequestTypeDef]
    ) -> CreateSchemaResponseTypeDef:
        """
        Creates a schema definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/create_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#create_schema)
        """

    async def delete_discoverer(
        self, **kwargs: Unpack[DeleteDiscovererRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a discoverer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/delete_discoverer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#delete_discoverer)
        """

    async def delete_registry(
        self, **kwargs: Unpack[DeleteRegistryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/delete_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#delete_registry)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the resource-based policy attached to the specified registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/delete_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#delete_resource_policy)
        """

    async def delete_schema(
        self, **kwargs: Unpack[DeleteSchemaRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a schema definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/delete_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#delete_schema)
        """

    async def delete_schema_version(
        self, **kwargs: Unpack[DeleteSchemaVersionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the schema version definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/delete_schema_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#delete_schema_version)
        """

    async def describe_code_binding(
        self, **kwargs: Unpack[DescribeCodeBindingRequestTypeDef]
    ) -> DescribeCodeBindingResponseTypeDef:
        """
        Describe the code binding URI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/describe_code_binding.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#describe_code_binding)
        """

    async def describe_discoverer(
        self, **kwargs: Unpack[DescribeDiscovererRequestTypeDef]
    ) -> DescribeDiscovererResponseTypeDef:
        """
        Describes the discoverer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/describe_discoverer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#describe_discoverer)
        """

    async def describe_registry(
        self, **kwargs: Unpack[DescribeRegistryRequestTypeDef]
    ) -> DescribeRegistryResponseTypeDef:
        """
        Describes the registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/describe_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#describe_registry)
        """

    async def describe_schema(
        self, **kwargs: Unpack[DescribeSchemaRequestTypeDef]
    ) -> DescribeSchemaResponseTypeDef:
        """
        Retrieve the schema definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/describe_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#describe_schema)
        """

    async def export_schema(
        self, **kwargs: Unpack[ExportSchemaRequestTypeDef]
    ) -> ExportSchemaResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/export_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#export_schema)
        """

    async def get_code_binding_source(
        self, **kwargs: Unpack[GetCodeBindingSourceRequestTypeDef]
    ) -> GetCodeBindingSourceResponseTypeDef:
        """
        Get the code binding source URI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/get_code_binding_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#get_code_binding_source)
        """

    async def get_discovered_schema(
        self, **kwargs: Unpack[GetDiscoveredSchemaRequestTypeDef]
    ) -> GetDiscoveredSchemaResponseTypeDef:
        """
        Get the discovered schema that was generated based on sampled events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/get_discovered_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#get_discovered_schema)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves the resource-based policy attached to a given registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/get_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#get_resource_policy)
        """

    async def list_discoverers(
        self, **kwargs: Unpack[ListDiscoverersRequestTypeDef]
    ) -> ListDiscoverersResponseTypeDef:
        """
        List the discoverers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/list_discoverers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#list_discoverers)
        """

    async def list_registries(
        self, **kwargs: Unpack[ListRegistriesRequestTypeDef]
    ) -> ListRegistriesResponseTypeDef:
        """
        List the registries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/list_registries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#list_registries)
        """

    async def list_schema_versions(
        self, **kwargs: Unpack[ListSchemaVersionsRequestTypeDef]
    ) -> ListSchemaVersionsResponseTypeDef:
        """
        Provides a list of the schema versions and related information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/list_schema_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#list_schema_versions)
        """

    async def list_schemas(
        self, **kwargs: Unpack[ListSchemasRequestTypeDef]
    ) -> ListSchemasResponseTypeDef:
        """
        List the schemas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/list_schemas.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#list_schemas)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Get tags for resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#list_tags_for_resource)
        """

    async def put_code_binding(
        self, **kwargs: Unpack[PutCodeBindingRequestTypeDef]
    ) -> PutCodeBindingResponseTypeDef:
        """
        Put code binding URI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/put_code_binding.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#put_code_binding)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        The name of the policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/put_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#put_resource_policy)
        """

    async def search_schemas(
        self, **kwargs: Unpack[SearchSchemasRequestTypeDef]
    ) -> SearchSchemasResponseTypeDef:
        """
        Search the schemas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/search_schemas.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#search_schemas)
        """

    async def start_discoverer(
        self, **kwargs: Unpack[StartDiscovererRequestTypeDef]
    ) -> StartDiscovererResponseTypeDef:
        """
        Starts the discoverer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/start_discoverer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#start_discoverer)
        """

    async def stop_discoverer(
        self, **kwargs: Unpack[StopDiscovererRequestTypeDef]
    ) -> StopDiscovererResponseTypeDef:
        """
        Stops the discoverer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/stop_discoverer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#stop_discoverer)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Add tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#untag_resource)
        """

    async def update_discoverer(
        self, **kwargs: Unpack[UpdateDiscovererRequestTypeDef]
    ) -> UpdateDiscovererResponseTypeDef:
        """
        Updates the discoverer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/update_discoverer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#update_discoverer)
        """

    async def update_registry(
        self, **kwargs: Unpack[UpdateRegistryRequestTypeDef]
    ) -> UpdateRegistryResponseTypeDef:
        """
        Updates a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/update_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#update_registry)
        """

    async def update_schema(
        self, **kwargs: Unpack[UpdateSchemaRequestTypeDef]
    ) -> UpdateSchemaResponseTypeDef:
        """
        Updates the schema definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/update_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#update_schema)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_discoverers"]
    ) -> ListDiscoverersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_registries"]
    ) -> ListRegistriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_schema_versions"]
    ) -> ListSchemaVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_schemas"]
    ) -> ListSchemasPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_schemas"]
    ) -> SearchSchemasPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["code_binding_exists"]
    ) -> CodeBindingExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas.html#Schemas.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas.html#Schemas.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/client/)
        """
