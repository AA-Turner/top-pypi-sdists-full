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
        ListBillingViewSegmentsPaginator,
        ListBillingViewsPaginator,
        ListBusinessSupportAccountChargesPaginator,
        ListBusinessSupportSubscriptionHistoryPaginator,
        ListContractsPaginator,
        ListContractualInvestmentAttestationsPaginator,
        ListContractualInvestmentSummariesPaginator,
        ListContractualInvestmentsPaginator,
        ListEnterpriseSupportLinkedAccountChargesPaginator,
        ListSourceViewsForBillingViewPaginator,
    )

    session = Session()
    client: BillingClient = session.client("billing")

    get_credit_allocation_history_paginator: GetCreditAllocationHistoryPaginator = client.get_paginator("get_credit_allocation_history")
    list_billing_view_segments_paginator: ListBillingViewSegmentsPaginator = client.get_paginator("list_billing_view_segments")
    list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
    list_business_support_account_charges_paginator: ListBusinessSupportAccountChargesPaginator = client.get_paginator("list_business_support_account_charges")
    list_business_support_subscription_history_paginator: ListBusinessSupportSubscriptionHistoryPaginator = client.get_paginator("list_business_support_subscription_history")
    list_contracts_paginator: ListContractsPaginator = client.get_paginator("list_contracts")
    list_contractual_investment_attestations_paginator: ListContractualInvestmentAttestationsPaginator = client.get_paginator("list_contractual_investment_attestations")
    list_contractual_investment_summaries_paginator: ListContractualInvestmentSummariesPaginator = client.get_paginator("list_contractual_investment_summaries")
    list_contractual_investments_paginator: ListContractualInvestmentsPaginator = client.get_paginator("list_contractual_investments")
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
    ListBillingViewSegmentsRequestPaginateTypeDef,
    ListBillingViewSegmentsResponseTypeDef,
    ListBillingViewsRequestPaginateTypeDef,
    ListBillingViewsResponseTypeDef,
    ListBusinessSupportAccountChargesRequestPaginateTypeDef,
    ListBusinessSupportAccountChargesResponseTypeDef,
    ListBusinessSupportSubscriptionHistoryRequestPaginateTypeDef,
    ListBusinessSupportSubscriptionHistoryResponseTypeDef,
    ListContractsRequestPaginateTypeDef,
    ListContractsResponseTypeDef,
    ListContractualInvestmentAttestationsRequestPaginateTypeDef,
    ListContractualInvestmentAttestationsResponseTypeDef,
    ListContractualInvestmentsRequestPaginateTypeDef,
    ListContractualInvestmentsResponseTypeDef,
    ListContractualInvestmentSummariesRequestPaginateTypeDef,
    ListContractualInvestmentSummariesResponseTypeDef,
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
    "ListContractsPaginator",
    "ListContractualInvestmentAttestationsPaginator",
    "ListContractualInvestmentSummariesPaginator",
    "ListContractualInvestmentsPaginator",
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
    _ListBillingViewSegmentsPaginatorBase = Paginator[ListBillingViewSegmentsResponseTypeDef]
