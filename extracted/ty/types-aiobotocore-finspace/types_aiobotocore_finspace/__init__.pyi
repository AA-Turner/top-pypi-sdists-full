"""
Main interface for finspace service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_finspace import (
        Client,
        FinspaceClient,
        ListKxEnvironmentsPaginator,
    )

    session = get_session()
    async with session.create_client("finspace") as client:
        client: FinspaceClient
        ...


    list_kx_environments_paginator: ListKxEnvironmentsPaginator = client.get_paginator("list_kx_environments")
    ```
"""

from .client import FinspaceClient
from .paginator import ListKxEnvironmentsPaginator

Client = FinspaceClient

__all__ = ("Client", "FinspaceClient", "ListKxEnvironmentsPaginator")
