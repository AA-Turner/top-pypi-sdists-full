"""
Main interface for kinesis-video-media service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_media/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_kinesis_video_media import (
        Client,
        KinesisVideoMediaClient,
    )

    session = Session()
    client: KinesisVideoMediaClient = session.client("kinesis-video-media")
    ```
"""

from .client import KinesisVideoMediaClient

Client = KinesisVideoMediaClient


__all__ = ("Client", "KinesisVideoMediaClient")
