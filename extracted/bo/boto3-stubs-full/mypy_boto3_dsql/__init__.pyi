"""
Main interface for dsql service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dsql/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dsql import (
        AuroraDSQLClient,
        Client,
        ClusterActiveWaiter,
        ClusterNotExistsWaiter,
        ListClustersPaginator,
        ListStreamsPaginator,
        StreamActiveWaiter,
        StreamNotExistsWaiter,
    )

    session = Session()
    client: AuroraDSQLClient = session.client("dsql")

    cluster_active_waiter: ClusterActiveWaiter = client.get_waiter("cluster_active")
    cluster_not_exists_waiter: ClusterNotExistsWaiter = client.get_waiter("cluster_not_exists")
    stream_active_waiter: StreamActiveWaiter = client.get_waiter("stream_active")
    stream_not_exists_waiter: StreamNotExistsWaiter = client.get_waiter("stream_not_exists")

    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""

from .client import AuroraDSQLClient
from .paginator import ListClustersPaginator, ListStreamsPaginator
from .waiter import (
    ClusterActiveWaiter,
    ClusterNotExistsWaiter,
    StreamActiveWaiter,
    StreamNotExistsWaiter,
)

Client = AuroraDSQLClient

__all__ = (
    "AuroraDSQLClient",
    "Client",
    "ClusterActiveWaiter",
    "ClusterNotExistsWaiter",
    "ListClustersPaginator",
    "ListStreamsPaginator",
    "StreamActiveWaiter",
    "StreamNotExistsWaiter",
)
