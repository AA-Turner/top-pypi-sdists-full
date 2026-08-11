"""
Main interface for elementalinference service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_elementalinference import (
        Client,
        ElementalInferenceClient,
        FeedDeletedWaiter,
        ListDictionariesPaginator,
        ListFeedsPaginator,
        SearchFixturesPaginator,
    )

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")

    feed_deleted_waiter: FeedDeletedWaiter = client.get_waiter("feed_deleted")

    list_dictionaries_paginator: ListDictionariesPaginator = client.get_paginator("list_dictionaries")
    list_feeds_paginator: ListFeedsPaginator = client.get_paginator("list_feeds")
    search_fixtures_paginator: SearchFixturesPaginator = client.get_paginator("search_fixtures")
    ```
"""

from .client import ElementalInferenceClient
from .paginator import ListDictionariesPaginator, ListFeedsPaginator, SearchFixturesPaginator
from .waiter import FeedDeletedWaiter

Client = ElementalInferenceClient


__all__ = (
    "Client",
    "ElementalInferenceClient",
    "FeedDeletedWaiter",
    "ListDictionariesPaginator",
    "ListFeedsPaginator",
    "SearchFixturesPaginator",
)
