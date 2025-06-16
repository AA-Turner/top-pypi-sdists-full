"""
Main interface for notificationscontacts service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notificationscontacts/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_notificationscontacts import (
        Client,
        ListEmailContactsPaginator,
        UserNotificationsContactsClient,
    )

    session = get_session()
    async with session.create_client("notificationscontacts") as client:
        client: UserNotificationsContactsClient
        ...


    list_email_contacts_paginator: ListEmailContactsPaginator = client.get_paginator("list_email_contacts")
    ```
"""

from .client import UserNotificationsContactsClient
from .paginator import ListEmailContactsPaginator

Client = UserNotificationsContactsClient

__all__ = ("Client", "ListEmailContactsPaginator", "UserNotificationsContactsClient")
