"""
Type annotations for evidently service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_evidently.client import CloudWatchEvidentlyClient
    from types_aiobotocore_evidently.paginator import (
        ListExperimentsPaginator,
        ListFeaturesPaginator,
        ListLaunchesPaginator,
        ListProjectsPaginator,
        ListSegmentReferencesPaginator,
        ListSegmentsPaginator,
    )

    session = get_session()
    with session.create_client("evidently") as client:
        client: CloudWatchEvidentlyClient

        list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
        list_features_paginator: ListFeaturesPaginator = client.get_paginator("list_features")
        list_launches_paginator: ListLaunchesPaginator = client.get_paginator("list_launches")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_segment_references_paginator: ListSegmentReferencesPaginator = client.get_paginator("list_segment_references")
        list_segments_paginator: ListSegmentsPaginator = client.get_paginator("list_segments")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListExperimentsRequestPaginateTypeDef,
    ListExperimentsResponseTypeDef,
    ListFeaturesRequestPaginateTypeDef,
    ListFeaturesResponseTypeDef,
    ListLaunchesRequestPaginateTypeDef,
    ListLaunchesResponseTypeDef,
    ListProjectsRequestPaginateTypeDef,
    ListProjectsResponseTypeDef,
    ListSegmentReferencesRequestPaginateTypeDef,
    ListSegmentReferencesResponseTypeDef,
    ListSegmentsRequestPaginateTypeDef,
    ListSegmentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListExperimentsPaginator",
    "ListFeaturesPaginator",
    "ListLaunchesPaginator",
    "ListProjectsPaginator",
    "ListSegmentReferencesPaginator",
    "ListSegmentsPaginator",
)

if TYPE_CHECKING:
    _ListExperimentsPaginatorBase = AioPaginator[ListExperimentsResponseTypeDef]
else:
    _ListExperimentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListExperimentsPaginator(_ListExperimentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListExperiments.html#CloudWatchEvidently.Paginator.ListExperiments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listexperimentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExperimentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListExperiments.html#CloudWatchEvidently.Paginator.ListExperiments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listexperimentspaginator)
        """

if TYPE_CHECKING:
    _ListFeaturesPaginatorBase = AioPaginator[ListFeaturesResponseTypeDef]
else:
    _ListFeaturesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFeaturesPaginator(_ListFeaturesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListFeatures.html#CloudWatchEvidently.Paginator.ListFeatures)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listfeaturespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFeaturesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFeaturesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListFeatures.html#CloudWatchEvidently.Paginator.ListFeatures.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listfeaturespaginator)
        """

if TYPE_CHECKING:
    _ListLaunchesPaginatorBase = AioPaginator[ListLaunchesResponseTypeDef]
else:
    _ListLaunchesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLaunchesPaginator(_ListLaunchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListLaunches.html#CloudWatchEvidently.Paginator.ListLaunches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listlaunchespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLaunchesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLaunchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListLaunches.html#CloudWatchEvidently.Paginator.ListLaunches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listlaunchespaginator)
        """

if TYPE_CHECKING:
    _ListProjectsPaginatorBase = AioPaginator[ListProjectsResponseTypeDef]
else:
    _ListProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProjectsPaginator(_ListProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListProjects.html#CloudWatchEvidently.Paginator.ListProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listprojectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListProjects.html#CloudWatchEvidently.Paginator.ListProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listprojectspaginator)
        """

if TYPE_CHECKING:
    _ListSegmentReferencesPaginatorBase = AioPaginator[ListSegmentReferencesResponseTypeDef]
else:
    _ListSegmentReferencesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSegmentReferencesPaginator(_ListSegmentReferencesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListSegmentReferences.html#CloudWatchEvidently.Paginator.ListSegmentReferences)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listsegmentreferencespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSegmentReferencesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSegmentReferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListSegmentReferences.html#CloudWatchEvidently.Paginator.ListSegmentReferences.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listsegmentreferencespaginator)
        """

if TYPE_CHECKING:
    _ListSegmentsPaginatorBase = AioPaginator[ListSegmentsResponseTypeDef]
else:
    _ListSegmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSegmentsPaginator(_ListSegmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListSegments.html#CloudWatchEvidently.Paginator.ListSegments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listsegmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSegmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSegmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListSegments.html#CloudWatchEvidently.Paginator.ListSegments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listsegmentspaginator)
        """
