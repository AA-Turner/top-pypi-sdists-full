"""
Type annotations for importexport service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_importexport.client import ImportExportClient
    from types_aiobotocore_importexport.paginator import (
        ListJobsPaginator,
    )

    session = get_session()
    with session.create_client("importexport") as client:
        client: ImportExportClient

        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListJobsInputPaginateTypeDef, ListJobsOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListJobsPaginator",)

if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsOutputTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/paginator/ListJobs.html#ImportExport.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/paginators/#listjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/paginator/ListJobs.html#ImportExport.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/paginators/#listjobspaginator)
        """
