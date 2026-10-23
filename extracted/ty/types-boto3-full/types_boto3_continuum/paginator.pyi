"""
Type annotations for continuum service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_continuum.client import ContinuumClient
    from types_boto3_continuum.paginator import (
        ListAssociatedCollectorsPaginator,
        ListAssociatedEnvironmentsPaginator,
        ListCodeFindingsPaginator,
        ListCodeIssueArtifactsPaginator,
        ListCodeIssuesPaginator,
        ListCodeScansPaginator,
        ListEnvironmentsPaginator,
        ListIntegrationsPaginator,
    )

    session = Session()
    client: ContinuumClient = session.client("continuum")

    list_associated_collectors_paginator: ListAssociatedCollectorsPaginator = client.get_paginator("list_associated_collectors")
    list_associated_environments_paginator: ListAssociatedEnvironmentsPaginator = client.get_paginator("list_associated_environments")
    list_code_findings_paginator: ListCodeFindingsPaginator = client.get_paginator("list_code_findings")
    list_code_issue_artifacts_paginator: ListCodeIssueArtifactsPaginator = client.get_paginator("list_code_issue_artifacts")
    list_code_issues_paginator: ListCodeIssuesPaginator = client.get_paginator("list_code_issues")
    list_code_scans_paginator: ListCodeScansPaginator = client.get_paginator("list_code_scans")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    list_integrations_paginator: ListIntegrationsPaginator = client.get_paginator("list_integrations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAssociatedCollectorsInputPaginateTypeDef,
    ListAssociatedCollectorsOutputTypeDef,
    ListAssociatedEnvironmentsInputPaginateTypeDef,
    ListAssociatedEnvironmentsOutputTypeDef,
    ListCodeFindingsInputPaginateTypeDef,
    ListCodeFindingsOutputTypeDef,
    ListCodeIssueArtifactsInputPaginateTypeDef,
    ListCodeIssueArtifactsOutputTypeDef,
    ListCodeIssuesInputPaginateTypeDef,
    ListCodeIssuesOutputTypeDef,
    ListCodeScansInputPaginateTypeDef,
    ListCodeScansOutputTypeDef,
    ListEnvironmentsInputPaginateTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListIntegrationsInputPaginateTypeDef,
    ListIntegrationsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssociatedCollectorsPaginator",
    "ListAssociatedEnvironmentsPaginator",
    "ListCodeFindingsPaginator",
    "ListCodeIssueArtifactsPaginator",
    "ListCodeIssuesPaginator",
    "ListCodeScansPaginator",
    "ListEnvironmentsPaginator",
    "ListIntegrationsPaginator",
)

if TYPE_CHECKING:
    _ListAssociatedCollectorsPaginatorBase = Paginator[ListAssociatedCollectorsOutputTypeDef]
else:
    _ListAssociatedCollectorsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssociatedCollectorsPaginator(_ListAssociatedCollectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListAssociatedCollectors.html#Continuum.Paginator.ListAssociatedCollectors)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listassociatedcollectorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociatedCollectorsInputPaginateTypeDef]
    ) -> PageIterator[ListAssociatedCollectorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListAssociatedCollectors.html#Continuum.Paginator.ListAssociatedCollectors.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listassociatedcollectorspaginator)
        """

if TYPE_CHECKING:
    _ListAssociatedEnvironmentsPaginatorBase = Paginator[ListAssociatedEnvironmentsOutputTypeDef]
else:
    _ListAssociatedEnvironmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssociatedEnvironmentsPaginator(_ListAssociatedEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListAssociatedEnvironments.html#Continuum.Paginator.ListAssociatedEnvironments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listassociatedenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociatedEnvironmentsInputPaginateTypeDef]
    ) -> PageIterator[ListAssociatedEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListAssociatedEnvironments.html#Continuum.Paginator.ListAssociatedEnvironments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listassociatedenvironmentspaginator)
        """

if TYPE_CHECKING:
    _ListCodeFindingsPaginatorBase = Paginator[ListCodeFindingsOutputTypeDef]
else:
    _ListCodeFindingsPaginatorBase = Paginator  # type: ignore[assignment]

class ListCodeFindingsPaginator(_ListCodeFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListCodeFindings.html#Continuum.Paginator.ListCodeFindings)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listcodefindingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeFindingsInputPaginateTypeDef]
    ) -> PageIterator[ListCodeFindingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListCodeFindings.html#Continuum.Paginator.ListCodeFindings.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listcodefindingspaginator)
        """

if TYPE_CHECKING:
    _ListCodeIssueArtifactsPaginatorBase = Paginator[ListCodeIssueArtifactsOutputTypeDef]
else:
    _ListCodeIssueArtifactsPaginatorBase = Paginator  # type: ignore[assignment]

class ListCodeIssueArtifactsPaginator(_ListCodeIssueArtifactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListCodeIssueArtifacts.html#Continuum.Paginator.ListCodeIssueArtifacts)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listcodeissueartifactspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeIssueArtifactsInputPaginateTypeDef]
    ) -> PageIterator[ListCodeIssueArtifactsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListCodeIssueArtifacts.html#Continuum.Paginator.ListCodeIssueArtifacts.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listcodeissueartifactspaginator)
        """

if TYPE_CHECKING:
    _ListCodeIssuesPaginatorBase = Paginator[ListCodeIssuesOutputTypeDef]
else:
    _ListCodeIssuesPaginatorBase = Paginator  # type: ignore[assignment]

class ListCodeIssuesPaginator(_ListCodeIssuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListCodeIssues.html#Continuum.Paginator.ListCodeIssues)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listcodeissuespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeIssuesInputPaginateTypeDef]
    ) -> PageIterator[ListCodeIssuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListCodeIssues.html#Continuum.Paginator.ListCodeIssues.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listcodeissuespaginator)
        """

if TYPE_CHECKING:
    _ListCodeScansPaginatorBase = Paginator[ListCodeScansOutputTypeDef]
else:
    _ListCodeScansPaginatorBase = Paginator  # type: ignore[assignment]

class ListCodeScansPaginator(_ListCodeScansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListCodeScans.html#Continuum.Paginator.ListCodeScans)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listcodescanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeScansInputPaginateTypeDef]
    ) -> PageIterator[ListCodeScansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListCodeScans.html#Continuum.Paginator.ListCodeScans.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listcodescanspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = Paginator[ListEnvironmentsOutputTypeDef]
else:
    _ListEnvironmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListEnvironments.html#Continuum.Paginator.ListEnvironments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsInputPaginateTypeDef]
    ) -> PageIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListEnvironments.html#Continuum.Paginator.ListEnvironments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listenvironmentspaginator)
        """

if TYPE_CHECKING:
    _ListIntegrationsPaginatorBase = Paginator[ListIntegrationsOutputTypeDef]
else:
    _ListIntegrationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListIntegrationsPaginator(_ListIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListIntegrations.html#Continuum.Paginator.ListIntegrations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listintegrationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegrationsInputPaginateTypeDef]
    ) -> PageIterator[ListIntegrationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/paginator/ListIntegrations.html#Continuum.Paginator.ListIntegrations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/paginators/#listintegrationspaginator)
        """
