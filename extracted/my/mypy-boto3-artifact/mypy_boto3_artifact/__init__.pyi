"""
Main interface for artifact service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_artifact import (
        ArtifactClient,
        Client,
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

from .client import ArtifactClient
from .paginator import (
    ListComplianceInquiriesPaginator,
    ListComplianceInquiryQueriesPaginator,
    ListCustomerAgreementsPaginator,
    ListReportsPaginator,
    ListReportVersionsPaginator,
)

Client = ArtifactClient

__all__ = (
    "ArtifactClient",
    "Client",
    "ListComplianceInquiriesPaginator",
    "ListComplianceInquiryQueriesPaginator",
    "ListCustomerAgreementsPaginator",
    "ListReportVersionsPaginator",
    "ListReportsPaginator",
)
