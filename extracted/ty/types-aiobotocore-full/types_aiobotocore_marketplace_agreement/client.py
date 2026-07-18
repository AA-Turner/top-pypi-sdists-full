"""
Type annotations for marketplace-agreement service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_agreement.client import AgreementServiceClient

    session = get_session()
    async with session.create_client("marketplace-agreement") as client:
        client: AgreementServiceClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    GetAgreementEntitlementsPaginator,
    GetAgreementTermsPaginator,
    ListAgreementCancellationRequestsPaginator,
    ListAgreementChargesPaginator,
    ListAgreementInvoiceLineItemsPaginator,
    ListAgreementPaymentRequestsPaginator,
    ListBillingAdjustmentRequestsPaginator,
    SearchAgreementsPaginator,
)
from .type_defs import (
    AcceptAgreementCancellationRequestInputTypeDef,
    AcceptAgreementCancellationRequestOutputTypeDef,
    AcceptAgreementPaymentRequestInputTypeDef,
    AcceptAgreementPaymentRequestOutputTypeDef,
    AcceptAgreementRequestInputTypeDef,
    AcceptAgreementRequestOutputTypeDef,
    BatchCreateBillingAdjustmentRequestInputTypeDef,
    BatchCreateBillingAdjustmentRequestOutputTypeDef,
    CancelAgreementCancellationRequestInputTypeDef,
    CancelAgreementCancellationRequestOutputTypeDef,
    CancelAgreementInputTypeDef,
    CancelAgreementPaymentRequestInputTypeDef,
    CancelAgreementPaymentRequestOutputTypeDef,
    CreateAgreementRequestInputTypeDef,
    CreateAgreementRequestOutputTypeDef,
    DescribeAgreementInputTypeDef,
    DescribeAgreementOutputTypeDef,
    GetAgreementCancellationRequestInputTypeDef,
    GetAgreementCancellationRequestOutputTypeDef,
    GetAgreementEntitlementsInputTypeDef,
    GetAgreementEntitlementsOutputTypeDef,
    GetAgreementPaymentRequestInputTypeDef,
    GetAgreementPaymentRequestOutputTypeDef,
    GetAgreementTermsInputTypeDef,
    GetAgreementTermsOutputTypeDef,
    GetBillingAdjustmentRequestInputTypeDef,
    GetBillingAdjustmentRequestOutputTypeDef,
    ListAgreementCancellationRequestsInputTypeDef,
    ListAgreementCancellationRequestsOutputTypeDef,
    ListAgreementChargesInputTypeDef,
    ListAgreementChargesOutputTypeDef,
    ListAgreementInvoiceLineItemsInputTypeDef,
    ListAgreementInvoiceLineItemsOutputTypeDef,
    ListAgreementPaymentRequestsInputTypeDef,
    ListAgreementPaymentRequestsOutputTypeDef,
    ListBillingAdjustmentRequestsInputTypeDef,
    ListBillingAdjustmentRequestsOutputTypeDef,
    RejectAgreementCancellationRequestInputTypeDef,
    RejectAgreementCancellationRequestOutputTypeDef,
    RejectAgreementPaymentRequestInputTypeDef,
    RejectAgreementPaymentRequestOutputTypeDef,
    SearchAgreementsInputTypeDef,
    SearchAgreementsOutputTypeDef,
    SendAgreementCancellationRequestInputTypeDef,
    SendAgreementCancellationRequestOutputTypeDef,
    SendAgreementPaymentRequestInputTypeDef,
    SendAgreementPaymentRequestOutputTypeDef,
    UpdatePurchaseOrdersInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("AgreementServiceClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class AgreementServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement.html#AgreementService.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AgreementServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement.html#AgreementService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#generate_presigned_url)
        """

    async def accept_agreement_cancellation_request(
        self, **kwargs: Unpack[AcceptAgreementCancellationRequestInputTypeDef]
    ) -> AcceptAgreementCancellationRequestOutputTypeDef:
        """
        Allows buyers (acceptors) to accept a cancellation request that is in
        <code>PENDING_APPROVAL</code> status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/accept_agreement_cancellation_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#accept_agreement_cancellation_request)
        """

    async def accept_agreement_payment_request(
        self, **kwargs: Unpack[AcceptAgreementPaymentRequestInputTypeDef]
    ) -> AcceptAgreementPaymentRequestOutputTypeDef:
        """
        Allows buyers (acceptors) to accept a payment request that is in
        <code>PENDING_APPROVAL</code> status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/accept_agreement_payment_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#accept_agreement_payment_request)
        """

    async def accept_agreement_request(
        self, **kwargs: Unpack[AcceptAgreementRequestInputTypeDef]
    ) -> AcceptAgreementRequestOutputTypeDef:
        """
        Accepts an agreement request to finalize the agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/accept_agreement_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#accept_agreement_request)
        """

    async def batch_create_billing_adjustment_request(
        self, **kwargs: Unpack[BatchCreateBillingAdjustmentRequestInputTypeDef]
    ) -> BatchCreateBillingAdjustmentRequestOutputTypeDef:
        """
        Allows sellers (proposers) to submit billing adjustment requests for one or
        more invoices within an agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/batch_create_billing_adjustment_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#batch_create_billing_adjustment_request)
        """

    async def cancel_agreement(
        self, **kwargs: Unpack[CancelAgreementInputTypeDef]
    ) -> dict[str, Any]:
        """
        Allows an acceptor to cancel an active agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/cancel_agreement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#cancel_agreement)
        """

    async def cancel_agreement_cancellation_request(
        self, **kwargs: Unpack[CancelAgreementCancellationRequestInputTypeDef]
    ) -> CancelAgreementCancellationRequestOutputTypeDef:
        """
        Allows sellers (proposers) to withdraw an existing agreement cancellation
        request that is in a pending state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/cancel_agreement_cancellation_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#cancel_agreement_cancellation_request)
        """

    async def cancel_agreement_payment_request(
        self, **kwargs: Unpack[CancelAgreementPaymentRequestInputTypeDef]
    ) -> CancelAgreementPaymentRequestOutputTypeDef:
        """
        Allows sellers (proposers) to cancel a payment request that is in
        <code>PENDING_APPROVAL</code> status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/cancel_agreement_payment_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#cancel_agreement_payment_request)
        """

    async def create_agreement_request(
        self, **kwargs: Unpack[CreateAgreementRequestInputTypeDef]
    ) -> CreateAgreementRequestOutputTypeDef:
        """
        Creates an agreement request that acts as a quote for the terms you want to
        accept.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/create_agreement_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#create_agreement_request)
        """

    async def describe_agreement(
        self, **kwargs: Unpack[DescribeAgreementInputTypeDef]
    ) -> DescribeAgreementOutputTypeDef:
        """
        Provides details about an agreement, such as the proposer, acceptor, start
        date, and end date.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/describe_agreement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#describe_agreement)
        """

    async def get_agreement_cancellation_request(
        self, **kwargs: Unpack[GetAgreementCancellationRequestInputTypeDef]
    ) -> GetAgreementCancellationRequestOutputTypeDef:
        """
        Retrieves detailed information about a specific agreement cancellation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_agreement_cancellation_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_agreement_cancellation_request)
        """

    async def get_agreement_entitlements(
        self, **kwargs: Unpack[GetAgreementEntitlementsInputTypeDef]
    ) -> GetAgreementEntitlementsOutputTypeDef:
        """
        Obtains details about the entitlements of an agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_agreement_entitlements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_agreement_entitlements)
        """

    async def get_agreement_payment_request(
        self, **kwargs: Unpack[GetAgreementPaymentRequestInputTypeDef]
    ) -> GetAgreementPaymentRequestOutputTypeDef:
        """
        Retrieves detailed information about a specific payment request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_agreement_payment_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_agreement_payment_request)
        """

    async def get_agreement_terms(
        self, **kwargs: Unpack[GetAgreementTermsInputTypeDef]
    ) -> GetAgreementTermsOutputTypeDef:
        """
        Obtains details about the terms in an agreement that you participated in as
        proposer or acceptor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_agreement_terms.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_agreement_terms)
        """

    async def get_billing_adjustment_request(
        self, **kwargs: Unpack[GetBillingAdjustmentRequestInputTypeDef]
    ) -> GetBillingAdjustmentRequestOutputTypeDef:
        """
        Retrieves detailed information about a specific billing adjustment request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_billing_adjustment_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_billing_adjustment_request)
        """

    async def list_agreement_cancellation_requests(
        self, **kwargs: Unpack[ListAgreementCancellationRequestsInputTypeDef]
    ) -> ListAgreementCancellationRequestsOutputTypeDef:
        """
        Lists agreement cancellation requests available to you as a seller or buyer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/list_agreement_cancellation_requests.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#list_agreement_cancellation_requests)
        """

    async def list_agreement_charges(
        self, **kwargs: Unpack[ListAgreementChargesInputTypeDef]
    ) -> ListAgreementChargesOutputTypeDef:
        """
        Allows acceptors to view charges and purchase orders that are associated with
        an agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/list_agreement_charges.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#list_agreement_charges)
        """

    async def list_agreement_invoice_line_items(
        self, **kwargs: Unpack[ListAgreementInvoiceLineItemsInputTypeDef]
    ) -> ListAgreementInvoiceLineItemsOutputTypeDef:
        """
        Allows sellers (proposers) to retrieve aggregated billing data from AWS
        Marketplace agreements using flexible grouping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/list_agreement_invoice_line_items.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#list_agreement_invoice_line_items)
        """

    async def list_agreement_payment_requests(
        self, **kwargs: Unpack[ListAgreementPaymentRequestsInputTypeDef]
    ) -> ListAgreementPaymentRequestsOutputTypeDef:
        """
        Lists payment requests available to you as a seller or buyer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/list_agreement_payment_requests.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#list_agreement_payment_requests)
        """

    async def list_billing_adjustment_requests(
        self, **kwargs: Unpack[ListBillingAdjustmentRequestsInputTypeDef]
    ) -> ListBillingAdjustmentRequestsOutputTypeDef:
        """
        Lists billing adjustment requests for a specific agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/list_billing_adjustment_requests.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#list_billing_adjustment_requests)
        """

    async def reject_agreement_cancellation_request(
        self, **kwargs: Unpack[RejectAgreementCancellationRequestInputTypeDef]
    ) -> RejectAgreementCancellationRequestOutputTypeDef:
        """
        Allows buyers (acceptors) to reject a cancellation request that is in
        <code>PENDING_APPROVAL</code> status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/reject_agreement_cancellation_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#reject_agreement_cancellation_request)
        """

    async def reject_agreement_payment_request(
        self, **kwargs: Unpack[RejectAgreementPaymentRequestInputTypeDef]
    ) -> RejectAgreementPaymentRequestOutputTypeDef:
        """
        Allows buyers (acceptors) to reject a payment request that is in
        <code>PENDING_APPROVAL</code> status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/reject_agreement_payment_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#reject_agreement_payment_request)
        """

    async def search_agreements(
        self, **kwargs: Unpack[SearchAgreementsInputTypeDef]
    ) -> SearchAgreementsOutputTypeDef:
        """
        Searches across all agreements that a proposer or an acceptor has in AWS
        Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/search_agreements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#search_agreements)
        """

    async def send_agreement_cancellation_request(
        self, **kwargs: Unpack[SendAgreementCancellationRequestInputTypeDef]
    ) -> SendAgreementCancellationRequestOutputTypeDef:
        """
        Allows sellers (proposers) to submit a cancellation request for an active
        agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/send_agreement_cancellation_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#send_agreement_cancellation_request)
        """

    async def send_agreement_payment_request(
        self, **kwargs: Unpack[SendAgreementPaymentRequestInputTypeDef]
    ) -> SendAgreementPaymentRequestOutputTypeDef:
        """
        Allows sellers (proposers) to submit a payment request to buyers (acceptors)
        for a specific charge amount for an agreement that includes a
        <code>VariablePaymentTerm</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/send_agreement_payment_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#send_agreement_payment_request)
        """

    async def update_purchase_orders(
        self, **kwargs: Unpack[UpdatePurchaseOrdersInputTypeDef]
    ) -> dict[str, Any]:
        """
        Allows acceptors to associate purchase orders with agreement charges after an
        agreement is created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/update_purchase_orders.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#update_purchase_orders)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_agreement_entitlements"]
    ) -> GetAgreementEntitlementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_agreement_terms"]
    ) -> GetAgreementTermsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agreement_cancellation_requests"]
    ) -> ListAgreementCancellationRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agreement_charges"]
    ) -> ListAgreementChargesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agreement_invoice_line_items"]
    ) -> ListAgreementInvoiceLineItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agreement_payment_requests"]
    ) -> ListAgreementPaymentRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_billing_adjustment_requests"]
    ) -> ListBillingAdjustmentRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_agreements"]
    ) -> SearchAgreementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement.html#AgreementService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement.html#AgreementService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/client/)
        """
