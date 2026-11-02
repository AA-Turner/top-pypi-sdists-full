"""
Main interface for agent-registry-control service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry_control/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_agent_registry_control import (
        AgentRegistryControlClient,
        Client,
        ListRegistriesPaginator,
        ListRegistryRecordsPaginator,
        RegistryReadyWaiter,
        RegistryRecordApprovedWaiter,
    )

    session = Session()
    client: AgentRegistryControlClient = session.client("agent-registry-control")

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
