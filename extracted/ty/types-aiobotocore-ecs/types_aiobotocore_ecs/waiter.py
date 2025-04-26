"""
Type annotations for ecs service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ecs.client import ECSClient
    from types_aiobotocore_ecs.waiter import (
        ServicesInactiveWaiter,
        ServicesStableWaiter,
        TasksRunningWaiter,
        TasksStoppedWaiter,
    )

    session = get_session()
    async with session.create_client("ecs") as client:
        client: ECSClient

        services_inactive_waiter: ServicesInactiveWaiter = client.get_waiter("services_inactive")
        services_stable_waiter: ServicesStableWaiter = client.get_waiter("services_stable")
        tasks_running_waiter: TasksRunningWaiter = client.get_waiter("tasks_running")
        tasks_stopped_waiter: TasksStoppedWaiter = client.get_waiter("tasks_stopped")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeServicesRequestWaitExtraTypeDef,
    DescribeServicesRequestWaitTypeDef,
    DescribeTasksRequestWaitExtraTypeDef,
    DescribeTasksRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ServicesInactiveWaiter",
    "ServicesStableWaiter",
    "TasksRunningWaiter",
    "TasksStoppedWaiter",
)


class ServicesInactiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesInactive.html#ECS.Waiter.ServicesInactive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#servicesinactivewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServicesRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesInactive.html#ECS.Waiter.ServicesInactive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#servicesinactivewaiter)
        """


class ServicesStableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesStable.html#ECS.Waiter.ServicesStable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#servicesstablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServicesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesStable.html#ECS.Waiter.ServicesStable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#servicesstablewaiter)
        """


class TasksRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksRunning.html#ECS.Waiter.TasksRunning)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#tasksrunningwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTasksRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksRunning.html#ECS.Waiter.TasksRunning.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#tasksrunningwaiter)
        """


class TasksStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksStopped.html#ECS.Waiter.TasksStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#tasksstoppedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTasksRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksStopped.html#ECS.Waiter.TasksStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#tasksstoppedwaiter)
        """
