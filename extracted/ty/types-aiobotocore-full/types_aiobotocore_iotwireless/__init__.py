"""
Main interface for iotwireless service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotwireless/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotwireless import (
        Client,
        IoTWirelessClient,
    )

    session = get_session()
    async with session.create_client("iotwireless") as client:
        client: IoTWirelessClient
        ...

    ```
"""

from .client import IoTWirelessClient

Client = IoTWirelessClient


__all__ = ("Client", "IoTWirelessClient")
