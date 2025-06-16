"""
Main interface for repostspace service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_repostspace import (
        Client,
        ListSpacesPaginator,
        RePostPrivateClient,
    )

    session = get_session()
    async with session.create_client("repostspace") as client:
        client: RePostPrivateClient
        ...


    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    ```
"""

from .client import RePostPrivateClient
from .paginator import ListSpacesPaginator

Client = RePostPrivateClient

__all__ = ("Client", "ListSpacesPaginator", "RePostPrivateClient")
