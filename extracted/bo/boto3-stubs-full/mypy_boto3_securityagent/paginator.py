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
        ListDiscoveredEndpointsPaginator,
        ListFindingsPaginator,
        ListIntegratedResourcesPaginator,
        ListIntegrationsPaginator,
        ListMembershipsPaginator,
        ListPentestJobTasksPaginator,
        ListPentestJobsForPentestPaginator,
        ListPentestsPaginator,
        ListTargetDomainsPaginator,
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
    ListTargetDomainsInputPaginateTypeDef,
    ListTargetDomainsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
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
)


if TYPE_CHECKING:
    _ListAgentSpacesPaginatorBase = Paginator[ListAgentSpacesOutputTypeDef]
else:
    _ListAgentSpacesPaginatorBase = Paginator  # type: ignore[assignment]


class ListAgentSpacesPaginator(_ListAgentSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListAgentSpaces.html#SecurityAgent.Paginator.ListAgentSpaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listagentspacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentSpacesInputPaginateTypeDef]
    ) -> PageIterator[ListAgentSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListAgentSpaces.html#SecurityAgent.Paginator.ListAgentSpaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listagentspacespaginator)
        """


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = Paginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListApplications.html#SecurityAgent.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListApplications.html#SecurityAgent.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListArtifactsPaginatorBase = Paginator[ListArtifactsOutputTypeDef]
else:
    _ListArtifactsPaginatorBase = Paginator  # type: ignore[assignment]


class ListArtifactsPaginator(_ListArtifactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListArtifacts.html#SecurityAgent.Paginator.ListArtifacts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listartifactspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArtifactsInputPaginateTypeDef]
    ) -> PageIterator[ListArtifactsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListArtifacts.html#SecurityAgent.Paginator.ListArtifacts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listartifactspaginator)
        """


if TYPE_CHECKING:
    _ListDiscoveredEndpointsPaginatorBase = Paginator[ListDiscoveredEndpointsOutputTypeDef]
else:
    _ListDiscoveredEndpointsPaginatorBase = Paginator  # type: ignore[assignment]


class ListDiscoveredEndpointsPaginator(_ListDiscoveredEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListDiscoveredEndpoints.html#SecurityAgent.Paginator.ListDiscoveredEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listdiscoveredendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDiscoveredEndpointsInputPaginateTypeDef]
    ) -> PageIterator[ListDiscoveredEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListDiscoveredEndpoints.html#SecurityAgent.Paginator.ListDiscoveredEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listdiscoveredendpointspaginator)
        """


if TYPE_CHECKING:
    _ListFindingsPaginatorBase = Paginator[ListFindingsOutputTypeDef]
else:
    _ListFindingsPaginatorBase = Paginator  # type: ignore[assignment]


class ListFindingsPaginator(_ListFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListFindings.html#SecurityAgent.Paginator.ListFindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listfindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingsInputPaginateTypeDef]
    ) -> PageIterator[ListFindingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListFindings.html#SecurityAgent.Paginator.ListFindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listfindingspaginator)
        """


if TYPE_CHECKING:
    _ListIntegratedResourcesPaginatorBase = Paginator[ListIntegratedResourcesOutputTypeDef]
else:
    _ListIntegratedResourcesPaginatorBase = Paginator  # type: ignore[assignment]


class ListIntegratedResourcesPaginator(_ListIntegratedResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegratedResources.html#SecurityAgent.Paginator.ListIntegratedResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listintegratedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegratedResourcesInputPaginateTypeDef]
    ) -> PageIterator[ListIntegratedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegratedResources.html#SecurityAgent.Paginator.ListIntegratedResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listintegratedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListIntegrationsPaginatorBase = Paginator[ListIntegrationsOutputTypeDef]
else:
    _ListIntegrationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListIntegrationsPaginator(_ListIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegrations.html#SecurityAgent.Paginator.ListIntegrations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listintegrationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegrationsInputPaginateTypeDef]
    ) -> PageIterator[ListIntegrationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListIntegrations.html#SecurityAgent.Paginator.ListIntegrations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listintegrationspaginator)
        """


if TYPE_CHECKING:
    _ListMembershipsPaginatorBase = Paginator[ListMembershipsResponseTypeDef]
else:
    _ListMembershipsPaginatorBase = Paginator  # type: ignore[assignment]


class ListMembershipsPaginator(_ListMembershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListMemberships.html#SecurityAgent.Paginator.ListMemberships)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listmembershipspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMembershipsRequestPaginateTypeDef]
    ) -> PageIterator[ListMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListMemberships.html#SecurityAgent.Paginator.ListMemberships.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listmembershipspaginator)
        """


if TYPE_CHECKING:
    _ListPentestJobTasksPaginatorBase = Paginator[ListPentestJobTasksOutputTypeDef]
else:
    _ListPentestJobTasksPaginatorBase = Paginator  # type: ignore[assignment]


class ListPentestJobTasksPaginator(_ListPentestJobTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobTasks.html#SecurityAgent.Paginator.ListPentestJobTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestjobtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPentestJobTasksInputPaginateTypeDef]
    ) -> PageIterator[ListPentestJobTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobTasks.html#SecurityAgent.Paginator.ListPentestJobTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestjobtaskspaginator)
        """


if TYPE_CHECKING:
    _ListPentestJobsForPentestPaginatorBase = Paginator[ListPentestJobsForPentestOutputTypeDef]
else:
    _ListPentestJobsForPentestPaginatorBase = Paginator  # type: ignore[assignment]


class ListPentestJobsForPentestPaginator(_ListPentestJobsForPentestPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobsForPentest.html#SecurityAgent.Paginator.ListPentestJobsForPentest)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestjobsforpentestpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPentestJobsForPentestInputPaginateTypeDef]
    ) -> PageIterator[ListPentestJobsForPentestOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentestJobsForPentest.html#SecurityAgent.Paginator.ListPentestJobsForPentest.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestjobsforpentestpaginator)
        """


if TYPE_CHECKING:
    _ListPentestsPaginatorBase = Paginator[ListPentestsOutputTypeDef]
else:
    _ListPentestsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPentestsPaginator(_ListPentestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentests.html#SecurityAgent.Paginator.ListPentests)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPentestsInputPaginateTypeDef]
    ) -> PageIterator[ListPentestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListPentests.html#SecurityAgent.Paginator.ListPentests.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listpentestspaginator)
        """


if TYPE_CHECKING:
    _ListTargetDomainsPaginatorBase = Paginator[ListTargetDomainsOutputTypeDef]
else:
    _ListTargetDomainsPaginatorBase = Paginator  # type: ignore[assignment]


class ListTargetDomainsPaginator(_ListTargetDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListTargetDomains.html#SecurityAgent.Paginator.ListTargetDomains)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listtargetdomainspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetDomainsInputPaginateTypeDef]
    ) -> PageIterator[ListTargetDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/paginator/ListTargetDomains.html#SecurityAgent.Paginator.ListTargetDomains.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/paginators/#listtargetdomainspaginator)
        """
