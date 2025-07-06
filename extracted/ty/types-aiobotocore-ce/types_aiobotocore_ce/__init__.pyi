"""
Main interface for ce service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ce import (
        Client,
        CostExplorerClient,
        GetAnomaliesPaginator,
        GetAnomalyMonitorsPaginator,
        GetAnomalySubscriptionsPaginator,
        GetCostAndUsageComparisonsPaginator,
        GetCostComparisonDriversPaginator,
    )

    session = get_session()
    async with session.create_client("ce") as client:
        client: CostExplorerClient
        ...


    get_anomalies_paginator: GetAnomaliesPaginator = client.get_paginator("get_anomalies")
    get_anomaly_monitors_paginator: GetAnomalyMonitorsPaginator = client.get_paginator("get_anomaly_monitors")
    get_anomaly_subscriptions_paginator: GetAnomalySubscriptionsPaginator = client.get_paginator("get_anomaly_subscriptions")
    get_cost_and_usage_comparisons_paginator: GetCostAndUsageComparisonsPaginator = client.get_paginator("get_cost_and_usage_comparisons")
    get_cost_comparison_drivers_paginator: GetCostComparisonDriversPaginator = client.get_paginator("get_cost_comparison_drivers")
    ```
"""

from .client import CostExplorerClient
from .paginator import (
    GetAnomaliesPaginator,
    GetAnomalyMonitorsPaginator,
    GetAnomalySubscriptionsPaginator,
    GetCostAndUsageComparisonsPaginator,
    GetCostComparisonDriversPaginator,
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
)
