"""
Type annotations for mediaconnect service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediaconnect.client import MediaConnectClient
    from types_aiobotocore_mediaconnect.waiter import (
        FlowActiveWaiter,
        FlowDeletedWaiter,
        FlowStandbyWaiter,
        InputActiveWaiter,
        InputDeletedWaiter,
        InputStandbyWaiter,
        OutputActiveWaiter,
        OutputDeletedWaiter,
        OutputRoutedWaiter,
        OutputStandbyWaiter,
    )

    session = get_session()
    async with session.create_client("mediaconnect") as client:
        client: MediaConnectClient

        flow_active_waiter: FlowActiveWaiter = client.get_waiter("flow_active")
        flow_deleted_waiter: FlowDeletedWaiter = client.get_waiter("flow_deleted")
        flow_standby_waiter: FlowStandbyWaiter = client.get_waiter("flow_standby")
        input_active_waiter: InputActiveWaiter = client.get_waiter("input_active")
        input_deleted_waiter: InputDeletedWaiter = client.get_waiter("input_deleted")
        input_standby_waiter: InputStandbyWaiter = client.get_waiter("input_standby")
        output_active_waiter: OutputActiveWaiter = client.get_waiter("output_active")
        output_deleted_waiter: OutputDeletedWaiter = client.get_waiter("output_deleted")
        output_routed_waiter: OutputRoutedWaiter = client.get_waiter("output_routed")
        output_standby_waiter: OutputStandbyWaiter = client.get_waiter("output_standby")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeFlowRequestWaitExtraExtraTypeDef,
    DescribeFlowRequestWaitExtraTypeDef,
    DescribeFlowRequestWaitTypeDef,
    GetRouterInputRequestWaitExtraExtraTypeDef,
    GetRouterInputRequestWaitExtraTypeDef,
    GetRouterInputRequestWaitTypeDef,
    GetRouterOutputRequestWaitExtraExtraExtraTypeDef,
    GetRouterOutputRequestWaitExtraExtraTypeDef,
    GetRouterOutputRequestWaitExtraTypeDef,
    GetRouterOutputRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "FlowActiveWaiter",
    "FlowDeletedWaiter",
    "FlowStandbyWaiter",
    "InputActiveWaiter",
    "InputDeletedWaiter",
    "InputStandbyWaiter",
    "OutputActiveWaiter",
    "OutputDeletedWaiter",
    "OutputRoutedWaiter",
    "OutputStandbyWaiter",
)

class FlowActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowActive.html#MediaConnect.Waiter.FlowActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFlowRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowActive.html#MediaConnect.Waiter.FlowActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowactivewaiter)
        """

class FlowDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowDeleted.html#MediaConnect.Waiter.FlowDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFlowRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowDeleted.html#MediaConnect.Waiter.FlowDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowdeletedwaiter)
        """

class FlowStandbyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowStandby.html#MediaConnect.Waiter.FlowStandby)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowstandbywaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFlowRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowStandby.html#MediaConnect.Waiter.FlowStandby.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowstandbywaiter)
        """

class InputActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputActive.html#MediaConnect.Waiter.InputActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#inputactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterInputRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputActive.html#MediaConnect.Waiter.InputActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#inputactivewaiter)
        """

class InputDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputDeleted.html#MediaConnect.Waiter.InputDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#inputdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterInputRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputDeleted.html#MediaConnect.Waiter.InputDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#inputdeletedwaiter)
        """

class InputStandbyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputStandby.html#MediaConnect.Waiter.InputStandby)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#inputstandbywaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterInputRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputStandby.html#MediaConnect.Waiter.InputStandby.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#inputstandbywaiter)
        """

class OutputActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputActive.html#MediaConnect.Waiter.OutputActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#outputactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterOutputRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputActive.html#MediaConnect.Waiter.OutputActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#outputactivewaiter)
        """

class OutputDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputDeleted.html#MediaConnect.Waiter.OutputDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#outputdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterOutputRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputDeleted.html#MediaConnect.Waiter.OutputDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#outputdeletedwaiter)
        """

class OutputRoutedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputRouted.html#MediaConnect.Waiter.OutputRouted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#outputroutedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterOutputRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputRouted.html#MediaConnect.Waiter.OutputRouted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#outputroutedwaiter)
        """

class OutputStandbyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputStandby.html#MediaConnect.Waiter.OutputStandby)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#outputstandbywaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterOutputRequestWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputStandby.html#MediaConnect.Waiter.OutputStandby.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#outputstandbywaiter)
        """
