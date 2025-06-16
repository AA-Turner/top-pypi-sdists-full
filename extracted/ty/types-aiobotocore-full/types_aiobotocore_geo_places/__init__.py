"""
Main interface for geo-places service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_places/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_geo_places import (
        Client,
        LocationServicePlacesV2Client,
    )

    session = get_session()
    async with session.create_client("geo-places") as client:
        client: LocationServicePlacesV2Client
        ...

    ```
"""

from .client import LocationServicePlacesV2Client

Client = LocationServicePlacesV2Client


__all__ = ("Client", "LocationServicePlacesV2Client")
