"""
Main interface for support-app service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_support_app import (
        Client,
        SupportAppClient,
    )

    session = get_session()
    async with session.create_client("support-app") as client:
        client: SupportAppClient
        ...

    ```
"""

from .client import SupportAppClient

Client = SupportAppClient


__all__ = ("Client", "SupportAppClient")
