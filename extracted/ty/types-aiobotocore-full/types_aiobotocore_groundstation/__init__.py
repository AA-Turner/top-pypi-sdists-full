"""
Main interface for groundstation service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_groundstation import (
        Client,
        ContactScheduledWaiter,
        ContactUpdatedWaiter,
        GroundStationClient,
        ListAntennasPaginator,
        ListConfigsPaginator,
        ListContactVersionsPaginator,
        ListContactsPaginator,
        ListDataflowEndpointGroupsPaginator,
        ListEphemeridesPaginator,
        ListGroundStationReservationsPaginator,
        ListGroundStationsPaginator,
        ListMissionProfilesPaginator,
        ListSatellitesPaginator,
    )

    session = get_session()
    async with session.create_client("groundstation") as client:
        client: GroundStationClient
        ...


    contact_scheduled_waiter: ContactScheduledWaiter = client.get_waiter("contact_scheduled")
    contact_updated_waiter: ContactUpdatedWaiter = client.get_waiter("contact_updated")

    list_antennas_paginator: ListAntennasPaginator = client.get_paginator("list_antennas")
    list_configs_paginator: ListConfigsPaginator = client.get_paginator("list_configs")
    list_contact_versions_paginator: ListContactVersionsPaginator = client.get_paginator("list_contact_versions")
    list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
    list_dataflow_endpoint_groups_paginator: ListDataflowEndpointGroupsPaginator = client.get_paginator("list_dataflow_endpoint_groups")
    list_ephemerides_paginator: ListEphemeridesPaginator = client.get_paginator("list_ephemerides")
    list_ground_station_reservations_paginator: ListGroundStationReservationsPaginator = client.get_paginator("list_ground_station_reservations")
    list_ground_stations_paginator: ListGroundStationsPaginator = client.get_paginator("list_ground_stations")
    list_mission_profiles_paginator: ListMissionProfilesPaginator = client.get_paginator("list_mission_profiles")
    list_satellites_paginator: ListSatellitesPaginator = client.get_paginator("list_satellites")
    ```
"""

from .client import GroundStationClient
from .paginator import (
    ListAntennasPaginator,
    ListConfigsPaginator,
    ListContactsPaginator,
    ListContactVersionsPaginator,
    ListDataflowEndpointGroupsPaginator,
    ListEphemeridesPaginator,
    ListGroundStationReservationsPaginator,
    ListGroundStationsPaginator,
    ListMissionProfilesPaginator,
    ListSatellitesPaginator,
)
from .waiter import ContactScheduledWaiter, ContactUpdatedWaiter

Client = GroundStationClient


__all__ = (
    "Client",
    "ContactScheduledWaiter",
    "ContactUpdatedWaiter",
    "GroundStationClient",
    "ListAntennasPaginator",
    "ListConfigsPaginator",
    "ListContactVersionsPaginator",
    "ListContactsPaginator",
    "ListDataflowEndpointGroupsPaginator",
    "ListEphemeridesPaginator",
    "ListGroundStationReservationsPaginator",
    "ListGroundStationsPaginator",
    "ListMissionProfilesPaginator",
    "ListSatellitesPaginator",
)
