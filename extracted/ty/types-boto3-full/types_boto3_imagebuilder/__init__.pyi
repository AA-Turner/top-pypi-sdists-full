"""
Main interface for imagebuilder service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_imagebuilder/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_imagebuilder import (
        Client,
        ImagebuilderClient,
        ListLifecycleExecutionResourcesPaginator,
        ListLifecycleExecutionsPaginator,
        ListLifecyclePoliciesPaginator,
        ListWaitingWorkflowStepsPaginator,
        ListWorkflowBuildVersionsPaginator,
        ListWorkflowsPaginator,
    )

    session = Session()
    client: ImagebuilderClient = session.client("imagebuilder")

    list_lifecycle_execution_resources_paginator: ListLifecycleExecutionResourcesPaginator = client.get_paginator("list_lifecycle_execution_resources")
    list_lifecycle_executions_paginator: ListLifecycleExecutionsPaginator = client.get_paginator("list_lifecycle_executions")
    list_lifecycle_policies_paginator: ListLifecyclePoliciesPaginator = client.get_paginator("list_lifecycle_policies")
    list_waiting_workflow_steps_paginator: ListWaitingWorkflowStepsPaginator = client.get_paginator("list_waiting_workflow_steps")
    list_workflow_build_versions_paginator: ListWorkflowBuildVersionsPaginator = client.get_paginator("list_workflow_build_versions")
    list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

from .client import ImagebuilderClient
from .paginator import (
    ListLifecycleExecutionResourcesPaginator,
    ListLifecycleExecutionsPaginator,
    ListLifecyclePoliciesPaginator,
    ListWaitingWorkflowStepsPaginator,
    ListWorkflowBuildVersionsPaginator,
    ListWorkflowsPaginator,
)

Client = ImagebuilderClient

__all__ = (
    "Client",
    "ImagebuilderClient",
    "ListLifecycleExecutionResourcesPaginator",
    "ListLifecycleExecutionsPaginator",
    "ListLifecyclePoliciesPaginator",
    "ListWaitingWorkflowStepsPaginator",
    "ListWorkflowBuildVersionsPaginator",
    "ListWorkflowsPaginator",
)
