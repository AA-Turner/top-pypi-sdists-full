"""
Main interface for memorydb service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_memorydb import (
        Client,
        DescribeACLsPaginator,
        DescribeClustersPaginator,
        DescribeEngineVersionsPaginator,
        DescribeEventsPaginator,
        DescribeMultiRegionClustersPaginator,
        DescribeParameterGroupsPaginator,
        DescribeParametersPaginator,
        DescribeReservedNodesOfferingsPaginator,
        DescribeReservedNodesPaginator,
        DescribeServiceUpdatesPaginator,
        DescribeSnapshotsPaginator,
        DescribeSubnetGroupsPaginator,
        DescribeUsersPaginator,
        MemoryDBClient,
    )

    session = get_session()
    async with session.create_client("memorydb") as client:
        client: MemoryDBClient
        ...


    describe_acls_paginator: DescribeACLsPaginator = client.get_paginator("describe_acls")
    describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
    describe_engine_versions_paginator: DescribeEngineVersionsPaginator = client.get_paginator("describe_engine_versions")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_multi_region_clusters_paginator: DescribeMultiRegionClustersPaginator = client.get_paginator("describe_multi_region_clusters")
    describe_parameter_groups_paginator: DescribeParameterGroupsPaginator = client.get_paginator("describe_parameter_groups")
    describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
    describe_reserved_nodes_offerings_paginator: DescribeReservedNodesOfferingsPaginator = client.get_paginator("describe_reserved_nodes_offerings")
    describe_reserved_nodes_paginator: DescribeReservedNodesPaginator = client.get_paginator("describe_reserved_nodes")
    describe_service_updates_paginator: DescribeServiceUpdatesPaginator = client.get_paginator("describe_service_updates")
    describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
    describe_subnet_groups_paginator: DescribeSubnetGroupsPaginator = client.get_paginator("describe_subnet_groups")
    describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
    ```
"""

from .client import MemoryDBClient
from .paginator import (
    DescribeACLsPaginator,
    DescribeClustersPaginator,
    DescribeEngineVersionsPaginator,
    DescribeEventsPaginator,
    DescribeMultiRegionClustersPaginator,
    DescribeParameterGroupsPaginator,
    DescribeParametersPaginator,
    DescribeReservedNodesOfferingsPaginator,
    DescribeReservedNodesPaginator,
    DescribeServiceUpdatesPaginator,
    DescribeSnapshotsPaginator,
    DescribeSubnetGroupsPaginator,
    DescribeUsersPaginator,
)

Client = MemoryDBClient


__all__ = (
    "Client",
    "DescribeACLsPaginator",
    "DescribeClustersPaginator",
    "DescribeEngineVersionsPaginator",
    "DescribeEventsPaginator",
    "DescribeMultiRegionClustersPaginator",
    "DescribeParameterGroupsPaginator",
    "DescribeParametersPaginator",
    "DescribeReservedNodesOfferingsPaginator",
    "DescribeReservedNodesPaginator",
    "DescribeServiceUpdatesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeSubnetGroupsPaginator",
    "DescribeUsersPaginator",
    "MemoryDBClient",
)
