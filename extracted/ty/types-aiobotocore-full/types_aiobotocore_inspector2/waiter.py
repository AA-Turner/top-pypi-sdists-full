"""
Type annotations for inspector2 service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_inspector2.client import Inspector2Client
    from types_aiobotocore_inspector2.waiter import (
        ConnectorConnectedWaiter,
        ConnectorDeletedWaiter,
        ConnectorEnabledWaiter,
    )

    session = get_session()
    async with session.create_client("inspector2") as client:
        client: Inspector2Client

        connector_connected_waiter: ConnectorConnectedWaiter = client.get_waiter("connector_connected")
        connector_deleted_waiter: ConnectorDeletedWaiter = client.get_waiter("connector_deleted")
        connector_enabled_waiter: ConnectorEnabledWaiter = client.get_waiter("connector_enabled")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    ListConnectorsRequestWaitExtraExtraTypeDef,
    ListConnectorsRequestWaitExtraTypeDef,
    ListConnectorsRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ConnectorConnectedWaiter", "ConnectorDeletedWaiter", "ConnectorEnabledWaiter")


class ConnectorConnectedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorConnected.html#Inspector2.Waiter.ConnectorConnected)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/waiters/#connectorconnectedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorConnected.html#Inspector2.Waiter.ConnectorConnected.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/waiters/#connectorconnectedwaiter)
        """


class ConnectorDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorDeleted.html#Inspector2.Waiter.ConnectorDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/waiters/#connectordeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorDeleted.html#Inspector2.Waiter.ConnectorDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/waiters/#connectordeletedwaiter)
        """


class ConnectorEnabledWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorEnabled.html#Inspector2.Waiter.ConnectorEnabled)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/waiters/#connectorenabledwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorEnabled.html#Inspector2.Waiter.ConnectorEnabled.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/waiters/#connectorenabledwaiter)
        """
