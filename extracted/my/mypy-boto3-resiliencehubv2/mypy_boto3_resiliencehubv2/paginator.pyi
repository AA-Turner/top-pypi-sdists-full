"""
Type annotations for resiliencehubv2 service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_resiliencehubv2.client import ResilienceHubV2Client
    from mypy_boto3_resiliencehubv2.paginator import (
        ListAssertionsPaginator,
        ListDependenciesPaginator,
        ListFailureModeAssessmentsPaginator,
        ListFailureModeFindingsPaginator,
        ListInputSourcesPaginator,
        ListPoliciesPaginator,
        ListReportsPaginator,
        ListResolvedTestRunTargetResourcesPaginator,
        ListResourcesPaginator,
        ListServiceEventsPaginator,
        ListServiceFunctionsPaginator,
        ListServiceTopologyEdgesPaginator,
        ListServicesPaginator,
        ListSystemEventsPaginator,
        ListSystemsPaginator,
        ListTestRunEventsPaginator,
        ListTestRunSourcesPaginator,
        ListTestRunsPaginator,
        ListTestSourcesPaginator,
        ListTestsPaginator,
        ListUserJourneysPaginator,
    )

    session = Session()
    client: ResilienceHubV2Client = session.client("resiliencehubv2")

    list_assertions_paginator: ListAssertionsPaginator = client.get_paginator("list_assertions")
    list_dependencies_paginator: ListDependenciesPaginator = client.get_paginator("list_dependencies")
    list_failure_mode_assessments_paginator: ListFailureModeAssessmentsPaginator = client.get_paginator("list_failure_mode_assessments")
    list_failure_mode_findings_paginator: ListFailureModeFindingsPaginator = client.get_paginator("list_failure_mode_findings")
    list_input_sources_paginator: ListInputSourcesPaginator = client.get_paginator("list_input_sources")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    list_resolved_test_run_target_resources_paginator: ListResolvedTestRunTargetResourcesPaginator = client.get_paginator("list_resolved_test_run_target_resources")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    list_service_events_paginator: ListServiceEventsPaginator = client.get_paginator("list_service_events")
    list_service_functions_paginator: ListServiceFunctionsPaginator = client.get_paginator("list_service_functions")
    list_service_topology_edges_paginator: ListServiceTopologyEdgesPaginator = client.get_paginator("list_service_topology_edges")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    list_system_events_paginator: ListSystemEventsPaginator = client.get_paginator("list_system_events")
    list_systems_paginator: ListSystemsPaginator = client.get_paginator("list_systems")
    list_test_run_events_paginator: ListTestRunEventsPaginator = client.get_paginator("list_test_run_events")
    list_test_run_sources_paginator: ListTestRunSourcesPaginator = client.get_paginator("list_test_run_sources")
    list_test_runs_paginator: ListTestRunsPaginator = client.get_paginator("list_test_runs")
    list_test_sources_paginator: ListTestSourcesPaginator = client.get_paginator("list_test_sources")
    list_tests_paginator: ListTestsPaginator = client.get_paginator("list_tests")
    list_user_journeys_paginator: ListUserJourneysPaginator = client.get_paginator("list_user_journeys")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    ListResolvedTestRunTargetResourcesRequestPaginateTypeDef,
    ListResolvedTestRunTargetResourcesResponseTypeDef,
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
    ListTestRunEventsRequestPaginateTypeDef,
    ListTestRunEventsResponseTypeDef,
    ListTestRunSourcesRequestPaginateTypeDef,
    ListTestRunSourcesResponseTypeDef,
    ListTestRunsRequestPaginateTypeDef,
    ListTestRunsResponseTypeDef,
    ListTestSourcesRequestPaginateTypeDef,
    ListTestSourcesResponseTypeDef,
    ListTestsRequestPaginateTypeDef,
    ListTestsResponseTypeDef,
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
    "ListResolvedTestRunTargetResourcesPaginator",
    "ListResourcesPaginator",
    "ListServiceEventsPaginator",
    "ListServiceFunctionsPaginator",
    "ListServiceTopologyEdgesPaginator",
    "ListServicesPaginator",
    "ListSystemEventsPaginator",
    "ListSystemsPaginator",
    "ListTestRunEventsPaginator",
    "ListTestRunSourcesPaginator",
    "ListTestRunsPaginator",
    "ListTestSourcesPaginator",
    "ListTestsPaginator",
    "ListUserJourneysPaginator",
)

if TYPE_CHECKING:
    _ListAssertionsPaginatorBase = Paginator[ListAssertionsResponseTypeDef]
else:
    _ListAssertionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssertionsPaginator(_ListAssertionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListAssertions.html#ResilienceHubV2.Paginator.ListAssertions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listassertionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssertionsRequestPaginateTypeDef]
    ) -> PageIterator[ListAssertionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListAssertions.html#ResilienceHubV2.Paginator.ListAssertions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listassertionspaginator)
        """

