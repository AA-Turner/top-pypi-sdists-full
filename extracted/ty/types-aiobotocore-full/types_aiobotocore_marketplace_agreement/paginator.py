"""
Type annotations for marketplace-agreement service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_marketplace_agreement.client import AgreementServiceClient
    from types_aiobotocore_marketplace_agreement.paginator import (
        ListAgreementCancellationRequestsPaginator,
        ListAgreementInvoiceLineItemsPaginator,
        ListAgreementPaymentRequestsPaginator,
        ListBillingAdjustmentRequestsPaginator,
    )

    session = get_session()
    with session.create_client("marketplace-agreement") as client:
        client: AgreementServiceClient

        list_agreement_cancellation_requests_paginator: ListAgreementCancellationRequestsPaginator = client.get_paginator("list_agreement_cancellation_requests")
        list_agreement_invoice_line_items_paginator: ListAgreementInvoiceLineItemsPaginator = client.get_paginator("list_agreement_invoice_line_items")
        list_agreement_payment_requests_paginator: ListAgreementPaymentRequestsPaginator = client.get_paginator("list_agreement_payment_requests")
        list_billing_adjustment_requests_paginator: ListBillingAdjustmentRequestsPaginator = client.get_paginator("list_billing_adjustment_requests")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
