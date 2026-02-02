"""
Type annotations for wickr service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_wickr.client import WickrAdminAPIClient
    from mypy_boto3_wickr.paginator import (
        ListBlockedGuestUsersPaginator,
        ListBotsPaginator,
        ListDevicesForUserPaginator,
        ListGuestUsersPaginator,
        ListNetworksPaginator,
        ListSecurityGroupUsersPaginator,
        ListSecurityGroupsPaginator,
        ListUsersPaginator,
    )

    session = Session()
    client: WickrAdminAPIClient = session.client("wickr")

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

from botocore.paginate import PageIterator, Paginator

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
    _ListBlockedGuestUsersPaginatorBase = Paginator[ListBlockedGuestUsersResponseTypeDef]
else:
    _ListBlockedGuestUsersPaginatorBase = Paginator  # type: ignore[assignment]

class ListBlockedGuestUsersPaginator(_ListBlockedGuestUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListBlockedGuestUsers.html#WickrAdminAPI.Paginator.ListBlockedGuestUsers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listblockedguestuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBlockedGuestUsersRequestPaginateTypeDef]
    ) -> PageIterator[ListBlockedGuestUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListBlockedGuestUsers.html#WickrAdminAPI.Paginator.ListBlockedGuestUsers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listblockedguestuserspaginator)
        """

if TYPE_CHECKING:
    _ListBotsPaginatorBase = Paginator[ListBotsResponseTypeDef]
else:
    _ListBotsPaginatorBase = Paginator  # type: ignore[assignment]

class ListBotsPaginator(_ListBotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListBots.html#WickrAdminAPI.Paginator.ListBots)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listbotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBotsRequestPaginateTypeDef]
    ) -> PageIterator[ListBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListBots.html#WickrAdminAPI.Paginator.ListBots.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listbotspaginator)
        """

if TYPE_CHECKING:
    _ListDevicesForUserPaginatorBase = Paginator[ListDevicesForUserResponseTypeDef]
else:
    _ListDevicesForUserPaginatorBase = Paginator  # type: ignore[assignment]

class ListDevicesForUserPaginator(_ListDevicesForUserPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListDevicesForUser.html#WickrAdminAPI.Paginator.ListDevicesForUser)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listdevicesforuserpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicesForUserRequestPaginateTypeDef]
    ) -> PageIterator[ListDevicesForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListDevicesForUser.html#WickrAdminAPI.Paginator.ListDevicesForUser.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listdevicesforuserpaginator)
        """

if TYPE_CHECKING:
    _ListGuestUsersPaginatorBase = Paginator[ListGuestUsersResponseTypeDef]
else:
    _ListGuestUsersPaginatorBase = Paginator  # type: ignore[assignment]

class ListGuestUsersPaginator(_ListGuestUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListGuestUsers.html#WickrAdminAPI.Paginator.ListGuestUsers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listguestuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGuestUsersRequestPaginateTypeDef]
    ) -> PageIterator[ListGuestUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListGuestUsers.html#WickrAdminAPI.Paginator.ListGuestUsers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listguestuserspaginator)
        """

if TYPE_CHECKING:
    _ListNetworksPaginatorBase = Paginator[ListNetworksResponseTypeDef]
else:
    _ListNetworksPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworksPaginator(_ListNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListNetworks.html#WickrAdminAPI.Paginator.ListNetworks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listnetworkspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworksRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListNetworks.html#WickrAdminAPI.Paginator.ListNetworks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listnetworkspaginator)
        """

if TYPE_CHECKING:
    _ListSecurityGroupUsersPaginatorBase = Paginator[ListSecurityGroupUsersResponseTypeDef]
else:
    _ListSecurityGroupUsersPaginatorBase = Paginator  # type: ignore[assignment]

class ListSecurityGroupUsersPaginator(_ListSecurityGroupUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListSecurityGroupUsers.html#WickrAdminAPI.Paginator.ListSecurityGroupUsers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listsecuritygroupuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityGroupUsersRequestPaginateTypeDef]
    ) -> PageIterator[ListSecurityGroupUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListSecurityGroupUsers.html#WickrAdminAPI.Paginator.ListSecurityGroupUsers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listsecuritygroupuserspaginator)
        """

if TYPE_CHECKING:
    _ListSecurityGroupsPaginatorBase = Paginator[ListSecurityGroupsResponseTypeDef]
else:
    _ListSecurityGroupsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSecurityGroupsPaginator(_ListSecurityGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListSecurityGroups.html#WickrAdminAPI.Paginator.ListSecurityGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listsecuritygroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityGroupsRequestPaginateTypeDef]
    ) -> PageIterator[ListSecurityGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListSecurityGroups.html#WickrAdminAPI.Paginator.ListSecurityGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listsecuritygroupspaginator)
        """

if TYPE_CHECKING:
    _ListUsersPaginatorBase = Paginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = Paginator  # type: ignore[assignment]

class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListUsers.html#WickrAdminAPI.Paginator.ListUsers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/paginator/ListUsers.html#WickrAdminAPI.Paginator.ListUsers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/paginators/#listuserspaginator)
        """
