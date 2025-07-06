"""
Type annotations for groundstation service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_groundstation.client import GroundStationClient
    from types_aiobotocore_groundstation.paginator import (
        ListConfigsPaginator,
        ListContactsPaginator,
        ListDataflowEndpointGroupsPaginator,
        ListEphemeridesPaginator,
        ListGroundStationsPaginator,
        ListMissionProfilesPaginator,
        ListSatellitesPaginator,
    )

    session = get_session()
    with session.create_client("groundstation") as client:
        client: GroundStationClient

        list_configs_paginator: ListConfigsPaginator = client.get_paginator("list_configs")
        list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
        list_dataflow_endpoint_groups_paginator: ListDataflowEndpointGroupsPaginator = client.get_paginator("list_dataflow_endpoint_groups")
        list_ephemerides_paginator: ListEphemeridesPaginator = client.get_paginator("list_ephemerides")
        list_ground_stations_paginator: ListGroundStationsPaginator = client.get_paginator("list_ground_stations")
        list_mission_profiles_paginator: ListMissionProfilesPaginator = client.get_paginator("list_mission_profiles")
        list_satellites_paginator: ListSatellitesPaginator = client.get_paginator("list_satellites")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListConfigsRequestPaginateTypeDef,
    ListConfigsResponseTypeDef,
    ListContactsRequestPaginateTypeDef,
    ListContactsResponseTypeDef,
    ListDataflowEndpointGroupsRequestPaginateTypeDef,
    ListDataflowEndpointGroupsResponseTypeDef,
    ListEphemeridesRequestPaginateTypeDef,
    ListEphemeridesResponseTypeDef,
    ListGroundStationsRequestPaginateTypeDef,
    ListGroundStationsResponseTypeDef,
    ListMissionProfilesRequestPaginateTypeDef,
    ListMissionProfilesResponseTypeDef,
    ListSatellitesRequestPaginateTypeDef,
    ListSatellitesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListConfigsPaginator",
    "ListContactsPaginator",
    "ListDataflowEndpointGroupsPaginator",
    "ListEphemeridesPaginator",
    "ListGroundStationsPaginator",
    "ListMissionProfilesPaginator",
    "ListSatellitesPaginator",
)


if TYPE_CHECKING:
    _ListConfigsPaginatorBase = AioPaginator[ListConfigsResponseTypeDef]
else:
    _ListConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConfigsPaginator(_ListConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListConfigs.html#GroundStation.Paginator.ListConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listconfigspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListConfigs.html#GroundStation.Paginator.ListConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listconfigspaginator)
        """


if TYPE_CHECKING:
    _ListContactsPaginatorBase = AioPaginator[ListContactsResponseTypeDef]
else:
    _ListContactsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListContactsPaginator(_ListContactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListContacts.html#GroundStation.Paginator.ListContacts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listcontactspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContactsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListContacts.html#GroundStation.Paginator.ListContacts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listcontactspaginator)
        """


if TYPE_CHECKING:
    _ListDataflowEndpointGroupsPaginatorBase = AioPaginator[
        ListDataflowEndpointGroupsResponseTypeDef
    ]
else:
    _ListDataflowEndpointGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDataflowEndpointGroupsPaginator(_ListDataflowEndpointGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListDataflowEndpointGroups.html#GroundStation.Paginator.ListDataflowEndpointGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listdataflowendpointgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataflowEndpointGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataflowEndpointGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListDataflowEndpointGroups.html#GroundStation.Paginator.ListDataflowEndpointGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listdataflowendpointgroupspaginator)
        """


if TYPE_CHECKING:
    _ListEphemeridesPaginatorBase = AioPaginator[ListEphemeridesResponseTypeDef]
else:
    _ListEphemeridesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEphemeridesPaginator(_ListEphemeridesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListEphemerides.html#GroundStation.Paginator.ListEphemerides)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listephemeridespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEphemeridesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEphemeridesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListEphemerides.html#GroundStation.Paginator.ListEphemerides.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listephemeridespaginator)
        """


if TYPE_CHECKING:
    _ListGroundStationsPaginatorBase = AioPaginator[ListGroundStationsResponseTypeDef]
else:
    _ListGroundStationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGroundStationsPaginator(_ListGroundStationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListGroundStations.html#GroundStation.Paginator.ListGroundStations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listgroundstationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroundStationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroundStationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListGroundStations.html#GroundStation.Paginator.ListGroundStations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listgroundstationspaginator)
        """


if TYPE_CHECKING:
    _ListMissionProfilesPaginatorBase = AioPaginator[ListMissionProfilesResponseTypeDef]
else:
    _ListMissionProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMissionProfilesPaginator(_ListMissionProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListMissionProfiles.html#GroundStation.Paginator.ListMissionProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listmissionprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMissionProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMissionProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListMissionProfiles.html#GroundStation.Paginator.ListMissionProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listmissionprofilespaginator)
        """


if TYPE_CHECKING:
    _ListSatellitesPaginatorBase = AioPaginator[ListSatellitesResponseTypeDef]
else:
    _ListSatellitesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSatellitesPaginator(_ListSatellitesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListSatellites.html#GroundStation.Paginator.ListSatellites)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listsatellitespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSatellitesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSatellitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation/paginator/ListSatellites.html#GroundStation.Paginator.ListSatellites.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_groundstation/paginators/#listsatellitespaginator)
        """
