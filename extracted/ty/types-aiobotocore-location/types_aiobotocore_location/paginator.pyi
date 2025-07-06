"""
Type annotations for location service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_location.client import LocationServiceClient
    from types_aiobotocore_location.paginator import (
        ForecastGeofenceEventsPaginator,
        GetDevicePositionHistoryPaginator,
        ListDevicePositionsPaginator,
        ListGeofenceCollectionsPaginator,
        ListGeofencesPaginator,
        ListKeysPaginator,
        ListMapsPaginator,
        ListPlaceIndexesPaginator,
        ListRouteCalculatorsPaginator,
        ListTrackerConsumersPaginator,
        ListTrackersPaginator,
    )

    session = get_session()
    with session.create_client("location") as client:
        client: LocationServiceClient

        forecast_geofence_events_paginator: ForecastGeofenceEventsPaginator = client.get_paginator("forecast_geofence_events")
        get_device_position_history_paginator: GetDevicePositionHistoryPaginator = client.get_paginator("get_device_position_history")
        list_device_positions_paginator: ListDevicePositionsPaginator = client.get_paginator("list_device_positions")
        list_geofence_collections_paginator: ListGeofenceCollectionsPaginator = client.get_paginator("list_geofence_collections")
        list_geofences_paginator: ListGeofencesPaginator = client.get_paginator("list_geofences")
        list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
        list_maps_paginator: ListMapsPaginator = client.get_paginator("list_maps")
        list_place_indexes_paginator: ListPlaceIndexesPaginator = client.get_paginator("list_place_indexes")
        list_route_calculators_paginator: ListRouteCalculatorsPaginator = client.get_paginator("list_route_calculators")
        list_tracker_consumers_paginator: ListTrackerConsumersPaginator = client.get_paginator("list_tracker_consumers")
        list_trackers_paginator: ListTrackersPaginator = client.get_paginator("list_trackers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ForecastGeofenceEventsRequestPaginateTypeDef,
    ForecastGeofenceEventsResponseTypeDef,
    GetDevicePositionHistoryRequestPaginateTypeDef,
    GetDevicePositionHistoryResponseTypeDef,
    ListDevicePositionsRequestPaginateTypeDef,
    ListDevicePositionsResponseTypeDef,
    ListGeofenceCollectionsRequestPaginateTypeDef,
    ListGeofenceCollectionsResponseTypeDef,
    ListGeofencesRequestPaginateTypeDef,
    ListGeofencesResponseTypeDef,
    ListKeysRequestPaginateTypeDef,
    ListKeysResponseTypeDef,
    ListMapsRequestPaginateTypeDef,
    ListMapsResponseTypeDef,
    ListPlaceIndexesRequestPaginateTypeDef,
    ListPlaceIndexesResponseTypeDef,
    ListRouteCalculatorsRequestPaginateTypeDef,
    ListRouteCalculatorsResponseTypeDef,
    ListTrackerConsumersRequestPaginateTypeDef,
    ListTrackerConsumersResponseTypeDef,
    ListTrackersRequestPaginateTypeDef,
    ListTrackersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ForecastGeofenceEventsPaginator",
    "GetDevicePositionHistoryPaginator",
    "ListDevicePositionsPaginator",
    "ListGeofenceCollectionsPaginator",
    "ListGeofencesPaginator",
    "ListKeysPaginator",
    "ListMapsPaginator",
    "ListPlaceIndexesPaginator",
    "ListRouteCalculatorsPaginator",
    "ListTrackerConsumersPaginator",
    "ListTrackersPaginator",
)

if TYPE_CHECKING:
    _ForecastGeofenceEventsPaginatorBase = AioPaginator[ForecastGeofenceEventsResponseTypeDef]
else:
    _ForecastGeofenceEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ForecastGeofenceEventsPaginator(_ForecastGeofenceEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ForecastGeofenceEvents.html#LocationService.Paginator.ForecastGeofenceEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#forecastgeofenceeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ForecastGeofenceEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ForecastGeofenceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ForecastGeofenceEvents.html#LocationService.Paginator.ForecastGeofenceEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#forecastgeofenceeventspaginator)
        """

if TYPE_CHECKING:
    _GetDevicePositionHistoryPaginatorBase = AioPaginator[GetDevicePositionHistoryResponseTypeDef]
