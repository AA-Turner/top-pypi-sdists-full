"""
Main interface for migrationhubstrategy service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_migrationhubstrategy import (
        Client,
        GetServerDetailsPaginator,
        ListAnalyzableServersPaginator,
        ListApplicationComponentsPaginator,
        ListCollectorsPaginator,
        ListImportFileTaskPaginator,
        ListServersPaginator,
        MigrationHubStrategyRecommendationsClient,
    )

    session = get_session()
    async with session.create_client("migrationhubstrategy") as client:
        client: MigrationHubStrategyRecommendationsClient
        ...


    get_server_details_paginator: GetServerDetailsPaginator = client.get_paginator("get_server_details")
    list_analyzable_servers_paginator: ListAnalyzableServersPaginator = client.get_paginator("list_analyzable_servers")
    list_application_components_paginator: ListApplicationComponentsPaginator = client.get_paginator("list_application_components")
    list_collectors_paginator: ListCollectorsPaginator = client.get_paginator("list_collectors")
    list_import_file_task_paginator: ListImportFileTaskPaginator = client.get_paginator("list_import_file_task")
    list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
    ```
"""

from .client import MigrationHubStrategyRecommendationsClient
from .paginator import (
    GetServerDetailsPaginator,
    ListAnalyzableServersPaginator,
    ListApplicationComponentsPaginator,
    ListCollectorsPaginator,
    ListImportFileTaskPaginator,
    ListServersPaginator,
)

Client = MigrationHubStrategyRecommendationsClient

__all__ = (
    "Client",
    "GetServerDetailsPaginator",
    "ListAnalyzableServersPaginator",
    "ListApplicationComponentsPaginator",
    "ListCollectorsPaginator",
    "ListImportFileTaskPaginator",
    "ListServersPaginator",
    "MigrationHubStrategyRecommendationsClient",
)
