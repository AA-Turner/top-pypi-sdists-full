"""
Main interface for agent-registry service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_registry/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_agent_registry import (
        AgentRegistryClient,
        Client,
        ListDiscoverableRegistryRecordsPaginator,
    )

    session = Session()
    client: AgentRegistryClient = session.client("agent-registry")

    list_discoverable_registry_records_paginator: ListDiscoverableRegistryRecordsPaginator = client.get_paginator("list_discoverable_registry_records")
    ```
"""

from .client import AgentRegistryClient
from .paginator import ListDiscoverableRegistryRecordsPaginator

Client = AgentRegistryClient


__all__ = ("AgentRegistryClient", "Client", "ListDiscoverableRegistryRecordsPaginator")
