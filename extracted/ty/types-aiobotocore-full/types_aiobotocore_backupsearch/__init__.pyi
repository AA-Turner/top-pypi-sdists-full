"""
Main interface for backupsearch service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_backupsearch import (
        BackupSearchClient,
        Client,
        ListSearchJobBackupsPaginator,
        ListSearchJobResultsPaginator,
        ListSearchJobsPaginator,
        ListSearchResultExportJobsPaginator,
    )

    session = get_session()
    async with session.create_client("backupsearch") as client:
        client: BackupSearchClient
        ...


    list_search_job_backups_paginator: ListSearchJobBackupsPaginator = client.get_paginator("list_search_job_backups")
    list_search_job_results_paginator: ListSearchJobResultsPaginator = client.get_paginator("list_search_job_results")
    list_search_jobs_paginator: ListSearchJobsPaginator = client.get_paginator("list_search_jobs")
    list_search_result_export_jobs_paginator: ListSearchResultExportJobsPaginator = client.get_paginator("list_search_result_export_jobs")
    ```
"""

from .client import BackupSearchClient
from .paginator import (
    ListSearchJobBackupsPaginator,
    ListSearchJobResultsPaginator,
    ListSearchJobsPaginator,
    ListSearchResultExportJobsPaginator,
)

Client = BackupSearchClient

__all__ = (
    "BackupSearchClient",
    "Client",
    "ListSearchJobBackupsPaginator",
    "ListSearchJobResultsPaginator",
    "ListSearchJobsPaginator",
    "ListSearchResultExportJobsPaginator",
)
