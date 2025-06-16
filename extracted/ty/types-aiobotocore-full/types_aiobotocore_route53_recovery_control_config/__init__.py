"""
Main interface for route53-recovery-control-config service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53_recovery_control_config import (
        Client,
        ClusterCreatedWaiter,
        ClusterDeletedWaiter,
        ControlPanelCreatedWaiter,
        ControlPanelDeletedWaiter,
        ListAssociatedRoute53HealthChecksPaginator,
        ListClustersPaginator,
        ListControlPanelsPaginator,
        ListRoutingControlsPaginator,
        ListSafetyRulesPaginator,
        Route53RecoveryControlConfigClient,
        RoutingControlCreatedWaiter,
        RoutingControlDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("route53-recovery-control-config") as client:
        client: Route53RecoveryControlConfigClient
        ...


    cluster_created_waiter: ClusterCreatedWaiter = client.get_waiter("cluster_created")
    cluster_deleted_waiter: ClusterDeletedWaiter = client.get_waiter("cluster_deleted")
    control_panel_created_waiter: ControlPanelCreatedWaiter = client.get_waiter("control_panel_created")
    control_panel_deleted_waiter: ControlPanelDeletedWaiter = client.get_waiter("control_panel_deleted")
    routing_control_created_waiter: RoutingControlCreatedWaiter = client.get_waiter("routing_control_created")
    routing_control_deleted_waiter: RoutingControlDeletedWaiter = client.get_waiter("routing_control_deleted")

    list_associated_route53_health_checks_paginator: ListAssociatedRoute53HealthChecksPaginator = client.get_paginator("list_associated_route53_health_checks")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_control_panels_paginator: ListControlPanelsPaginator = client.get_paginator("list_control_panels")
    list_routing_controls_paginator: ListRoutingControlsPaginator = client.get_paginator("list_routing_controls")
    list_safety_rules_paginator: ListSafetyRulesPaginator = client.get_paginator("list_safety_rules")
    ```
"""

from .client import Route53RecoveryControlConfigClient
from .paginator import (
    ListAssociatedRoute53HealthChecksPaginator,
    ListClustersPaginator,
    ListControlPanelsPaginator,
    ListRoutingControlsPaginator,
    ListSafetyRulesPaginator,
)
from .waiter import (
    ClusterCreatedWaiter,
    ClusterDeletedWaiter,
    ControlPanelCreatedWaiter,
    ControlPanelDeletedWaiter,
    RoutingControlCreatedWaiter,
    RoutingControlDeletedWaiter,
)

Client = Route53RecoveryControlConfigClient


__all__ = (
    "Client",
    "ClusterCreatedWaiter",
    "ClusterDeletedWaiter",
    "ControlPanelCreatedWaiter",
    "ControlPanelDeletedWaiter",
    "ListAssociatedRoute53HealthChecksPaginator",
    "ListClustersPaginator",
    "ListControlPanelsPaginator",
    "ListRoutingControlsPaginator",
    "ListSafetyRulesPaginator",
    "Route53RecoveryControlConfigClient",
    "RoutingControlCreatedWaiter",
    "RoutingControlDeletedWaiter",
)
