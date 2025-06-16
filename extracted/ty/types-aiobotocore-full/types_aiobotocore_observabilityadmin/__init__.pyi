"""
Main interface for observabilityadmin service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_observabilityadmin import (
        Client,
        CloudWatchObservabilityAdminServiceClient,
        ListResourceTelemetryForOrganizationPaginator,
        ListResourceTelemetryPaginator,
    )

    session = get_session()
    async with session.create_client("observabilityadmin") as client:
        client: CloudWatchObservabilityAdminServiceClient
        ...


    list_resource_telemetry_for_organization_paginator: ListResourceTelemetryForOrganizationPaginator = client.get_paginator("list_resource_telemetry_for_organization")
    list_resource_telemetry_paginator: ListResourceTelemetryPaginator = client.get_paginator("list_resource_telemetry")
    ```
"""

from .client import CloudWatchObservabilityAdminServiceClient
from .paginator import ListResourceTelemetryForOrganizationPaginator, ListResourceTelemetryPaginator

Client = CloudWatchObservabilityAdminServiceClient

__all__ = (
    "Client",
    "CloudWatchObservabilityAdminServiceClient",
    "ListResourceTelemetryForOrganizationPaginator",
    "ListResourceTelemetryPaginator",
)
