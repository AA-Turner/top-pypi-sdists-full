"""
Main interface for observabilityadmin service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_observabilityadmin import (
        Client,
        CloudWatchObservabilityAdminServiceClient,
        ListCentralizationRulesForOrganizationPaginator,
        ListConnectorsPaginator,
        ListDatasetIntegrationsPaginator,
        ListResourceTelemetryForOrganizationPaginator,
        ListResourceTelemetryPaginator,
        ListS3TableIntegrationsPaginator,
        ListTelemetryPipelinesPaginator,
        ListTelemetryRulesForOrganizationPaginator,
        ListTelemetryRulesPaginator,
        ListThirdPartyTelemetryEnrichmentsPaginator,
    )

    session = Session()
    client: CloudWatchObservabilityAdminServiceClient = session.client("observabilityadmin")

    list_centralization_rules_for_organization_paginator: ListCentralizationRulesForOrganizationPaginator = client.get_paginator("list_centralization_rules_for_organization")
    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    list_dataset_integrations_paginator: ListDatasetIntegrationsPaginator = client.get_paginator("list_dataset_integrations")
    list_resource_telemetry_for_organization_paginator: ListResourceTelemetryForOrganizationPaginator = client.get_paginator("list_resource_telemetry_for_organization")
    list_resource_telemetry_paginator: ListResourceTelemetryPaginator = client.get_paginator("list_resource_telemetry")
    list_s3_table_integrations_paginator: ListS3TableIntegrationsPaginator = client.get_paginator("list_s3_table_integrations")
    list_telemetry_pipelines_paginator: ListTelemetryPipelinesPaginator = client.get_paginator("list_telemetry_pipelines")
    list_telemetry_rules_for_organization_paginator: ListTelemetryRulesForOrganizationPaginator = client.get_paginator("list_telemetry_rules_for_organization")
    list_telemetry_rules_paginator: ListTelemetryRulesPaginator = client.get_paginator("list_telemetry_rules")
    list_third_party_telemetry_enrichments_paginator: ListThirdPartyTelemetryEnrichmentsPaginator = client.get_paginator("list_third_party_telemetry_enrichments")
    ```
"""

from .client import CloudWatchObservabilityAdminServiceClient
from .paginator import (
    ListCentralizationRulesForOrganizationPaginator,
    ListConnectorsPaginator,
    ListDatasetIntegrationsPaginator,
    ListResourceTelemetryForOrganizationPaginator,
    ListResourceTelemetryPaginator,
    ListS3TableIntegrationsPaginator,
    ListTelemetryPipelinesPaginator,
    ListTelemetryRulesForOrganizationPaginator,
    ListTelemetryRulesPaginator,
    ListThirdPartyTelemetryEnrichmentsPaginator,
)

Client = CloudWatchObservabilityAdminServiceClient


__all__ = (
    "Client",
    "CloudWatchObservabilityAdminServiceClient",
    "ListCentralizationRulesForOrganizationPaginator",
    "ListConnectorsPaginator",
    "ListDatasetIntegrationsPaginator",
    "ListResourceTelemetryForOrganizationPaginator",
    "ListResourceTelemetryPaginator",
    "ListS3TableIntegrationsPaginator",
    "ListTelemetryPipelinesPaginator",
    "ListTelemetryRulesForOrganizationPaginator",
    "ListTelemetryRulesPaginator",
    "ListThirdPartyTelemetryEnrichmentsPaginator",
)
