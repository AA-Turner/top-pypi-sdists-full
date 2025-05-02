"""
Type annotations for elb service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elb.client import ElasticLoadBalancingClient
    from types_aiobotocore_elb.waiter import (
        AnyInstanceInServiceWaiter,
        InstanceDeregisteredWaiter,
        InstanceInServiceWaiter,
    )

    session = get_session()
    async with session.create_client("elb") as client:
        client: ElasticLoadBalancingClient

        any_instance_in_service_waiter: AnyInstanceInServiceWaiter = client.get_waiter("any_instance_in_service")
        instance_deregistered_waiter: InstanceDeregisteredWaiter = client.get_waiter("instance_deregistered")
        instance_in_service_waiter: InstanceInServiceWaiter = client.get_waiter("instance_in_service")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeEndPointStateInputWaitExtraExtraTypeDef,
    DescribeEndPointStateInputWaitExtraTypeDef,
    DescribeEndPointStateInputWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("AnyInstanceInServiceWaiter", "InstanceDeregisteredWaiter", "InstanceInServiceWaiter")


class AnyInstanceInServiceWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/AnyInstanceInService.html#ElasticLoadBalancing.Waiter.AnyInstanceInService)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#anyinstanceinservicewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndPointStateInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/AnyInstanceInService.html#ElasticLoadBalancing.Waiter.AnyInstanceInService.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#anyinstanceinservicewaiter)
        """


class InstanceDeregisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/InstanceDeregistered.html#ElasticLoadBalancing.Waiter.InstanceDeregistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#instancederegisteredwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndPointStateInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/InstanceDeregistered.html#ElasticLoadBalancing.Waiter.InstanceDeregistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#instancederegisteredwaiter)
        """


class InstanceInServiceWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/InstanceInService.html#ElasticLoadBalancing.Waiter.InstanceInService)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#instanceinservicewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndPointStateInputWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/waiter/InstanceInService.html#ElasticLoadBalancing.Waiter.InstanceInService.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elb/waiters/#instanceinservicewaiter)
        """
