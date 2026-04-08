"""
Main interface for devops-agent service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_devops_agent import (
        Client,
        DevOpsAgentServiceClient,
        ListAgentSpacesPaginator,
        ListAssociationsPaginator,
        ListBacklogTasksPaginator,
        ListExecutionsPaginator,
        ListGoalsPaginator,
        ListJournalRecordsPaginator,
        ListServicesPaginator,
    )

    session = get_session()
    async with session.create_client("devops-agent") as client:
        client: DevOpsAgentServiceClient
        ...


    list_agent_spaces_paginator: ListAgentSpacesPaginator = client.get_paginator("list_agent_spaces")
    list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
    list_backlog_tasks_paginator: ListBacklogTasksPaginator = client.get_paginator("list_backlog_tasks")
    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_goals_paginator: ListGoalsPaginator = client.get_paginator("list_goals")
    list_journal_records_paginator: ListJournalRecordsPaginator = client.get_paginator("list_journal_records")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from .client import DevOpsAgentServiceClient
from .paginator import (
    ListAgentSpacesPaginator,
    ListAssociationsPaginator,
    ListBacklogTasksPaginator,
    ListExecutionsPaginator,
    ListGoalsPaginator,
    ListJournalRecordsPaginator,
    ListServicesPaginator,
)

Client = DevOpsAgentServiceClient

__all__ = (
    "Client",
    "DevOpsAgentServiceClient",
    "ListAgentSpacesPaginator",
    "ListAssociationsPaginator",
    "ListBacklogTasksPaginator",
    "ListExecutionsPaginator",
    "ListGoalsPaginator",
    "ListJournalRecordsPaginator",
    "ListServicesPaginator",
)
