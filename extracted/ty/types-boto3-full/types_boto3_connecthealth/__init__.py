"""
Main interface for connecthealth service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connecthealth/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_connecthealth import (
        Client,
        ConnectHealthClient,
        ListDatasetsPaginator,
        ListDomainsPaginator,
        ListSubscriptionsPaginator,
    )

    session = Session()
    client: ConnectHealthClient = session.client("connecthealth")

    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from .client import ConnectHealthClient
from .paginator import ListDatasetsPaginator, ListDomainsPaginator, ListSubscriptionsPaginator

Client = ConnectHealthClient


__all__ = (
    "Client",
    "ConnectHealthClient",
    "ListDatasetsPaginator",
    "ListDomainsPaginator",
    "ListSubscriptionsPaginator",
)
