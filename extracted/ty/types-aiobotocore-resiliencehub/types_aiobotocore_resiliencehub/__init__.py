"""
Main interface for resiliencehub service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_resiliencehub import (
        Client,
        ListAppAssessmentResourceDriftsPaginator,
        ListMetricsPaginator,
        ListResourceGroupingRecommendationsPaginator,
        ResilienceHubClient,
    )

    session = get_session()
    async with session.create_client("resiliencehub") as client:
        client: ResilienceHubClient
        ...


    list_app_assessment_resource_drifts_paginator: ListAppAssessmentResourceDriftsPaginator = client.get_paginator("list_app_assessment_resource_drifts")
    list_metrics_paginator: ListMetricsPaginator = client.get_paginator("list_metrics")
    list_resource_grouping_recommendations_paginator: ListResourceGroupingRecommendationsPaginator = client.get_paginator("list_resource_grouping_recommendations")
    ```
"""

from .client import ResilienceHubClient
from .paginator import (
    ListAppAssessmentResourceDriftsPaginator,
    ListMetricsPaginator,
    ListResourceGroupingRecommendationsPaginator,
)

Client = ResilienceHubClient


__all__ = (
    "Client",
    "ListAppAssessmentResourceDriftsPaginator",
    "ListMetricsPaginator",
    "ListResourceGroupingRecommendationsPaginator",
    "ResilienceHubClient",
)
