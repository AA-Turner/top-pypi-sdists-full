"""
Main interface for wickr service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_wickr import (
        Client,
        ListBlockedGuestUsersPaginator,
        ListBotsPaginator,
        ListDevicesForUserPaginator,
        ListGuestUsersPaginator,
        ListNetworksPaginator,
        ListSecurityGroupUsersPaginator,
        ListSecurityGroupsPaginator,
        ListUsersPaginator,
        WickrAdminAPIClient,
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

from .client import WickrAdminAPIClient
from .paginator import (
    ListBlockedGuestUsersPaginator,
    ListBotsPaginator,
    ListDevicesForUserPaginator,
    ListGuestUsersPaginator,
    ListNetworksPaginator,
    ListSecurityGroupsPaginator,
    ListSecurityGroupUsersPaginator,
    ListUsersPaginator,
)

Client = WickrAdminAPIClient


__all__ = (
    "Client",
    "ListBlockedGuestUsersPaginator",
    "ListBotsPaginator",
    "ListDevicesForUserPaginator",
    "ListGuestUsersPaginator",
    "ListNetworksPaginator",
    "ListSecurityGroupUsersPaginator",
    "ListSecurityGroupsPaginator",
    "ListUsersPaginator",
    "WickrAdminAPIClient",
)
