"""
Main interface for kendra service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kendra import (
        Client,
        KendraClient,
    )

    session = get_session()
    async with session.create_client("kendra") as client:
        client: KendraClient
        ...

    ```
"""

from .client import KendraClient

Client = KendraClient

__all__ = ("Client", "KendraClient")
