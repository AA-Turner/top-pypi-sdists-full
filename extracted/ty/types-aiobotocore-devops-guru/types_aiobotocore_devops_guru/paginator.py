"""
Type annotations for devops-guru service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_devops_guru.client import DevOpsGuruClient
    from types_aiobotocore_devops_guru.paginator import (
        DescribeOrganizationResourceCollectionHealthPaginator,
        DescribeResourceCollectionHealthPaginator,
        GetCostEstimationPaginator,
        GetResourceCollectionPaginator,
        ListAnomaliesForInsightPaginator,
        ListAnomalousLogGroupsPaginator,
        ListEventsPaginator,
        ListInsightsPaginator,
        ListMonitoredResourcesPaginator,
        ListNotificationChannelsPaginator,
        ListOrganizationInsightsPaginator,
        ListRecommendationsPaginator,
        SearchInsightsPaginator,
        SearchOrganizationInsightsPaginator,
    )

    session = get_session()
    with session.create_client("devops-guru") as client:
        client: DevOpsGuruClient

        describe_organization_resource_collection_health_paginator: DescribeOrganizationResourceCollectionHealthPaginator = client.get_paginator("describe_organization_resource_collection_health")
        describe_resource_collection_health_paginator: DescribeResourceCollectionHealthPaginator = client.get_paginator("describe_resource_collection_health")
        get_cost_estimation_paginator: GetCostEstimationPaginator = client.get_paginator("get_cost_estimation")
        get_resource_collection_paginator: GetResourceCollectionPaginator = client.get_paginator("get_resource_collection")
        list_anomalies_for_insight_paginator: ListAnomaliesForInsightPaginator = client.get_paginator("list_anomalies_for_insight")
        list_anomalous_log_groups_paginator: ListAnomalousLogGroupsPaginator = client.get_paginator("list_anomalous_log_groups")
        list_events_paginator: ListEventsPaginator = client.get_paginator("list_events")
        list_insights_paginator: ListInsightsPaginator = client.get_paginator("list_insights")
        list_monitored_resources_paginator: ListMonitoredResourcesPaginator = client.get_paginator("list_monitored_resources")
        list_notification_channels_paginator: ListNotificationChannelsPaginator = client.get_paginator("list_notification_channels")
        list_organization_insights_paginator: ListOrganizationInsightsPaginator = client.get_paginator("list_organization_insights")
        list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
        search_insights_paginator: SearchInsightsPaginator = client.get_paginator("search_insights")
        search_organization_insights_paginator: SearchOrganizationInsightsPaginator = client.get_paginator("search_organization_insights")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeOrganizationResourceCollectionHealthRequestPaginateTypeDef,
    DescribeOrganizationResourceCollectionHealthResponseTypeDef,
    DescribeResourceCollectionHealthRequestPaginateTypeDef,
    DescribeResourceCollectionHealthResponseTypeDef,
    GetCostEstimationRequestPaginateTypeDef,
    GetCostEstimationResponseTypeDef,
    GetResourceCollectionRequestPaginateTypeDef,
    GetResourceCollectionResponseTypeDef,
    ListAnomaliesForInsightRequestPaginateTypeDef,
    ListAnomaliesForInsightResponseTypeDef,
    ListAnomalousLogGroupsRequestPaginateTypeDef,
    ListAnomalousLogGroupsResponseTypeDef,
    ListEventsRequestPaginateTypeDef,
    ListEventsResponseTypeDef,
    ListInsightsRequestPaginateTypeDef,
    ListInsightsResponseTypeDef,
    ListMonitoredResourcesRequestPaginateTypeDef,
    ListMonitoredResourcesResponseTypeDef,
    ListNotificationChannelsRequestPaginateTypeDef,
    ListNotificationChannelsResponseTypeDef,
    ListOrganizationInsightsRequestPaginateTypeDef,
    ListOrganizationInsightsResponseTypeDef,
    ListRecommendationsRequestPaginateTypeDef,
    ListRecommendationsResponseTypeDef,
    SearchInsightsRequestPaginateTypeDef,
    SearchInsightsResponseTypeDef,
    SearchOrganizationInsightsRequestPaginateTypeDef,
    SearchOrganizationInsightsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeOrganizationResourceCollectionHealthPaginator",
    "DescribeResourceCollectionHealthPaginator",
    "GetCostEstimationPaginator",
    "GetResourceCollectionPaginator",
    "ListAnomaliesForInsightPaginator",
    "ListAnomalousLogGroupsPaginator",
    "ListEventsPaginator",
    "ListInsightsPaginator",
    "ListMonitoredResourcesPaginator",
    "ListNotificationChannelsPaginator",
    "ListOrganizationInsightsPaginator",
    "ListRecommendationsPaginator",
    "SearchInsightsPaginator",
    "SearchOrganizationInsightsPaginator",
)


if TYPE_CHECKING:
    _DescribeOrganizationResourceCollectionHealthPaginatorBase = AioPaginator[
        DescribeOrganizationResourceCollectionHealthResponseTypeDef
    ]
else:
    _DescribeOrganizationResourceCollectionHealthPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeOrganizationResourceCollectionHealthPaginator(
    _DescribeOrganizationResourceCollectionHealthPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeOrganizationResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeOrganizationResourceCollectionHealth)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#describeorganizationresourcecollectionhealthpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOrganizationResourceCollectionHealthRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeOrganizationResourceCollectionHealthResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeOrganizationResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeOrganizationResourceCollectionHealth.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#describeorganizationresourcecollectionhealthpaginator)
        """


