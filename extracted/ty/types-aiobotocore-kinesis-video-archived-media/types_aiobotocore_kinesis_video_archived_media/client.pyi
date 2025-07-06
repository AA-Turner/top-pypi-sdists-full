"""
Type annotations for kinesis-video-archived-media service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient

    session = get_session()
    async with session.create_client("kinesis-video-archived-media") as client:
        client: KinesisVideoArchivedMediaClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import GetImagesPaginator, ListFragmentsPaginator
from .type_defs import (
    GetClipInputTypeDef,
    GetClipOutputTypeDef,
    GetDASHStreamingSessionURLInputTypeDef,
    GetDASHStreamingSessionURLOutputTypeDef,
    GetHLSStreamingSessionURLInputTypeDef,
    GetHLSStreamingSessionURLOutputTypeDef,
    GetImagesInputTypeDef,
    GetImagesOutputTypeDef,
    GetMediaForFragmentListInputTypeDef,
    GetMediaForFragmentListOutputTypeDef,
    ListFragmentsInputTypeDef,
    ListFragmentsOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("KinesisVideoArchivedMediaClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ClientLimitExceededException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidCodecPrivateDataException: Type[BotocoreClientError]
    InvalidMediaFrameException: Type[BotocoreClientError]
    MissingCodecPrivateDataException: Type[BotocoreClientError]
    NoDataRetentionException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    UnsupportedStreamMediaTypeException: Type[BotocoreClientError]

class KinesisVideoArchivedMediaClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoArchivedMediaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#generate_presigned_url)
        """

    async def get_clip(self, **kwargs: Unpack[GetClipInputTypeDef]) -> GetClipOutputTypeDef:
        """
        Downloads an MP4 file (clip) containing the archived, on-demand media from the
        specified video stream over the specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/get_clip.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_clip)
        """

    async def get_dash_streaming_session_url(
        self, **kwargs: Unpack[GetDASHStreamingSessionURLInputTypeDef]
    ) -> GetDASHStreamingSessionURLOutputTypeDef:
        """
        Retrieves an MPEG Dynamic Adaptive Streaming over HTTP (DASH) URL for the
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/get_dash_streaming_session_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_dash_streaming_session_url)
        """

    async def get_hls_streaming_session_url(
        self, **kwargs: Unpack[GetHLSStreamingSessionURLInputTypeDef]
    ) -> GetHLSStreamingSessionURLOutputTypeDef:
        """
        Retrieves an HTTP Live Streaming (HLS) URL for the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/get_hls_streaming_session_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_hls_streaming_session_url)
        """

    async def get_images(self, **kwargs: Unpack[GetImagesInputTypeDef]) -> GetImagesOutputTypeDef:
        """
        Retrieves a list of images corresponding to each timestamp for a given time
        range, sampling interval, and image format configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/get_images.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_images)
        """

    async def get_media_for_fragment_list(
        self, **kwargs: Unpack[GetMediaForFragmentListInputTypeDef]
    ) -> GetMediaForFragmentListOutputTypeDef:
        """
        Gets media for a list of fragments (specified by fragment number) from the
        archived data in an Amazon Kinesis video stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/get_media_for_fragment_list.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_media_for_fragment_list)
        """

    async def list_fragments(
        self, **kwargs: Unpack[ListFragmentsInputTypeDef]
    ) -> ListFragmentsOutputTypeDef:
        """
        Returns a list of <a>Fragment</a> objects from the specified stream and
        timestamp range within the archived data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/list_fragments.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#list_fragments)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_images"]
    ) -> GetImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fragments"]
    ) -> ListFragmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/)
        """
