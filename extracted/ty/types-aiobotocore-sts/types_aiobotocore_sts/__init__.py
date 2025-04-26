"""
Main interface for sts service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sts import (
        Client,
        STSClient,
    )

    session = get_session()
    async with session.create_client("sts") as client:
        client: STSClient
        ...

    ```
"""

from .client import STSClient

Client = STSClient


__all__ = ("Client", "STSClient")