if TYPE_CHECKING:
    _DescribeResourceCollectionHealthPaginatorBase = AioPaginator[
        DescribeResourceCollectionHealthResponseTypeDef
    ]
else:
    _DescribeResourceCollectionHealthPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeResourceCollectionHealthPaginator(_DescribeResourceCollectionHealthPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeResourceCollectionHealth)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#describeresourcecollectionhealthpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeResourceCollectionHealthRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeResourceCollectionHealthResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/DescribeResourceCollectionHealth.html#DevOpsGuru.Paginator.DescribeResourceCollectionHealth.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#describeresourcecollectionhealthpaginator)
        """


if TYPE_CHECKING:
    _GetCostEstimationPaginatorBase = AioPaginator[GetCostEstimationResponseTypeDef]
else:
    _GetCostEstimationPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetCostEstimationPaginator(_GetCostEstimationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetCostEstimation.html#DevOpsGuru.Paginator.GetCostEstimation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#getcostestimationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCostEstimationRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCostEstimationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetCostEstimation.html#DevOpsGuru.Paginator.GetCostEstimation.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#getcostestimationpaginator)
        """


if TYPE_CHECKING:
    _GetResourceCollectionPaginatorBase = AioPaginator[GetResourceCollectionResponseTypeDef]
else:
    _GetResourceCollectionPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetResourceCollectionPaginator(_GetResourceCollectionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetResourceCollection.html#DevOpsGuru.Paginator.GetResourceCollection)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#getresourcecollectionpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourceCollectionRequestPaginateTypeDef]
    ) -> AioPageIterator[GetResourceCollectionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/GetResourceCollection.html#DevOpsGuru.Paginator.GetResourceCollection.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#getresourcecollectionpaginator)
        """


if TYPE_CHECKING:
    _ListAnomaliesForInsightPaginatorBase = AioPaginator[ListAnomaliesForInsightResponseTypeDef]
else:
    _ListAnomaliesForInsightPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAnomaliesForInsightPaginator(_ListAnomaliesForInsightPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomaliesForInsight.html#DevOpsGuru.Paginator.ListAnomaliesForInsight)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listanomaliesforinsightpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAnomaliesForInsightRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAnomaliesForInsightResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomaliesForInsight.html#DevOpsGuru.Paginator.ListAnomaliesForInsight.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listanomaliesforinsightpaginator)
        """


if TYPE_CHECKING:
    _ListAnomalousLogGroupsPaginatorBase = AioPaginator[ListAnomalousLogGroupsResponseTypeDef]
else:
    _ListAnomalousLogGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAnomalousLogGroupsPaginator(_ListAnomalousLogGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomalousLogGroups.html#DevOpsGuru.Paginator.ListAnomalousLogGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listanomalousloggroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAnomalousLogGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAnomalousLogGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListAnomalousLogGroups.html#DevOpsGuru.Paginator.ListAnomalousLogGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listanomalousloggroupspaginator)
        """


if TYPE_CHECKING:
    _ListEventsPaginatorBase = AioPaginator[ListEventsResponseTypeDef]
else:
    _ListEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventsPaginator(_ListEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListEvents.html#DevOpsGuru.Paginator.ListEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListEvents.html#DevOpsGuru.Paginator.ListEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listeventspaginator)
        """


if TYPE_CHECKING:
    _ListInsightsPaginatorBase = AioPaginator[ListInsightsResponseTypeDef]
else:
    _ListInsightsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInsightsPaginator(_ListInsightsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListInsights.html#DevOpsGuru.Paginator.ListInsights)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listinsightspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInsightsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListInsights.html#DevOpsGuru.Paginator.ListInsights.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listinsightspaginator)
        """


if TYPE_CHECKING:
    _ListMonitoredResourcesPaginatorBase = AioPaginator[ListMonitoredResourcesResponseTypeDef]
else:
    _ListMonitoredResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMonitoredResourcesPaginator(_ListMonitoredResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListMonitoredResources.html#DevOpsGuru.Paginator.ListMonitoredResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listmonitoredresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitoredResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMonitoredResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListMonitoredResources.html#DevOpsGuru.Paginator.ListMonitoredResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listmonitoredresourcespaginator)
        """


if TYPE_CHECKING:
    _ListNotificationChannelsPaginatorBase = AioPaginator[ListNotificationChannelsResponseTypeDef]
else:
    _ListNotificationChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNotificationChannelsPaginator(_ListNotificationChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListNotificationChannels.html#DevOpsGuru.Paginator.ListNotificationChannels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listnotificationchannelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListNotificationChannels.html#DevOpsGuru.Paginator.ListNotificationChannels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listnotificationchannelspaginator)
        """


if TYPE_CHECKING:
    _ListOrganizationInsightsPaginatorBase = AioPaginator[ListOrganizationInsightsResponseTypeDef]
else:
    _ListOrganizationInsightsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOrganizationInsightsPaginator(_ListOrganizationInsightsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListOrganizationInsights.html#DevOpsGuru.Paginator.ListOrganizationInsights)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listorganizationinsightspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrganizationInsightsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOrganizationInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListOrganizationInsights.html#DevOpsGuru.Paginator.ListOrganizationInsights.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listorganizationinsightspaginator)
        """


if TYPE_CHECKING:
    _ListRecommendationsPaginatorBase = AioPaginator[ListRecommendationsResponseTypeDef]
else:
    _ListRecommendationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecommendationsPaginator(_ListRecommendationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListRecommendations.html#DevOpsGuru.Paginator.ListRecommendations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listrecommendationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecommendationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/ListRecommendations.html#DevOpsGuru.Paginator.ListRecommendations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#listrecommendationspaginator)
        """


if TYPE_CHECKING:
    _SearchInsightsPaginatorBase = AioPaginator[SearchInsightsResponseTypeDef]
else:
    _SearchInsightsPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchInsightsPaginator(_SearchInsightsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchInsights.html#DevOpsGuru.Paginator.SearchInsights)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#searchinsightspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchInsightsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchInsights.html#DevOpsGuru.Paginator.SearchInsights.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#searchinsightspaginator)
        """


if TYPE_CHECKING:
    _SearchOrganizationInsightsPaginatorBase = AioPaginator[
        SearchOrganizationInsightsResponseTypeDef
    ]
else:
    _SearchOrganizationInsightsPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchOrganizationInsightsPaginator(_SearchOrganizationInsightsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchOrganizationInsights.html#DevOpsGuru.Paginator.SearchOrganizationInsights)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#searchorganizationinsightspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchOrganizationInsightsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchOrganizationInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru/paginator/SearchOrganizationInsights.html#DevOpsGuru.Paginator.SearchOrganizationInsights.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/paginators/#searchorganizationinsightspaginator)
        """
