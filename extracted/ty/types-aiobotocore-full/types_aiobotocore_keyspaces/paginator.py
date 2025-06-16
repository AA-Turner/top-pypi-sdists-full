"""
Type annotations for keyspaces service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_keyspaces.client import KeyspacesClient
    from types_aiobotocore_keyspaces.paginator import (
        ListKeyspacesPaginator,
        ListTablesPaginator,
        ListTagsForResourcePaginator,
        ListTypesPaginator,
    )

    session = get_session()
    with session.create_client("keyspaces") as client:
        client: KeyspacesClient

        list_keyspaces_paginator: ListKeyspacesPaginator = client.get_paginator("list_keyspaces")
        list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_types_paginator: ListTypesPaginator = client.get_paginator("list_types")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListKeyspacesRequestPaginateTypeDef,
    ListKeyspacesResponseTypeDef,
    ListTablesRequestPaginateTypeDef,
    ListTablesResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypesRequestPaginateTypeDef,
    ListTypesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListKeyspacesPaginator",
    "ListTablesPaginator",
    "ListTagsForResourcePaginator",
    "ListTypesPaginator",
)


if TYPE_CHECKING:
    _ListKeyspacesPaginatorBase = AioPaginator[ListKeyspacesResponseTypeDef]
else:
    _ListKeyspacesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListKeyspacesPaginator(_ListKeyspacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/paginator/ListKeyspaces.html#Keyspaces.Paginator.ListKeyspaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/paginators/#listkeyspacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKeyspacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKeyspacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/paginator/ListKeyspaces.html#Keyspaces.Paginator.ListKeyspaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/paginators/#listkeyspacespaginator)
        """


if TYPE_CHECKING:
    _ListTablesPaginatorBase = AioPaginator[ListTablesResponseTypeDef]
else:
    _ListTablesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTablesPaginator(_ListTablesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/paginator/ListTables.html#Keyspaces.Paginator.ListTables)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/paginators/#listtablespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTablesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTablesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/paginator/ListTables.html#Keyspaces.Paginator.ListTables.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/paginators/#listtablespaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/paginator/ListTagsForResource.html#Keyspaces.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/paginator/ListTagsForResource.html#Keyspaces.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _ListTypesPaginatorBase = AioPaginator[ListTypesResponseTypeDef]
else:
    _ListTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTypesPaginator(_ListTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/paginator/ListTypes.html#Keyspaces.Paginator.ListTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/paginators/#listtypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspaces/paginator/ListTypes.html#Keyspaces.Paginator.ListTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/paginators/#listtypespaginator)
        """
