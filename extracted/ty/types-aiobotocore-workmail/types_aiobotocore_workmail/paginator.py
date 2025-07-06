"""
Type annotations for workmail service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_workmail.client import WorkMailClient
    from types_aiobotocore_workmail.paginator import (
        ListAliasesPaginator,
        ListAvailabilityConfigurationsPaginator,
        ListGroupMembersPaginator,
        ListGroupsPaginator,
        ListMailboxPermissionsPaginator,
        ListOrganizationsPaginator,
        ListPersonalAccessTokensPaginator,
        ListResourceDelegatesPaginator,
        ListResourcesPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    with session.create_client("workmail") as client:
        client: WorkMailClient

        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_availability_configurations_paginator: ListAvailabilityConfigurationsPaginator = client.get_paginator("list_availability_configurations")
        list_group_members_paginator: ListGroupMembersPaginator = client.get_paginator("list_group_members")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_mailbox_permissions_paginator: ListMailboxPermissionsPaginator = client.get_paginator("list_mailbox_permissions")
        list_organizations_paginator: ListOrganizationsPaginator = client.get_paginator("list_organizations")
        list_personal_access_tokens_paginator: ListPersonalAccessTokensPaginator = client.get_paginator("list_personal_access_tokens")
        list_resource_delegates_paginator: ListResourceDelegatesPaginator = client.get_paginator("list_resource_delegates")
        list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAliasesRequestPaginateTypeDef,
    ListAliasesResponseTypeDef,
    ListAvailabilityConfigurationsRequestPaginateTypeDef,
    ListAvailabilityConfigurationsResponseTypeDef,
    ListGroupMembersRequestPaginateTypeDef,
    ListGroupMembersResponseTypeDef,
    ListGroupsRequestPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListMailboxPermissionsRequestPaginateTypeDef,
    ListMailboxPermissionsResponseTypeDef,
    ListOrganizationsRequestPaginateTypeDef,
    ListOrganizationsResponseTypeDef,
    ListPersonalAccessTokensRequestPaginateTypeDef,
    ListPersonalAccessTokensResponseTypeDef,
    ListResourceDelegatesRequestPaginateTypeDef,
    ListResourceDelegatesResponseTypeDef,
    ListResourcesRequestPaginateTypeDef,
    ListResourcesResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAliasesPaginator",
    "ListAvailabilityConfigurationsPaginator",
    "ListGroupMembersPaginator",
    "ListGroupsPaginator",
    "ListMailboxPermissionsPaginator",
    "ListOrganizationsPaginator",
    "ListPersonalAccessTokensPaginator",
    "ListResourceDelegatesPaginator",
    "ListResourcesPaginator",
    "ListUsersPaginator",
)


if TYPE_CHECKING:
    _ListAliasesPaginatorBase = AioPaginator[ListAliasesResponseTypeDef]
else:
    _ListAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAliasesPaginator(_ListAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListAliases.html#WorkMail.Paginator.ListAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listaliasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListAliases.html#WorkMail.Paginator.ListAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listaliasespaginator)
        """


if TYPE_CHECKING:
    _ListAvailabilityConfigurationsPaginatorBase = AioPaginator[
        ListAvailabilityConfigurationsResponseTypeDef
    ]
else:
    _ListAvailabilityConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAvailabilityConfigurationsPaginator(_ListAvailabilityConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListAvailabilityConfigurations.html#WorkMail.Paginator.ListAvailabilityConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listavailabilityconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAvailabilityConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAvailabilityConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListAvailabilityConfigurations.html#WorkMail.Paginator.ListAvailabilityConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listavailabilityconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListGroupMembersPaginatorBase = AioPaginator[ListGroupMembersResponseTypeDef]
else:
    _ListGroupMembersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGroupMembersPaginator(_ListGroupMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListGroupMembers.html#WorkMail.Paginator.ListGroupMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listgroupmemberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListGroupMembers.html#WorkMail.Paginator.ListGroupMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listgroupmemberspaginator)
        """


if TYPE_CHECKING:
    _ListGroupsPaginatorBase = AioPaginator[ListGroupsResponseTypeDef]
else:
    _ListGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGroupsPaginator(_ListGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListGroups.html#WorkMail.Paginator.ListGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListGroups.html#WorkMail.Paginator.ListGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listgroupspaginator)
        """


if TYPE_CHECKING:
    _ListMailboxPermissionsPaginatorBase = AioPaginator[ListMailboxPermissionsResponseTypeDef]
else:
    _ListMailboxPermissionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMailboxPermissionsPaginator(_ListMailboxPermissionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListMailboxPermissions.html#WorkMail.Paginator.ListMailboxPermissions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listmailboxpermissionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMailboxPermissionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMailboxPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListMailboxPermissions.html#WorkMail.Paginator.ListMailboxPermissions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listmailboxpermissionspaginator)
        """


if TYPE_CHECKING:
    _ListOrganizationsPaginatorBase = AioPaginator[ListOrganizationsResponseTypeDef]
else:
    _ListOrganizationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOrganizationsPaginator(_ListOrganizationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListOrganizations.html#WorkMail.Paginator.ListOrganizations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listorganizationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrganizationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOrganizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListOrganizations.html#WorkMail.Paginator.ListOrganizations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listorganizationspaginator)
        """


if TYPE_CHECKING:
    _ListPersonalAccessTokensPaginatorBase = AioPaginator[ListPersonalAccessTokensResponseTypeDef]
else:
    _ListPersonalAccessTokensPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPersonalAccessTokensPaginator(_ListPersonalAccessTokensPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListPersonalAccessTokens.html#WorkMail.Paginator.ListPersonalAccessTokens)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listpersonalaccesstokenspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPersonalAccessTokensRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPersonalAccessTokensResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListPersonalAccessTokens.html#WorkMail.Paginator.ListPersonalAccessTokens.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listpersonalaccesstokenspaginator)
        """


if TYPE_CHECKING:
    _ListResourceDelegatesPaginatorBase = AioPaginator[ListResourceDelegatesResponseTypeDef]
else:
    _ListResourceDelegatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceDelegatesPaginator(_ListResourceDelegatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListResourceDelegates.html#WorkMail.Paginator.ListResourceDelegates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listresourcedelegatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceDelegatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceDelegatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListResourceDelegates.html#WorkMail.Paginator.ListResourceDelegates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listresourcedelegatespaginator)
        """


if TYPE_CHECKING:
    _ListResourcesPaginatorBase = AioPaginator[ListResourcesResponseTypeDef]
else:
    _ListResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourcesPaginator(_ListResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListResources.html#WorkMail.Paginator.ListResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListResources.html#WorkMail.Paginator.ListResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listresourcespaginator)
        """


if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListUsers.html#WorkMail.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listuserspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListUsers.html#WorkMail.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listuserspaginator)
        """
