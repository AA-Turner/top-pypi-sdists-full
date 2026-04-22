"""
Main interface for interconnect service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_interconnect import (
        Client,
        ConnectionAvailableWaiter,
        ConnectionDeletedWaiter,
        InterconnectClient,
        ListAttachPointsPaginator,
        ListConnectionsPaginator,
        ListEnvironmentsPaginator,
    )

    session = get_session()
    async with session.create_client("interconnect") as client:
        client: InterconnectClient
        ...


    connection_available_waiter: ConnectionAvailableWaiter = client.get_waiter("connection_available")
    connection_deleted_waiter: ConnectionDeletedWaiter = client.get_waiter("connection_deleted")

    list_attach_points_paginator: ListAttachPointsPaginator = client.get_paginator("list_attach_points")
    list_connections_paginator: ListConnectionsPaginator = client.get_paginator("list_connections")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

from .client import InterconnectClient
from .paginator import (
    ListAttachPointsPaginator,
    ListConnectionsPaginator,
    ListEnvironmentsPaginator,
)
from .waiter import ConnectionAvailableWaiter, ConnectionDeletedWaiter

Client = InterconnectClient


__all__ = (
    "Client",
    "ConnectionAvailableWaiter",
    "ConnectionDeletedWaiter",
    "InterconnectClient",
    "ListAttachPointsPaginator",
    "ListConnectionsPaginator",
    "ListEnvironmentsPaginator",
)
