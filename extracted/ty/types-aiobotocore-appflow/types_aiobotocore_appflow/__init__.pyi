"""
Main interface for appflow service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appflow import (
        AppflowClient,
        Client,
    )

    session = get_session()
    async with session.create_client("appflow") as client:
        client: AppflowClient
        ...

    ```
"""

from .client import AppflowClient

Client = AppflowClient

__all__ = ("AppflowClient", "Client")
