"""
Main interface for cloudwatchomni service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatchomni/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudwatchomni import (
        Client,
        CloudWatchOmniClient,
        GetContextGraphPaginator,
        GetTelemetryQueryResultsPaginator,
        ListAccessGrantsPaginator,
        ListAccessProfilesPaginator,
        ListAlertsPaginator,
        ListDomainAccessGrantsForOrganizationPaginator,
        ListDomainsPaginator,
        ListIntegrationsPaginator,
        ListOmniDashboardsPaginator,
        ListSpacesForOrganizationPaginator,
        ListSpacesPaginator,
        ListTelemetryFieldsPaginator,
        ListTelemetryQuerySessionsPaginator,
        ListViewsPaginator,
        SearchPrincipalsPaginator,
    )

    session = Session()
    client: CloudWatchOmniClient = session.client("cloudwatchomni")

    get_context_graph_paginator: GetContextGraphPaginator = client.get_paginator("get_context_graph")
    get_telemetry_query_results_paginator: GetTelemetryQueryResultsPaginator = client.get_paginator("get_telemetry_query_results")
    list_access_grants_paginator: ListAccessGrantsPaginator = client.get_paginator("list_access_grants")
    list_access_profiles_paginator: ListAccessProfilesPaginator = client.get_paginator("list_access_profiles")
    list_alerts_paginator: ListAlertsPaginator = client.get_paginator("list_alerts")
    list_domain_access_grants_for_organization_paginator: ListDomainAccessGrantsForOrganizationPaginator = client.get_paginator("list_domain_access_grants_for_organization")
    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_integrations_paginator: ListIntegrationsPaginator = client.get_paginator("list_integrations")
    list_omni_dashboards_paginator: ListOmniDashboardsPaginator = client.get_paginator("list_omni_dashboards")
    list_spaces_for_organization_paginator: ListSpacesForOrganizationPaginator = client.get_paginator("list_spaces_for_organization")
    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    list_telemetry_fields_paginator: ListTelemetryFieldsPaginator = client.get_paginator("list_telemetry_fields")
    list_telemetry_query_sessions_paginator: ListTelemetryQuerySessionsPaginator = client.get_paginator("list_telemetry_query_sessions")
    list_views_paginator: ListViewsPaginator = client.get_paginator("list_views")
    search_principals_paginator: SearchPrincipalsPaginator = client.get_paginator("search_principals")
    ```
"""

from .client import CloudWatchOmniClient
from .paginator import (
    GetContextGraphPaginator,
    GetTelemetryQueryResultsPaginator,
    ListAccessGrantsPaginator,
    ListAccessProfilesPaginator,
    ListAlertsPaginator,
    ListDomainAccessGrantsForOrganizationPaginator,
    ListDomainsPaginator,
    ListIntegrationsPaginator,
    ListOmniDashboardsPaginator,
    ListSpacesForOrganizationPaginator,
    ListSpacesPaginator,
    ListTelemetryFieldsPaginator,
    ListTelemetryQuerySessionsPaginator,
    ListViewsPaginator,
    SearchPrincipalsPaginator,
)

Client = CloudWatchOmniClient


__all__ = (
    "Client",
    "CloudWatchOmniClient",
    "GetContextGraphPaginator",
    "GetTelemetryQueryResultsPaginator",
    "ListAccessGrantsPaginator",
    "ListAccessProfilesPaginator",
    "ListAlertsPaginator",
    "ListDomainAccessGrantsForOrganizationPaginator",
    "ListDomainsPaginator",
    "ListIntegrationsPaginator",
    "ListOmniDashboardsPaginator",
    "ListSpacesForOrganizationPaginator",
    "ListSpacesPaginator",
    "ListTelemetryFieldsPaginator",
    "ListTelemetryQuerySessionsPaginator",
    "ListViewsPaginator",
    "SearchPrincipalsPaginator",
)
