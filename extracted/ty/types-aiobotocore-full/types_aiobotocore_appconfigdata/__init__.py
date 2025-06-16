"""
Main interface for appconfigdata service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfigdata/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appconfigdata import (
        AppConfigDataClient,
        Client,
    )

    session = get_session()
    async with session.create_client("appconfigdata") as client:
        client: AppConfigDataClient
        ...

    ```
"""

from .client import AppConfigDataClient

Client = AppConfigDataClient


__all__ = ("AppConfigDataClient", "Client")
