"""
Main interface for cloudsearch service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudsearch import (
        Client,
        CloudSearchClient,
    )

    session = get_session()
    async with session.create_client("cloudsearch") as client:
        client: CloudSearchClient
        ...

    ```
"""

from .client import CloudSearchClient

Client = CloudSearchClient


__all__ = ("Client", "CloudSearchClient")
