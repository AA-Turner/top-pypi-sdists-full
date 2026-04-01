"""
Main interface for securityagent service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_securityagent/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_securityagent import (
        Client,
        ListAgentSpacesPaginator,
        ListApplicationsPaginator,
        ListArtifactsPaginator,
        ListDiscoveredEndpointsPaginator,
        ListFindingsPaginator,
        ListIntegratedResourcesPaginator,
        ListIntegrationsPaginator,
        ListMembershipsPaginator,
        ListPentestJobTasksPaginator,
        ListPentestJobsForPentestPaginator,
        ListPentestsPaginator,
        ListTargetDomainsPaginator,
        SecurityAgentClient,
    )

    session = Session()
    client: SecurityAgentClient = session.client("securityagent")

    list_agent_spaces_paginator: ListAgentSpacesPaginator = client.get_paginator("list_agent_spaces")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
    list_discovered_endpoints_paginator: ListDiscoveredEndpointsPaginator = client.get_paginator("list_discovered_endpoints")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_integrated_resources_paginator: ListIntegratedResourcesPaginator = client.get_paginator("list_integrated_resources")
    list_integrations_paginator: ListIntegrationsPaginator = client.get_paginator("list_integrations")
    list_memberships_paginator: ListMembershipsPaginator = client.get_paginator("list_memberships")
    list_pentest_job_tasks_paginator: ListPentestJobTasksPaginator = client.get_paginator("list_pentest_job_tasks")
    list_pentest_jobs_for_pentest_paginator: ListPentestJobsForPentestPaginator = client.get_paginator("list_pentest_jobs_for_pentest")
    list_pentests_paginator: ListPentestsPaginator = client.get_paginator("list_pentests")
    list_target_domains_paginator: ListTargetDomainsPaginator = client.get_paginator("list_target_domains")
    ```
"""

from .client import SecurityAgentClient
from .paginator import (
    ListAgentSpacesPaginator,
    ListApplicationsPaginator,
    ListArtifactsPaginator,
    ListDiscoveredEndpointsPaginator,
    ListFindingsPaginator,
    ListIntegratedResourcesPaginator,
    ListIntegrationsPaginator,
    ListMembershipsPaginator,
    ListPentestJobsForPentestPaginator,
    ListPentestJobTasksPaginator,
    ListPentestsPaginator,
    ListTargetDomainsPaginator,
)

Client = SecurityAgentClient

__all__ = (
    "Client",
    "ListAgentSpacesPaginator",
    "ListApplicationsPaginator",
    "ListArtifactsPaginator",
    "ListDiscoveredEndpointsPaginator",
    "ListFindingsPaginator",
    "ListIntegratedResourcesPaginator",
    "ListIntegrationsPaginator",
    "ListMembershipsPaginator",
    "ListPentestJobTasksPaginator",
    "ListPentestJobsForPentestPaginator",
    "ListPentestsPaginator",
    "ListTargetDomainsPaginator",
    "SecurityAgentClient",
)
