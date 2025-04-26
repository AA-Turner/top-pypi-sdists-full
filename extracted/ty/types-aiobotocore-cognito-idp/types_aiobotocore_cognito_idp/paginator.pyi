"""
Type annotations for cognito-idp service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cognito_idp.client import CognitoIdentityProviderClient
    from types_aiobotocore_cognito_idp.paginator import (
        AdminListGroupsForUserPaginator,
        AdminListUserAuthEventsPaginator,
        ListGroupsPaginator,
        ListIdentityProvidersPaginator,
        ListResourceServersPaginator,
        ListUserPoolClientsPaginator,
        ListUserPoolsPaginator,
        ListUsersInGroupPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    with session.create_client("cognito-idp") as client:
        client: CognitoIdentityProviderClient

        admin_list_groups_for_user_paginator: AdminListGroupsForUserPaginator = client.get_paginator("admin_list_groups_for_user")
        admin_list_user_auth_events_paginator: AdminListUserAuthEventsPaginator = client.get_paginator("admin_list_user_auth_events")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_identity_providers_paginator: ListIdentityProvidersPaginator = client.get_paginator("list_identity_providers")
        list_resource_servers_paginator: ListResourceServersPaginator = client.get_paginator("list_resource_servers")
        list_user_pool_clients_paginator: ListUserPoolClientsPaginator = client.get_paginator("list_user_pool_clients")
        list_user_pools_paginator: ListUserPoolsPaginator = client.get_paginator("list_user_pools")
        list_users_in_group_paginator: ListUsersInGroupPaginator = client.get_paginator("list_users_in_group")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    AdminListGroupsForUserRequestPaginateTypeDef,
    AdminListGroupsForUserResponseTypeDef,
    AdminListUserAuthEventsRequestPaginateTypeDef,
    AdminListUserAuthEventsResponseTypeDef,
    ListGroupsRequestPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListIdentityProvidersRequestPaginateTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListResourceServersRequestPaginateTypeDef,
    ListResourceServersResponseTypeDef,
    ListUserPoolClientsRequestPaginateTypeDef,
    ListUserPoolClientsResponseTypeDef,
    ListUserPoolsRequestPaginateTypeDef,
    ListUserPoolsResponseTypeDef,
    ListUsersInGroupRequestPaginateTypeDef,
    ListUsersInGroupResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "AdminListGroupsForUserPaginator",
    "AdminListUserAuthEventsPaginator",
    "ListGroupsPaginator",
    "ListIdentityProvidersPaginator",
    "ListResourceServersPaginator",
    "ListUserPoolClientsPaginator",
    "ListUserPoolsPaginator",
    "ListUsersInGroupPaginator",
    "ListUsersPaginator",
)

if TYPE_CHECKING:
    _AdminListGroupsForUserPaginatorBase = AioPaginator[AdminListGroupsForUserResponseTypeDef]
else:
    _AdminListGroupsForUserPaginatorBase = AioPaginator  # type: ignore[assignment]

class AdminListGroupsForUserPaginator(_AdminListGroupsForUserPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/AdminListGroupsForUser.html#CognitoIdentityProvider.Paginator.AdminListGroupsForUser)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#adminlistgroupsforuserpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[AdminListGroupsForUserRequestPaginateTypeDef]
    ) -> AioPageIterator[AdminListGroupsForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/AdminListGroupsForUser.html#CognitoIdentityProvider.Paginator.AdminListGroupsForUser.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#adminlistgroupsforuserpaginator)
        """

if TYPE_CHECKING:
    _AdminListUserAuthEventsPaginatorBase = AioPaginator[AdminListUserAuthEventsResponseTypeDef]
else:
    _AdminListUserAuthEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class AdminListUserAuthEventsPaginator(_AdminListUserAuthEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/AdminListUserAuthEvents.html#CognitoIdentityProvider.Paginator.AdminListUserAuthEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#adminlistuserautheventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[AdminListUserAuthEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[AdminListUserAuthEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/AdminListUserAuthEvents.html#CognitoIdentityProvider.Paginator.AdminListUserAuthEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#adminlistuserautheventspaginator)
        """

if TYPE_CHECKING:
    _ListGroupsPaginatorBase = AioPaginator[ListGroupsResponseTypeDef]
else:
    _ListGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupsPaginator(_ListGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListGroups.html#CognitoIdentityProvider.Paginator.ListGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListGroups.html#CognitoIdentityProvider.Paginator.ListGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listgroupspaginator)
        """

if TYPE_CHECKING:
    _ListIdentityProvidersPaginatorBase = AioPaginator[ListIdentityProvidersResponseTypeDef]
else:
    _ListIdentityProvidersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIdentityProvidersPaginator(_ListIdentityProvidersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListIdentityProviders.html#CognitoIdentityProvider.Paginator.ListIdentityProviders)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listidentityproviderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdentityProvidersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIdentityProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListIdentityProviders.html#CognitoIdentityProvider.Paginator.ListIdentityProviders.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listidentityproviderspaginator)
        """

if TYPE_CHECKING:
    _ListResourceServersPaginatorBase = AioPaginator[ListResourceServersResponseTypeDef]
else:
    _ListResourceServersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceServersPaginator(_ListResourceServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListResourceServers.html#CognitoIdentityProvider.Paginator.ListResourceServers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listresourceserverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceServersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListResourceServers.html#CognitoIdentityProvider.Paginator.ListResourceServers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listresourceserverspaginator)
        """

if TYPE_CHECKING:
    _ListUserPoolClientsPaginatorBase = AioPaginator[ListUserPoolClientsResponseTypeDef]
else:
    _ListUserPoolClientsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserPoolClientsPaginator(_ListUserPoolClientsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUserPoolClients.html#CognitoIdentityProvider.Paginator.ListUserPoolClients)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listuserpoolclientspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserPoolClientsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserPoolClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUserPoolClients.html#CognitoIdentityProvider.Paginator.ListUserPoolClients.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listuserpoolclientspaginator)
        """

if TYPE_CHECKING:
    _ListUserPoolsPaginatorBase = AioPaginator[ListUserPoolsResponseTypeDef]
else:
    _ListUserPoolsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserPoolsPaginator(_ListUserPoolsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUserPools.html#CognitoIdentityProvider.Paginator.ListUserPools)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listuserpoolspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserPoolsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserPoolsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUserPools.html#CognitoIdentityProvider.Paginator.ListUserPools.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listuserpoolspaginator)
        """

if TYPE_CHECKING:
    _ListUsersInGroupPaginatorBase = AioPaginator[ListUsersInGroupResponseTypeDef]
else:
    _ListUsersInGroupPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUsersInGroupPaginator(_ListUsersInGroupPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUsersInGroup.html#CognitoIdentityProvider.Paginator.ListUsersInGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listusersingrouppaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersInGroupRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersInGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUsersInGroup.html#CognitoIdentityProvider.Paginator.ListUsersInGroup.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listusersingrouppaginator)
        """

if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUsers.html#CognitoIdentityProvider.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/paginator/ListUsers.html#CognitoIdentityProvider.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/paginators/#listuserspaginator)
        """
