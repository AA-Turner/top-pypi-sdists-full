"""
Type annotations for polly service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_polly.client import PollyClient
    from mypy_boto3_polly.waiter import (
        VoiceActiveWaiter,
    )

    session = Session()
    client: PollyClient = session.client("polly")

    voice_active_waiter: VoiceActiveWaiter = client.get_waiter("voice_active")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetVoiceInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("VoiceActiveWaiter",)

class VoiceActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/waiter/VoiceActive.html#Polly.Waiter.VoiceActive)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/waiters/#voiceactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetVoiceInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/waiter/VoiceActive.html#Polly.Waiter.VoiceActive.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/waiters/#voiceactivewaiter)
        """
