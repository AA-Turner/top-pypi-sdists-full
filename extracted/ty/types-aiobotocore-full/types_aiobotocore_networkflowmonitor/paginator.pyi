"""
Type annotations for networkflowmonitor service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_networkflowmonitor.client import NetworkFlowMonitorClient
    from types_aiobotocore_networkflowmonitor.paginator import (
        GetQueryResultsMonitorTopContributorsPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsDataPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsPaginator,
        ListMonitorsPaginator,
        ListScopesPaginator,
    )

    session = get_session()
    with session.create_client("networkflowmonitor") as client:
        client: NetworkFlowMonitorClient

        get_query_results_monitor_top_contributors_paginator: GetQueryResultsMonitorTopContributorsPaginator = client.get_paginator("get_query_results_monitor_top_contributors")
        get_query_results_workload_insights_top_contributors_data_paginator: GetQueryResultsWorkloadInsightsTopContributorsDataPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors_data")
        get_query_results_workload_insights_top_contributors_paginator: GetQueryResultsWorkloadInsightsTopContributorsPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors")
        list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
        list_scopes_paginator: ListScopesPaginator = client.get_paginator("list_scopes")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetQueryResultsMonitorTopContributorsInputPaginateTypeDef,
    GetQueryResultsMonitorTopContributorsOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataInputPaginateTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsInputPaginateTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef,
    ListMonitorsInputPaginateTypeDef,
    ListMonitorsOutputTypeDef,
    ListScopesInputPaginateTypeDef,
    ListScopesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetQueryResultsMonitorTopContributorsPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsDataPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsPaginator",
    "ListMonitorsPaginator",
    "ListScopesPaginator",
)

if TYPE_CHECKING:
    _GetQueryResultsMonitorTopContributorsPaginatorBase = AioPaginator[
        GetQueryResultsMonitorTopContributorsOutputTypeDef
    ]
else:
    _GetQueryResultsMonitorTopContributorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetQueryResultsMonitorTopContributorsPaginator(
    _GetQueryResultsMonitorTopContributorsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsMonitorTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsMonitorTopContributors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsmonitortopcontributorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueryResultsMonitorTopContributorsInputPaginateTypeDef]
    ) -> AioPageIterator[GetQueryResultsMonitorTopContributorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsMonitorTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsMonitorTopContributors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsmonitortopcontributorspaginator)
        """

if TYPE_CHECKING:
    _GetQueryResultsWorkloadInsightsTopContributorsDataPaginatorBase = AioPaginator[
        GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef
    ]
else:
    _GetQueryResultsWorkloadInsightsTopContributorsDataPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetQueryResultsWorkloadInsightsTopContributorsDataPaginator(
    _GetQueryResultsWorkloadInsightsTopContributorsDataPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributorsData.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributorsData)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorsdatapaginator)
    """
    def paginate(  # type: ignore[override]
        self,
        **kwargs: Unpack[GetQueryResultsWorkloadInsightsTopContributorsDataInputPaginateTypeDef],
    ) -> AioPageIterator[GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributorsData.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributorsData.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorsdatapaginator)
        """

if TYPE_CHECKING:
    _GetQueryResultsWorkloadInsightsTopContributorsPaginatorBase = AioPaginator[
        GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef
    ]
else:
    _GetQueryResultsWorkloadInsightsTopContributorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetQueryResultsWorkloadInsightsTopContributorsPaginator(
    _GetQueryResultsWorkloadInsightsTopContributorsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueryResultsWorkloadInsightsTopContributorsInputPaginateTypeDef]
    ) -> AioPageIterator[GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorspaginator)
        """

if TYPE_CHECKING:
    _ListMonitorsPaginatorBase = AioPaginator[ListMonitorsOutputTypeDef]
else:
    _ListMonitorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMonitorsPaginator(_ListMonitorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListMonitors.html#NetworkFlowMonitor.Paginator.ListMonitors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#listmonitorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitorsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListMonitors.html#NetworkFlowMonitor.Paginator.ListMonitors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#listmonitorspaginator)
        """

if TYPE_CHECKING:
    _ListScopesPaginatorBase = AioPaginator[ListScopesOutputTypeDef]
else:
    _ListScopesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListScopesPaginator(_ListScopesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListScopes.html#NetworkFlowMonitor.Paginator.ListScopes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#listscopespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScopesInputPaginateTypeDef]
    ) -> AioPageIterator[ListScopesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListScopes.html#NetworkFlowMonitor.Paginator.ListScopes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#listscopespaginator)
        """
