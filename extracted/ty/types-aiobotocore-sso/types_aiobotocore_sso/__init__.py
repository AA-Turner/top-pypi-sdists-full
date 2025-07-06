"""
Main interface for sso service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sso import (
        Client,
        ListAccountRolesPaginator,
        ListAccountsPaginator,
        SSOClient,
    )

    session = get_session()
    async with session.create_client("sso") as client:
        client: SSOClient
        ...


    list_account_roles_paginator: ListAccountRolesPaginator = client.get_paginator("list_account_roles")
    list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    ```
"""

from .client import SSOClient
from .paginator import ListAccountRolesPaginator, ListAccountsPaginator

Client = SSOClient


__all__ = ("Client", "ListAccountRolesPaginator", "ListAccountsPaginator", "SSOClient")
