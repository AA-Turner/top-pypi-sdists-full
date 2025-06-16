"""
Type annotations for dsql service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dsql.client import AuroraDSQLClient
    from types_aiobotocore_dsql.waiter import (
        ClusterActiveWaiter,
        ClusterNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("dsql") as client:
        client: AuroraDSQLClient

        cluster_active_waiter: ClusterActiveWaiter = client.get_waiter("cluster_active")
        cluster_not_exists_waiter: ClusterNotExistsWaiter = client.get_waiter("cluster_not_exists")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetClusterInputWaitExtraTypeDef, GetClusterInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ClusterActiveWaiter", "ClusterNotExistsWaiter")


class ClusterActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/waiter/ClusterActive.html#AuroraDSQL.Waiter.ClusterActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/waiters/#clusteractivewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetClusterInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/waiter/ClusterActive.html#AuroraDSQL.Waiter.ClusterActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/waiters/#clusteractivewaiter)
        """


class ClusterNotExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/waiter/ClusterNotExists.html#AuroraDSQL.Waiter.ClusterNotExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/waiters/#clusternotexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetClusterInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/waiter/ClusterNotExists.html#AuroraDSQL.Waiter.ClusterNotExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/waiters/#clusternotexistswaiter)
        """
