"""
Main interface for iotsecuretunneling service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotsecuretunneling import (
        Client,
        IoTSecureTunnelingClient,
    )

    session = get_session()
    async with session.create_client("iotsecuretunneling") as client:
        client: IoTSecureTunnelingClient
        ...

    ```
"""

from .client import IoTSecureTunnelingClient

Client = IoTSecureTunnelingClient

__all__ = ("Client", "IoTSecureTunnelingClient")
