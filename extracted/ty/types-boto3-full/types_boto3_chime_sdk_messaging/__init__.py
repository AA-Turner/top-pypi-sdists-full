"""
Main interface for chime-sdk-messaging service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_messaging/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_chime_sdk_messaging import (
        ChimeSDKMessagingClient,
        Client,
    )

    session = Session()
    client: ChimeSDKMessagingClient = session.client("chime-sdk-messaging")
    ```
"""

from .client import ChimeSDKMessagingClient

Client = ChimeSDKMessagingClient


__all__ = ("ChimeSDKMessagingClient", "Client")
