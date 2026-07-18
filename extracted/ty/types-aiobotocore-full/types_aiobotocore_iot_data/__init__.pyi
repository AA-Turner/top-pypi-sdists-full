"""
Main interface for iot-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot_data import (
        Client,
        IoTDataPlaneClient,
        ListRetainedMessagesPaginator,
        ListSubscriptionsPaginator,
    )

    session = get_session()
    async with session.create_client("iot-data") as client:
        client: IoTDataPlaneClient
        ...


    list_retained_messages_paginator: ListRetainedMessagesPaginator = client.get_paginator("list_retained_messages")
    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from .client import IoTDataPlaneClient
from .paginator import ListRetainedMessagesPaginator, ListSubscriptionsPaginator

Client = IoTDataPlaneClient

__all__ = (
    "Client",
    "IoTDataPlaneClient",
    "ListRetainedMessagesPaginator",
    "ListSubscriptionsPaginator",
)
