"""
Type annotations for appstream service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appstream.client import AppStreamClient
    from types_aiobotocore_appstream.paginator import (
        DescribeDirectoryConfigsPaginator,
        DescribeFleetsPaginator,
        DescribeImageBuildersPaginator,
        DescribeImagesPaginator,
        DescribeSessionsPaginator,
        DescribeStacksPaginator,
        DescribeUserStackAssociationsPaginator,
        DescribeUsersPaginator,
        ListAssociatedFleetsPaginator,
        ListAssociatedStacksPaginator,
    )

    session = get_session()
    with session.create_client("appstream") as client:
        client: AppStreamClient

        describe_directory_configs_paginator: DescribeDirectoryConfigsPaginator = client.get_paginator("describe_directory_configs")
        describe_fleets_paginator: DescribeFleetsPaginator = client.get_paginator("describe_fleets")
        describe_image_builders_paginator: DescribeImageBuildersPaginator = client.get_paginator("describe_image_builders")
        describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
        describe_sessions_paginator: DescribeSessionsPaginator = client.get_paginator("describe_sessions")
        describe_stacks_paginator: DescribeStacksPaginator = client.get_paginator("describe_stacks")
        describe_user_stack_associations_paginator: DescribeUserStackAssociationsPaginator = client.get_paginator("describe_user_stack_associations")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
        list_associated_fleets_paginator: ListAssociatedFleetsPaginator = client.get_paginator("list_associated_fleets")
        list_associated_stacks_paginator: ListAssociatedStacksPaginator = client.get_paginator("list_associated_stacks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeDirectoryConfigsRequestPaginateTypeDef,
    DescribeDirectoryConfigsResultTypeDef,
    DescribeFleetsRequestPaginateTypeDef,
    DescribeFleetsResultTypeDef,
    DescribeImageBuildersRequestPaginateTypeDef,
    DescribeImageBuildersResultTypeDef,
    DescribeImagesRequestPaginateTypeDef,
    DescribeImagesResultTypeDef,
    DescribeSessionsRequestPaginateTypeDef,
    DescribeSessionsResultTypeDef,
    DescribeStacksRequestPaginateTypeDef,
    DescribeStacksResultTypeDef,
    DescribeUsersRequestPaginateTypeDef,
    DescribeUsersResultTypeDef,
    DescribeUserStackAssociationsRequestPaginateTypeDef,
    DescribeUserStackAssociationsResultTypeDef,
    ListAssociatedFleetsRequestPaginateTypeDef,
    ListAssociatedFleetsResultTypeDef,
    ListAssociatedStacksRequestPaginateTypeDef,
    ListAssociatedStacksResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeDirectoryConfigsPaginator",
    "DescribeFleetsPaginator",
    "DescribeImageBuildersPaginator",
    "DescribeImagesPaginator",
    "DescribeSessionsPaginator",
    "DescribeStacksPaginator",
    "DescribeUserStackAssociationsPaginator",
    "DescribeUsersPaginator",
    "ListAssociatedFleetsPaginator",
    "ListAssociatedStacksPaginator",
)


if TYPE_CHECKING:
    _DescribeDirectoryConfigsPaginatorBase = AioPaginator[DescribeDirectoryConfigsResultTypeDef]
else:
    _DescribeDirectoryConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDirectoryConfigsPaginator(_DescribeDirectoryConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeDirectoryConfigs.html#AppStream.Paginator.DescribeDirectoryConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describedirectoryconfigspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDirectoryConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDirectoryConfigsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeDirectoryConfigs.html#AppStream.Paginator.DescribeDirectoryConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describedirectoryconfigspaginator)
        """


if TYPE_CHECKING:
    _DescribeFleetsPaginatorBase = AioPaginator[DescribeFleetsResultTypeDef]
else:
    _DescribeFleetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeFleetsPaginator(_DescribeFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeFleets.html#AppStream.Paginator.DescribeFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describefleetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFleetsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeFleets.html#AppStream.Paginator.DescribeFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describefleetspaginator)
        """


if TYPE_CHECKING:
    _DescribeImageBuildersPaginatorBase = AioPaginator[DescribeImageBuildersResultTypeDef]
else:
    _DescribeImageBuildersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeImageBuildersPaginator(_DescribeImageBuildersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImageBuilders.html#AppStream.Paginator.DescribeImageBuilders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeimagebuilderspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImageBuildersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeImageBuildersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImageBuilders.html#AppStream.Paginator.DescribeImageBuilders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeimagebuilderspaginator)
        """


if TYPE_CHECKING:
    _DescribeImagesPaginatorBase = AioPaginator[DescribeImagesResultTypeDef]
else:
    _DescribeImagesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeImagesPaginator(_DescribeImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImages.html#AppStream.Paginator.DescribeImages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeimagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImagesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImages.html#AppStream.Paginator.DescribeImages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeimagespaginator)
        """


if TYPE_CHECKING:
    _DescribeSessionsPaginatorBase = AioPaginator[DescribeSessionsResultTypeDef]
else:
    _DescribeSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSessionsPaginator(_DescribeSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeSessions.html#AppStream.Paginator.DescribeSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describesessionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSessionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeSessions.html#AppStream.Paginator.DescribeSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describesessionspaginator)
        """


if TYPE_CHECKING:
    _DescribeStacksPaginatorBase = AioPaginator[DescribeStacksResultTypeDef]
else:
    _DescribeStacksPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeStacksPaginator(_DescribeStacksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeStacks.html#AppStream.Paginator.DescribeStacks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describestackspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStacksRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeStacksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeStacks.html#AppStream.Paginator.DescribeStacks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describestackspaginator)
        """


if TYPE_CHECKING:
    _DescribeUserStackAssociationsPaginatorBase = AioPaginator[
        DescribeUserStackAssociationsResultTypeDef
    ]
else:
    _DescribeUserStackAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeUserStackAssociationsPaginator(_DescribeUserStackAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUserStackAssociations.html#AppStream.Paginator.DescribeUserStackAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeuserstackassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeUserStackAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeUserStackAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUserStackAssociations.html#AppStream.Paginator.DescribeUserStackAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeuserstackassociationspaginator)
        """


if TYPE_CHECKING:
    _DescribeUsersPaginatorBase = AioPaginator[DescribeUsersResultTypeDef]
else:
    _DescribeUsersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeUsersPaginator(_DescribeUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUsers.html#AppStream.Paginator.DescribeUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeuserspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUsers.html#AppStream.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeuserspaginator)
        """


if TYPE_CHECKING:
    _ListAssociatedFleetsPaginatorBase = AioPaginator[ListAssociatedFleetsResultTypeDef]
else:
    _ListAssociatedFleetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssociatedFleetsPaginator(_ListAssociatedFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedFleets.html#AppStream.Paginator.ListAssociatedFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#listassociatedfleetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociatedFleetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociatedFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedFleets.html#AppStream.Paginator.ListAssociatedFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#listassociatedfleetspaginator)
        """


if TYPE_CHECKING:
    _ListAssociatedStacksPaginatorBase = AioPaginator[ListAssociatedStacksResultTypeDef]
else:
    _ListAssociatedStacksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssociatedStacksPaginator(_ListAssociatedStacksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedStacks.html#AppStream.Paginator.ListAssociatedStacks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#listassociatedstackspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociatedStacksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociatedStacksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedStacks.html#AppStream.Paginator.ListAssociatedStacks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#listassociatedstackspaginator)
        """