if TYPE_CHECKING:
    _ListDependenciesPaginatorBase = Paginator[ListDependenciesResponseTypeDef]
else:
    _ListDependenciesPaginatorBase = Paginator  # type: ignore[assignment]

class ListDependenciesPaginator(_ListDependenciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListDependencies.html#ResilienceHubV2.Paginator.ListDependencies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listdependenciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDependenciesRequestPaginateTypeDef]
    ) -> PageIterator[ListDependenciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListDependencies.html#ResilienceHubV2.Paginator.ListDependencies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listdependenciespaginator)
        """

if TYPE_CHECKING:
    _ListFailureModeAssessmentsPaginatorBase = Paginator[ListFailureModeAssessmentsResponseTypeDef]
else:
    _ListFailureModeAssessmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListFailureModeAssessmentsPaginator(_ListFailureModeAssessmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListFailureModeAssessments.html#ResilienceHubV2.Paginator.ListFailureModeAssessments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listfailuremodeassessmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFailureModeAssessmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListFailureModeAssessmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListFailureModeAssessments.html#ResilienceHubV2.Paginator.ListFailureModeAssessments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listfailuremodeassessmentspaginator)
        """

if TYPE_CHECKING:
    _ListFailureModeFindingsPaginatorBase = Paginator[ListFailureModeFindingsResponseTypeDef]
else:
    _ListFailureModeFindingsPaginatorBase = Paginator  # type: ignore[assignment]

class ListFailureModeFindingsPaginator(_ListFailureModeFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListFailureModeFindings.html#ResilienceHubV2.Paginator.ListFailureModeFindings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listfailuremodefindingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFailureModeFindingsRequestPaginateTypeDef]
    ) -> PageIterator[ListFailureModeFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListFailureModeFindings.html#ResilienceHubV2.Paginator.ListFailureModeFindings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listfailuremodefindingspaginator)
        """

if TYPE_CHECKING:
    _ListInputSourcesPaginatorBase = Paginator[ListInputSourcesResponseTypeDef]
else:
    _ListInputSourcesPaginatorBase = Paginator  # type: ignore[assignment]

class ListInputSourcesPaginator(_ListInputSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListInputSources.html#ResilienceHubV2.Paginator.ListInputSources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listinputsourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInputSourcesRequestPaginateTypeDef]
    ) -> PageIterator[ListInputSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListInputSources.html#ResilienceHubV2.Paginator.ListInputSources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listinputsourcespaginator)
        """

if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = Paginator[ListPoliciesResponseTypeDef]
else:
    _ListPoliciesPaginatorBase = Paginator  # type: ignore[assignment]

class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListPolicies.html#ResilienceHubV2.Paginator.ListPolicies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesRequestPaginateTypeDef]
    ) -> PageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListPolicies.html#ResilienceHubV2.Paginator.ListPolicies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListReportsPaginatorBase = Paginator[ListReportsResponseTypeDef]
else:
    _ListReportsPaginatorBase = Paginator  # type: ignore[assignment]

class ListReportsPaginator(_ListReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListReports.html#ResilienceHubV2.Paginator.ListReports)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listreportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportsRequestPaginateTypeDef]
    ) -> PageIterator[ListReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListReports.html#ResilienceHubV2.Paginator.ListReports.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listreportspaginator)
        """

if TYPE_CHECKING:
    _ListResolvedTestRunTargetResourcesPaginatorBase = Paginator[
        ListResolvedTestRunTargetResourcesResponseTypeDef
    ]
else:
    _ListResolvedTestRunTargetResourcesPaginatorBase = Paginator  # type: ignore[assignment]

class ListResolvedTestRunTargetResourcesPaginator(_ListResolvedTestRunTargetResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListResolvedTestRunTargetResources.html#ResilienceHubV2.Paginator.ListResolvedTestRunTargetResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listresolvedtestruntargetresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResolvedTestRunTargetResourcesRequestPaginateTypeDef]
    ) -> PageIterator[ListResolvedTestRunTargetResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListResolvedTestRunTargetResources.html#ResilienceHubV2.Paginator.ListResolvedTestRunTargetResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listresolvedtestruntargetresourcespaginator)
        """

if TYPE_CHECKING:
    _ListResourcesPaginatorBase = Paginator[ListResourcesResponseTypeDef]
else:
    _ListResourcesPaginatorBase = Paginator  # type: ignore[assignment]

class ListResourcesPaginator(_ListResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListResources.html#ResilienceHubV2.Paginator.ListResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcesRequestPaginateTypeDef]
    ) -> PageIterator[ListResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListResources.html#ResilienceHubV2.Paginator.ListResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listresourcespaginator)
        """

if TYPE_CHECKING:
    _ListServiceEventsPaginatorBase = Paginator[ListServiceEventsResponseTypeDef]
else:
    _ListServiceEventsPaginatorBase = Paginator  # type: ignore[assignment]

class ListServiceEventsPaginator(_ListServiceEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceEvents.html#ResilienceHubV2.Paginator.ListServiceEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listserviceeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceEventsRequestPaginateTypeDef]
    ) -> PageIterator[ListServiceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceEvents.html#ResilienceHubV2.Paginator.ListServiceEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listserviceeventspaginator)
        """

if TYPE_CHECKING:
    _ListServiceFunctionsPaginatorBase = Paginator[ListServiceFunctionsResponseTypeDef]
else:
    _ListServiceFunctionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListServiceFunctionsPaginator(_ListServiceFunctionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceFunctions.html#ResilienceHubV2.Paginator.ListServiceFunctions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listservicefunctionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceFunctionsRequestPaginateTypeDef]
    ) -> PageIterator[ListServiceFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceFunctions.html#ResilienceHubV2.Paginator.ListServiceFunctions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listservicefunctionspaginator)
        """

if TYPE_CHECKING:
    _ListServiceTopologyEdgesPaginatorBase = Paginator[ListServiceTopologyEdgesResponseTypeDef]
else:
    _ListServiceTopologyEdgesPaginatorBase = Paginator  # type: ignore[assignment]

class ListServiceTopologyEdgesPaginator(_ListServiceTopologyEdgesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceTopologyEdges.html#ResilienceHubV2.Paginator.ListServiceTopologyEdges)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listservicetopologyedgespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceTopologyEdgesRequestPaginateTypeDef]
    ) -> PageIterator[ListServiceTopologyEdgesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServiceTopologyEdges.html#ResilienceHubV2.Paginator.ListServiceTopologyEdges.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listservicetopologyedgespaginator)
        """

if TYPE_CHECKING:
    _ListServicesPaginatorBase = Paginator[ListServicesResponseTypeDef]
else:
    _ListServicesPaginatorBase = Paginator  # type: ignore[assignment]

class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServices.html#ResilienceHubV2.Paginator.ListServices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listservicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesRequestPaginateTypeDef]
    ) -> PageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListServices.html#ResilienceHubV2.Paginator.ListServices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listservicespaginator)
        """

if TYPE_CHECKING:
    _ListSystemEventsPaginatorBase = Paginator[ListSystemEventsResponseTypeDef]
else:
    _ListSystemEventsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSystemEventsPaginator(_ListSystemEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListSystemEvents.html#ResilienceHubV2.Paginator.ListSystemEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listsystemeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSystemEventsRequestPaginateTypeDef]
    ) -> PageIterator[ListSystemEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListSystemEvents.html#ResilienceHubV2.Paginator.ListSystemEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listsystemeventspaginator)
        """

if TYPE_CHECKING:
    _ListSystemsPaginatorBase = Paginator[ListSystemsResponseTypeDef]
else:
    _ListSystemsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSystemsPaginator(_ListSystemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListSystems.html#ResilienceHubV2.Paginator.ListSystems)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listsystemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSystemsRequestPaginateTypeDef]
    ) -> PageIterator[ListSystemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListSystems.html#ResilienceHubV2.Paginator.ListSystems.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listsystemspaginator)
        """

if TYPE_CHECKING:
    _ListTestRunEventsPaginatorBase = Paginator[ListTestRunEventsResponseTypeDef]
else:
    _ListTestRunEventsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTestRunEventsPaginator(_ListTestRunEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTestRunEvents.html#ResilienceHubV2.Paginator.ListTestRunEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestruneventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestRunEventsRequestPaginateTypeDef]
    ) -> PageIterator[ListTestRunEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTestRunEvents.html#ResilienceHubV2.Paginator.ListTestRunEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestruneventspaginator)
        """

if TYPE_CHECKING:
    _ListTestRunSourcesPaginatorBase = Paginator[ListTestRunSourcesResponseTypeDef]
else:
    _ListTestRunSourcesPaginatorBase = Paginator  # type: ignore[assignment]

class ListTestRunSourcesPaginator(_ListTestRunSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTestRunSources.html#ResilienceHubV2.Paginator.ListTestRunSources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestrunsourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestRunSourcesRequestPaginateTypeDef]
    ) -> PageIterator[ListTestRunSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTestRunSources.html#ResilienceHubV2.Paginator.ListTestRunSources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestrunsourcespaginator)
        """

if TYPE_CHECKING:
    _ListTestRunsPaginatorBase = Paginator[ListTestRunsResponseTypeDef]
else:
    _ListTestRunsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTestRunsPaginator(_ListTestRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTestRuns.html#ResilienceHubV2.Paginator.ListTestRuns)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestrunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestRunsRequestPaginateTypeDef]
    ) -> PageIterator[ListTestRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTestRuns.html#ResilienceHubV2.Paginator.ListTestRuns.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestrunspaginator)
        """

if TYPE_CHECKING:
    _ListTestSourcesPaginatorBase = Paginator[ListTestSourcesResponseTypeDef]
else:
    _ListTestSourcesPaginatorBase = Paginator  # type: ignore[assignment]

class ListTestSourcesPaginator(_ListTestSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTestSources.html#ResilienceHubV2.Paginator.ListTestSources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestsourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestSourcesRequestPaginateTypeDef]
    ) -> PageIterator[ListTestSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTestSources.html#ResilienceHubV2.Paginator.ListTestSources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestsourcespaginator)
        """

if TYPE_CHECKING:
    _ListTestsPaginatorBase = Paginator[ListTestsResponseTypeDef]
else:
    _ListTestsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTestsPaginator(_ListTestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTests.html#ResilienceHubV2.Paginator.ListTests)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestsRequestPaginateTypeDef]
    ) -> PageIterator[ListTestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListTests.html#ResilienceHubV2.Paginator.ListTests.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listtestspaginator)
        """

if TYPE_CHECKING:
    _ListUserJourneysPaginatorBase = Paginator[ListUserJourneysResponseTypeDef]
else:
    _ListUserJourneysPaginatorBase = Paginator  # type: ignore[assignment]

class ListUserJourneysPaginator(_ListUserJourneysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListUserJourneys.html#ResilienceHubV2.Paginator.ListUserJourneys)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listuserjourneyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserJourneysRequestPaginateTypeDef]
    ) -> PageIterator[ListUserJourneysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/paginator/ListUserJourneys.html#ResilienceHubV2.Paginator.ListUserJourneys.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/paginators/#listuserjourneyspaginator)
        """
