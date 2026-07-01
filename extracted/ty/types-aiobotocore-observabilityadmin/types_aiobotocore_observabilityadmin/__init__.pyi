"""
Main interface for observabilityadmin service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_observabilityadmin import (
        Client,
        CloudWatchObservabilityAdminServiceClient,
        ListCentralizationRulesForOrganizationPaginator,
        ListResourceTelemetryForOrganizationPaginator,
        ListResourceTelemetryPaginator,
        ListS3TableIntegrationsPaginator,
        ListTelemetryPipelinesPaginator,
        ListTelemetryRulesForOrganizationPaginator,
        ListTelemetryRulesPaginator,
    )

    session = get_session()
    async with session.create_client("observabilityadmin") as client:
        client: CloudWatchObservabilityAdminServiceClient
        ...


    list_centralization_rules_for_organization_paginator: ListCentralizationRulesForOrganizationPaginator = client.get_paginator("list_centralization_rules_for_organization")
    list_resource_telemetry_for_organization_paginator: ListResourceTelemetryForOrganizationPaginator = client.get_paginator("list_resource_telemetry_for_organization")
    list_resource_telemetry_paginator: ListResourceTelemetryPaginator = client.get_paginator("list_resource_telemetry")
    list_s3_table_integrations_paginator: ListS3TableIntegrationsPaginator = client.get_paginator("list_s3_table_integrations")
    list_telemetry_pipelines_paginator: ListTelemetryPipelinesPaginator = client.get_paginator("list_telemetry_pipelines")
    list_telemetry_rules_for_organization_paginator: ListTelemetryRulesForOrganizationPaginator = client.get_paginator("list_telemetry_rules_for_organization")
    list_telemetry_rules_paginator: ListTelemetryRulesPaginator = client.get_paginator("list_telemetry_rules")
    ```
"""

from .client import CloudWatchObservabilityAdminServiceClient
from .paginator import (
    ListCentralizationRulesForOrganizationPaginator,
    ListResourceTelemetryForOrganizationPaginator,
    ListResourceTelemetryPaginator,
    ListS3TableIntegrationsPaginator,
    ListTelemetryPipelinesPaginator,
    ListTelemetryRulesForOrganizationPaginator,
    ListTelemetryRulesPaginator,
)

Client = CloudWatchObservabilityAdminServiceClient

__all__ = (
    "Client",
    "CloudWatchObservabilityAdminServiceClient",
    "ListCentralizationRulesForOrganizationPaginator",
    "ListResourceTelemetryForOrganizationPaginator",
    "ListResourceTelemetryPaginator",
    "ListS3TableIntegrationsPaginator",
    "ListTelemetryPipelinesPaginator",
    "ListTelemetryRulesForOrganizationPaginator",
    "ListTelemetryRulesPaginator",
)
