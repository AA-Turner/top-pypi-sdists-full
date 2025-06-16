"""
Main interface for chime-sdk-meetings service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_meetings import (
        ChimeSDKMeetingsClient,
        Client,
    )

    session = get_session()
    async with session.create_client("chime-sdk-meetings") as client:
        client: ChimeSDKMeetingsClient
        ...

    ```
"""

from .client import ChimeSDKMeetingsClient

Client = ChimeSDKMeetingsClient

__all__ = ("ChimeSDKMeetingsClient", "Client")
