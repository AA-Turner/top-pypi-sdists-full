"""
Main interface for pi service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pi import (
        Client,
        ListPerformanceAnalysisReportRecommendationsPaginator,
        PIClient,
    )

    session = get_session()
    async with session.create_client("pi") as client:
        client: PIClient
        ...


    list_performance_analysis_report_recommendations_paginator: ListPerformanceAnalysisReportRecommendationsPaginator = client.get_paginator("list_performance_analysis_report_recommendations")
    ```
"""

from .client import PIClient
from .paginator import ListPerformanceAnalysisReportRecommendationsPaginator

Client = PIClient

__all__ = ("Client", "ListPerformanceAnalysisReportRecommendationsPaginator", "PIClient")
