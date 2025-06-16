"""
Main interface for xray service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_xray/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_xray import (
        BatchGetTracesPaginator,
        Client,
        GetGroupsPaginator,
        GetSamplingRulesPaginator,
        GetSamplingStatisticSummariesPaginator,
        GetServiceGraphPaginator,
        GetTimeSeriesServiceStatisticsPaginator,
        GetTraceGraphPaginator,
        GetTraceSummariesPaginator,
        ListResourcePoliciesPaginator,
        ListTagsForResourcePaginator,
        XRayClient,
    )

    session = get_session()
    async with session.create_client("xray") as client:
        client: XRayClient
        ...


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

from .client import XRayClient
from .paginator import (
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

Client = XRayClient


__all__ = (
    "BatchGetTracesPaginator",
    "Client",
    "GetGroupsPaginator",
    "GetSamplingRulesPaginator",
    "GetSamplingStatisticSummariesPaginator",
    "GetServiceGraphPaginator",
    "GetTimeSeriesServiceStatisticsPaginator",
    "GetTraceGraphPaginator",
    "GetTraceSummariesPaginator",
    "ListResourcePoliciesPaginator",
    "ListTagsForResourcePaginator",
    "XRayClient",
)
