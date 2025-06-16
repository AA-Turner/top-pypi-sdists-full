"""
Type annotations for ce service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ce.client import CostExplorerClient
    from types_aiobotocore_ce.paginator import (
        GetAnomaliesPaginator,
        GetAnomalyMonitorsPaginator,
        GetAnomalySubscriptionsPaginator,
        GetCostAndUsageComparisonsPaginator,
        GetCostComparisonDriversPaginator,
    )

    session = get_session()
    with session.create_client("ce") as client:
        client: CostExplorerClient

        get_anomalies_paginator: GetAnomaliesPaginator = client.get_paginator("get_anomalies")
        get_anomaly_monitors_paginator: GetAnomalyMonitorsPaginator = client.get_paginator("get_anomaly_monitors")
        get_anomaly_subscriptions_paginator: GetAnomalySubscriptionsPaginator = client.get_paginator("get_anomaly_subscriptions")
        get_cost_and_usage_comparisons_paginator: GetCostAndUsageComparisonsPaginator = client.get_paginator("get_cost_and_usage_comparisons")
        get_cost_comparison_drivers_paginator: GetCostComparisonDriversPaginator = client.get_paginator("get_cost_comparison_drivers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetAnomaliesRequestPaginateTypeDef,
    GetAnomaliesResponseTypeDef,
    GetAnomalyMonitorsRequestPaginateTypeDef,
    GetAnomalyMonitorsResponsePaginatorTypeDef,
    GetAnomalySubscriptionsRequestPaginateTypeDef,
    GetAnomalySubscriptionsResponsePaginatorTypeDef,
    GetCostAndUsageComparisonsRequestPaginateTypeDef,
    GetCostAndUsageComparisonsResponsePaginatorTypeDef,
    GetCostComparisonDriversRequestPaginateTypeDef,
    GetCostComparisonDriversResponsePaginatorTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetAnomaliesPaginator",
    "GetAnomalyMonitorsPaginator",
    "GetAnomalySubscriptionsPaginator",
    "GetCostAndUsageComparisonsPaginator",
    "GetCostComparisonDriversPaginator",
)

if TYPE_CHECKING:
    _GetAnomaliesPaginatorBase = AioPaginator[GetAnomaliesResponseTypeDef]
else:
    _GetAnomaliesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetAnomaliesPaginator(_GetAnomaliesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalies.html#CostExplorer.Paginator.GetAnomalies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomaliespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAnomaliesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAnomaliesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalies.html#CostExplorer.Paginator.GetAnomalies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomaliespaginator)
        """

if TYPE_CHECKING:
    _GetAnomalyMonitorsPaginatorBase = AioPaginator[GetAnomalyMonitorsResponsePaginatorTypeDef]
else:
    _GetAnomalyMonitorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetAnomalyMonitorsPaginator(_GetAnomalyMonitorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalyMonitors.html#CostExplorer.Paginator.GetAnomalyMonitors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomalymonitorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAnomalyMonitorsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAnomalyMonitorsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalyMonitors.html#CostExplorer.Paginator.GetAnomalyMonitors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomalymonitorspaginator)
        """

if TYPE_CHECKING:
    _GetAnomalySubscriptionsPaginatorBase = AioPaginator[
        GetAnomalySubscriptionsResponsePaginatorTypeDef
    ]
else:
    _GetAnomalySubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetAnomalySubscriptionsPaginator(_GetAnomalySubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalySubscriptions.html#CostExplorer.Paginator.GetAnomalySubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomalysubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAnomalySubscriptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAnomalySubscriptionsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalySubscriptions.html#CostExplorer.Paginator.GetAnomalySubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomalysubscriptionspaginator)
        """

if TYPE_CHECKING:
    _GetCostAndUsageComparisonsPaginatorBase = AioPaginator[
        GetCostAndUsageComparisonsResponsePaginatorTypeDef
    ]
else:
    _GetCostAndUsageComparisonsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetCostAndUsageComparisonsPaginator(_GetCostAndUsageComparisonsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetCostAndUsageComparisons.html#CostExplorer.Paginator.GetCostAndUsageComparisons)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getcostandusagecomparisonspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCostAndUsageComparisonsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCostAndUsageComparisonsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetCostAndUsageComparisons.html#CostExplorer.Paginator.GetCostAndUsageComparisons.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getcostandusagecomparisonspaginator)
        """

if TYPE_CHECKING:
    _GetCostComparisonDriversPaginatorBase = AioPaginator[
        GetCostComparisonDriversResponsePaginatorTypeDef
    ]
else:
    _GetCostComparisonDriversPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetCostComparisonDriversPaginator(_GetCostComparisonDriversPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetCostComparisonDrivers.html#CostExplorer.Paginator.GetCostComparisonDrivers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getcostcomparisondriverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCostComparisonDriversRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCostComparisonDriversResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetCostComparisonDrivers.html#CostExplorer.Paginator.GetCostComparisonDrivers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getcostcomparisondriverspaginator)
        """
