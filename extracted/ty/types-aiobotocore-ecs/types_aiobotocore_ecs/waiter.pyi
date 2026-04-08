"""
Type annotations for ecs service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ecs.client import ECSClient
    from types_aiobotocore_ecs.waiter import (
        DaemonActiveWaiter,
        DaemonDeploymentStoppedWaiter,
        DaemonDeploymentSuccessfulWaiter,
        DaemonTaskDefinitionActiveWaiter,
        DaemonTaskDefinitionDeletedWaiter,
        ServicesInactiveWaiter,
        ServicesStableWaiter,
        TasksRunningWaiter,
        TasksStoppedWaiter,
    )

    session = get_session()
    async with session.create_client("ecs") as client:
        client: ECSClient

        daemon_active_waiter: DaemonActiveWaiter = client.get_waiter("daemon_active")
        daemon_deployment_stopped_waiter: DaemonDeploymentStoppedWaiter = client.get_waiter("daemon_deployment_stopped")
        daemon_deployment_successful_waiter: DaemonDeploymentSuccessfulWaiter = client.get_waiter("daemon_deployment_successful")
        daemon_task_definition_active_waiter: DaemonTaskDefinitionActiveWaiter = client.get_waiter("daemon_task_definition_active")
        daemon_task_definition_deleted_waiter: DaemonTaskDefinitionDeletedWaiter = client.get_waiter("daemon_task_definition_deleted")
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
    DescribeDaemonDeploymentsRequestWaitExtraTypeDef,
    DescribeDaemonDeploymentsRequestWaitTypeDef,
    DescribeDaemonRequestWaitTypeDef,
    DescribeDaemonTaskDefinitionRequestWaitExtraTypeDef,
    DescribeDaemonTaskDefinitionRequestWaitTypeDef,
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
    "DaemonActiveWaiter",
    "DaemonDeploymentStoppedWaiter",
    "DaemonDeploymentSuccessfulWaiter",
    "DaemonTaskDefinitionActiveWaiter",
    "DaemonTaskDefinitionDeletedWaiter",
    "ServicesInactiveWaiter",
    "ServicesStableWaiter",
    "TasksRunningWaiter",
    "TasksStoppedWaiter",
)

class DaemonActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonActive.html#ECS.Waiter.DaemonActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemonactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonActive.html#ECS.Waiter.DaemonActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemonactivewaiter)
        """

class DaemonDeploymentStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonDeploymentStopped.html#ECS.Waiter.DaemonDeploymentStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemondeploymentstoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonDeploymentsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonDeploymentStopped.html#ECS.Waiter.DaemonDeploymentStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemondeploymentstoppedwaiter)
        """

class DaemonDeploymentSuccessfulWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonDeploymentSuccessful.html#ECS.Waiter.DaemonDeploymentSuccessful)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemondeploymentsuccessfulwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonDeploymentsRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonDeploymentSuccessful.html#ECS.Waiter.DaemonDeploymentSuccessful.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemondeploymentsuccessfulwaiter)
        """

class DaemonTaskDefinitionActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonTaskDefinitionActive.html#ECS.Waiter.DaemonTaskDefinitionActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemontaskdefinitionactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonTaskDefinitionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonTaskDefinitionActive.html#ECS.Waiter.DaemonTaskDefinitionActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemontaskdefinitionactivewaiter)
        """

class DaemonTaskDefinitionDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonTaskDefinitionDeleted.html#ECS.Waiter.DaemonTaskDefinitionDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemontaskdefinitiondeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonTaskDefinitionRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonTaskDefinitionDeleted.html#ECS.Waiter.DaemonTaskDefinitionDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#daemontaskdefinitiondeletedwaiter)
        """

class ServicesInactiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesInactive.html#ECS.Waiter.ServicesInactive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/waiters/#servicesinactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServicesRequestWaitTypeDef]
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
        self, **kwargs: Unpack[DescribeServicesRequestWaitExtraTypeDef]
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
