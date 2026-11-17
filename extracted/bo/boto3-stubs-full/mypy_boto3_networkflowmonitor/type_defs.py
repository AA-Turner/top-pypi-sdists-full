"""
Type annotations for networkflowmonitor service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_networkflowmonitor/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_networkflowmonitor.type_defs import AccountToAddTypeDef

    data: AccountToAddTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    DestinationCategoryType,
    FilterOperatorType,
    MetricUnitType,
    MonitorLocalResourceTypeType,
    MonitorMetricType,
    MonitorRemoteResourceTypeType,
    MonitorStatusType,
    OrgMembershipStatusType,
    QueryStatusType,
    ScopeCoverageStatusType,
    ScopeStatusType,
    WorkloadInsightsMetricType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountToAddTypeDef",
    "AdditionalFlowInfoTypeDef",
    "ClientLocationTypeDef",
    "CreateMonitorInputTypeDef",
    "CreateMonitorOutputTypeDef",
    "CreatePerformanceMonitorInputTypeDef",
    "CreatePerformanceMonitorOutputTypeDef",
    "CreateScopeInputTypeDef",
    "CreateScopeOutputTypeDef",
    "DeleteMonitorInputTypeDef",
    "DeletePerformanceMonitorInputTypeDef",
    "DeleteScopeInputTypeDef",
    "FilterParameterTypeDef",
    "GetMonitorInputTypeDef",
    "GetMonitorOutputTypeDef",
    "GetMonitorScopeSuggestionsInputPaginateTypeDef",
    "GetMonitorScopeSuggestionsInputTypeDef",
    "GetMonitorScopeSuggestionsOutputTypeDef",
    "GetPerformanceMonitorInputTypeDef",
    "GetPerformanceMonitorOutputTypeDef",
    "GetQueryResultsMonitorTopContributorsInputPaginateTypeDef",
    "GetQueryResultsMonitorTopContributorsInputTypeDef",
    "GetQueryResultsMonitorTopContributorsOutputTypeDef",
    "GetQueryResultsPerformanceMonitorInputPaginateTypeDef",
    "GetQueryResultsPerformanceMonitorInputTypeDef",
    "GetQueryResultsPerformanceMonitorOutputTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsDataInputPaginateTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsDataInputTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsInputPaginateTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsInputTypeDef",
    "GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef",
    "GetQueryStatusMonitorTopContributorsInputTypeDef",
    "GetQueryStatusMonitorTopContributorsOutputTypeDef",
    "GetQueryStatusPerformanceMonitorInputTypeDef",
    "GetQueryStatusPerformanceMonitorOutputTypeDef",
    "GetQueryStatusWorkloadInsightsTopContributorsDataInputTypeDef",
    "GetQueryStatusWorkloadInsightsTopContributorsDataOutputTypeDef",
    "GetQueryStatusWorkloadInsightsTopContributorsInputTypeDef",
    "GetQueryStatusWorkloadInsightsTopContributorsOutputTypeDef",
    "GetScopeInputTypeDef",
    "GetScopeOutputTypeDef",
    "KubernetesMetadataTypeDef",
    "ListMonitorsInputPaginateTypeDef",
    "ListMonitorsInputTypeDef",
    "ListMonitorsOutputTypeDef",
    "ListPerformanceMonitorsInputPaginateTypeDef",
    "ListPerformanceMonitorsInputTypeDef",
    "ListPerformanceMonitorsOutputTypeDef",
    "ListScopesInputPaginateTypeDef",
    "ListScopesInputTypeDef",
    "ListScopesOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MonitorLocalResourceTypeDef",
    "MonitorRemoteResourceTypeDef",
    "MonitorSummaryTypeDef",
    "MonitorTopContributorsRowTypeDef",
    "NetworkTypeDef",
    "PaginatorConfigTypeDef",
    "PerformanceMonitorSummaryTypeDef",
    "PerformanceMonitorTargetTypeDef",
    "QueryFieldTypeDef",
    "ResponseMetadataTypeDef",
    "ScopeSummaryTypeDef",
    "StartQueryMonitorTopContributorsInputTypeDef",
    "StartQueryMonitorTopContributorsOutputTypeDef",
    "StartQueryPerformanceMonitorInputTypeDef",
    "StartQueryPerformanceMonitorOutputTypeDef",
    "StartQueryWorkloadInsightsTopContributorsDataInputTypeDef",
    "StartQueryWorkloadInsightsTopContributorsDataOutputTypeDef",
    "StartQueryWorkloadInsightsTopContributorsInputTypeDef",
    "StartQueryWorkloadInsightsTopContributorsOutputTypeDef",
    "StopQueryMonitorTopContributorsInputTypeDef",
    "StopQueryPerformanceMonitorInputTypeDef",
    "StopQueryWorkloadInsightsTopContributorsDataInputTypeDef",
    "StopQueryWorkloadInsightsTopContributorsInputTypeDef",
    "TagResourceInputTypeDef",
    "TargetIdTypeDef",
    "TargetIdentifierTypeDef",
    "TargetResourceTypeDef",
    "TimestampTypeDef",
    "TraversedComponentTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateMonitorInputTypeDef",
    "UpdateMonitorOutputTypeDef",
    "UpdatePerformanceMonitorInputTypeDef",
    "UpdatePerformanceMonitorOutputTypeDef",
    "UpdateScopeInputTypeDef",
    "UpdateScopeOutputTypeDef",
    "WorkloadInsightsTopContributorsDataPointTypeDef",
    "WorkloadInsightsTopContributorsRowTypeDef",
)


class AccountToAddTypeDef(TypedDict):
    accountId: str
    region: str
    membership: OrgMembershipStatusType


class ClientLocationTypeDef(TypedDict):
    city: NotRequired[str]
    subdivision: NotRequired[str]
    country: NotRequired[str]


class NetworkTypeDef(TypedDict):
    asName: NotRequired[str]
    asNumber: NotRequired[int]


MonitorLocalResourceTypeDef = TypedDict(
    "MonitorLocalResourceTypeDef",
    {
        "type": MonitorLocalResourceTypeType,
        "identifier": str,
    },
)
MonitorRemoteResourceTypeDef = TypedDict(
    "MonitorRemoteResourceTypeDef",
    {
        "type": MonitorRemoteResourceTypeType,
        "identifier": str,
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


PerformanceMonitorTargetTypeDef = TypedDict(
    "PerformanceMonitorTargetTypeDef",
    {
        "type": Literal["AWS::EC2::VPC"],
        "identifier": str,
    },
)


class DeleteMonitorInputTypeDef(TypedDict):
    monitorName: str


class DeletePerformanceMonitorInputTypeDef(TypedDict):
    monitorName: str


class DeleteScopeInputTypeDef(TypedDict):
    scopeId: str


FilterParameterTypeDef = TypedDict(
    "FilterParameterTypeDef",
    {
        "field": str,
        "operator": FilterOperatorType,
        "values": Sequence[str],
    },
)


class GetMonitorInputTypeDef(TypedDict):
    monitorName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetMonitorScopeSuggestionsInputTypeDef(TypedDict):
    monitorArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class GetPerformanceMonitorInputTypeDef(TypedDict):
    monitorName: str


class GetQueryResultsMonitorTopContributorsInputTypeDef(TypedDict):
    monitorName: str
    queryId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetQueryResultsPerformanceMonitorInputTypeDef(TypedDict):
    monitorName: str
    queryId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


QueryFieldTypeDef = TypedDict(
    "QueryFieldTypeDef",
    {
        "name": str,
        "type": str,
    },
)


class GetQueryResultsWorkloadInsightsTopContributorsDataInputTypeDef(TypedDict):
    scopeId: str
    queryId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class WorkloadInsightsTopContributorsDataPointTypeDef(TypedDict):
    timestamps: list[datetime]
    values: list[float]
    label: str


class GetQueryResultsWorkloadInsightsTopContributorsInputTypeDef(TypedDict):
    scopeId: str
    queryId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class WorkloadInsightsTopContributorsRowTypeDef(TypedDict):
    accountId: NotRequired[str]
    localSubnetId: NotRequired[str]
    localAz: NotRequired[str]
    localVpcId: NotRequired[str]
    localRegion: NotRequired[str]
    remoteIdentifier: NotRequired[str]
    value: NotRequired[int]
    localSubnetArn: NotRequired[str]
    localVpcArn: NotRequired[str]


class GetQueryStatusMonitorTopContributorsInputTypeDef(TypedDict):
    monitorName: str
    queryId: str


class GetQueryStatusPerformanceMonitorInputTypeDef(TypedDict):
    monitorName: str
    queryId: str


class GetQueryStatusWorkloadInsightsTopContributorsDataInputTypeDef(TypedDict):
    scopeId: str
    queryId: str


class GetQueryStatusWorkloadInsightsTopContributorsInputTypeDef(TypedDict):
    scopeId: str
    queryId: str


class GetScopeInputTypeDef(TypedDict):
    scopeId: str


class KubernetesMetadataTypeDef(TypedDict):
    localServiceName: NotRequired[str]
    localPodName: NotRequired[str]
    localPodNamespace: NotRequired[str]
    remoteServiceName: NotRequired[str]
    remotePodName: NotRequired[str]
    remotePodNamespace: NotRequired[str]


class ListMonitorsInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    monitorStatus: NotRequired[MonitorStatusType]


class MonitorSummaryTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType


class ListPerformanceMonitorsInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    monitorStatus: NotRequired[MonitorStatusType]
    monitorType: NotRequired[Literal["VPC"]]


class ListScopesInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ScopeSummaryTypeDef(TypedDict):
    scopeId: str
    status: ScopeStatusType
    scopeArn: str


class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str


class TraversedComponentTypeDef(TypedDict):
    componentId: NotRequired[str]
    componentType: NotRequired[str]
    componentArn: NotRequired[str]
    serviceName: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class StopQueryMonitorTopContributorsInputTypeDef(TypedDict):
    monitorName: str
    queryId: str


class StopQueryPerformanceMonitorInputTypeDef(TypedDict):
    monitorName: str
    queryId: str


class StopQueryWorkloadInsightsTopContributorsDataInputTypeDef(TypedDict):
    scopeId: str
    queryId: str


class StopQueryWorkloadInsightsTopContributorsInputTypeDef(TypedDict):
    scopeId: str
    queryId: str


class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class TargetIdTypeDef(TypedDict):
    accountId: NotRequired[str]


class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class AdditionalFlowInfoTypeDef(TypedDict):
    network: NotRequired[NetworkTypeDef]
    clientLocation: NotRequired[ClientLocationTypeDef]


class CreateMonitorInputTypeDef(TypedDict):
    monitorName: str
    localResources: Sequence[MonitorLocalResourceTypeDef]
    scopeArn: str
    remoteResources: NotRequired[Sequence[MonitorRemoteResourceTypeDef]]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateMonitorInputTypeDef(TypedDict):
    monitorName: str
    localResourcesToAdd: NotRequired[Sequence[MonitorLocalResourceTypeDef]]
    localResourcesToRemove: NotRequired[Sequence[MonitorLocalResourceTypeDef]]
    remoteResourcesToAdd: NotRequired[Sequence[MonitorRemoteResourceTypeDef]]
    remoteResourcesToRemove: NotRequired[Sequence[MonitorRemoteResourceTypeDef]]
    clientToken: NotRequired[str]


class CreateMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    localResources: list[MonitorLocalResourceTypeDef]
    remoteResources: list[MonitorRemoteResourceTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateScopeOutputTypeDef(TypedDict):
    scopeId: str
    status: ScopeStatusType
    scopeArn: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    localResources: list[MonitorLocalResourceTypeDef]
    remoteResources: list[MonitorRemoteResourceTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetMonitorScopeSuggestionsOutputTypeDef(TypedDict):
    status: ScopeCoverageStatusType
    accountsToAdd: list[AccountToAddTypeDef]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetQueryStatusMonitorTopContributorsOutputTypeDef(TypedDict):
    status: QueryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueryStatusPerformanceMonitorOutputTypeDef(TypedDict):
    status: QueryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueryStatusWorkloadInsightsTopContributorsDataOutputTypeDef(TypedDict):
    status: QueryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueryStatusWorkloadInsightsTopContributorsOutputTypeDef(TypedDict):
    status: QueryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartQueryMonitorTopContributorsOutputTypeDef(TypedDict):
    queryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartQueryPerformanceMonitorOutputTypeDef(TypedDict):
    queryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartQueryWorkloadInsightsTopContributorsDataOutputTypeDef(TypedDict):
    queryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartQueryWorkloadInsightsTopContributorsOutputTypeDef(TypedDict):
    queryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    localResources: list[MonitorLocalResourceTypeDef]
    remoteResources: list[MonitorRemoteResourceTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScopeOutputTypeDef(TypedDict):
    scopeId: str
    status: ScopeStatusType
    scopeArn: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePerformanceMonitorInputTypeDef(TypedDict):
    monitorName: str
    targets: Sequence[PerformanceMonitorTargetTypeDef]
    scopeArn: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreatePerformanceMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    monitorType: Literal["VPC"]
    targets: list[PerformanceMonitorTargetTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetPerformanceMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    monitorType: Literal["VPC"]
    targets: list[PerformanceMonitorTargetTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PerformanceMonitorSummaryTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    monitorType: Literal["VPC"]
    targets: NotRequired[list[PerformanceMonitorTargetTypeDef]]


class UpdatePerformanceMonitorInputTypeDef(TypedDict):
    monitorName: str
    targetsToAdd: NotRequired[Sequence[PerformanceMonitorTargetTypeDef]]
    targetsToRemove: NotRequired[Sequence[PerformanceMonitorTargetTypeDef]]
    clientToken: NotRequired[str]


class UpdatePerformanceMonitorOutputTypeDef(TypedDict):
    monitorArn: str
    monitorName: str
    monitorStatus: MonitorStatusType
    monitorType: Literal["VPC"]
    targets: list[PerformanceMonitorTargetTypeDef]
    createdAt: datetime
    modifiedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetMonitorScopeSuggestionsInputPaginateTypeDef(TypedDict):
    monitorArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetQueryResultsMonitorTopContributorsInputPaginateTypeDef(TypedDict):
    monitorName: str
    queryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetQueryResultsPerformanceMonitorInputPaginateTypeDef(TypedDict):
    monitorName: str
    queryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetQueryResultsWorkloadInsightsTopContributorsDataInputPaginateTypeDef(TypedDict):
    scopeId: str
    queryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetQueryResultsWorkloadInsightsTopContributorsInputPaginateTypeDef(TypedDict):
    scopeId: str
    queryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitorsInputPaginateTypeDef(TypedDict):
    monitorStatus: NotRequired[MonitorStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPerformanceMonitorsInputPaginateTypeDef(TypedDict):
    monitorStatus: NotRequired[MonitorStatusType]
    monitorType: NotRequired[Literal["VPC"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListScopesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetQueryResultsPerformanceMonitorOutputTypeDef(TypedDict):
    fields: list[QueryFieldTypeDef]
    data: list[list[str]]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef(TypedDict):
    unit: MetricUnitType
    datapoints: list[WorkloadInsightsTopContributorsDataPointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef(TypedDict):
    topContributors: list[WorkloadInsightsTopContributorsRowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMonitorsOutputTypeDef(TypedDict):
    monitors: list[MonitorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListScopesOutputTypeDef(TypedDict):
    scopes: list[ScopeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartQueryMonitorTopContributorsInputTypeDef(TypedDict):
    monitorName: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    metricName: MonitorMetricType
    destinationCategory: DestinationCategoryType
    limit: NotRequired[int]


class StartQueryPerformanceMonitorInputTypeDef(TypedDict):
    monitorName: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    queryType: Literal["TOP_PATHS"]
    filterParameters: NotRequired[Sequence[FilterParameterTypeDef]]
    limit: NotRequired[int]


class StartQueryWorkloadInsightsTopContributorsDataInputTypeDef(TypedDict):
    scopeId: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    metricName: WorkloadInsightsMetricType
    destinationCategory: DestinationCategoryType


class StartQueryWorkloadInsightsTopContributorsInputTypeDef(TypedDict):
    scopeId: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    metricName: WorkloadInsightsMetricType
    destinationCategory: DestinationCategoryType
    limit: NotRequired[int]


class TargetIdentifierTypeDef(TypedDict):
    targetId: TargetIdTypeDef
    targetType: Literal["ACCOUNT"]


class MonitorTopContributorsRowTypeDef(TypedDict):
    localIp: NotRequired[str]
    snatIp: NotRequired[str]
    localInstanceId: NotRequired[str]
    localVpcId: NotRequired[str]
    localRegion: NotRequired[str]
    localAz: NotRequired[str]
    localSubnetId: NotRequired[str]
    targetPort: NotRequired[int]
    destinationCategory: NotRequired[DestinationCategoryType]
    remoteVpcId: NotRequired[str]
    remoteRegion: NotRequired[str]
    remoteAz: NotRequired[str]
    remoteSubnetId: NotRequired[str]
    remoteInstanceId: NotRequired[str]
    remoteIp: NotRequired[str]
    dnatIp: NotRequired[str]
    value: NotRequired[int]
    traversedConstructs: NotRequired[list[TraversedComponentTypeDef]]
    kubernetesMetadata: NotRequired[KubernetesMetadataTypeDef]
    localInstanceArn: NotRequired[str]
    localSubnetArn: NotRequired[str]
    localVpcArn: NotRequired[str]
    remoteInstanceArn: NotRequired[str]
    remoteSubnetArn: NotRequired[str]
    remoteVpcArn: NotRequired[str]
    additionalFlowInfo: NotRequired[AdditionalFlowInfoTypeDef]


class ListPerformanceMonitorsOutputTypeDef(TypedDict):
    monitors: list[PerformanceMonitorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class TargetResourceTypeDef(TypedDict):
    targetIdentifier: TargetIdentifierTypeDef
    region: str


class GetQueryResultsMonitorTopContributorsOutputTypeDef(TypedDict):
    unit: MetricUnitType
    topContributors: list[MonitorTopContributorsRowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateScopeInputTypeDef(TypedDict):
    targets: Sequence[TargetResourceTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class GetScopeOutputTypeDef(TypedDict):
    scopeId: str
    status: ScopeStatusType
    scopeArn: str
    targets: list[TargetResourceTypeDef]
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScopeInputTypeDef(TypedDict):
    scopeId: str
    resourcesToAdd: NotRequired[Sequence[TargetResourceTypeDef]]
    resourcesToDelete: NotRequired[Sequence[TargetResourceTypeDef]]
