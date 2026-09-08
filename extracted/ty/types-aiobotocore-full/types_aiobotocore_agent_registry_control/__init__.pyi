"""
Main interface for agent-registry-control service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_agent_registry_control import (
        AgentRegistryControlClient,
        Client,
        ListRegistriesPaginator,
        ListRegistryRecordsPaginator,
        RegistryReadyWaiter,
        RegistryRecordApprovedWaiter,
    )

    session = get_session()
    async with session.create_client("agent-registry-control") as client:
        client: AgentRegistryControlClient
        ...


    registry_ready_waiter: RegistryReadyWaiter = client.get_waiter("registry_ready")
    registry_record_approved_waiter: RegistryRecordApprovedWaiter = client.get_waiter("registry_record_approved")

    list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
    list_registry_records_paginator: ListRegistryRecordsPaginator = client.get_paginator("list_registry_records")
    ```
"""

from .client import AgentRegistryControlClient
from .paginator import ListRegistriesPaginator, ListRegistryRecordsPaginator
from .waiter import RegistryReadyWaiter, RegistryRecordApprovedWaiter

Client = AgentRegistryControlClient

__all__ = (
    "AgentRegistryControlClient",
    "Client",
    "ListRegistriesPaginator",
    "ListRegistryRecordsPaginator",
    "RegistryReadyWaiter",
    "RegistryRecordApprovedWaiter",
)
