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
        ListReputationEntitiesPaginator,
        ListResourceTenantsPaginator,
        ListTenantResourcesPaginator,
        ListTenantsPaginator,
        SESV2Client,
    )

    session = get_session()
    async with session.create_client("sesv2") as client:
        client: SESV2Client
        ...


    list_multi_region_endpoints_paginator: ListMultiRegionEndpointsPaginator = client.get_paginator("list_multi_region_endpoints")
    list_reputation_entities_paginator: ListReputationEntitiesPaginator = client.get_paginator("list_reputation_entities")
    list_resource_tenants_paginator: ListResourceTenantsPaginator = client.get_paginator("list_resource_tenants")
    list_tenant_resources_paginator: ListTenantResourcesPaginator = client.get_paginator("list_tenant_resources")
    list_tenants_paginator: ListTenantsPaginator = client.get_paginator("list_tenants")
    ```
"""

from .client import SESV2Client
from .paginator import (
    ListMultiRegionEndpointsPaginator,
    ListReputationEntitiesPaginator,
    ListResourceTenantsPaginator,
    ListTenantResourcesPaginator,
    ListTenantsPaginator,
)

Client = SESV2Client

__all__ = (
    "Client",
    "ListMultiRegionEndpointsPaginator",
    "ListReputationEntitiesPaginator",
    "ListResourceTenantsPaginator",
    "ListTenantResourcesPaginator",
    "ListTenantsPaginator",
    "SESV2Client",
)
