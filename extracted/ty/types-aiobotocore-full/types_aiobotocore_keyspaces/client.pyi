"""
Type annotations for keyspaces service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_keyspaces.client import KeyspacesClient

    session = get_session()
    async with session.create_client("keyspaces") as client:
        client: KeyspacesClient
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
    ListKeyspacesPaginator,
    ListTablesPaginator,
    ListTagsForResourcePaginator,
    ListTypesPaginator,
)
from .type_defs import (
    CreateKeyspaceRequestTypeDef,
    CreateKeyspaceResponseTypeDef,
    CreateTableRequestTypeDef,
    CreateTableResponseTypeDef,
    CreateTypeRequestTypeDef,
    CreateTypeResponseTypeDef,
    DeleteKeyspaceRequestTypeDef,
    DeleteTableRequestTypeDef,
    DeleteTypeRequestTypeDef,
    DeleteTypeResponseTypeDef,
    GetKeyspaceRequestTypeDef,
    GetKeyspaceResponseTypeDef,
    GetTableAutoScalingSettingsRequestTypeDef,
    GetTableAutoScalingSettingsResponseTypeDef,
    GetTableRequestTypeDef,
    GetTableResponseTypeDef,
    GetTypeRequestTypeDef,
    GetTypeResponseTypeDef,
    ListKeyspacesRequestTypeDef,
    ListKeyspacesResponseTypeDef,
    ListTablesRequestTypeDef,
    ListTablesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypesRequestTypeDef,
    ListTypesResponseTypeDef,
    RestoreTableRequestTypeDef,
    RestoreTableResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateKeyspaceRequestTypeDef,
    UpdateKeyspaceResponseTypeDef,
    UpdateTableRequestTypeDef,
    UpdateTableResponseTypeDef,
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

__all__ = ("KeyspacesClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class KeyspacesClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KeyspacesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#generate_presigned_url)
        """

    async def create_keyspace(
        self, **kwargs: Unpack[CreateKeyspaceRequestTypeDef]
    ) -> CreateKeyspaceResponseTypeDef:
        """
        The <code>CreateKeyspace</code> operation adds a new keyspace to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/create_keyspace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#create_keyspace)
        """

    async def create_table(
        self, **kwargs: Unpack[CreateTableRequestTypeDef]
    ) -> CreateTableResponseTypeDef:
        """
        The <code>CreateTable</code> operation adds a new table to the specified
        keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/create_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#create_table)
        """

    async def create_type(
        self, **kwargs: Unpack[CreateTypeRequestTypeDef]
    ) -> CreateTypeResponseTypeDef:
        """
        The <code>CreateType</code> operation creates a new user-defined type in the
        specified keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/create_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#create_type)
        """

    async def delete_keyspace(
        self, **kwargs: Unpack[DeleteKeyspaceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The <code>DeleteKeyspace</code> operation deletes a keyspace and all of its
        tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/delete_keyspace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#delete_keyspace)
        """

    async def delete_table(self, **kwargs: Unpack[DeleteTableRequestTypeDef]) -> Dict[str, Any]:
        """
        The <code>DeleteTable</code> operation deletes a table and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/delete_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#delete_table)
        """

    async def delete_type(
        self, **kwargs: Unpack[DeleteTypeRequestTypeDef]
    ) -> DeleteTypeResponseTypeDef:
        """
        The <code>DeleteType</code> operation deletes a user-defined type (UDT).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/delete_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#delete_type)
        """

    async def get_keyspace(
        self, **kwargs: Unpack[GetKeyspaceRequestTypeDef]
    ) -> GetKeyspaceResponseTypeDef:
        """
        Returns the name of the specified keyspace, the Amazon Resource Name (ARN), the
        replication strategy, the Amazon Web Services Regions of a multi-Region
        keyspace, and the status of newly added Regions after an
        <code>UpdateKeyspace</code> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_keyspace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#get_keyspace)
        """

    async def get_table(self, **kwargs: Unpack[GetTableRequestTypeDef]) -> GetTableResponseTypeDef:
        """
        Returns information about the table, including the table's name and current
        status, the keyspace name, configuration settings, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#get_table)
        """

    async def get_table_auto_scaling_settings(
        self, **kwargs: Unpack[GetTableAutoScalingSettingsRequestTypeDef]
    ) -> GetTableAutoScalingSettingsResponseTypeDef:
        """
        Returns auto scaling related settings of the specified table in JSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_table_auto_scaling_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#get_table_auto_scaling_settings)
        """

    async def get_type(self, **kwargs: Unpack[GetTypeRequestTypeDef]) -> GetTypeResponseTypeDef:
        """
        The <code>GetType</code> operation returns information about the type, for
        example the field definitions, the timestamp when the type was last modified,
        the level of nesting, the status, and details about if the type is used in
        other types and tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#get_type)
        """

    async def list_keyspaces(
        self, **kwargs: Unpack[ListKeyspacesRequestTypeDef]
    ) -> ListKeyspacesResponseTypeDef:
        """
        The <code>ListKeyspaces</code> operation returns a list of keyspaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/list_keyspaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#list_keyspaces)
        """

    async def list_tables(
        self, **kwargs: Unpack[ListTablesRequestTypeDef]
    ) -> ListTablesResponseTypeDef:
        """
        The <code>ListTables</code> operation returns a list of tables for a specified
        keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/list_tables.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#list_tables)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all tags associated with the specified Amazon Keyspaces
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#list_tags_for_resource)
        """

    async def list_types(
        self, **kwargs: Unpack[ListTypesRequestTypeDef]
    ) -> ListTypesResponseTypeDef:
        """
        The <code>ListTypes</code> operation returns a list of types for a specified
        keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/list_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#list_types)
        """

    async def restore_table(
        self, **kwargs: Unpack[RestoreTableRequestTypeDef]
    ) -> RestoreTableResponseTypeDef:
        """
        Restores the table to the specified point in time within the
        <code>earliest_restorable_timestamp</code> and the current time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/restore_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#restore_table)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates a set of tags with a Amazon Keyspaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the association of tags from a Amazon Keyspaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#untag_resource)
        """

    async def update_keyspace(
        self, **kwargs: Unpack[UpdateKeyspaceRequestTypeDef]
    ) -> UpdateKeyspaceResponseTypeDef:
        """
        Adds a new Amazon Web Services Region to the keyspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/update_keyspace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#update_keyspace)
        """

    async def update_table(
        self, **kwargs: Unpack[UpdateTableRequestTypeDef]
    ) -> UpdateTableResponseTypeDef:
        """
        Adds new columns to the table or updates one of the table's settings, for
        example capacity mode, auto scaling, encryption, point-in-time recovery, or ttl
        settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/update_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#update_table)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_keyspaces"]
    ) -> ListKeyspacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tables"]
    ) -> ListTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_types"]
    ) -> ListTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces.html#Keyspaces.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/client/)
        """
