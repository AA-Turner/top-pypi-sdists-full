"""
Main interface for transcribe service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transcribe/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_transcribe import (
        Client,
        TranscribeServiceClient,
    )

    session = Session()
    client: TranscribeServiceClient = session.client("transcribe")
    ```
"""

from .client import TranscribeServiceClient

Client = TranscribeServiceClient

__all__ = ("Client", "TranscribeServiceClient")
