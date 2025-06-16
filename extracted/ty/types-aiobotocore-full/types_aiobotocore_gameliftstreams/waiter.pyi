"""
Type annotations for gameliftstreams service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_gameliftstreams.client import GameLiftStreamsClient
    from types_aiobotocore_gameliftstreams.waiter import (
        ApplicationDeletedWaiter,
        ApplicationReadyWaiter,
        StreamGroupActiveWaiter,
        StreamGroupDeletedWaiter,
        StreamSessionActiveWaiter,
    )

    session = get_session()
    async with session.create_client("gameliftstreams") as client:
        client: GameLiftStreamsClient

        application_deleted_waiter: ApplicationDeletedWaiter = client.get_waiter("application_deleted")
        application_ready_waiter: ApplicationReadyWaiter = client.get_waiter("application_ready")
        stream_group_active_waiter: StreamGroupActiveWaiter = client.get_waiter("stream_group_active")
        stream_group_deleted_waiter: StreamGroupDeletedWaiter = client.get_waiter("stream_group_deleted")
        stream_session_active_waiter: StreamSessionActiveWaiter = client.get_waiter("stream_session_active")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetApplicationInputWaitExtraTypeDef,
    GetApplicationInputWaitTypeDef,
    GetStreamGroupInputWaitExtraTypeDef,
    GetStreamGroupInputWaitTypeDef,
    GetStreamSessionInputWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ApplicationDeletedWaiter",
    "ApplicationReadyWaiter",
    "StreamGroupActiveWaiter",
    "StreamGroupDeletedWaiter",
    "StreamSessionActiveWaiter",
)

class ApplicationDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/ApplicationDeleted.html#GameLiftStreams.Waiter.ApplicationDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#applicationdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetApplicationInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/ApplicationDeleted.html#GameLiftStreams.Waiter.ApplicationDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#applicationdeletedwaiter)
        """

class ApplicationReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/ApplicationReady.html#GameLiftStreams.Waiter.ApplicationReady)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#applicationreadywaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetApplicationInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/ApplicationReady.html#GameLiftStreams.Waiter.ApplicationReady.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#applicationreadywaiter)
        """

class StreamGroupActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/StreamGroupActive.html#GameLiftStreams.Waiter.StreamGroupActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#streamgroupactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetStreamGroupInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/StreamGroupActive.html#GameLiftStreams.Waiter.StreamGroupActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#streamgroupactivewaiter)
        """

class StreamGroupDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/StreamGroupDeleted.html#GameLiftStreams.Waiter.StreamGroupDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#streamgroupdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetStreamGroupInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/StreamGroupDeleted.html#GameLiftStreams.Waiter.StreamGroupDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#streamgroupdeletedwaiter)
        """

class StreamSessionActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/StreamSessionActive.html#GameLiftStreams.Waiter.StreamSessionActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#streamsessionactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetStreamSessionInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/waiter/StreamSessionActive.html#GameLiftStreams.Waiter.StreamSessionActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/waiters/#streamsessionactivewaiter)
        """
