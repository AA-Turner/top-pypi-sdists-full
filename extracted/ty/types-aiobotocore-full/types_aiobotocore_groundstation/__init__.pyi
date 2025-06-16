"""
Main interface for groundstation service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_groundstation import (
        Client,
        ContactScheduledWaiter,
        GroundStationClient,
        ListConfigsPaginator,
        ListContactsPaginator,
        ListDataflowEndpointGroupsPaginator,
        ListEphemeridesPaginator,
        ListGroundStationsPaginator,
        ListMissionProfilesPaginator,
        ListSatellitesPaginator,
    )

    session = get_session()
    async with session.create_client("groundstation") as client:
        client: GroundStationClient
        ...


    contact_scheduled_waiter: ContactScheduledWaiter = client.get_waiter("contact_scheduled")

    list_configs_paginator: ListConfigsPaginator = client.get_paginator("list_configs")
    list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
    list_dataflow_endpoint_groups_paginator: ListDataflowEndpointGroupsPaginator = client.get_paginator("list_dataflow_endpoint_groups")
    list_ephemerides_paginator: ListEphemeridesPaginator = client.get_paginator("list_ephemerides")
    list_ground_stations_paginator: ListGroundStationsPaginator = client.get_paginator("list_ground_stations")
    list_mission_profiles_paginator: ListMissionProfilesPaginator = client.get_paginator("list_mission_profiles")
    list_satellites_paginator: ListSatellitesPaginator = client.get_paginator("list_satellites")
    ```
"""

from .client import GroundStationClient
from .paginator import (
    ListConfigsPaginator,
    ListContactsPaginator,
    ListDataflowEndpointGroupsPaginator,
    ListEphemeridesPaginator,
    ListGroundStationsPaginator,
    ListMissionProfilesPaginator,
    ListSatellitesPaginator,
)
from .waiter import ContactScheduledWaiter

Client = GroundStationClient

__all__ = (
    "Client",
    "ContactScheduledWaiter",
    "GroundStationClient",
    "ListConfigsPaginator",
    "ListContactsPaginator",
    "ListDataflowEndpointGroupsPaginator",
    "ListEphemeridesPaginator",
    "ListGroundStationsPaginator",
    "ListMissionProfilesPaginator",
    "ListSatellitesPaginator",
)
