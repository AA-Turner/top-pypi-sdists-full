"""
Type annotations for ses service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_ses.client import SESClient
    from types_boto3_ses.waiter import (
        IdentityExistsWaiter,
    )

    session = Session()
    client: SESClient = session.client("ses")

    identity_exists_waiter: IdentityExistsWaiter = client.get_waiter("identity_exists")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetIdentityVerificationAttributesRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("IdentityExistsWaiter",)

class IdentityExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/waiter/IdentityExists.html#SES.Waiter.IdentityExists)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/waiters/#identityexistswaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetIdentityVerificationAttributesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/waiter/IdentityExists.html#SES.Waiter.IdentityExists.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/waiters/#identityexistswaiter)
        """