else:
    _ListBillingViewSegmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListBillingViewSegmentsPaginator(_ListBillingViewSegmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViewSegments.html#Billing.Paginator.ListBillingViewSegments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbillingviewsegmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingViewSegmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListBillingViewSegmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViewSegments.html#Billing.Paginator.ListBillingViewSegments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbillingviewsegmentspaginator)
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
    _ListBusinessSupportAccountChargesPaginatorBase = Paginator[
        ListBusinessSupportAccountChargesResponseTypeDef
    ]
else:
    _ListBusinessSupportAccountChargesPaginatorBase = Paginator  # type: ignore[assignment]

class ListBusinessSupportAccountChargesPaginator(_ListBusinessSupportAccountChargesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBusinessSupportAccountCharges.html#Billing.Paginator.ListBusinessSupportAccountCharges)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbusinesssupportaccountchargespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBusinessSupportAccountChargesRequestPaginateTypeDef]
    ) -> PageIterator[ListBusinessSupportAccountChargesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBusinessSupportAccountCharges.html#Billing.Paginator.ListBusinessSupportAccountCharges.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbusinesssupportaccountchargespaginator)
        """

if TYPE_CHECKING:
    _ListBusinessSupportSubscriptionHistoryPaginatorBase = Paginator[
        ListBusinessSupportSubscriptionHistoryResponseTypeDef
    ]
else:
    _ListBusinessSupportSubscriptionHistoryPaginatorBase = Paginator  # type: ignore[assignment]

class ListBusinessSupportSubscriptionHistoryPaginator(
    _ListBusinessSupportSubscriptionHistoryPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBusinessSupportSubscriptionHistory.html#Billing.Paginator.ListBusinessSupportSubscriptionHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbusinesssupportsubscriptionhistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBusinessSupportSubscriptionHistoryRequestPaginateTypeDef]
    ) -> PageIterator[ListBusinessSupportSubscriptionHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBusinessSupportSubscriptionHistory.html#Billing.Paginator.ListBusinessSupportSubscriptionHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listbusinesssupportsubscriptionhistorypaginator)
        """

if TYPE_CHECKING:
    _ListContractsPaginatorBase = Paginator[ListContractsResponseTypeDef]
else:
    _ListContractsPaginatorBase = Paginator  # type: ignore[assignment]

class ListContractsPaginator(_ListContractsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListContracts.html#Billing.Paginator.ListContracts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listcontractspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContractsRequestPaginateTypeDef]
    ) -> PageIterator[ListContractsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListContracts.html#Billing.Paginator.ListContracts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listcontractspaginator)
        """

if TYPE_CHECKING:
    _ListContractualInvestmentAttestationsPaginatorBase = Paginator[
        ListContractualInvestmentAttestationsResponseTypeDef
    ]
else:
    _ListContractualInvestmentAttestationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListContractualInvestmentAttestationsPaginator(
    _ListContractualInvestmentAttestationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListContractualInvestmentAttestations.html#Billing.Paginator.ListContractualInvestmentAttestations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listcontractualinvestmentattestationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContractualInvestmentAttestationsRequestPaginateTypeDef]
    ) -> PageIterator[ListContractualInvestmentAttestationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListContractualInvestmentAttestations.html#Billing.Paginator.ListContractualInvestmentAttestations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listcontractualinvestmentattestationspaginator)
        """

if TYPE_CHECKING:
    _ListContractualInvestmentSummariesPaginatorBase = Paginator[
        ListContractualInvestmentSummariesResponseTypeDef
    ]
else:
    _ListContractualInvestmentSummariesPaginatorBase = Paginator  # type: ignore[assignment]

class ListContractualInvestmentSummariesPaginator(_ListContractualInvestmentSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListContractualInvestmentSummaries.html#Billing.Paginator.ListContractualInvestmentSummaries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listcontractualinvestmentsummariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContractualInvestmentSummariesRequestPaginateTypeDef]
    ) -> PageIterator[ListContractualInvestmentSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListContractualInvestmentSummaries.html#Billing.Paginator.ListContractualInvestmentSummaries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listcontractualinvestmentsummariespaginator)
        """

if TYPE_CHECKING:
    _ListContractualInvestmentsPaginatorBase = Paginator[ListContractualInvestmentsResponseTypeDef]
else:
    _ListContractualInvestmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListContractualInvestmentsPaginator(_ListContractualInvestmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListContractualInvestments.html#Billing.Paginator.ListContractualInvestments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listcontractualinvestmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContractualInvestmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListContractualInvestmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListContractualInvestments.html#Billing.Paginator.ListContractualInvestments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/paginators/#listcontractualinvestmentspaginator)
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
