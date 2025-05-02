"""
Type annotations for transfer service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_transfer.client import TransferClient
    from types_aiobotocore_transfer.waiter import (
        ServerOfflineWaiter,
        ServerOnlineWaiter,
    )

    session = get_session()
    async with session.create_client("transfer") as client:
        client: TransferClient

        server_offline_waiter: ServerOfflineWaiter = client.get_waiter("server_offline")
        server_online_waiter: ServerOnlineWaiter = client.get_waiter("server_online")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import DescribeServerRequestWaitExtraTypeDef, DescribeServerRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ServerOfflineWaiter", "ServerOnlineWaiter")

class ServerOfflineWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/waiter/ServerOffline.html#Transfer.Waiter.ServerOffline)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/waiters/#serverofflinewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServerRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/waiter/ServerOffline.html#Transfer.Waiter.ServerOffline.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/waiters/#serverofflinewaiter)
        """

class ServerOnlineWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/waiter/ServerOnline.html#Transfer.Waiter.ServerOnline)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/waiters/#serveronlinewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServerRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/waiter/ServerOnline.html#Transfer.Waiter.ServerOnline.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/waiters/#serveronlinewaiter)
        """
