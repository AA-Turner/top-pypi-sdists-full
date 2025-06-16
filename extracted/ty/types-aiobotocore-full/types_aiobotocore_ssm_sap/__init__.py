"""
Main interface for ssm-sap service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm_sap import (
        Client,
        ListApplicationsPaginator,
        ListComponentsPaginator,
        ListDatabasesPaginator,
        ListOperationEventsPaginator,
        ListOperationsPaginator,
        SsmSapClient,
    )

    session = get_session()
    async with session.create_client("ssm-sap") as client:
        client: SsmSapClient
        ...


    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
    list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
    list_operation_events_paginator: ListOperationEventsPaginator = client.get_paginator("list_operation_events")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    ```
"""

from .client import SsmSapClient
from .paginator import (
    ListApplicationsPaginator,
    ListComponentsPaginator,
    ListDatabasesPaginator,
    ListOperationEventsPaginator,
    ListOperationsPaginator,
)

Client = SsmSapClient


__all__ = (
    "Client",
    "ListApplicationsPaginator",
    "ListComponentsPaginator",
    "ListDatabasesPaginator",
    "ListOperationEventsPaginator",
    "ListOperationsPaginator",
    "SsmSapClient",
)
