"""
Type annotations for codeguru-security service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codeguru_security.client import CodeGuruSecurityClient
    from types_aiobotocore_codeguru_security.paginator import (
        GetFindingsPaginator,
        ListFindingsMetricsPaginator,
        ListScansPaginator,
    )

    session = get_session()
    with session.create_client("codeguru-security") as client:
        client: CodeGuruSecurityClient

        get_findings_paginator: GetFindingsPaginator = client.get_paginator("get_findings")
        list_findings_metrics_paginator: ListFindingsMetricsPaginator = client.get_paginator("list_findings_metrics")
        list_scans_paginator: ListScansPaginator = client.get_paginator("list_scans")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetFindingsRequestPaginateTypeDef,
    GetFindingsResponseTypeDef,
    ListFindingsMetricsRequestPaginateTypeDef,
    ListFindingsMetricsResponseTypeDef,
    ListScansRequestPaginateTypeDef,
    ListScansResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("GetFindingsPaginator", "ListFindingsMetricsPaginator", "ListScansPaginator")


if TYPE_CHECKING:
    _GetFindingsPaginatorBase = AioPaginator[GetFindingsResponseTypeDef]
else:
    _GetFindingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetFindingsPaginator(_GetFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/GetFindings.html#CodeGuruSecurity.Paginator.GetFindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#getfindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetFindingsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/GetFindings.html#CodeGuruSecurity.Paginator.GetFindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#getfindingspaginator)
        """


if TYPE_CHECKING:
    _ListFindingsMetricsPaginatorBase = AioPaginator[ListFindingsMetricsResponseTypeDef]
else:
    _ListFindingsMetricsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFindingsMetricsPaginator(_ListFindingsMetricsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListFindingsMetrics.html#CodeGuruSecurity.Paginator.ListFindingsMetrics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#listfindingsmetricspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingsMetricsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFindingsMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListFindingsMetrics.html#CodeGuruSecurity.Paginator.ListFindingsMetrics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#listfindingsmetricspaginator)
        """


if TYPE_CHECKING:
    _ListScansPaginatorBase = AioPaginator[ListScansResponseTypeDef]
else:
    _ListScansPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListScansPaginator(_ListScansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListScans.html#CodeGuruSecurity.Paginator.ListScans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#listscanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScansRequestPaginateTypeDef]
    ) -> AioPageIterator[ListScansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/paginator/ListScans.html#CodeGuruSecurity.Paginator.ListScans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/paginators/#listscanspaginator)
        """
