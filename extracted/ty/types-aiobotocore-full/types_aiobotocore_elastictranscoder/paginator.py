"""
Type annotations for elastictranscoder service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elastictranscoder.client import ElasticTranscoderClient
    from types_aiobotocore_elastictranscoder.paginator import (
        ListJobsByPipelinePaginator,
        ListJobsByStatusPaginator,
        ListPipelinesPaginator,
        ListPresetsPaginator,
    )

    session = get_session()
    with session.create_client("elastictranscoder") as client:
        client: ElasticTranscoderClient

        list_jobs_by_pipeline_paginator: ListJobsByPipelinePaginator = client.get_paginator("list_jobs_by_pipeline")
        list_jobs_by_status_paginator: ListJobsByStatusPaginator = client.get_paginator("list_jobs_by_status")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        list_presets_paginator: ListPresetsPaginator = client.get_paginator("list_presets")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListJobsByPipelineRequestPaginateTypeDef,
    ListJobsByPipelineResponseTypeDef,
    ListJobsByStatusRequestPaginateTypeDef,
    ListJobsByStatusResponseTypeDef,
    ListPipelinesRequestPaginateTypeDef,
    ListPipelinesResponseTypeDef,
    ListPresetsRequestPaginateTypeDef,
    ListPresetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListJobsByPipelinePaginator",
    "ListJobsByStatusPaginator",
    "ListPipelinesPaginator",
    "ListPresetsPaginator",
)


if TYPE_CHECKING:
    _ListJobsByPipelinePaginatorBase = AioPaginator[ListJobsByPipelineResponseTypeDef]
else:
    _ListJobsByPipelinePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobsByPipelinePaginator(_ListJobsByPipelinePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListJobsByPipeline.html#ElasticTranscoder.Paginator.ListJobsByPipeline)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listjobsbypipelinepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsByPipelineRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsByPipelineResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListJobsByPipeline.html#ElasticTranscoder.Paginator.ListJobsByPipeline.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listjobsbypipelinepaginator)
        """


if TYPE_CHECKING:
    _ListJobsByStatusPaginatorBase = AioPaginator[ListJobsByStatusResponseTypeDef]
else:
    _ListJobsByStatusPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobsByStatusPaginator(_ListJobsByStatusPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListJobsByStatus.html#ElasticTranscoder.Paginator.ListJobsByStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listjobsbystatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsByStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsByStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListJobsByStatus.html#ElasticTranscoder.Paginator.ListJobsByStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listjobsbystatuspaginator)
        """


if TYPE_CHECKING:
    _ListPipelinesPaginatorBase = AioPaginator[ListPipelinesResponseTypeDef]
else:
    _ListPipelinesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPipelinesPaginator(_ListPipelinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListPipelines.html#ElasticTranscoder.Paginator.ListPipelines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listpipelinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelinesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListPipelines.html#ElasticTranscoder.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listpipelinespaginator)
        """


if TYPE_CHECKING:
    _ListPresetsPaginatorBase = AioPaginator[ListPresetsResponseTypeDef]
else:
    _ListPresetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPresetsPaginator(_ListPresetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListPresets.html#ElasticTranscoder.Paginator.ListPresets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listpresetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPresetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPresetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/paginator/ListPresets.html#ElasticTranscoder.Paginator.ListPresets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listpresetspaginator)
        """
