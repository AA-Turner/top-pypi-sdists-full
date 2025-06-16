"""
Type annotations for ds-data service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ds_data.client import DirectoryServiceDataClient
    from types_aiobotocore_ds_data.paginator import (
        ListGroupMembersPaginator,
        ListGroupsForMemberPaginator,
        ListGroupsPaginator,
        ListUsersPaginator,
        SearchGroupsPaginator,
        SearchUsersPaginator,
    )

    session = get_session()
    with session.create_client("ds-data") as client:
        client: DirectoryServiceDataClient

        list_group_members_paginator: ListGroupMembersPaginator = client.get_paginator("list_group_members")
        list_groups_for_member_paginator: ListGroupsForMemberPaginator = client.get_paginator("list_groups_for_member")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        search_groups_paginator: SearchGroupsPaginator = client.get_paginator("search_groups")
        search_users_paginator: SearchUsersPaginator = client.get_paginator("search_users")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListGroupMembersRequestPaginateTypeDef,
    ListGroupMembersResultTypeDef,
    ListGroupsForMemberRequestPaginateTypeDef,
    ListGroupsForMemberResultTypeDef,
    ListGroupsRequestPaginateTypeDef,
    ListGroupsResultTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResultTypeDef,
    SearchGroupsRequestPaginateTypeDef,
    SearchGroupsResultTypeDef,
    SearchUsersRequestPaginateTypeDef,
    SearchUsersResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListGroupMembersPaginator",
    "ListGroupsForMemberPaginator",
    "ListGroupsPaginator",
    "ListUsersPaginator",
    "SearchGroupsPaginator",
    "SearchUsersPaginator",
)


if TYPE_CHECKING:
    _ListGroupMembersPaginatorBase = AioPaginator[ListGroupMembersResultTypeDef]
else:
    _ListGroupMembersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGroupMembersPaginator(_ListGroupMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroupMembers.html#DirectoryServiceData.Paginator.ListGroupMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupmemberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupMembersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroupMembers.html#DirectoryServiceData.Paginator.ListGroupMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupmemberspaginator)
        """


if TYPE_CHECKING:
    _ListGroupsForMemberPaginatorBase = AioPaginator[ListGroupsForMemberResultTypeDef]
else:
    _ListGroupsForMemberPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGroupsForMemberPaginator(_ListGroupsForMemberPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroupsForMember.html#DirectoryServiceData.Paginator.ListGroupsForMember)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupsformemberpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsForMemberRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsForMemberResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroupsForMember.html#DirectoryServiceData.Paginator.ListGroupsForMember.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupsformemberpaginator)
        """


if TYPE_CHECKING:
    _ListGroupsPaginatorBase = AioPaginator[ListGroupsResultTypeDef]
else:
    _ListGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGroupsPaginator(_ListGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroups.html#DirectoryServiceData.Paginator.ListGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListGroups.html#DirectoryServiceData.Paginator.ListGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupspaginator)
        """


if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResultTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListUsers.html#DirectoryServiceData.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listuserspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/ListUsers.html#DirectoryServiceData.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listuserspaginator)
        """


if TYPE_CHECKING:
    _SearchGroupsPaginatorBase = AioPaginator[SearchGroupsResultTypeDef]
else:
    _SearchGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchGroupsPaginator(_SearchGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/SearchGroups.html#DirectoryServiceData.Paginator.SearchGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#searchgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/SearchGroups.html#DirectoryServiceData.Paginator.SearchGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#searchgroupspaginator)
        """


if TYPE_CHECKING:
    _SearchUsersPaginatorBase = AioPaginator[SearchUsersResultTypeDef]
else:
    _SearchUsersPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchUsersPaginator(_SearchUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/SearchUsers.html#DirectoryServiceData.Paginator.SearchUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#searchuserspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data/paginator/SearchUsers.html#DirectoryServiceData.Paginator.SearchUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#searchuserspaginator)
        """
