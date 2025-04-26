"""
Main interface for sms-voice service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sms_voice/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sms_voice import (
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
