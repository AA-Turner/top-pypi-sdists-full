"""
Main interface for workspaces-instances service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workspaces_instances import (
        Client,
        ListInstanceTypesPaginator,
        ListRegionsPaginator,
        ListWorkspaceInstancesPaginator,
        WorkspacesInstancesClient,
    )

    session = get_session()
    async with session.create_client("workspaces-instances") as client:
        client: WorkspacesInstancesClient
        ...


    list_instance_types_paginator: ListInstanceTypesPaginator = client.get_paginator("list_instance_types")
    list_regions_paginator: ListRegionsPaginator = client.get_paginator("list_regions")
    list_workspace_instances_paginator: ListWorkspaceInstancesPaginator = client.get_paginator("list_workspace_instances")
    ```
"""

from .client import WorkspacesInstancesClient
from .paginator import (
    ListInstanceTypesPaginator,
    ListRegionsPaginator,
    ListWorkspaceInstancesPaginator,
)

Client = WorkspacesInstancesClient


__all__ = (
    "Client",
    "ListInstanceTypesPaginator",
    "ListRegionsPaginator",
    "ListWorkspaceInstancesPaginator",
    "WorkspacesInstancesClient",
)
