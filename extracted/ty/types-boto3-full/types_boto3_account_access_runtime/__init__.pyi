"""
Main interface for account-access-runtime service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_account_access_runtime/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_account_access_runtime import (
        AccountAccessRuntimeClient,
        Client,
        ListRolesPaginator,
    )

    session = Session()
    client: AccountAccessRuntimeClient = session.client("account-access-runtime")

    list_roles_paginator: ListRolesPaginator = client.get_paginator("list_roles")
    ```
"""

from .client import AccountAccessRuntimeClient
from .paginator import ListRolesPaginator

Client = AccountAccessRuntimeClient

__all__ = ("AccountAccessRuntimeClient", "Client", "ListRolesPaginator")
