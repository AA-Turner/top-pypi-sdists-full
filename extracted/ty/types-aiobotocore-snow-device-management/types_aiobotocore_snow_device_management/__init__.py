"""
Main interface for snow-device-management service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_snow_device_management import (
        Client,
        ListDeviceResourcesPaginator,
        ListDevicesPaginator,
        ListExecutionsPaginator,
        ListTasksPaginator,
        SnowDeviceManagementClient,
    )

    session = get_session()
    async with session.create_client("snow-device-management") as client:
        client: SnowDeviceManagementClient
        ...


    list_device_resources_paginator: ListDeviceResourcesPaginator = client.get_paginator("list_device_resources")
    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```
"""

from .client import SnowDeviceManagementClient
from .paginator import (
    ListDeviceResourcesPaginator,
    ListDevicesPaginator,
    ListExecutionsPaginator,
    ListTasksPaginator,
)

Client = SnowDeviceManagementClient


__all__ = (
    "Client",
    "ListDeviceResourcesPaginator",
    "ListDevicesPaginator",
    "ListExecutionsPaginator",
    "ListTasksPaginator",
    "SnowDeviceManagementClient",
)
