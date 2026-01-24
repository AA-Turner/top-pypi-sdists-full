"""
Main interface for ce service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ce/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ce import (
        Client,
        CostExplorerClient,
        GetAnomaliesPaginator,
        GetAnomalyMonitorsPaginator,
        GetAnomalySubscriptionsPaginator,
        GetCostAndUsageComparisonsPaginator,
        GetCostComparisonDriversPaginator,
        GetReservationPurchaseRecommendationPaginator,
        GetRightsizingRecommendationPaginator,
        ListCommitmentPurchaseAnalysesPaginator,
        ListCostAllocationTagBackfillHistoryPaginator,
        ListCostAllocationTagsPaginator,
        ListCostCategoryDefinitionsPaginator,
        ListCostCategoryResourceAssociationsPaginator,
        ListSavingsPlansPurchaseRecommendationGenerationPaginator,
    )

    session = Session()
    client: CostExplorerClient = session.client("ce")

    get_anomalies_paginator: GetAnomaliesPaginator = client.get_paginator("get_anomalies")
    get_anomaly_monitors_paginator: GetAnomalyMonitorsPaginator = client.get_paginator("get_anomaly_monitors")
    get_anomaly_subscriptions_paginator: GetAnomalySubscriptionsPaginator = client.get_paginator("get_anomaly_subscriptions")
    get_cost_and_usage_comparisons_paginator: GetCostAndUsageComparisonsPaginator = client.get_paginator("get_cost_and_usage_comparisons")
    get_cost_comparison_drivers_paginator: GetCostComparisonDriversPaginator = client.get_paginator("get_cost_comparison_drivers")
    get_reservation_purchase_recommendation_paginator: GetReservationPurchaseRecommendationPaginator = client.get_paginator("get_reservation_purchase_recommendation")
    get_rightsizing_recommendation_paginator: GetRightsizingRecommendationPaginator = client.get_paginator("get_rightsizing_recommendation")
    list_commitment_purchase_analyses_paginator: ListCommitmentPurchaseAnalysesPaginator = client.get_paginator("list_commitment_purchase_analyses")
    list_cost_allocation_tag_backfill_history_paginator: ListCostAllocationTagBackfillHistoryPaginator = client.get_paginator("list_cost_allocation_tag_backfill_history")
    list_cost_allocation_tags_paginator: ListCostAllocationTagsPaginator = client.get_paginator("list_cost_allocation_tags")
    list_cost_category_definitions_paginator: ListCostCategoryDefinitionsPaginator = client.get_paginator("list_cost_category_definitions")
    list_cost_category_resource_associations_paginator: ListCostCategoryResourceAssociationsPaginator = client.get_paginator("list_cost_category_resource_associations")
    list_savings_plans_purchase_recommendation_generation_paginator: ListSavingsPlansPurchaseRecommendationGenerationPaginator = client.get_paginator("list_savings_plans_purchase_recommendation_generation")
    ```
"""

from .client import CostExplorerClient
from .paginator import (
    GetAnomaliesPaginator,
    GetAnomalyMonitorsPaginator,
    GetAnomalySubscriptionsPaginator,
    GetCostAndUsageComparisonsPaginator,
    GetCostComparisonDriversPaginator,
    GetReservationPurchaseRecommendationPaginator,
    GetRightsizingRecommendationPaginator,
    ListCommitmentPurchaseAnalysesPaginator,
    ListCostAllocationTagBackfillHistoryPaginator,
    ListCostAllocationTagsPaginator,
    ListCostCategoryDefinitionsPaginator,
    ListCostCategoryResourceAssociationsPaginator,
    ListSavingsPlansPurchaseRecommendationGenerationPaginator,
)

Client = CostExplorerClient

__all__ = (
    "Client",
    "CostExplorerClient",
    "GetAnomaliesPaginator",
    "GetAnomalyMonitorsPaginator",
    "GetAnomalySubscriptionsPaginator",
    "GetCostAndUsageComparisonsPaginator",
    "GetCostComparisonDriversPaginator",
    "GetReservationPurchaseRecommendationPaginator",
    "GetRightsizingRecommendationPaginator",
    "ListCommitmentPurchaseAnalysesPaginator",
    "ListCostAllocationTagBackfillHistoryPaginator",
    "ListCostAllocationTagsPaginator",
    "ListCostCategoryDefinitionsPaginator",
    "ListCostCategoryResourceAssociationsPaginator",
    "ListSavingsPlansPurchaseRecommendationGenerationPaginator",
)
