"""
Type annotations for ds service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_ds.client import DirectoryServiceClient
    from types_boto3_ds.waiter import (
        HybridADUpdatedWaiter,
    )

    session = Session()
    client: DirectoryServiceClient = session.client("ds")

    hybrid_ad_updated_waiter: HybridADUpdatedWaiter = client.get_waiter("hybrid_ad_updated")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeHybridADUpdateRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("HybridADUpdatedWaiter",)


class HybridADUpdatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/waiter/HybridADUpdated.html#DirectoryService.Waiter.HybridADUpdated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds/waiters/#hybridadupdatedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeHybridADUpdateRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/waiter/HybridADUpdated.html#DirectoryService.Waiter.HybridADUpdated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ds/waiters/#hybridadupdatedwaiter)
        """
