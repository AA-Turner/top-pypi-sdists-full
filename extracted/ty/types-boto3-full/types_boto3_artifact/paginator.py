"""
Type annotations for artifact service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_artifact.client import ArtifactClient
    from types_boto3_artifact.paginator import (
        ListComplianceInquiriesPaginator,
        ListComplianceInquiryQueriesPaginator,
        ListCustomerAgreementsPaginator,
        ListReportVersionsPaginator,
        ListReportsPaginator,
    )

    session = Session()
    client: ArtifactClient = session.client("artifact")

    list_compliance_inquiries_paginator: ListComplianceInquiriesPaginator = client.get_paginator("list_compliance_inquiries")
    list_compliance_inquiry_queries_paginator: ListComplianceInquiryQueriesPaginator = client.get_paginator("list_compliance_inquiry_queries")
    list_customer_agreements_paginator: ListCustomerAgreementsPaginator = client.get_paginator("list_customer_agreements")
    list_report_versions_paginator: ListReportVersionsPaginator = client.get_paginator("list_report_versions")
    list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListComplianceInquiriesRequestPaginateTypeDef,
    ListComplianceInquiriesResponseTypeDef,
    ListComplianceInquiryQueriesRequestPaginateTypeDef,
    ListComplianceInquiryQueriesResponseTypeDef,
    ListCustomerAgreementsRequestPaginateTypeDef,
    ListCustomerAgreementsResponseTypeDef,
    ListReportsRequestPaginateTypeDef,
    ListReportsResponseTypeDef,
    ListReportVersionsRequestPaginateTypeDef,
    ListReportVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListComplianceInquiriesPaginator",
    "ListComplianceInquiryQueriesPaginator",
    "ListCustomerAgreementsPaginator",
    "ListReportVersionsPaginator",
    "ListReportsPaginator",
)


if TYPE_CHECKING:
    _ListComplianceInquiriesPaginatorBase = Paginator[ListComplianceInquiriesResponseTypeDef]
else:
    _ListComplianceInquiriesPaginatorBase = Paginator  # type: ignore[assignment]


class ListComplianceInquiriesPaginator(_ListComplianceInquiriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListComplianceInquiries.html#Artifact.Paginator.ListComplianceInquiries)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listcomplianceinquiriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComplianceInquiriesRequestPaginateTypeDef]
    ) -> PageIterator[ListComplianceInquiriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListComplianceInquiries.html#Artifact.Paginator.ListComplianceInquiries.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listcomplianceinquiriespaginator)
        """


if TYPE_CHECKING:
    _ListComplianceInquiryQueriesPaginatorBase = Paginator[
        ListComplianceInquiryQueriesResponseTypeDef
    ]
else:
    _ListComplianceInquiryQueriesPaginatorBase = Paginator  # type: ignore[assignment]


class ListComplianceInquiryQueriesPaginator(_ListComplianceInquiryQueriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListComplianceInquiryQueries.html#Artifact.Paginator.ListComplianceInquiryQueries)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listcomplianceinquiryqueriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComplianceInquiryQueriesRequestPaginateTypeDef]
    ) -> PageIterator[ListComplianceInquiryQueriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListComplianceInquiryQueries.html#Artifact.Paginator.ListComplianceInquiryQueries.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listcomplianceinquiryqueriespaginator)
        """


if TYPE_CHECKING:
    _ListCustomerAgreementsPaginatorBase = Paginator[ListCustomerAgreementsResponseTypeDef]
else:
    _ListCustomerAgreementsPaginatorBase = Paginator  # type: ignore[assignment]


class ListCustomerAgreementsPaginator(_ListCustomerAgreementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListCustomerAgreements.html#Artifact.Paginator.ListCustomerAgreements)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listcustomeragreementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomerAgreementsRequestPaginateTypeDef]
    ) -> PageIterator[ListCustomerAgreementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListCustomerAgreements.html#Artifact.Paginator.ListCustomerAgreements.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listcustomeragreementspaginator)
        """


if TYPE_CHECKING:
    _ListReportVersionsPaginatorBase = Paginator[ListReportVersionsResponseTypeDef]
else:
    _ListReportVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListReportVersionsPaginator(_ListReportVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReportVersions.html#Artifact.Paginator.ListReportVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listreportversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListReportVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReportVersions.html#Artifact.Paginator.ListReportVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listreportversionspaginator)
        """


if TYPE_CHECKING:
    _ListReportsPaginatorBase = Paginator[ListReportsResponseTypeDef]
else:
    _ListReportsPaginatorBase = Paginator  # type: ignore[assignment]


class ListReportsPaginator(_ListReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReports.html#Artifact.Paginator.ListReports)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listreportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportsRequestPaginateTypeDef]
    ) -> PageIterator[ListReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReports.html#Artifact.Paginator.ListReports.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_artifact/paginators/#listreportspaginator)
        """
