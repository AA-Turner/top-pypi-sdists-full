"""
Type annotations for billing service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_billing.client import BillingClient
    from types_aiobotocore_billing.paginator import (
        GetCreditAllocationHistoryPaginator,
        ListBillingViewsPaginator,
        ListSourceViewsForBillingViewPaginator,
    )

    session = get_session()
    with session.create_client("billing") as client:
        client: BillingClient

        get_credit_allocation_history_paginator: GetCreditAllocationHistoryPaginator = client.get_paginator("get_credit_allocation_history")
        list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
        list_source_views_for_billing_view_paginator: ListSourceViewsForBillingViewPaginator = client.get_paginator("list_source_views_for_billing_view")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetCreditAllocationHistoryRequestPaginateTypeDef,
    GetCreditAllocationHistoryResponseTypeDef,
    ListBillingViewsRequestPaginateTypeDef,
    ListBillingViewsResponseTypeDef,
    ListSourceViewsForBillingViewRequestPaginateTypeDef,
    ListSourceViewsForBillingViewResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetCreditAllocationHistoryPaginator",
    "ListBillingViewsPaginator",
    "ListSourceViewsForBillingViewPaginator",
)

if TYPE_CHECKING:
    _GetCreditAllocationHistoryPaginatorBase = AioPaginator[
        GetCreditAllocationHistoryResponseTypeDef
    ]
else:
    _GetCreditAllocationHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetCreditAllocationHistoryPaginator(_GetCreditAllocationHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/GetCreditAllocationHistory.html#Billing.Paginator.GetCreditAllocationHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#getcreditallocationhistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCreditAllocationHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCreditAllocationHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/GetCreditAllocationHistory.html#Billing.Paginator.GetCreditAllocationHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#getcreditallocationhistorypaginator)
        """

if TYPE_CHECKING:
    _ListBillingViewsPaginatorBase = AioPaginator[ListBillingViewsResponseTypeDef]
else:
    _ListBillingViewsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBillingViewsPaginator(_ListBillingViewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbillingviewspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingViewsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBillingViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbillingviewspaginator)
        """

if TYPE_CHECKING:
    _ListSourceViewsForBillingViewPaginatorBase = AioPaginator[
        ListSourceViewsForBillingViewResponseTypeDef
    ]
else:
    _ListSourceViewsForBillingViewPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSourceViewsForBillingViewPaginator(_ListSourceViewsForBillingViewPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListSourceViewsForBillingView.html#Billing.Paginator.ListSourceViewsForBillingView)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listsourceviewsforbillingviewpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceViewsForBillingViewRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSourceViewsForBillingViewResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListSourceViewsForBillingView.html#Billing.Paginator.ListSourceViewsForBillingView.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listsourceviewsforbillingviewpaginator)
        """
