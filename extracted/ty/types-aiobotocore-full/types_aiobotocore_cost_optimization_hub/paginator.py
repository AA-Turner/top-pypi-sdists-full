"""
Type annotations for cost-optimization-hub service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cost_optimization_hub.client import CostOptimizationHubClient
    from types_aiobotocore_cost_optimization_hub.paginator import (
        ListEfficiencyMetricsPaginator,
        ListEnrollmentStatusesPaginator,
        ListRecommendationSummariesPaginator,
        ListRecommendationsPaginator,
    )

    session = get_session()
    with session.create_client("cost-optimization-hub") as client:
        client: CostOptimizationHubClient

        list_efficiency_metrics_paginator: ListEfficiencyMetricsPaginator = client.get_paginator("list_efficiency_metrics")
        list_enrollment_statuses_paginator: ListEnrollmentStatusesPaginator = client.get_paginator("list_enrollment_statuses")
        list_recommendation_summaries_paginator: ListRecommendationSummariesPaginator = client.get_paginator("list_recommendation_summaries")
        list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListEfficiencyMetricsRequestPaginateTypeDef,
    ListEfficiencyMetricsResponseTypeDef,
    ListEnrollmentStatusesRequestPaginateTypeDef,
    ListEnrollmentStatusesResponseTypeDef,
    ListRecommendationsRequestPaginateTypeDef,
    ListRecommendationsResponseTypeDef,
    ListRecommendationSummariesRequestPaginateTypeDef,
    ListRecommendationSummariesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListEfficiencyMetricsPaginator",
    "ListEnrollmentStatusesPaginator",
    "ListRecommendationSummariesPaginator",
    "ListRecommendationsPaginator",
)


if TYPE_CHECKING:
    _ListEfficiencyMetricsPaginatorBase = AioPaginator[ListEfficiencyMetricsResponseTypeDef]
else:
    _ListEfficiencyMetricsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEfficiencyMetricsPaginator(_ListEfficiencyMetricsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/paginator/ListEfficiencyMetrics.html#CostOptimizationHub.Paginator.ListEfficiencyMetrics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/paginators/#listefficiencymetricspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEfficiencyMetricsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEfficiencyMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/paginator/ListEfficiencyMetrics.html#CostOptimizationHub.Paginator.ListEfficiencyMetrics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/paginators/#listefficiencymetricspaginator)
        """


if TYPE_CHECKING:
    _ListEnrollmentStatusesPaginatorBase = AioPaginator[ListEnrollmentStatusesResponseTypeDef]
else:
    _ListEnrollmentStatusesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnrollmentStatusesPaginator(_ListEnrollmentStatusesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/paginator/ListEnrollmentStatuses.html#CostOptimizationHub.Paginator.ListEnrollmentStatuses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/paginators/#listenrollmentstatusespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnrollmentStatusesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnrollmentStatusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/paginator/ListEnrollmentStatuses.html#CostOptimizationHub.Paginator.ListEnrollmentStatuses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/paginators/#listenrollmentstatusespaginator)
        """


if TYPE_CHECKING:
    _ListRecommendationSummariesPaginatorBase = AioPaginator[
        ListRecommendationSummariesResponseTypeDef
    ]
else:
    _ListRecommendationSummariesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecommendationSummariesPaginator(_ListRecommendationSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/paginator/ListRecommendationSummaries.html#CostOptimizationHub.Paginator.ListRecommendationSummaries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/paginators/#listrecommendationsummariespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecommendationSummariesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecommendationSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/paginator/ListRecommendationSummaries.html#CostOptimizationHub.Paginator.ListRecommendationSummaries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/paginators/#listrecommendationsummariespaginator)
        """


if TYPE_CHECKING:
    _ListRecommendationsPaginatorBase = AioPaginator[ListRecommendationsResponseTypeDef]
else:
    _ListRecommendationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecommendationsPaginator(_ListRecommendationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/paginator/ListRecommendations.html#CostOptimizationHub.Paginator.ListRecommendations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/paginators/#listrecommendationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecommendationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/paginator/ListRecommendations.html#CostOptimizationHub.Paginator.ListRecommendations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/paginators/#listrecommendationspaginator)
        """
