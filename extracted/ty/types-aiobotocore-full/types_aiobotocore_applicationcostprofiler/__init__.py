"""
Main interface for applicationcostprofiler service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_applicationcostprofiler/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_applicationcostprofiler import (
        ApplicationCostProfilerClient,
        Client,
        ListReportDefinitionsPaginator,
    )

    session = get_session()
    async with session.create_client("applicationcostprofiler") as client:
        client: ApplicationCostProfilerClient
        ...


    list_report_definitions_paginator: ListReportDefinitionsPaginator = client.get_paginator("list_report_definitions")
    ```
"""

from .client import ApplicationCostProfilerClient
from .paginator import ListReportDefinitionsPaginator

Client = ApplicationCostProfilerClient


__all__ = ("ApplicationCostProfilerClient", "Client", "ListReportDefinitionsPaginator")
