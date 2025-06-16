"""
Type annotations for geo-routes service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_geo_routes.client import LocationServiceRoutesV2Client

    session = get_session()
    async with session.create_client("geo-routes") as client:
        client: LocationServiceRoutesV2Client
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CalculateIsolinesRequestTypeDef,
    CalculateIsolinesResponseTypeDef,
    CalculateRouteMatrixRequestTypeDef,
    CalculateRouteMatrixResponseTypeDef,
    CalculateRoutesRequestTypeDef,
    CalculateRoutesResponseTypeDef,
    OptimizeWaypointsRequestTypeDef,
    OptimizeWaypointsResponseTypeDef,
    SnapToRoadsRequestTypeDef,
    SnapToRoadsResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("LocationServiceRoutesV2Client",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LocationServiceRoutesV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServiceRoutesV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/#generate_presigned_url)
        """

    async def calculate_isolines(
        self, **kwargs: Unpack[CalculateIsolinesRequestTypeDef]
    ) -> CalculateIsolinesResponseTypeDef:
        """
        Use the <code>CalculateIsolines</code> action to find service areas that can be
        reached in a given threshold of time, distance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/calculate_isolines.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/#calculate_isolines)
        """

    async def calculate_route_matrix(
        self, **kwargs: Unpack[CalculateRouteMatrixRequestTypeDef]
    ) -> CalculateRouteMatrixResponseTypeDef:
        """
        Use <code>CalculateRouteMatrix</code> to compute results for all pairs of
        Origins to Destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/calculate_route_matrix.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/#calculate_route_matrix)
        """

    async def calculate_routes(
        self, **kwargs: Unpack[CalculateRoutesRequestTypeDef]
    ) -> CalculateRoutesResponseTypeDef:
        """
        <code>CalculateRoutes</code> computes routes given the following required
        parameters: <code>Origin</code> and <code>Destination</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/calculate_routes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/#calculate_routes)
        """

    async def optimize_waypoints(
        self, **kwargs: Unpack[OptimizeWaypointsRequestTypeDef]
    ) -> OptimizeWaypointsResponseTypeDef:
        """
        <code>OptimizeWaypoints</code> calculates the optimal order to travel between a
        set of waypoints to minimize either the travel time or the distance travelled
        during the journey, based on road network restrictions and the traffic pattern
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/optimize_waypoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/#optimize_waypoints)
        """

    async def snap_to_roads(
        self, **kwargs: Unpack[SnapToRoadsRequestTypeDef]
    ) -> SnapToRoadsResponseTypeDef:
        """
        <code>SnapToRoads</code> matches GPS trace to roads most likely traveled on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes/client/snap_to_roads.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/#snap_to_roads)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-routes.html#LocationServiceRoutesV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/client/)
        """
