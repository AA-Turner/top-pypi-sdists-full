"""
Main interface for cur service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cur import (
        Client,
        CostandUsageReportServiceClient,
        DescribeReportDefinitionsPaginator,
    )

    session = Session()
    client: CostandUsageReportServiceClient = session.client("cur")

    describe_report_definitions_paginator: DescribeReportDefinitionsPaginator = client.get_paginator("describe_report_definitions")
    ```
"""

from .client import CostandUsageReportServiceClient
from .paginator import DescribeReportDefinitionsPaginator

Client = CostandUsageReportServiceClient


__all__ = ("Client", "CostandUsageReportServiceClient", "DescribeReportDefinitionsPaginator")
