"""
Type annotations for macie2 service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_macie2.client import Macie2Client
    from types_aiobotocore_macie2.waiter import (
        FindingRevealedWaiter,
    )

    session = get_session()
    async with session.create_client("macie2") as client:
        client: Macie2Client

        finding_revealed_waiter: FindingRevealedWaiter = client.get_waiter("finding_revealed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetSensitiveDataOccurrencesRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("FindingRevealedWaiter",)


class FindingRevealedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/waiter/FindingRevealed.html#Macie2.Waiter.FindingRevealed)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/waiters/#findingrevealedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSensitiveDataOccurrencesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/waiter/FindingRevealed.html#Macie2.Waiter.FindingRevealed.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/waiters/#findingrevealedwaiter)
        """
