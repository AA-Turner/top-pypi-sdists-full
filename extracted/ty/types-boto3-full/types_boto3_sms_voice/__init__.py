"""
Main interface for sms-voice service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms_voice/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sms_voice import (
        Client,
        SMSVoiceClient,
    )

    session = Session()
    client: SMSVoiceClient = session.client("sms-voice")
    ```
"""

from .client import SMSVoiceClient

Client = SMSVoiceClient


__all__ = ("Client", "SMSVoiceClient")
