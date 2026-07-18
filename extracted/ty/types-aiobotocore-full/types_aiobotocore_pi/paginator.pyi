"""
Type annotations for pi service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pi.client import PIClient
    from types_aiobotocore_pi.paginator import (
        ListPerformanceAnalysisReportRecommendationsPaginator,
    )

    session = get_session()
    with session.create_client("pi") as client:
        client: PIClient

        list_performance_analysis_report_recommendations_paginator: ListPerformanceAnalysisReportRecommendationsPaginator = client.get_paginator("list_performance_analysis_report_recommendations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _ListPerformanceAnalysisReportRecommendationsPaginatorBase = AioPaginator[
        ListPerformanceAnalysisReportRecommendationsResponseTypeDef
    ]
else:
    _ListPerformanceAnalysisReportRecommendationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPerformanceAnalysisReportRecommendationsPaginator(
    _ListPerformanceAnalysisReportRecommendationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi/paginator/ListPerformanceAnalysisReportRecommendations.html#PI.Paginator.ListPerformanceAnalysisReportRecommendations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/paginators/#listperformanceanalysisreportrecommendationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPerformanceAnalysisReportRecommendationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPerformanceAnalysisReportRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi/paginator/ListPerformanceAnalysisReportRecommendations.html#PI.Paginator.ListPerformanceAnalysisReportRecommendations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/paginators/#listperformanceanalysisreportrecommendationspaginator)
        """
