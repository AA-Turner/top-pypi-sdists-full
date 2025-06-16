"""
Type annotations for mediapackage-vod service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediapackage_vod.client import MediaPackageVodClient
    from types_aiobotocore_mediapackage_vod.paginator import (
        ListAssetsPaginator,
        ListPackagingConfigurationsPaginator,
        ListPackagingGroupsPaginator,
    )

    session = get_session()
    with session.create_client("mediapackage-vod") as client:
        client: MediaPackageVodClient

        list_assets_paginator: ListAssetsPaginator = client.get_paginator("list_assets")
        list_packaging_configurations_paginator: ListPackagingConfigurationsPaginator = client.get_paginator("list_packaging_configurations")
        list_packaging_groups_paginator: ListPackagingGroupsPaginator = client.get_paginator("list_packaging_groups")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAssetsRequestPaginateTypeDef,
    ListAssetsResponseTypeDef,
    ListPackagingConfigurationsRequestPaginateTypeDef,
    ListPackagingConfigurationsResponseTypeDef,
    ListPackagingGroupsRequestPaginateTypeDef,
    ListPackagingGroupsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssetsPaginator",
    "ListPackagingConfigurationsPaginator",
    "ListPackagingGroupsPaginator",
)

if TYPE_CHECKING:
    _ListAssetsPaginatorBase = AioPaginator[ListAssetsResponseTypeDef]
else:
    _ListAssetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssetsPaginator(_ListAssetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListAssets.html#MediaPackageVod.Paginator.ListAssets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/paginators/#listassetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListAssets.html#MediaPackageVod.Paginator.ListAssets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/paginators/#listassetspaginator)
        """

if TYPE_CHECKING:
    _ListPackagingConfigurationsPaginatorBase = AioPaginator[
        ListPackagingConfigurationsResponseTypeDef
    ]
else:
    _ListPackagingConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPackagingConfigurationsPaginator(_ListPackagingConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListPackagingConfigurations.html#MediaPackageVod.Paginator.ListPackagingConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/paginators/#listpackagingconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPackagingConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPackagingConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListPackagingConfigurations.html#MediaPackageVod.Paginator.ListPackagingConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/paginators/#listpackagingconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListPackagingGroupsPaginatorBase = AioPaginator[ListPackagingGroupsResponseTypeDef]
else:
    _ListPackagingGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPackagingGroupsPaginator(_ListPackagingGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListPackagingGroups.html#MediaPackageVod.Paginator.ListPackagingGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/paginators/#listpackaginggroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPackagingGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPackagingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod/paginator/ListPackagingGroups.html#MediaPackageVod.Paginator.ListPackagingGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage_vod/paginators/#listpackaginggroupspaginator)
        """
