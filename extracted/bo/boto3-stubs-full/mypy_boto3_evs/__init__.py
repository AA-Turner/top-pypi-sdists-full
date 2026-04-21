"""
Main interface for evs service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_evs import (
        Client,
        EVSClient,
        ListEnvironmentConnectorsPaginator,
        ListEnvironmentHostsPaginator,
        ListEnvironmentVlansPaginator,
        ListEnvironmentsPaginator,
        ListVmEntitlementsPaginator,
    )

    session = Session()
    client: EVSClient = session.client("evs")

    list_environment_connectors_paginator: ListEnvironmentConnectorsPaginator = client.get_paginator("list_environment_connectors")
    list_environment_hosts_paginator: ListEnvironmentHostsPaginator = client.get_paginator("list_environment_hosts")
    list_environment_vlans_paginator: ListEnvironmentVlansPaginator = client.get_paginator("list_environment_vlans")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    list_vm_entitlements_paginator: ListVmEntitlementsPaginator = client.get_paginator("list_vm_entitlements")
    ```
"""

from .client import EVSClient
from .paginator import (
    ListEnvironmentConnectorsPaginator,
    ListEnvironmentHostsPaginator,
    ListEnvironmentsPaginator,
    ListEnvironmentVlansPaginator,
    ListVmEntitlementsPaginator,
)

Client = EVSClient


__all__ = (
    "Client",
    "EVSClient",
    "ListEnvironmentConnectorsPaginator",
    "ListEnvironmentHostsPaginator",
    "ListEnvironmentVlansPaginator",
    "ListEnvironmentsPaginator",
    "ListVmEntitlementsPaginator",
)
