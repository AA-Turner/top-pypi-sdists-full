"""
Main interface for cognito-sync service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_sync import (
        Client,
        CognitoSyncClient,
    )

    session = get_session()
    async with session.create_client("cognito-sync") as client:
        client: CognitoSyncClient
        ...

    ```
"""

from .client import CognitoSyncClient

Client = CognitoSyncClient


__all__ = ("Client", "CognitoSyncClient")
