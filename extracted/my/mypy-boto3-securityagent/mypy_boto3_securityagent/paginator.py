"""
Type annotations for securityagent service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_securityagent.client import SecurityAgentClient
    from mypy_boto3_securityagent.paginator import (
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

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListAgentSpacesPaginatorBase = Paginator[ListAgentSpacesOutputTypeDef]
else:
    _ListAgentSpacesPaginatorBase = Paginator  # type: ignore[assignment]


class ListAgentSpacesPaginator(_ListAgentSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListAgentSpaces.html#SecurityAgent.Paginator.ListAgentSpaces)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listagentspacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentSpacesInputPaginateTypeDef]
    ) -> PageIterator[ListAgentSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListAgentSpaces.html#SecurityAgent.Paginator.ListAgentSpaces.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listagentspacespaginator)
        """


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = Paginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListApplications.html#SecurityAgent.Paginator.ListApplications)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListApplications.html#SecurityAgent.Paginator.ListApplications.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListArtifactsPaginatorBase = Paginator[ListArtifactsOutputTypeDef]
else:
    _ListArtifactsPaginatorBase = Paginator  # type: ignore[assignment]


class ListArtifactsPaginator(_ListArtifactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListArtifacts.html#SecurityAgent.Paginator.ListArtifacts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listartifactspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArtifactsInputPaginateTypeDef]
    ) -> PageIterator[ListArtifactsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListArtifacts.html#SecurityAgent.Paginator.ListArtifacts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listartifactspaginator)
        """


if TYPE_CHECKING:
    _ListCodeReviewJobTasksPaginatorBase = Paginator[ListCodeReviewJobTasksOutputTypeDef]
else:
    _ListCodeReviewJobTasksPaginatorBase = Paginator  # type: ignore[assignment]


class ListCodeReviewJobTasksPaginator(_ListCodeReviewJobTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviewJobTasks.html#SecurityAgent.Paginator.ListCodeReviewJobTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listcodereviewjobtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeReviewJobTasksInputPaginateTypeDef]
    ) -> PageIterator[ListCodeReviewJobTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviewJobTasks.html#SecurityAgent.Paginator.ListCodeReviewJobTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listcodereviewjobtaskspaginator)
        """


if TYPE_CHECKING:
    _ListCodeReviewJobsForCodeReviewPaginatorBase = Paginator[
        ListCodeReviewJobsForCodeReviewOutputTypeDef
    ]
else:
    _ListCodeReviewJobsForCodeReviewPaginatorBase = Paginator  # type: ignore[assignment]


class ListCodeReviewJobsForCodeReviewPaginator(_ListCodeReviewJobsForCodeReviewPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviewJobsForCodeReview.html#SecurityAgent.Paginator.ListCodeReviewJobsForCodeReview)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listcodereviewjobsforcodereviewpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeReviewJobsForCodeReviewInputPaginateTypeDef]
    ) -> PageIterator[ListCodeReviewJobsForCodeReviewOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviewJobsForCodeReview.html#SecurityAgent.Paginator.ListCodeReviewJobsForCodeReview.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listcodereviewjobsforcodereviewpaginator)
        """


if TYPE_CHECKING:
    _ListCodeReviewsPaginatorBase = Paginator[ListCodeReviewsOutputTypeDef]
else:
    _ListCodeReviewsPaginatorBase = Paginator  # type: ignore[assignment]


class ListCodeReviewsPaginator(_ListCodeReviewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviews.html#SecurityAgent.Paginator.ListCodeReviews)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listcodereviewspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeReviewsInputPaginateTypeDef]
    ) -> PageIterator[ListCodeReviewsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListCodeReviews.html#SecurityAgent.Paginator.ListCodeReviews.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listcodereviewspaginator)
        """


if TYPE_CHECKING:
    _ListDiscoveredEndpointsPaginatorBase = Paginator[ListDiscoveredEndpointsOutputTypeDef]
else:
    _ListDiscoveredEndpointsPaginatorBase = Paginator  # type: ignore[assignment]


class ListDiscoveredEndpointsPaginator(_ListDiscoveredEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListDiscoveredEndpoints.html#SecurityAgent.Paginator.ListDiscoveredEndpoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listdiscoveredendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDiscoveredEndpointsInputPaginateTypeDef]
    ) -> PageIterator[ListDiscoveredEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListDiscoveredEndpoints.html#SecurityAgent.Paginator.ListDiscoveredEndpoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listdiscoveredendpointspaginator)
        """


if TYPE_CHECKING:
    _ListFindingsPaginatorBase = Paginator[ListFindingsOutputTypeDef]
else:
    _ListFindingsPaginatorBase = Paginator  # type: ignore[assignment]


class ListFindingsPaginator(_ListFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListFindings.html#SecurityAgent.Paginator.ListFindings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listfindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingsInputPaginateTypeDef]
    ) -> PageIterator[ListFindingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListFindings.html#SecurityAgent.Paginator.ListFindings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listfindingspaginator)
        """


if TYPE_CHECKING:
    _ListIntegratedResourcesPaginatorBase = Paginator[ListIntegratedResourcesOutputTypeDef]
else:
    _ListIntegratedResourcesPaginatorBase = Paginator  # type: ignore[assignment]


class ListIntegratedResourcesPaginator(_ListIntegratedResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegratedResources.html#SecurityAgent.Paginator.ListIntegratedResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listintegratedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegratedResourcesInputPaginateTypeDef]
    ) -> PageIterator[ListIntegratedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegratedResources.html#SecurityAgent.Paginator.ListIntegratedResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listintegratedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListIntegrationsPaginatorBase = Paginator[ListIntegrationsOutputTypeDef]
else:
    _ListIntegrationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListIntegrationsPaginator(_ListIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegrations.html#SecurityAgent.Paginator.ListIntegrations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listintegrationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegrationsInputPaginateTypeDef]
    ) -> PageIterator[ListIntegrationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegrations.html#SecurityAgent.Paginator.ListIntegrations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listintegrationspaginator)
        """


if TYPE_CHECKING:
    _ListMembershipsPaginatorBase = Paginator[ListMembershipsResponseTypeDef]
else:
    _ListMembershipsPaginatorBase = Paginator  # type: ignore[assignment]


class ListMembershipsPaginator(_ListMembershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListMemberships.html#SecurityAgent.Paginator.ListMemberships)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listmembershipspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMembershipsRequestPaginateTypeDef]
    ) -> PageIterator[ListMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListMemberships.html#SecurityAgent.Paginator.ListMemberships.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listmembershipspaginator)
        """


if TYPE_CHECKING:
    _ListPentestJobTasksPaginatorBase = Paginator[ListPentestJobTasksOutputTypeDef]
else:
    _ListPentestJobTasksPaginatorBase = Paginator  # type: ignore[assignment]


class ListPentestJobTasksPaginator(_ListPentestJobTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobTasks.html#SecurityAgent.Paginator.ListPentestJobTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestjobtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPentestJobTasksInputPaginateTypeDef]
    ) -> PageIterator[ListPentestJobTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobTasks.html#SecurityAgent.Paginator.ListPentestJobTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestjobtaskspaginator)
        """


if TYPE_CHECKING:
    _ListPentestJobsForPentestPaginatorBase = Paginator[ListPentestJobsForPentestOutputTypeDef]
else:
    _ListPentestJobsForPentestPaginatorBase = Paginator  # type: ignore[assignment]


class ListPentestJobsForPentestPaginator(_ListPentestJobsForPentestPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobsForPentest.html#SecurityAgent.Paginator.ListPentestJobsForPentest)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestjobsforpentestpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPentestJobsForPentestInputPaginateTypeDef]
    ) -> PageIterator[ListPentestJobsForPentestOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobsForPentest.html#SecurityAgent.Paginator.ListPentestJobsForPentest.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestjobsforpentestpaginator)
        """


if TYPE_CHECKING:
    _ListPentestsPaginatorBase = Paginator[ListPentestsOutputTypeDef]
else:
    _ListPentestsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPentestsPaginator(_ListPentestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentests.html#SecurityAgent.Paginator.ListPentests)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPentestsInputPaginateTypeDef]
    ) -> PageIterator[ListPentestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentests.html#SecurityAgent.Paginator.ListPentests.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestspaginator)
        """


if TYPE_CHECKING:
    _ListPrivateConnectionsPaginatorBase = Paginator[ListPrivateConnectionsOutputTypeDef]
else:
    _ListPrivateConnectionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPrivateConnectionsPaginator(_ListPrivateConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPrivateConnections.html#SecurityAgent.Paginator.ListPrivateConnections)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listprivateconnectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrivateConnectionsInputPaginateTypeDef]
    ) -> PageIterator[ListPrivateConnectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPrivateConnections.html#SecurityAgent.Paginator.ListPrivateConnections.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listprivateconnectionspaginator)
        """


if TYPE_CHECKING:
    _ListSecurityRequirementPacksPaginatorBase = Paginator[
        ListSecurityRequirementPacksOutputTypeDef
    ]
else:
    _ListSecurityRequirementPacksPaginatorBase = Paginator  # type: ignore[assignment]


class ListSecurityRequirementPacksPaginator(_ListSecurityRequirementPacksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListSecurityRequirementPacks.html#SecurityAgent.Paginator.ListSecurityRequirementPacks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listsecurityrequirementpackspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityRequirementPacksInputPaginateTypeDef]
    ) -> PageIterator[ListSecurityRequirementPacksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListSecurityRequirementPacks.html#SecurityAgent.Paginator.ListSecurityRequirementPacks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listsecurityrequirementpackspaginator)
        """


if TYPE_CHECKING:
    _ListSecurityRequirementsPaginatorBase = Paginator[ListSecurityRequirementsOutputTypeDef]
else:
    _ListSecurityRequirementsPaginatorBase = Paginator  # type: ignore[assignment]


class ListSecurityRequirementsPaginator(_ListSecurityRequirementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListSecurityRequirements.html#SecurityAgent.Paginator.ListSecurityRequirements)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listsecurityrequirementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityRequirementsInputPaginateTypeDef]
    ) -> PageIterator[ListSecurityRequirementsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListSecurityRequirements.html#SecurityAgent.Paginator.ListSecurityRequirements.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listsecurityrequirementspaginator)
        """


if TYPE_CHECKING:
    _ListTargetDomainsPaginatorBase = Paginator[ListTargetDomainsOutputTypeDef]
else:
    _ListTargetDomainsPaginatorBase = Paginator  # type: ignore[assignment]


class ListTargetDomainsPaginator(_ListTargetDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListTargetDomains.html#SecurityAgent.Paginator.ListTargetDomains)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listtargetdomainspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetDomainsInputPaginateTypeDef]
    ) -> PageIterator[ListTargetDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListTargetDomains.html#SecurityAgent.Paginator.ListTargetDomains.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listtargetdomainspaginator)
        """


if TYPE_CHECKING:
    _ListThreatModelJobTasksPaginatorBase = Paginator[ListThreatModelJobTasksOutputTypeDef]
else:
    _ListThreatModelJobTasksPaginatorBase = Paginator  # type: ignore[assignment]


class ListThreatModelJobTasksPaginator(_ListThreatModelJobTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModelJobTasks.html#SecurityAgent.Paginator.ListThreatModelJobTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listthreatmodeljobtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThreatModelJobTasksInputPaginateTypeDef]
    ) -> PageIterator[ListThreatModelJobTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModelJobTasks.html#SecurityAgent.Paginator.ListThreatModelJobTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listthreatmodeljobtaskspaginator)
        """


if TYPE_CHECKING:
    _ListThreatModelJobsPaginatorBase = Paginator[ListThreatModelJobsOutputTypeDef]
else:
    _ListThreatModelJobsPaginatorBase = Paginator  # type: ignore[assignment]


class ListThreatModelJobsPaginator(_ListThreatModelJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModelJobs.html#SecurityAgent.Paginator.ListThreatModelJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listthreatmodeljobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThreatModelJobsInputPaginateTypeDef]
    ) -> PageIterator[ListThreatModelJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModelJobs.html#SecurityAgent.Paginator.ListThreatModelJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listthreatmodeljobspaginator)
        """


if TYPE_CHECKING:
    _ListThreatModelsPaginatorBase = Paginator[ListThreatModelsOutputTypeDef]
else:
    _ListThreatModelsPaginatorBase = Paginator  # type: ignore[assignment]


class ListThreatModelsPaginator(_ListThreatModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModels.html#SecurityAgent.Paginator.ListThreatModels)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listthreatmodelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThreatModelsInputPaginateTypeDef]
    ) -> PageIterator[ListThreatModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreatModels.html#SecurityAgent.Paginator.ListThreatModels.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listthreatmodelspaginator)
        """


if TYPE_CHECKING:
    _ListThreatsPaginatorBase = Paginator[ListThreatsOutputTypeDef]
else:
    _ListThreatsPaginatorBase = Paginator  # type: ignore[assignment]


class ListThreatsPaginator(_ListThreatsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreats.html#SecurityAgent.Paginator.ListThreats)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listthreatspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThreatsInputPaginateTypeDef]
    ) -> PageIterator[ListThreatsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListThreats.html#SecurityAgent.Paginator.ListThreats.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listthreatspaginator)
        """
