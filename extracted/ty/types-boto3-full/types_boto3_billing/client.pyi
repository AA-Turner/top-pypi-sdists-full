"""
Type annotations for billing service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_billing.client import BillingClient

    session = Session()
    client: BillingClient = session.client("billing")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    GetCreditAllocationHistoryPaginator,
    ListBillingViewsPaginator,
    ListEnterpriseSupportLinkedAccountChargesPaginator,
    ListSourceViewsForBillingViewPaginator,
)
from .type_defs import (
    AssociateSourceViewsRequestTypeDef,
    AssociateSourceViewsResponseTypeDef,
    CreateBillingViewRequestTypeDef,
    CreateBillingViewResponseTypeDef,
    DeleteBillingViewRequestTypeDef,
    DeleteBillingViewResponseTypeDef,
    DisassociateSourceViewsRequestTypeDef,
    DisassociateSourceViewsResponseTypeDef,
    GetBillingPreferencesRequestTypeDef,
    GetBillingPreferencesResponseTypeDef,
    GetBillingViewRequestTypeDef,
    GetBillingViewResponseTypeDef,
    GetCreditAllocationHistoryRequestTypeDef,
    GetCreditAllocationHistoryResponseTypeDef,
    GetCreditsRequestTypeDef,
    GetCreditsResponseTypeDef,
    GetEnterpriseSupportChargeSummaryRequestTypeDef,
    GetEnterpriseSupportChargeSummaryResponseTypeDef,
    GetEnterpriseSupportContractDetailsRequestTypeDef,
    GetEnterpriseSupportContractDetailsResponseTypeDef,
    GetResourcePolicyRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    ListBillingViewsRequestTypeDef,
    ListBillingViewsResponseTypeDef,
    ListEnterpriseSupportLinkedAccountChargesRequestTypeDef,
    ListEnterpriseSupportLinkedAccountChargesResponseTypeDef,
    ListSourceViewsForBillingViewRequestTypeDef,
    ListSourceViewsForBillingViewResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RedeemCreditsRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateBillingPreferencesRequestTypeDef,
    UpdateBillingViewRequestTypeDef,
    UpdateBillingViewResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("BillingClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    BillingViewHealthStatusException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class BillingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing.html#Billing.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BillingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing.html#Billing.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#generate_presigned_url)
        """

    def associate_source_views(
        self, **kwargs: Unpack[AssociateSourceViewsRequestTypeDef]
    ) -> AssociateSourceViewsResponseTypeDef:
        """
        Associates one or more source billing views with an existing billing view.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/associate_source_views.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#associate_source_views)
        """

    def create_billing_view(
        self, **kwargs: Unpack[CreateBillingViewRequestTypeDef]
    ) -> CreateBillingViewResponseTypeDef:
        """
        Creates a billing view with the specified billing view attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/create_billing_view.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#create_billing_view)
        """

    def delete_billing_view(
        self, **kwargs: Unpack[DeleteBillingViewRequestTypeDef]
    ) -> DeleteBillingViewResponseTypeDef:
        """
        Deletes the specified billing view.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/delete_billing_view.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#delete_billing_view)
        """

    def disassociate_source_views(
        self, **kwargs: Unpack[DisassociateSourceViewsRequestTypeDef]
    ) -> DisassociateSourceViewsResponseTypeDef:
        """
        Removes the association between one or more source billing views and an
        existing billing view.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/disassociate_source_views.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#disassociate_source_views)
        """

    def get_billing_preferences(
        self, **kwargs: Unpack[GetBillingPreferencesRequestTypeDef]
    ) -> GetBillingPreferencesResponseTypeDef:
        """
        Retrieves billing preferences for the specified feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_billing_preferences.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_billing_preferences)
        """

    def get_billing_view(
        self, **kwargs: Unpack[GetBillingViewRequestTypeDef]
    ) -> GetBillingViewResponseTypeDef:
        """
        Returns the metadata associated to the specified billing view ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_billing_view.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_billing_view)
        """

    def get_credit_allocation_history(
        self, **kwargs: Unpack[GetCreditAllocationHistoryRequestTypeDef]
    ) -> GetCreditAllocationHistoryResponseTypeDef:
        """
        Returns the per-billing-month allocation history for credits applied to an
        Amazon Web Services account's bills.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_credit_allocation_history.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_credit_allocation_history)
        """

    def get_credits(self, **kwargs: Unpack[GetCreditsRequestTypeDef]) -> GetCreditsResponseTypeDef:
        """
        Returns the list of Amazon Web Services account credits for the specified
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_credits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_credits)
        """

    def get_enterprise_support_charge_summary(
        self, **kwargs: Unpack[GetEnterpriseSupportChargeSummaryRequestTypeDef]
    ) -> GetEnterpriseSupportChargeSummaryResponseTypeDef:
        """
        Returns a summary of Enterprise Support data aggregated across all accounts in
        the Enterprise Support profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_enterprise_support_charge_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_enterprise_support_charge_summary)
        """

    def get_enterprise_support_contract_details(
        self, **kwargs: Unpack[GetEnterpriseSupportContractDetailsRequestTypeDef]
    ) -> GetEnterpriseSupportContractDetailsResponseTypeDef:
        """
        Returns Enterprise Support contract details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_enterprise_support_contract_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_enterprise_support_contract_details)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Returns the resource-based policy document attached to the resource in
        <code>JSON</code> format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_resource_policy)
        """

    def list_billing_views(
        self, **kwargs: Unpack[ListBillingViewsRequestTypeDef]
    ) -> ListBillingViewsResponseTypeDef:
        """
        Lists the billing views available for a given time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/list_billing_views.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#list_billing_views)
        """

    def list_enterprise_support_linked_account_charges(
        self, **kwargs: Unpack[ListEnterpriseSupportLinkedAccountChargesRequestTypeDef]
    ) -> ListEnterpriseSupportLinkedAccountChargesResponseTypeDef:
        """
        Returns Support-eligible spend broken down at linked account level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/list_enterprise_support_linked_account_charges.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#list_enterprise_support_linked_account_charges)
        """

    def list_source_views_for_billing_view(
        self, **kwargs: Unpack[ListSourceViewsForBillingViewRequestTypeDef]
    ) -> ListSourceViewsForBillingViewResponseTypeDef:
        """
        Lists the source views (managed Amazon Web Services billing views) associated
        with the billing view.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/list_source_views_for_billing_view.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#list_source_views_for_billing_view)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags associated with the billing view resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#list_tags_for_resource)
        """

    def redeem_credits(self, **kwargs: Unpack[RedeemCreditsRequestTypeDef]) -> dict[str, Any]:
        """
        Redeems an Amazon Web Services promotional credit code on behalf of the calling
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/redeem_credits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#redeem_credits)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        An API operation for adding one or more tags (key-value pairs) to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#untag_resource)
        """

    def update_billing_preferences(
        self, **kwargs: Unpack[UpdateBillingPreferencesRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates billing preferences for the specified feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/update_billing_preferences.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#update_billing_preferences)
        """

    def update_billing_view(
        self, **kwargs: Unpack[UpdateBillingViewRequestTypeDef]
    ) -> UpdateBillingViewResponseTypeDef:
        """
        An API to update the attributes of the billing view.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/update_billing_view.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#update_billing_view)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_credit_allocation_history"]
    ) -> GetCreditAllocationHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_billing_views"]
    ) -> ListBillingViewsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_enterprise_support_linked_account_charges"]
    ) -> ListEnterpriseSupportLinkedAccountChargesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_source_views_for_billing_view"]
    ) -> ListSourceViewsForBillingViewPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/client/#get_paginator)
        """
