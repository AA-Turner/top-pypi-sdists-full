"""
Main interface for networkflowmonitor service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_networkflowmonitor import (
        Client,
        GetMonitorScopeSuggestionsPaginator,
        GetQueryResultsMonitorTopContributorsPaginator,
        GetQueryResultsPerformanceMonitorPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsDataPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsPaginator,
        ListMonitorsPaginator,
        ListPerformanceMonitorsPaginator,
        ListScopesPaginator,
        NetworkFlowMonitorClient,
    )

    session = Session()
    client: NetworkFlowMonitorClient = session.client("networkflowmonitor")

    get_monitor_scope_suggestions_paginator: GetMonitorScopeSuggestionsPaginator = client.get_paginator("get_monitor_scope_suggestions")
    get_query_results_monitor_top_contributors_paginator: GetQueryResultsMonitorTopContributorsPaginator = client.get_paginator("get_query_results_monitor_top_contributors")
    get_query_results_performance_monitor_paginator: GetQueryResultsPerformanceMonitorPaginator = client.get_paginator("get_query_results_performance_monitor")
    get_query_results_workload_insights_top_contributors_data_paginator: GetQueryResultsWorkloadInsightsTopContributorsDataPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors_data")
    get_query_results_workload_insights_top_contributors_paginator: GetQueryResultsWorkloadInsightsTopContributorsPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors")
    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    list_performance_monitors_paginator: ListPerformanceMonitorsPaginator = client.get_paginator("list_performance_monitors")
    list_scopes_paginator: ListScopesPaginator = client.get_paginator("list_scopes")
    ```
"""

from .client import NetworkFlowMonitorClient
from .paginator import (
    GetMonitorScopeSuggestionsPaginator,
    GetQueryResultsMonitorTopContributorsPaginator,
    GetQueryResultsPerformanceMonitorPaginator,
    GetQueryResultsWorkloadInsightsTopContributorsDataPaginator,
    GetQueryResultsWorkloadInsightsTopContributorsPaginator,
    ListMonitorsPaginator,
    ListPerformanceMonitorsPaginator,
    ListScopesPaginator,
)

Client = NetworkFlowMonitorClient

__all__ = (
    "Client",
    "GetMonitorScopeSuggestionsPaginator",
    "GetQueryResultsMonitorTopContributorsPaginator",
    "GetQueryResultsPerformanceMonitorPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsDataPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsPaginator",
    "ListMonitorsPaginator",
    "ListPerformanceMonitorsPaginator",
    "ListScopesPaginator",
    "NetworkFlowMonitorClient",
)