else:
    _GetDevicePositionHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetDevicePositionHistoryPaginator(_GetDevicePositionHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/GetDevicePositionHistory.html#LocationService.Paginator.GetDevicePositionHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#getdevicepositionhistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDevicePositionHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDevicePositionHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/GetDevicePositionHistory.html#LocationService.Paginator.GetDevicePositionHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#getdevicepositionhistorypaginator)
        """

if TYPE_CHECKING:
    _ListDevicePositionsPaginatorBase = AioPaginator[ListDevicePositionsResponseTypeDef]
else:
    _ListDevicePositionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDevicePositionsPaginator(_ListDevicePositionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListDevicePositions.html#LocationService.Paginator.ListDevicePositions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listdevicepositionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicePositionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDevicePositionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListDevicePositions.html#LocationService.Paginator.ListDevicePositions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listdevicepositionspaginator)
        """

if TYPE_CHECKING:
    _ListGeofenceCollectionsPaginatorBase = AioPaginator[ListGeofenceCollectionsResponseTypeDef]
else:
    _ListGeofenceCollectionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGeofenceCollectionsPaginator(_ListGeofenceCollectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofenceCollections.html#LocationService.Paginator.ListGeofenceCollections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listgeofencecollectionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGeofenceCollectionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGeofenceCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofenceCollections.html#LocationService.Paginator.ListGeofenceCollections.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listgeofencecollectionspaginator)
        """

if TYPE_CHECKING:
    _ListGeofencesPaginatorBase = AioPaginator[ListGeofencesResponseTypeDef]
else:
    _ListGeofencesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGeofencesPaginator(_ListGeofencesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofences.html#LocationService.Paginator.ListGeofences)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listgeofencespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGeofencesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGeofencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListGeofences.html#LocationService.Paginator.ListGeofences.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listgeofencespaginator)
        """

if TYPE_CHECKING:
    _ListKeysPaginatorBase = AioPaginator[ListKeysResponseTypeDef]
else:
    _ListKeysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListKeysPaginator(_ListKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListKeys.html#LocationService.Paginator.ListKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listkeyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListKeys.html#LocationService.Paginator.ListKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listkeyspaginator)
        """

if TYPE_CHECKING:
    _ListMapsPaginatorBase = AioPaginator[ListMapsResponseTypeDef]
else:
    _ListMapsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMapsPaginator(_ListMapsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListMaps.html#LocationService.Paginator.ListMaps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listmapspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMapsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMapsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListMaps.html#LocationService.Paginator.ListMaps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listmapspaginator)
        """

if TYPE_CHECKING:
    _ListPlaceIndexesPaginatorBase = AioPaginator[ListPlaceIndexesResponseTypeDef]
else:
    _ListPlaceIndexesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPlaceIndexesPaginator(_ListPlaceIndexesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListPlaceIndexes.html#LocationService.Paginator.ListPlaceIndexes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listplaceindexespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlaceIndexesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPlaceIndexesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListPlaceIndexes.html#LocationService.Paginator.ListPlaceIndexes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listplaceindexespaginator)
        """

if TYPE_CHECKING:
    _ListRouteCalculatorsPaginatorBase = AioPaginator[ListRouteCalculatorsResponseTypeDef]
else:
    _ListRouteCalculatorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRouteCalculatorsPaginator(_ListRouteCalculatorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListRouteCalculators.html#LocationService.Paginator.ListRouteCalculators)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listroutecalculatorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRouteCalculatorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRouteCalculatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListRouteCalculators.html#LocationService.Paginator.ListRouteCalculators.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listroutecalculatorspaginator)
        """

if TYPE_CHECKING:
    _ListTrackerConsumersPaginatorBase = AioPaginator[ListTrackerConsumersResponseTypeDef]
else:
    _ListTrackerConsumersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrackerConsumersPaginator(_ListTrackerConsumersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackerConsumers.html#LocationService.Paginator.ListTrackerConsumers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listtrackerconsumerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrackerConsumersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrackerConsumersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackerConsumers.html#LocationService.Paginator.ListTrackerConsumers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listtrackerconsumerspaginator)
        """

if TYPE_CHECKING:
    _ListTrackersPaginatorBase = AioPaginator[ListTrackersResponseTypeDef]
else:
    _ListTrackersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrackersPaginator(_ListTrackersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackers.html#LocationService.Paginator.ListTrackers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listtrackerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrackersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrackersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/paginator/ListTrackers.html#LocationService.Paginator.ListTrackers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/paginators/#listtrackerspaginator)
        """
