"""
Type annotations for xray service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_xray.client import XRayClient
    from types_aiobotocore_xray.paginator import (
        BatchGetTracesPaginator,
        GetGroupsPaginator,
        GetSamplingRulesPaginator,
        GetSamplingStatisticSummariesPaginator,
        GetServiceGraphPaginator,
        GetTimeSeriesServiceStatisticsPaginator,
        GetTraceGraphPaginator,
        GetTraceSummariesPaginator,
        ListResourcePoliciesPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("xray") as client:
        client: XRayClient

        batch_get_traces_paginator: BatchGetTracesPaginator = client.get_paginator("batch_get_traces")
        get_groups_paginator: GetGroupsPaginator = client.get_paginator("get_groups")
        get_sampling_rules_paginator: GetSamplingRulesPaginator = client.get_paginator("get_sampling_rules")
        get_sampling_statistic_summaries_paginator: GetSamplingStatisticSummariesPaginator = client.get_paginator("get_sampling_statistic_summaries")
        get_service_graph_paginator: GetServiceGraphPaginator = client.get_paginator("get_service_graph")
        get_time_series_service_statistics_paginator: GetTimeSeriesServiceStatisticsPaginator = client.get_paginator("get_time_series_service_statistics")
        get_trace_graph_paginator: GetTraceGraphPaginator = client.get_paginator("get_trace_graph")
        get_trace_summaries_paginator: GetTraceSummariesPaginator = client.get_paginator("get_trace_summaries")
        list_resource_policies_paginator: ListResourcePoliciesPaginator = client.get_paginator("list_resource_policies")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    BatchGetTracesRequestPaginateTypeDef,
    BatchGetTracesResultTypeDef,
    GetGroupsRequestPaginateTypeDef,
    GetGroupsResultTypeDef,
    GetSamplingRulesRequestPaginateTypeDef,
    GetSamplingRulesResultTypeDef,
    GetSamplingStatisticSummariesRequestPaginateTypeDef,
    GetSamplingStatisticSummariesResultTypeDef,
    GetServiceGraphRequestPaginateTypeDef,
    GetServiceGraphResultTypeDef,
    GetTimeSeriesServiceStatisticsRequestPaginateTypeDef,
    GetTimeSeriesServiceStatisticsResultTypeDef,
    GetTraceGraphRequestPaginateTypeDef,
    GetTraceGraphResultTypeDef,
    GetTraceSummariesRequestPaginateTypeDef,
    GetTraceSummariesResultTypeDef,
    ListResourcePoliciesRequestPaginateTypeDef,
    ListResourcePoliciesResultTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "BatchGetTracesPaginator",
    "GetGroupsPaginator",
    "GetSamplingRulesPaginator",
    "GetSamplingStatisticSummariesPaginator",
    "GetServiceGraphPaginator",
    "GetTimeSeriesServiceStatisticsPaginator",
    "GetTraceGraphPaginator",
    "GetTraceSummariesPaginator",
    "ListResourcePoliciesPaginator",
    "ListTagsForResourcePaginator",
)


if TYPE_CHECKING:
    _BatchGetTracesPaginatorBase = AioPaginator[BatchGetTracesResultTypeDef]
else:
    _BatchGetTracesPaginatorBase = AioPaginator  # type: ignore[assignment]


class BatchGetTracesPaginator(_BatchGetTracesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/BatchGetTraces.html#XRay.Paginator.BatchGetTraces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#batchgettracespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[BatchGetTracesRequestPaginateTypeDef]
    ) -> AioPageIterator[BatchGetTracesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/BatchGetTraces.html#XRay.Paginator.BatchGetTraces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#batchgettracespaginator)
        """


if TYPE_CHECKING:
    _GetGroupsPaginatorBase = AioPaginator[GetGroupsResultTypeDef]
