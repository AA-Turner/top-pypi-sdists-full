"""
Type annotations for ses service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ses.client import SESClient
    from types_aiobotocore_ses.waiter import (
        IdentityExistsWaiter,
    )

    session = get_session()
    async with session.create_client("ses") as client:
        client: SESClient

        identity_exists_waiter: IdentityExistsWaiter = client.get_waiter("identity_exists")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetIdentityVerificationAttributesRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("IdentityExistsWaiter",)


class IdentityExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/waiter/IdentityExists.html#SES.Waiter.IdentityExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/waiters/#identityexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetIdentityVerificationAttributesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/waiter/IdentityExists.html#SES.Waiter.IdentityExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/waiters/#identityexistswaiter)
        """
