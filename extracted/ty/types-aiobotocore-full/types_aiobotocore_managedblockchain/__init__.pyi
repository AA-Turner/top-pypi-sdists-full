"""
Main interface for managedblockchain service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_managedblockchain import (
        Client,
        ListAccessorsPaginator,
        ManagedBlockchainClient,
    )

    session = get_session()
    async with session.create_client("managedblockchain") as client:
        client: ManagedBlockchainClient
        ...


    list_accessors_paginator: ListAccessorsPaginator = client.get_paginator("list_accessors")
    ```
"""

from .client import ManagedBlockchainClient
from .paginator import ListAccessorsPaginator

Client = ManagedBlockchainClient

__all__ = ("Client", "ListAccessorsPaginator", "ManagedBlockchainClient")
