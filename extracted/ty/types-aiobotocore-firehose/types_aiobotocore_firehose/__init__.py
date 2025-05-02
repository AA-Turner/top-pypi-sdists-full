"""
Main interface for firehose service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_firehose/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_firehose import (
        Client,
        FirehoseClient,
    )

    session = get_session()
    async with session.create_client("firehose") as client:
        client: FirehoseClient
        ...

    ```
"""

from .client import FirehoseClient

Client = FirehoseClient


__all__ = ("Client", "FirehoseClient")
