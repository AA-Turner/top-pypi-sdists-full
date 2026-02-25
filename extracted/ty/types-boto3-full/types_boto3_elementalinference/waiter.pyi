"""
Type annotations for elementalinference service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_elementalinference.client import ElementalInferenceClient
    from types_boto3_elementalinference.waiter import (
        FeedDeletedWaiter,
    )

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")

    feed_deleted_waiter: FeedDeletedWaiter = client.get_waiter("feed_deleted")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetFeedRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("FeedDeletedWaiter",)

class FeedDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/waiter/FeedDeleted.html#ElementalInference.Waiter.FeedDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/waiters/#feeddeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetFeedRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/waiter/FeedDeleted.html#ElementalInference.Waiter.FeedDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/waiters/#feeddeletedwaiter)
        """
