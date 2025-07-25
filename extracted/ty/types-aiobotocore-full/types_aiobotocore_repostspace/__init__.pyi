"""
Main interface for repostspace service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_repostspace import (
        ChannelCreatedWaiter,
        ChannelDeletedWaiter,
        Client,
        ListChannelsPaginator,
        ListSpacesPaginator,
        RePostPrivateClient,
        SpaceCreatedWaiter,
        SpaceDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("repostspace") as client:
        client: RePostPrivateClient
        ...


    channel_created_waiter: ChannelCreatedWaiter = client.get_waiter("channel_created")
    channel_deleted_waiter: ChannelDeletedWaiter = client.get_waiter("channel_deleted")
    space_created_waiter: SpaceCreatedWaiter = client.get_waiter("space_created")
    space_deleted_waiter: SpaceDeletedWaiter = client.get_waiter("space_deleted")

    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    ```
"""

from .client import RePostPrivateClient
from .paginator import ListChannelsPaginator, ListSpacesPaginator
from .waiter import (
    ChannelCreatedWaiter,
    ChannelDeletedWaiter,
    SpaceCreatedWaiter,
    SpaceDeletedWaiter,
)

Client = RePostPrivateClient

__all__ = (
    "ChannelCreatedWaiter",
    "ChannelDeletedWaiter",
    "Client",
    "ListChannelsPaginator",
    "ListSpacesPaginator",
    "RePostPrivateClient",
    "SpaceCreatedWaiter",
    "SpaceDeletedWaiter",
)
