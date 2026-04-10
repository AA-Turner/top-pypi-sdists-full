"""
Type annotations for bcm-dashboards service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bcm_dashboards/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_bcm_dashboards.client import BillingandCostManagementDashboardsClient
    from types_boto3_bcm_dashboards.paginator import (
        ListDashboardsPaginator,
        ListScheduledReportsPaginator,
    )

    session = Session()
    client: BillingandCostManagementDashboardsClient = session.client("bcm-dashboards")

    list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
    list_scheduled_reports_paginator: ListScheduledReportsPaginator = client.get_paginator("list_scheduled_reports")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDashboardsRequestPaginateTypeDef,
    ListDashboardsResponseTypeDef,
    ListScheduledReportsRequestPaginateTypeDef,
    ListScheduledReportsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDashboardsPaginator", "ListScheduledReportsPaginator")

if TYPE_CHECKING:
    _ListDashboardsPaginatorBase = Paginator[ListDashboardsResponseTypeDef]
else:
    _ListDashboardsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDashboardsPaginator(_ListDashboardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-dashboards/paginator/ListDashboards.html#BillingandCostManagementDashboards.Paginator.ListDashboards)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bcm_dashboards/paginators/#listdashboardspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDashboardsRequestPaginateTypeDef]
    ) -> PageIterator[ListDashboardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-dashboards/paginator/ListDashboards.html#BillingandCostManagementDashboards.Paginator.ListDashboards.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bcm_dashboards/paginators/#listdashboardspaginator)
        """

if TYPE_CHECKING:
    _ListScheduledReportsPaginatorBase = Paginator[ListScheduledReportsResponseTypeDef]
else:
    _ListScheduledReportsPaginatorBase = Paginator  # type: ignore[assignment]

class ListScheduledReportsPaginator(_ListScheduledReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-dashboards/paginator/ListScheduledReports.html#BillingandCostManagementDashboards.Paginator.ListScheduledReports)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bcm_dashboards/paginators/#listscheduledreportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScheduledReportsRequestPaginateTypeDef]
    ) -> PageIterator[ListScheduledReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-dashboards/paginator/ListScheduledReports.html#BillingandCostManagementDashboards.Paginator.ListScheduledReports.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bcm_dashboards/paginators/#listscheduledreportspaginator)
        """
