"""
Type annotations for s3files service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_s3files.client import S3FilesClient
    from mypy_boto3_s3files.paginator import (
        ListAccessPointsPaginator,
        ListFileSystemsPaginator,
        ListMountTargetsPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: S3FilesClient = session.client("s3files")

    list_access_points_paginator: ListAccessPointsPaginator = client.get_paginator("list_access_points")
    list_file_systems_paginator: ListFileSystemsPaginator = client.get_paginator("list_file_systems")
    list_mount_targets_paginator: ListMountTargetsPaginator = client.get_paginator("list_mount_targets")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccessPointsRequestPaginateTypeDef,
    ListAccessPointsResponseTypeDef,
    ListFileSystemsRequestPaginateTypeDef,
    ListFileSystemsResponseTypeDef,
    ListMountTargetsRequestPaginateTypeDef,
    ListMountTargetsResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAccessPointsPaginator",
    "ListFileSystemsPaginator",
    "ListMountTargetsPaginator",
    "ListTagsForResourcePaginator",
)

if TYPE_CHECKING:
    _ListAccessPointsPaginatorBase = Paginator[ListAccessPointsResponseTypeDef]
else:
    _ListAccessPointsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAccessPointsPaginator(_ListAccessPointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/paginator/ListAccessPoints.html#S3Files.Paginator.ListAccessPoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/paginators/#listaccesspointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessPointsRequestPaginateTypeDef]
    ) -> PageIterator[ListAccessPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/paginator/ListAccessPoints.html#S3Files.Paginator.ListAccessPoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/paginators/#listaccesspointspaginator)
        """

if TYPE_CHECKING:
    _ListFileSystemsPaginatorBase = Paginator[ListFileSystemsResponseTypeDef]
else:
    _ListFileSystemsPaginatorBase = Paginator  # type: ignore[assignment]

class ListFileSystemsPaginator(_ListFileSystemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/paginator/ListFileSystems.html#S3Files.Paginator.ListFileSystems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/paginators/#listfilesystemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFileSystemsRequestPaginateTypeDef]
    ) -> PageIterator[ListFileSystemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/paginator/ListFileSystems.html#S3Files.Paginator.ListFileSystems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/paginators/#listfilesystemspaginator)
        """

if TYPE_CHECKING:
    _ListMountTargetsPaginatorBase = Paginator[ListMountTargetsResponseTypeDef]
else:
    _ListMountTargetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListMountTargetsPaginator(_ListMountTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/paginator/ListMountTargets.html#S3Files.Paginator.ListMountTargets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/paginators/#listmounttargetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMountTargetsRequestPaginateTypeDef]
    ) -> PageIterator[ListMountTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/paginator/ListMountTargets.html#S3Files.Paginator.ListMountTargets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/paginators/#listmounttargetspaginator)
        """

if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = Paginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = Paginator  # type: ignore[assignment]

class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/paginator/ListTagsForResource.html#S3Files.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/paginators/#listtagsforresourcepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/paginator/ListTagsForResource.html#S3Files.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/paginators/#listtagsforresourcepaginator)
        """
