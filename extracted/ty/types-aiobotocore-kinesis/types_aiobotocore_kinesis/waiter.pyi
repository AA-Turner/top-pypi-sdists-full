"""
Type annotations for kinesis service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesis.client import KinesisClient
    from types_aiobotocore_kinesis.waiter import (
        ChannelActiveWaiter,
        StreamExistsWaiter,
        StreamNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("kinesis") as client:
        client: KinesisClient

        channel_active_waiter: ChannelActiveWaiter = client.get_waiter("channel_active")
        stream_exists_waiter: StreamExistsWaiter = client.get_waiter("stream_exists")
        stream_not_exists_waiter: StreamNotExistsWaiter = client.get_waiter("stream_not_exists")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeChannelInputWaitTypeDef,
    DescribeStreamInputWaitExtraTypeDef,
    DescribeStreamInputWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ChannelActiveWaiter", "StreamExistsWaiter", "StreamNotExistsWaiter")

class ChannelActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/waiter/ChannelActive.html#Kinesis.Waiter.ChannelActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#channelactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChannelInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/waiter/ChannelActive.html#Kinesis.Waiter.ChannelActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#channelactivewaiter)
        """

class StreamExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/waiter/StreamExists.html#Kinesis.Waiter.StreamExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#streamexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStreamInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/waiter/StreamExists.html#Kinesis.Waiter.StreamExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#streamexistswaiter)
        """

class StreamNotExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/waiter/StreamNotExists.html#Kinesis.Waiter.StreamNotExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#streamnotexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStreamInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/waiter/StreamNotExists.html#Kinesis.Waiter.StreamNotExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#streamnotexistswaiter)
        """
