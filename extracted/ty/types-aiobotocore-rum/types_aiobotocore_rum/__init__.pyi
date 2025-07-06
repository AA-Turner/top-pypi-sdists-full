"""
Main interface for rum service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rum import (
        BatchGetRumMetricDefinitionsPaginator,
        Client,
        CloudWatchRUMClient,
        GetAppMonitorDataPaginator,
        ListAppMonitorsPaginator,
        ListRumMetricsDestinationsPaginator,
    )

    session = get_session()
    async with session.create_client("rum") as client:
        client: CloudWatchRUMClient
        ...


    batch_get_rum_metric_definitions_paginator: BatchGetRumMetricDefinitionsPaginator = client.get_paginator("batch_get_rum_metric_definitions")
    get_app_monitor_data_paginator: GetAppMonitorDataPaginator = client.get_paginator("get_app_monitor_data")
    list_app_monitors_paginator: ListAppMonitorsPaginator = client.get_paginator("list_app_monitors")
    list_rum_metrics_destinations_paginator: ListRumMetricsDestinationsPaginator = client.get_paginator("list_rum_metrics_destinations")
    ```
"""

from .client import CloudWatchRUMClient
from .paginator import (
    BatchGetRumMetricDefinitionsPaginator,
    GetAppMonitorDataPaginator,
    ListAppMonitorsPaginator,
    ListRumMetricsDestinationsPaginator,
)

Client = CloudWatchRUMClient

__all__ = (
    "BatchGetRumMetricDefinitionsPaginator",
    "Client",
    "CloudWatchRUMClient",
    "GetAppMonitorDataPaginator",
    "ListAppMonitorsPaginator",
    "ListRumMetricsDestinationsPaginator",
)
