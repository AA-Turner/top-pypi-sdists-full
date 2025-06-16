"""
Main interface for networkflowmonitor service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_networkflowmonitor import (
        Client,
        GetQueryResultsMonitorTopContributorsPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsDataPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsPaginator,
        ListMonitorsPaginator,
        ListScopesPaginator,
        NetworkFlowMonitorClient,
    )

    session = get_session()
    async with session.create_client("networkflowmonitor") as client:
        client: NetworkFlowMonitorClient
        ...


    get_query_results_monitor_top_contributors_paginator: GetQueryResultsMonitorTopContributorsPaginator = client.get_paginator("get_query_results_monitor_top_contributors")
    get_query_results_workload_insights_top_contributors_data_paginator: GetQueryResultsWorkloadInsightsTopContributorsDataPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors_data")
    get_query_results_workload_insights_top_contributors_paginator: GetQueryResultsWorkloadInsightsTopContributorsPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors")
    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    list_scopes_paginator: ListScopesPaginator = client.get_paginator("list_scopes")
    ```
"""

from .client import NetworkFlowMonitorClient
from .paginator import (
    GetQueryResultsMonitorTopContributorsPaginator,
    GetQueryResultsWorkloadInsightsTopContributorsDataPaginator,
    GetQueryResultsWorkloadInsightsTopContributorsPaginator,
    ListMonitorsPaginator,
    ListScopesPaginator,
)

Client = NetworkFlowMonitorClient


__all__ = (
    "Client",
    "GetQueryResultsMonitorTopContributorsPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsDataPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsPaginator",
    "ListMonitorsPaginator",
    "ListScopesPaginator",
    "NetworkFlowMonitorClient",
)
