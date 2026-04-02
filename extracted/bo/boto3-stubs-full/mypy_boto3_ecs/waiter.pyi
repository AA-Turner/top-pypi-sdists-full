"""
Type annotations for ecs service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ecs.client import ECSClient
    from mypy_boto3_ecs.waiter import (
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

    session = Session()
    client: ECSClient = session.client("ecs")

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

from botocore.waiter import Waiter

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

class DaemonActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonActive.html#ECS.Waiter.DaemonActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemonactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonActive.html#ECS.Waiter.DaemonActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemonactivewaiter)
        """

class DaemonDeploymentStoppedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonDeploymentStopped.html#ECS.Waiter.DaemonDeploymentStopped)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemondeploymentstoppedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonDeploymentsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonDeploymentStopped.html#ECS.Waiter.DaemonDeploymentStopped.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemondeploymentstoppedwaiter)
        """

class DaemonDeploymentSuccessfulWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonDeploymentSuccessful.html#ECS.Waiter.DaemonDeploymentSuccessful)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemondeploymentsuccessfulwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonDeploymentsRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonDeploymentSuccessful.html#ECS.Waiter.DaemonDeploymentSuccessful.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemondeploymentsuccessfulwaiter)
        """

class DaemonTaskDefinitionActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonTaskDefinitionActive.html#ECS.Waiter.DaemonTaskDefinitionActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemontaskdefinitionactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonTaskDefinitionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonTaskDefinitionActive.html#ECS.Waiter.DaemonTaskDefinitionActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemontaskdefinitionactivewaiter)
        """

class DaemonTaskDefinitionDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonTaskDefinitionDeleted.html#ECS.Waiter.DaemonTaskDefinitionDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemontaskdefinitiondeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDaemonTaskDefinitionRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/DaemonTaskDefinitionDeleted.html#ECS.Waiter.DaemonTaskDefinitionDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#daemontaskdefinitiondeletedwaiter)
        """

class ServicesInactiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesInactive.html#ECS.Waiter.ServicesInactive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#servicesinactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServicesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesInactive.html#ECS.Waiter.ServicesInactive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#servicesinactivewaiter)
        """

class ServicesStableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesStable.html#ECS.Waiter.ServicesStable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#servicesstablewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServicesRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesStable.html#ECS.Waiter.ServicesStable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#servicesstablewaiter)
        """

class TasksRunningWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksRunning.html#ECS.Waiter.TasksRunning)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#tasksrunningwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTasksRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksRunning.html#ECS.Waiter.TasksRunning.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#tasksrunningwaiter)
        """

class TasksStoppedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksStopped.html#ECS.Waiter.TasksStopped)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#tasksstoppedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTasksRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksStopped.html#ECS.Waiter.TasksStopped.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#tasksstoppedwaiter)
        """
