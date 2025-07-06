"""
Main interface for arc-zonal-shift service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_arc_zonal_shift import (
        ARCZonalShiftClient,
        Client,
        ListAutoshiftsPaginator,
        ListManagedResourcesPaginator,
        ListZonalShiftsPaginator,
    )

    session = get_session()
    async with session.create_client("arc-zonal-shift") as client:
        client: ARCZonalShiftClient
        ...


    list_autoshifts_paginator: ListAutoshiftsPaginator = client.get_paginator("list_autoshifts")
    list_managed_resources_paginator: ListManagedResourcesPaginator = client.get_paginator("list_managed_resources")
    list_zonal_shifts_paginator: ListZonalShiftsPaginator = client.get_paginator("list_zonal_shifts")
    ```
"""

from .client import ARCZonalShiftClient
from .paginator import (
    ListAutoshiftsPaginator,
    ListManagedResourcesPaginator,
    ListZonalShiftsPaginator,
)

Client = ARCZonalShiftClient


__all__ = (
    "ARCZonalShiftClient",
    "Client",
    "ListAutoshiftsPaginator",
    "ListManagedResourcesPaginator",
    "ListZonalShiftsPaginator",
)
