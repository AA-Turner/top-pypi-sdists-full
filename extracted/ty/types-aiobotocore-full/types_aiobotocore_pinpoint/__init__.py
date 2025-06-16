"""
Main interface for pinpoint service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pinpoint import (
        Client,
        PinpointClient,
    )

    session = get_session()
    async with session.create_client("pinpoint") as client:
        client: PinpointClient
        ...

    ```
"""

from .client import PinpointClient

Client = PinpointClient


__all__ = ("Client", "PinpointClient")
