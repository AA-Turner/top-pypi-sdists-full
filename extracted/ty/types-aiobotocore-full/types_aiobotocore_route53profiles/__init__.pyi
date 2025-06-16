"""
Main interface for route53profiles service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53profiles import (
        Client,
        ListProfileAssociationsPaginator,
        ListProfileResourceAssociationsPaginator,
        ListProfilesPaginator,
        Route53ProfilesClient,
    )

    session = get_session()
    async with session.create_client("route53profiles") as client:
        client: Route53ProfilesClient
        ...


    list_profile_associations_paginator: ListProfileAssociationsPaginator = client.get_paginator("list_profile_associations")
    list_profile_resource_associations_paginator: ListProfileResourceAssociationsPaginator = client.get_paginator("list_profile_resource_associations")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    ```
"""

from .client import Route53ProfilesClient
from .paginator import (
    ListProfileAssociationsPaginator,
    ListProfileResourceAssociationsPaginator,
    ListProfilesPaginator,
)

Client = Route53ProfilesClient

__all__ = (
    "Client",
    "ListProfileAssociationsPaginator",
    "ListProfileResourceAssociationsPaginator",
    "ListProfilesPaginator",
    "Route53ProfilesClient",
)
