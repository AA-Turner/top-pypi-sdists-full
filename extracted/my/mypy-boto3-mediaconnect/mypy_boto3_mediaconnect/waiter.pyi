"""
Type annotations for mediaconnect service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mediaconnect.client import MediaConnectClient
    from mypy_boto3_mediaconnect.waiter import (
        DestinationEndpointConnectedWaiter,
        DestinationEndpointDeregisteredWaiter,
        DestinationEndpointDisconnectedWaiter,
        DestinationEndpointRegisteredWaiter,
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
        OutputUnroutedWaiter,
        SourceEndpointConnectedWaiter,
        SourceEndpointConnectingWaiter,
        SourceEndpointDeregisteredWaiter,
        SourceEndpointDisconnectedWaiter,
        SourceEndpointDisconnectingWaiter,
        SourceEndpointRegisteredWaiter,
    )

    session = Session()
    client: MediaConnectClient = session.client("mediaconnect")

    destination_endpoint_connected_waiter: DestinationEndpointConnectedWaiter = client.get_waiter("destination_endpoint_connected")
    destination_endpoint_deregistered_waiter: DestinationEndpointDeregisteredWaiter = client.get_waiter("destination_endpoint_deregistered")
    destination_endpoint_disconnected_waiter: DestinationEndpointDisconnectedWaiter = client.get_waiter("destination_endpoint_disconnected")
    destination_endpoint_registered_waiter: DestinationEndpointRegisteredWaiter = client.get_waiter("destination_endpoint_registered")
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
    output_unrouted_waiter: OutputUnroutedWaiter = client.get_waiter("output_unrouted")
    source_endpoint_connected_waiter: SourceEndpointConnectedWaiter = client.get_waiter("source_endpoint_connected")
    source_endpoint_connecting_waiter: SourceEndpointConnectingWaiter = client.get_waiter("source_endpoint_connecting")
    source_endpoint_deregistered_waiter: SourceEndpointDeregisteredWaiter = client.get_waiter("source_endpoint_deregistered")
    source_endpoint_disconnected_waiter: SourceEndpointDisconnectedWaiter = client.get_waiter("source_endpoint_disconnected")
    source_endpoint_disconnecting_waiter: SourceEndpointDisconnectingWaiter = client.get_waiter("source_endpoint_disconnecting")
    source_endpoint_registered_waiter: SourceEndpointRegisteredWaiter = client.get_waiter("source_endpoint_registered")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeFlowRequestWaitExtraExtraTypeDef,
    DescribeFlowRequestWaitExtraTypeDef,
    DescribeFlowRequestWaitTypeDef,
    GetDestinationEndpointRequestWaitExtraExtraExtraTypeDef,
    GetDestinationEndpointRequestWaitExtraExtraTypeDef,
    GetDestinationEndpointRequestWaitExtraTypeDef,
    GetDestinationEndpointRequestWaitTypeDef,
    GetRouterInputRequestWaitExtraExtraTypeDef,
    GetRouterInputRequestWaitExtraTypeDef,
    GetRouterInputRequestWaitTypeDef,
    GetRouterOutputRequestWaitExtraExtraExtraExtraTypeDef,
    GetRouterOutputRequestWaitExtraExtraExtraTypeDef,
    GetRouterOutputRequestWaitExtraExtraTypeDef,
    GetRouterOutputRequestWaitExtraTypeDef,
    GetRouterOutputRequestWaitTypeDef,
    GetSourceEndpointRequestWaitExtraExtraExtraExtraExtraTypeDef,
    GetSourceEndpointRequestWaitExtraExtraExtraExtraTypeDef,
    GetSourceEndpointRequestWaitExtraExtraExtraTypeDef,
    GetSourceEndpointRequestWaitExtraExtraTypeDef,
    GetSourceEndpointRequestWaitExtraTypeDef,
    GetSourceEndpointRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DestinationEndpointConnectedWaiter",
    "DestinationEndpointDeregisteredWaiter",
    "DestinationEndpointDisconnectedWaiter",
    "DestinationEndpointRegisteredWaiter",
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
    "OutputUnroutedWaiter",
    "SourceEndpointConnectedWaiter",
    "SourceEndpointConnectingWaiter",
    "SourceEndpointDeregisteredWaiter",
    "SourceEndpointDisconnectedWaiter",
    "SourceEndpointDisconnectingWaiter",
    "SourceEndpointRegisteredWaiter",
)

class DestinationEndpointConnectedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/DestinationEndpointConnected.html#MediaConnect.Waiter.DestinationEndpointConnected)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#destinationendpointconnectedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetDestinationEndpointRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/DestinationEndpointConnected.html#MediaConnect.Waiter.DestinationEndpointConnected.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#destinationendpointconnectedwaiter)
        """

class DestinationEndpointDeregisteredWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/DestinationEndpointDeregistered.html#MediaConnect.Waiter.DestinationEndpointDeregistered)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#destinationendpointderegisteredwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetDestinationEndpointRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/DestinationEndpointDeregistered.html#MediaConnect.Waiter.DestinationEndpointDeregistered.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#destinationendpointderegisteredwaiter)
        """

class DestinationEndpointDisconnectedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/DestinationEndpointDisconnected.html#MediaConnect.Waiter.DestinationEndpointDisconnected)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#destinationendpointdisconnectedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetDestinationEndpointRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/DestinationEndpointDisconnected.html#MediaConnect.Waiter.DestinationEndpointDisconnected.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#destinationendpointdisconnectedwaiter)
        """

class DestinationEndpointRegisteredWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/DestinationEndpointRegistered.html#MediaConnect.Waiter.DestinationEndpointRegistered)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#destinationendpointregisteredwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetDestinationEndpointRequestWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/DestinationEndpointRegistered.html#MediaConnect.Waiter.DestinationEndpointRegistered.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#destinationendpointregisteredwaiter)
        """

class FlowActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowActive.html#MediaConnect.Waiter.FlowActive)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#flowactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFlowRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowActive.html#MediaConnect.Waiter.FlowActive.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#flowactivewaiter)
        """

class FlowDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowDeleted.html#MediaConnect.Waiter.FlowDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#flowdeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFlowRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowDeleted.html#MediaConnect.Waiter.FlowDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#flowdeletedwaiter)
        """

class FlowStandbyWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowStandby.html#MediaConnect.Waiter.FlowStandby)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#flowstandbywaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFlowRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/FlowStandby.html#MediaConnect.Waiter.FlowStandby.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#flowstandbywaiter)
        """

class InputActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputActive.html#MediaConnect.Waiter.InputActive)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#inputactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterInputRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputActive.html#MediaConnect.Waiter.InputActive.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#inputactivewaiter)
        """

class InputDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputDeleted.html#MediaConnect.Waiter.InputDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#inputdeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterInputRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputDeleted.html#MediaConnect.Waiter.InputDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#inputdeletedwaiter)
        """

class InputStandbyWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputStandby.html#MediaConnect.Waiter.InputStandby)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#inputstandbywaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterInputRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/InputStandby.html#MediaConnect.Waiter.InputStandby.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#inputstandbywaiter)
        """

class OutputActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputActive.html#MediaConnect.Waiter.OutputActive)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterOutputRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputActive.html#MediaConnect.Waiter.OutputActive.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputactivewaiter)
        """

class OutputDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputDeleted.html#MediaConnect.Waiter.OutputDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputdeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterOutputRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputDeleted.html#MediaConnect.Waiter.OutputDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputdeletedwaiter)
        """

class OutputRoutedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputRouted.html#MediaConnect.Waiter.OutputRouted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputroutedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterOutputRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputRouted.html#MediaConnect.Waiter.OutputRouted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputroutedwaiter)
        """

class OutputStandbyWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputStandby.html#MediaConnect.Waiter.OutputStandby)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputstandbywaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterOutputRequestWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputStandby.html#MediaConnect.Waiter.OutputStandby.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputstandbywaiter)
        """

class OutputUnroutedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputUnrouted.html#MediaConnect.Waiter.OutputUnrouted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputunroutedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouterOutputRequestWaitExtraExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/OutputUnrouted.html#MediaConnect.Waiter.OutputUnrouted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#outputunroutedwaiter)
        """

class SourceEndpointConnectedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointConnected.html#MediaConnect.Waiter.SourceEndpointConnected)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointconnectedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSourceEndpointRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointConnected.html#MediaConnect.Waiter.SourceEndpointConnected.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointconnectedwaiter)
        """

class SourceEndpointConnectingWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointConnecting.html#MediaConnect.Waiter.SourceEndpointConnecting)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointconnectingwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSourceEndpointRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointConnecting.html#MediaConnect.Waiter.SourceEndpointConnecting.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointconnectingwaiter)
        """

class SourceEndpointDeregisteredWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointDeregistered.html#MediaConnect.Waiter.SourceEndpointDeregistered)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointderegisteredwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSourceEndpointRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointDeregistered.html#MediaConnect.Waiter.SourceEndpointDeregistered.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointderegisteredwaiter)
        """

class SourceEndpointDisconnectedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointDisconnected.html#MediaConnect.Waiter.SourceEndpointDisconnected)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointdisconnectedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSourceEndpointRequestWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointDisconnected.html#MediaConnect.Waiter.SourceEndpointDisconnected.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointdisconnectedwaiter)
        """

class SourceEndpointDisconnectingWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointDisconnecting.html#MediaConnect.Waiter.SourceEndpointDisconnecting)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointdisconnectingwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSourceEndpointRequestWaitExtraExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointDisconnecting.html#MediaConnect.Waiter.SourceEndpointDisconnecting.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointdisconnectingwaiter)
        """

class SourceEndpointRegisteredWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointRegistered.html#MediaConnect.Waiter.SourceEndpointRegistered)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointregisteredwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSourceEndpointRequestWaitExtraExtraExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/waiter/SourceEndpointRegistered.html#MediaConnect.Waiter.SourceEndpointRegistered.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/waiters/#sourceendpointregisteredwaiter)
        """
