"""
Type annotations for athena service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_athena.client import AthenaClient
    from types_aiobotocore_athena.paginator import (
        GetQueryResultsPaginator,
        ListDataCatalogsPaginator,
        ListDatabasesPaginator,
        ListNamedQueriesPaginator,
        ListQueryExecutionsPaginator,
        ListTableMetadataPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("athena") as client:
        client: AthenaClient

        get_query_results_paginator: GetQueryResultsPaginator = client.get_paginator("get_query_results")
        list_data_catalogs_paginator: ListDataCatalogsPaginator = client.get_paginator("list_data_catalogs")
        list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
        list_named_queries_paginator: ListNamedQueriesPaginator = client.get_paginator("list_named_queries")
        list_query_executions_paginator: ListQueryExecutionsPaginator = client.get_paginator("list_query_executions")
        list_table_metadata_paginator: ListTableMetadataPaginator = client.get_paginator("list_table_metadata")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetQueryResultsInputPaginateTypeDef,
    GetQueryResultsOutputTypeDef,
    ListDatabasesInputPaginateTypeDef,
    ListDatabasesOutputTypeDef,
    ListDataCatalogsInputPaginateTypeDef,
    ListDataCatalogsOutputTypeDef,
    ListNamedQueriesInputPaginateTypeDef,
    ListNamedQueriesOutputTypeDef,
    ListQueryExecutionsInputPaginateTypeDef,
    ListQueryExecutionsOutputTypeDef,
    ListTableMetadataInputPaginateTypeDef,
    ListTableMetadataOutputTypeDef,
    ListTagsForResourceInputPaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetQueryResultsPaginator",
    "ListDataCatalogsPaginator",
    "ListDatabasesPaginator",
    "ListNamedQueriesPaginator",
    "ListQueryExecutionsPaginator",
    "ListTableMetadataPaginator",
    "ListTagsForResourcePaginator",
)


if TYPE_CHECKING:
    _GetQueryResultsPaginatorBase = AioPaginator[GetQueryResultsOutputTypeDef]
else:
    _GetQueryResultsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetQueryResultsPaginator(_GetQueryResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/GetQueryResults.html#Athena.Paginator.GetQueryResults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#getqueryresultspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueryResultsInputPaginateTypeDef]
    ) -> AioPageIterator[GetQueryResultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/GetQueryResults.html#Athena.Paginator.GetQueryResults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#getqueryresultspaginator)
        """


if TYPE_CHECKING:
    _ListDataCatalogsPaginatorBase = AioPaginator[ListDataCatalogsOutputTypeDef]
else:
    _ListDataCatalogsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDataCatalogsPaginator(_ListDataCatalogsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListDataCatalogs.html#Athena.Paginator.ListDataCatalogs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listdatacatalogspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataCatalogsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDataCatalogsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListDataCatalogs.html#Athena.Paginator.ListDataCatalogs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listdatacatalogspaginator)
        """


if TYPE_CHECKING:
    _ListDatabasesPaginatorBase = AioPaginator[ListDatabasesOutputTypeDef]
else:
    _ListDatabasesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDatabasesPaginator(_ListDatabasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListDatabases.html#Athena.Paginator.ListDatabases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listdatabasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatabasesInputPaginateTypeDef]
    ) -> AioPageIterator[ListDatabasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListDatabases.html#Athena.Paginator.ListDatabases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listdatabasespaginator)
        """


if TYPE_CHECKING:
    _ListNamedQueriesPaginatorBase = AioPaginator[ListNamedQueriesOutputTypeDef]
else:
    _ListNamedQueriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNamedQueriesPaginator(_ListNamedQueriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListNamedQueries.html#Athena.Paginator.ListNamedQueries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listnamedqueriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNamedQueriesInputPaginateTypeDef]
    ) -> AioPageIterator[ListNamedQueriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListNamedQueries.html#Athena.Paginator.ListNamedQueries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listnamedqueriespaginator)
        """


if TYPE_CHECKING:
    _ListQueryExecutionsPaginatorBase = AioPaginator[ListQueryExecutionsOutputTypeDef]
else:
    _ListQueryExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQueryExecutionsPaginator(_ListQueryExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListQueryExecutions.html#Athena.Paginator.ListQueryExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listqueryexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueryExecutionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListQueryExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListQueryExecutions.html#Athena.Paginator.ListQueryExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listqueryexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListTableMetadataPaginatorBase = AioPaginator[ListTableMetadataOutputTypeDef]
else:
    _ListTableMetadataPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTableMetadataPaginator(_ListTableMetadataPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListTableMetadata.html#Athena.Paginator.ListTableMetadata)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listtablemetadatapaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTableMetadataInputPaginateTypeDef]
    ) -> AioPageIterator[ListTableMetadataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListTableMetadata.html#Athena.Paginator.ListTableMetadata.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listtablemetadatapaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceOutputTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListTagsForResource.html#Athena.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceInputPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/paginator/ListTagsForResource.html#Athena.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/paginators/#listtagsforresourcepaginator)
        """
