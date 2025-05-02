"""
Main interface for ebs service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ebs import (
        Client,
        EBSClient,
    )

    session = get_session()
    async with session.create_client("ebs") as client:
        client: EBSClient
        ...

    ```
"""

from .client import EBSClient

Client = EBSClient

__all__ = ("Client", "EBSClient")
