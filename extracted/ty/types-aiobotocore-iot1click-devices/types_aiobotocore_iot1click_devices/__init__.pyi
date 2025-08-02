"""
Main interface for iot1click-devices service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot1click_devices import (
        Client,
        IoT1ClickDevicesServiceClient,
        ListDeviceEventsPaginator,
        ListDevicesPaginator,
    )

    session = get_session()
    async with session.create_client("iot1click-devices") as client:
        client: IoT1ClickDevicesServiceClient
        ...


    list_device_events_paginator: ListDeviceEventsPaginator = client.get_paginator("list_device_events")
    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import IoT1ClickDevicesServiceClient
from .paginator import ListDeviceEventsPaginator, ListDevicesPaginator

Client = IoT1ClickDevicesServiceClient

__all__ = (
    "Client",
    "IoT1ClickDevicesServiceClient",
    "ListDeviceEventsPaginator",
    "ListDevicesPaginator",
)
