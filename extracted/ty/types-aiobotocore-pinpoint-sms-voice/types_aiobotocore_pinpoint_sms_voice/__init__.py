"""
Main interface for pinpoint-sms-voice service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pinpoint_sms_voice import (
        Client,
        PinpointSMSVoiceClient,
    )

    session = get_session()
    async with session.create_client("pinpoint-sms-voice") as client:
        client: PinpointSMSVoiceClient
        ...

    ```
"""

from .client import PinpointSMSVoiceClient

Client = PinpointSMSVoiceClient


__all__ = ("Client", "PinpointSMSVoiceClient")
