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

    session = get_session()
    with session.create_client("securityagent") as client:
        client: SecurityAgentClient

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

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
