"""
Main interface for ds-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ds_data import (
        Client,
        DirectoryServiceDataClient,
        ListGroupMembersPaginator,
        ListGroupsForMemberPaginator,
        ListGroupsPaginator,
        ListUsersPaginator,
        SearchGroupsPaginator,
        SearchUsersPaginator,
    )

    session = get_session()
    async with session.create_client("ds-data") as client:
        client: DirectoryServiceDataClient
        ...


    list_group_members_paginator: ListGroupMembersPaginator = client.get_paginator("list_group_members")
    list_groups_for_member_paginator: ListGroupsForMemberPaginator = client.get_paginator("list_groups_for_member")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    search_groups_paginator: SearchGroupsPaginator = client.get_paginator("search_groups")
    search_users_paginator: SearchUsersPaginator = client.get_paginator("search_users")
    ```
"""

from .client import DirectoryServiceDataClient
from .paginator import (
    ListGroupMembersPaginator,
    ListGroupsForMemberPaginator,
    ListGroupsPaginator,
    ListUsersPaginator,
    SearchGroupsPaginator,
    SearchUsersPaginator,
)

Client = DirectoryServiceDataClient


__all__ = (
    "Client",
    "DirectoryServiceDataClient",
    "ListGroupMembersPaginator",
    "ListGroupsForMemberPaginator",
    "ListGroupsPaginator",
    "ListUsersPaginator",
    "SearchGroupsPaginator",
    "SearchUsersPaginator",
)
