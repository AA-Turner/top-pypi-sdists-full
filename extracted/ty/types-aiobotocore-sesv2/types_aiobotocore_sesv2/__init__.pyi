"""
Main interface for sesv2 service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sesv2 import (
        Client,
        ListMultiRegionEndpointsPaginator,
        SESV2Client,
    )

    session = get_session()
    async with session.create_client("sesv2") as client:
        client: SESV2Client
        ...


    list_multi_region_endpoints_paginator: ListMultiRegionEndpointsPaginator = client.get_paginator("list_multi_region_endpoints")
    ```
"""

from .client import SESV2Client
from .paginator import ListMultiRegionEndpointsPaginator

Client = SESV2Client

__all__ = ("Client", "ListMultiRegionEndpointsPaginator", "SESV2Client")
