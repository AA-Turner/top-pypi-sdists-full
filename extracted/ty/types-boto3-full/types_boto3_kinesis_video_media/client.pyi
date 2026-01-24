"""
Type annotations for kinesis-video-media service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_media/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_kinesis_video_media.client import KinesisVideoMediaClient

    session = Session()
    client: KinesisVideoMediaClient = session.client("kinesis-video-media")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import GetMediaInputTypeDef, GetMediaOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("KinesisVideoMediaClient",)

class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ClientLimitExceededException: type[BotocoreClientError]
    ConnectionLimitExceededException: type[BotocoreClientError]
    InvalidArgumentException: type[BotocoreClientError]
    InvalidEndpointException: type[BotocoreClientError]
    NotAuthorizedException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]

class KinesisVideoMediaClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media.html#KinesisVideoMedia.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_media/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoMediaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media.html#KinesisVideoMedia.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_media/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_media/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_media/client/#generate_presigned_url)
        """

    def get_media(self, **kwargs: Unpack[GetMediaInputTypeDef]) -> GetMediaOutputTypeDef:
        """
        Use this API to retrieve media content from a Kinesis video stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media/client/get_media.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_media/client/#get_media)
        """
