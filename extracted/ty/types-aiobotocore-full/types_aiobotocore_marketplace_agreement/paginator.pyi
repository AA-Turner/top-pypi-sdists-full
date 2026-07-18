"""
Type annotations for marketplace-agreement service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_marketplace_agreement.client import AgreementServiceClient
    from types_aiobotocore_marketplace_agreement.paginator import (
        GetAgreementEntitlementsPaginator,
        GetAgreementTermsPaginator,
        ListAgreementCancellationRequestsPaginator,
        ListAgreementChargesPaginator,
        ListAgreementInvoiceLineItemsPaginator,
        ListAgreementPaymentRequestsPaginator,
        ListBillingAdjustmentRequestsPaginator,
        SearchAgreementsPaginator,
    )

    session = get_session()
    with session.create_client("marketplace-agreement") as client:
        client: AgreementServiceClient

        get_agreement_entitlements_paginator: GetAgreementEntitlementsPaginator = client.get_paginator("get_agreement_entitlements")
        get_agreement_terms_paginator: GetAgreementTermsPaginator = client.get_paginator("get_agreement_terms")
        list_agreement_cancellation_requests_paginator: ListAgreementCancellationRequestsPaginator = client.get_paginator("list_agreement_cancellation_requests")
        list_agreement_charges_paginator: ListAgreementChargesPaginator = client.get_paginator("list_agreement_charges")
        list_agreement_invoice_line_items_paginator: ListAgreementInvoiceLineItemsPaginator = client.get_paginator("list_agreement_invoice_line_items")
        list_agreement_payment_requests_paginator: ListAgreementPaymentRequestsPaginator = client.get_paginator("list_agreement_payment_requests")
        list_billing_adjustment_requests_paginator: ListBillingAdjustmentRequestsPaginator = client.get_paginator("list_billing_adjustment_requests")
        search_agreements_paginator: SearchAgreementsPaginator = client.get_paginator("search_agreements")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetAgreementEntitlementsInputPaginateTypeDef,
    GetAgreementEntitlementsOutputTypeDef,
    GetAgreementTermsInputPaginateTypeDef,
    GetAgreementTermsOutputTypeDef,
    ListAgreementCancellationRequestsInputPaginateTypeDef,
    ListAgreementCancellationRequestsOutputTypeDef,
    ListAgreementChargesInputPaginateTypeDef,
    ListAgreementChargesOutputTypeDef,
    ListAgreementInvoiceLineItemsInputPaginateTypeDef,
    ListAgreementInvoiceLineItemsOutputTypeDef,
    ListAgreementPaymentRequestsInputPaginateTypeDef,
    ListAgreementPaymentRequestsOutputTypeDef,
    ListBillingAdjustmentRequestsInputPaginateTypeDef,
    ListBillingAdjustmentRequestsOutputTypeDef,
    SearchAgreementsInputPaginateTypeDef,
    SearchAgreementsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetAgreementEntitlementsPaginator",
    "GetAgreementTermsPaginator",
    "ListAgreementCancellationRequestsPaginator",
    "ListAgreementChargesPaginator",
    "ListAgreementInvoiceLineItemsPaginator",
    "ListAgreementPaymentRequestsPaginator",
    "ListBillingAdjustmentRequestsPaginator",
    "SearchAgreementsPaginator",
)

if TYPE_CHECKING:
    _GetAgreementEntitlementsPaginatorBase = AioPaginator[GetAgreementEntitlementsOutputTypeDef]
else:
    _GetAgreementEntitlementsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetAgreementEntitlementsPaginator(_GetAgreementEntitlementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementEntitlements.html#AgreementService.Paginator.GetAgreementEntitlements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#getagreemententitlementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgreementEntitlementsInputPaginateTypeDef]
    ) -> AioPageIterator[GetAgreementEntitlementsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementEntitlements.html#AgreementService.Paginator.GetAgreementEntitlements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#getagreemententitlementspaginator)
        """

if TYPE_CHECKING:
    _GetAgreementTermsPaginatorBase = AioPaginator[GetAgreementTermsOutputTypeDef]
