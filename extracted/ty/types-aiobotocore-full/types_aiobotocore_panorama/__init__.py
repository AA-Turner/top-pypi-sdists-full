"""
Main interface for panorama service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_panorama import (
        Client,
        PanoramaClient,
    )

    session = get_session()
    async with session.create_client("panorama") as client:
        client: PanoramaClient
        ...

    ```
"""

from .client import PanoramaClient

Client = PanoramaClient


__all__ = ("Client", "PanoramaClient")
