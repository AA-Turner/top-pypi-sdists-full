"""
Type annotations for signer service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signer/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_signer.client import SignerClient
    from types_boto3_signer.waiter import (
        SuccessfulSigningJobWaiter,
    )

    session = Session()
    client: SignerClient = session.client("signer")

    successful_signing_job_waiter: SuccessfulSigningJobWaiter = client.get_waiter("successful_signing_job")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeSigningJobRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SuccessfulSigningJobWaiter",)


class SuccessfulSigningJobWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/waiter/SuccessfulSigningJob.html#Signer.Waiter.SuccessfulSigningJob)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signer/waiters/#successfulsigningjobwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSigningJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/waiter/SuccessfulSigningJob.html#Signer.Waiter.SuccessfulSigningJob.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signer/waiters/#successfulsigningjobwaiter)
        """
