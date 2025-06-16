"""
Type annotations for mediapackage-vod service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediapackage_vod.client import MediaPackageVodClient

    session = get_session()
    async with session.create_client("mediapackage-vod") as client:
        client: MediaPackageVodClient
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

from .paginator import (
    ListAssetsPaginator,
    ListPackagingConfigurationsPaginator,
    ListPackagingGroupsPaginator,
)
from .type_defs import (
    ConfigureLogsRequestTypeDef,
    ConfigureLogsResponseTypeDef,
    CreateAssetRequestTypeDef,
    CreateAssetResponseTypeDef,
    CreatePackagingConfigurationRequestTypeDef,
    CreatePackagingConfigurationResponseTypeDef,
    CreatePackagingGroupRequestTypeDef,
    CreatePackagingGroupResponseTypeDef,
    DeleteAssetRequestTypeDef,
    DeletePackagingConfigurationRequestTypeDef,
    DeletePackagingGroupRequestTypeDef,
    DescribeAssetRequestTypeDef,
    DescribeAssetResponseTypeDef,
    DescribePackagingConfigurationRequestTypeDef,
    DescribePackagingConfigurationResponseTypeDef,
    DescribePackagingGroupRequestTypeDef,
    DescribePackagingGroupResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ListAssetsRequestTypeDef,
    ListAssetsResponseTypeDef,
    ListPackagingConfigurationsRequestTypeDef,
    ListPackagingConfigurationsResponseTypeDef,
    ListPackagingGroupsRequestTypeDef,
    ListPackagingGroupsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdatePackagingGroupRequestTypeDef,
    UpdatePackagingGroupResponseTypeDef,
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

__all__ = ("MediaPackageVodClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]

class MediaPackageVodClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod.html#MediaPackageVod.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaPackageVodClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod.html#MediaPackageVod.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#generate_presigned_url)
        """

    async def configure_logs(
        self, **kwargs: Unpack[ConfigureLogsRequestTypeDef]
    ) -> ConfigureLogsResponseTypeDef:
        """
        Changes the packaging group's properities to configure log subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/configure_logs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#configure_logs)
        """

    async def create_asset(
        self, **kwargs: Unpack[CreateAssetRequestTypeDef]
    ) -> CreateAssetResponseTypeDef:
        """
        Creates a new MediaPackage VOD Asset resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/create_asset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#create_asset)
        """

    async def create_packaging_configuration(
        self, **kwargs: Unpack[CreatePackagingConfigurationRequestTypeDef]
    ) -> CreatePackagingConfigurationResponseTypeDef:
        """
        Creates a new MediaPackage VOD PackagingConfiguration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/create_packaging_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#create_packaging_configuration)
        """

    async def create_packaging_group(
        self, **kwargs: Unpack[CreatePackagingGroupRequestTypeDef]
    ) -> CreatePackagingGroupResponseTypeDef:
        """
        Creates a new MediaPackage VOD PackagingGroup resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/create_packaging_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#create_packaging_group)
        """

    async def delete_asset(self, **kwargs: Unpack[DeleteAssetRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an existing MediaPackage VOD Asset resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/delete_asset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#delete_asset)
        """

    async def delete_packaging_configuration(
        self, **kwargs: Unpack[DeletePackagingConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a MediaPackage VOD PackagingConfiguration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/delete_packaging_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#delete_packaging_configuration)
        """

    async def delete_packaging_group(
        self, **kwargs: Unpack[DeletePackagingGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a MediaPackage VOD PackagingGroup resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/delete_packaging_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#delete_packaging_group)
        """

    async def describe_asset(
        self, **kwargs: Unpack[DescribeAssetRequestTypeDef]
    ) -> DescribeAssetResponseTypeDef:
        """
        Returns a description of a MediaPackage VOD Asset resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/describe_asset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#describe_asset)
        """

    async def describe_packaging_configuration(
        self, **kwargs: Unpack[DescribePackagingConfigurationRequestTypeDef]
    ) -> DescribePackagingConfigurationResponseTypeDef:
        """
        Returns a description of a MediaPackage VOD PackagingConfiguration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/describe_packaging_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#describe_packaging_configuration)
        """

    async def describe_packaging_group(
        self, **kwargs: Unpack[DescribePackagingGroupRequestTypeDef]
    ) -> DescribePackagingGroupResponseTypeDef:
        """
        Returns a description of a MediaPackage VOD PackagingGroup resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/describe_packaging_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#describe_packaging_group)
        """

    async def list_assets(
        self, **kwargs: Unpack[ListAssetsRequestTypeDef]
    ) -> ListAssetsResponseTypeDef:
        """
        Returns a collection of MediaPackage VOD Asset resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/list_assets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#list_assets)
        """

    async def list_packaging_configurations(
        self, **kwargs: Unpack[ListPackagingConfigurationsRequestTypeDef]
    ) -> ListPackagingConfigurationsResponseTypeDef:
        """
        Returns a collection of MediaPackage VOD PackagingConfiguration resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/list_packaging_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#list_packaging_configurations)
        """

    async def list_packaging_groups(
        self, **kwargs: Unpack[ListPackagingGroupsRequestTypeDef]
    ) -> ListPackagingGroupsResponseTypeDef:
        """
        Returns a collection of MediaPackage VOD PackagingGroup resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/list_packaging_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#list_packaging_groups)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags assigned to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#list_tags_for_resource)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#untag_resource)
        """

    async def update_packaging_group(
        self, **kwargs: Unpack[UpdatePackagingGroupRequestTypeDef]
    ) -> UpdatePackagingGroupResponseTypeDef:
        """
        Updates a specific packaging group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/update_packaging_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#update_packaging_group)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_assets"]
    ) -> ListAssetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_packaging_configurations"]
    ) -> ListPackagingConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_packaging_groups"]
    ) -> ListPackagingGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod.html#MediaPackageVod.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod.html#MediaPackageVod.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/client/)
        """
