"""
Main interface for timestream-write service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_timestream_write import (
        Client,
        TimestreamWriteClient,
    )

    session = get_session()
    async with session.create_client("timestream-write") as client:
        client: TimestreamWriteClient
        ...

    ```
"""

from .client import TimestreamWriteClient

Client = TimestreamWriteClient

__all__ = ("Client", "TimestreamWriteClient")
