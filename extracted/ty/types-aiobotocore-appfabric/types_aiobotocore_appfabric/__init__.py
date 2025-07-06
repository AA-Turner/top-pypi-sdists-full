"""
Main interface for appfabric service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appfabric import (
        AppFabricClient,
        Client,
        ListAppAuthorizationsPaginator,
        ListAppBundlesPaginator,
        ListIngestionDestinationsPaginator,
        ListIngestionsPaginator,
    )

    session = get_session()
    async with session.create_client("appfabric") as client:
        client: AppFabricClient
        ...


    list_app_authorizations_paginator: ListAppAuthorizationsPaginator = client.get_paginator("list_app_authorizations")
    list_app_bundles_paginator: ListAppBundlesPaginator = client.get_paginator("list_app_bundles")
    list_ingestion_destinations_paginator: ListIngestionDestinationsPaginator = client.get_paginator("list_ingestion_destinations")
    list_ingestions_paginator: ListIngestionsPaginator = client.get_paginator("list_ingestions")
    ```
"""

from .client import AppFabricClient
from .paginator import (
    ListAppAuthorizationsPaginator,
    ListAppBundlesPaginator,
    ListIngestionDestinationsPaginator,
    ListIngestionsPaginator,
)

Client = AppFabricClient


__all__ = (
    "AppFabricClient",
    "Client",
    "ListAppAuthorizationsPaginator",
    "ListAppBundlesPaginator",
    "ListIngestionDestinationsPaginator",
    "ListIngestionsPaginator",
)
