"""
Type annotations for signer service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_signer.client import SignerClient
    from types_aiobotocore_signer.waiter import (
        SuccessfulSigningJobWaiter,
    )

    session = get_session()
    async with session.create_client("signer") as client:
        client: SignerClient

        successful_signing_job_waiter: SuccessfulSigningJobWaiter = client.get_waiter("successful_signing_job")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import DescribeSigningJobRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("SuccessfulSigningJobWaiter",)

class SuccessfulSigningJobWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/waiter/SuccessfulSigningJob.html#Signer.Waiter.SuccessfulSigningJob)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/waiters/#successfulsigningjobwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSigningJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/waiter/SuccessfulSigningJob.html#Signer.Waiter.SuccessfulSigningJob.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/waiters/#successfulsigningjobwaiter)
        """
