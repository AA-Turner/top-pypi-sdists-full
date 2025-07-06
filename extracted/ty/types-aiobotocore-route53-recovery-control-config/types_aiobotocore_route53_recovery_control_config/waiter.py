"""
Type annotations for route53-recovery-control-config service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53_recovery_control_config.client import Route53RecoveryControlConfigClient
    from types_aiobotocore_route53_recovery_control_config.waiter import (
        ClusterCreatedWaiter,
        ClusterDeletedWaiter,
        ControlPanelCreatedWaiter,
        ControlPanelDeletedWaiter,
        RoutingControlCreatedWaiter,
        RoutingControlDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("route53-recovery-control-config") as client:
        client: Route53RecoveryControlConfigClient

        cluster_created_waiter: ClusterCreatedWaiter = client.get_waiter("cluster_created")
        cluster_deleted_waiter: ClusterDeletedWaiter = client.get_waiter("cluster_deleted")
        control_panel_created_waiter: ControlPanelCreatedWaiter = client.get_waiter("control_panel_created")
        control_panel_deleted_waiter: ControlPanelDeletedWaiter = client.get_waiter("control_panel_deleted")
        routing_control_created_waiter: RoutingControlCreatedWaiter = client.get_waiter("routing_control_created")
        routing_control_deleted_waiter: RoutingControlDeletedWaiter = client.get_waiter("routing_control_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeClusterRequestWaitExtraTypeDef,
    DescribeClusterRequestWaitTypeDef,
    DescribeControlPanelRequestWaitExtraTypeDef,
    DescribeControlPanelRequestWaitTypeDef,
    DescribeRoutingControlRequestWaitExtraTypeDef,
    DescribeRoutingControlRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ClusterCreatedWaiter",
    "ClusterDeletedWaiter",
    "ControlPanelCreatedWaiter",
    "ControlPanelDeletedWaiter",
    "RoutingControlCreatedWaiter",
    "RoutingControlDeletedWaiter",
)


class ClusterCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ClusterCreated.html#Route53RecoveryControlConfig.Waiter.ClusterCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#clustercreatedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClusterRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ClusterCreated.html#Route53RecoveryControlConfig.Waiter.ClusterCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#clustercreatedwaiter)
        """


class ClusterDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ClusterDeleted.html#Route53RecoveryControlConfig.Waiter.ClusterDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#clusterdeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClusterRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ClusterDeleted.html#Route53RecoveryControlConfig.Waiter.ClusterDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#clusterdeletedwaiter)
        """


class ControlPanelCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ControlPanelCreated.html#Route53RecoveryControlConfig.Waiter.ControlPanelCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#controlpanelcreatedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeControlPanelRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ControlPanelCreated.html#Route53RecoveryControlConfig.Waiter.ControlPanelCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#controlpanelcreatedwaiter)
        """


class ControlPanelDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ControlPanelDeleted.html#Route53RecoveryControlConfig.Waiter.ControlPanelDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#controlpaneldeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeControlPanelRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/ControlPanelDeleted.html#Route53RecoveryControlConfig.Waiter.ControlPanelDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#controlpaneldeletedwaiter)
        """


class RoutingControlCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/RoutingControlCreated.html#Route53RecoveryControlConfig.Waiter.RoutingControlCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#routingcontrolcreatedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRoutingControlRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/RoutingControlCreated.html#Route53RecoveryControlConfig.Waiter.RoutingControlCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#routingcontrolcreatedwaiter)
        """


class RoutingControlDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/RoutingControlDeleted.html#Route53RecoveryControlConfig.Waiter.RoutingControlDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#routingcontroldeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRoutingControlRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/waiter/RoutingControlDeleted.html#Route53RecoveryControlConfig.Waiter.RoutingControlDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/waiters/#routingcontroldeletedwaiter)
        """
