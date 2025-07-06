"""
Type annotations for kinesis-video-archived-media service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient
    from types_aiobotocore_kinesis_video_archived_media.paginator import (
        GetImagesPaginator,
        ListFragmentsPaginator,
    )

    session = get_session()
    with session.create_client("kinesis-video-archived-media") as client:
        client: KinesisVideoArchivedMediaClient

        get_images_paginator: GetImagesPaginator = client.get_paginator("get_images")
        list_fragments_paginator: ListFragmentsPaginator = client.get_paginator("list_fragments")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetImagesInputPaginateTypeDef,
    GetImagesOutputTypeDef,
    ListFragmentsInputPaginateTypeDef,
    ListFragmentsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetImagesPaginator", "ListFragmentsPaginator")

if TYPE_CHECKING:
    _GetImagesPaginatorBase = AioPaginator[GetImagesOutputTypeDef]
else:
    _GetImagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetImagesPaginator(_GetImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/GetImages.html#KinesisVideoArchivedMedia.Paginator.GetImages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/#getimagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetImagesInputPaginateTypeDef]
    ) -> AioPageIterator[GetImagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/GetImages.html#KinesisVideoArchivedMedia.Paginator.GetImages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/#getimagespaginator)
        """

if TYPE_CHECKING:
    _ListFragmentsPaginatorBase = AioPaginator[ListFragmentsOutputTypeDef]
else:
    _ListFragmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFragmentsPaginator(_ListFragmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/ListFragments.html#KinesisVideoArchivedMedia.Paginator.ListFragments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/#listfragmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFragmentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListFragmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/ListFragments.html#KinesisVideoArchivedMedia.Paginator.ListFragments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/#listfragmentspaginator)
        """