else:
    _GetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetGroupsPaginator(_GetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetGroups.html#XRay.Paginator.GetGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#getgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetGroups.html#XRay.Paginator.GetGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#getgroupspaginator)
        """


if TYPE_CHECKING:
    _GetSamplingRulesPaginatorBase = AioPaginator[GetSamplingRulesResultTypeDef]
else:
    _GetSamplingRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetSamplingRulesPaginator(_GetSamplingRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetSamplingRules.html#XRay.Paginator.GetSamplingRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#getsamplingrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetSamplingRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetSamplingRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetSamplingRules.html#XRay.Paginator.GetSamplingRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#getsamplingrulespaginator)
        """


if TYPE_CHECKING:
    _GetSamplingStatisticSummariesPaginatorBase = AioPaginator[
        GetSamplingStatisticSummariesResultTypeDef
    ]
else:
    _GetSamplingStatisticSummariesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetSamplingStatisticSummariesPaginator(_GetSamplingStatisticSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetSamplingStatisticSummaries.html#XRay.Paginator.GetSamplingStatisticSummaries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#getsamplingstatisticsummariespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetSamplingStatisticSummariesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetSamplingStatisticSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetSamplingStatisticSummaries.html#XRay.Paginator.GetSamplingStatisticSummaries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#getsamplingstatisticsummariespaginator)
        """


if TYPE_CHECKING:
    _GetServiceGraphPaginatorBase = AioPaginator[GetServiceGraphResultTypeDef]
else:
    _GetServiceGraphPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetServiceGraphPaginator(_GetServiceGraphPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetServiceGraph.html#XRay.Paginator.GetServiceGraph)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#getservicegraphpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceGraphRequestPaginateTypeDef]
    ) -> AioPageIterator[GetServiceGraphResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetServiceGraph.html#XRay.Paginator.GetServiceGraph.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#getservicegraphpaginator)
        """


if TYPE_CHECKING:
    _GetTimeSeriesServiceStatisticsPaginatorBase = AioPaginator[
        GetTimeSeriesServiceStatisticsResultTypeDef
    ]
else:
    _GetTimeSeriesServiceStatisticsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetTimeSeriesServiceStatisticsPaginator(_GetTimeSeriesServiceStatisticsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTimeSeriesServiceStatistics.html#XRay.Paginator.GetTimeSeriesServiceStatistics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#gettimeseriesservicestatisticspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetTimeSeriesServiceStatisticsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetTimeSeriesServiceStatisticsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTimeSeriesServiceStatistics.html#XRay.Paginator.GetTimeSeriesServiceStatistics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#gettimeseriesservicestatisticspaginator)
        """


if TYPE_CHECKING:
    _GetTraceGraphPaginatorBase = AioPaginator[GetTraceGraphResultTypeDef]
else:
    _GetTraceGraphPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetTraceGraphPaginator(_GetTraceGraphPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTraceGraph.html#XRay.Paginator.GetTraceGraph)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#gettracegraphpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetTraceGraphRequestPaginateTypeDef]
    ) -> AioPageIterator[GetTraceGraphResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTraceGraph.html#XRay.Paginator.GetTraceGraph.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#gettracegraphpaginator)
        """


if TYPE_CHECKING:
    _GetTraceSummariesPaginatorBase = AioPaginator[GetTraceSummariesResultTypeDef]
else:
    _GetTraceSummariesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetTraceSummariesPaginator(_GetTraceSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTraceSummaries.html#XRay.Paginator.GetTraceSummaries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#gettracesummariespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetTraceSummariesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetTraceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/GetTraceSummaries.html#XRay.Paginator.GetTraceSummaries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#gettracesummariespaginator)
        """


if TYPE_CHECKING:
    _ListResourcePoliciesPaginatorBase = AioPaginator[ListResourcePoliciesResultTypeDef]
else:
    _ListResourcePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourcePoliciesPaginator(_ListResourcePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/ListResourcePolicies.html#XRay.Paginator.ListResourcePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#listresourcepoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourcePoliciesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/ListResourcePolicies.html#XRay.Paginator.ListResourcePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#listresourcepoliciespaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/ListTagsForResource.html#XRay.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray/paginator/ListTagsForResource.html#XRay.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/paginators/#listtagsforresourcepaginator)
        """
