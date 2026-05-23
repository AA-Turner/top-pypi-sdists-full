"""
Type annotations for pi service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_pi.client import PIClient
    from mypy_boto3_pi.paginator import (
        ListPerformanceAnalysisReportRecommendationsPaginator,
    )

    session = Session()
    client: PIClient = session.client("pi")

    list_performance_analysis_report_recommendations_paginator: ListPerformanceAnalysisReportRecommendationsPaginator = client.get_paginator("list_performance_analysis_report_recommendations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListPerformanceAnalysisReportRecommendationsRequestPaginateTypeDef,
    ListPerformanceAnalysisReportRecommendationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListPerformanceAnalysisReportRecommendationsPaginator",)


if TYPE_CHECKING:
    _ListPerformanceAnalysisReportRecommendationsPaginatorBase = Paginator[
        ListPerformanceAnalysisReportRecommendationsResponseTypeDef
    ]
else:
    _ListPerformanceAnalysisReportRecommendationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPerformanceAnalysisReportRecommendationsPaginator(
    _ListPerformanceAnalysisReportRecommendationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi/paginator/ListPerformanceAnalysisReportRecommendations.html#PI.Paginator.ListPerformanceAnalysisReportRecommendations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/paginators/#listperformanceanalysisreportrecommendationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPerformanceAnalysisReportRecommendationsRequestPaginateTypeDef]
    ) -> PageIterator[ListPerformanceAnalysisReportRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi/paginator/ListPerformanceAnalysisReportRecommendations.html#PI.Paginator.ListPerformanceAnalysisReportRecommendations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/paginators/#listperformanceanalysisreportrecommendationspaginator)
        """
