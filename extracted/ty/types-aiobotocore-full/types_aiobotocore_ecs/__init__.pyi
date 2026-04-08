"""
Main interface for ecs service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ecs import (
        Client,
        DaemonActiveWaiter,
        DaemonDeploymentStoppedWaiter,
        DaemonDeploymentSuccessfulWaiter,
        DaemonTaskDefinitionActiveWaiter,
        DaemonTaskDefinitionDeletedWaiter,
        ECSClient,
        ListAccountSettingsPaginator,
        ListAttributesPaginator,
        ListClustersPaginator,
        ListContainerInstancesPaginator,
        ListServicesByNamespacePaginator,
        ListServicesPaginator,
        ListTaskDefinitionFamiliesPaginator,
        ListTaskDefinitionsPaginator,
        ListTasksPaginator,
        ServicesInactiveWaiter,
        ServicesStableWaiter,
        TasksRunningWaiter,
        TasksStoppedWaiter,
    )

    session = get_session()
    async with session.create_client("ecs") as client:
        client: ECSClient
        ...


    daemon_active_waiter: DaemonActiveWaiter = client.get_waiter("daemon_active")
    daemon_deployment_stopped_waiter: DaemonDeploymentStoppedWaiter = client.get_waiter("daemon_deployment_stopped")
    daemon_deployment_successful_waiter: DaemonDeploymentSuccessfulWaiter = client.get_waiter("daemon_deployment_successful")
    daemon_task_definition_active_waiter: DaemonTaskDefinitionActiveWaiter = client.get_waiter("daemon_task_definition_active")
    daemon_task_definition_deleted_waiter: DaemonTaskDefinitionDeletedWaiter = client.get_waiter("daemon_task_definition_deleted")
    services_inactive_waiter: ServicesInactiveWaiter = client.get_waiter("services_inactive")
    services_stable_waiter: ServicesStableWaiter = client.get_waiter("services_stable")
    tasks_running_waiter: TasksRunningWaiter = client.get_waiter("tasks_running")
    tasks_stopped_waiter: TasksStoppedWaiter = client.get_waiter("tasks_stopped")

    list_account_settings_paginator: ListAccountSettingsPaginator = client.get_paginator("list_account_settings")
    list_attributes_paginator: ListAttributesPaginator = client.get_paginator("list_attributes")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_container_instances_paginator: ListContainerInstancesPaginator = client.get_paginator("list_container_instances")
    list_services_by_namespace_paginator: ListServicesByNamespacePaginator = client.get_paginator("list_services_by_namespace")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    list_task_definition_families_paginator: ListTaskDefinitionFamiliesPaginator = client.get_paginator("list_task_definition_families")
    list_task_definitions_paginator: ListTaskDefinitionsPaginator = client.get_paginator("list_task_definitions")
    list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```
"""

from .client import ECSClient
from .paginator import (
    ListAccountSettingsPaginator,
    ListAttributesPaginator,
    ListClustersPaginator,
    ListContainerInstancesPaginator,
    ListServicesByNamespacePaginator,
    ListServicesPaginator,
    ListTaskDefinitionFamiliesPaginator,
    ListTaskDefinitionsPaginator,
    ListTasksPaginator,
)
from .waiter import (
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

Client = ECSClient

__all__ = (
    "Client",
    "DaemonActiveWaiter",
    "DaemonDeploymentStoppedWaiter",
    "DaemonDeploymentSuccessfulWaiter",
    "DaemonTaskDefinitionActiveWaiter",
    "DaemonTaskDefinitionDeletedWaiter",
    "ECSClient",
    "ListAccountSettingsPaginator",
    "ListAttributesPaginator",
    "ListClustersPaginator",
    "ListContainerInstancesPaginator",
    "ListServicesByNamespacePaginator",
    "ListServicesPaginator",
    "ListTaskDefinitionFamiliesPaginator",
    "ListTaskDefinitionsPaginator",
    "ListTasksPaginator",
    "ServicesInactiveWaiter",
    "ServicesStableWaiter",
    "TasksRunningWaiter",
    "TasksStoppedWaiter",
)
