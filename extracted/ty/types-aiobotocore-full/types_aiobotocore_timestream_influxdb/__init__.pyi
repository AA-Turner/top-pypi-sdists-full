"""
Main interface for timestream-influxdb service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_timestream_influxdb import (
        Client,
        ListDbClustersPaginator,
        ListDbInstancesForClusterPaginator,
        ListDbInstancesPaginator,
        ListDbParameterGroupsPaginator,
        TimestreamInfluxDBClient,
    )

    session = get_session()
    async with session.create_client("timestream-influxdb") as client:
        client: TimestreamInfluxDBClient
        ...


    list_db_clusters_paginator: ListDbClustersPaginator = client.get_paginator("list_db_clusters")
    list_db_instances_for_cluster_paginator: ListDbInstancesForClusterPaginator = client.get_paginator("list_db_instances_for_cluster")
    list_db_instances_paginator: ListDbInstancesPaginator = client.get_paginator("list_db_instances")
    list_db_parameter_groups_paginator: ListDbParameterGroupsPaginator = client.get_paginator("list_db_parameter_groups")
    ```
"""

from .client import TimestreamInfluxDBClient
from .paginator import (
    ListDbClustersPaginator,
    ListDbInstancesForClusterPaginator,
    ListDbInstancesPaginator,
    ListDbParameterGroupsPaginator,
)

Client = TimestreamInfluxDBClient

__all__ = (
    "Client",
    "ListDbClustersPaginator",
    "ListDbInstancesForClusterPaginator",
    "ListDbInstancesPaginator",
    "ListDbParameterGroupsPaginator",
    "TimestreamInfluxDBClient",
)
