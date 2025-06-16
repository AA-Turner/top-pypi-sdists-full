"""
Main interface for dsql service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_dsql import (
        AuroraDSQLClient,
        Client,
        ClusterActiveWaiter,
        ClusterNotExistsWaiter,
        ListClustersPaginator,
    )

    session = get_session()
    async with session.create_client("dsql") as client:
        client: AuroraDSQLClient
        ...


    cluster_active_waiter: ClusterActiveWaiter = client.get_waiter("cluster_active")
    cluster_not_exists_waiter: ClusterNotExistsWaiter = client.get_waiter("cluster_not_exists")

    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    ```
"""

from .client import AuroraDSQLClient
from .paginator import ListClustersPaginator
from .waiter import ClusterActiveWaiter, ClusterNotExistsWaiter

Client = AuroraDSQLClient


__all__ = (
    "AuroraDSQLClient",
    "Client",
    "ClusterActiveWaiter",
    "ClusterNotExistsWaiter",
    "ListClustersPaginator",
)
