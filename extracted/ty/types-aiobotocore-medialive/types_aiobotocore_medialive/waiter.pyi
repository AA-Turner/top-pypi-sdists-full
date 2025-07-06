"""
Type annotations for medialive service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_medialive.client import MediaLiveClient
    from types_aiobotocore_medialive.waiter import (
        ChannelCreatedWaiter,
        ChannelDeletedWaiter,
        ChannelPlacementGroupAssignedWaiter,
        ChannelPlacementGroupDeletedWaiter,
        ChannelPlacementGroupUnassignedWaiter,
        ChannelRunningWaiter,
        ChannelStoppedWaiter,
        ClusterCreatedWaiter,
        ClusterDeletedWaiter,
        InputAttachedWaiter,
        InputDeletedWaiter,
        InputDetachedWaiter,
        MultiplexCreatedWaiter,
        MultiplexDeletedWaiter,
        MultiplexRunningWaiter,
        MultiplexStoppedWaiter,
        NodeDeregisteredWaiter,
        NodeRegisteredWaiter,
        SignalMapCreatedWaiter,
        SignalMapMonitorDeletedWaiter,
        SignalMapMonitorDeployedWaiter,
        SignalMapUpdatedWaiter,
    )

    session = get_session()
    async with session.create_client("medialive") as client:
        client: MediaLiveClient

        channel_created_waiter: ChannelCreatedWaiter = client.get_waiter("channel_created")
        channel_deleted_waiter: ChannelDeletedWaiter = client.get_waiter("channel_deleted")
        channel_placement_group_assigned_waiter: ChannelPlacementGroupAssignedWaiter = client.get_waiter("channel_placement_group_assigned")
        channel_placement_group_deleted_waiter: ChannelPlacementGroupDeletedWaiter = client.get_waiter("channel_placement_group_deleted")
        channel_placement_group_unassigned_waiter: ChannelPlacementGroupUnassignedWaiter = client.get_waiter("channel_placement_group_unassigned")
        channel_running_waiter: ChannelRunningWaiter = client.get_waiter("channel_running")
        channel_stopped_waiter: ChannelStoppedWaiter = client.get_waiter("channel_stopped")
        cluster_created_waiter: ClusterCreatedWaiter = client.get_waiter("cluster_created")
        cluster_deleted_waiter: ClusterDeletedWaiter = client.get_waiter("cluster_deleted")
        input_attached_waiter: InputAttachedWaiter = client.get_waiter("input_attached")
        input_deleted_waiter: InputDeletedWaiter = client.get_waiter("input_deleted")
        input_detached_waiter: InputDetachedWaiter = client.get_waiter("input_detached")
        multiplex_created_waiter: MultiplexCreatedWaiter = client.get_waiter("multiplex_created")
        multiplex_deleted_waiter: MultiplexDeletedWaiter = client.get_waiter("multiplex_deleted")
        multiplex_running_waiter: MultiplexRunningWaiter = client.get_waiter("multiplex_running")
        multiplex_stopped_waiter: MultiplexStoppedWaiter = client.get_waiter("multiplex_stopped")
        node_deregistered_waiter: NodeDeregisteredWaiter = client.get_waiter("node_deregistered")
        node_registered_waiter: NodeRegisteredWaiter = client.get_waiter("node_registered")
        signal_map_created_waiter: SignalMapCreatedWaiter = client.get_waiter("signal_map_created")
        signal_map_monitor_deleted_waiter: SignalMapMonitorDeletedWaiter = client.get_waiter("signal_map_monitor_deleted")
        signal_map_monitor_deployed_waiter: SignalMapMonitorDeployedWaiter = client.get_waiter("signal_map_monitor_deployed")
        signal_map_updated_waiter: SignalMapUpdatedWaiter = client.get_waiter("signal_map_updated")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeChannelPlacementGroupRequestWaitExtraExtraTypeDef,
    DescribeChannelPlacementGroupRequestWaitExtraTypeDef,
    DescribeChannelPlacementGroupRequestWaitTypeDef,
    DescribeChannelRequestWaitExtraExtraExtraTypeDef,
    DescribeChannelRequestWaitExtraExtraTypeDef,
    DescribeChannelRequestWaitExtraTypeDef,
    DescribeChannelRequestWaitTypeDef,
    DescribeClusterRequestWaitExtraTypeDef,
    DescribeClusterRequestWaitTypeDef,
    DescribeInputRequestWaitExtraExtraTypeDef,
    DescribeInputRequestWaitExtraTypeDef,
    DescribeInputRequestWaitTypeDef,
    DescribeMultiplexRequestWaitExtraExtraExtraTypeDef,
    DescribeMultiplexRequestWaitExtraExtraTypeDef,
    DescribeMultiplexRequestWaitExtraTypeDef,
    DescribeMultiplexRequestWaitTypeDef,
    DescribeNodeRequestWaitExtraTypeDef,
    DescribeNodeRequestWaitTypeDef,
    GetSignalMapRequestWaitExtraExtraExtraTypeDef,
    GetSignalMapRequestWaitExtraExtraTypeDef,
    GetSignalMapRequestWaitExtraTypeDef,
    GetSignalMapRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ChannelCreatedWaiter",
    "ChannelDeletedWaiter",
    "ChannelPlacementGroupAssignedWaiter",
    "ChannelPlacementGroupDeletedWaiter",
    "ChannelPlacementGroupUnassignedWaiter",
    "ChannelRunningWaiter",
    "ChannelStoppedWaiter",
    "ClusterCreatedWaiter",
    "ClusterDeletedWaiter",
    "InputAttachedWaiter",
    "InputDeletedWaiter",
    "InputDetachedWaiter",
    "MultiplexCreatedWaiter",
    "MultiplexDeletedWaiter",
    "MultiplexRunningWaiter",
    "MultiplexStoppedWaiter",
    "NodeDeregisteredWaiter",
    "NodeRegisteredWaiter",
    "SignalMapCreatedWaiter",
    "SignalMapMonitorDeletedWaiter",
    "SignalMapMonitorDeployedWaiter",
    "SignalMapUpdatedWaiter",
)

class ChannelCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelCreated.html#MediaLive.Waiter.ChannelCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelcreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChannelRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelCreated.html#MediaLive.Waiter.ChannelCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelcreatedwaiter)
        """

class ChannelDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelDeleted.html#MediaLive.Waiter.ChannelDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channeldeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChannelRequestWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelDeleted.html#MediaLive.Waiter.ChannelDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channeldeletedwaiter)
        """

class ChannelPlacementGroupAssignedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelPlacementGroupAssigned.html#MediaLive.Waiter.ChannelPlacementGroupAssigned)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelplacementgroupassignedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChannelPlacementGroupRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelPlacementGroupAssigned.html#MediaLive.Waiter.ChannelPlacementGroupAssigned.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelplacementgroupassignedwaiter)
        """

class ChannelPlacementGroupDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelPlacementGroupDeleted.html#MediaLive.Waiter.ChannelPlacementGroupDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelplacementgroupdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChannelPlacementGroupRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelPlacementGroupDeleted.html#MediaLive.Waiter.ChannelPlacementGroupDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelplacementgroupdeletedwaiter)
        """

class ChannelPlacementGroupUnassignedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelPlacementGroupUnassigned.html#MediaLive.Waiter.ChannelPlacementGroupUnassigned)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelplacementgroupunassignedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChannelPlacementGroupRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelPlacementGroupUnassigned.html#MediaLive.Waiter.ChannelPlacementGroupUnassigned.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelplacementgroupunassignedwaiter)
        """

class ChannelRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelRunning.html#MediaLive.Waiter.ChannelRunning)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelrunningwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChannelRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelRunning.html#MediaLive.Waiter.ChannelRunning.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelrunningwaiter)
        """

class ChannelStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelStopped.html#MediaLive.Waiter.ChannelStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelstoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChannelRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ChannelStopped.html#MediaLive.Waiter.ChannelStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelstoppedwaiter)
        """

class ClusterCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ClusterCreated.html#MediaLive.Waiter.ClusterCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#clustercreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClusterRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ClusterCreated.html#MediaLive.Waiter.ClusterCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#clustercreatedwaiter)
        """

class ClusterDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ClusterDeleted.html#MediaLive.Waiter.ClusterDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#clusterdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClusterRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/ClusterDeleted.html#MediaLive.Waiter.ClusterDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#clusterdeletedwaiter)
        """

class InputAttachedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/InputAttached.html#MediaLive.Waiter.InputAttached)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputattachedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInputRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/InputAttached.html#MediaLive.Waiter.InputAttached.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputattachedwaiter)
        """

class InputDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/InputDeleted.html#MediaLive.Waiter.InputDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInputRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/InputDeleted.html#MediaLive.Waiter.InputDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputdeletedwaiter)
        """

class InputDetachedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/InputDetached.html#MediaLive.Waiter.InputDetached)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputdetachedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInputRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/InputDetached.html#MediaLive.Waiter.InputDetached.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputdetachedwaiter)
        """

class MultiplexCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/MultiplexCreated.html#MediaLive.Waiter.MultiplexCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexcreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMultiplexRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/MultiplexCreated.html#MediaLive.Waiter.MultiplexCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexcreatedwaiter)
        """

class MultiplexDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/MultiplexDeleted.html#MediaLive.Waiter.MultiplexDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMultiplexRequestWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/MultiplexDeleted.html#MediaLive.Waiter.MultiplexDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexdeletedwaiter)
        """

class MultiplexRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/MultiplexRunning.html#MediaLive.Waiter.MultiplexRunning)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexrunningwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMultiplexRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/MultiplexRunning.html#MediaLive.Waiter.MultiplexRunning.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexrunningwaiter)
        """

class MultiplexStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/MultiplexStopped.html#MediaLive.Waiter.MultiplexStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexstoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMultiplexRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/MultiplexStopped.html#MediaLive.Waiter.MultiplexStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexstoppedwaiter)
        """

class NodeDeregisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/NodeDeregistered.html#MediaLive.Waiter.NodeDeregistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#nodederegisteredwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNodeRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/NodeDeregistered.html#MediaLive.Waiter.NodeDeregistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#nodederegisteredwaiter)
        """

class NodeRegisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/NodeRegistered.html#MediaLive.Waiter.NodeRegistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#noderegisteredwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNodeRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/NodeRegistered.html#MediaLive.Waiter.NodeRegistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#noderegisteredwaiter)
        """

class SignalMapCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/SignalMapCreated.html#MediaLive.Waiter.SignalMapCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#signalmapcreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSignalMapRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/SignalMapCreated.html#MediaLive.Waiter.SignalMapCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#signalmapcreatedwaiter)
        """

class SignalMapMonitorDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/SignalMapMonitorDeleted.html#MediaLive.Waiter.SignalMapMonitorDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#signalmapmonitordeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSignalMapRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/SignalMapMonitorDeleted.html#MediaLive.Waiter.SignalMapMonitorDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#signalmapmonitordeletedwaiter)
        """

class SignalMapMonitorDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/SignalMapMonitorDeployed.html#MediaLive.Waiter.SignalMapMonitorDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#signalmapmonitordeployedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSignalMapRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/SignalMapMonitorDeployed.html#MediaLive.Waiter.SignalMapMonitorDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#signalmapmonitordeployedwaiter)
        """

class SignalMapUpdatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/SignalMapUpdated.html#MediaLive.Waiter.SignalMapUpdated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#signalmapupdatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetSignalMapRequestWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/waiter/SignalMapUpdated.html#MediaLive.Waiter.SignalMapUpdated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#signalmapupdatedwaiter)
        """
