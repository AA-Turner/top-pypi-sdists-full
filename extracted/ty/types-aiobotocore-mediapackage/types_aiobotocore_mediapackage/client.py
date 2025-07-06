"""
Type annotations for mediapackage service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediapackage.client import MediaPackageClient

    session = get_session()
    async with session.create_client("mediapackage") as client:
        client: MediaPackageClient
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

from .paginator import ListChannelsPaginator, ListHarvestJobsPaginator, ListOriginEndpointsPaginator
from .type_defs import (
    ConfigureLogsRequestTypeDef,
    ConfigureLogsResponseTypeDef,
    CreateChannelRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateHarvestJobRequestTypeDef,
    CreateHarvestJobResponseTypeDef,
    CreateOriginEndpointRequestTypeDef,
    CreateOriginEndpointResponseTypeDef,
    DeleteChannelRequestTypeDef,
    DeleteOriginEndpointRequestTypeDef,
    DescribeChannelRequestTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeHarvestJobRequestTypeDef,
    DescribeHarvestJobResponseTypeDef,
    DescribeOriginEndpointRequestTypeDef,
    DescribeOriginEndpointResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ListChannelsRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListHarvestJobsRequestTypeDef,
    ListHarvestJobsResponseTypeDef,
    ListOriginEndpointsRequestTypeDef,
    ListOriginEndpointsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RotateChannelCredentialsRequestTypeDef,
    RotateChannelCredentialsResponseTypeDef,
    RotateIngestEndpointCredentialsRequestTypeDef,
    RotateIngestEndpointCredentialsResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateChannelRequestTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateOriginEndpointRequestTypeDef,
    UpdateOriginEndpointResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("MediaPackageClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]


class MediaPackageClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaPackageClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#generate_presigned_url)
        """

    async def configure_logs(
        self, **kwargs: Unpack[ConfigureLogsRequestTypeDef]
    ) -> ConfigureLogsResponseTypeDef:
        """
        Changes the Channel's properities to configure log subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/configure_logs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#configure_logs)
        """

    async def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a new Channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/create_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#create_channel)
        """

    async def create_harvest_job(
        self, **kwargs: Unpack[CreateHarvestJobRequestTypeDef]
    ) -> CreateHarvestJobResponseTypeDef:
        """
        Creates a new HarvestJob record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/create_harvest_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#create_harvest_job)
        """

    async def create_origin_endpoint(
        self, **kwargs: Unpack[CreateOriginEndpointRequestTypeDef]
    ) -> CreateOriginEndpointResponseTypeDef:
        """
        Creates a new OriginEndpoint record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/create_origin_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#create_origin_endpoint)
        """

    async def delete_channel(self, **kwargs: Unpack[DeleteChannelRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an existing Channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/delete_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#delete_channel)
        """

    async def delete_origin_endpoint(
        self, **kwargs: Unpack[DeleteOriginEndpointRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing OriginEndpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/delete_origin_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#delete_origin_endpoint)
        """

    async def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Gets details about a Channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/describe_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#describe_channel)
        """

    async def describe_harvest_job(
        self, **kwargs: Unpack[DescribeHarvestJobRequestTypeDef]
    ) -> DescribeHarvestJobResponseTypeDef:
        """
        Gets details about an existing HarvestJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/describe_harvest_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#describe_harvest_job)
        """

    async def describe_origin_endpoint(
        self, **kwargs: Unpack[DescribeOriginEndpointRequestTypeDef]
    ) -> DescribeOriginEndpointResponseTypeDef:
        """
        Gets details about an existing OriginEndpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/describe_origin_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#describe_origin_endpoint)
        """

    async def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Returns a collection of Channels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/list_channels.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#list_channels)
        """

    async def list_harvest_jobs(
        self, **kwargs: Unpack[ListHarvestJobsRequestTypeDef]
    ) -> ListHarvestJobsResponseTypeDef:
        """
        Returns a collection of HarvestJob records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/list_harvest_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#list_harvest_jobs)
        """

    async def list_origin_endpoints(
        self, **kwargs: Unpack[ListOriginEndpointsRequestTypeDef]
    ) -> ListOriginEndpointsResponseTypeDef:
        """
        Returns a collection of OriginEndpoint records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/list_origin_endpoints.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#list_origin_endpoints)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#list_tags_for_resource)
        """

    async def rotate_channel_credentials(
        self, **kwargs: Unpack[RotateChannelCredentialsRequestTypeDef]
    ) -> RotateChannelCredentialsResponseTypeDef:
        """
        Changes the Channel's first IngestEndpoint's username and password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/rotate_channel_credentials.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#rotate_channel_credentials)
        """

    async def rotate_ingest_endpoint_credentials(
        self, **kwargs: Unpack[RotateIngestEndpointCredentialsRequestTypeDef]
    ) -> RotateIngestEndpointCredentialsResponseTypeDef:
        """
        Rotate the IngestEndpoint's username and password, as specified by the
        IngestEndpoint's id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/rotate_ingest_endpoint_credentials.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#rotate_ingest_endpoint_credentials)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#untag_resource)
        """

    async def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates an existing Channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/update_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#update_channel)
        """

    async def update_origin_endpoint(
        self, **kwargs: Unpack[UpdateOriginEndpointRequestTypeDef]
    ) -> UpdateOriginEndpointResponseTypeDef:
        """
        Updates an existing OriginEndpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/update_origin_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#update_origin_endpoint)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_channels"]
    ) -> ListChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_harvest_jobs"]
    ) -> ListHarvestJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_origin_endpoints"]
    ) -> ListOriginEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/)
        """
