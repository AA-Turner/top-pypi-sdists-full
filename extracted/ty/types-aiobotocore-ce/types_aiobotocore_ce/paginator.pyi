"""
Type annotations for ce service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/)

Copyright 2026 Vlad Emelianov

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
        GetReservationPurchaseRecommendationPaginator,
        GetRightsizingRecommendationPaginator,
        ListCommitmentPurchaseAnalysesPaginator,
        ListCostAllocationTagBackfillHistoryPaginator,
        ListCostAllocationTagsPaginator,
        ListCostCategoryDefinitionsPaginator,
        ListCostCategoryResourceAssociationsPaginator,
        ListSavingsPlansPurchaseRecommendationGenerationPaginator,
    )

    session = get_session()
    with session.create_client("ce") as client:
        client: CostExplorerClient

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
    GetReservationPurchaseRecommendationRequestPaginateTypeDef,
    GetReservationPurchaseRecommendationResponseTypeDef,
    GetRightsizingRecommendationRequestPaginateTypeDef,
    GetRightsizingRecommendationResponseTypeDef,
    ListCommitmentPurchaseAnalysesRequestPaginateTypeDef,
    ListCommitmentPurchaseAnalysesResponseTypeDef,
    ListCostAllocationTagBackfillHistoryRequestPaginateTypeDef,
    ListCostAllocationTagBackfillHistoryResponseTypeDef,
    ListCostAllocationTagsRequestPaginateTypeDef,
    ListCostAllocationTagsResponseTypeDef,
    ListCostCategoryDefinitionsRequestPaginateTypeDef,
    ListCostCategoryDefinitionsResponseTypeDef,
    ListCostCategoryResourceAssociationsRequestPaginateTypeDef,
    ListCostCategoryResourceAssociationsResponseTypeDef,
    ListSavingsPlansPurchaseRecommendationGenerationRequestPaginateTypeDef,
    ListSavingsPlansPurchaseRecommendationGenerationResponseTypeDef,
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
    "GetReservationPurchaseRecommendationPaginator",
    "GetRightsizingRecommendationPaginator",
    "ListCommitmentPurchaseAnalysesPaginator",
    "ListCostAllocationTagBackfillHistoryPaginator",
    "ListCostAllocationTagsPaginator",
    "ListCostCategoryDefinitionsPaginator",
    "ListCostCategoryResourceAssociationsPaginator",
    "ListSavingsPlansPurchaseRecommendationGenerationPaginator",
)

if TYPE_CHECKING:
    _GetAnomaliesPaginatorBase = AioPaginator[GetAnomaliesResponseTypeDef]
else:
    _GetAnomaliesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetAnomaliesPaginator(_GetAnomaliesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalies.html#CostExplorer.Paginator.GetAnomalies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomaliespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAnomaliesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAnomaliesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalies.html#CostExplorer.Paginator.GetAnomalies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomaliespaginator)
        """

if TYPE_CHECKING:
    _GetAnomalyMonitorsPaginatorBase = AioPaginator[GetAnomalyMonitorsResponsePaginatorTypeDef]
