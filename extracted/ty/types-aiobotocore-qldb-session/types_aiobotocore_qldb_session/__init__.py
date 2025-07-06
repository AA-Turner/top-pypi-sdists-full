"""
Main interface for qldb-session service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb_session/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qldb_session import (
        Client,
        QLDBSessionClient,
    )

    session = get_session()
    async with session.create_client("qldb-session") as client:
        client: QLDBSessionClient
        ...

    ```
"""

from .client import QLDBSessionClient

Client = QLDBSessionClient


__all__ = ("Client", "QLDBSessionClient")
