"""
Type annotations for finspace-data service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_finspace_data.client import FinSpaceDataClient
    from types_aiobotocore_finspace_data.paginator import (
        ListChangesetsPaginator,
        ListDataViewsPaginator,
        ListDatasetsPaginator,
        ListPermissionGroupsPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    with session.create_client("finspace-data") as client:
        client: FinSpaceDataClient

        list_changesets_paginator: ListChangesetsPaginator = client.get_paginator("list_changesets")
        list_data_views_paginator: ListDataViewsPaginator = client.get_paginator("list_data_views")
        list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
        list_permission_groups_paginator: ListPermissionGroupsPaginator = client.get_paginator("list_permission_groups")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChangesetsRequestPaginateTypeDef,
    ListChangesetsResponseTypeDef,
    ListDatasetsRequestPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListDataViewsRequestPaginateTypeDef,
    ListDataViewsResponseTypeDef,
    ListPermissionGroupsRequestPaginateTypeDef,
    ListPermissionGroupsResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChangesetsPaginator",
    "ListDataViewsPaginator",
    "ListDatasetsPaginator",
    "ListPermissionGroupsPaginator",
    "ListUsersPaginator",
)


if TYPE_CHECKING:
    _ListChangesetsPaginatorBase = AioPaginator[ListChangesetsResponseTypeDef]
else:
    _ListChangesetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChangesetsPaginator(_ListChangesetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListChangesets.html#FinSpaceData.Paginator.ListChangesets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listchangesetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChangesetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChangesetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListChangesets.html#FinSpaceData.Paginator.ListChangesets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listchangesetspaginator)
        """


if TYPE_CHECKING:
    _ListDataViewsPaginatorBase = AioPaginator[ListDataViewsResponseTypeDef]
else:
    _ListDataViewsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDataViewsPaginator(_ListDataViewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDataViews.html#FinSpaceData.Paginator.ListDataViews)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listdataviewspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataViewsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDataViews.html#FinSpaceData.Paginator.ListDataViews.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listdataviewspaginator)
        """


if TYPE_CHECKING:
    _ListDatasetsPaginatorBase = AioPaginator[ListDatasetsResponseTypeDef]
else:
    _ListDatasetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDatasetsPaginator(_ListDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDatasets.html#FinSpaceData.Paginator.ListDatasets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listdatasetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListDatasets.html#FinSpaceData.Paginator.ListDatasets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listdatasetspaginator)
        """


if TYPE_CHECKING:
    _ListPermissionGroupsPaginatorBase = AioPaginator[ListPermissionGroupsResponseTypeDef]
else:
    _ListPermissionGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPermissionGroupsPaginator(_ListPermissionGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListPermissionGroups.html#FinSpaceData.Paginator.ListPermissionGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listpermissiongroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPermissionGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPermissionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListPermissionGroups.html#FinSpaceData.Paginator.ListPermissionGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listpermissiongroupspaginator)
        """


if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListUsers.html#FinSpaceData.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listuserspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/paginator/ListUsers.html#FinSpaceData.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/paginators/#listuserspaginator)
        """
