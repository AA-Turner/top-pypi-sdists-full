"""
Main interface for identitystore service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_identitystore import (
        Client,
        IdentityStoreClient,
        ListGroupMembershipsForMemberPaginator,
        ListGroupMembershipsPaginator,
        ListGroupsPaginator,
        ListIdentityStoresPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    async with session.create_client("identitystore") as client:
        client: IdentityStoreClient
        ...


    list_group_memberships_for_member_paginator: ListGroupMembershipsForMemberPaginator = client.get_paginator("list_group_memberships_for_member")
    list_group_memberships_paginator: ListGroupMembershipsPaginator = client.get_paginator("list_group_memberships")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    list_identity_stores_paginator: ListIdentityStoresPaginator = client.get_paginator("list_identity_stores")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""

from .client import IdentityStoreClient
from .paginator import (
    ListGroupMembershipsForMemberPaginator,
    ListGroupMembershipsPaginator,
    ListGroupsPaginator,
    ListIdentityStoresPaginator,
    ListUsersPaginator,
)

Client = IdentityStoreClient


__all__ = (
    "Client",
    "IdentityStoreClient",
    "ListGroupMembershipsForMemberPaginator",
    "ListGroupMembershipsPaginator",
    "ListGroupsPaginator",
    "ListIdentityStoresPaginator",
    "ListUsersPaginator",
)
