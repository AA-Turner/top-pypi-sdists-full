"""
Main interface for route53-recovery-cluster service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53_recovery_cluster import (
        Client,
        ListRoutingControlsPaginator,
        Route53RecoveryClusterClient,
    )

    session = get_session()
    async with session.create_client("route53-recovery-cluster") as client:
        client: Route53RecoveryClusterClient
        ...


    list_routing_controls_paginator: ListRoutingControlsPaginator = client.get_paginator("list_routing_controls")
    ```
"""

from .client import Route53RecoveryClusterClient
from .paginator import ListRoutingControlsPaginator

Client = Route53RecoveryClusterClient

__all__ = ("Client", "ListRoutingControlsPaginator", "Route53RecoveryClusterClient")
