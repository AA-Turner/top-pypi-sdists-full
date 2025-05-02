"""
Main interface for iotevents-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotevents_data import (
        Client,
        IoTEventsDataClient,
    )

    session = get_session()
    async with session.create_client("iotevents-data") as client:
        client: IoTEventsDataClient
        ...

    ```
"""

from .client import IoTEventsDataClient

Client = IoTEventsDataClient

__all__ = ("Client", "IoTEventsDataClient")
