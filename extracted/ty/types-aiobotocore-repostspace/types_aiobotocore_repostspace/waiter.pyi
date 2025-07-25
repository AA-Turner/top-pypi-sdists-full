"""
Type annotations for repostspace service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_repostspace.client import RePostPrivateClient
    from types_aiobotocore_repostspace.waiter import (
        ChannelCreatedWaiter,
        ChannelDeletedWaiter,
        SpaceCreatedWaiter,
        SpaceDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("repostspace") as client:
        client: RePostPrivateClient

        channel_created_waiter: ChannelCreatedWaiter = client.get_waiter("channel_created")
        channel_deleted_waiter: ChannelDeletedWaiter = client.get_waiter("channel_deleted")
        space_created_waiter: SpaceCreatedWaiter = client.get_waiter("space_created")
        space_deleted_waiter: SpaceDeletedWaiter = client.get_waiter("space_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetChannelInputWaitExtraTypeDef,
    GetChannelInputWaitTypeDef,
    GetSpaceInputWaitExtraTypeDef,
    GetSpaceInputWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ChannelCreatedWaiter",
    "ChannelDeletedWaiter",
    "SpaceCreatedWaiter",
    "SpaceDeletedWaiter",
)

class ChannelCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/waiter/ChannelCreated.html#RePostPrivate.Waiter.ChannelCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/waiters/#channelcreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetChannelInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/waiter/ChannelCreated.html#RePostPrivate.Waiter.ChannelCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/waiters/#channelcreatedwaiter)
        """

class ChannelDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/waiter/ChannelDeleted.html#RePostPrivate.Waiter.ChannelDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/waiters/#channeldeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetChannelInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/waiter/ChannelDeleted.html#RePostPrivate.Waiter.ChannelDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/waiters/#channeldeletedwaiter)
        """

class SpaceCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/waiter/SpaceCreated.html#RePostPrivate.Waiter.SpaceCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/waiters/#spacecreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSpaceInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/waiter/SpaceCreated.html#RePostPrivate.Waiter.SpaceCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/waiters/#spacecreatedwaiter)
        """

class SpaceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/waiter/SpaceDeleted.html#RePostPrivate.Waiter.SpaceDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/waiters/#spacedeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSpaceInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/waiter/SpaceDeleted.html#RePostPrivate.Waiter.SpaceDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/waiters/#spacedeletedwaiter)
        """
