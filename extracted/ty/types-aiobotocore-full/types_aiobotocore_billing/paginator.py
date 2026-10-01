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
        ListBillingViewSegmentsPaginator,
        ListBillingViewsPaginator,
        ListBusinessSupportAccountChargesPaginator,
        ListBusinessSupportSubscriptionHistoryPaginator,
        ListEnterpriseSupportLinkedAccountChargesPaginator,
        ListSourceViewsForBillingViewPaginator,
    )

    session = get_session()
    with session.create_client("billing") as client:
        client: BillingClient

        get_credit_allocation_history_paginator: GetCreditAllocationHistoryPaginator = client.get_paginator("get_credit_allocation_history")
        list_billing_view_segments_paginator: ListBillingViewSegmentsPaginator = client.get_paginator("list_billing_view_segments")
        list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
        list_business_support_account_charges_paginator: ListBusinessSupportAccountChargesPaginator = client.get_paginator("list_business_support_account_charges")
        list_business_support_subscription_history_paginator: ListBusinessSupportSubscriptionHistoryPaginator = client.get_paginator("list_business_support_subscription_history")
        list_enterprise_support_linked_account_charges_paginator: ListEnterpriseSupportLinkedAccountChargesPaginator = client.get_paginator("list_enterprise_support_linked_account_charges")
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
    ListBillingViewSegmentsRequestPaginateTypeDef,
    ListBillingViewSegmentsResponseTypeDef,
    ListBillingViewsRequestPaginateTypeDef,
    ListBillingViewsResponseTypeDef,
    ListBusinessSupportAccountChargesRequestPaginateTypeDef,
    ListBusinessSupportAccountChargesResponseTypeDef,
    ListBusinessSupportSubscriptionHistoryRequestPaginateTypeDef,
    ListBusinessSupportSubscriptionHistoryResponseTypeDef,
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
    "ListBillingViewSegmentsPaginator",
    "ListBillingViewsPaginator",
    "ListBusinessSupportAccountChargesPaginator",
    "ListBusinessSupportSubscriptionHistoryPaginator",
    "ListEnterpriseSupportLinkedAccountChargesPaginator",
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
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#getcreditallocationhistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCreditAllocationHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCreditAllocationHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/GetCreditAllocationHistory.html#Billing.Paginator.GetCreditAllocationHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#getcreditallocationhistorypaginator)
        """


if TYPE_CHECKING:
    _ListBillingViewSegmentsPaginatorBase = AioPaginator[ListBillingViewSegmentsResponseTypeDef]
else:
    _ListBillingViewSegmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBillingViewSegmentsPaginator(_ListBillingViewSegmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViewSegments.html#Billing.Paginator.ListBillingViewSegments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbillingviewsegmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingViewSegmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBillingViewSegmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViewSegments.html#Billing.Paginator.ListBillingViewSegments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbillingviewsegmentspaginator)
        """


if TYPE_CHECKING:
    _ListBillingViewsPaginatorBase = AioPaginator[ListBillingViewsResponseTypeDef]
else:
    _ListBillingViewsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBillingViewsPaginator(_ListBillingViewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbillingviewspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingViewsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBillingViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbillingviewspaginator)
        """


if TYPE_CHECKING:
    _ListBusinessSupportAccountChargesPaginatorBase = AioPaginator[
        ListBusinessSupportAccountChargesResponseTypeDef
    ]
else:
    _ListBusinessSupportAccountChargesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBusinessSupportAccountChargesPaginator(_ListBusinessSupportAccountChargesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBusinessSupportAccountCharges.html#Billing.Paginator.ListBusinessSupportAccountCharges)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbusinesssupportaccountchargespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBusinessSupportAccountChargesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBusinessSupportAccountChargesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBusinessSupportAccountCharges.html#Billing.Paginator.ListBusinessSupportAccountCharges.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbusinesssupportaccountchargespaginator)
        """


if TYPE_CHECKING:
    _ListBusinessSupportSubscriptionHistoryPaginatorBase = AioPaginator[
        ListBusinessSupportSubscriptionHistoryResponseTypeDef
    ]
else:
    _ListBusinessSupportSubscriptionHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBusinessSupportSubscriptionHistoryPaginator(
    _ListBusinessSupportSubscriptionHistoryPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBusinessSupportSubscriptionHistory.html#Billing.Paginator.ListBusinessSupportSubscriptionHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbusinesssupportsubscriptionhistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBusinessSupportSubscriptionHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBusinessSupportSubscriptionHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBusinessSupportSubscriptionHistory.html#Billing.Paginator.ListBusinessSupportSubscriptionHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbusinesssupportsubscriptionhistorypaginator)
        """


if TYPE_CHECKING:
    _ListEnterpriseSupportLinkedAccountChargesPaginatorBase = AioPaginator[
        ListEnterpriseSupportLinkedAccountChargesResponseTypeDef
    ]
else:
    _ListEnterpriseSupportLinkedAccountChargesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnterpriseSupportLinkedAccountChargesPaginator(
    _ListEnterpriseSupportLinkedAccountChargesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListEnterpriseSupportLinkedAccountCharges.html#Billing.Paginator.ListEnterpriseSupportLinkedAccountCharges)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listenterprisesupportlinkedaccountchargespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnterpriseSupportLinkedAccountChargesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnterpriseSupportLinkedAccountChargesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListEnterpriseSupportLinkedAccountCharges.html#Billing.Paginator.ListEnterpriseSupportLinkedAccountCharges.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listenterprisesupportlinkedaccountchargespaginator)
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
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listsourceviewsforbillingviewpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceViewsForBillingViewRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSourceViewsForBillingViewResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListSourceViewsForBillingView.html#Billing.Paginator.ListSourceViewsForBillingView.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listsourceviewsforbillingviewpaginator)
        """
