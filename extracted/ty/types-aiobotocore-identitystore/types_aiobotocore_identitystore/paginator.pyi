"""
Type annotations for identitystore service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_identitystore.client import IdentityStoreClient
    from types_aiobotocore_identitystore.paginator import (
        ListGroupMembershipsForMemberPaginator,
        ListGroupMembershipsPaginator,
        ListGroupsPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    with session.create_client("identitystore") as client:
        client: IdentityStoreClient

        list_group_memberships_for_member_paginator: ListGroupMembershipsForMemberPaginator = client.get_paginator("list_group_memberships_for_member")
        list_group_memberships_paginator: ListGroupMembershipsPaginator = client.get_paginator("list_group_memberships")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListGroupMembershipsForMemberRequestPaginateTypeDef,
    ListGroupMembershipsForMemberResponseTypeDef,
    ListGroupMembershipsRequestPaginateTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsRequestPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListGroupMembershipsForMemberPaginator",
    "ListGroupMembershipsPaginator",
    "ListGroupsPaginator",
    "ListUsersPaginator",
)

if TYPE_CHECKING:
    _ListGroupMembershipsForMemberPaginatorBase = AioPaginator[
        ListGroupMembershipsForMemberResponseTypeDef
    ]
else:
    _ListGroupMembershipsForMemberPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupMembershipsForMemberPaginator(_ListGroupMembershipsForMemberPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroupMembershipsForMember.html#IdentityStore.Paginator.ListGroupMembershipsForMember)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/paginators/#listgroupmembershipsformemberpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupMembershipsForMemberRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupMembershipsForMemberResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroupMembershipsForMember.html#IdentityStore.Paginator.ListGroupMembershipsForMember.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/paginators/#listgroupmembershipsformemberpaginator)
        """

if TYPE_CHECKING:
    _ListGroupMembershipsPaginatorBase = AioPaginator[ListGroupMembershipsResponseTypeDef]
else:
    _ListGroupMembershipsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupMembershipsPaginator(_ListGroupMembershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroupMemberships.html#IdentityStore.Paginator.ListGroupMemberships)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/paginators/#listgroupmembershipspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupMembershipsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroupMemberships.html#IdentityStore.Paginator.ListGroupMemberships.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/paginators/#listgroupmembershipspaginator)
        """

if TYPE_CHECKING:
    _ListGroupsPaginatorBase = AioPaginator[ListGroupsResponseTypeDef]
else:
    _ListGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupsPaginator(_ListGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroups.html#IdentityStore.Paginator.ListGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/paginators/#listgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListGroups.html#IdentityStore.Paginator.ListGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/paginators/#listgroupspaginator)
        """

if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListUsers.html#IdentityStore.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/paginators/#listuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore/paginator/ListUsers.html#IdentityStore.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/paginators/#listuserspaginator)
        """
