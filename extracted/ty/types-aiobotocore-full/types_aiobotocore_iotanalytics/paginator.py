"""
Type annotations for iotanalytics service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iotanalytics.client import IoTAnalyticsClient
    from types_aiobotocore_iotanalytics.paginator import (
        ListChannelsPaginator,
        ListDatasetContentsPaginator,
        ListDatasetsPaginator,
        ListDatastoresPaginator,
        ListPipelinesPaginator,
    )

    session = get_session()
    with session.create_client("iotanalytics") as client:
        client: IoTAnalyticsClient

        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_dataset_contents_paginator: ListDatasetContentsPaginator = client.get_paginator("list_dataset_contents")
        list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
        list_datastores_paginator: ListDatastoresPaginator = client.get_paginator("list_datastores")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChannelsRequestPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListDatasetContentsRequestPaginateTypeDef,
    ListDatasetContentsResponseTypeDef,
    ListDatasetsRequestPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListDatastoresRequestPaginateTypeDef,
    ListDatastoresResponseTypeDef,
    ListPipelinesRequestPaginateTypeDef,
    ListPipelinesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChannelsPaginator",
    "ListDatasetContentsPaginator",
    "ListDatasetsPaginator",
    "ListDatastoresPaginator",
    "ListPipelinesPaginator",
)


if TYPE_CHECKING:
    _ListChannelsPaginatorBase = AioPaginator[ListChannelsResponseTypeDef]
else:
    _ListChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChannelsPaginator(_ListChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListChannels.html#IoTAnalytics.Paginator.ListChannels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listchannelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListChannels.html#IoTAnalytics.Paginator.ListChannels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listchannelspaginator)
        """


if TYPE_CHECKING:
    _ListDatasetContentsPaginatorBase = AioPaginator[ListDatasetContentsResponseTypeDef]
else:
    _ListDatasetContentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDatasetContentsPaginator(_ListDatasetContentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatasetContents.html#IoTAnalytics.Paginator.ListDatasetContents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listdatasetcontentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetContentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatasetContents.html#IoTAnalytics.Paginator.ListDatasetContents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listdatasetcontentspaginator)
        """


if TYPE_CHECKING:
    _ListDatasetsPaginatorBase = AioPaginator[ListDatasetsResponseTypeDef]
else:
    _ListDatasetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDatasetsPaginator(_ListDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatasets.html#IoTAnalytics.Paginator.ListDatasets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listdatasetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatasets.html#IoTAnalytics.Paginator.ListDatasets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listdatasetspaginator)
        """


if TYPE_CHECKING:
    _ListDatastoresPaginatorBase = AioPaginator[ListDatastoresResponseTypeDef]
else:
    _ListDatastoresPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDatastoresPaginator(_ListDatastoresPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatastores.html#IoTAnalytics.Paginator.ListDatastores)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listdatastorespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatastoresRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatastoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListDatastores.html#IoTAnalytics.Paginator.ListDatastores.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listdatastorespaginator)
        """


if TYPE_CHECKING:
    _ListPipelinesPaginatorBase = AioPaginator[ListPipelinesResponseTypeDef]
else:
    _ListPipelinesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPipelinesPaginator(_ListPipelinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListPipelines.html#IoTAnalytics.Paginator.ListPipelines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listpipelinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelinesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics/paginator/ListPipelines.html#IoTAnalytics.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotanalytics/paginators/#listpipelinespaginator)
        """
