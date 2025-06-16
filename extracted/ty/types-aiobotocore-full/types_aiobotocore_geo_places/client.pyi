"""
Type annotations for geo-places service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_geo_places.client import LocationServicePlacesV2Client

    session = get_session()
    async with session.create_client("geo-places") as client:
        client: LocationServicePlacesV2Client
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
    AutocompleteRequestTypeDef,
    AutocompleteResponseTypeDef,
    GeocodeRequestTypeDef,
    GeocodeResponseTypeDef,
    GetPlaceRequestTypeDef,
    GetPlaceResponseTypeDef,
    ReverseGeocodeRequestTypeDef,
    ReverseGeocodeResponseTypeDef,
    SearchNearbyRequestTypeDef,
    SearchNearbyResponseTypeDef,
    SearchTextRequestTypeDef,
    SearchTextResponseTypeDef,
    SuggestRequestTypeDef,
    SuggestResponseTypeDef,
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

__all__ = ("LocationServicePlacesV2Client",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LocationServicePlacesV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServicePlacesV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#generate_presigned_url)
        """

    async def autocomplete(
        self, **kwargs: Unpack[AutocompleteRequestTypeDef]
    ) -> AutocompleteResponseTypeDef:
        """
        The autocomplete operation speeds up and increases the accuracy of entering
        addresses by providing a list of address candidates matching a partially
        entered address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/autocomplete.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#autocomplete)
        """

    async def geocode(self, **kwargs: Unpack[GeocodeRequestTypeDef]) -> GeocodeResponseTypeDef:
        """
        The <code>Geocode</code> action allows you to obtain coordinates, addresses,
        and other information about places.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/geocode.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#geocode)
        """

    async def get_place(self, **kwargs: Unpack[GetPlaceRequestTypeDef]) -> GetPlaceResponseTypeDef:
        """
        Finds a place by its unique ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/get_place.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#get_place)
        """

    async def reverse_geocode(
        self, **kwargs: Unpack[ReverseGeocodeRequestTypeDef]
    ) -> ReverseGeocodeResponseTypeDef:
        """
        The <code>ReverseGeocode</code> operation allows you to retrieve addresses and
        place information from coordinates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/reverse_geocode.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#reverse_geocode)
        """

    async def search_nearby(
        self, **kwargs: Unpack[SearchNearbyRequestTypeDef]
    ) -> SearchNearbyResponseTypeDef:
        """
        Search nearby a specified location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/search_nearby.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#search_nearby)
        """

    async def search_text(
        self, **kwargs: Unpack[SearchTextRequestTypeDef]
    ) -> SearchTextResponseTypeDef:
        """
        Use the <code>SearchText</code> operation to search for geocode and place
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/search_text.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#search_text)
        """

    async def suggest(self, **kwargs: Unpack[SuggestRequestTypeDef]) -> SuggestResponseTypeDef:
        """
        The <code>Suggest</code> operation finds addresses or place candidates based on
        incomplete or misspelled queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/suggest.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/#suggest)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html#LocationServicePlacesV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/client/)
        """
