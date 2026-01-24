"""
Main interface for bcm-dashboards service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_dashboards/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bcm_dashboards import (
        BillingandCostManagementDashboardsClient,
        Client,
        ListDashboardsPaginator,
    )

    session = get_session()
    async with session.create_client("bcm-dashboards") as client:
        client: BillingandCostManagementDashboardsClient
        ...


    list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
    ```
"""

from .client import BillingandCostManagementDashboardsClient
from .paginator import ListDashboardsPaginator

Client = BillingandCostManagementDashboardsClient

__all__ = ("BillingandCostManagementDashboardsClient", "Client", "ListDashboardsPaginator")
