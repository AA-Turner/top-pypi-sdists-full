"""
Type annotations for continuum service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_continuum.client import ContinuumClient
    from types_boto3_continuum.waiter import (
        CodeScanSucceededWaiter,
    )

    session = Session()
    client: ContinuumClient = session.client("continuum")

    code_scan_succeeded_waiter: CodeScanSucceededWaiter = client.get_waiter("code_scan_succeeded")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetCodeScanInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("CodeScanSucceededWaiter",)

class CodeScanSucceededWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/waiter/CodeScanSucceeded.html#Continuum.Waiter.CodeScanSucceeded)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/waiters/#codescansucceededwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetCodeScanInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/waiter/CodeScanSucceeded.html#Continuum.Waiter.CodeScanSucceeded.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/waiters/#codescansucceededwaiter)
        """
