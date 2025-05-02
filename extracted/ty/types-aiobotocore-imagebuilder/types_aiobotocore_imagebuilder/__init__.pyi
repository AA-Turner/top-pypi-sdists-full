"""
Main interface for imagebuilder service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_imagebuilder import (
        Client,
        ImagebuilderClient,
    )

    session = get_session()
    async with session.create_client("imagebuilder") as client:
        client: ImagebuilderClient
        ...

    ```
"""

from .client import ImagebuilderClient

Client = ImagebuilderClient

__all__ = ("Client", "ImagebuilderClient")
