"""
Main interface for bcm-dashboards service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bcm_dashboards/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bcm_dashboards import (
        BillingandCostManagementDashboardsClient,
        Client,
        ListDashboardsPaginator,
        ListScheduledReportsPaginator,
    )

    session = Session()
    client: BillingandCostManagementDashboardsClient = session.client("bcm-dashboards")

    list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
    list_scheduled_reports_paginator: ListScheduledReportsPaginator = client.get_paginator("list_scheduled_reports")
    ```
"""

from .client import BillingandCostManagementDashboardsClient
from .paginator import ListDashboardsPaginator, ListScheduledReportsPaginator

Client = BillingandCostManagementDashboardsClient

__all__ = (
    "BillingandCostManagementDashboardsClient",
    "Client",
    "ListDashboardsPaginator",
    "ListScheduledReportsPaginator",
)
