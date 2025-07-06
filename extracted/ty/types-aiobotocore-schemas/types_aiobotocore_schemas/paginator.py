"""
Type annotations for schemas service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_schemas.client import SchemasClient
    from types_aiobotocore_schemas.paginator import (
        ListDiscoverersPaginator,
        ListRegistriesPaginator,
        ListSchemaVersionsPaginator,
        ListSchemasPaginator,
        SearchSchemasPaginator,
    )

    session = get_session()
    with session.create_client("schemas") as client:
        client: SchemasClient

        list_discoverers_paginator: ListDiscoverersPaginator = client.get_paginator("list_discoverers")
        list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
        list_schema_versions_paginator: ListSchemaVersionsPaginator = client.get_paginator("list_schema_versions")
        list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
        search_schemas_paginator: SearchSchemasPaginator = client.get_paginator("search_schemas")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDiscoverersRequestPaginateTypeDef,
    ListDiscoverersResponseTypeDef,
    ListRegistriesRequestPaginateTypeDef,
    ListRegistriesResponseTypeDef,
    ListSchemasRequestPaginateTypeDef,
    ListSchemasResponseTypeDef,
    ListSchemaVersionsRequestPaginateTypeDef,
    ListSchemaVersionsResponseTypeDef,
    SearchSchemasRequestPaginateTypeDef,
    SearchSchemasResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDiscoverersPaginator",
    "ListRegistriesPaginator",
    "ListSchemaVersionsPaginator",
    "ListSchemasPaginator",
    "SearchSchemasPaginator",
)


if TYPE_CHECKING:
    _ListDiscoverersPaginatorBase = AioPaginator[ListDiscoverersResponseTypeDef]
else:
    _ListDiscoverersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDiscoverersPaginator(_ListDiscoverersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListDiscoverers.html#Schemas.Paginator.ListDiscoverers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#listdiscovererspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDiscoverersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDiscoverersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListDiscoverers.html#Schemas.Paginator.ListDiscoverers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#listdiscovererspaginator)
        """


if TYPE_CHECKING:
    _ListRegistriesPaginatorBase = AioPaginator[ListRegistriesResponseTypeDef]
else:
    _ListRegistriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRegistriesPaginator(_ListRegistriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListRegistries.html#Schemas.Paginator.ListRegistries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#listregistriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistriesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListRegistries.html#Schemas.Paginator.ListRegistries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#listregistriespaginator)
        """


if TYPE_CHECKING:
    _ListSchemaVersionsPaginatorBase = AioPaginator[ListSchemaVersionsResponseTypeDef]
else:
    _ListSchemaVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSchemaVersionsPaginator(_ListSchemaVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListSchemaVersions.html#Schemas.Paginator.ListSchemaVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#listschemaversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchemaVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSchemaVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListSchemaVersions.html#Schemas.Paginator.ListSchemaVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#listschemaversionspaginator)
        """


if TYPE_CHECKING:
    _ListSchemasPaginatorBase = AioPaginator[ListSchemasResponseTypeDef]
else:
    _ListSchemasPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSchemasPaginator(_ListSchemasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListSchemas.html#Schemas.Paginator.ListSchemas)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#listschemaspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchemasRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/ListSchemas.html#Schemas.Paginator.ListSchemas.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#listschemaspaginator)
        """


if TYPE_CHECKING:
    _SearchSchemasPaginatorBase = AioPaginator[SearchSchemasResponseTypeDef]
else:
    _SearchSchemasPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchSchemasPaginator(_SearchSchemasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/SearchSchemas.html#Schemas.Paginator.SearchSchemas)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#searchschemaspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchSchemasRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas/paginator/SearchSchemas.html#Schemas.Paginator.SearchSchemas.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_schemas/paginators/#searchschemaspaginator)
        """
