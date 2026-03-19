"""
Main interface for connecthealth service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connecthealth import (
        Client,
        ConnectHealthClient,
        ListDomainsPaginator,
        ListSubscriptionsPaginator,
    )

    session = get_session()
    async with session.create_client("connecthealth") as client:
        client: ConnectHealthClient
        ...


    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from .client import ConnectHealthClient
from .paginator import ListDomainsPaginator, ListSubscriptionsPaginator

Client = ConnectHealthClient


__all__ = ("Client", "ConnectHealthClient", "ListDomainsPaginator", "ListSubscriptionsPaginator")
