"""
Main interface for elementalinference service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_elementalinference import (
        Client,
        ElementalInferenceClient,
        FeedDeletedWaiter,
        ListDictionariesPaginator,
        ListFeedsPaginator,
    )

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")

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
