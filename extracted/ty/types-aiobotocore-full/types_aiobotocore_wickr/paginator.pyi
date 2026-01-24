"""
Type annotations for wickr service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_wickr.client import WickrAdminAPIClient
    from types_aiobotocore_wickr.paginator import (
        ListBlockedGuestUsersPaginator,
        ListBotsPaginator,
        ListDevicesForUserPaginator,
        ListGuestUsersPaginator,
        ListNetworksPaginator,
        ListSecurityGroupUsersPaginator,
        ListSecurityGroupsPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    with session.create_client("wickr") as client:
        client: WickrAdminAPIClient

        list_blocked_guest_users_paginator: ListBlockedGuestUsersPaginator = client.get_paginator("list_blocked_guest_users")
        list_bots_paginator: ListBotsPaginator = client.get_paginator("list_bots")
        list_devices_for_user_paginator: ListDevicesForUserPaginator = client.get_paginator("list_devices_for_user")
        list_guest_users_paginator: ListGuestUsersPaginator = client.get_paginator("list_guest_users")
        list_networks_paginator: ListNetworksPaginator = client.get_paginator("list_networks")
        list_security_group_users_paginator: ListSecurityGroupUsersPaginator = client.get_paginator("list_security_group_users")
        list_security_groups_paginator: ListSecurityGroupsPaginator = client.get_paginator("list_security_groups")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListBlockedGuestUsersRequestPaginateTypeDef,
    ListBlockedGuestUsersResponseTypeDef,
    ListBotsRequestPaginateTypeDef,
    ListBotsResponseTypeDef,
    ListDevicesForUserRequestPaginateTypeDef,
    ListDevicesForUserResponseTypeDef,
    ListGuestUsersRequestPaginateTypeDef,
    ListGuestUsersResponseTypeDef,
    ListNetworksRequestPaginateTypeDef,
    ListNetworksResponseTypeDef,
    ListSecurityGroupsRequestPaginateTypeDef,
    ListSecurityGroupsResponseTypeDef,
    ListSecurityGroupUsersRequestPaginateTypeDef,
    ListSecurityGroupUsersResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBlockedGuestUsersPaginator",
    "ListBotsPaginator",
    "ListDevicesForUserPaginator",
    "ListGuestUsersPaginator",
    "ListNetworksPaginator",
    "ListSecurityGroupUsersPaginator",
    "ListSecurityGroupsPaginator",
    "ListUsersPaginator",
)

if TYPE_CHECKING:
    _ListBlockedGuestUsersPaginatorBase = AioPaginator[ListBlockedGuestUsersResponseTypeDef]
else:
    _ListBlockedGuestUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBlockedGuestUsersPaginator(_ListBlockedGuestUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListBlockedGuestUsers.html#WickrAdminAPI.Paginator.ListBlockedGuestUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listblockedguestuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBlockedGuestUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBlockedGuestUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListBlockedGuestUsers.html#WickrAdminAPI.Paginator.ListBlockedGuestUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listblockedguestuserspaginator)
        """

if TYPE_CHECKING:
    _ListBotsPaginatorBase = AioPaginator[ListBotsResponseTypeDef]
else:
    _ListBotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBotsPaginator(_ListBotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListBots.html#WickrAdminAPI.Paginator.ListBots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listbotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBotsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListBots.html#WickrAdminAPI.Paginator.ListBots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listbotspaginator)
        """

if TYPE_CHECKING:
    _ListDevicesForUserPaginatorBase = AioPaginator[ListDevicesForUserResponseTypeDef]
else:
    _ListDevicesForUserPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDevicesForUserPaginator(_ListDevicesForUserPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListDevicesForUser.html#WickrAdminAPI.Paginator.ListDevicesForUser)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listdevicesforuserpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicesForUserRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDevicesForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListDevicesForUser.html#WickrAdminAPI.Paginator.ListDevicesForUser.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listdevicesforuserpaginator)
        """

if TYPE_CHECKING:
    _ListGuestUsersPaginatorBase = AioPaginator[ListGuestUsersResponseTypeDef]
else:
    _ListGuestUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGuestUsersPaginator(_ListGuestUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListGuestUsers.html#WickrAdminAPI.Paginator.ListGuestUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listguestuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGuestUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGuestUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListGuestUsers.html#WickrAdminAPI.Paginator.ListGuestUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listguestuserspaginator)
        """

if TYPE_CHECKING:
    _ListNetworksPaginatorBase = AioPaginator[ListNetworksResponseTypeDef]
else:
    _ListNetworksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworksPaginator(_ListNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListNetworks.html#WickrAdminAPI.Paginator.ListNetworks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listnetworkspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListNetworks.html#WickrAdminAPI.Paginator.ListNetworks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listnetworkspaginator)
        """

if TYPE_CHECKING:
    _ListSecurityGroupUsersPaginatorBase = AioPaginator[ListSecurityGroupUsersResponseTypeDef]
else:
    _ListSecurityGroupUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSecurityGroupUsersPaginator(_ListSecurityGroupUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListSecurityGroupUsers.html#WickrAdminAPI.Paginator.ListSecurityGroupUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listsecuritygroupuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityGroupUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityGroupUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListSecurityGroupUsers.html#WickrAdminAPI.Paginator.ListSecurityGroupUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listsecuritygroupuserspaginator)
        """

if TYPE_CHECKING:
    _ListSecurityGroupsPaginatorBase = AioPaginator[ListSecurityGroupsResponseTypeDef]
else:
    _ListSecurityGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSecurityGroupsPaginator(_ListSecurityGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListSecurityGroups.html#WickrAdminAPI.Paginator.ListSecurityGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listsecuritygroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListSecurityGroups.html#WickrAdminAPI.Paginator.ListSecurityGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listsecuritygroupspaginator)
        """

if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListUsers.html#WickrAdminAPI.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListUsers.html#WickrAdminAPI.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wickr/paginators/#listuserspaginator)
        """
