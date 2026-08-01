"""
Type annotations for billing service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_billing.client import BillingClient
    from mypy_boto3_billing.paginator import (
        GetCreditAllocationHistoryPaginator,
        ListBillingViewsPaginator,
        ListEnterpriseSupportLinkedAccountChargesPaginator,
        ListSourceViewsForBillingViewPaginator,
    )

    session = Session()
    client: BillingClient = session.client("billing")

    get_credit_allocation_history_paginator: GetCreditAllocationHistoryPaginator = client.get_paginator("get_credit_allocation_history")
    list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
    list_enterprise_support_linked_account_charges_paginator: ListEnterpriseSupportLinkedAccountChargesPaginator = client.get_paginator("list_enterprise_support_linked_account_charges")
    list_source_views_for_billing_view_paginator: ListSourceViewsForBillingViewPaginator = client.get_paginator("list_source_views_for_billing_view")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetCreditAllocationHistoryRequestPaginateTypeDef,
    GetCreditAllocationHistoryResponseTypeDef,
    ListBillingViewsRequestPaginateTypeDef,
    ListBillingViewsResponseTypeDef,
    ListEnterpriseSupportLinkedAccountChargesRequestPaginateTypeDef,
    ListEnterpriseSupportLinkedAccountChargesResponseTypeDef,
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
    "ListEnterpriseSupportLinkedAccountChargesPaginator",
    "ListSourceViewsForBillingViewPaginator",
)

if TYPE_CHECKING:
    _GetCreditAllocationHistoryPaginatorBase = Paginator[GetCreditAllocationHistoryResponseTypeDef]
else:
    _GetCreditAllocationHistoryPaginatorBase = Paginator  # type: ignore[assignment]

class GetCreditAllocationHistoryPaginator(_GetCreditAllocationHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/GetCreditAllocationHistory.html#Billing.Paginator.GetCreditAllocationHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#getcreditallocationhistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCreditAllocationHistoryRequestPaginateTypeDef]
    ) -> PageIterator[GetCreditAllocationHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/GetCreditAllocationHistory.html#Billing.Paginator.GetCreditAllocationHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#getcreditallocationhistorypaginator)
        """

if TYPE_CHECKING:
    _ListBillingViewsPaginatorBase = Paginator[ListBillingViewsResponseTypeDef]
else:
    _ListBillingViewsPaginatorBase = Paginator  # type: ignore[assignment]

class ListBillingViewsPaginator(_ListBillingViewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbillingviewspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingViewsRequestPaginateTypeDef]
    ) -> PageIterator[ListBillingViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbillingviewspaginator)
        """

if TYPE_CHECKING:
    _ListEnterpriseSupportLinkedAccountChargesPaginatorBase = Paginator[
        ListEnterpriseSupportLinkedAccountChargesResponseTypeDef
    ]
else:
    _ListEnterpriseSupportLinkedAccountChargesPaginatorBase = Paginator  # type: ignore[assignment]

class ListEnterpriseSupportLinkedAccountChargesPaginator(
    _ListEnterpriseSupportLinkedAccountChargesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListEnterpriseSupportLinkedAccountCharges.html#Billing.Paginator.ListEnterpriseSupportLinkedAccountCharges)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listenterprisesupportlinkedaccountchargespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnterpriseSupportLinkedAccountChargesRequestPaginateTypeDef]
    ) -> PageIterator[ListEnterpriseSupportLinkedAccountChargesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListEnterpriseSupportLinkedAccountCharges.html#Billing.Paginator.ListEnterpriseSupportLinkedAccountCharges.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listenterprisesupportlinkedaccountchargespaginator)
        """

if TYPE_CHECKING:
    _ListSourceViewsForBillingViewPaginatorBase = Paginator[
        ListSourceViewsForBillingViewResponseTypeDef
    ]
else:
    _ListSourceViewsForBillingViewPaginatorBase = Paginator  # type: ignore[assignment]

class ListSourceViewsForBillingViewPaginator(_ListSourceViewsForBillingViewPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListSourceViewsForBillingView.html#Billing.Paginator.ListSourceViewsForBillingView)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listsourceviewsforbillingviewpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceViewsForBillingViewRequestPaginateTypeDef]
    ) -> PageIterator[ListSourceViewsForBillingViewResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListSourceViewsForBillingView.html#Billing.Paginator.ListSourceViewsForBillingView.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listsourceviewsforbillingviewpaginator)
        """
