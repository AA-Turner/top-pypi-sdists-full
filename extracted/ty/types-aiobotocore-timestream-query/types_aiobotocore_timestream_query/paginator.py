"""
Type annotations for timestream-query service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_timestream_query.client import TimestreamQueryClient
    from types_aiobotocore_timestream_query.paginator import (
        ListScheduledQueriesPaginator,
        ListTagsForResourcePaginator,
        QueryPaginator,
    )

    session = get_session()
    with session.create_client("timestream-query") as client:
        client: TimestreamQueryClient

        list_scheduled_queries_paginator: ListScheduledQueriesPaginator = client.get_paginator("list_scheduled_queries")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        query_paginator: QueryPaginator = client.get_paginator("query")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListScheduledQueriesRequestPaginateTypeDef,
    ListScheduledQueriesResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    QueryRequestPaginateTypeDef,
    QueryResponsePaginatorTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListScheduledQueriesPaginator", "ListTagsForResourcePaginator", "QueryPaginator")


if TYPE_CHECKING:
    _ListScheduledQueriesPaginatorBase = AioPaginator[ListScheduledQueriesResponseTypeDef]
else:
    _ListScheduledQueriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListScheduledQueriesPaginator(_ListScheduledQueriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/ListScheduledQueries.html#TimestreamQuery.Paginator.ListScheduledQueries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators/#listscheduledqueriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScheduledQueriesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListScheduledQueriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/ListScheduledQueries.html#TimestreamQuery.Paginator.ListScheduledQueries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators/#listscheduledqueriespaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/ListTagsForResource.html#TimestreamQuery.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/ListTagsForResource.html#TimestreamQuery.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _QueryPaginatorBase = AioPaginator[QueryResponsePaginatorTypeDef]
else:
    _QueryPaginatorBase = AioPaginator  # type: ignore[assignment]


class QueryPaginator(_QueryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/Query.html#TimestreamQuery.Paginator.Query)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators/#querypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[QueryRequestPaginateTypeDef]
    ) -> AioPageIterator[QueryResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query/paginator/Query.html#TimestreamQuery.Paginator.Query.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/paginators/#querypaginator)
        """
