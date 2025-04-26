"""
Main interface for stepfunctions service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_stepfunctions import (
        Client,
        GetExecutionHistoryPaginator,
        ListActivitiesPaginator,
        ListExecutionsPaginator,
        ListMapRunsPaginator,
        ListStateMachinesPaginator,
        SFNClient,
    )

    session = get_session()
    async with session.create_client("stepfunctions") as client:
        client: SFNClient
        ...


    get_execution_history_paginator: GetExecutionHistoryPaginator = client.get_paginator("get_execution_history")
    list_activities_paginator: ListActivitiesPaginator = client.get_paginator("list_activities")
    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_map_runs_paginator: ListMapRunsPaginator = client.get_paginator("list_map_runs")
    list_state_machines_paginator: ListStateMachinesPaginator = client.get_paginator("list_state_machines")
    ```
"""

from .client import SFNClient
from .paginator import (
    GetExecutionHistoryPaginator,
    ListActivitiesPaginator,
    ListExecutionsPaginator,
    ListMapRunsPaginator,
    ListStateMachinesPaginator,
)

Client = SFNClient

__all__ = (
    "Client",
    "GetExecutionHistoryPaginator",
    "ListActivitiesPaginator",
    "ListExecutionsPaginator",
    "ListMapRunsPaginator",
    "ListStateMachinesPaginator",
    "SFNClient",
)
