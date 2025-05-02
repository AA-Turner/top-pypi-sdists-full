"""
Main interface for detective service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_detective import (
        Client,
        DetectiveClient,
    )

    session = get_session()
    async with session.create_client("detective") as client:
        client: DetectiveClient
        ...

    ```
"""

from .client import DetectiveClient

Client = DetectiveClient


__all__ = ("Client", "DetectiveClient")
