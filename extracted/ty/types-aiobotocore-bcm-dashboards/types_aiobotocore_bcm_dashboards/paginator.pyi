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
    )

    session = get_session()
    with session.create_client("bcm-dashboards") as client:
        client: BillingandCostManagementDashboardsClient

        list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListDashboardsRequestPaginateTypeDef, ListDashboardsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDashboardsPaginator",)

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
