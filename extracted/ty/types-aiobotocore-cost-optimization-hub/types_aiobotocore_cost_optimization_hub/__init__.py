"""
Main interface for cost-optimization-hub service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cost_optimization_hub/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cost_optimization_hub import (
        Client,
        CostOptimizationHubClient,
        ListEfficiencyMetricsPaginator,
        ListEnrollmentStatusesPaginator,
        ListRecommendationSummariesPaginator,
        ListRecommendationsPaginator,
    )

    session = get_session()
    async with session.create_client("cost-optimization-hub") as client:
        client: CostOptimizationHubClient
        ...


    list_efficiency_metrics_paginator: ListEfficiencyMetricsPaginator = client.get_paginator("list_efficiency_metrics")
    list_enrollment_statuses_paginator: ListEnrollmentStatusesPaginator = client.get_paginator("list_enrollment_statuses")
    list_recommendation_summaries_paginator: ListRecommendationSummariesPaginator = client.get_paginator("list_recommendation_summaries")
    list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
    ```
"""

from .client import CostOptimizationHubClient
from .paginator import (
    ListEfficiencyMetricsPaginator,
    ListEnrollmentStatusesPaginator,
    ListRecommendationsPaginator,
    ListRecommendationSummariesPaginator,
)

Client = CostOptimizationHubClient


__all__ = (
    "Client",
    "CostOptimizationHubClient",
    "ListEfficiencyMetricsPaginator",
    "ListEnrollmentStatusesPaginator",
    "ListRecommendationSummariesPaginator",
    "ListRecommendationsPaginator",
)
