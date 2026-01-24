"""
Main interface for mwaa-serverless service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa_serverless/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mwaa_serverless import (
        Client,
        ListTaskInstancesPaginator,
        ListWorkflowRunsPaginator,
        ListWorkflowVersionsPaginator,
        ListWorkflowsPaginator,
        MWAAServerlessClient,
    )

    session = get_session()
    async with session.create_client("mwaa-serverless") as client:
        client: MWAAServerlessClient
        ...


    list_task_instances_paginator: ListTaskInstancesPaginator = client.get_paginator("list_task_instances")
    list_workflow_runs_paginator: ListWorkflowRunsPaginator = client.get_paginator("list_workflow_runs")
    list_workflow_versions_paginator: ListWorkflowVersionsPaginator = client.get_paginator("list_workflow_versions")
    list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

from .client import MWAAServerlessClient
from .paginator import (
    ListTaskInstancesPaginator,
    ListWorkflowRunsPaginator,
    ListWorkflowsPaginator,
    ListWorkflowVersionsPaginator,
)

Client = MWAAServerlessClient

__all__ = (
    "Client",
    "ListTaskInstancesPaginator",
    "ListWorkflowRunsPaginator",
    "ListWorkflowVersionsPaginator",
    "ListWorkflowsPaginator",
    "MWAAServerlessClient",
)
