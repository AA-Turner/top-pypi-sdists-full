"""
Main interface for geo-maps service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_geo_maps import (
        Client,
        LocationServiceMapsV2Client,
    )

    session = get_session()
    async with session.create_client("geo-maps") as client:
        client: LocationServiceMapsV2Client
        ...

    ```
"""

from .client import LocationServiceMapsV2Client

Client = LocationServiceMapsV2Client

__all__ = ("Client", "LocationServiceMapsV2Client")
