"""
Type annotations for lookoutvision service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lookoutvision.client import LookoutforVisionClient
    from types_aiobotocore_lookoutvision.paginator import (
        ListDatasetEntriesPaginator,
        ListModelPackagingJobsPaginator,
        ListModelsPaginator,
        ListProjectsPaginator,
    )

    session = get_session()
    with session.create_client("lookoutvision") as client:
        client: LookoutforVisionClient

        list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
        list_model_packaging_jobs_paginator: ListModelPackagingJobsPaginator = client.get_paginator("list_model_packaging_jobs")
        list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDatasetEntriesRequestPaginateTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListModelPackagingJobsRequestPaginateTypeDef,
    ListModelPackagingJobsResponseTypeDef,
    ListModelsRequestPaginateTypeDef,
    ListModelsResponseTypeDef,
    ListProjectsRequestPaginateTypeDef,
    ListProjectsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDatasetEntriesPaginator",
    "ListModelPackagingJobsPaginator",
    "ListModelsPaginator",
    "ListProjectsPaginator",
)

if TYPE_CHECKING:
    _ListDatasetEntriesPaginatorBase = AioPaginator[ListDatasetEntriesResponseTypeDef]
else:
    _ListDatasetEntriesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDatasetEntriesPaginator(_ListDatasetEntriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListDatasetEntries.html#LookoutforVision.Paginator.ListDatasetEntries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listdatasetentriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetEntriesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListDatasetEntries.html#LookoutforVision.Paginator.ListDatasetEntries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listdatasetentriespaginator)
        """

if TYPE_CHECKING:
    _ListModelPackagingJobsPaginatorBase = AioPaginator[ListModelPackagingJobsResponseTypeDef]
else:
    _ListModelPackagingJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelPackagingJobsPaginator(_ListModelPackagingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModelPackagingJobs.html#LookoutforVision.Paginator.ListModelPackagingJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listmodelpackagingjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelPackagingJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelPackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModelPackagingJobs.html#LookoutforVision.Paginator.ListModelPackagingJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listmodelpackagingjobspaginator)
        """

if TYPE_CHECKING:
    _ListModelsPaginatorBase = AioPaginator[ListModelsResponseTypeDef]
else:
    _ListModelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelsPaginator(_ListModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModels.html#LookoutforVision.Paginator.ListModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listmodelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListModels.html#LookoutforVision.Paginator.ListModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listmodelspaginator)
        """

if TYPE_CHECKING:
    _ListProjectsPaginatorBase = AioPaginator[ListProjectsResponseTypeDef]
else:
    _ListProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProjectsPaginator(_ListProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListProjects.html#LookoutforVision.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listprojectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision/paginator/ListProjects.html#LookoutforVision.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/paginators/#listprojectspaginator)
        """
