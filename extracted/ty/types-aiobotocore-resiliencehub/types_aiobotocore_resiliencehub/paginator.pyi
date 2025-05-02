"""
Type annotations for resiliencehub service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resiliencehub.client import ResilienceHubClient
    from types_aiobotocore_resiliencehub.paginator import (
        ListAppAssessmentResourceDriftsPaginator,
        ListMetricsPaginator,
        ListResourceGroupingRecommendationsPaginator,
    )

    session = get_session()
    with session.create_client("resiliencehub") as client:
        client: ResilienceHubClient

        list_app_assessment_resource_drifts_paginator: ListAppAssessmentResourceDriftsPaginator = client.get_paginator("list_app_assessment_resource_drifts")
        list_metrics_paginator: ListMetricsPaginator = client.get_paginator("list_metrics")
        list_resource_grouping_recommendations_paginator: ListResourceGroupingRecommendationsPaginator = client.get_paginator("list_resource_grouping_recommendations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAppAssessmentResourceDriftsRequestPaginateTypeDef,
    ListAppAssessmentResourceDriftsResponseTypeDef,
    ListMetricsRequestPaginateTypeDef,
    ListMetricsResponseTypeDef,
    ListResourceGroupingRecommendationsRequestPaginateTypeDef,
    ListResourceGroupingRecommendationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAppAssessmentResourceDriftsPaginator",
    "ListMetricsPaginator",
    "ListResourceGroupingRecommendationsPaginator",
)

if TYPE_CHECKING:
    _ListAppAssessmentResourceDriftsPaginatorBase = AioPaginator[
        ListAppAssessmentResourceDriftsResponseTypeDef
    ]
else:
    _ListAppAssessmentResourceDriftsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAppAssessmentResourceDriftsPaginator(_ListAppAssessmentResourceDriftsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListAppAssessmentResourceDrifts.html#ResilienceHub.Paginator.ListAppAssessmentResourceDrifts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listappassessmentresourcedriftspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppAssessmentResourceDriftsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAppAssessmentResourceDriftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListAppAssessmentResourceDrifts.html#ResilienceHub.Paginator.ListAppAssessmentResourceDrifts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listappassessmentresourcedriftspaginator)
        """

if TYPE_CHECKING:
    _ListMetricsPaginatorBase = AioPaginator[ListMetricsResponseTypeDef]
else:
    _ListMetricsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMetricsPaginator(_ListMetricsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListMetrics.html#ResilienceHub.Paginator.ListMetrics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listmetricspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMetricsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListMetrics.html#ResilienceHub.Paginator.ListMetrics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listmetricspaginator)
        """

if TYPE_CHECKING:
    _ListResourceGroupingRecommendationsPaginatorBase = AioPaginator[
        ListResourceGroupingRecommendationsResponseTypeDef
    ]
else:
    _ListResourceGroupingRecommendationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceGroupingRecommendationsPaginator(
    _ListResourceGroupingRecommendationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListResourceGroupingRecommendations.html#ResilienceHub.Paginator.ListResourceGroupingRecommendations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listresourcegroupingrecommendationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceGroupingRecommendationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceGroupingRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListResourceGroupingRecommendations.html#ResilienceHub.Paginator.ListResourceGroupingRecommendations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listresourcegroupingrecommendationspaginator)
        """
