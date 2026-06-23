"""
Type annotations for application-signals service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_application_signals.client import CloudWatchApplicationSignalsClient

    session = Session()
    client: CloudWatchApplicationSignalsClient = session.client("application-signals")
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
    GetInstrumentationConfigurationStatusPaginator,
    ListEntityEventsPaginator,
    ListInstrumentationConfigurationsPaginator,
    ListServiceDependenciesPaginator,
    ListServiceDependentsPaginator,
    ListServiceLevelObjectiveExclusionWindowsPaginator,
    ListServiceLevelObjectivesPaginator,
    ListServiceOperationsPaginator,
    ListServicesPaginator,
    ListServiceStatesPaginator,
)
from .type_defs import (
    BatchDeleteInstrumentationConfigurationsRequestTypeDef,
    BatchDeleteInstrumentationConfigurationsResponseTypeDef,
    BatchGetServiceLevelObjectiveBudgetReportInputTypeDef,
    BatchGetServiceLevelObjectiveBudgetReportOutputTypeDef,
    BatchUpdateExclusionWindowsInputTypeDef,
    BatchUpdateExclusionWindowsOutputTypeDef,
    CreateInstrumentationConfigurationRequestTypeDef,
    CreateInstrumentationConfigurationResponseTypeDef,
    CreateServiceLevelObjectiveInputTypeDef,
    CreateServiceLevelObjectiveOutputTypeDef,
    DeleteInstrumentationConfigurationRequestTypeDef,
    DeleteInstrumentationConfigurationResponseTypeDef,
    DeleteServiceLevelObjectiveInputTypeDef,
    GetInstrumentationConfigurationRequestTypeDef,
    GetInstrumentationConfigurationResponseTypeDef,
    GetInstrumentationConfigurationStatusRequestTypeDef,
    GetInstrumentationConfigurationStatusResponseTypeDef,
    GetServiceInputTypeDef,
    GetServiceLevelObjectiveInputTypeDef,
    GetServiceLevelObjectiveOutputTypeDef,
    GetServiceOutputTypeDef,
    InstrumentationConfigurationsPageTypeDef,
    ListAuditFindingsInputTypeDef,
    ListAuditFindingsOutputTypeDef,
    ListEntityEventsInputTypeDef,
    ListEntityEventsOutputTypeDef,
    ListGroupingAttributeDefinitionsInputTypeDef,
    ListGroupingAttributeDefinitionsOutputTypeDef,
    ListInstrumentationConfigurationsRequestTypeDef,
    ListServiceDependenciesInputTypeDef,
    ListServiceDependenciesOutputTypeDef,
    ListServiceDependentsInputTypeDef,
    ListServiceDependentsOutputTypeDef,
    ListServiceLevelObjectiveExclusionWindowsInputTypeDef,
    ListServiceLevelObjectiveExclusionWindowsOutputTypeDef,
    ListServiceLevelObjectivesInputTypeDef,
    ListServiceLevelObjectivesOutputTypeDef,
    ListServiceOperationsInputTypeDef,
    ListServiceOperationsOutputTypeDef,
    ListServicesInputTypeDef,
    ListServicesOutputTypeDef,
    ListServiceStatesInputTypeDef,
    ListServiceStatesOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutGroupingConfigurationInputTypeDef,
    PutGroupingConfigurationOutputTypeDef,
    ReportInstrumentationConfigurationStatusRequestTypeDef,
    ReportInstrumentationConfigurationStatusResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateServiceLevelObjectiveInputTypeDef,
    UpdateServiceLevelObjectiveOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CloudWatchApplicationSignalsClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class CloudWatchApplicationSignalsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchApplicationSignalsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#generate_presigned_url)
        """

    def batch_delete_instrumentation_configurations(
        self, **kwargs: Unpack[BatchDeleteInstrumentationConfigurationsRequestTypeDef]
    ) -> BatchDeleteInstrumentationConfigurationsResponseTypeDef:
        """
        Deletes multiple instrumentation configurations in a single request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/batch_delete_instrumentation_configurations.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#batch_delete_instrumentation_configurations)
        """

    def batch_get_service_level_objective_budget_report(
        self, **kwargs: Unpack[BatchGetServiceLevelObjectiveBudgetReportInputTypeDef]
    ) -> BatchGetServiceLevelObjectiveBudgetReportOutputTypeDef:
        """
        Use this operation to retrieve one or more <i>service level objective (SLO)
        budget reports</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/batch_get_service_level_objective_budget_report.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#batch_get_service_level_objective_budget_report)
        """

    def batch_update_exclusion_windows(
        self, **kwargs: Unpack[BatchUpdateExclusionWindowsInputTypeDef]
    ) -> BatchUpdateExclusionWindowsOutputTypeDef:
        """
        Add or remove time window exclusions for one or more Service Level Objectives
        (SLOs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/batch_update_exclusion_windows.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#batch_update_exclusion_windows)
        """

    def create_instrumentation_configuration(
        self, **kwargs: Unpack[CreateInstrumentationConfigurationRequestTypeDef]
    ) -> CreateInstrumentationConfigurationResponseTypeDef:
        """
        Creates a dynamic instrumentation configuration for a specific code or endpoint
        location within a service and environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/create_instrumentation_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#create_instrumentation_configuration)
        """

    def create_service_level_objective(
        self, **kwargs: Unpack[CreateServiceLevelObjectiveInputTypeDef]
    ) -> CreateServiceLevelObjectiveOutputTypeDef:
        """
        Creates a service level objective (SLO), which can help you ensure that your
        critical business operations are meeting customer expectations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/create_service_level_objective.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#create_service_level_objective)
        """

    def delete_grouping_configuration(self) -> dict[str, Any]:
        """
        Deletes the grouping configuration for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/delete_grouping_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#delete_grouping_configuration)
        """

    def delete_instrumentation_configuration(
        self, **kwargs: Unpack[DeleteInstrumentationConfigurationRequestTypeDef]
    ) -> DeleteInstrumentationConfigurationResponseTypeDef:
        """
        Deletes the specified instrumentation configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/delete_instrumentation_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#delete_instrumentation_configuration)
        """

    def delete_service_level_objective(
        self, **kwargs: Unpack[DeleteServiceLevelObjectiveInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the specified service level objective.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/delete_service_level_objective.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#delete_service_level_objective)
        """

    def get_instrumentation_configuration(
        self, **kwargs: Unpack[GetInstrumentationConfigurationRequestTypeDef]
    ) -> GetInstrumentationConfigurationResponseTypeDef:
        """
        Returns the details of a single instrumentation configuration identified by
        service, environment, signal type, and location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_instrumentation_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_instrumentation_configuration)
        """

    def get_instrumentation_configuration_status(
        self, **kwargs: Unpack[GetInstrumentationConfigurationStatusRequestTypeDef]
    ) -> GetInstrumentationConfigurationStatusResponseTypeDef:
        """
        Retrieves the status history for a single instrumentation configuration during
        a specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_instrumentation_configuration_status.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_instrumentation_configuration_status)
        """

    def get_service(self, **kwargs: Unpack[GetServiceInputTypeDef]) -> GetServiceOutputTypeDef:
        """
        Returns information about a service discovered by Application Signals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_service.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_service)
        """

    def get_service_level_objective(
        self, **kwargs: Unpack[GetServiceLevelObjectiveInputTypeDef]
    ) -> GetServiceLevelObjectiveOutputTypeDef:
        """
        Returns information about one SLO created in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_service_level_objective.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_service_level_objective)
        """

    def list_audit_findings(
        self, **kwargs: Unpack[ListAuditFindingsInputTypeDef]
    ) -> ListAuditFindingsOutputTypeDef:
        """
        Returns a list of audit findings that provide automated analysis of service
        behavior and root cause analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_audit_findings.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_audit_findings)
        """

    def list_entity_events(
        self, **kwargs: Unpack[ListEntityEventsInputTypeDef]
    ) -> ListEntityEventsOutputTypeDef:
        """
        Returns a list of change events for a specific entity, such as deployments,
        configuration changes, or other state-changing activities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_entity_events.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_entity_events)
        """

    def list_grouping_attribute_definitions(
        self, **kwargs: Unpack[ListGroupingAttributeDefinitionsInputTypeDef]
    ) -> ListGroupingAttributeDefinitionsOutputTypeDef:
        """
        Returns the current grouping configuration for this account, including all
        custom grouping attribute definitions that have been configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_grouping_attribute_definitions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_grouping_attribute_definitions)
        """

    def list_instrumentation_configurations(
        self, **kwargs: Unpack[ListInstrumentationConfigurationsRequestTypeDef]
    ) -> InstrumentationConfigurationsPageTypeDef:
        """
        Returns all active instrumentation configurations for a service and environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_instrumentation_configurations.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_instrumentation_configurations)
        """

    def list_service_dependencies(
        self, **kwargs: Unpack[ListServiceDependenciesInputTypeDef]
    ) -> ListServiceDependenciesOutputTypeDef:
        """
        Returns a list of service dependencies of the service that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_dependencies.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_service_dependencies)
        """

    def list_service_dependents(
        self, **kwargs: Unpack[ListServiceDependentsInputTypeDef]
    ) -> ListServiceDependentsOutputTypeDef:
        """
        Returns the list of dependents that invoked the specified service during the
        provided time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_dependents.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_service_dependents)
        """

    def list_service_level_objective_exclusion_windows(
        self, **kwargs: Unpack[ListServiceLevelObjectiveExclusionWindowsInputTypeDef]
    ) -> ListServiceLevelObjectiveExclusionWindowsOutputTypeDef:
        """
        Retrieves all exclusion windows configured for a specific SLO.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_level_objective_exclusion_windows.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_service_level_objective_exclusion_windows)
        """

    def list_service_level_objectives(
        self, **kwargs: Unpack[ListServiceLevelObjectivesInputTypeDef]
    ) -> ListServiceLevelObjectivesOutputTypeDef:
        """
        Returns a list of SLOs created in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_level_objectives.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_service_level_objectives)
        """

    def list_service_operations(
        self, **kwargs: Unpack[ListServiceOperationsInputTypeDef]
    ) -> ListServiceOperationsOutputTypeDef:
        """
        Returns a list of the <i>operations</i> of this service that have been
        discovered by Application Signals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_operations.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_service_operations)
        """

    def list_service_states(
        self, **kwargs: Unpack[ListServiceStatesInputTypeDef]
    ) -> ListServiceStatesOutputTypeDef:
        """
        Returns information about the last deployment and other change states of
        services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_service_states.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_service_states)
        """

    def list_services(
        self, **kwargs: Unpack[ListServicesInputTypeDef]
    ) -> ListServicesOutputTypeDef:
        """
        Returns a list of services that have been discovered by Application Signals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_services.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_services)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with a CloudWatch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/list_tags_for_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#list_tags_for_resource)
        """

    def put_grouping_configuration(
        self, **kwargs: Unpack[PutGroupingConfigurationInputTypeDef]
    ) -> PutGroupingConfigurationOutputTypeDef:
        """
        Creates or updates the grouping configuration for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/put_grouping_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#put_grouping_configuration)
        """

    def report_instrumentation_configuration_status(
        self, **kwargs: Unpack[ReportInstrumentationConfigurationStatusRequestTypeDef]
    ) -> ReportInstrumentationConfigurationStatusResponseTypeDef:
        """
        Reports the status of one or more instrumentation configurations from SDK
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/report_instrumentation_configuration_status.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#report_instrumentation_configuration_status)
        """

    def start_discovery(self) -> dict[str, Any]:
        """
        Enables this Amazon Web Services account to be able to use CloudWatch
        Application Signals by creating the
        <i>AWSServiceRoleForCloudWatchApplicationSignals</i> service-linked role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/start_discovery.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#start_discovery)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch
        resource, such as a service level objective.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/tag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/untag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#untag_resource)
        """

    def update_service_level_objective(
        self, **kwargs: Unpack[UpdateServiceLevelObjectiveInputTypeDef]
    ) -> UpdateServiceLevelObjectiveOutputTypeDef:
        """
        Updates an existing service level objective (SLO).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/update_service_level_objective.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#update_service_level_objective)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_instrumentation_configuration_status"]
    ) -> GetInstrumentationConfigurationStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_entity_events"]
    ) -> ListEntityEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_instrumentation_configurations"]
    ) -> ListInstrumentationConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_dependencies"]
    ) -> ListServiceDependenciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_dependents"]
    ) -> ListServiceDependentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_level_objective_exclusion_windows"]
    ) -> ListServiceLevelObjectiveExclusionWindowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_level_objectives"]
    ) -> ListServiceLevelObjectivesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_operations"]
    ) -> ListServiceOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_states"]
    ) -> ListServiceStatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_services"]
    ) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/client/#get_paginator)
        """
