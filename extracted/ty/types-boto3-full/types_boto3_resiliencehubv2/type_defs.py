"""
Type annotations for resiliencehubv2 service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_resiliencehubv2/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_resiliencehubv2.type_defs import AchievabilityTypeDef

    data: AchievabilityTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    AchievabilityStatusType,
    ActorTypeType,
    AssertionSourceType,
    AssessmentErrorCodeType,
    AssessmentStatusType,
    AssessmentStepType,
    DependencyCriticalityType,
    DependencyDiscoveryInputType,
    DependencyDiscoveryStatusType,
    FailureCategoryType,
    FindingSeverityType,
    FindingStatusType,
    InputSourceTypeType,
    MultiAzDisasterRecoveryApproachType,
    MultiRegionDisasterRecoveryApproachType,
    PolicyComponentType,
    PolicyValueSourceType,
    QueryGranularityType,
    ReportGenerationErrorCodeType,
    ReportGenerationStatusType,
    ResourceDiscoveryErrorCodeType,
    ResourceDiscoveryRunStatusType,
    ServiceEventTypeType,
    ServiceFunctionCriticalityType,
    ServiceFunctionSourceType,
    SystemEventTypeType,
    TopologyTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AchievabilityTypeDef",
    "AssertionCreatedMetadataTypeDef",
    "AssertionDeletedMetadataTypeDef",
    "AssertionTypeDef",
    "AssertionUpdatedMetadataTypeDef",
    "AssessmentCostTypeDef",
    "AssessmentSummaryTypeDef",
    "AssociatedSystemOutputTypeDef",
    "AssociatedSystemTypeDef",
    "AssociatedSystemUnionTypeDef",
    "AvailabilitySloTypeDef",
    "CreateAssertionRequestTypeDef",
    "CreateAssertionResponseTypeDef",
    "CreateInputSourceRequestTypeDef",
    "CreateInputSourceResponseTypeDef",
    "CreatePolicyRequestTypeDef",
    "CreatePolicyResponseTypeDef",
    "CreateReportRequestTypeDef",
    "CreateReportResponseTypeDef",
    "CreateServiceFunctionRequestTypeDef",
    "CreateServiceFunctionResourcesRequestTypeDef",
    "CreateServiceFunctionResourcesResponseTypeDef",
    "CreateServiceFunctionResponseTypeDef",
    "CreateServiceRequestTypeDef",
    "CreateServiceResponseTypeDef",
    "CreateSystemRequestTypeDef",
    "CreateSystemResponseTypeDef",
    "CreateUserJourneyRequestTypeDef",
    "CreateUserJourneyResponseTypeDef",
    "CrossAccountRoleTypeDef",
    "DataRecoveryTargetsTypeDef",
    "DeleteAssertionRequestTypeDef",
    "DeleteAssertionResponseTypeDef",
    "DeleteInputSourceRequestTypeDef",
    "DeleteInputSourceResponseTypeDef",
    "DeletePolicyRequestTypeDef",
    "DeletePolicyResponseTypeDef",
    "DeleteServiceFunctionRequestTypeDef",
    "DeleteServiceFunctionResourcesRequestTypeDef",
    "DeleteServiceFunctionResourcesResponseTypeDef",
    "DeleteServiceFunctionResponseTypeDef",
    "DeleteServiceRequestTypeDef",
    "DeleteServiceResponseTypeDef",
    "DeleteSystemRequestTypeDef",
    "DeleteSystemResponseTypeDef",
    "DeleteUserJourneyRequestTypeDef",
    "DeleteUserJourneyResponseTypeDef",
    "DependencyDiscoveryConfigTypeDef",
    "DependencySummaryTypeDef",
    "DisasterRecoverySourceTypeDef",
    "EdgePropertySummaryTypeDef",
    "EffectivePolicyValuesTypeDef",
    "EksSourceOutputTypeDef",
    "EksSourceTypeDef",
    "EksSourceUnionTypeDef",
    "EventActorTypeDef",
    "FailedReportOutputTypeDef",
    "FindingSummaryTypeDef",
    "FindingTypeDef",
    "GetFailureModeFindingRequestTypeDef",
    "GetFailureModeFindingResponseTypeDef",
    "GetPolicyRequestTypeDef",
    "GetPolicyResponseTypeDef",
    "GetServiceRequestTypeDef",
    "GetServiceRequestWaitExtraTypeDef",
    "GetServiceRequestWaitTypeDef",
    "GetServiceResponseTypeDef",
    "GetSystemRequestTypeDef",
    "GetSystemResponseTypeDef",
    "GetUserJourneyRequestTypeDef",
    "GetUserJourneyResponseTypeDef",
    "ImportAppRequestTypeDef",
    "ImportAppResponseTypeDef",
    "ImportPolicyRequestTypeDef",
    "ImportPolicyResponseTypeDef",
    "InfrastructureAndCodeRecommendationTypeDef",
    "InputSourceSummaryTypeDef",
    "InputSourceTypeDef",
    "ListAssertionsRequestPaginateTypeDef",
    "ListAssertionsRequestTypeDef",
    "ListAssertionsResponseTypeDef",
    "ListDependenciesRequestPaginateTypeDef",
    "ListDependenciesRequestTypeDef",
    "ListDependenciesResponseTypeDef",
    "ListFailureModeAssessmentsRequestPaginateTypeDef",
    "ListFailureModeAssessmentsRequestTypeDef",
    "ListFailureModeAssessmentsRequestWaitTypeDef",
    "ListFailureModeAssessmentsResponseTypeDef",
    "ListFailureModeFindingsRequestPaginateTypeDef",
    "ListFailureModeFindingsRequestTypeDef",
    "ListFailureModeFindingsResponseTypeDef",
    "ListInputSourcesRequestPaginateTypeDef",
    "ListInputSourcesRequestTypeDef",
    "ListInputSourcesResponseTypeDef",
    "ListPoliciesRequestPaginateTypeDef",
    "ListPoliciesRequestTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListReportsRequestPaginateTypeDef",
    "ListReportsRequestTypeDef",
    "ListReportsRequestWaitTypeDef",
    "ListReportsResponseTypeDef",
    "ListResourcesRequestPaginateTypeDef",
    "ListResourcesRequestTypeDef",
    "ListResourcesResponseTypeDef",
    "ListServiceEventsRequestPaginateTypeDef",
    "ListServiceEventsRequestTypeDef",
    "ListServiceEventsResponseTypeDef",
    "ListServiceFunctionsRequestPaginateTypeDef",
    "ListServiceFunctionsRequestTypeDef",
    "ListServiceFunctionsResponseTypeDef",
    "ListServiceTopologyEdgesRequestPaginateTypeDef",
    "ListServiceTopologyEdgesRequestTypeDef",
    "ListServiceTopologyEdgesResponseTypeDef",
    "ListServicesRequestPaginateTypeDef",
    "ListServicesRequestTypeDef",
    "ListServicesResponseTypeDef",
    "ListSystemEventsRequestPaginateTypeDef",
    "ListSystemEventsRequestTypeDef",
    "ListSystemEventsResponseTypeDef",
    "ListSystemsRequestPaginateTypeDef",
    "ListSystemsRequestTypeDef",
    "ListSystemsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUserJourneysRequestPaginateTypeDef",
    "ListUserJourneysRequestTypeDef",
    "ListUserJourneysResponseTypeDef",
    "MultiAzTargetsTypeDef",
    "MultiRegionTargetsTypeDef",
    "ObservabilityRecommendationTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionModelOutputTypeDef",
    "PermissionModelTypeDef",
    "PermissionModelUnionTypeDef",
    "PolicySummaryTypeDef",
    "PolicyTypeDef",
    "QueryDataPointTypeDef",
    "QueryRangeTypeDef",
    "ReportGenerationResultTypeDef",
    "ReportOutputConfigurationTypeDef",
    "ReportOutputTypeDef",
    "ResourceConfigurationTypeDef",
    "ResourceDiscoveryStatusTypeDef",
    "ResourceTagOutputTypeDef",
    "ResourceTagTypeDef",
    "ResourceTagUnionTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "S3ReportOutputConfigurationTypeDef",
    "S3ReportOutputTypeDef",
    "ServiceAchievabilityUpdatedMetadataTypeDef",
    "ServiceEventDetailsTypeDef",
    "ServiceEventMetadataTypeDef",
    "ServiceEventTypeDef",
    "ServiceFunctionCreatedMetadataTypeDef",
    "ServiceFunctionDeletedMetadataTypeDef",
    "ServiceFunctionResourcesAddedMetadataTypeDef",
    "ServiceFunctionResourcesRemovedMetadataTypeDef",
    "ServiceFunctionTypeDef",
    "ServiceFunctionUpdatedMetadataTypeDef",
    "ServicePolicyAssociatedMetadataTypeDef",
    "ServicePolicyDisassociatedMetadataTypeDef",
    "ServiceReferenceChangesTypeDef",
    "ServiceReferenceTypeDef",
    "ServiceReportConfigurationOutputTypeDef",
    "ServiceReportConfigurationTypeDef",
    "ServiceReportConfigurationUnionTypeDef",
    "ServiceResourceTypeDef",
    "ServiceResourcesAssociatedMetadataTypeDef",
    "ServiceResourcesDisassociatedMetadataTypeDef",
    "ServiceSummaryTypeDef",
    "ServiceSystemAssociatedMetadataTypeDef",
    "ServiceSystemDisassociatedMetadataTypeDef",
    "ServiceTopologyEdgeSummaryTypeDef",
    "ServiceTypeDef",
    "ServiceWorkflowUpdatedMetadataTypeDef",
    "SloSourceTypeDef",
    "StartFailureModeAssessmentRequestTypeDef",
    "StartFailureModeAssessmentResponseTypeDef",
    "StringChangeTypeDef",
    "SystemEventDetailsTypeDef",
    "SystemEventMetadataTypeDef",
    "SystemEventTypeDef",
    "SystemPolicyAssociatedMetadataTypeDef",
    "SystemPolicyDisassociatedMetadataTypeDef",
    "SystemServiceAssociatedMetadataTypeDef",
    "SystemServiceDisassociatedMetadataTypeDef",
    "SystemSummaryTypeDef",
    "SystemTypeDef",
    "SystemUserJourneyCreatedMetadataTypeDef",
    "SystemUserJourneyDeletedMetadataTypeDef",
    "SystemUserJourneyUpdatedMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "TargetSourceTypeDef",
    "TestingRecommendationTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAssertionRequestTypeDef",
    "UpdateAssertionResponseTypeDef",
    "UpdateDependencyRequestTypeDef",
    "UpdateDependencyResponseTypeDef",
    "UpdateFailureModeFindingRequestTypeDef",
    "UpdateFailureModeFindingResponseTypeDef",
    "UpdatePolicyRequestTypeDef",
    "UpdatePolicyResponseTypeDef",
    "UpdateServiceFunctionRequestTypeDef",
    "UpdateServiceFunctionResponseTypeDef",
    "UpdateServiceRequestTypeDef",
    "UpdateServiceResponseTypeDef",
    "UpdateSystemRequestTypeDef",
    "UpdateSystemResponseTypeDef",
    "UpdateUserJourneyRequestTypeDef",
    "UpdateUserJourneyResponseTypeDef",
    "UserJourneyChangesTypeDef",
    "UserJourneySummaryTypeDef",
    "UserJourneyTypeDef",
    "WaiterConfigTypeDef",
)


class AchievabilityTypeDef(TypedDict):
    availabilitySlo: NotRequired[AchievabilityStatusType]
    multiAzRtoRpo: NotRequired[AchievabilityStatusType]
    multiRegionRtoRpo: NotRequired[AchievabilityStatusType]


class AssertionCreatedMetadataTypeDef(TypedDict):
    assertionId: NotRequired[str]
    assertionName: NotRequired[str]


class AssertionDeletedMetadataTypeDef(TypedDict):
    assertionId: NotRequired[str]
    assertionName: NotRequired[str]


class AssertionTypeDef(TypedDict):
    serviceArn: str
    assertionId: str
    text: str
    source: AssertionSourceType
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class AssertionUpdatedMetadataTypeDef(TypedDict):
    assertionId: NotRequired[str]
    assertionName: NotRequired[str]


class AssessmentCostTypeDef(TypedDict):
    amount: NotRequired[float]
    currency: NotRequired[Literal["USD"]]


class AssociatedSystemOutputTypeDef(TypedDict):
    systemArn: str
    systemName: NotRequired[str]
    userJourneyIds: NotRequired[list[str]]


class AssociatedSystemTypeDef(TypedDict):
    systemArn: str
    systemName: NotRequired[str]
    userJourneyIds: NotRequired[Sequence[str]]


class AvailabilitySloTypeDef(TypedDict):
    target: NotRequired[float]


class CreateAssertionRequestTypeDef(TypedDict):
    serviceArn: str
    text: str
    clientToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DataRecoveryTargetsTypeDef(TypedDict):
    timeBetweenBackupsInMinutes: NotRequired[int]


class MultiAzTargetsTypeDef(TypedDict):
    rtoInMinutes: NotRequired[int]
    rpoInMinutes: NotRequired[int]
    disasterRecoveryApproach: NotRequired[MultiAzDisasterRecoveryApproachType]


class MultiRegionTargetsTypeDef(TypedDict):
    rtoInMinutes: NotRequired[int]
    rpoInMinutes: NotRequired[int]
    disasterRecoveryApproach: NotRequired[MultiRegionDisasterRecoveryApproachType]


class CreateReportRequestTypeDef(TypedDict):
    serviceArn: str
    reportType: Literal["FAILURE_MODE"]
    clientToken: NotRequired[str]


class CreateServiceFunctionRequestTypeDef(TypedDict):
    name: str
    serviceArn: str
    criticality: ServiceFunctionCriticalityType
    description: NotRequired[str]
    clientToken: NotRequired[str]


class CreateServiceFunctionResourcesRequestTypeDef(TypedDict):
    serviceArn: str
    serviceFunctionId: str
    resources: Sequence[str]


class ServiceFunctionTypeDef(TypedDict):
    serviceArn: str
    serviceFunctionId: str
    name: str
    criticality: ServiceFunctionCriticalityType
    description: NotRequired[str]
    resourceCount: NotRequired[int]
    source: NotRequired[ServiceFunctionSourceType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class CreateSystemRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    sharingEnabled: NotRequired[bool]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class SystemTypeDef(TypedDict):
    systemArn: str
    systemId: str
    name: str
    description: NotRequired[str]
    sharingEnabled: NotRequired[bool]
    tags: NotRequired[dict[str, str]]
    kmsKeyId: NotRequired[str]
    organizationId: NotRequired[str]
    ouId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class CreateUserJourneyRequestTypeDef(TypedDict):
    systemArn: str
    name: str
    description: NotRequired[str]
    policyArn: NotRequired[str]
    clientToken: NotRequired[str]


class UserJourneyTypeDef(TypedDict):
    userJourneyId: str
    name: str
    description: NotRequired[str]
    policyArn: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class CrossAccountRoleTypeDef(TypedDict):
    crossAccountRoleArn: str
    externalId: NotRequired[str]


class DeleteAssertionRequestTypeDef(TypedDict):
    serviceArn: str
    assertionId: str


class DeleteInputSourceRequestTypeDef(TypedDict):
    serviceArn: str
    inputSourceId: str


class DeletePolicyRequestTypeDef(TypedDict):
    policyArn: str


class DeleteServiceFunctionRequestTypeDef(TypedDict):
    serviceArn: str
    serviceFunctionId: str


class DeleteServiceFunctionResourcesRequestTypeDef(TypedDict):
    serviceArn: str
    serviceFunctionId: str
    resources: Sequence[str]


class DeleteServiceRequestTypeDef(TypedDict):
    serviceArn: str


class DeleteSystemRequestTypeDef(TypedDict):
    systemArn: str


class DeleteUserJourneyRequestTypeDef(TypedDict):
    systemArn: str
    userJourneyId: str


class DependencyDiscoveryConfigTypeDef(TypedDict):
    status: DependencyDiscoveryStatusType
    updatedAt: NotRequired[datetime]


class DisasterRecoverySourceTypeDef(TypedDict):
    value: NotRequired[str]
    policyName: NotRequired[str]
    source: NotRequired[PolicyValueSourceType]


class EdgePropertySummaryTypeDef(TypedDict):
    topologyType: NotRequired[TopologyTypeType]
    label: NotRequired[str]


class SloSourceTypeDef(TypedDict):
    value: NotRequired[float]
    policyName: NotRequired[str]
    source: NotRequired[PolicyValueSourceType]


class TargetSourceTypeDef(TypedDict):
    value: NotRequired[int]
    policyName: NotRequired[str]
    source: NotRequired[PolicyValueSourceType]


class EksSourceOutputTypeDef(TypedDict):
    clusterArn: str
    namespaces: list[str]


class EksSourceTypeDef(TypedDict):
    clusterArn: str
    namespaces: Sequence[str]


EventActorTypeDef = TypedDict(
    "EventActorTypeDef",
    {
        "type": ActorTypeType,
        "principalId": str,
        "accountId": NotRequired[str],
        "userName": NotRequired[str],
    },
)


class FailedReportOutputTypeDef(TypedDict):
    errorCode: ReportGenerationErrorCodeType
    errorMessage: NotRequired[str]


class FindingSummaryTypeDef(TypedDict):
    serviceArn: NotRequired[str]
    findingId: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    failureCategory: NotRequired[FailureCategoryType]
    severity: NotRequired[FindingSeverityType]
    status: NotRequired[FindingStatusType]
    policyComponent: NotRequired[PolicyComponentType]
    updatedAt: NotRequired[datetime]


class InfrastructureAndCodeRecommendationTypeDef(TypedDict):
    suggestedChanges: NotRequired[list[str]]


class ObservabilityRecommendationTypeDef(TypedDict):
    suggestedChanges: NotRequired[list[str]]


class TestingRecommendationTypeDef(TypedDict):
    suggestedChanges: NotRequired[list[str]]


class GetFailureModeFindingRequestTypeDef(TypedDict):
    findingId: str
    serviceArn: str


class GetPolicyRequestTypeDef(TypedDict):
    policyArn: str


class GetServiceRequestTypeDef(TypedDict):
    serviceArn: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class GetSystemRequestTypeDef(TypedDict):
    systemArn: str


class GetUserJourneyRequestTypeDef(TypedDict):
    systemArn: str
    userJourneyId: str


class ResourceTagOutputTypeDef(TypedDict):
    key: str
    values: list[str]


InputSourceTypeDef = TypedDict(
    "InputSourceTypeDef",
    {
        "identifier": str,
        "type": InputSourceTypeType,
    },
)


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAssertionsRequestTypeDef(TypedDict):
    serviceArn: str
    source: NotRequired[AssertionSourceType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ListFailureModeAssessmentsRequestTypeDef(TypedDict):
    serviceArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListFailureModeFindingsRequestTypeDef(TypedDict):
    serviceArn: str
    severity: NotRequired[FindingSeverityType]
    failureCategory: NotRequired[FailureCategoryType]
    status: NotRequired[FindingStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


ListInputSourcesRequestTypeDef = TypedDict(
    "ListInputSourcesRequestTypeDef",
    {
        "serviceArn": str,
        "type": NotRequired[InputSourceTypeType],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)


class ListPoliciesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListReportsRequestTypeDef(TypedDict):
    serviceArn: NotRequired[str]
    reportType: NotRequired[Literal["FAILURE_MODE"]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListResourcesRequestTypeDef(TypedDict):
    serviceArn: str
    serviceFunctionId: NotRequired[str]
    awsRegion: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListServiceFunctionsRequestTypeDef(TypedDict):
    serviceArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListServiceTopologyEdgesRequestTypeDef(TypedDict):
    serviceArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListServicesRequestTypeDef(TypedDict):
    systemArn: NotRequired[str]
    userJourneyId: NotRequired[str]
    ouId: NotRequired[str]
    accountId: NotRequired[str]
    assessmentStatus: NotRequired[AssessmentStatusType]
    policyArn: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSystemsRequestTypeDef(TypedDict):
    ouId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SystemSummaryTypeDef(TypedDict):
    systemId: str
    name: str
    systemArn: NotRequired[str]
    userJourneysCount: NotRequired[int]
    servicesCount: NotRequired[int]
    organizationId: NotRequired[str]
    ouId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class ListUserJourneysRequestTypeDef(TypedDict):
    systemArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class UserJourneySummaryTypeDef(TypedDict):
    userJourneyId: str
    name: str
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class QueryDataPointTypeDef(TypedDict):
    timestamp: datetime
    queryCount: int


class S3ReportOutputConfigurationTypeDef(TypedDict):
    bucketPath: str
    bucketOwner: str


class S3ReportOutputTypeDef(TypedDict):
    s3ObjectKey: str


class ResourceDiscoveryStatusTypeDef(TypedDict):
    status: NotRequired[ResourceDiscoveryRunStatusType]
    lastRunAt: NotRequired[datetime]
    errorCode: NotRequired[ResourceDiscoveryErrorCodeType]
    errorMessage: NotRequired[str]


class ResourceTagTypeDef(TypedDict):
    key: str
    values: Sequence[str]


class ResourceTypeDef(TypedDict):
    identifier: str
    awsRegion: NotRequired[str]
    awsAccountId: NotRequired[str]
    resourceType: NotRequired[str]


class ServiceAchievabilityUpdatedMetadataTypeDef(TypedDict):
    assessmentId: NotRequired[str]
    availabilitySlo: NotRequired[str]
    multiAzRtoRpo: NotRequired[str]
    multiRegionRtoRpo: NotRequired[str]


class ServiceFunctionCreatedMetadataTypeDef(TypedDict):
    serviceFunctionId: NotRequired[str]
    serviceFunctionName: NotRequired[str]


class ServiceFunctionDeletedMetadataTypeDef(TypedDict):
    serviceFunctionId: NotRequired[str]
    serviceFunctionName: NotRequired[str]


class ServiceFunctionResourcesAddedMetadataTypeDef(TypedDict):
    serviceFunctionId: NotRequired[str]
    serviceFunctionName: NotRequired[str]
    resourcesAdded: NotRequired[list[str]]


class ServiceFunctionResourcesRemovedMetadataTypeDef(TypedDict):
    serviceFunctionId: NotRequired[str]
    serviceFunctionName: NotRequired[str]
    resourcesRemoved: NotRequired[list[str]]


class ServiceFunctionUpdatedMetadataTypeDef(TypedDict):
    serviceFunctionId: NotRequired[str]
    serviceFunctionName: NotRequired[str]
    resourcesAdded: NotRequired[list[str]]
    resourcesRemoved: NotRequired[list[str]]


class ServicePolicyAssociatedMetadataTypeDef(TypedDict):
    policyName: NotRequired[str]
    policyArn: NotRequired[str]


class ServicePolicyDisassociatedMetadataTypeDef(TypedDict):
    policyName: NotRequired[str]
    policyArn: NotRequired[str]


class ServiceResourcesAssociatedMetadataTypeDef(TypedDict):
    resourceCount: NotRequired[int]
    resourceTypes: NotRequired[list[str]]


class ServiceResourcesDisassociatedMetadataTypeDef(TypedDict):
    resourceCount: NotRequired[int]
    resourceTypes: NotRequired[list[str]]


class ServiceSystemAssociatedMetadataTypeDef(TypedDict):
    systemName: NotRequired[str]
    systemArn: NotRequired[str]


class ServiceSystemDisassociatedMetadataTypeDef(TypedDict):
    systemId: NotRequired[str]
    systemName: NotRequired[str]
    systemArn: NotRequired[str]


class ServiceWorkflowUpdatedMetadataTypeDef(TypedDict):
    serviceFunctionId: NotRequired[str]
    serviceFunctionName: NotRequired[str]


class ServiceReferenceTypeDef(TypedDict):
    serviceId: NotRequired[str]
    serviceName: NotRequired[str]


class StartFailureModeAssessmentRequestTypeDef(TypedDict):
    serviceArn: str
    clientToken: NotRequired[str]


class StringChangeTypeDef(TypedDict):
    oldValue: NotRequired[str]
    newValue: NotRequired[str]


class SystemPolicyAssociatedMetadataTypeDef(TypedDict):
    policyName: NotRequired[str]
    policyArn: NotRequired[str]


class SystemPolicyDisassociatedMetadataTypeDef(TypedDict):
    policyName: NotRequired[str]
    policyArn: NotRequired[str]


class SystemServiceAssociatedMetadataTypeDef(TypedDict):
    serviceName: NotRequired[str]
    serviceArn: NotRequired[str]
    userJourneys: NotRequired[list[str]]


class SystemServiceDisassociatedMetadataTypeDef(TypedDict):
    serviceName: NotRequired[str]
    serviceArn: NotRequired[str]
    userJourneysAffected: NotRequired[list[str]]
    comment: NotRequired[str]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateAssertionRequestTypeDef(TypedDict):
    serviceArn: str
    assertionId: str
    text: NotRequired[str]


class UpdateDependencyRequestTypeDef(TypedDict):
    serviceArn: str
    dependencyId: str
    criticality: NotRequired[DependencyCriticalityType]
    comment: NotRequired[str]


class UpdateFailureModeFindingRequestTypeDef(TypedDict):
    findingId: str
    status: FindingStatusType
    serviceArn: str
    comment: NotRequired[str]


class UpdateServiceFunctionRequestTypeDef(TypedDict):
    serviceArn: str
    serviceFunctionId: str
    name: NotRequired[str]
    description: NotRequired[str]
    criticality: NotRequired[ServiceFunctionCriticalityType]


class UpdateSystemRequestTypeDef(TypedDict):
    systemArn: str
    description: NotRequired[str]
    sharingEnabled: NotRequired[bool]


class UpdateUserJourneyRequestTypeDef(TypedDict):
    systemArn: str
    userJourneyId: str
    name: NotRequired[str]
    description: NotRequired[str]
    policyArn: NotRequired[str]


class AssessmentSummaryTypeDef(TypedDict):
    assessmentId: str
    serviceArn: str
    assessmentStatus: NotRequired[AssessmentStatusType]
    assessmentStep: NotRequired[AssessmentStepType]
    totalFindings: NotRequired[int]
    startedAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]
    errorMessage: NotRequired[str]
    errorCode: NotRequired[AssessmentErrorCodeType]
    assessmentCost: NotRequired[AssessmentCostTypeDef]
    billableAssessmentUnitCount: NotRequired[int]
    achievability: NotRequired[AchievabilityTypeDef]


AssociatedSystemUnionTypeDef = Union[AssociatedSystemTypeDef, AssociatedSystemOutputTypeDef]


class ImportPolicyRequestTypeDef(TypedDict):
    v1PolicyArn: str
    kmsKeyId: NotRequired[str]
    availabilitySlo: NotRequired[AvailabilitySloTypeDef]
    multiAzDisasterRecoveryApproach: NotRequired[MultiAzDisasterRecoveryApproachType]
    multiRegionDisasterRecoveryApproach: NotRequired[MultiRegionDisasterRecoveryApproachType]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class CreateAssertionResponseTypeDef(TypedDict):
    assertion: AssertionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInputSourceResponseTypeDef(TypedDict):
    serviceArn: str
    inputSourceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateServiceFunctionResourcesResponseTypeDef(TypedDict):
    serviceArn: str
    serviceFunctionId: str
    resources: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAssertionResponseTypeDef(TypedDict):
    assertionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteInputSourceResponseTypeDef(TypedDict):
    serviceArn: str
    inputSourceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePolicyResponseTypeDef(TypedDict):
    policyArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteServiceFunctionResourcesResponseTypeDef(TypedDict):
    serviceArn: str
    serviceFunctionId: str
    resources: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteServiceFunctionResponseTypeDef(TypedDict):
    serviceFunctionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteServiceResponseTypeDef(TypedDict):
    serviceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSystemResponseTypeDef(TypedDict):
    systemArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteUserJourneyResponseTypeDef(TypedDict):
    userJourneyId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssertionsResponseTypeDef(TypedDict):
    assertions: list[AssertionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartFailureModeAssessmentResponseTypeDef(TypedDict):
    assessmentId: str
    serviceArn: str
    assessmentStatus: AssessmentStatusType
    startedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssertionResponseTypeDef(TypedDict):
    assertion: AssertionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDependencyResponseTypeDef(TypedDict):
    dependencyId: str
    dependencyName: str
    location: str
    criticality: DependencyCriticalityType
    comment: str
    provider: str
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePolicyRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    availabilitySlo: NotRequired[AvailabilitySloTypeDef]
    multiAz: NotRequired[MultiAzTargetsTypeDef]
    multiRegion: NotRequired[MultiRegionTargetsTypeDef]
    dataRecovery: NotRequired[DataRecoveryTargetsTypeDef]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class PolicySummaryTypeDef(TypedDict):
    policyArn: str
    name: str
    availabilitySlo: NotRequired[AvailabilitySloTypeDef]
    multiAz: NotRequired[MultiAzTargetsTypeDef]
    multiRegion: NotRequired[MultiRegionTargetsTypeDef]
    dataRecovery: NotRequired[DataRecoveryTargetsTypeDef]
    associatedServiceCount: NotRequired[int]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class PolicyTypeDef(TypedDict):
    policyArn: str
    name: str
    description: NotRequired[str]
    availabilitySlo: NotRequired[AvailabilitySloTypeDef]
    multiAz: NotRequired[MultiAzTargetsTypeDef]
    multiRegion: NotRequired[MultiRegionTargetsTypeDef]
    dataRecovery: NotRequired[DataRecoveryTargetsTypeDef]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    associatedServiceCount: NotRequired[int]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class UpdatePolicyRequestTypeDef(TypedDict):
    policyArn: str
    description: NotRequired[str]
    availabilitySlo: NotRequired[AvailabilitySloTypeDef]
    multiAz: NotRequired[MultiAzTargetsTypeDef]
    multiRegion: NotRequired[MultiRegionTargetsTypeDef]
    dataRecovery: NotRequired[DataRecoveryTargetsTypeDef]


class CreateServiceFunctionResponseTypeDef(TypedDict):
    serviceFunction: ServiceFunctionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListServiceFunctionsResponseTypeDef(TypedDict):
    serviceFunctions: list[ServiceFunctionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateServiceFunctionResponseTypeDef(TypedDict):
    serviceFunction: ServiceFunctionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSystemResponseTypeDef(TypedDict):
    system: SystemTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSystemResponseTypeDef(TypedDict):
    system: SystemTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSystemResponseTypeDef(TypedDict):
    system: SystemTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserJourneyResponseTypeDef(TypedDict):
    userJourney: UserJourneyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetUserJourneyResponseTypeDef(TypedDict):
    userJourney: UserJourneyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserJourneyResponseTypeDef(TypedDict):
    userJourney: UserJourneyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PermissionModelOutputTypeDef(TypedDict):
    invokerRoleName: str
    crossAccountRoles: NotRequired[list[CrossAccountRoleTypeDef]]


class PermissionModelTypeDef(TypedDict):
    invokerRoleName: str
    crossAccountRoles: NotRequired[Sequence[CrossAccountRoleTypeDef]]


class ServiceSummaryTypeDef(TypedDict):
    serviceArn: str
    name: str
    associatedSystems: NotRequired[list[AssociatedSystemOutputTypeDef]]
    regions: NotRequired[list[str]]
    policyArn: NotRequired[str]
    assessmentStatus: NotRequired[AssessmentStatusType]
    openFindingsCount: NotRequired[int]
    resolvedFindingsCount: NotRequired[int]
    dependencyDiscovery: NotRequired[DependencyDiscoveryConfigTypeDef]
    achievability: NotRequired[AchievabilityTypeDef]
    organizationId: NotRequired[str]
    ouId: NotRequired[str]
    accountId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class ServiceTopologyEdgeSummaryTypeDef(TypedDict):
    sourceResourceIdentifier: str
    destinationResourceIdentifier: str
    properties: NotRequired[list[EdgePropertySummaryTypeDef]]


class EffectivePolicyValuesTypeDef(TypedDict):
    availabilitySlo: NotRequired[SloSourceTypeDef]
    multiAzRto: NotRequired[TargetSourceTypeDef]
    multiAzRpo: NotRequired[TargetSourceTypeDef]
    multiAzDrApproach: NotRequired[DisasterRecoverySourceTypeDef]
    multiRegionRto: NotRequired[TargetSourceTypeDef]
    multiRegionRpo: NotRequired[TargetSourceTypeDef]
    multiRegionDrApproach: NotRequired[DisasterRecoverySourceTypeDef]
    dataRecoveryTimeBetweenBackups: NotRequired[TargetSourceTypeDef]


EksSourceUnionTypeDef = Union[EksSourceTypeDef, EksSourceOutputTypeDef]


class ListFailureModeFindingsResponseTypeDef(TypedDict):
    findingsSummary: list[FindingSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class FindingTypeDef(TypedDict):
    findingId: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    failureCategory: NotRequired[FailureCategoryType]
    status: NotRequired[FindingStatusType]
    reasoning: NotRequired[str]
    comment: NotRequired[str]
    severity: NotRequired[FindingSeverityType]
    serviceFunctions: NotRequired[list[str]]
    policyComponent: NotRequired[PolicyComponentType]
    infrastructureAndCodeRecommendations: NotRequired[
        list[InfrastructureAndCodeRecommendationTypeDef]
    ]
    observabilityRecommendations: NotRequired[list[ObservabilityRecommendationTypeDef]]
    testingRecommendations: NotRequired[list[TestingRecommendationTypeDef]]
    updatedAt: NotRequired[datetime]


class GetServiceRequestWaitExtraTypeDef(TypedDict):
    serviceArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetServiceRequestWaitTypeDef(TypedDict):
    serviceArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class ListFailureModeAssessmentsRequestWaitTypeDef(TypedDict):
    serviceArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class ListReportsRequestWaitTypeDef(TypedDict):
    serviceArn: NotRequired[str]
    reportType: NotRequired[Literal["FAILURE_MODE"]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


InputSourceSummaryTypeDef = TypedDict(
    "InputSourceSummaryTypeDef",
    {
        "inputSourceId": str,
        "type": NotRequired[InputSourceTypeType],
        "resourceTags": NotRequired[list[ResourceTagOutputTypeDef]],
        "cfnStackArn": NotRequired[str],
        "tfStateFileUrl": NotRequired[str],
        "eks": NotRequired[EksSourceOutputTypeDef],
        "designFileS3Url": NotRequired[str],
        "createdAt": NotRequired[datetime],
    },
)


class ListAssertionsRequestPaginateTypeDef(TypedDict):
    serviceArn: str
    source: NotRequired[AssertionSourceType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFailureModeAssessmentsRequestPaginateTypeDef(TypedDict):
    serviceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFailureModeFindingsRequestPaginateTypeDef(TypedDict):
    serviceArn: str
    severity: NotRequired[FindingSeverityType]
    failureCategory: NotRequired[FailureCategoryType]
    status: NotRequired[FindingStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListInputSourcesRequestPaginateTypeDef = TypedDict(
    "ListInputSourcesRequestPaginateTypeDef",
    {
        "serviceArn": str,
        "type": NotRequired[InputSourceTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListPoliciesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListReportsRequestPaginateTypeDef(TypedDict):
    serviceArn: NotRequired[str]
    reportType: NotRequired[Literal["FAILURE_MODE"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourcesRequestPaginateTypeDef(TypedDict):
    serviceArn: str
    serviceFunctionId: NotRequired[str]
    awsRegion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceFunctionsRequestPaginateTypeDef(TypedDict):
    serviceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceTopologyEdgesRequestPaginateTypeDef(TypedDict):
    serviceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServicesRequestPaginateTypeDef(TypedDict):
    systemArn: NotRequired[str]
    userJourneyId: NotRequired[str]
    ouId: NotRequired[str]
    accountId: NotRequired[str]
    assessmentStatus: NotRequired[AssessmentStatusType]
    policyArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSystemsRequestPaginateTypeDef(TypedDict):
    ouId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUserJourneysRequestPaginateTypeDef(TypedDict):
    systemArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDependenciesRequestPaginateTypeDef(TypedDict):
    serviceArn: NotRequired[str]
    queryRangeStartTime: NotRequired[TimestampTypeDef]
    queryRangeEndTime: NotRequired[TimestampTypeDef]
    queryRangeGranularity: NotRequired[QueryGranularityType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDependenciesRequestTypeDef(TypedDict):
    serviceArn: NotRequired[str]
    queryRangeStartTime: NotRequired[TimestampTypeDef]
    queryRangeEndTime: NotRequired[TimestampTypeDef]
    queryRangeGranularity: NotRequired[QueryGranularityType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListServiceEventsRequestPaginateTypeDef(TypedDict):
    serviceArn: str
    eventTypes: NotRequired[Sequence[ServiceEventTypeType]]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceEventsRequestTypeDef(TypedDict):
    serviceArn: str
    eventTypes: NotRequired[Sequence[ServiceEventTypeType]]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSystemEventsRequestPaginateTypeDef(TypedDict):
    systemArn: str
    eventTypes: NotRequired[Sequence[SystemEventTypeType]]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSystemEventsRequestTypeDef(TypedDict):
    systemArn: str
    eventTypes: NotRequired[Sequence[SystemEventTypeType]]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSystemsResponseTypeDef(TypedDict):
    systemSummaries: list[SystemSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListUserJourneysResponseTypeDef(TypedDict):
    userJourneySummaries: list[UserJourneySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class QueryRangeTypeDef(TypedDict):
    startTime: datetime
    endTime: datetime
    granularity: QueryGranularityType
    dataPoints: list[QueryDataPointTypeDef]


class ReportOutputConfigurationTypeDef(TypedDict):
    s3: NotRequired[S3ReportOutputConfigurationTypeDef]


class ReportOutputTypeDef(TypedDict):
    s3ReportOutput: NotRequired[S3ReportOutputTypeDef]
    failedReportOutput: NotRequired[FailedReportOutputTypeDef]


ResourceTagUnionTypeDef = Union[ResourceTagTypeDef, ResourceTagOutputTypeDef]


class ServiceResourceTypeDef(TypedDict):
    resourceIdentifier: str
    resource: ResourceTypeDef
    inputSource: NotRequired[InputSourceTypeDef]


class ServiceEventMetadataTypeDef(TypedDict):
    serviceCreated: NotRequired[dict[str, Any]]
    serviceDeleted: NotRequired[dict[str, Any]]
    serviceSystemAssociated: NotRequired[ServiceSystemAssociatedMetadataTypeDef]
    serviceSystemDisassociated: NotRequired[ServiceSystemDisassociatedMetadataTypeDef]
    serviceResourcesAssociated: NotRequired[ServiceResourcesAssociatedMetadataTypeDef]
    serviceResourcesDisassociated: NotRequired[ServiceResourcesDisassociatedMetadataTypeDef]
    serviceWorkflowUpdated: NotRequired[ServiceWorkflowUpdatedMetadataTypeDef]
    serviceInputSourcesUpdated: NotRequired[dict[str, Any]]
    servicePolicyAssociated: NotRequired[ServicePolicyAssociatedMetadataTypeDef]
    servicePolicyDisassociated: NotRequired[ServicePolicyDisassociatedMetadataTypeDef]
    serviceFunctionCreated: NotRequired[ServiceFunctionCreatedMetadataTypeDef]
    serviceFunctionUpdated: NotRequired[ServiceFunctionUpdatedMetadataTypeDef]
    serviceFunctionDeleted: NotRequired[ServiceFunctionDeletedMetadataTypeDef]
    serviceFunctionResourcesAdded: NotRequired[ServiceFunctionResourcesAddedMetadataTypeDef]
    serviceFunctionResourcesRemoved: NotRequired[ServiceFunctionResourcesRemovedMetadataTypeDef]
    serviceAchievabilityUpdated: NotRequired[ServiceAchievabilityUpdatedMetadataTypeDef]
    assertionCreated: NotRequired[AssertionCreatedMetadataTypeDef]
    assertionUpdated: NotRequired[AssertionUpdatedMetadataTypeDef]
    assertionDeleted: NotRequired[AssertionDeletedMetadataTypeDef]


class ServiceReferenceChangesTypeDef(TypedDict):
    added: NotRequired[list[ServiceReferenceTypeDef]]
    removed: NotRequired[list[ServiceReferenceTypeDef]]


class SystemUserJourneyCreatedMetadataTypeDef(TypedDict):
    userJourneyName: NotRequired[str]
    associatedServices: NotRequired[list[ServiceReferenceTypeDef]]


class SystemUserJourneyDeletedMetadataTypeDef(TypedDict):
    userJourneyName: NotRequired[str]
    associatedServicesAtDeletion: NotRequired[list[ServiceReferenceTypeDef]]


class ListFailureModeAssessmentsResponseTypeDef(TypedDict):
    assessmentSummaries: list[AssessmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ImportAppRequestTypeDef(TypedDict):
    v1AppArn: str
    policyArn: NotRequired[str]
    kmsKeyId: NotRequired[str]
    skipManuallyAddedResources: NotRequired[bool]
    associatedSystems: NotRequired[Sequence[AssociatedSystemUnionTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class ListPoliciesResponseTypeDef(TypedDict):
    policySummaries: list[PolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreatePolicyResponseTypeDef(TypedDict):
    policy: PolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetPolicyResponseTypeDef(TypedDict):
    policy: PolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ImportPolicyResponseTypeDef(TypedDict):
    policy: PolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePolicyResponseTypeDef(TypedDict):
    policy: PolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


PermissionModelUnionTypeDef = Union[PermissionModelTypeDef, PermissionModelOutputTypeDef]


class ListServicesResponseTypeDef(TypedDict):
    serviceSummaries: list[ServiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListServiceTopologyEdgesResponseTypeDef(TypedDict):
    serviceTopologyEdgeSummaries: list[ServiceTopologyEdgeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetFailureModeFindingResponseTypeDef(TypedDict):
    finding: FindingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFailureModeFindingResponseTypeDef(TypedDict):
    finding: FindingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListInputSourcesResponseTypeDef(TypedDict):
    inputSourceSummaries: list[InputSourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DependencySummaryTypeDef(TypedDict):
    dependencyId: str
    serviceArn: str
    dependencyName: str
    dnsName: str
    location: str
    lastDetectedTime: datetime
    sourceRegions: list[str]
    queryRange: QueryRangeTypeDef
    criticality: DependencyCriticalityType
    provider: NotRequired[str]
    comment: NotRequired[str]


class ServiceReportConfigurationOutputTypeDef(TypedDict):
    reportOutputs: list[ReportOutputConfigurationTypeDef]


class ServiceReportConfigurationTypeDef(TypedDict):
    reportOutputs: Sequence[ReportOutputConfigurationTypeDef]


class ReportGenerationResultTypeDef(TypedDict):
    reportType: Literal["FAILURE_MODE"]
    status: ReportGenerationStatusType
    serviceArn: NotRequired[str]
    assessmentId: NotRequired[str]
    createdAt: NotRequired[datetime]
    reportOutput: NotRequired[ReportOutputTypeDef]


class ResourceConfigurationTypeDef(TypedDict):
    resourceTags: NotRequired[Sequence[ResourceTagUnionTypeDef]]
    cfnStackArn: NotRequired[str]
    tfStateFileUrl: NotRequired[str]
    eks: NotRequired[EksSourceUnionTypeDef]
    designFileS3Url: NotRequired[str]


class ListResourcesResponseTypeDef(TypedDict):
    serviceFunctionId: str
    serviceResources: list[ServiceResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ServiceEventDetailsTypeDef(TypedDict):
    title: str
    description: str
    eventMetadata: NotRequired[ServiceEventMetadataTypeDef]


class UserJourneyChangesTypeDef(TypedDict):
    journeyDescription: NotRequired[StringChangeTypeDef]
    associatedServices: NotRequired[ServiceReferenceChangesTypeDef]


class ListDependenciesResponseTypeDef(TypedDict):
    dependencySummaries: list[DependencySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ServiceTypeDef(TypedDict):
    serviceArn: str
    name: str
    description: NotRequired[str]
    associatedSystems: NotRequired[list[AssociatedSystemOutputTypeDef]]
    policyArn: NotRequired[str]
    regions: NotRequired[list[str]]
    permissionModel: NotRequired[PermissionModelOutputTypeDef]
    dependencyDiscovery: NotRequired[DependencyDiscoveryConfigTypeDef]
    effectivePolicyValues: NotRequired[EffectivePolicyValuesTypeDef]
    achievability: NotRequired[AchievabilityTypeDef]
    reportConfiguration: NotRequired[ServiceReportConfigurationOutputTypeDef]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    estimatedAssessmentCost: NotRequired[AssessmentCostTypeDef]
    resourceDiscovery: NotRequired[ResourceDiscoveryStatusTypeDef]
    assessmentStatus: NotRequired[AssessmentStatusType]
    rerunAssessment: NotRequired[bool]
    openFindingsCount: NotRequired[int]
    resolvedFindingsCount: NotRequired[int]
    organizationId: NotRequired[str]
    ouId: NotRequired[str]
    accountId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


ServiceReportConfigurationUnionTypeDef = Union[
    ServiceReportConfigurationTypeDef, ServiceReportConfigurationOutputTypeDef
]


class CreateReportResponseTypeDef(TypedDict):
    reportGenerationResult: ReportGenerationResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListReportsResponseTypeDef(TypedDict):
    reportGenerationResults: list[ReportGenerationResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateInputSourceRequestTypeDef(TypedDict):
    serviceArn: str
    resourceConfiguration: ResourceConfigurationTypeDef
    clientToken: NotRequired[str]


class ServiceEventTypeDef(TypedDict):
    eventId: str
    timestamp: datetime
    eventType: ServiceEventTypeType
    serviceArn: str
    actor: EventActorTypeDef
    eventDetails: ServiceEventDetailsTypeDef


class SystemUserJourneyUpdatedMetadataTypeDef(TypedDict):
    userJourneyName: NotRequired[str]
    changes: NotRequired[UserJourneyChangesTypeDef]


class CreateServiceResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetServiceResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ImportAppResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateServiceResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateServiceRequestTypeDef(TypedDict):
    name: str
    regions: Sequence[str]
    permissionModel: PermissionModelUnionTypeDef
    description: NotRequired[str]
    associatedSystems: NotRequired[Sequence[AssociatedSystemUnionTypeDef]]
    policyArn: NotRequired[str]
    dependencyDiscovery: NotRequired[DependencyDiscoveryInputType]
    reportConfiguration: NotRequired[ServiceReportConfigurationUnionTypeDef]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class UpdateServiceRequestTypeDef(TypedDict):
    serviceArn: str
    description: NotRequired[str]
    associatedSystems: NotRequired[Sequence[AssociatedSystemUnionTypeDef]]
    policyArn: NotRequired[str]
    regions: NotRequired[Sequence[str]]
    permissionModel: NotRequired[PermissionModelUnionTypeDef]
    dependencyDiscovery: NotRequired[DependencyDiscoveryInputType]
    reportConfiguration: NotRequired[ServiceReportConfigurationUnionTypeDef]


class ListServiceEventsResponseTypeDef(TypedDict):
    events: list[ServiceEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SystemEventMetadataTypeDef(TypedDict):
    systemCreated: NotRequired[dict[str, Any]]
    systemDeleted: NotRequired[dict[str, Any]]
    systemUserJourneyCreated: NotRequired[SystemUserJourneyCreatedMetadataTypeDef]
    systemUserJourneyUpdated: NotRequired[SystemUserJourneyUpdatedMetadataTypeDef]
    systemUserJourneyDeleted: NotRequired[SystemUserJourneyDeletedMetadataTypeDef]
    systemServiceAssociated: NotRequired[SystemServiceAssociatedMetadataTypeDef]
    systemServiceDisassociated: NotRequired[SystemServiceDisassociatedMetadataTypeDef]
    systemPolicyAssociated: NotRequired[SystemPolicyAssociatedMetadataTypeDef]
    systemPolicyDisassociated: NotRequired[SystemPolicyDisassociatedMetadataTypeDef]


class SystemEventDetailsTypeDef(TypedDict):
    title: str
    description: str
    eventMetadata: NotRequired[SystemEventMetadataTypeDef]


class SystemEventTypeDef(TypedDict):
    eventId: str
    timestamp: datetime
    eventType: SystemEventTypeType
    systemArn: str
    actor: EventActorTypeDef
    eventDetails: SystemEventDetailsTypeDef


class ListSystemEventsResponseTypeDef(TypedDict):
    events: list[SystemEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
