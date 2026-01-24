"""
Type annotations for artifact service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_artifact.client import ArtifactClient
    from types_aiobotocore_artifact.paginator import (
        ListCustomerAgreementsPaginator,
        ListReportVersionsPaginator,
        ListReportsPaginator,
    )

    session = get_session()
    with session.create_client("artifact") as client:
        client: ArtifactClient

        list_customer_agreements_paginator: ListCustomerAgreementsPaginator = client.get_paginator("list_customer_agreements")
        list_report_versions_paginator: ListReportVersionsPaginator = client.get_paginator("list_report_versions")
        list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
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

__all__ = ("ListCustomerAgreementsPaginator", "ListReportVersionsPaginator", "ListReportsPaginator")

if TYPE_CHECKING:
    _ListCustomerAgreementsPaginatorBase = AioPaginator[ListCustomerAgreementsResponseTypeDef]
else:
    _ListCustomerAgreementsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCustomerAgreementsPaginator(_ListCustomerAgreementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListCustomerAgreements.html#Artifact.Paginator.ListCustomerAgreements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listcustomeragreementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomerAgreementsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomerAgreementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListCustomerAgreements.html#Artifact.Paginator.ListCustomerAgreements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listcustomeragreementspaginator)
        """

if TYPE_CHECKING:
    _ListReportVersionsPaginatorBase = AioPaginator[ListReportVersionsResponseTypeDef]
else:
    _ListReportVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReportVersionsPaginator(_ListReportVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReportVersions.html#Artifact.Paginator.ListReportVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listreportversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReportVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReportVersions.html#Artifact.Paginator.ListReportVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listreportversionspaginator)
        """

if TYPE_CHECKING:
    _ListReportsPaginatorBase = AioPaginator[ListReportsResponseTypeDef]
else:
    _ListReportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReportsPaginator(_ListReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReports.html#Artifact.Paginator.ListReports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listreportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReports.html#Artifact.Paginator.ListReports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listreportspaginator)
        """
