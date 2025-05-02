"""
Main interface for cur service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cur/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cur import (
        Client,
        CostandUsageReportServiceClient,
        DescribeReportDefinitionsPaginator,
    )

    session = get_session()
    async with session.create_client("cur") as client:
        client: CostandUsageReportServiceClient
        ...


    describe_report_definitions_paginator: DescribeReportDefinitionsPaginator = client.get_paginator("describe_report_definitions")
    ```
"""

from .client import CostandUsageReportServiceClient
from .paginator import DescribeReportDefinitionsPaginator

Client = CostandUsageReportServiceClient


__all__ = ("Client", "CostandUsageReportServiceClient", "DescribeReportDefinitionsPaginator")
