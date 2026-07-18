"""
Type annotations for securityagent service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_securityagent.client import SecurityAgentClient
    from types_aiobotocore_securityagent.paginator import (
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
    )

    session = get_session()
    with session.create_client("securityagent") as client:
        client: SecurityAgentClient

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

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAgentSpacesInputPaginateTypeDef,
    ListAgentSpacesOutputTypeDef,
    ListApplicationsRequestPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListArtifactsInputPaginateTypeDef,
    ListArtifactsOutputTypeDef,
    ListCodeReviewJobsForCodeReviewInputPaginateTypeDef,
    ListCodeReviewJobsForCodeReviewOutputTypeDef,
    ListCodeReviewJobTasksInputPaginateTypeDef,
    ListCodeReviewJobTasksOutputTypeDef,
    ListCodeReviewsInputPaginateTypeDef,
    ListCodeReviewsOutputTypeDef,
    ListDiscoveredEndpointsInputPaginateTypeDef,
    ListDiscoveredEndpointsOutputTypeDef,
    ListFindingsInputPaginateTypeDef,
    ListFindingsOutputTypeDef,
    ListIntegratedResourcesInputPaginateTypeDef,
    ListIntegratedResourcesOutputTypeDef,
    ListIntegrationsInputPaginateTypeDef,
    ListIntegrationsOutputTypeDef,
    ListMembershipsRequestPaginateTypeDef,
    ListMembershipsResponseTypeDef,
    ListPentestJobsForPentestInputPaginateTypeDef,
    ListPentestJobsForPentestOutputTypeDef,
    ListPentestJobTasksInputPaginateTypeDef,
    ListPentestJobTasksOutputTypeDef,
    ListPentestsInputPaginateTypeDef,
    ListPentestsOutputTypeDef,
    ListPrivateConnectionsInputPaginateTypeDef,
    ListPrivateConnectionsOutputTypeDef,
    ListSecurityRequirementPacksInputPaginateTypeDef,
    ListSecurityRequirementPacksOutputTypeDef,
    ListSecurityRequirementsInputPaginateTypeDef,
    ListSecurityRequirementsOutputTypeDef,
    ListTargetDomainsInputPaginateTypeDef,
    ListTargetDomainsOutputTypeDef,
    ListThreatModelJobsInputPaginateTypeDef,
    ListThreatModelJobsOutputTypeDef,
    ListThreatModelJobTasksInputPaginateTypeDef,
    ListThreatModelJobTasksOutputTypeDef,
    ListThreatModelsInputPaginateTypeDef,
    ListThreatModelsOutputTypeDef,
    ListThreatsInputPaginateTypeDef,
    ListThreatsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
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
)


if TYPE_CHECKING:
    _ListAgentSpacesPaginatorBase = AioPaginator[ListAgentSpacesOutputTypeDef]
else:
    _ListAgentSpacesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAgentSpacesPaginator(_ListAgentSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListAgentSpaces.html#SecurityAgent.Paginator.ListAgentSpaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listagentspacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentSpacesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAgentSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListAgentSpaces.html#SecurityAgent.Paginator.ListAgentSpaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listagentspacespaginator)
        """


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListApplications.html#SecurityAgent.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListApplications.html#SecurityAgent.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListArtifactsPaginatorBase = AioPaginator[ListArtifactsOutputTypeDef]
else:
    _ListArtifactsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListArtifactsPaginator(_ListArtifactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListArtifacts.html#SecurityAgent.Paginator.ListArtifacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listartifactspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArtifactsInputPaginateTypeDef]
    ) -> AioPageIterator[ListArtifactsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListArtifacts.html#SecurityAgent.Paginator.ListArtifacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listartifactspaginator)
        """


if TYPE_CHECKING:
    _ListCodeReviewJobTasksPaginatorBase = AioPaginator[ListCodeReviewJobTasksOutputTypeDef]
else:
    _ListCodeReviewJobTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCodeReviewJobTasksPaginator(_ListCodeReviewJobTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviewJobTasks.html#SecurityAgent.Paginator.ListCodeReviewJobTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listcodereviewjobtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeReviewJobTasksInputPaginateTypeDef]
    ) -> AioPageIterator[ListCodeReviewJobTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviewJobTasks.html#SecurityAgent.Paginator.ListCodeReviewJobTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listcodereviewjobtaskspaginator)
        """


if TYPE_CHECKING:
    _ListCodeReviewJobsForCodeReviewPaginatorBase = AioPaginator[
        ListCodeReviewJobsForCodeReviewOutputTypeDef
    ]
else:
    _ListCodeReviewJobsForCodeReviewPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCodeReviewJobsForCodeReviewPaginator(_ListCodeReviewJobsForCodeReviewPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviewJobsForCodeReview.html#SecurityAgent.Paginator.ListCodeReviewJobsForCodeReview)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listcodereviewjobsforcodereviewpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeReviewJobsForCodeReviewInputPaginateTypeDef]
    ) -> AioPageIterator[ListCodeReviewJobsForCodeReviewOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviewJobsForCodeReview.html#SecurityAgent.Paginator.ListCodeReviewJobsForCodeReview.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listcodereviewjobsforcodereviewpaginator)
        """


if TYPE_CHECKING:
    _ListCodeReviewsPaginatorBase = AioPaginator[ListCodeReviewsOutputTypeDef]
else:
    _ListCodeReviewsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCodeReviewsPaginator(_ListCodeReviewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviews.html#SecurityAgent.Paginator.ListCodeReviews)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listcodereviewspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeReviewsInputPaginateTypeDef]
    ) -> AioPageIterator[ListCodeReviewsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviews.html#SecurityAgent.Paginator.ListCodeReviews.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listcodereviewspaginator)
        """


if TYPE_CHECKING:
    _ListDiscoveredEndpointsPaginatorBase = AioPaginator[ListDiscoveredEndpointsOutputTypeDef]
else:
    _ListDiscoveredEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDiscoveredEndpointsPaginator(_ListDiscoveredEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListDiscoveredEndpoints.html#SecurityAgent.Paginator.ListDiscoveredEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listdiscoveredendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDiscoveredEndpointsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDiscoveredEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListDiscoveredEndpoints.html#SecurityAgent.Paginator.ListDiscoveredEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listdiscoveredendpointspaginator)
        """


if TYPE_CHECKING:
    _ListFindingsPaginatorBase = AioPaginator[ListFindingsOutputTypeDef]
else:
    _ListFindingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFindingsPaginator(_ListFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListFindings.html#SecurityAgent.Paginator.ListFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listfindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingsInputPaginateTypeDef]
    ) -> AioPageIterator[ListFindingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListFindings.html#SecurityAgent.Paginator.ListFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listfindingspaginator)
        """


if TYPE_CHECKING:
    _ListIntegratedResourcesPaginatorBase = AioPaginator[ListIntegratedResourcesOutputTypeDef]
else:
    _ListIntegratedResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIntegratedResourcesPaginator(_ListIntegratedResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegratedResources.html#SecurityAgent.Paginator.ListIntegratedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listintegratedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegratedResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListIntegratedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegratedResources.html#SecurityAgent.Paginator.ListIntegratedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listintegratedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListIntegrationsPaginatorBase = AioPaginator[ListIntegrationsOutputTypeDef]
else:
    _ListIntegrationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIntegrationsPaginator(_ListIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegrations.html#SecurityAgent.Paginator.ListIntegrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listintegrationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegrationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListIntegrationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegrations.html#SecurityAgent.Paginator.ListIntegrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listintegrationspaginator)
        """


if TYPE_CHECKING:
    _ListMembershipsPaginatorBase = AioPaginator[ListMembershipsResponseTypeDef]
else:
    _ListMembershipsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMembershipsPaginator(_ListMembershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListMemberships.html#SecurityAgent.Paginator.ListMemberships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listmembershipspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMembershipsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListMemberships.html#SecurityAgent.Paginator.ListMemberships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listmembershipspaginator)
        """


if TYPE_CHECKING:
    _ListPentestJobTasksPaginatorBase = AioPaginator[ListPentestJobTasksOutputTypeDef]
else:
    _ListPentestJobTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPentestJobTasksPaginator(_ListPentestJobTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobTasks.html#SecurityAgent.Paginator.ListPentestJobTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listpentestjobtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPentestJobTasksInputPaginateTypeDef]
    ) -> AioPageIterator[ListPentestJobTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobTasks.html#SecurityAgent.Paginator.ListPentestJobTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listpentestjobtaskspaginator)
        """


if TYPE_CHECKING:
    _ListPentestJobsForPentestPaginatorBase = AioPaginator[ListPentestJobsForPentestOutputTypeDef]
else:
    _ListPentestJobsForPentestPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPentestJobsForPentestPaginator(_ListPentestJobsForPentestPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobsForPentest.html#SecurityAgent.Paginator.ListPentestJobsForPentest)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listpentestjobsforpentestpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPentestJobsForPentestInputPaginateTypeDef]
    ) -> AioPageIterator[ListPentestJobsForPentestOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobsForPentest.html#SecurityAgent.Paginator.ListPentestJobsForPentest.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listpentestjobsforpentestpaginator)
        """


if TYPE_CHECKING:
    _ListPentestsPaginatorBase = AioPaginator[ListPentestsOutputTypeDef]
else:
    _ListPentestsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPentestsPaginator(_ListPentestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentests.html#SecurityAgent.Paginator.ListPentests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listpentestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPentestsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPentestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentests.html#SecurityAgent.Paginator.ListPentests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listpentestspaginator)
        """


if TYPE_CHECKING:
    _ListPrivateConnectionsPaginatorBase = AioPaginator[ListPrivateConnectionsOutputTypeDef]
else:
    _ListPrivateConnectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPrivateConnectionsPaginator(_ListPrivateConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPrivateConnections.html#SecurityAgent.Paginator.ListPrivateConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listprivateconnectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrivateConnectionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPrivateConnectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPrivateConnections.html#SecurityAgent.Paginator.ListPrivateConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listprivateconnectionspaginator)
        """


if TYPE_CHECKING:
    _ListSecurityRequirementPacksPaginatorBase = AioPaginator[
        ListSecurityRequirementPacksOutputTypeDef
    ]
else:
    _ListSecurityRequirementPacksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSecurityRequirementPacksPaginator(_ListSecurityRequirementPacksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListSecurityRequirementPacks.html#SecurityAgent.Paginator.ListSecurityRequirementPacks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listsecurityrequirementpackspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityRequirementPacksInputPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityRequirementPacksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListSecurityRequirementPacks.html#SecurityAgent.Paginator.ListSecurityRequirementPacks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listsecurityrequirementpackspaginator)
        """


if TYPE_CHECKING:
    _ListSecurityRequirementsPaginatorBase = AioPaginator[ListSecurityRequirementsOutputTypeDef]
else:
    _ListSecurityRequirementsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSecurityRequirementsPaginator(_ListSecurityRequirementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListSecurityRequirements.html#SecurityAgent.Paginator.ListSecurityRequirements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listsecurityrequirementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityRequirementsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityRequirementsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListSecurityRequirements.html#SecurityAgent.Paginator.ListSecurityRequirements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listsecurityrequirementspaginator)
        """


if TYPE_CHECKING:
    _ListTargetDomainsPaginatorBase = AioPaginator[ListTargetDomainsOutputTypeDef]
else:
    _ListTargetDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTargetDomainsPaginator(_ListTargetDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListTargetDomains.html#SecurityAgent.Paginator.ListTargetDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listtargetdomainspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetDomainsInputPaginateTypeDef]
    ) -> AioPageIterator[ListTargetDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListTargetDomains.html#SecurityAgent.Paginator.ListTargetDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listtargetdomainspaginator)
        """


if TYPE_CHECKING:
    _ListThreatModelJobTasksPaginatorBase = AioPaginator[ListThreatModelJobTasksOutputTypeDef]
else:
    _ListThreatModelJobTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThreatModelJobTasksPaginator(_ListThreatModelJobTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModelJobTasks.html#SecurityAgent.Paginator.ListThreatModelJobTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listthreatmodeljobtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThreatModelJobTasksInputPaginateTypeDef]
    ) -> AioPageIterator[ListThreatModelJobTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModelJobTasks.html#SecurityAgent.Paginator.ListThreatModelJobTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listthreatmodeljobtaskspaginator)
        """


if TYPE_CHECKING:
    _ListThreatModelJobsPaginatorBase = AioPaginator[ListThreatModelJobsOutputTypeDef]
else:
    _ListThreatModelJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThreatModelJobsPaginator(_ListThreatModelJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModelJobs.html#SecurityAgent.Paginator.ListThreatModelJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listthreatmodeljobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThreatModelJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListThreatModelJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModelJobs.html#SecurityAgent.Paginator.ListThreatModelJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listthreatmodeljobspaginator)
        """


if TYPE_CHECKING:
    _ListThreatModelsPaginatorBase = AioPaginator[ListThreatModelsOutputTypeDef]
else:
    _ListThreatModelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThreatModelsPaginator(_ListThreatModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModels.html#SecurityAgent.Paginator.ListThreatModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listthreatmodelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThreatModelsInputPaginateTypeDef]
    ) -> AioPageIterator[ListThreatModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModels.html#SecurityAgent.Paginator.ListThreatModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listthreatmodelspaginator)
        """


if TYPE_CHECKING:
    _ListThreatsPaginatorBase = AioPaginator[ListThreatsOutputTypeDef]
else:
    _ListThreatsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThreatsPaginator(_ListThreatsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreats.html#SecurityAgent.Paginator.ListThreats)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listthreatspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThreatsInputPaginateTypeDef]
    ) -> AioPageIterator[ListThreatsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreats.html#SecurityAgent.Paginator.ListThreats.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityagent/paginators/#listthreatspaginator)
        """
