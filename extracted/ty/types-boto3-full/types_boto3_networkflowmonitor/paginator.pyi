"""
Type annotations for networkflowmonitor service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_networkflowmonitor.client import NetworkFlowMonitorClient
    from types_boto3_networkflowmonitor.paginator import (
        GetMonitorScopeSuggestionsPaginator,
        GetQueryResultsMonitorTopContributorsPaginator,
        GetQueryResultsPerformanceMonitorPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsDataPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsPaginator,
        ListMonitorsPaginator,
        ListPerformanceMonitorsPaginator,
        ListScopesPaginator,
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

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetMonitorScopeSuggestionsInputPaginateTypeDef,
    GetMonitorScopeSuggestionsOutputTypeDef,
    GetQueryResultsMonitorTopContributorsInputPaginateTypeDef,
    GetQueryResultsMonitorTopContributorsOutputTypeDef,
    GetQueryResultsPerformanceMonitorInputPaginateTypeDef,
    GetQueryResultsPerformanceMonitorOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataInputPaginateTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsInputPaginateTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef,
    ListMonitorsInputPaginateTypeDef,
    ListMonitorsOutputTypeDef,
    ListPerformanceMonitorsInputPaginateTypeDef,
    ListPerformanceMonitorsOutputTypeDef,
    ListScopesInputPaginateTypeDef,
    ListScopesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetMonitorScopeSuggestionsPaginator",
    "GetQueryResultsMonitorTopContributorsPaginator",
    "GetQueryResultsPerformanceMonitorPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsDataPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsPaginator",
    "ListMonitorsPaginator",
    "ListPerformanceMonitorsPaginator",
    "ListScopesPaginator",
)

if TYPE_CHECKING:
    _GetMonitorScopeSuggestionsPaginatorBase = Paginator[GetMonitorScopeSuggestionsOutputTypeDef]
else:
    _GetMonitorScopeSuggestionsPaginatorBase = Paginator  # type: ignore[assignment]

class GetMonitorScopeSuggestionsPaginator(_GetMonitorScopeSuggestionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetMonitorScopeSuggestions.html#NetworkFlowMonitor.Paginator.GetMonitorScopeSuggestions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getmonitorscopesuggestionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetMonitorScopeSuggestionsInputPaginateTypeDef]
    ) -> PageIterator[GetMonitorScopeSuggestionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetMonitorScopeSuggestions.html#NetworkFlowMonitor.Paginator.GetMonitorScopeSuggestions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getmonitorscopesuggestionspaginator)
        """

if TYPE_CHECKING:
    _GetQueryResultsMonitorTopContributorsPaginatorBase = Paginator[
        GetQueryResultsMonitorTopContributorsOutputTypeDef
    ]
else:
    _GetQueryResultsMonitorTopContributorsPaginatorBase = Paginator  # type: ignore[assignment]

class GetQueryResultsMonitorTopContributorsPaginator(
    _GetQueryResultsMonitorTopContributorsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsMonitorTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsMonitorTopContributors)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getqueryresultsmonitortopcontributorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueryResultsMonitorTopContributorsInputPaginateTypeDef]
    ) -> PageIterator[GetQueryResultsMonitorTopContributorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsMonitorTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsMonitorTopContributors.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getqueryresultsmonitortopcontributorspaginator)
        """

if TYPE_CHECKING:
    _GetQueryResultsPerformanceMonitorPaginatorBase = Paginator[
        GetQueryResultsPerformanceMonitorOutputTypeDef
    ]
else:
    _GetQueryResultsPerformanceMonitorPaginatorBase = Paginator  # type: ignore[assignment]

class GetQueryResultsPerformanceMonitorPaginator(_GetQueryResultsPerformanceMonitorPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsPerformanceMonitor.html#NetworkFlowMonitor.Paginator.GetQueryResultsPerformanceMonitor)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getqueryresultsperformancemonitorpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueryResultsPerformanceMonitorInputPaginateTypeDef]
    ) -> PageIterator[GetQueryResultsPerformanceMonitorOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsPerformanceMonitor.html#NetworkFlowMonitor.Paginator.GetQueryResultsPerformanceMonitor.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getqueryresultsperformancemonitorpaginator)
        """

if TYPE_CHECKING:
    _GetQueryResultsWorkloadInsightsTopContributorsDataPaginatorBase = Paginator[
        GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef
    ]
else:
    _GetQueryResultsWorkloadInsightsTopContributorsDataPaginatorBase = Paginator  # type: ignore[assignment]

class GetQueryResultsWorkloadInsightsTopContributorsDataPaginator(
    _GetQueryResultsWorkloadInsightsTopContributorsDataPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributorsData.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributorsData)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorsdatapaginator)
    """
    def paginate(  # type: ignore[override]
        self,
        **kwargs: Unpack[GetQueryResultsWorkloadInsightsTopContributorsDataInputPaginateTypeDef],
    ) -> PageIterator[GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributorsData.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributorsData.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorsdatapaginator)
        """

if TYPE_CHECKING:
    _GetQueryResultsWorkloadInsightsTopContributorsPaginatorBase = Paginator[
        GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef
    ]
else:
    _GetQueryResultsWorkloadInsightsTopContributorsPaginatorBase = Paginator  # type: ignore[assignment]

class GetQueryResultsWorkloadInsightsTopContributorsPaginator(
    _GetQueryResultsWorkloadInsightsTopContributorsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributors)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueryResultsWorkloadInsightsTopContributorsInputPaginateTypeDef]
    ) -> PageIterator[GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributors.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorspaginator)
        """

if TYPE_CHECKING:
    _ListMonitorsPaginatorBase = Paginator[ListMonitorsOutputTypeDef]
else:
    _ListMonitorsPaginatorBase = Paginator  # type: ignore[assignment]

class ListMonitorsPaginator(_ListMonitorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListMonitors.html#NetworkFlowMonitor.Paginator.ListMonitors)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#listmonitorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitorsInputPaginateTypeDef]
    ) -> PageIterator[ListMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListMonitors.html#NetworkFlowMonitor.Paginator.ListMonitors.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#listmonitorspaginator)
        """

if TYPE_CHECKING:
    _ListPerformanceMonitorsPaginatorBase = Paginator[ListPerformanceMonitorsOutputTypeDef]
else:
    _ListPerformanceMonitorsPaginatorBase = Paginator  # type: ignore[assignment]

class ListPerformanceMonitorsPaginator(_ListPerformanceMonitorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListPerformanceMonitors.html#NetworkFlowMonitor.Paginator.ListPerformanceMonitors)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#listperformancemonitorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPerformanceMonitorsInputPaginateTypeDef]
    ) -> PageIterator[ListPerformanceMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListPerformanceMonitors.html#NetworkFlowMonitor.Paginator.ListPerformanceMonitors.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#listperformancemonitorspaginator)
        """

if TYPE_CHECKING:
    _ListScopesPaginatorBase = Paginator[ListScopesOutputTypeDef]
else:
    _ListScopesPaginatorBase = Paginator  # type: ignore[assignment]

class ListScopesPaginator(_ListScopesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListScopes.html#NetworkFlowMonitor.Paginator.ListScopes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#listscopespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScopesInputPaginateTypeDef]
    ) -> PageIterator[ListScopesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListScopes.html#NetworkFlowMonitor.Paginator.ListScopes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkflowmonitor/paginators/#listscopespaginator)
        """
