"""
Main interface for pi service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pi/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_pi import (
        Client,
        ListPerformanceAnalysisReportRecommendationsPaginator,
        PIClient,
    )

    session = Session()
    client: PIClient = session.client("pi")

    list_performance_analysis_report_recommendations_paginator: ListPerformanceAnalysisReportRecommendationsPaginator = client.get_paginator("list_performance_analysis_report_recommendations")
    ```
"""

from .client import PIClient
from .paginator import ListPerformanceAnalysisReportRecommendationsPaginator

Client = PIClient


__all__ = ("Client", "ListPerformanceAnalysisReportRecommendationsPaginator", "PIClient")
