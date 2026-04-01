"""
Type annotations for marketplace-agreement service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_marketplace_agreement.client import AgreementServiceClient

    session = Session()
    client: AgreementServiceClient = session.client("marketplace-agreement")
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
    ListAgreementCancellationRequestsPaginator,
    ListAgreementInvoiceLineItemsPaginator,
    ListAgreementPaymentRequestsPaginator,
    ListBillingAdjustmentRequestsPaginator,
)
from .type_defs import (
    BatchCreateBillingAdjustmentRequestInputTypeDef,
    BatchCreateBillingAdjustmentRequestOutputTypeDef,
    CancelAgreementCancellationRequestInputTypeDef,
    CancelAgreementCancellationRequestOutputTypeDef,
    CancelAgreementPaymentRequestInputTypeDef,
    CancelAgreementPaymentRequestOutputTypeDef,
    DescribeAgreementInputTypeDef,
    DescribeAgreementOutputTypeDef,
    GetAgreementCancellationRequestInputTypeDef,
    GetAgreementCancellationRequestOutputTypeDef,
    GetAgreementPaymentRequestInputTypeDef,
    GetAgreementPaymentRequestOutputTypeDef,
    GetAgreementTermsInputTypeDef,
    GetAgreementTermsOutputTypeDef,
    GetBillingAdjustmentRequestInputTypeDef,
    GetBillingAdjustmentRequestOutputTypeDef,
    ListAgreementCancellationRequestsInputTypeDef,
    ListAgreementCancellationRequestsOutputTypeDef,
    ListAgreementInvoiceLineItemsInputTypeDef,
    ListAgreementInvoiceLineItemsOutputTypeDef,
    ListAgreementPaymentRequestsInputTypeDef,
    ListAgreementPaymentRequestsOutputTypeDef,
    ListBillingAdjustmentRequestsInputTypeDef,
    ListBillingAdjustmentRequestsOutputTypeDef,
    SearchAgreementsInputTypeDef,
    SearchAgreementsOutputTypeDef,
    SendAgreementCancellationRequestInputTypeDef,
    SendAgreementCancellationRequestOutputTypeDef,
    SendAgreementPaymentRequestInputTypeDef,
    SendAgreementPaymentRequestOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AgreementServiceClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class AgreementServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement.html#AgreementService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AgreementServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement.html#AgreementService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#generate_presigned_url)
        """

    def batch_create_billing_adjustment_request(
        self, **kwargs: Unpack[BatchCreateBillingAdjustmentRequestInputTypeDef]
    ) -> BatchCreateBillingAdjustmentRequestOutputTypeDef:
        """
        Allows sellers (proposers) to submit billing adjustment requests for one or
        more invoices within an agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/batch_create_billing_adjustment_request.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#batch_create_billing_adjustment_request)
        """

    def cancel_agreement_cancellation_request(
        self, **kwargs: Unpack[CancelAgreementCancellationRequestInputTypeDef]
    ) -> CancelAgreementCancellationRequestOutputTypeDef:
        """
        Allows sellers (proposers) to withdraw an existing agreement cancellation
        request that is in a pending state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/cancel_agreement_cancellation_request.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#cancel_agreement_cancellation_request)
        """

    def cancel_agreement_payment_request(
        self, **kwargs: Unpack[CancelAgreementPaymentRequestInputTypeDef]
    ) -> CancelAgreementPaymentRequestOutputTypeDef:
        """
        Allows sellers (proposers) to cancel a payment request that is in
        <code>PENDING_APPROVAL</code> status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/cancel_agreement_payment_request.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#cancel_agreement_payment_request)
        """

    def describe_agreement(
        self, **kwargs: Unpack[DescribeAgreementInputTypeDef]
    ) -> DescribeAgreementOutputTypeDef:
        """
        Provides details about an agreement, such as the proposer, acceptor, start
        date, and end date.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/describe_agreement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#describe_agreement)
        """

    def get_agreement_cancellation_request(
        self, **kwargs: Unpack[GetAgreementCancellationRequestInputTypeDef]
    ) -> GetAgreementCancellationRequestOutputTypeDef:
        """
        Retrieves detailed information about a specific agreement cancellation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_agreement_cancellation_request.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#get_agreement_cancellation_request)
        """

    def get_agreement_payment_request(
        self, **kwargs: Unpack[GetAgreementPaymentRequestInputTypeDef]
    ) -> GetAgreementPaymentRequestOutputTypeDef:
        """
        Retrieves detailed information about a specific payment request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_agreement_payment_request.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#get_agreement_payment_request)
        """

    def get_agreement_terms(
        self, **kwargs: Unpack[GetAgreementTermsInputTypeDef]
    ) -> GetAgreementTermsOutputTypeDef:
        """
        Obtains details about the terms in an agreement that you participated in as
        proposer or acceptor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_agreement_terms.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#get_agreement_terms)
        """

    def get_billing_adjustment_request(
        self, **kwargs: Unpack[GetBillingAdjustmentRequestInputTypeDef]
    ) -> GetBillingAdjustmentRequestOutputTypeDef:
        """
        Retrieves detailed information about a specific billing adjustment request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_billing_adjustment_request.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#get_billing_adjustment_request)
        """

    def list_agreement_cancellation_requests(
        self, **kwargs: Unpack[ListAgreementCancellationRequestsInputTypeDef]
    ) -> ListAgreementCancellationRequestsOutputTypeDef:
        """
        Lists agreement cancellation requests available to you as a seller or buyer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/list_agreement_cancellation_requests.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#list_agreement_cancellation_requests)
        """

    def list_agreement_invoice_line_items(
        self, **kwargs: Unpack[ListAgreementInvoiceLineItemsInputTypeDef]
    ) -> ListAgreementInvoiceLineItemsOutputTypeDef:
        """
        Allows sellers (proposers) to retrieve aggregated billing data from AWS
        Marketplace agreements using flexible grouping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/list_agreement_invoice_line_items.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#list_agreement_invoice_line_items)
        """

    def list_agreement_payment_requests(
        self, **kwargs: Unpack[ListAgreementPaymentRequestsInputTypeDef]
    ) -> ListAgreementPaymentRequestsOutputTypeDef:
        """
        Lists payment requests available to you as a seller or buyer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/list_agreement_payment_requests.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#list_agreement_payment_requests)
        """

    def list_billing_adjustment_requests(
        self, **kwargs: Unpack[ListBillingAdjustmentRequestsInputTypeDef]
    ) -> ListBillingAdjustmentRequestsOutputTypeDef:
        """
        Lists billing adjustment requests for a specific agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/list_billing_adjustment_requests.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#list_billing_adjustment_requests)
        """

    def search_agreements(
        self, **kwargs: Unpack[SearchAgreementsInputTypeDef]
    ) -> SearchAgreementsOutputTypeDef:
        """
        Searches across all agreements that a proposer has in AWS Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/search_agreements.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#search_agreements)
        """

    def send_agreement_cancellation_request(
        self, **kwargs: Unpack[SendAgreementCancellationRequestInputTypeDef]
    ) -> SendAgreementCancellationRequestOutputTypeDef:
        """
        Allows sellers (proposers) to submit a cancellation request for an active
        agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/send_agreement_cancellation_request.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#send_agreement_cancellation_request)
        """

    def send_agreement_payment_request(
        self, **kwargs: Unpack[SendAgreementPaymentRequestInputTypeDef]
    ) -> SendAgreementPaymentRequestOutputTypeDef:
        """
        Allows sellers (proposers) to submit a payment request to buyers (acceptors)
        for a specific charge amount for an agreement that includes a
        <code>VariablePaymentTerm</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/send_agreement_payment_request.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#send_agreement_payment_request)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agreement_cancellation_requests"]
    ) -> ListAgreementCancellationRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agreement_invoice_line_items"]
    ) -> ListAgreementInvoiceLineItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agreement_payment_requests"]
    ) -> ListAgreementPaymentRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_billing_adjustment_requests"]
    ) -> ListBillingAdjustmentRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/client/#get_paginator)
        """
