"""
Main interface for elementalinference service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_elementalinference import (
        Client,
        ElementalInferenceClient,
        FeedDeletedWaiter,
        ListDictionariesPaginator,
        ListFeedsPaginator,
    )

    session = get_session()
    async with session.create_client("elementalinference") as client:
        client: ElementalInferenceClient
        ...


    feed_deleted_waiter: FeedDeletedWaiter = client.get_waiter("feed_deleted")

    list_dictionaries_paginator: ListDictionariesPaginator = client.get_paginator("list_dictionaries")
    list_feeds_paginator: ListFeedsPaginator = client.get_paginator("list_feeds")
    ```
"""

from .client import ElementalInferenceClient
from .paginator import ListDictionariesPaginator, ListFeedsPaginator
from .waiter import FeedDeletedWaiter

Client = ElementalInferenceClient


__all__ = (
    "Client",
    "ElementalInferenceClient",
    "FeedDeletedWaiter",
    "ListDictionariesPaginator",
    "ListFeedsPaginator",
)
