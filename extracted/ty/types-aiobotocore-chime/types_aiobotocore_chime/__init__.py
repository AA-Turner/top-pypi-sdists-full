"""
Main interface for chime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime import (
        ChimeClient,
        Client,
        ListAccountsPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    async with session.create_client("chime") as client:
        client: ChimeClient
        ...


    list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""

from .client import ChimeClient
from .paginator import ListAccountsPaginator, ListUsersPaginator

Client = ChimeClient


__all__ = ("ChimeClient", "Client", "ListAccountsPaginator", "ListUsersPaginator")
