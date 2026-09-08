"""
Type annotations for account-access service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_account_access.client import AccountAccessClient
    from types_aiobotocore_account_access.waiter import (
        ApplicationActiveWaiter,
    )

    session = get_session()
    async with session.create_client("account-access") as client:
        client: AccountAccessClient

        application_active_waiter: ApplicationActiveWaiter = client.get_waiter("application_active")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetApplicationRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ApplicationActiveWaiter",)

class ApplicationActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/waiter/ApplicationActive.html#AccountAccess.Waiter.ApplicationActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/waiters/#applicationactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetApplicationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/waiter/ApplicationActive.html#AccountAccess.Waiter.ApplicationActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/waiters/#applicationactivewaiter)
        """
