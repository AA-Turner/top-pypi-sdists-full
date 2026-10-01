"""
Main interface for eventbridgev2 service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_eventbridgev2 import (
        Client,
        EventBridgeV2Client,
        EventBusActiveWaiter,
        EventBusDeletedWaiter,
        ListEventBusesPaginator,
        ListEventSourcesPaginator,
        ListResourcePoliciesPaginator,
        ListSubscribersPaginator,
    )

    session = get_session()
    async with session.create_client("eventbridgev2") as client:
        client: EventBridgeV2Client
        ...


    event_bus_active_waiter: EventBusActiveWaiter = client.get_waiter("event_bus_active")
    event_bus_deleted_waiter: EventBusDeletedWaiter = client.get_waiter("event_bus_deleted")

    list_event_buses_paginator: ListEventBusesPaginator = client.get_paginator("list_event_buses")
    list_event_sources_paginator: ListEventSourcesPaginator = client.get_paginator("list_event_sources")
    list_resource_policies_paginator: ListResourcePoliciesPaginator = client.get_paginator("list_resource_policies")
    list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```
"""

from .client import EventBridgeV2Client
from .paginator import (
    ListEventBusesPaginator,
    ListEventSourcesPaginator,
    ListResourcePoliciesPaginator,
    ListSubscribersPaginator,
)
from .waiter import EventBusActiveWaiter, EventBusDeletedWaiter

Client = EventBridgeV2Client

__all__ = (
    "Client",
    "EventBridgeV2Client",
    "EventBusActiveWaiter",
    "EventBusDeletedWaiter",
    "ListEventBusesPaginator",
    "ListEventSourcesPaginator",
    "ListResourcePoliciesPaginator",
    "ListSubscribersPaginator",
)
