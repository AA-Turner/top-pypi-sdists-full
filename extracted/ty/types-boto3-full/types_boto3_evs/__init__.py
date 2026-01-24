"""
Main interface for evs service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_evs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_evs import (
        Client,
        EVSClient,
        ListEnvironmentHostsPaginator,
        ListEnvironmentVlansPaginator,
        ListEnvironmentsPaginator,
    )

    session = Session()
    client: EVSClient = session.client("evs")

    list_environment_hosts_paginator: ListEnvironmentHostsPaginator = client.get_paginator("list_environment_hosts")
    list_environment_vlans_paginator: ListEnvironmentVlansPaginator = client.get_paginator("list_environment_vlans")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

from .client import EVSClient
from .paginator import (
    ListEnvironmentHostsPaginator,
    ListEnvironmentsPaginator,
    ListEnvironmentVlansPaginator,
)

Client = EVSClient


__all__ = (
    "Client",
    "EVSClient",
    "ListEnvironmentHostsPaginator",
    "ListEnvironmentVlansPaginator",
    "ListEnvironmentsPaginator",
)
