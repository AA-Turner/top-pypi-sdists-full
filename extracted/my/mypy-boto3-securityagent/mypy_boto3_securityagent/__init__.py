"""
Main interface for securityagent service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_securityagent import (
        Client,
        ListAgentSpacesPaginator,
        ListApplicationsPaginator,
        ListArtifactsPaginator,
        ListCodeReviewJobTasksPaginator,
        ListCodeReviewJobsForCodeReviewPaginator,
        ListCodeReviewsPaginator,
        ListDiscoveredEndpointsPaginator,
        ListFindingsPaginator,
        ListIntegratedResourcesPaginator,
        ListIntegrationsPaginator,
        ListMembershipsPaginator,
        ListPentestJobTasksPaginator,
        ListPentestJobsForPentestPaginator,
        ListPentestsPaginator,
        ListPrivateConnectionsPaginator,
        ListSecurityRequirementPacksPaginator,
        ListSecurityRequirementsPaginator,
        ListTargetDomainsPaginator,
        ListThreatModelJobTasksPaginator,
        ListThreatModelJobsPaginator,
        ListThreatModelsPaginator,
        ListThreatsPaginator,
        SecurityAgentClient,
    )

    session = Session()
    client: SecurityAgentClient = session.client("securityagent")

    list_agent_spaces_paginator: ListAgentSpacesPaginator = client.get_paginator("list_agent_spaces")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
    list_code_review_job_tasks_paginator: ListCodeReviewJobTasksPaginator = client.get_paginator("list_code_review_job_tasks")
    list_code_review_jobs_for_code_review_paginator: ListCodeReviewJobsForCodeReviewPaginator = client.get_paginator("list_code_review_jobs_for_code_review")
    list_code_reviews_paginator: ListCodeReviewsPaginator = client.get_paginator("list_code_reviews")
    list_discovered_endpoints_paginator: ListDiscoveredEndpointsPaginator = client.get_paginator("list_discovered_endpoints")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_integrated_resources_paginator: ListIntegratedResourcesPaginator = client.get_paginator("list_integrated_resources")
    list_integrations_paginator: ListIntegrationsPaginator = client.get_paginator("list_integrations")
    list_memberships_paginator: ListMembershipsPaginator = client.get_paginator("list_memberships")
    list_pentest_job_tasks_paginator: ListPentestJobTasksPaginator = client.get_paginator("list_pentest_job_tasks")
    list_pentest_jobs_for_pentest_paginator: ListPentestJobsForPentestPaginator = client.get_paginator("list_pentest_jobs_for_pentest")
    list_pentests_paginator: ListPentestsPaginator = client.get_paginator("list_pentests")
    list_private_connections_paginator: ListPrivateConnectionsPaginator = client.get_paginator("list_private_connections")
    list_security_requirement_packs_paginator: ListSecurityRequirementPacksPaginator = client.get_paginator("list_security_requirement_packs")
    list_security_requirements_paginator: ListSecurityRequirementsPaginator = client.get_paginator("list_security_requirements")
    list_target_domains_paginator: ListTargetDomainsPaginator = client.get_paginator("list_target_domains")
    list_threat_model_job_tasks_paginator: ListThreatModelJobTasksPaginator = client.get_paginator("list_threat_model_job_tasks")
    list_threat_model_jobs_paginator: ListThreatModelJobsPaginator = client.get_paginator("list_threat_model_jobs")
    list_threat_models_paginator: ListThreatModelsPaginator = client.get_paginator("list_threat_models")
    list_threats_paginator: ListThreatsPaginator = client.get_paginator("list_threats")
    ```
"""

from .client import SecurityAgentClient
from .paginator import (
    ListAgentSpacesPaginator,
    ListApplicationsPaginator,
    ListArtifactsPaginator,
    ListCodeReviewJobsForCodeReviewPaginator,
    ListCodeReviewJobTasksPaginator,
    ListCodeReviewsPaginator,
    ListDiscoveredEndpointsPaginator,
    ListFindingsPaginator,
    ListIntegratedResourcesPaginator,
    ListIntegrationsPaginator,
    ListMembershipsPaginator,
    ListPentestJobsForPentestPaginator,
    ListPentestJobTasksPaginator,
    ListPentestsPaginator,
    ListPrivateConnectionsPaginator,
    ListSecurityRequirementPacksPaginator,
    ListSecurityRequirementsPaginator,
    ListTargetDomainsPaginator,
    ListThreatModelJobsPaginator,
    ListThreatModelJobTasksPaginator,
    ListThreatModelsPaginator,
    ListThreatsPaginator,
)

Client = SecurityAgentClient


__all__ = (
    "Client",
    "ListAgentSpacesPaginator",
    "ListApplicationsPaginator",
    "ListArtifactsPaginator",
    "ListCodeReviewJobTasksPaginator",
    "ListCodeReviewJobsForCodeReviewPaginator",
    "ListCodeReviewsPaginator",
    "ListDiscoveredEndpointsPaginator",
    "ListFindingsPaginator",
    "ListIntegratedResourcesPaginator",
    "ListIntegrationsPaginator",
    "ListMembershipsPaginator",
    "ListPentestJobTasksPaginator",
    "ListPentestJobsForPentestPaginator",
    "ListPentestsPaginator",
    "ListPrivateConnectionsPaginator",
    "ListSecurityRequirementPacksPaginator",
    "ListSecurityRequirementsPaginator",
    "ListTargetDomainsPaginator",
    "ListThreatModelJobTasksPaginator",
    "ListThreatModelJobsPaginator",
    "ListThreatModelsPaginator",
    "ListThreatsPaginator",
    "SecurityAgentClient",
)
