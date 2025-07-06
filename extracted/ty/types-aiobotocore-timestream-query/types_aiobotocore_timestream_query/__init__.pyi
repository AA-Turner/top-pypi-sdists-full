"""
Main interface for timestream-query service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_timestream_query import (
        Client,
        ListScheduledQueriesPaginator,
        ListTagsForResourcePaginator,
        QueryPaginator,
        TimestreamQueryClient,
    )

    session = get_session()
    async with session.create_client("timestream-query") as client:
        client: TimestreamQueryClient
        ...


    list_scheduled_queries_paginator: ListScheduledQueriesPaginator = client.get_paginator("list_scheduled_queries")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    query_paginator: QueryPaginator = client.get_paginator("query")
    ```
"""

from .client import TimestreamQueryClient
from .paginator import ListScheduledQueriesPaginator, ListTagsForResourcePaginator, QueryPaginator

Client = TimestreamQueryClient

__all__ = (
    "Client",
    "ListScheduledQueriesPaginator",
    "ListTagsForResourcePaginator",
    "QueryPaginator",
    "TimestreamQueryClient",
)
