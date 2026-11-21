"""
Main interface for agent-discovery service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_discovery/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_agent_discovery import (
        AgentDiscoveryClient,
        Client,
        SearchPublicRecordsPaginator,
    )

    session = Session()
    client: AgentDiscoveryClient = session.client("agent-discovery")

    search_public_records_paginator: SearchPublicRecordsPaginator = client.get_paginator("search_public_records")
    ```
"""

from .client import AgentDiscoveryClient
from .paginator import SearchPublicRecordsPaginator

Client = AgentDiscoveryClient


__all__ = ("AgentDiscoveryClient", "Client", "SearchPublicRecordsPaginator")
