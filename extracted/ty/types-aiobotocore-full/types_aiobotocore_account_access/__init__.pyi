"""
Main interface for account-access service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_account_access import (
        AccountAccessClient,
        ApplicationActiveWaiter,
        Client,
        ListApplicationsPaginator,
        ListEntitlementsPaginator,
    )

    session = get_session()
    async with session.create_client("account-access") as client:
        client: AccountAccessClient
        ...


    application_active_waiter: ApplicationActiveWaiter = client.get_waiter("application_active")

    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_entitlements_paginator: ListEntitlementsPaginator = client.get_paginator("list_entitlements")
    ```
"""

from .client import AccountAccessClient
from .paginator import ListApplicationsPaginator, ListEntitlementsPaginator
from .waiter import ApplicationActiveWaiter

Client = AccountAccessClient

__all__ = (
    "AccountAccessClient",
    "ApplicationActiveWaiter",
    "Client",
    "ListApplicationsPaginator",
    "ListEntitlementsPaginator",
)
