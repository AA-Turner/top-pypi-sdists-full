"""
Main interface for geo-routes service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_routes/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_geo_routes import (
        Client,
        LocationServiceRoutesV2Client,
    )

    session = get_session()
    async with session.create_client("geo-routes") as client:
        client: LocationServiceRoutesV2Client
        ...

    ```
"""

from .client import LocationServiceRoutesV2Client

Client = LocationServiceRoutesV2Client

__all__ = ("Client", "LocationServiceRoutesV2Client")
