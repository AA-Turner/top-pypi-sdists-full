"""
Main interface for mediastore-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediastore_data import (
        Client,
        ListItemsPaginator,
        MediaStoreDataClient,
    )

    session = get_session()
    async with session.create_client("mediastore-data") as client:
        client: MediaStoreDataClient
        ...


    list_items_paginator: ListItemsPaginator = client.get_paginator("list_items")
    ```
"""

from .client import MediaStoreDataClient
from .paginator import ListItemsPaginator

Client = MediaStoreDataClient


__all__ = ("Client", "ListItemsPaginator", "MediaStoreDataClient")
