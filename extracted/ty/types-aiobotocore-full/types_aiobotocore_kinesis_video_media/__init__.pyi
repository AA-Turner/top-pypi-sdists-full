"""
Main interface for kinesis-video-media service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_media/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_media import (
        Client,
        KinesisVideoMediaClient,
    )

    session = get_session()
    async with session.create_client("kinesis-video-media") as client:
        client: KinesisVideoMediaClient
        ...

    ```
"""

from .client import KinesisVideoMediaClient

Client = KinesisVideoMediaClient

__all__ = ("Client", "KinesisVideoMediaClient")
