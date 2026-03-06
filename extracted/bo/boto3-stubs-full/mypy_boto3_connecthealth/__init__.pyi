"""
Main interface for connecthealth service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connecthealth/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_connecthealth import (
        Client,
        ConnectHealthClient,
        ListDomainsPaginator,
        ListSubscriptionsPaginator,
    )

    session = Session()
    client: ConnectHealthClient = session.client("connecthealth")

    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from .client import ConnectHealthClient
from .paginator import ListDomainsPaginator, ListSubscriptionsPaginator

Client = ConnectHealthClient

__all__ = ("Client", "ConnectHealthClient", "ListDomainsPaginator", "ListSubscriptionsPaginator")
