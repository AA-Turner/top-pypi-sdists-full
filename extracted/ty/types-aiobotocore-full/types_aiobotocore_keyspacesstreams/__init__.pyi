"""
Main interface for keyspacesstreams service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspacesstreams/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_keyspacesstreams import (
        Client,
        GetStreamPaginator,
        KeyspacesStreamsClient,
        ListStreamsPaginator,
    )

    session = get_session()
    async with session.create_client("keyspacesstreams") as client:
        client: KeyspacesStreamsClient
        ...


    get_stream_paginator: GetStreamPaginator = client.get_paginator("get_stream")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""

from .client import KeyspacesStreamsClient
from .paginator import GetStreamPaginator, ListStreamsPaginator

Client = KeyspacesStreamsClient

__all__ = ("Client", "GetStreamPaginator", "KeyspacesStreamsClient", "ListStreamsPaginator")
