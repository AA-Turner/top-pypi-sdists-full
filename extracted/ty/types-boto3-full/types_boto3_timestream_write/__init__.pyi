"""
Main interface for timestream-write service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_write/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_timestream_write import (
        Client,
        TimestreamWriteClient,
    )

    session = Session()
    client: TimestreamWriteClient = session.client("timestream-write")
    ```
"""

from .client import TimestreamWriteClient

Client = TimestreamWriteClient

__all__ = ("Client", "TimestreamWriteClient")
