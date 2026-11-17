"""
Type annotations for opensearchmemory service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_opensearchmemory.client import OpenSearchMemoryClient
    from mypy_boto3_opensearchmemory.waiter import (
        SpaceActiveWaiter,
        SpaceDeletedWaiter,
    )

    session = Session()
    client: OpenSearchMemoryClient = session.client("opensearchmemory")

    space_active_waiter: SpaceActiveWaiter = client.get_waiter("space_active")
    space_deleted_waiter: SpaceDeletedWaiter = client.get_waiter("space_deleted")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetSpaceRequestWaitExtraTypeDef, GetSpaceRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SpaceActiveWaiter", "SpaceDeletedWaiter")


class SpaceActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/waiter/SpaceActive.html#OpenSearchMemory.Waiter.SpaceActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/waiters/#spaceactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSpaceRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/waiter/SpaceActive.html#OpenSearchMemory.Waiter.SpaceActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/waiters/#spaceactivewaiter)
        """


class SpaceDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/waiter/SpaceDeleted.html#OpenSearchMemory.Waiter.SpaceDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/waiters/#spacedeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSpaceRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/waiter/SpaceDeleted.html#OpenSearchMemory.Waiter.SpaceDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchmemory/waiters/#spacedeletedwaiter)
        """
