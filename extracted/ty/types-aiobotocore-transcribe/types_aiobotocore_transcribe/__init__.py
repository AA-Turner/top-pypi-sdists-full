"""
Main interface for transcribe service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_transcribe import (
        Client,
        TranscribeServiceClient,
    )

    session = get_session()
    async with session.create_client("transcribe") as client:
        client: TranscribeServiceClient
        ...

    ```
"""

from .client import TranscribeServiceClient

Client = TranscribeServiceClient


__all__ = ("Client", "TranscribeServiceClient")
