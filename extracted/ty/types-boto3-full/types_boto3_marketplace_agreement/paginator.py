"""
Type annotations for marketplace-agreement service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_marketplace_agreement.client import AgreementServiceClient
    from types_boto3_marketplace_agreement.paginator import (
        ListAgreementCancellationRequestsPaginator,
        ListAgreementInvoiceLineItemsPaginator,
        ListAgreementPaymentRequestsPaginator,
        ListBillingAdjustmentRequestsPaginator,
    )

    session = Session()
    client: AgreementServiceClient = session.client("marketplace-agreement")

    list_agreement_cancellation_requests_paginator: ListAgreementCancellationRequestsPaginator = client.get_paginator("list_agreement_cancellation_requests")
    list_agreement_invoice_line_items_paginator: ListAgreementInvoiceLineItemsPaginator = client.get_paginator("list_agreement_invoice_line_items")
    list_agreement_payment_requests_paginator: ListAgreementPaymentRequestsPaginator = client.get_paginator("list_agreement_payment_requests")
    list_billing_adjustment_requests_paginator: ListBillingAdjustmentRequestsPaginator = client.get_paginator("list_billing_adjustment_requests")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAgreementCancellationRequestsInputPaginateTypeDef,
    ListAgreementCancellationRequestsOutputTypeDef,
    ListAgreementInvoiceLineItemsInputPaginateTypeDef,
    ListAgreementInvoiceLineItemsOutputTypeDef,
    ListAgreementPaymentRequestsInputPaginateTypeDef,
    ListAgreementPaymentRequestsOutputTypeDef,
    ListBillingAdjustmentRequestsInputPaginateTypeDef,
    ListBillingAdjustmentRequestsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAgreementCancellationRequestsPaginator",
    "ListAgreementInvoiceLineItemsPaginator",
    "ListAgreementPaymentRequestsPaginator",
    "ListBillingAdjustmentRequestsPaginator",
)


if TYPE_CHECKING:
    _ListAgreementCancellationRequestsPaginatorBase = Paginator[
        ListAgreementCancellationRequestsOutputTypeDef
    ]
else:
    _ListAgreementCancellationRequestsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAgreementCancellationRequestsPaginator(_ListAgreementCancellationRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCancellationRequests.html#AgreementService.Paginator.ListAgreementCancellationRequests)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/paginators/#listagreementcancellationrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementCancellationRequestsInputPaginateTypeDef]
    ) -> PageIterator[ListAgreementCancellationRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCancellationRequests.html#AgreementService.Paginator.ListAgreementCancellationRequests.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/paginators/#listagreementcancellationrequestspaginator)
        """


if TYPE_CHECKING:
    _ListAgreementInvoiceLineItemsPaginatorBase = Paginator[
        ListAgreementInvoiceLineItemsOutputTypeDef
    ]
else:
    _ListAgreementInvoiceLineItemsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAgreementInvoiceLineItemsPaginator(_ListAgreementInvoiceLineItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementInvoiceLineItems.html#AgreementService.Paginator.ListAgreementInvoiceLineItems)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/paginators/#listagreementinvoicelineitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementInvoiceLineItemsInputPaginateTypeDef]
    ) -> PageIterator[ListAgreementInvoiceLineItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementInvoiceLineItems.html#AgreementService.Paginator.ListAgreementInvoiceLineItems.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/paginators/#listagreementinvoicelineitemspaginator)
        """


if TYPE_CHECKING:
    _ListAgreementPaymentRequestsPaginatorBase = Paginator[
        ListAgreementPaymentRequestsOutputTypeDef
    ]
else:
    _ListAgreementPaymentRequestsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAgreementPaymentRequestsPaginator(_ListAgreementPaymentRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementPaymentRequests.html#AgreementService.Paginator.ListAgreementPaymentRequests)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/paginators/#listagreementpaymentrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementPaymentRequestsInputPaginateTypeDef]
    ) -> PageIterator[ListAgreementPaymentRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementPaymentRequests.html#AgreementService.Paginator.ListAgreementPaymentRequests.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/paginators/#listagreementpaymentrequestspaginator)
        """


if TYPE_CHECKING:
    _ListBillingAdjustmentRequestsPaginatorBase = Paginator[
        ListBillingAdjustmentRequestsOutputTypeDef
    ]
else:
    _ListBillingAdjustmentRequestsPaginatorBase = Paginator  # type: ignore[assignment]


class ListBillingAdjustmentRequestsPaginator(_ListBillingAdjustmentRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListBillingAdjustmentRequests.html#AgreementService.Paginator.ListBillingAdjustmentRequests)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/paginators/#listbillingadjustmentrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingAdjustmentRequestsInputPaginateTypeDef]
    ) -> PageIterator[ListBillingAdjustmentRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListBillingAdjustmentRequests.html#AgreementService.Paginator.ListBillingAdjustmentRequests.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/paginators/#listbillingadjustmentrequestspaginator)
        """
