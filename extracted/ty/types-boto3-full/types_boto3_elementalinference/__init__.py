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
        ListFeedsPaginator,
    )

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")

    feed_deleted_waiter: FeedDeletedWaiter = client.get_waiter("feed_deleted")

    list_feeds_paginator: ListFeedsPaginator = client.get_paginator("list_feeds")
    ```
"""

from .client import ElementalInferenceClient
from .paginator import ListFeedsPaginator
from .waiter import FeedDeletedWaiter

Client = ElementalInferenceClient


__all__ = ("Client", "ElementalInferenceClient", "FeedDeletedWaiter", "ListFeedsPaginator")
