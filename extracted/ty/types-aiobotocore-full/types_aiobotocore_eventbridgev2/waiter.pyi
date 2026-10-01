"""
Type annotations for eventbridgev2 service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_eventbridgev2.client import EventBridgeV2Client
    from types_aiobotocore_eventbridgev2.waiter import (
        EventBusActiveWaiter,
        EventBusDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("eventbridgev2") as client:
        client: EventBridgeV2Client

        event_bus_active_waiter: EventBusActiveWaiter = client.get_waiter("event_bus_active")
        event_bus_deleted_waiter: EventBusDeletedWaiter = client.get_waiter("event_bus_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import DescribeEventBusRequestWaitExtraTypeDef, DescribeEventBusRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("EventBusActiveWaiter", "EventBusDeletedWaiter")

class EventBusActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/waiter/EventBusActive.html#EventBridgeV2.Waiter.EventBusActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/waiters/#eventbusactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventBusRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/waiter/EventBusActive.html#EventBridgeV2.Waiter.EventBusActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/waiters/#eventbusactivewaiter)
        """

class EventBusDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/waiter/EventBusDeleted.html#EventBridgeV2.Waiter.EventBusDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/waiters/#eventbusdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventBusRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/waiter/EventBusDeleted.html#EventBridgeV2.Waiter.EventBusDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/waiters/#eventbusdeletedwaiter)
        """
