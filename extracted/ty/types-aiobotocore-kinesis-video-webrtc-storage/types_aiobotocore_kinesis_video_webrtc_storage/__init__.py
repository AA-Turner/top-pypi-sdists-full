"""
Main interface for kinesis-video-webrtc-storage service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_webrtc_storage/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_webrtc_storage import (
        Client,
        KinesisVideoWebRTCStorageClient,
    )

    session = get_session()
    async with session.create_client("kinesis-video-webrtc-storage") as client:
        client: KinesisVideoWebRTCStorageClient
        ...

    ```
"""

from .client import KinesisVideoWebRTCStorageClient

Client = KinesisVideoWebRTCStorageClient


__all__ = ("Client", "KinesisVideoWebRTCStorageClient")
