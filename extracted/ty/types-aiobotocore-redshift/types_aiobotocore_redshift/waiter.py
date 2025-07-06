"""
Type annotations for redshift service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_redshift.client import RedshiftClient
    from types_aiobotocore_redshift.waiter import (
        ClusterAvailableWaiter,
        ClusterDeletedWaiter,
        ClusterRestoredWaiter,
        SnapshotAvailableWaiter,
    )

    session = get_session()
    async with session.create_client("redshift") as client:
        client: RedshiftClient

        cluster_available_waiter: ClusterAvailableWaiter = client.get_waiter("cluster_available")
        cluster_deleted_waiter: ClusterDeletedWaiter = client.get_waiter("cluster_deleted")
        cluster_restored_waiter: ClusterRestoredWaiter = client.get_waiter("cluster_restored")
        snapshot_available_waiter: SnapshotAvailableWaiter = client.get_waiter("snapshot_available")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeClustersMessageWaitExtraExtraTypeDef,
    DescribeClustersMessageWaitExtraTypeDef,
    DescribeClustersMessageWaitTypeDef,
    DescribeClusterSnapshotsMessageWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ClusterAvailableWaiter",
    "ClusterDeletedWaiter",
    "ClusterRestoredWaiter",
    "SnapshotAvailableWaiter",
)


class ClusterAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterAvailable.html#Redshift.Waiter.ClusterAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusteravailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClustersMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterAvailable.html#Redshift.Waiter.ClusterAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusteravailablewaiter)
        """


class ClusterDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterDeleted.html#Redshift.Waiter.ClusterDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusterdeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClustersMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterDeleted.html#Redshift.Waiter.ClusterDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusterdeletedwaiter)
        """


class ClusterRestoredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterRestored.html#Redshift.Waiter.ClusterRestored)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusterrestoredwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClustersMessageWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/ClusterRestored.html#Redshift.Waiter.ClusterRestored.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#clusterrestoredwaiter)
        """


class SnapshotAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/SnapshotAvailable.html#Redshift.Waiter.SnapshotAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#snapshotavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClusterSnapshotsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/waiter/SnapshotAvailable.html#Redshift.Waiter.SnapshotAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/waiters/#snapshotavailablewaiter)
        """
