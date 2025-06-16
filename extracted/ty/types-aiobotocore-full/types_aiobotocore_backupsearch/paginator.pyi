"""
Type annotations for backupsearch service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_backupsearch.client import BackupSearchClient
    from types_aiobotocore_backupsearch.paginator import (
        ListSearchJobBackupsPaginator,
        ListSearchJobResultsPaginator,
        ListSearchJobsPaginator,
        ListSearchResultExportJobsPaginator,
    )

    session = get_session()
    with session.create_client("backupsearch") as client:
        client: BackupSearchClient

        list_search_job_backups_paginator: ListSearchJobBackupsPaginator = client.get_paginator("list_search_job_backups")
        list_search_job_results_paginator: ListSearchJobResultsPaginator = client.get_paginator("list_search_job_results")
        list_search_jobs_paginator: ListSearchJobsPaginator = client.get_paginator("list_search_jobs")
        list_search_result_export_jobs_paginator: ListSearchResultExportJobsPaginator = client.get_paginator("list_search_result_export_jobs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListSearchJobBackupsInputPaginateTypeDef,
    ListSearchJobBackupsOutputTypeDef,
    ListSearchJobResultsInputPaginateTypeDef,
    ListSearchJobResultsOutputTypeDef,
    ListSearchJobsInputPaginateTypeDef,
    ListSearchJobsOutputTypeDef,
    ListSearchResultExportJobsInputPaginateTypeDef,
    ListSearchResultExportJobsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListSearchJobBackupsPaginator",
    "ListSearchJobResultsPaginator",
    "ListSearchJobsPaginator",
    "ListSearchResultExportJobsPaginator",
)

if TYPE_CHECKING:
    _ListSearchJobBackupsPaginatorBase = AioPaginator[ListSearchJobBackupsOutputTypeDef]
else:
    _ListSearchJobBackupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSearchJobBackupsPaginator(_ListSearchJobBackupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobBackups.html#BackupSearch.Paginator.ListSearchJobBackups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/paginators/#listsearchjobbackupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSearchJobBackupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSearchJobBackupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobBackups.html#BackupSearch.Paginator.ListSearchJobBackups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/paginators/#listsearchjobbackupspaginator)
        """

if TYPE_CHECKING:
    _ListSearchJobResultsPaginatorBase = AioPaginator[ListSearchJobResultsOutputTypeDef]
else:
    _ListSearchJobResultsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSearchJobResultsPaginator(_ListSearchJobResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobResults.html#BackupSearch.Paginator.ListSearchJobResults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/paginators/#listsearchjobresultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSearchJobResultsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSearchJobResultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobResults.html#BackupSearch.Paginator.ListSearchJobResults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/paginators/#listsearchjobresultspaginator)
        """

if TYPE_CHECKING:
    _ListSearchJobsPaginatorBase = AioPaginator[ListSearchJobsOutputTypeDef]
else:
    _ListSearchJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSearchJobsPaginator(_ListSearchJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobs.html#BackupSearch.Paginator.ListSearchJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/paginators/#listsearchjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSearchJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSearchJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobs.html#BackupSearch.Paginator.ListSearchJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/paginators/#listsearchjobspaginator)
        """

if TYPE_CHECKING:
    _ListSearchResultExportJobsPaginatorBase = AioPaginator[ListSearchResultExportJobsOutputTypeDef]
else:
    _ListSearchResultExportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSearchResultExportJobsPaginator(_ListSearchResultExportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchResultExportJobs.html#BackupSearch.Paginator.ListSearchResultExportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/paginators/#listsearchresultexportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSearchResultExportJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSearchResultExportJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchResultExportJobs.html#BackupSearch.Paginator.ListSearchResultExportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupsearch/paginators/#listsearchresultexportjobspaginator)
        """