else:
    _GetAgreementTermsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetAgreementTermsPaginator(_GetAgreementTermsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementTerms.html#AgreementService.Paginator.GetAgreementTerms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#getagreementtermspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgreementTermsInputPaginateTypeDef]
    ) -> AioPageIterator[GetAgreementTermsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementTerms.html#AgreementService.Paginator.GetAgreementTerms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#getagreementtermspaginator)
        """

if TYPE_CHECKING:
    _ListAgreementCancellationRequestsPaginatorBase = AioPaginator[
        ListAgreementCancellationRequestsOutputTypeDef
    ]
else:
    _ListAgreementCancellationRequestsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgreementCancellationRequestsPaginator(_ListAgreementCancellationRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCancellationRequests.html#AgreementService.Paginator.ListAgreementCancellationRequests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listagreementcancellationrequestspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementCancellationRequestsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAgreementCancellationRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCancellationRequests.html#AgreementService.Paginator.ListAgreementCancellationRequests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listagreementcancellationrequestspaginator)
        """

if TYPE_CHECKING:
    _ListAgreementChargesPaginatorBase = AioPaginator[ListAgreementChargesOutputTypeDef]
else:
    _ListAgreementChargesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgreementChargesPaginator(_ListAgreementChargesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCharges.html#AgreementService.Paginator.ListAgreementCharges)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listagreementchargespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementChargesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAgreementChargesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCharges.html#AgreementService.Paginator.ListAgreementCharges.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listagreementchargespaginator)
        """

if TYPE_CHECKING:
    _ListAgreementInvoiceLineItemsPaginatorBase = AioPaginator[
        ListAgreementInvoiceLineItemsOutputTypeDef
    ]
else:
    _ListAgreementInvoiceLineItemsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgreementInvoiceLineItemsPaginator(_ListAgreementInvoiceLineItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementInvoiceLineItems.html#AgreementService.Paginator.ListAgreementInvoiceLineItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listagreementinvoicelineitemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementInvoiceLineItemsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAgreementInvoiceLineItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementInvoiceLineItems.html#AgreementService.Paginator.ListAgreementInvoiceLineItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listagreementinvoicelineitemspaginator)
        """

if TYPE_CHECKING:
    _ListAgreementPaymentRequestsPaginatorBase = AioPaginator[
        ListAgreementPaymentRequestsOutputTypeDef
    ]
else:
    _ListAgreementPaymentRequestsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgreementPaymentRequestsPaginator(_ListAgreementPaymentRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementPaymentRequests.html#AgreementService.Paginator.ListAgreementPaymentRequests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listagreementpaymentrequestspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementPaymentRequestsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAgreementPaymentRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementPaymentRequests.html#AgreementService.Paginator.ListAgreementPaymentRequests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listagreementpaymentrequestspaginator)
        """

if TYPE_CHECKING:
    _ListBillingAdjustmentRequestsPaginatorBase = AioPaginator[
        ListBillingAdjustmentRequestsOutputTypeDef
    ]
else:
    _ListBillingAdjustmentRequestsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBillingAdjustmentRequestsPaginator(_ListBillingAdjustmentRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListBillingAdjustmentRequests.html#AgreementService.Paginator.ListBillingAdjustmentRequests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listbillingadjustmentrequestspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingAdjustmentRequestsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBillingAdjustmentRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListBillingAdjustmentRequests.html#AgreementService.Paginator.ListBillingAdjustmentRequests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#listbillingadjustmentrequestspaginator)
        """

if TYPE_CHECKING:
    _SearchAgreementsPaginatorBase = AioPaginator[SearchAgreementsOutputTypeDef]
else:
    _SearchAgreementsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchAgreementsPaginator(_SearchAgreementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/SearchAgreements.html#AgreementService.Paginator.SearchAgreements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#searchagreementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchAgreementsInputPaginateTypeDef]
    ) -> AioPageIterator[SearchAgreementsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/SearchAgreements.html#AgreementService.Paginator.SearchAgreements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/#searchagreementspaginator)
        """
