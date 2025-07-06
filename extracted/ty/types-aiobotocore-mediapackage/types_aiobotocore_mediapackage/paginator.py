"""
Type annotations for mediapackage service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediapackage.client import MediaPackageClient
    from types_aiobotocore_mediapackage.paginator import (
        ListChannelsPaginator,
        ListHarvestJobsPaginator,
        ListOriginEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("mediapackage") as client:
        client: MediaPackageClient

        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_harvest_jobs_paginator: ListHarvestJobsPaginator = client.get_paginator("list_harvest_jobs")
        list_origin_endpoints_paginator: ListOriginEndpointsPaginator = client.get_paginator("list_origin_endpoints")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChannelsRequestPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListHarvestJobsRequestPaginateTypeDef,
    ListHarvestJobsResponseTypeDef,
    ListOriginEndpointsRequestPaginateTypeDef,
    ListOriginEndpointsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListChannelsPaginator", "ListHarvestJobsPaginator", "ListOriginEndpointsPaginator")


if TYPE_CHECKING:
    _ListChannelsPaginatorBase = AioPaginator[ListChannelsResponseTypeDef]
else:
    _ListChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChannelsPaginator(_ListChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListChannels.html#MediaPackage.Paginator.ListChannels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listchannelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListChannels.html#MediaPackage.Paginator.ListChannels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listchannelspaginator)
        """


if TYPE_CHECKING:
    _ListHarvestJobsPaginatorBase = AioPaginator[ListHarvestJobsResponseTypeDef]
else:
    _ListHarvestJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListHarvestJobsPaginator(_ListHarvestJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListHarvestJobs.html#MediaPackage.Paginator.ListHarvestJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listharvestjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHarvestJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHarvestJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListHarvestJobs.html#MediaPackage.Paginator.ListHarvestJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listharvestjobspaginator)
        """


if TYPE_CHECKING:
    _ListOriginEndpointsPaginatorBase = AioPaginator[ListOriginEndpointsResponseTypeDef]
else:
    _ListOriginEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOriginEndpointsPaginator(_ListOriginEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListOriginEndpoints.html#MediaPackage.Paginator.ListOriginEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listoriginendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOriginEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOriginEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/paginator/ListOriginEndpoints.html#MediaPackage.Paginator.ListOriginEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listoriginendpointspaginator)
        """
