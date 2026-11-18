"""
Type annotations for marketplace-agreement service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_marketplace_agreement.client import AgreementServiceClient
    from mypy_boto3_marketplace_agreement.paginator import (
        GetAgreementEntitlementsPaginator,
        GetAgreementRequestApprovalPlansPaginator,
        GetAgreementRequestTermsPaginator,
        GetAgreementTermsPaginator,
        ListAgreementApprovalsPaginator,
        ListAgreementCancellationRequestsPaginator,
        ListAgreementChargesPaginator,
        ListAgreementInvoiceLineItemsPaginator,
        ListAgreementPaymentRequestsPaginator,
        ListAgreementRequestsPaginator,
        ListBillingAdjustmentRequestsPaginator,
        SearchAgreementsPaginator,
    )

    session = Session()
    client: AgreementServiceClient = session.client("marketplace-agreement")

    get_agreement_entitlements_paginator: GetAgreementEntitlementsPaginator = client.get_paginator("get_agreement_entitlements")
    get_agreement_request_approval_plans_paginator: GetAgreementRequestApprovalPlansPaginator = client.get_paginator("get_agreement_request_approval_plans")
    get_agreement_request_terms_paginator: GetAgreementRequestTermsPaginator = client.get_paginator("get_agreement_request_terms")
    get_agreement_terms_paginator: GetAgreementTermsPaginator = client.get_paginator("get_agreement_terms")
    list_agreement_approvals_paginator: ListAgreementApprovalsPaginator = client.get_paginator("list_agreement_approvals")
    list_agreement_cancellation_requests_paginator: ListAgreementCancellationRequestsPaginator = client.get_paginator("list_agreement_cancellation_requests")
    list_agreement_charges_paginator: ListAgreementChargesPaginator = client.get_paginator("list_agreement_charges")
    list_agreement_invoice_line_items_paginator: ListAgreementInvoiceLineItemsPaginator = client.get_paginator("list_agreement_invoice_line_items")
    list_agreement_payment_requests_paginator: ListAgreementPaymentRequestsPaginator = client.get_paginator("list_agreement_payment_requests")
    list_agreement_requests_paginator: ListAgreementRequestsPaginator = client.get_paginator("list_agreement_requests")
    list_billing_adjustment_requests_paginator: ListBillingAdjustmentRequestsPaginator = client.get_paginator("list_billing_adjustment_requests")
    search_agreements_paginator: SearchAgreementsPaginator = client.get_paginator("search_agreements")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetAgreementEntitlementsInputPaginateTypeDef,
    GetAgreementEntitlementsOutputTypeDef,
    GetAgreementRequestApprovalPlansInputPaginateTypeDef,
    GetAgreementRequestApprovalPlansOutputTypeDef,
    GetAgreementRequestTermsInputPaginateTypeDef,
    GetAgreementRequestTermsOutputTypeDef,
    GetAgreementTermsInputPaginateTypeDef,
    GetAgreementTermsOutputTypeDef,
    ListAgreementApprovalsInputPaginateTypeDef,
    ListAgreementApprovalsOutputTypeDef,
    ListAgreementCancellationRequestsInputPaginateTypeDef,
    ListAgreementCancellationRequestsOutputTypeDef,
    ListAgreementChargesInputPaginateTypeDef,
    ListAgreementChargesOutputTypeDef,
    ListAgreementInvoiceLineItemsInputPaginateTypeDef,
    ListAgreementInvoiceLineItemsOutputTypeDef,
    ListAgreementPaymentRequestsInputPaginateTypeDef,
    ListAgreementPaymentRequestsOutputTypeDef,
    ListAgreementRequestsInputPaginateTypeDef,
    ListAgreementRequestsOutputTypeDef,
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
    "GetAgreementRequestApprovalPlansPaginator",
    "GetAgreementRequestTermsPaginator",
    "GetAgreementTermsPaginator",
    "ListAgreementApprovalsPaginator",
    "ListAgreementCancellationRequestsPaginator",
    "ListAgreementChargesPaginator",
    "ListAgreementInvoiceLineItemsPaginator",
    "ListAgreementPaymentRequestsPaginator",
    "ListAgreementRequestsPaginator",
    "ListBillingAdjustmentRequestsPaginator",
    "SearchAgreementsPaginator",
)


if TYPE_CHECKING:
    _GetAgreementEntitlementsPaginatorBase = Paginator[GetAgreementEntitlementsOutputTypeDef]
else:
    _GetAgreementEntitlementsPaginatorBase = Paginator  # type: ignore[assignment]


class GetAgreementEntitlementsPaginator(_GetAgreementEntitlementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementEntitlements.html#AgreementService.Paginator.GetAgreementEntitlements)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#getagreemententitlementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgreementEntitlementsInputPaginateTypeDef]
    ) -> PageIterator[GetAgreementEntitlementsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementEntitlements.html#AgreementService.Paginator.GetAgreementEntitlements.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#getagreemententitlementspaginator)
        """


if TYPE_CHECKING:
    _GetAgreementRequestApprovalPlansPaginatorBase = Paginator[
        GetAgreementRequestApprovalPlansOutputTypeDef
    ]
else:
    _GetAgreementRequestApprovalPlansPaginatorBase = Paginator  # type: ignore[assignment]


