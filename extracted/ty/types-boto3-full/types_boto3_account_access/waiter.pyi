"""
Type annotations for account-access service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_account_access/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_account_access.client import AccountAccessClient
    from types_boto3_account_access.waiter import (
        ApplicationActiveWaiter,
    )

    session = Session()
    client: AccountAccessClient = session.client("account-access")

    application_active_waiter: ApplicationActiveWaiter = client.get_waiter("application_active")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetApplicationRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ApplicationActiveWaiter",)

class ApplicationActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/waiter/ApplicationActive.html#AccountAccess.Waiter.ApplicationActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_account_access/waiters/#applicationactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetApplicationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/waiter/ApplicationActive.html#AccountAccess.Waiter.ApplicationActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_account_access/waiters/#applicationactivewaiter)
        """
