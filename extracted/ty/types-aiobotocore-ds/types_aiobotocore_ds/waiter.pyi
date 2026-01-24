"""
Type annotations for ds service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ds.client import DirectoryServiceClient
    from types_aiobotocore_ds.waiter import (
        HybridADUpdatedWaiter,
    )

    session = get_session()
    async with session.create_client("ds") as client:
        client: DirectoryServiceClient

        hybrid_ad_updated_waiter: HybridADUpdatedWaiter = client.get_waiter("hybrid_ad_updated")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import DescribeHybridADUpdateRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("HybridADUpdatedWaiter",)

class HybridADUpdatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/waiter/HybridADUpdated.html#DirectoryService.Waiter.HybridADUpdated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/waiters/#hybridadupdatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeHybridADUpdateRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/waiter/HybridADUpdated.html#DirectoryService.Waiter.HybridADUpdated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/waiters/#hybridadupdatedwaiter)
        """
