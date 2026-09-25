"""
Type annotations for eventbridgev2 service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_eventbridgev2/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_eventbridgev2.client import EventBridgeV2Client
    from types_boto3_eventbridgev2.waiter import (
        EventBusActiveWaiter,
        EventBusDeletedWaiter,
    )

    session = Session()
    client: EventBridgeV2Client = session.client("eventbridgev2")

    event_bus_active_waiter: EventBusActiveWaiter = client.get_waiter("event_bus_active")
    event_bus_deleted_waiter: EventBusDeletedWaiter = client.get_waiter("event_bus_deleted")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeEventBusRequestWaitExtraTypeDef, DescribeEventBusRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("EventBusActiveWaiter", "EventBusDeletedWaiter")


class EventBusActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/waiter/EventBusActive.html#EventBridgeV2.Waiter.EventBusActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_eventbridgev2/waiters/#eventbusactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventBusRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/waiter/EventBusActive.html#EventBridgeV2.Waiter.EventBusActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_eventbridgev2/waiters/#eventbusactivewaiter)
        """


class EventBusDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/waiter/EventBusDeleted.html#EventBridgeV2.Waiter.EventBusDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_eventbridgev2/waiters/#eventbusdeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventBusRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/waiter/EventBusDeleted.html#EventBridgeV2.Waiter.EventBusDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_eventbridgev2/waiters/#eventbusdeletedwaiter)
        """
