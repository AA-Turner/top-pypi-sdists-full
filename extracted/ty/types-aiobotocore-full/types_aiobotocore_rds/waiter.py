"""
Type annotations for rds service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rds.client import RDSClient
    from types_aiobotocore_rds.waiter import (
        DBClusterAvailableWaiter,
        DBClusterDeletedWaiter,
        DBClusterSnapshotAvailableWaiter,
        DBClusterSnapshotDeletedWaiter,
        DBInstanceAvailableWaiter,
        DBInstanceDeletedWaiter,
        DBSnapshotAvailableWaiter,
        DBSnapshotCompletedWaiter,
        DBSnapshotDeletedWaiter,
        TenantDatabaseAvailableWaiter,
        TenantDatabaseDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("rds") as client:
        client: RDSClient

        db_cluster_available_waiter: DBClusterAvailableWaiter = client.get_waiter("db_cluster_available")
        db_cluster_deleted_waiter: DBClusterDeletedWaiter = client.get_waiter("db_cluster_deleted")
        db_cluster_snapshot_available_waiter: DBClusterSnapshotAvailableWaiter = client.get_waiter("db_cluster_snapshot_available")
        db_cluster_snapshot_deleted_waiter: DBClusterSnapshotDeletedWaiter = client.get_waiter("db_cluster_snapshot_deleted")
        db_instance_available_waiter: DBInstanceAvailableWaiter = client.get_waiter("db_instance_available")
        db_instance_deleted_waiter: DBInstanceDeletedWaiter = client.get_waiter("db_instance_deleted")
        db_snapshot_available_waiter: DBSnapshotAvailableWaiter = client.get_waiter("db_snapshot_available")
        db_snapshot_completed_waiter: DBSnapshotCompletedWaiter = client.get_waiter("db_snapshot_completed")
        db_snapshot_deleted_waiter: DBSnapshotDeletedWaiter = client.get_waiter("db_snapshot_deleted")
        tenant_database_available_waiter: TenantDatabaseAvailableWaiter = client.get_waiter("tenant_database_available")
        tenant_database_deleted_waiter: TenantDatabaseDeletedWaiter = client.get_waiter("tenant_database_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeDBClustersMessageWaitExtraTypeDef,
    DescribeDBClustersMessageWaitTypeDef,
    DescribeDBClusterSnapshotsMessageWaitExtraTypeDef,
    DescribeDBClusterSnapshotsMessageWaitTypeDef,
    DescribeDBInstancesMessageWaitExtraTypeDef,
    DescribeDBInstancesMessageWaitTypeDef,
    DescribeDBSnapshotsMessageWaitExtraExtraTypeDef,
    DescribeDBSnapshotsMessageWaitExtraTypeDef,
    DescribeDBSnapshotsMessageWaitTypeDef,
    DescribeTenantDatabasesMessageWaitExtraTypeDef,
    DescribeTenantDatabasesMessageWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DBClusterAvailableWaiter",
    "DBClusterDeletedWaiter",
    "DBClusterSnapshotAvailableWaiter",
    "DBClusterSnapshotDeletedWaiter",
    "DBInstanceAvailableWaiter",
    "DBInstanceDeletedWaiter",
    "DBSnapshotAvailableWaiter",
    "DBSnapshotCompletedWaiter",
    "DBSnapshotDeletedWaiter",
    "TenantDatabaseAvailableWaiter",
    "TenantDatabaseDeletedWaiter",
)


class DBClusterAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterAvailable.html#RDS.Waiter.DBClusterAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclusteravailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClustersMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterAvailable.html#RDS.Waiter.DBClusterAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclusteravailablewaiter)
        """


class DBClusterDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterDeleted.html#RDS.Waiter.DBClusterDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclusterdeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClustersMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterDeleted.html#RDS.Waiter.DBClusterDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclusterdeletedwaiter)
        """


class DBClusterSnapshotAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterSnapshotAvailable.html#RDS.Waiter.DBClusterSnapshotAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclustersnapshotavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterSnapshotsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterSnapshotAvailable.html#RDS.Waiter.DBClusterSnapshotAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclustersnapshotavailablewaiter)
        """


class DBClusterSnapshotDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterSnapshotDeleted.html#RDS.Waiter.DBClusterSnapshotDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclustersnapshotdeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterSnapshotsMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterSnapshotDeleted.html#RDS.Waiter.DBClusterSnapshotDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclustersnapshotdeletedwaiter)
        """


class DBInstanceAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBInstanceAvailable.html#RDS.Waiter.DBInstanceAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbinstanceavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBInstancesMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBInstanceAvailable.html#RDS.Waiter.DBInstanceAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbinstanceavailablewaiter)
        """


class DBInstanceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBInstanceDeleted.html#RDS.Waiter.DBInstanceDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbinstancedeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBInstancesMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBInstanceDeleted.html#RDS.Waiter.DBInstanceDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbinstancedeletedwaiter)
        """


class DBSnapshotAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotAvailable.html#RDS.Waiter.DBSnapshotAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBSnapshotsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotAvailable.html#RDS.Waiter.DBSnapshotAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotavailablewaiter)
        """


class DBSnapshotCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotCompleted.html#RDS.Waiter.DBSnapshotCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBSnapshotsMessageWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotCompleted.html#RDS.Waiter.DBSnapshotCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotcompletedwaiter)
        """


class DBSnapshotDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotDeleted.html#RDS.Waiter.DBSnapshotDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotdeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBSnapshotsMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotDeleted.html#RDS.Waiter.DBSnapshotDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotdeletedwaiter)
        """


class TenantDatabaseAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/TenantDatabaseAvailable.html#RDS.Waiter.TenantDatabaseAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#tenantdatabaseavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTenantDatabasesMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/TenantDatabaseAvailable.html#RDS.Waiter.TenantDatabaseAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#tenantdatabaseavailablewaiter)
        """


class TenantDatabaseDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/TenantDatabaseDeleted.html#RDS.Waiter.TenantDatabaseDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#tenantdatabasedeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTenantDatabasesMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/TenantDatabaseDeleted.html#RDS.Waiter.TenantDatabaseDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#tenantdatabasedeletedwaiter)
        """
