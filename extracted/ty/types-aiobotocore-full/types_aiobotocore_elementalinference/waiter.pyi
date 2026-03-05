"""
Type annotations for elementalinference service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elementalinference.client import ElementalInferenceClient
    from types_aiobotocore_elementalinference.waiter import (
        FeedDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("elementalinference") as client:
        client: ElementalInferenceClient

        feed_deleted_waiter: FeedDeletedWaiter = client.get_waiter("feed_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetFeedRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("FeedDeletedWaiter",)

class FeedDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/waiter/FeedDeleted.html#ElementalInference.Waiter.FeedDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/waiters/#feeddeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetFeedRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/waiter/FeedDeleted.html#ElementalInference.Waiter.FeedDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/waiters/#feeddeletedwaiter)
        """
