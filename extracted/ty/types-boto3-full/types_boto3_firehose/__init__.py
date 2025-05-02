"""
Main interface for firehose service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_firehose/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_firehose import (
        Client,
        FirehoseClient,
    )

    session = Session()
    client: FirehoseClient = session.client("firehose")
    ```
"""

from .client import FirehoseClient

Client = FirehoseClient


__all__ = ("Client", "FirehoseClient")
