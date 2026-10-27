"""
Main interface for billing service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_billing import (
        BillingClient,
        Client,
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

from .client import BillingClient
from .paginator import (
    GetCreditAllocationHistoryPaginator,
    ListBillingViewSegmentsPaginator,
    ListBillingViewsPaginator,
    ListBusinessSupportAccountChargesPaginator,
    ListBusinessSupportSubscriptionHistoryPaginator,
    ListContractsPaginator,
    ListContractualInvestmentAttestationsPaginator,
    ListContractualInvestmentsPaginator,
    ListContractualInvestmentSummariesPaginator,
    ListEnterpriseSupportLinkedAccountChargesPaginator,
    ListSourceViewsForBillingViewPaginator,
)

Client = BillingClient

__all__ = (
    "BillingClient",
    "Client",
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
