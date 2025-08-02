"""
Main interface for sms-voice service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms_voice/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sms_voice import (
        Client,
        SMSVoiceClient,
    )

    session = get_session()
    async with session.create_client("sms-voice") as client:
        client: SMSVoiceClient
        ...

    ```
"""

from .client import SMSVoiceClient

Client = SMSVoiceClient


__all__ = ("Client", "SMSVoiceClient")
