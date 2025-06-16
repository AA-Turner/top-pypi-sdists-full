"""
Type annotations for elasticache service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elasticache.client import ElastiCacheClient
    from types_aiobotocore_elasticache.waiter import (
        CacheClusterAvailableWaiter,
        CacheClusterDeletedWaiter,
        ReplicationGroupAvailableWaiter,
        ReplicationGroupDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("elasticache") as client:
        client: ElastiCacheClient

        cache_cluster_available_waiter: CacheClusterAvailableWaiter = client.get_waiter("cache_cluster_available")
        cache_cluster_deleted_waiter: CacheClusterDeletedWaiter = client.get_waiter("cache_cluster_deleted")
        replication_group_available_waiter: ReplicationGroupAvailableWaiter = client.get_waiter("replication_group_available")
        replication_group_deleted_waiter: ReplicationGroupDeletedWaiter = client.get_waiter("replication_group_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeCacheClustersMessageWaitExtraTypeDef,
    DescribeCacheClustersMessageWaitTypeDef,
    DescribeReplicationGroupsMessageWaitExtraTypeDef,
    DescribeReplicationGroupsMessageWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "CacheClusterAvailableWaiter",
    "CacheClusterDeletedWaiter",
    "ReplicationGroupAvailableWaiter",
    "ReplicationGroupDeletedWaiter",
)

class CacheClusterAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/waiter/CacheClusterAvailable.html#ElastiCache.Waiter.CacheClusterAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/waiters/#cacheclusteravailablewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCacheClustersMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/waiter/CacheClusterAvailable.html#ElastiCache.Waiter.CacheClusterAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/waiters/#cacheclusteravailablewaiter)
        """

class CacheClusterDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/waiter/CacheClusterDeleted.html#ElastiCache.Waiter.CacheClusterDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/waiters/#cacheclusterdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCacheClustersMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/waiter/CacheClusterDeleted.html#ElastiCache.Waiter.CacheClusterDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/waiters/#cacheclusterdeletedwaiter)
        """

class ReplicationGroupAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/waiter/ReplicationGroupAvailable.html#ElastiCache.Waiter.ReplicationGroupAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/waiters/#replicationgroupavailablewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationGroupsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/waiter/ReplicationGroupAvailable.html#ElastiCache.Waiter.ReplicationGroupAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/waiters/#replicationgroupavailablewaiter)
        """

class ReplicationGroupDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/waiter/ReplicationGroupDeleted.html#ElastiCache.Waiter.ReplicationGroupDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/waiters/#replicationgroupdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationGroupsMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/waiter/ReplicationGroupDeleted.html#ElastiCache.Waiter.ReplicationGroupDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/waiters/#replicationgroupdeletedwaiter)
        """
