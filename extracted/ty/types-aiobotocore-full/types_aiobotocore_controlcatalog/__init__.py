"""
Main interface for controlcatalog service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_controlcatalog import (
        Client,
        ControlCatalogClient,
        ListCommonControlsPaginator,
        ListControlMappingsPaginator,
        ListControlsPaginator,
        ListDomainsPaginator,
        ListObjectivesPaginator,
    )

    session = get_session()
    async with session.create_client("controlcatalog") as client:
        client: ControlCatalogClient
        ...


    list_common_controls_paginator: ListCommonControlsPaginator = client.get_paginator("list_common_controls")
    list_control_mappings_paginator: ListControlMappingsPaginator = client.get_paginator("list_control_mappings")
    list_controls_paginator: ListControlsPaginator = client.get_paginator("list_controls")
    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_objectives_paginator: ListObjectivesPaginator = client.get_paginator("list_objectives")
    ```
"""

from .client import ControlCatalogClient
from .paginator import (
    ListCommonControlsPaginator,
    ListControlMappingsPaginator,
    ListControlsPaginator,
    ListDomainsPaginator,
    ListObjectivesPaginator,
)

Client = ControlCatalogClient


__all__ = (
    "Client",
    "ControlCatalogClient",
    "ListCommonControlsPaginator",
    "ListControlMappingsPaginator",
    "ListControlsPaginator",
    "ListDomainsPaginator",
    "ListObjectivesPaginator",
)
