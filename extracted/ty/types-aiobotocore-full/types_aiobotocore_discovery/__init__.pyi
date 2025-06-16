"""
Main interface for discovery service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_discovery import (
        ApplicationDiscoveryServiceClient,
        Client,
        DescribeAgentsPaginator,
        DescribeContinuousExportsPaginator,
        DescribeExportConfigurationsPaginator,
        DescribeExportTasksPaginator,
        DescribeImportTasksPaginator,
        DescribeTagsPaginator,
        ListConfigurationsPaginator,
    )

    session = get_session()
    async with session.create_client("discovery") as client:
        client: ApplicationDiscoveryServiceClient
        ...


    describe_agents_paginator: DescribeAgentsPaginator = client.get_paginator("describe_agents")
    describe_continuous_exports_paginator: DescribeContinuousExportsPaginator = client.get_paginator("describe_continuous_exports")
    describe_export_configurations_paginator: DescribeExportConfigurationsPaginator = client.get_paginator("describe_export_configurations")
    describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
    describe_import_tasks_paginator: DescribeImportTasksPaginator = client.get_paginator("describe_import_tasks")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    ```
"""

from .client import ApplicationDiscoveryServiceClient
from .paginator import (
    DescribeAgentsPaginator,
    DescribeContinuousExportsPaginator,
    DescribeExportConfigurationsPaginator,
    DescribeExportTasksPaginator,
    DescribeImportTasksPaginator,
    DescribeTagsPaginator,
    ListConfigurationsPaginator,
)

Client = ApplicationDiscoveryServiceClient

__all__ = (
    "ApplicationDiscoveryServiceClient",
    "Client",
    "DescribeAgentsPaginator",
    "DescribeContinuousExportsPaginator",
    "DescribeExportConfigurationsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeImportTasksPaginator",
    "DescribeTagsPaginator",
    "ListConfigurationsPaginator",
)
