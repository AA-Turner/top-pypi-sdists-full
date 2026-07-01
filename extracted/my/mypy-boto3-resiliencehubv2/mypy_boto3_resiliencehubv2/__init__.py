"""
Main interface for resiliencehubv2 service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_resiliencehubv2 import (
        Client,
        FailureModeAssessmentSuccessWaiter,
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
        ReportSucceededWaiter,
        ResilienceHubV2Client,
        ServiceAssessmentCompletedWaiter,
        ServiceResourceDiscoveryCompletedWaiter,
    )

    session = Session()
    client: ResilienceHubV2Client = session.client("resiliencehubv2")

    failure_mode_assessment_success_waiter: FailureModeAssessmentSuccessWaiter = client.get_waiter("failure_mode_assessment_success")
    report_succeeded_waiter: ReportSucceededWaiter = client.get_waiter("report_succeeded")
    service_assessment_completed_waiter: ServiceAssessmentCompletedWaiter = client.get_waiter("service_assessment_completed")
    service_resource_discovery_completed_waiter: ServiceResourceDiscoveryCompletedWaiter = client.get_waiter("service_resource_discovery_completed")

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

from .client import ResilienceHubV2Client
from .paginator import (
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
    ListServicesPaginator,
    ListServiceTopologyEdgesPaginator,
    ListSystemEventsPaginator,
    ListSystemsPaginator,
    ListUserJourneysPaginator,
)
from .waiter import (
    FailureModeAssessmentSuccessWaiter,
    ReportSucceededWaiter,
    ServiceAssessmentCompletedWaiter,
    ServiceResourceDiscoveryCompletedWaiter,
)

Client = ResilienceHubV2Client


__all__ = (
    "Client",
    "FailureModeAssessmentSuccessWaiter",
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
    "ReportSucceededWaiter",
    "ResilienceHubV2Client",
    "ServiceAssessmentCompletedWaiter",
    "ServiceResourceDiscoveryCompletedWaiter",
)
