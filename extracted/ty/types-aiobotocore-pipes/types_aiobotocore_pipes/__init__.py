"""
Main interface for pipes service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pipes import (
        Client,
        EventBridgePipesClient,
        ListPipesPaginator,
    )

    session = get_session()
    async with session.create_client("pipes") as client:
        client: EventBridgePipesClient
        ...


    list_pipes_paginator: ListPipesPaginator = client.get_paginator("list_pipes")
    ```
"""

from .client import EventBridgePipesClient
from .paginator import ListPipesPaginator

Client = EventBridgePipesClient


__all__ = ("Client", "EventBridgePipesClient", "ListPipesPaginator")
