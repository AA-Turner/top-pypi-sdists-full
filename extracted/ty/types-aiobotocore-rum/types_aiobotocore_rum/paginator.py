"""
Type annotations for rum service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rum.client import CloudWatchRUMClient
    from types_aiobotocore_rum.paginator import (
        BatchGetRumMetricDefinitionsPaginator,
        GetAppMonitorDataPaginator,
        ListAppMonitorsPaginator,
        ListRumMetricsDestinationsPaginator,
    )

    session = get_session()
    with session.create_client("rum") as client:
        client: CloudWatchRUMClient

        batch_get_rum_metric_definitions_paginator: BatchGetRumMetricDefinitionsPaginator = client.get_paginator("batch_get_rum_metric_definitions")
        get_app_monitor_data_paginator: GetAppMonitorDataPaginator = client.get_paginator("get_app_monitor_data")
        list_app_monitors_paginator: ListAppMonitorsPaginator = client.get_paginator("list_app_monitors")
        list_rum_metrics_destinations_paginator: ListRumMetricsDestinationsPaginator = client.get_paginator("list_rum_metrics_destinations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    BatchGetRumMetricDefinitionsRequestPaginateTypeDef,
    BatchGetRumMetricDefinitionsResponseTypeDef,
    GetAppMonitorDataRequestPaginateTypeDef,
    GetAppMonitorDataResponseTypeDef,
    ListAppMonitorsRequestPaginateTypeDef,
    ListAppMonitorsResponseTypeDef,
    ListRumMetricsDestinationsRequestPaginateTypeDef,
    ListRumMetricsDestinationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "BatchGetRumMetricDefinitionsPaginator",
    "GetAppMonitorDataPaginator",
    "ListAppMonitorsPaginator",
    "ListRumMetricsDestinationsPaginator",
)


if TYPE_CHECKING:
    _BatchGetRumMetricDefinitionsPaginatorBase = AioPaginator[
        BatchGetRumMetricDefinitionsResponseTypeDef
    ]
else:
    _BatchGetRumMetricDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class BatchGetRumMetricDefinitionsPaginator(_BatchGetRumMetricDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/BatchGetRumMetricDefinitions.html#CloudWatchRUM.Paginator.BatchGetRumMetricDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#batchgetrummetricdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[BatchGetRumMetricDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[BatchGetRumMetricDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/BatchGetRumMetricDefinitions.html#CloudWatchRUM.Paginator.BatchGetRumMetricDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#batchgetrummetricdefinitionspaginator)
        """


if TYPE_CHECKING:
    _GetAppMonitorDataPaginatorBase = AioPaginator[GetAppMonitorDataResponseTypeDef]
else:
    _GetAppMonitorDataPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetAppMonitorDataPaginator(_GetAppMonitorDataPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/GetAppMonitorData.html#CloudWatchRUM.Paginator.GetAppMonitorData)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#getappmonitordatapaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAppMonitorDataRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAppMonitorDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/GetAppMonitorData.html#CloudWatchRUM.Paginator.GetAppMonitorData.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#getappmonitordatapaginator)
        """


if TYPE_CHECKING:
    _ListAppMonitorsPaginatorBase = AioPaginator[ListAppMonitorsResponseTypeDef]
else:
    _ListAppMonitorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAppMonitorsPaginator(_ListAppMonitorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListAppMonitors.html#CloudWatchRUM.Paginator.ListAppMonitors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#listappmonitorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppMonitorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAppMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListAppMonitors.html#CloudWatchRUM.Paginator.ListAppMonitors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#listappmonitorspaginator)
        """


if TYPE_CHECKING:
    _ListRumMetricsDestinationsPaginatorBase = AioPaginator[
        ListRumMetricsDestinationsResponseTypeDef
    ]
else:
    _ListRumMetricsDestinationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRumMetricsDestinationsPaginator(_ListRumMetricsDestinationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListRumMetricsDestinations.html#CloudWatchRUM.Paginator.ListRumMetricsDestinations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#listrummetricsdestinationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRumMetricsDestinationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRumMetricsDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/paginator/ListRumMetricsDestinations.html#CloudWatchRUM.Paginator.ListRumMetricsDestinations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/paginators/#listrummetricsdestinationspaginator)
        """
