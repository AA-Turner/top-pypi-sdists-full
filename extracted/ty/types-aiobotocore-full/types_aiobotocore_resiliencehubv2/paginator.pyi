"""
Type annotations for resiliencehubv2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resiliencehubv2.client import ResilienceHubV2Client
    from types_aiobotocore_resiliencehubv2.paginator import (
        ListAssertionsPaginator,
        ListDependenciesPaginator,
        ListFailureModeAssessmentsPaginator,
        ListFailureModeFindingsPaginator,
        ListInputSourcesPaginator,
        ListPoliciesPaginator,
        ListReportsPaginator,
        ListResourcesPaginator,
        ListServiceEventsPaginator,
        ListServiceFunctionsPaginator,
        ListServiceTopologyEdgesPaginator,
        ListServicesPaginator,
        ListSystemEventsPaginator,
        ListSystemsPaginator,
        ListUserJourneysPaginator,
    )

    session = get_session()
    with session.create_client("resiliencehubv2") as client:
        client: ResilienceHubV2Client

        list_assertions_paginator: ListAssertionsPaginator = client.get_paginator("list_assertions")
        list_dependencies_paginator: ListDependenciesPaginator = client.get_paginator("list_dependencies")
        list_failure_mode_assessments_paginator: ListFailureModeAssessmentsPaginator = client.get_paginator("list_failure_mode_assessments")
        list_failure_mode_findings_paginator: ListFailureModeFindingsPaginator = client.get_paginator("list_failure_mode_findings")
        list_input_sources_paginator: ListInputSourcesPaginator = client.get_paginator("list_input_sources")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
        list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
        list_service_events_paginator: ListServiceEventsPaginator = client.get_paginator("list_service_events")
        list_service_functions_paginator: ListServiceFunctionsPaginator = client.get_paginator("list_service_functions")
        list_service_topology_edges_paginator: ListServiceTopologyEdgesPaginator = client.get_paginator("list_service_topology_edges")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
        list_system_events_paginator: ListSystemEventsPaginator = client.get_paginator("list_system_events")
        list_systems_paginator: ListSystemsPaginator = client.get_paginator("list_systems")
        list_user_journeys_paginator: ListUserJourneysPaginator = client.get_paginator("list_user_journeys")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAssertionsRequestPaginateTypeDef,
    ListAssertionsResponseTypeDef,
    ListDependenciesRequestPaginateTypeDef,
    ListDependenciesResponseTypeDef,
    ListFailureModeAssessmentsRequestPaginateTypeDef,
    ListFailureModeAssessmentsResponseTypeDef,
    ListFailureModeFindingsRequestPaginateTypeDef,
    ListFailureModeFindingsResponseTypeDef,
    ListInputSourcesRequestPaginateTypeDef,
    ListInputSourcesResponseTypeDef,
    ListPoliciesRequestPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListReportsRequestPaginateTypeDef,
    ListReportsResponseTypeDef,
    ListResourcesRequestPaginateTypeDef,
    ListResourcesResponseTypeDef,
    ListServiceEventsRequestPaginateTypeDef,
    ListServiceEventsResponseTypeDef,
    ListServiceFunctionsRequestPaginateTypeDef,
    ListServiceFunctionsResponseTypeDef,
    ListServicesRequestPaginateTypeDef,
    ListServicesResponseTypeDef,
    ListServiceTopologyEdgesRequestPaginateTypeDef,
    ListServiceTopologyEdgesResponseTypeDef,
    ListSystemEventsRequestPaginateTypeDef,
    ListSystemEventsResponseTypeDef,
    ListSystemsRequestPaginateTypeDef,
    ListSystemsResponseTypeDef,
    ListUserJourneysRequestPaginateTypeDef,
    ListUserJourneysResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssertionsPaginator",
    "ListDependenciesPaginator",
    "ListFailureModeAssessmentsPaginator",
    "ListFailureModeFindingsPaginator",
    "ListInputSourcesPaginator",
    "ListPoliciesPaginator",
    "ListReportsPaginator",
    "ListResourcesPaginator",
    "ListServiceEventsPaginator",
    "ListServiceFunctionsPaginator",
    "ListServiceTopologyEdgesPaginator",
    "ListServicesPaginator",
    "ListSystemEventsPaginator",
    "ListSystemsPaginator",
    "ListUserJourneysPaginator",
)

if TYPE_CHECKING:
    _ListAssertionsPaginatorBase = AioPaginator[ListAssertionsResponseTypeDef]
else:
    _ListAssertionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssertionsPaginator(_ListAssertionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListAssertions.html#ResilienceHubV2.Paginator.ListAssertions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listassertionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssertionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssertionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListAssertions.html#ResilienceHubV2.Paginator.ListAssertions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listassertionspaginator)
        """

if TYPE_CHECKING:
    _ListDependenciesPaginatorBase = AioPaginator[ListDependenciesResponseTypeDef]
