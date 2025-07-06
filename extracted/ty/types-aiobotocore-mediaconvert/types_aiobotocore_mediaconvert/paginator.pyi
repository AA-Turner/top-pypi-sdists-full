"""
Type annotations for mediaconvert service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediaconvert.client import MediaConvertClient
    from types_aiobotocore_mediaconvert.paginator import (
        DescribeEndpointsPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListPresetsPaginator,
        ListQueuesPaginator,
        ListVersionsPaginator,
        SearchJobsPaginator,
    )

    session = get_session()
    with session.create_client("mediaconvert") as client:
        client: MediaConvertClient

        describe_endpoints_paginator: DescribeEndpointsPaginator = client.get_paginator("describe_endpoints")
        list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_presets_paginator: ListPresetsPaginator = client.get_paginator("list_presets")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
        list_versions_paginator: ListVersionsPaginator = client.get_paginator("list_versions")
        search_jobs_paginator: SearchJobsPaginator = client.get_paginator("search_jobs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeEndpointsRequestPaginateTypeDef,
    DescribeEndpointsResponseTypeDef,
    ListJobsRequestPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesRequestPaginateTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListPresetsRequestPaginateTypeDef,
    ListPresetsResponseTypeDef,
    ListQueuesRequestPaginateTypeDef,
    ListQueuesResponseTypeDef,
    ListVersionsRequestPaginateTypeDef,
    ListVersionsResponseTypeDef,
    SearchJobsRequestPaginateTypeDef,
    SearchJobsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeEndpointsPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListPresetsPaginator",
    "ListQueuesPaginator",
    "ListVersionsPaginator",
    "SearchJobsPaginator",
)

if TYPE_CHECKING:
    _DescribeEndpointsPaginatorBase = AioPaginator[DescribeEndpointsResponseTypeDef]
else:
    _DescribeEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEndpointsPaginator(_DescribeEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/DescribeEndpoints.html#MediaConvert.Paginator.DescribeEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#describeendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/DescribeEndpoints.html#MediaConvert.Paginator.DescribeEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#describeendpointspaginator)
        """

if TYPE_CHECKING:
    _ListJobTemplatesPaginatorBase = AioPaginator[ListJobTemplatesResponseTypeDef]
else:
    _ListJobTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobTemplatesPaginator(_ListJobTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListJobTemplates.html#MediaConvert.Paginator.ListJobTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobtemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListJobTemplates.html#MediaConvert.Paginator.ListJobTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobtemplatespaginator)
        """

if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsResponseTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListJobs.html#MediaConvert.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListJobs.html#MediaConvert.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobspaginator)
        """

if TYPE_CHECKING:
    _ListPresetsPaginatorBase = AioPaginator[ListPresetsResponseTypeDef]
else:
    _ListPresetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPresetsPaginator(_ListPresetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListPresets.html#MediaConvert.Paginator.ListPresets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listpresetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPresetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPresetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListPresets.html#MediaConvert.Paginator.ListPresets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listpresetspaginator)
        """

if TYPE_CHECKING:
    _ListQueuesPaginatorBase = AioPaginator[ListQueuesResponseTypeDef]
else:
    _ListQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListQueuesPaginator(_ListQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListQueues.html#MediaConvert.Paginator.ListQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listqueuespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueuesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListQueues.html#MediaConvert.Paginator.ListQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listqueuespaginator)
        """

if TYPE_CHECKING:
    _ListVersionsPaginatorBase = AioPaginator[ListVersionsResponseTypeDef]
else:
    _ListVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVersionsPaginator(_ListVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListVersions.html#MediaConvert.Paginator.ListVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/ListVersions.html#MediaConvert.Paginator.ListVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listversionspaginator)
        """

if TYPE_CHECKING:
    _SearchJobsPaginatorBase = AioPaginator[SearchJobsResponseTypeDef]
else:
    _SearchJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchJobsPaginator(_SearchJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/SearchJobs.html#MediaConvert.Paginator.SearchJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#searchjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert/paginator/SearchJobs.html#MediaConvert.Paginator.SearchJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#searchjobspaginator)
        """
