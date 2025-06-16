"""
Main interface for application-signals service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_application_signals import (
        Client,
        CloudWatchApplicationSignalsClient,
        ListServiceDependenciesPaginator,
        ListServiceDependentsPaginator,
        ListServiceLevelObjectiveExclusionWindowsPaginator,
        ListServiceLevelObjectivesPaginator,
        ListServiceOperationsPaginator,
        ListServicesPaginator,
    )

    session = get_session()
    async with session.create_client("application-signals") as client:
        client: CloudWatchApplicationSignalsClient
        ...


    list_service_dependencies_paginator: ListServiceDependenciesPaginator = client.get_paginator("list_service_dependencies")
    list_service_dependents_paginator: ListServiceDependentsPaginator = client.get_paginator("list_service_dependents")
    list_service_level_objective_exclusion_windows_paginator: ListServiceLevelObjectiveExclusionWindowsPaginator = client.get_paginator("list_service_level_objective_exclusion_windows")
    list_service_level_objectives_paginator: ListServiceLevelObjectivesPaginator = client.get_paginator("list_service_level_objectives")
    list_service_operations_paginator: ListServiceOperationsPaginator = client.get_paginator("list_service_operations")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from .client import CloudWatchApplicationSignalsClient
from .paginator import (
    ListServiceDependenciesPaginator,
    ListServiceDependentsPaginator,
    ListServiceLevelObjectiveExclusionWindowsPaginator,
    ListServiceLevelObjectivesPaginator,
    ListServiceOperationsPaginator,
    ListServicesPaginator,
)

Client = CloudWatchApplicationSignalsClient

__all__ = (
    "Client",
    "CloudWatchApplicationSignalsClient",
    "ListServiceDependenciesPaginator",
    "ListServiceDependentsPaginator",
    "ListServiceLevelObjectiveExclusionWindowsPaginator",
    "ListServiceLevelObjectivesPaginator",
    "ListServiceOperationsPaginator",
    "ListServicesPaginator",
)
