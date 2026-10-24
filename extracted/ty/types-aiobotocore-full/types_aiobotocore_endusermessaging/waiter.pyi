"""
Type annotations for endusermessaging service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_endusermessaging.client import EndUserMessagingClient
    from types_aiobotocore_endusermessaging.waiter import (
        BrandProfileActiveWaiter,
        JobSuccessWaiter,
    )

    session = get_session()
    async with session.create_client("endusermessaging") as client:
        client: EndUserMessagingClient

        brand_profile_active_waiter: BrandProfileActiveWaiter = client.get_waiter("brand_profile_active")
        job_success_waiter: JobSuccessWaiter = client.get_waiter("job_success")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetBrandProfileInputWaitTypeDef, GetJobInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("BrandProfileActiveWaiter", "JobSuccessWaiter")

class BrandProfileActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/waiter/BrandProfileActive.html#EndUserMessaging.Waiter.BrandProfileActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/waiters/#brandprofileactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetBrandProfileInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/waiter/BrandProfileActive.html#EndUserMessaging.Waiter.BrandProfileActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/waiters/#brandprofileactivewaiter)
        """

class JobSuccessWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/waiter/JobSuccess.html#EndUserMessaging.Waiter.JobSuccess)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/waiters/#jobsuccesswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetJobInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/waiter/JobSuccess.html#EndUserMessaging.Waiter.JobSuccess.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/waiters/#jobsuccesswaiter)
        """
