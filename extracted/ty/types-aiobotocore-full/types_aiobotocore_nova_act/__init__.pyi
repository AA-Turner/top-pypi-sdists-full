"""
Main interface for nova-act service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_nova_act import (
        Client,
        ListActsPaginator,
        ListSessionsPaginator,
        ListWorkflowDefinitionsPaginator,
        ListWorkflowRunsPaginator,
        NovaActServiceClient,
    )

    session = get_session()
    async with session.create_client("nova-act") as client:
        client: NovaActServiceClient
        ...


    list_acts_paginator: ListActsPaginator = client.get_paginator("list_acts")
    list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
    list_workflow_definitions_paginator: ListWorkflowDefinitionsPaginator = client.get_paginator("list_workflow_definitions")
    list_workflow_runs_paginator: ListWorkflowRunsPaginator = client.get_paginator("list_workflow_runs")
    ```
"""

from .client import NovaActServiceClient
from .paginator import (
    ListActsPaginator,
    ListSessionsPaginator,
    ListWorkflowDefinitionsPaginator,
    ListWorkflowRunsPaginator,
)

Client = NovaActServiceClient

__all__ = (
    "Client",
    "ListActsPaginator",
    "ListSessionsPaginator",
    "ListWorkflowDefinitionsPaginator",
    "ListWorkflowRunsPaginator",
    "NovaActServiceClient",
)
