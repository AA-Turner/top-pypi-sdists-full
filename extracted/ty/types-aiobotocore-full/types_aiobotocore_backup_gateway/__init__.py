"""
Main interface for backup-gateway service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_backup_gateway import (
        BackupGatewayClient,
        Client,
        ListGatewaysPaginator,
        ListHypervisorsPaginator,
        ListVirtualMachinesPaginator,
    )

    session = get_session()
    async with session.create_client("backup-gateway") as client:
        client: BackupGatewayClient
        ...


    list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
    list_hypervisors_paginator: ListHypervisorsPaginator = client.get_paginator("list_hypervisors")
    list_virtual_machines_paginator: ListVirtualMachinesPaginator = client.get_paginator("list_virtual_machines")
    ```
"""

from .client import BackupGatewayClient
from .paginator import ListGatewaysPaginator, ListHypervisorsPaginator, ListVirtualMachinesPaginator

Client = BackupGatewayClient


__all__ = (
    "BackupGatewayClient",
    "Client",
    "ListGatewaysPaginator",
    "ListHypervisorsPaginator",
    "ListVirtualMachinesPaginator",
)