class GetAgreementRequestApprovalPlansPaginator(_GetAgreementRequestApprovalPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementRequestApprovalPlans.html#AgreementService.Paginator.GetAgreementRequestApprovalPlans)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#getagreementrequestapprovalplanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgreementRequestApprovalPlansInputPaginateTypeDef]
    ) -> PageIterator[GetAgreementRequestApprovalPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementRequestApprovalPlans.html#AgreementService.Paginator.GetAgreementRequestApprovalPlans.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#getagreementrequestapprovalplanspaginator)
        """


if TYPE_CHECKING:
    _GetAgreementRequestTermsPaginatorBase = Paginator[GetAgreementRequestTermsOutputTypeDef]
else:
    _GetAgreementRequestTermsPaginatorBase = Paginator  # type: ignore[assignment]


class GetAgreementRequestTermsPaginator(_GetAgreementRequestTermsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementRequestTerms.html#AgreementService.Paginator.GetAgreementRequestTerms)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#getagreementrequesttermspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgreementRequestTermsInputPaginateTypeDef]
    ) -> PageIterator[GetAgreementRequestTermsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementRequestTerms.html#AgreementService.Paginator.GetAgreementRequestTerms.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#getagreementrequesttermspaginator)
        """


if TYPE_CHECKING:
    _GetAgreementTermsPaginatorBase = Paginator[GetAgreementTermsOutputTypeDef]
else:
    _GetAgreementTermsPaginatorBase = Paginator  # type: ignore[assignment]


class GetAgreementTermsPaginator(_GetAgreementTermsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementTerms.html#AgreementService.Paginator.GetAgreementTerms)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#getagreementtermspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgreementTermsInputPaginateTypeDef]
    ) -> PageIterator[GetAgreementTermsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/GetAgreementTerms.html#AgreementService.Paginator.GetAgreementTerms.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#getagreementtermspaginator)
        """


if TYPE_CHECKING:
    _ListAgreementApprovalsPaginatorBase = Paginator[ListAgreementApprovalsOutputTypeDef]
else:
    _ListAgreementApprovalsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAgreementApprovalsPaginator(_ListAgreementApprovalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementApprovals.html#AgreementService.Paginator.ListAgreementApprovals)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementapprovalspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementApprovalsInputPaginateTypeDef]
    ) -> PageIterator[ListAgreementApprovalsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementApprovals.html#AgreementService.Paginator.ListAgreementApprovals.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementapprovalspaginator)
        """


if TYPE_CHECKING:
    _ListAgreementCancellationRequestsPaginatorBase = Paginator[
        ListAgreementCancellationRequestsOutputTypeDef
    ]
else:
    _ListAgreementCancellationRequestsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAgreementCancellationRequestsPaginator(_ListAgreementCancellationRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCancellationRequests.html#AgreementService.Paginator.ListAgreementCancellationRequests)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementcancellationrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementCancellationRequestsInputPaginateTypeDef]
    ) -> PageIterator[ListAgreementCancellationRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCancellationRequests.html#AgreementService.Paginator.ListAgreementCancellationRequests.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementcancellationrequestspaginator)
        """


if TYPE_CHECKING:
    _ListAgreementChargesPaginatorBase = Paginator[ListAgreementChargesOutputTypeDef]
else:
    _ListAgreementChargesPaginatorBase = Paginator  # type: ignore[assignment]


class ListAgreementChargesPaginator(_ListAgreementChargesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCharges.html#AgreementService.Paginator.ListAgreementCharges)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementchargespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementChargesInputPaginateTypeDef]
    ) -> PageIterator[ListAgreementChargesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementCharges.html#AgreementService.Paginator.ListAgreementCharges.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementchargespaginator)
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
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementinvoicelineitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementInvoiceLineItemsInputPaginateTypeDef]
    ) -> PageIterator[ListAgreementInvoiceLineItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementInvoiceLineItems.html#AgreementService.Paginator.ListAgreementInvoiceLineItems.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementinvoicelineitemspaginator)
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
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementpaymentrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementPaymentRequestsInputPaginateTypeDef]
    ) -> PageIterator[ListAgreementPaymentRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementPaymentRequests.html#AgreementService.Paginator.ListAgreementPaymentRequests.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementpaymentrequestspaginator)
        """


if TYPE_CHECKING:
    _ListAgreementRequestsPaginatorBase = Paginator[ListAgreementRequestsOutputTypeDef]
else:
    _ListAgreementRequestsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAgreementRequestsPaginator(_ListAgreementRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementRequests.html#AgreementService.Paginator.ListAgreementRequests)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgreementRequestsInputPaginateTypeDef]
    ) -> PageIterator[ListAgreementRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListAgreementRequests.html#AgreementService.Paginator.ListAgreementRequests.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listagreementrequestspaginator)
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
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listbillingadjustmentrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingAdjustmentRequestsInputPaginateTypeDef]
    ) -> PageIterator[ListBillingAdjustmentRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/ListBillingAdjustmentRequests.html#AgreementService.Paginator.ListBillingAdjustmentRequests.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#listbillingadjustmentrequestspaginator)
        """


if TYPE_CHECKING:
    _SearchAgreementsPaginatorBase = Paginator[SearchAgreementsOutputTypeDef]
else:
    _SearchAgreementsPaginatorBase = Paginator  # type: ignore[assignment]


class SearchAgreementsPaginator(_SearchAgreementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/SearchAgreements.html#AgreementService.Paginator.SearchAgreements)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#searchagreementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchAgreementsInputPaginateTypeDef]
    ) -> PageIterator[SearchAgreementsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement/paginator/SearchAgreements.html#AgreementService.Paginator.SearchAgreements.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/paginators/#searchagreementspaginator)
        """
