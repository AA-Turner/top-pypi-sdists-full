"""
Main interface for codeconnections service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeconnections/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeconnections import (
        Client,
        CodeConnectionsClient,
    )

    session = get_session()
    async with session.create_client("codeconnections") as client:
        client: CodeConnectionsClient
        ...

    ```
"""

from .client import CodeConnectionsClient

Client = CodeConnectionsClient


__all__ = ("Client", "CodeConnectionsClient")
