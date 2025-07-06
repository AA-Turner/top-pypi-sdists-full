"""
Main interface for iottwinmaker service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iottwinmaker import (
        Client,
        IoTTwinMakerClient,
    )

    session = get_session()
    async with session.create_client("iottwinmaker") as client:
        client: IoTTwinMakerClient
        ...

    ```
"""

from .client import IoTTwinMakerClient

Client = IoTTwinMakerClient

__all__ = ("Client", "IoTTwinMakerClient")