else:
    _GetAnomalyMonitorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetAnomalyMonitorsPaginator(_GetAnomalyMonitorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalyMonitors.html#CostExplorer.Paginator.GetAnomalyMonitors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomalymonitorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAnomalyMonitorsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAnomalyMonitorsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalyMonitors.html#CostExplorer.Paginator.GetAnomalyMonitors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomalymonitorspaginator)
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
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomalysubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAnomalySubscriptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAnomalySubscriptionsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetAnomalySubscriptions.html#CostExplorer.Paginator.GetAnomalySubscriptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getanomalysubscriptionspaginator)
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
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getcostandusagecomparisonspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCostAndUsageComparisonsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCostAndUsageComparisonsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetCostAndUsageComparisons.html#CostExplorer.Paginator.GetCostAndUsageComparisons.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getcostandusagecomparisonspaginator)
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
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getcostcomparisondriverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCostComparisonDriversRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCostComparisonDriversResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetCostComparisonDrivers.html#CostExplorer.Paginator.GetCostComparisonDrivers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getcostcomparisondriverspaginator)
        """

if TYPE_CHECKING:
    _GetReservationPurchaseRecommendationPaginatorBase = AioPaginator[
        GetReservationPurchaseRecommendationResponseTypeDef
    ]
else:
    _GetReservationPurchaseRecommendationPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetReservationPurchaseRecommendationPaginator(
    _GetReservationPurchaseRecommendationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetReservationPurchaseRecommendation.html#CostExplorer.Paginator.GetReservationPurchaseRecommendation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getreservationpurchaserecommendationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetReservationPurchaseRecommendationRequestPaginateTypeDef]
    ) -> AioPageIterator[GetReservationPurchaseRecommendationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetReservationPurchaseRecommendation.html#CostExplorer.Paginator.GetReservationPurchaseRecommendation.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getreservationpurchaserecommendationpaginator)
        """

if TYPE_CHECKING:
    _GetRightsizingRecommendationPaginatorBase = AioPaginator[
        GetRightsizingRecommendationResponseTypeDef
    ]
else:
    _GetRightsizingRecommendationPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetRightsizingRecommendationPaginator(_GetRightsizingRecommendationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetRightsizingRecommendation.html#CostExplorer.Paginator.GetRightsizingRecommendation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getrightsizingrecommendationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRightsizingRecommendationRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRightsizingRecommendationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/GetRightsizingRecommendation.html#CostExplorer.Paginator.GetRightsizingRecommendation.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#getrightsizingrecommendationpaginator)
        """

if TYPE_CHECKING:
    _ListCommitmentPurchaseAnalysesPaginatorBase = AioPaginator[
        ListCommitmentPurchaseAnalysesResponseTypeDef
    ]
else:
    _ListCommitmentPurchaseAnalysesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCommitmentPurchaseAnalysesPaginator(_ListCommitmentPurchaseAnalysesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCommitmentPurchaseAnalyses.html#CostExplorer.Paginator.ListCommitmentPurchaseAnalyses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcommitmentpurchaseanalysespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCommitmentPurchaseAnalysesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCommitmentPurchaseAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCommitmentPurchaseAnalyses.html#CostExplorer.Paginator.ListCommitmentPurchaseAnalyses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcommitmentpurchaseanalysespaginator)
        """

if TYPE_CHECKING:
    _ListCostAllocationTagBackfillHistoryPaginatorBase = AioPaginator[
        ListCostAllocationTagBackfillHistoryResponseTypeDef
    ]
else:
    _ListCostAllocationTagBackfillHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCostAllocationTagBackfillHistoryPaginator(
    _ListCostAllocationTagBackfillHistoryPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCostAllocationTagBackfillHistory.html#CostExplorer.Paginator.ListCostAllocationTagBackfillHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcostallocationtagbackfillhistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCostAllocationTagBackfillHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCostAllocationTagBackfillHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCostAllocationTagBackfillHistory.html#CostExplorer.Paginator.ListCostAllocationTagBackfillHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcostallocationtagbackfillhistorypaginator)
        """

if TYPE_CHECKING:
    _ListCostAllocationTagsPaginatorBase = AioPaginator[ListCostAllocationTagsResponseTypeDef]
else:
    _ListCostAllocationTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCostAllocationTagsPaginator(_ListCostAllocationTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCostAllocationTags.html#CostExplorer.Paginator.ListCostAllocationTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcostallocationtagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCostAllocationTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCostAllocationTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCostAllocationTags.html#CostExplorer.Paginator.ListCostAllocationTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcostallocationtagspaginator)
        """

if TYPE_CHECKING:
    _ListCostCategoryDefinitionsPaginatorBase = AioPaginator[
        ListCostCategoryDefinitionsResponseTypeDef
    ]
else:
    _ListCostCategoryDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCostCategoryDefinitionsPaginator(_ListCostCategoryDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCostCategoryDefinitions.html#CostExplorer.Paginator.ListCostCategoryDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcostcategorydefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCostCategoryDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCostCategoryDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCostCategoryDefinitions.html#CostExplorer.Paginator.ListCostCategoryDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcostcategorydefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListCostCategoryResourceAssociationsPaginatorBase = AioPaginator[
        ListCostCategoryResourceAssociationsResponseTypeDef
    ]
else:
    _ListCostCategoryResourceAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCostCategoryResourceAssociationsPaginator(
    _ListCostCategoryResourceAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCostCategoryResourceAssociations.html#CostExplorer.Paginator.ListCostCategoryResourceAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcostcategoryresourceassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCostCategoryResourceAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCostCategoryResourceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListCostCategoryResourceAssociations.html#CostExplorer.Paginator.ListCostCategoryResourceAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listcostcategoryresourceassociationspaginator)
        """

if TYPE_CHECKING:
    _ListSavingsPlansPurchaseRecommendationGenerationPaginatorBase = AioPaginator[
        ListSavingsPlansPurchaseRecommendationGenerationResponseTypeDef
    ]
else:
    _ListSavingsPlansPurchaseRecommendationGenerationPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSavingsPlansPurchaseRecommendationGenerationPaginator(
    _ListSavingsPlansPurchaseRecommendationGenerationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListSavingsPlansPurchaseRecommendationGeneration.html#CostExplorer.Paginator.ListSavingsPlansPurchaseRecommendationGeneration)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listsavingsplanspurchaserecommendationgenerationpaginator)
    """
    def paginate(  # type: ignore[override]
        self,
        **kwargs: Unpack[ListSavingsPlansPurchaseRecommendationGenerationRequestPaginateTypeDef],
    ) -> AioPageIterator[ListSavingsPlansPurchaseRecommendationGenerationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/paginator/ListSavingsPlansPurchaseRecommendationGeneration.html#CostExplorer.Paginator.ListSavingsPlansPurchaseRecommendationGeneration.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/paginators/#listsavingsplanspurchaserecommendationgenerationpaginator)
        """