else:
    _ListDependenciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDependenciesPaginator(_ListDependenciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListDependencies.html#ResilienceHubV2.Paginator.ListDependencies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listdependenciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDependenciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDependenciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListDependencies.html#ResilienceHubV2.Paginator.ListDependencies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listdependenciespaginator)
        """

if TYPE_CHECKING:
    _ListFailureModeAssessmentsPaginatorBase = AioPaginator[
        ListFailureModeAssessmentsResponseTypeDef
    ]
else:
    _ListFailureModeAssessmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFailureModeAssessmentsPaginator(_ListFailureModeAssessmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListFailureModeAssessments.html#ResilienceHubV2.Paginator.ListFailureModeAssessments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listfailuremodeassessmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFailureModeAssessmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFailureModeAssessmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListFailureModeAssessments.html#ResilienceHubV2.Paginator.ListFailureModeAssessments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listfailuremodeassessmentspaginator)
        """

if TYPE_CHECKING:
    _ListFailureModeFindingsPaginatorBase = AioPaginator[ListFailureModeFindingsResponseTypeDef]
else:
    _ListFailureModeFindingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFailureModeFindingsPaginator(_ListFailureModeFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListFailureModeFindings.html#ResilienceHubV2.Paginator.ListFailureModeFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listfailuremodefindingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFailureModeFindingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFailureModeFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListFailureModeFindings.html#ResilienceHubV2.Paginator.ListFailureModeFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listfailuremodefindingspaginator)
        """

if TYPE_CHECKING:
    _ListInputSourcesPaginatorBase = AioPaginator[ListInputSourcesResponseTypeDef]
else:
    _ListInputSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInputSourcesPaginator(_ListInputSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListInputSources.html#ResilienceHubV2.Paginator.ListInputSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listinputsourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInputSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInputSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListInputSources.html#ResilienceHubV2.Paginator.ListInputSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listinputsourcespaginator)
        """

if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = AioPaginator[ListPoliciesResponseTypeDef]
else:
    _ListPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListPolicies.html#ResilienceHubV2.Paginator.ListPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListPolicies.html#ResilienceHubV2.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListReportsPaginatorBase = AioPaginator[ListReportsResponseTypeDef]
else:
    _ListReportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReportsPaginator(_ListReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListReports.html#ResilienceHubV2.Paginator.ListReports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listreportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListReports.html#ResilienceHubV2.Paginator.ListReports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listreportspaginator)
        """

if TYPE_CHECKING:
    _ListResourcesPaginatorBase = AioPaginator[ListResourcesResponseTypeDef]
else:
    _ListResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourcesPaginator(_ListResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListResources.html#ResilienceHubV2.Paginator.ListResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListResources.html#ResilienceHubV2.Paginator.ListResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listresourcespaginator)
        """

if TYPE_CHECKING:
    _ListServiceEventsPaginatorBase = AioPaginator[ListServiceEventsResponseTypeDef]
else:
    _ListServiceEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceEventsPaginator(_ListServiceEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceEvents.html#ResilienceHubV2.Paginator.ListServiceEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listserviceeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceEvents.html#ResilienceHubV2.Paginator.ListServiceEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listserviceeventspaginator)
        """

if TYPE_CHECKING:
    _ListServiceFunctionsPaginatorBase = AioPaginator[ListServiceFunctionsResponseTypeDef]
else:
    _ListServiceFunctionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceFunctionsPaginator(_ListServiceFunctionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceFunctions.html#ResilienceHubV2.Paginator.ListServiceFunctions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listservicefunctionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceFunctionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceFunctions.html#ResilienceHubV2.Paginator.ListServiceFunctions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listservicefunctionspaginator)
        """

if TYPE_CHECKING:
    _ListServiceTopologyEdgesPaginatorBase = AioPaginator[ListServiceTopologyEdgesResponseTypeDef]
else:
    _ListServiceTopologyEdgesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceTopologyEdgesPaginator(_ListServiceTopologyEdgesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceTopologyEdges.html#ResilienceHubV2.Paginator.ListServiceTopologyEdges)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listservicetopologyedgespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceTopologyEdgesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceTopologyEdgesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceTopologyEdges.html#ResilienceHubV2.Paginator.ListServiceTopologyEdges.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listservicetopologyedgespaginator)
        """

if TYPE_CHECKING:
    _ListServicesPaginatorBase = AioPaginator[ListServicesResponseTypeDef]
else:
    _ListServicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServices.html#ResilienceHubV2.Paginator.ListServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listservicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServices.html#ResilienceHubV2.Paginator.ListServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listservicespaginator)
        """

if TYPE_CHECKING:
    _ListSystemEventsPaginatorBase = AioPaginator[ListSystemEventsResponseTypeDef]
else:
    _ListSystemEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSystemEventsPaginator(_ListSystemEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListSystemEvents.html#ResilienceHubV2.Paginator.ListSystemEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listsystemeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSystemEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSystemEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListSystemEvents.html#ResilienceHubV2.Paginator.ListSystemEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listsystemeventspaginator)
        """

if TYPE_CHECKING:
    _ListSystemsPaginatorBase = AioPaginator[ListSystemsResponseTypeDef]
else:
    _ListSystemsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSystemsPaginator(_ListSystemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListSystems.html#ResilienceHubV2.Paginator.ListSystems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listsystemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSystemsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSystemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListSystems.html#ResilienceHubV2.Paginator.ListSystems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listsystemspaginator)
        """

if TYPE_CHECKING:
    _ListUserJourneysPaginatorBase = AioPaginator[ListUserJourneysResponseTypeDef]
else:
    _ListUserJourneysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserJourneysPaginator(_ListUserJourneysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListUserJourneys.html#ResilienceHubV2.Paginator.ListUserJourneys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listuserjourneyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserJourneysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserJourneysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListUserJourneys.html#ResilienceHubV2.Paginator.ListUserJourneys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/paginators/#listuserjourneyspaginator)
        """
