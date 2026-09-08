"""
Main interface for agent-registry service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_agent_registry import (
        AgentRegistryClient,
        Client,
        ListDiscoverableRegistryRecordsPaginator,
    )

    session = get_session()
    async with session.create_client("agent-registry") as client:
        client: AgentRegistryClient
        ...


    list_discoverable_registry_records_paginator: ListDiscoverableRegistryRecordsPaginator = client.get_paginator("list_discoverable_registry_records")
    ```
"""

from .client import AgentRegistryClient
from .paginator import ListDiscoverableRegistryRecordsPaginator

Client = AgentRegistryClient


__all__ = ("AgentRegistryClient", "Client", "ListDiscoverableRegistryRecordsPaginator")
