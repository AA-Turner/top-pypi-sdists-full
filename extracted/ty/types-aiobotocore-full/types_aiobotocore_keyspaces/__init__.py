"""
Main interface for keyspaces service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspaces/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_keyspaces import (
        Client,
        KeyspacesClient,
        ListKeyspacesPaginator,
        ListTablesPaginator,
        ListTagsForResourcePaginator,
        ListTypesPaginator,
    )

    session = get_session()
    async with session.create_client("keyspaces") as client:
        client: KeyspacesClient
        ...


    list_keyspaces_paginator: ListKeyspacesPaginator = client.get_paginator("list_keyspaces")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_types_paginator: ListTypesPaginator = client.get_paginator("list_types")
    ```
"""

from .client import KeyspacesClient
from .paginator import (
    ListKeyspacesPaginator,
    ListTablesPaginator,
    ListTagsForResourcePaginator,
    ListTypesPaginator,
)

Client = KeyspacesClient


__all__ = (
    "Client",
    "KeyspacesClient",
    "ListKeyspacesPaginator",
    "ListTablesPaginator",
    "ListTagsForResourcePaginator",
    "ListTypesPaginator",
)
