"""
Type annotations for endusermessaging service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_endusermessaging.client import EndUserMessagingClient
    from mypy_boto3_endusermessaging.waiter import (
        BrandProfileActiveWaiter,
        JobSuccessWaiter,
    )

    session = Session()
    client: EndUserMessagingClient = session.client("endusermessaging")

    brand_profile_active_waiter: BrandProfileActiveWaiter = client.get_waiter("brand_profile_active")
    job_success_waiter: JobSuccessWaiter = client.get_waiter("job_success")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetBrandProfileInputWaitTypeDef, GetJobInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("BrandProfileActiveWaiter", "JobSuccessWaiter")

class BrandProfileActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/waiter/BrandProfileActive.html#EndUserMessaging.Waiter.BrandProfileActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/waiters/#brandprofileactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetBrandProfileInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/waiter/BrandProfileActive.html#EndUserMessaging.Waiter.BrandProfileActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/waiters/#brandprofileactivewaiter)
        """

class JobSuccessWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/waiter/JobSuccess.html#EndUserMessaging.Waiter.JobSuccess)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/waiters/#jobsuccesswaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetJobInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/waiter/JobSuccess.html#EndUserMessaging.Waiter.JobSuccess.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/waiters/#jobsuccesswaiter)
        """
