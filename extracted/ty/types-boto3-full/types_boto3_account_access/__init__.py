"""
Main interface for account-access service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_account_access/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_account_access import (
        AccountAccessClient,
        ApplicationActiveWaiter,
        Client,
        ListApplicationsPaginator,
        ListEntitlementsPaginator,
    )

    session = Session()
    client: AccountAccessClient = session.client("account-access")

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
