"""
Type annotations for mediaconnect service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediaconnect.client import MediaConnectClient
    from types_aiobotocore_mediaconnect.waiter import (
        FlowActiveWaiter,
        FlowDeletedWaiter,
        FlowStandbyWaiter,
    )

    session = get_session()
    async with session.create_client("mediaconnect") as client:
        client: MediaConnectClient

        flow_active_waiter: FlowActiveWaiter = client.get_waiter("flow_active")
        flow_deleted_waiter: FlowDeletedWaiter = client.get_waiter("flow_deleted")
        flow_standby_waiter: FlowStandbyWaiter = client.get_waiter("flow_standby")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeFlowRequestWaitExtraExtraTypeDef,
    DescribeFlowRequestWaitExtraTypeDef,
    DescribeFlowRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("FlowActiveWaiter", "FlowDeletedWaiter", "FlowStandbyWaiter")


class FlowActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowActive.html#MediaConnect.Waiter.FlowActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowactivewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFlowRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowActive.html#MediaConnect.Waiter.FlowActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowactivewaiter)
        """


class FlowDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowDeleted.html#MediaConnect.Waiter.FlowDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowdeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFlowRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowDeleted.html#MediaConnect.Waiter.FlowDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowdeletedwaiter)
        """


class FlowStandbyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowStandby.html#MediaConnect.Waiter.FlowStandby)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowstandbywaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFlowRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowStandby.html#MediaConnect.Waiter.FlowStandby.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowstandbywaiter)
        """
