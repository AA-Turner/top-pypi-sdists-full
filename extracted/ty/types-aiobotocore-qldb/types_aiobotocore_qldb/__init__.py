"""
Main interface for qldb service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qldb import (
        Client,
        QLDBClient,
    )

    session = get_session()
    async with session.create_client("qldb") as client:
        client: QLDBClient
        ...

    ```
"""

from .client import QLDBClient

Client = QLDBClient


__all__ = ("Client", "QLDBClient")
