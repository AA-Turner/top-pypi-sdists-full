"""
Main interface for kinesis-video-signaling service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_signaling/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_signaling import (
        Client,
        KinesisVideoSignalingChannelsClient,
    )

    session = get_session()
    async with session.create_client("kinesis-video-signaling") as client:
        client: KinesisVideoSignalingChannelsClient
        ...

    ```
"""

from .client import KinesisVideoSignalingChannelsClient

Client = KinesisVideoSignalingChannelsClient

__all__ = ("Client", "KinesisVideoSignalingChannelsClient")
