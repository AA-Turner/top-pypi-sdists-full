"""
Main interface for mediastore service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediastore import (
        Client,
        ListContainersPaginator,
        MediaStoreClient,
    )

    session = get_session()
    async with session.create_client("mediastore") as client:
        client: MediaStoreClient
        ...


    list_containers_paginator: ListContainersPaginator = client.get_paginator("list_containers")
    ```
"""

from .client import MediaStoreClient
from .paginator import ListContainersPaginator

Client = MediaStoreClient


__all__ = ("Client", "ListContainersPaginator", "MediaStoreClient")
