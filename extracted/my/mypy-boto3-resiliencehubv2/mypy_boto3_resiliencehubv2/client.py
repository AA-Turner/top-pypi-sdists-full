"""
Type annotations for resiliencehubv2 service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_resiliencehubv2.client import ResilienceHubV2Client

    session = Session()
    client: ResilienceHubV2Client = session.client("resiliencehubv2")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

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
from .type_defs import (
    CreateAssertionRequestTypeDef,
    CreateAssertionResponseTypeDef,
    CreateInputSourceRequestTypeDef,
    CreateInputSourceResponseTypeDef,
    CreatePolicyRequestTypeDef,
    CreatePolicyResponseTypeDef,
    CreateReportRequestTypeDef,
    CreateReportResponseTypeDef,
    CreateServiceFunctionRequestTypeDef,
    CreateServiceFunctionResourcesRequestTypeDef,
    CreateServiceFunctionResourcesResponseTypeDef,
    CreateServiceFunctionResponseTypeDef,
    CreateServiceRequestTypeDef,
    CreateServiceResponseTypeDef,
    CreateSystemRequestTypeDef,
    CreateSystemResponseTypeDef,
    CreateUserJourneyRequestTypeDef,
    CreateUserJourneyResponseTypeDef,
    DeleteAssertionRequestTypeDef,
    DeleteAssertionResponseTypeDef,
    DeleteInputSourceRequestTypeDef,
    DeleteInputSourceResponseTypeDef,
    DeletePolicyRequestTypeDef,
    DeletePolicyResponseTypeDef,
    DeleteServiceFunctionRequestTypeDef,
    DeleteServiceFunctionResourcesRequestTypeDef,
    DeleteServiceFunctionResourcesResponseTypeDef,
    DeleteServiceFunctionResponseTypeDef,
    DeleteServiceRequestTypeDef,
    DeleteServiceResponseTypeDef,
    DeleteSystemRequestTypeDef,
    DeleteSystemResponseTypeDef,
    DeleteUserJourneyRequestTypeDef,
    DeleteUserJourneyResponseTypeDef,
    GetFailureModeFindingRequestTypeDef,
    GetFailureModeFindingResponseTypeDef,
    GetPolicyRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetServiceRequestTypeDef,
    GetServiceResponseTypeDef,
    GetSystemRequestTypeDef,
    GetSystemResponseTypeDef,
    GetUserJourneyRequestTypeDef,
    GetUserJourneyResponseTypeDef,
    ImportAppRequestTypeDef,
    ImportAppResponseTypeDef,
    ImportPolicyRequestTypeDef,
    ImportPolicyResponseTypeDef,
    ListAssertionsRequestTypeDef,
    ListAssertionsResponseTypeDef,
    ListDependenciesRequestTypeDef,
    ListDependenciesResponseTypeDef,
    ListFailureModeAssessmentsRequestTypeDef,
    ListFailureModeAssessmentsResponseTypeDef,
    ListFailureModeFindingsRequestTypeDef,
    ListFailureModeFindingsResponseTypeDef,
    ListInputSourcesRequestTypeDef,
    ListInputSourcesResponseTypeDef,
    ListPoliciesRequestTypeDef,
    ListPoliciesResponseTypeDef,
    ListReportsRequestTypeDef,
    ListReportsResponseTypeDef,
    ListResourcesRequestTypeDef,
    ListResourcesResponseTypeDef,
    ListServiceEventsRequestTypeDef,
    ListServiceEventsResponseTypeDef,
    ListServiceFunctionsRequestTypeDef,
    ListServiceFunctionsResponseTypeDef,
    ListServicesRequestTypeDef,
    ListServicesResponseTypeDef,
    ListServiceTopologyEdgesRequestTypeDef,
    ListServiceTopologyEdgesResponseTypeDef,
    ListSystemEventsRequestTypeDef,
    ListSystemEventsResponseTypeDef,
    ListSystemsRequestTypeDef,
    ListSystemsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUserJourneysRequestTypeDef,
    ListUserJourneysResponseTypeDef,
    StartFailureModeAssessmentRequestTypeDef,
    StartFailureModeAssessmentResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAssertionRequestTypeDef,
    UpdateAssertionResponseTypeDef,
    UpdateDependencyRequestTypeDef,
    UpdateDependencyResponseTypeDef,
    UpdateFailureModeFindingRequestTypeDef,
    UpdateFailureModeFindingResponseTypeDef,
    UpdatePolicyRequestTypeDef,
    UpdatePolicyResponseTypeDef,
    UpdateServiceFunctionRequestTypeDef,
    UpdateServiceFunctionResponseTypeDef,
    UpdateServiceRequestTypeDef,
    UpdateServiceResponseTypeDef,
    UpdateSystemRequestTypeDef,
    UpdateSystemResponseTypeDef,
    UpdateUserJourneyRequestTypeDef,
    UpdateUserJourneyResponseTypeDef,
)
from .waiter import (
    FailureModeAssessmentSuccessWaiter,
    ReportSucceededWaiter,
    ServiceAssessmentCompletedWaiter,
    ServiceResourceDiscoveryCompletedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ResilienceHubV2Client",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class ResilienceHubV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2.html#ResilienceHubV2.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ResilienceHubV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2.html#ResilienceHubV2.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#generate_presigned_url)
        """

    def create_assertion(
        self, **kwargs: Unpack[CreateAssertionRequestTypeDef]
    ) -> CreateAssertionResponseTypeDef:
        """
        Creates a resilience assertion for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/create_assertion.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#create_assertion)
        """

    def create_input_source(
        self, **kwargs: Unpack[CreateInputSourceRequestTypeDef]
    ) -> CreateInputSourceResponseTypeDef:
        """
        Creates an input source for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/create_input_source.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#create_input_source)
        """

    def create_policy(
        self, **kwargs: Unpack[CreatePolicyRequestTypeDef]
    ) -> CreatePolicyResponseTypeDef:
        """
        Creates a resilience policy that defines availability and disaster recovery
        requirements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/create_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#create_policy)
        """

    def create_report(
        self, **kwargs: Unpack[CreateReportRequestTypeDef]
    ) -> CreateReportResponseTypeDef:
        """
        On-demand report creation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/create_report.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#create_report)
        """

    def create_service(
        self, **kwargs: Unpack[CreateServiceRequestTypeDef]
    ) -> CreateServiceResponseTypeDef:
        """
        Creates a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/create_service.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#create_service)
        """

    def create_service_function(
        self, **kwargs: Unpack[CreateServiceFunctionRequestTypeDef]
    ) -> CreateServiceFunctionResponseTypeDef:
        """
        Creates a service function within a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/create_service_function.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#create_service_function)
        """

    def create_service_function_resources(
        self, **kwargs: Unpack[CreateServiceFunctionResourcesRequestTypeDef]
    ) -> CreateServiceFunctionResourcesResponseTypeDef:
        """
        Associates resources with a service function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/create_service_function_resources.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#create_service_function_resources)
        """

    def create_system(
        self, **kwargs: Unpack[CreateSystemRequestTypeDef]
    ) -> CreateSystemResponseTypeDef:
        """
        Creates a system that represents a logical grouping of services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/create_system.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#create_system)
        """

    def create_user_journey(
        self, **kwargs: Unpack[CreateUserJourneyRequestTypeDef]
    ) -> CreateUserJourneyResponseTypeDef:
        """
        Creates a user journey within a system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/create_user_journey.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#create_user_journey)
        """

    def delete_assertion(
        self, **kwargs: Unpack[DeleteAssertionRequestTypeDef]
    ) -> DeleteAssertionResponseTypeDef:
        """
        Deletes a resilience assertion from a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/delete_assertion.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#delete_assertion)
        """

    def delete_input_source(
        self, **kwargs: Unpack[DeleteInputSourceRequestTypeDef]
    ) -> DeleteInputSourceResponseTypeDef:
        """
        Deletes an input source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/delete_input_source.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#delete_input_source)
        """

    def delete_policy(
        self, **kwargs: Unpack[DeletePolicyRequestTypeDef]
    ) -> DeletePolicyResponseTypeDef:
        """
        Deletes a resilience policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/delete_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#delete_policy)
        """

    def delete_service(
        self, **kwargs: Unpack[DeleteServiceRequestTypeDef]
    ) -> DeleteServiceResponseTypeDef:
        """
        Deletes a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/delete_service.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#delete_service)
        """

    def delete_service_function(
        self, **kwargs: Unpack[DeleteServiceFunctionRequestTypeDef]
    ) -> DeleteServiceFunctionResponseTypeDef:
        """
        Deletes a service function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/delete_service_function.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#delete_service_function)
        """

    def delete_service_function_resources(
        self, **kwargs: Unpack[DeleteServiceFunctionResourcesRequestTypeDef]
    ) -> DeleteServiceFunctionResourcesResponseTypeDef:
        """
        Removes resources from a service function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/delete_service_function_resources.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#delete_service_function_resources)
        """

    def delete_system(
        self, **kwargs: Unpack[DeleteSystemRequestTypeDef]
    ) -> DeleteSystemResponseTypeDef:
        """
        Deletes a system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/delete_system.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#delete_system)
        """

    def delete_user_journey(
        self, **kwargs: Unpack[DeleteUserJourneyRequestTypeDef]
    ) -> DeleteUserJourneyResponseTypeDef:
        """
        Deletes a user journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/delete_user_journey.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#delete_user_journey)
        """

    def get_failure_mode_finding(
        self, **kwargs: Unpack[GetFailureModeFindingRequestTypeDef]
    ) -> GetFailureModeFindingResponseTypeDef:
        """
        Retrieves a finding by findingId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_failure_mode_finding.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_failure_mode_finding)
        """

    def get_policy(self, **kwargs: Unpack[GetPolicyRequestTypeDef]) -> GetPolicyResponseTypeDef:
        """
        Retrieves a resilience policy by ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_policy)
        """

    def get_service(self, **kwargs: Unpack[GetServiceRequestTypeDef]) -> GetServiceResponseTypeDef:
        """
        Retrieves a service by ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_service.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_service)
        """

    def get_system(self, **kwargs: Unpack[GetSystemRequestTypeDef]) -> GetSystemResponseTypeDef:
        """
        Retrieves a system by ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_system.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_system)
        """

    def get_user_journey(
        self, **kwargs: Unpack[GetUserJourneyRequestTypeDef]
    ) -> GetUserJourneyResponseTypeDef:
        """
        Retrieves a user journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_user_journey.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_user_journey)
        """

    def import_app(self, **kwargs: Unpack[ImportAppRequestTypeDef]) -> ImportAppResponseTypeDef:
        """
        Imports a V1 app into the V2 resource model, creating a service with the same
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/import_app.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#import_app)
        """

    def import_policy(
        self, **kwargs: Unpack[ImportPolicyRequestTypeDef]
    ) -> ImportPolicyResponseTypeDef:
        """
        Imports a V1 policy into V2, mapping RTO/RPO values from V1 scenarios.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/import_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#import_policy)
        """

    def list_assertions(
        self, **kwargs: Unpack[ListAssertionsRequestTypeDef]
    ) -> ListAssertionsResponseTypeDef:
        """
        Lists resilience assertions for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_assertions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_assertions)
        """

    def list_dependencies(
        self, **kwargs: Unpack[ListDependenciesRequestTypeDef]
    ) -> ListDependenciesResponseTypeDef:
        """
        Lists dependencies discovered for services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_dependencies.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_dependencies)
        """

    def list_failure_mode_assessments(
        self, **kwargs: Unpack[ListFailureModeAssessmentsRequestTypeDef]
    ) -> ListFailureModeAssessmentsResponseTypeDef:
        """
        Lists failure mode assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_failure_mode_assessments.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_failure_mode_assessments)
        """

    def list_failure_mode_findings(
        self, **kwargs: Unpack[ListFailureModeFindingsRequestTypeDef]
    ) -> ListFailureModeFindingsResponseTypeDef:
        """
        List findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_failure_mode_findings.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_failure_mode_findings)
        """

    def list_input_sources(
        self, **kwargs: Unpack[ListInputSourcesRequestTypeDef]
    ) -> ListInputSourcesResponseTypeDef:
        """
        Lists input sources for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_input_sources.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_input_sources)
        """

    def list_policies(
        self, **kwargs: Unpack[ListPoliciesRequestTypeDef]
    ) -> ListPoliciesResponseTypeDef:
        """
        Lists resilience policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_policies.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_policies)
        """

    def list_reports(
        self, **kwargs: Unpack[ListReportsRequestTypeDef]
    ) -> ListReportsResponseTypeDef:
        """
        List reports for a service, or all reports owned by the account if serviceArn
        is not provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_reports.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_reports)
        """

    def list_resources(
        self, **kwargs: Unpack[ListResourcesRequestTypeDef]
    ) -> ListResourcesResponseTypeDef:
        """
        List resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_resources.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_resources)
        """

    def list_service_events(
        self, **kwargs: Unpack[ListServiceEventsRequestTypeDef]
    ) -> ListServiceEventsResponseTypeDef:
        """
        Lists events for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_service_events.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_service_events)
        """

    def list_service_functions(
        self, **kwargs: Unpack[ListServiceFunctionsRequestTypeDef]
    ) -> ListServiceFunctionsResponseTypeDef:
        """
        Lists service functions for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_service_functions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_service_functions)
        """

    def list_service_topology_edges(
        self, **kwargs: Unpack[ListServiceTopologyEdgesRequestTypeDef]
    ) -> ListServiceTopologyEdgesResponseTypeDef:
        """
        Lists topology edges for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_service_topology_edges.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_service_topology_edges)
        """

    def list_services(
        self, **kwargs: Unpack[ListServicesRequestTypeDef]
    ) -> ListServicesResponseTypeDef:
        """
        Lists services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_services.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_services)
        """

    def list_system_events(
        self, **kwargs: Unpack[ListSystemEventsRequestTypeDef]
    ) -> ListSystemEventsResponseTypeDef:
        """
        Lists events for a system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_system_events.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_system_events)
        """

    def list_systems(
        self, **kwargs: Unpack[ListSystemsRequestTypeDef]
    ) -> ListSystemsResponseTypeDef:
        """
        Lists systems.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_systems.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_systems)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_tags_for_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_tags_for_resource)
        """

    def list_user_journeys(
        self, **kwargs: Unpack[ListUserJourneysRequestTypeDef]
    ) -> ListUserJourneysResponseTypeDef:
        """
        Lists user journeys for a system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/list_user_journeys.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#list_user_journeys)
        """

    def start_failure_mode_assessment(
        self, **kwargs: Unpack[StartFailureModeAssessmentRequestTypeDef]
    ) -> StartFailureModeAssessmentResponseTypeDef:
        """
        Starts a failure mode assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/start_failure_mode_assessment.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#start_failure_mode_assessment)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/tag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/untag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#untag_resource)
        """

    def update_assertion(
        self, **kwargs: Unpack[UpdateAssertionRequestTypeDef]
    ) -> UpdateAssertionResponseTypeDef:
        """
        Updates a resilience assertion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/update_assertion.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#update_assertion)
        """

    def update_dependency(
        self, **kwargs: Unpack[UpdateDependencyRequestTypeDef]
    ) -> UpdateDependencyResponseTypeDef:
        """
        Updates a dependency classification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/update_dependency.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#update_dependency)
        """

    def update_failure_mode_finding(
        self, **kwargs: Unpack[UpdateFailureModeFindingRequestTypeDef]
    ) -> UpdateFailureModeFindingResponseTypeDef:
        """
        Updates an existing finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/update_failure_mode_finding.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#update_failure_mode_finding)
        """

    def update_policy(
        self, **kwargs: Unpack[UpdatePolicyRequestTypeDef]
    ) -> UpdatePolicyResponseTypeDef:
        """
        Updates an existing resilience policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/update_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#update_policy)
        """

    def update_service(
        self, **kwargs: Unpack[UpdateServiceRequestTypeDef]
    ) -> UpdateServiceResponseTypeDef:
        """
        Updates an existing service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/update_service.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#update_service)
        """

    def update_service_function(
        self, **kwargs: Unpack[UpdateServiceFunctionRequestTypeDef]
    ) -> UpdateServiceFunctionResponseTypeDef:
        """
        Updates a service function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/update_service_function.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#update_service_function)
        """

    def update_system(
        self, **kwargs: Unpack[UpdateSystemRequestTypeDef]
    ) -> UpdateSystemResponseTypeDef:
        """
        Updates an existing system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/update_system.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#update_system)
        """

    def update_user_journey(
        self, **kwargs: Unpack[UpdateUserJourneyRequestTypeDef]
    ) -> UpdateUserJourneyResponseTypeDef:
        """
        Updates an existing user journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/update_user_journey.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#update_user_journey)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_assertions"]
    ) -> ListAssertionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dependencies"]
    ) -> ListDependenciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_failure_mode_assessments"]
    ) -> ListFailureModeAssessmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_failure_mode_findings"]
    ) -> ListFailureModeFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_input_sources"]
    ) -> ListInputSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policies"]
    ) -> ListPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_reports"]
    ) -> ListReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resources"]
    ) -> ListResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_events"]
    ) -> ListServiceEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_functions"]
    ) -> ListServiceFunctionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_topology_edges"]
    ) -> ListServiceTopologyEdgesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_services"]
    ) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_system_events"]
    ) -> ListSystemEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_systems"]
    ) -> ListSystemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_user_journeys"]
    ) -> ListUserJourneysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["failure_mode_assessment_success"]
    ) -> FailureModeAssessmentSuccessWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["report_succeeded"]
    ) -> ReportSucceededWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["service_assessment_completed"]
    ) -> ServiceAssessmentCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["service_resource_discovery_completed"]
    ) -> ServiceResourceDiscoveryCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/client/#get_waiter)
        """
