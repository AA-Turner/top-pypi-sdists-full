"""
Type annotations for docdb service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_docdb.client import DocDBClient
    from types_aiobotocore_docdb.waiter import (
        DBInstanceAvailableWaiter,
        DBInstanceDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("docdb") as client:
        client: DocDBClient

        db_instance_available_waiter: DBInstanceAvailableWaiter = client.get_waiter("db_instance_available")
        db_instance_deleted_waiter: DBInstanceDeletedWaiter = client.get_waiter("db_instance_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeDBInstancesMessageWaitExtraTypeDef,
    DescribeDBInstancesMessageWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DBInstanceAvailableWaiter", "DBInstanceDeletedWaiter")

class DBInstanceAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/waiter/DBInstanceAvailable.html#DocDB.Waiter.DBInstanceAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/waiters/#dbinstanceavailablewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBInstancesMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/waiter/DBInstanceAvailable.html#DocDB.Waiter.DBInstanceAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/waiters/#dbinstanceavailablewaiter)
        """

class DBInstanceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/waiter/DBInstanceDeleted.html#DocDB.Waiter.DBInstanceDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/waiters/#dbinstancedeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBInstancesMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/waiter/DBInstanceDeleted.html#DocDB.Waiter.DBInstanceDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/waiters/#dbinstancedeletedwaiter)
        """
