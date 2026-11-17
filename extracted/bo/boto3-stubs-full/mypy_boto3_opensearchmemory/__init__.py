"""
Main interface for opensearchmemory service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_opensearchmemory import (
        Client,
        ListEventsPaginator,
        ListMemoriesPaginator,
        ListSpacesPaginator,
        OpenSearchMemoryClient,
        SearchEventsPaginator,
        SearchMemoriesPaginator,
        SpaceActiveWaiter,
        SpaceDeletedWaiter,
    )

    session = Session()
    client: OpenSearchMemoryClient = session.client("opensearchmemory")

    space_active_waiter: SpaceActiveWaiter = client.get_waiter("space_active")
    space_deleted_waiter: SpaceDeletedWaiter = client.get_waiter("space_deleted")

    list_events_paginator: ListEventsPaginator = client.get_paginator("list_events")
    list_memories_paginator: ListMemoriesPaginator = client.get_paginator("list_memories")
    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    search_events_paginator: SearchEventsPaginator = client.get_paginator("search_events")
    search_memories_paginator: SearchMemoriesPaginator = client.get_paginator("search_memories")
    ```
"""

from .client import OpenSearchMemoryClient
from .paginator import (
    ListEventsPaginator,
    ListMemoriesPaginator,
    ListSpacesPaginator,
    SearchEventsPaginator,
    SearchMemoriesPaginator,
)
from .waiter import SpaceActiveWaiter, SpaceDeletedWaiter

Client = OpenSearchMemoryClient


__all__ = (
    "Client",
    "ListEventsPaginator",
    "ListMemoriesPaginator",
    "ListSpacesPaginator",
    "OpenSearchMemoryClient",
    "SearchEventsPaginator",
    "SearchMemoriesPaginator",
    "SpaceActiveWaiter",
    "SpaceDeletedWaiter",
)
