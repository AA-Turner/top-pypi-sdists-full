"""
Type annotations for bcm-dashboards service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_dashboards/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bcm_dashboards.client import BillingandCostManagementDashboardsClient
    from types_aiobotocore_bcm_dashboards.paginator import (
        ListDashboardsPaginator,
        ListScheduledReportsPaginator,
    )

    session = get_session()
    with session.create_client("bcm-dashboards") as client:
        client: BillingandCostManagementDashboardsClient

        list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
        list_scheduled_reports_paginator: ListScheduledReportsPaginator = client.get_paginator("list_scheduled_reports")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _ListDashboardsPaginatorBase = AioPaginator[ListDashboardsResponseTypeDef]
else:
    _ListDashboardsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDashboardsPaginator(_ListDashboardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-dashboards/paginator/ListDashboards.html#BillingandCostManagementDashboards.Paginator.ListDashboards)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_dashboards/paginators/#listdashboardspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDashboardsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDashboardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-dashboards/paginator/ListDashboards.html#BillingandCostManagementDashboards.Paginator.ListDashboards.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_dashboards/paginators/#listdashboardspaginator)
        """


if TYPE_CHECKING:
    _ListScheduledReportsPaginatorBase = AioPaginator[ListScheduledReportsResponseTypeDef]
else:
    _ListScheduledReportsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListScheduledReportsPaginator(_ListScheduledReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-dashboards/paginator/ListScheduledReports.html#BillingandCostManagementDashboards.Paginator.ListScheduledReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_dashboards/paginators/#listscheduledreportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScheduledReportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListScheduledReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-dashboards/paginator/ListScheduledReports.html#BillingandCostManagementDashboards.Paginator.ListScheduledReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_dashboards/paginators/#listscheduledreportspaginator)
        """
