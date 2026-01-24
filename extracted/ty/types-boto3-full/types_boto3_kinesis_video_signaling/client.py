"""
Type annotations for kinesis-video-signaling service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_signaling/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_kinesis_video_signaling.client import KinesisVideoSignalingChannelsClient

    session = Session()
    client: KinesisVideoSignalingChannelsClient = session.client("kinesis-video-signaling")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    GetIceServerConfigRequestTypeDef,
    GetIceServerConfigResponseTypeDef,
    SendAlexaOfferToMasterRequestTypeDef,
    SendAlexaOfferToMasterResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("KinesisVideoSignalingChannelsClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ClientLimitExceededException: type[BotocoreClientError]
    InvalidArgumentException: type[BotocoreClientError]
    InvalidClientException: type[BotocoreClientError]
    NotAuthorizedException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    SessionExpiredException: type[BotocoreClientError]


class KinesisVideoSignalingChannelsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_signaling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoSignalingChannelsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_signaling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_signaling/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_signaling/client/#generate_presigned_url)
        """

    def get_ice_server_config(
        self, **kwargs: Unpack[GetIceServerConfigRequestTypeDef]
    ) -> GetIceServerConfigResponseTypeDef:
        """
        Gets the Interactive Connectivity Establishment (ICE) server configuration
        information, including URIs, username, and password which can be used to
        configure the WebRTC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling/client/get_ice_server_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_signaling/client/#get_ice_server_config)
        """

    def send_alexa_offer_to_master(
        self, **kwargs: Unpack[SendAlexaOfferToMasterRequestTypeDef]
    ) -> SendAlexaOfferToMasterResponseTypeDef:
        """
        This API allows you to connect WebRTC-enabled devices with Alexa display
        devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling/client/send_alexa_offer_to_master.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_signaling/client/#send_alexa_offer_to_master)
        """
