"""
Type annotations for interconnect service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_interconnect.client import InterconnectClient
    from types_aiobotocore_interconnect.waiter import (
        ConnectionAvailableWaiter,
        ConnectionDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("interconnect") as client:
        client: InterconnectClient

        connection_available_waiter: ConnectionAvailableWaiter = client.get_waiter("connection_available")
        connection_deleted_waiter: ConnectionDeletedWaiter = client.get_waiter("connection_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetConnectionRequestWaitExtraTypeDef, GetConnectionRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ConnectionAvailableWaiter", "ConnectionDeletedWaiter")


class ConnectionAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/waiter/ConnectionAvailable.html#Interconnect.Waiter.ConnectionAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/waiters/#connectionavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetConnectionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/waiter/ConnectionAvailable.html#Interconnect.Waiter.ConnectionAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/waiters/#connectionavailablewaiter)
        """


class ConnectionDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/waiter/ConnectionDeleted.html#Interconnect.Waiter.ConnectionDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/waiters/#connectiondeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetConnectionRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/waiter/ConnectionDeleted.html#Interconnect.Waiter.ConnectionDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/waiters/#connectiondeletedwaiter)
        """
