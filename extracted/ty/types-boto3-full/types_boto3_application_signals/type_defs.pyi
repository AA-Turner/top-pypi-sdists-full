"""
Type annotations for application-signals service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_signals/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_application_signals.type_defs import AttributeFilterOutputTypeDef

    data: AttributeFilterOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ChangeEventTypeType,
    ConnectionTypeType,
    DetailLevelType,
    DurationUnitType,
    EvaluationTypeType,
    MetricSourceTypeType,
    ServiceLevelIndicatorComparisonOperatorType,
    ServiceLevelIndicatorMetricTypeType,
    ServiceLevelObjectiveBudgetStatusType,
    SeverityType,
    StandardUnitType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AttributeFilterOutputTypeDef",
    "AttributeFilterTypeDef",
    "AttributeFilterUnionTypeDef",
    "AuditFindingTypeDef",
    "AuditTargetEntityTypeDef",
    "AuditTargetTypeDef",
    "AuditorResultTypeDef",
    "BatchGetServiceLevelObjectiveBudgetReportInputTypeDef",
    "BatchGetServiceLevelObjectiveBudgetReportOutputTypeDef",
    "BatchUpdateExclusionWindowsErrorTypeDef",
    "BatchUpdateExclusionWindowsInputTypeDef",
    "BatchUpdateExclusionWindowsOutputTypeDef",
    "BurnRateConfigurationTypeDef",
    "CalendarIntervalOutputTypeDef",
    "CalendarIntervalTypeDef",
    "CanaryEntityTypeDef",
    "ChangeEventTypeDef",
    "CreateServiceLevelObjectiveInputTypeDef",
    "CreateServiceLevelObjectiveOutputTypeDef",
    "DeleteServiceLevelObjectiveInputTypeDef",
    "DependencyConfigOutputTypeDef",
    "DependencyConfigTypeDef",
    "DependencyConfigUnionTypeDef",
    "DependencyGraphTypeDef",
    "DimensionTypeDef",
    "EdgeTypeDef",
    "ExclusionWindowOutputTypeDef",
    "ExclusionWindowTypeDef",
    "ExclusionWindowUnionTypeDef",
    "GetServiceInputTypeDef",
    "GetServiceLevelObjectiveInputTypeDef",
    "GetServiceLevelObjectiveOutputTypeDef",
    "GetServiceOutputTypeDef",
    "GoalOutputTypeDef",
    "GoalTypeDef",
    "GoalUnionTypeDef",
    "GroupingAttributeDefinitionOutputTypeDef",
    "GroupingAttributeDefinitionTypeDef",
    "GroupingAttributeDefinitionUnionTypeDef",
    "GroupingConfigurationTypeDef",
    "IntervalOutputTypeDef",
    "IntervalTypeDef",
    "ListAuditFindingsInputTypeDef",
    "ListAuditFindingsOutputTypeDef",
    "ListEntityEventsInputPaginateTypeDef",
    "ListEntityEventsInputTypeDef",
    "ListEntityEventsOutputTypeDef",
    "ListGroupingAttributeDefinitionsInputTypeDef",
    "ListGroupingAttributeDefinitionsOutputTypeDef",
    "ListServiceDependenciesInputPaginateTypeDef",
    "ListServiceDependenciesInputTypeDef",
    "ListServiceDependenciesOutputTypeDef",
    "ListServiceDependentsInputPaginateTypeDef",
    "ListServiceDependentsInputTypeDef",
    "ListServiceDependentsOutputTypeDef",
    "ListServiceLevelObjectiveExclusionWindowsInputPaginateTypeDef",
    "ListServiceLevelObjectiveExclusionWindowsInputTypeDef",
    "ListServiceLevelObjectiveExclusionWindowsOutputTypeDef",
    "ListServiceLevelObjectivesInputPaginateTypeDef",
    "ListServiceLevelObjectivesInputTypeDef",
    "ListServiceLevelObjectivesOutputTypeDef",
    "ListServiceOperationsInputPaginateTypeDef",
    "ListServiceOperationsInputTypeDef",
    "ListServiceOperationsOutputTypeDef",
    "ListServiceStatesInputPaginateTypeDef",
    "ListServiceStatesInputTypeDef",
    "ListServiceStatesOutputTypeDef",
    "ListServicesInputPaginateTypeDef",
    "ListServicesInputTypeDef",
    "ListServicesOutputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricDataQueryOutputTypeDef",
    "MetricDataQueryTypeDef",
    "MetricDataQueryUnionTypeDef",
    "MetricGraphTypeDef",
    "MetricOutputTypeDef",
    "MetricReferenceTypeDef",
    "MetricStatOutputTypeDef",
    "MetricStatTypeDef",
    "MetricStatUnionTypeDef",
    "MetricTypeDef",
    "MetricUnionTypeDef",
    "MonitoredRequestCountMetricDataQueriesOutputTypeDef",
    "MonitoredRequestCountMetricDataQueriesTypeDef",
    "MonitoredRequestCountMetricDataQueriesUnionTypeDef",
    "NodeTypeDef",
    "PaginatorConfigTypeDef",
    "PutGroupingConfigurationInputTypeDef",
    "PutGroupingConfigurationOutputTypeDef",
    "RecurrenceRuleTypeDef",
    "RequestBasedServiceLevelIndicatorConfigTypeDef",
    "RequestBasedServiceLevelIndicatorMetricConfigTypeDef",
    "RequestBasedServiceLevelIndicatorMetricTypeDef",
    "RequestBasedServiceLevelIndicatorTypeDef",
    "ResponseMetadataTypeDef",
    "RollingIntervalTypeDef",
    "ServiceDependencyTypeDef",
    "ServiceDependentTypeDef",
    "ServiceEntityTypeDef",
    "ServiceGroupTypeDef",
    "ServiceLevelIndicatorConfigTypeDef",
    "ServiceLevelIndicatorMetricConfigTypeDef",
    "ServiceLevelIndicatorMetricTypeDef",
    "ServiceLevelIndicatorTypeDef",
    "ServiceLevelObjectiveBudgetReportErrorTypeDef",
    "ServiceLevelObjectiveBudgetReportTypeDef",
    "ServiceLevelObjectiveEntityTypeDef",
    "ServiceLevelObjectiveSummaryTypeDef",
    "ServiceLevelObjectiveTypeDef",
    "ServiceOperationEntityTypeDef",
    "ServiceOperationTypeDef",
    "ServiceStateTypeDef",
    "ServiceSummaryTypeDef",
    "ServiceTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateServiceLevelObjectiveInputTypeDef",
    "UpdateServiceLevelObjectiveOutputTypeDef",
    "WindowTypeDef",
)

class AttributeFilterOutputTypeDef(TypedDict):
    AttributeFilterName: str
    AttributeFilterValues: list[str]

class AttributeFilterTypeDef(TypedDict):
    AttributeFilterName: str
    AttributeFilterValues: Sequence[str]

class AuditorResultTypeDef(TypedDict):
    Auditor: NotRequired[str]
    Description: NotRequired[str]
    Data: NotRequired[dict[str, str]]
    Severity: NotRequired[SeverityType]

class CanaryEntityTypeDef(TypedDict):
    CanaryName: str

ServiceEntityTypeDef = TypedDict(
    "ServiceEntityTypeDef",
    {
        "Type": NotRequired[str],
        "Name": NotRequired[str],
        "Environment": NotRequired[str],
        "AwsAccountId": NotRequired[str],
    },
)

class ServiceLevelObjectiveEntityTypeDef(TypedDict):
    SloName: NotRequired[str]
    SloArn: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ServiceLevelObjectiveBudgetReportErrorTypeDef(TypedDict):
    Name: str
    Arn: str
    ErrorCode: str
    ErrorMessage: str

class BatchUpdateExclusionWindowsErrorTypeDef(TypedDict):
    SloId: str
    ErrorCode: str
    ErrorMessage: str

class BurnRateConfigurationTypeDef(TypedDict):
    LookBackWindowMinutes: int

class CalendarIntervalOutputTypeDef(TypedDict):
    StartTime: datetime
    DurationUnit: DurationUnitType
    Duration: int

class ChangeEventTypeDef(TypedDict):
    Timestamp: datetime
    AccountId: str
    Region: str
    Entity: dict[str, str]
    ChangeEventType: ChangeEventTypeType
    EventId: str
    UserName: NotRequired[str]
    EventName: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class DeleteServiceLevelObjectiveInputTypeDef(TypedDict):
    Id: str

class DependencyConfigOutputTypeDef(TypedDict):
    DependencyKeyAttributes: dict[str, str]
    DependencyOperationName: str

class DependencyConfigTypeDef(TypedDict):
    DependencyKeyAttributes: Mapping[str, str]
    DependencyOperationName: str

class EdgeTypeDef(TypedDict):
    SourceNodeId: NotRequired[str]
    DestinationNodeId: NotRequired[str]
    Duration: NotRequired[float]
    ConnectionType: NotRequired[ConnectionTypeType]

NodeTypeDef = TypedDict(
    "NodeTypeDef",
    {
        "KeyAttributes": dict[str, str],
        "Name": str,
        "NodeId": str,
        "Operation": NotRequired[str],
        "Type": NotRequired[str],
        "Duration": NotRequired[float],
        "Status": NotRequired[str],
    },
)

class DimensionTypeDef(TypedDict):
    Name: str
    Value: str

class RecurrenceRuleTypeDef(TypedDict):
    Expression: str

class WindowTypeDef(TypedDict):
    DurationUnit: DurationUnitType
    Duration: int

class GetServiceLevelObjectiveInputTypeDef(TypedDict):
    Id: str

class GroupingAttributeDefinitionOutputTypeDef(TypedDict):
    GroupingName: str
    GroupingSourceKeys: NotRequired[list[str]]
    DefaultGroupingValue: NotRequired[str]

class GroupingAttributeDefinitionTypeDef(TypedDict):
    GroupingName: str
    GroupingSourceKeys: NotRequired[Sequence[str]]
    DefaultGroupingValue: NotRequired[str]

class RollingIntervalTypeDef(TypedDict):
    DurationUnit: DurationUnitType
    Duration: int

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListGroupingAttributeDefinitionsInputTypeDef(TypedDict):
    NextToken: NotRequired[str]
    AwsAccountId: NotRequired[str]
    IncludeLinkedAccounts: NotRequired[bool]

class ListServiceLevelObjectiveExclusionWindowsInputTypeDef(TypedDict):
    Id: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str

class ServiceGroupTypeDef(TypedDict):
    GroupName: str
    GroupValue: str
    GroupSource: str
    GroupIdentifier: str

class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

AttributeFilterUnionTypeDef = Union[AttributeFilterTypeDef, AttributeFilterOutputTypeDef]

class ServiceOperationEntityTypeDef(TypedDict):
    Service: NotRequired[ServiceEntityTypeDef]
    Operation: NotRequired[str]
    MetricType: NotRequired[str]

class BatchGetServiceLevelObjectiveBudgetReportInputTypeDef(TypedDict):
    Timestamp: TimestampTypeDef
    SloIds: Sequence[str]

class CalendarIntervalTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    DurationUnit: DurationUnitType
    Duration: int

class GetServiceInputTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]

class ListEntityEventsInputTypeDef(TypedDict):
    Entity: Mapping[str, str]
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListServiceDependenciesInputTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListServiceDependentsInputTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListServiceOperationsInputTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListServicesInputTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    IncludeLinkedAccounts: NotRequired[bool]
    AwsAccountId: NotRequired[str]

class BatchUpdateExclusionWindowsOutputTypeDef(TypedDict):
    SloIds: list[str]
    Errors: list[BatchUpdateExclusionWindowsErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListEntityEventsOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ChangeEvents: list[ChangeEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ServiceStateTypeDef(TypedDict):
    Service: dict[str, str]
    LatestChangeEvents: list[ChangeEventTypeDef]
    AttributeFilters: NotRequired[list[AttributeFilterOutputTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class ServiceLevelObjectiveSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    KeyAttributes: NotRequired[dict[str, str]]
    OperationName: NotRequired[str]
    DependencyConfig: NotRequired[DependencyConfigOutputTypeDef]
    CreatedTime: NotRequired[datetime]
    EvaluationType: NotRequired[EvaluationTypeType]
    MetricSourceType: NotRequired[MetricSourceTypeType]

DependencyConfigUnionTypeDef = Union[DependencyConfigTypeDef, DependencyConfigOutputTypeDef]

class DependencyGraphTypeDef(TypedDict):
    Nodes: NotRequired[list[NodeTypeDef]]
    Edges: NotRequired[list[EdgeTypeDef]]

class MetricOutputTypeDef(TypedDict):
    Namespace: NotRequired[str]
    MetricName: NotRequired[str]
    Dimensions: NotRequired[list[DimensionTypeDef]]

class MetricReferenceTypeDef(TypedDict):
    Namespace: str
    MetricType: str
    MetricName: str
    Dimensions: NotRequired[list[DimensionTypeDef]]
    AccountId: NotRequired[str]

class MetricTypeDef(TypedDict):
    Namespace: NotRequired[str]
    MetricName: NotRequired[str]
    Dimensions: NotRequired[Sequence[DimensionTypeDef]]

class ExclusionWindowOutputTypeDef(TypedDict):
    Window: WindowTypeDef
    StartTime: NotRequired[datetime]
    RecurrenceRule: NotRequired[RecurrenceRuleTypeDef]
    Reason: NotRequired[str]

class ExclusionWindowTypeDef(TypedDict):
    Window: WindowTypeDef
    StartTime: NotRequired[TimestampTypeDef]
    RecurrenceRule: NotRequired[RecurrenceRuleTypeDef]
    Reason: NotRequired[str]

class GroupingConfigurationTypeDef(TypedDict):
    GroupingAttributeDefinitions: list[GroupingAttributeDefinitionOutputTypeDef]
    UpdatedAt: datetime

class ListGroupingAttributeDefinitionsOutputTypeDef(TypedDict):
    GroupingAttributeDefinitions: list[GroupingAttributeDefinitionOutputTypeDef]
    UpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

GroupingAttributeDefinitionUnionTypeDef = Union[
    GroupingAttributeDefinitionTypeDef, GroupingAttributeDefinitionOutputTypeDef
]

class IntervalOutputTypeDef(TypedDict):
    RollingInterval: NotRequired[RollingIntervalTypeDef]
    CalendarInterval: NotRequired[CalendarIntervalOutputTypeDef]

class ListEntityEventsInputPaginateTypeDef(TypedDict):
    Entity: Mapping[str, str]
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceDependenciesInputPaginateTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceDependentsInputPaginateTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceLevelObjectiveExclusionWindowsInputPaginateTypeDef(TypedDict):
    Id: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceOperationsInputPaginateTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    KeyAttributes: Mapping[str, str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServicesInputPaginateTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    IncludeLinkedAccounts: NotRequired[bool]
    AwsAccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceStatesInputPaginateTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    IncludeLinkedAccounts: NotRequired[bool]
    AwsAccountId: NotRequired[str]
    AttributeFilters: NotRequired[Sequence[AttributeFilterUnionTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceStatesInputTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    IncludeLinkedAccounts: NotRequired[bool]
    AwsAccountId: NotRequired[str]
    AttributeFilters: NotRequired[Sequence[AttributeFilterUnionTypeDef]]

class AuditTargetEntityTypeDef(TypedDict):
    Service: NotRequired[ServiceEntityTypeDef]
    Slo: NotRequired[ServiceLevelObjectiveEntityTypeDef]
    ServiceOperation: NotRequired[ServiceOperationEntityTypeDef]
    Canary: NotRequired[CanaryEntityTypeDef]

class IntervalTypeDef(TypedDict):
    RollingInterval: NotRequired[RollingIntervalTypeDef]
    CalendarInterval: NotRequired[CalendarIntervalTypeDef]

class ListServiceStatesOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ServiceStates: list[ServiceStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListServiceLevelObjectivesOutputTypeDef(TypedDict):
    SloSummaries: list[ServiceLevelObjectiveSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListServiceLevelObjectivesInputPaginateTypeDef(TypedDict):
    KeyAttributes: NotRequired[Mapping[str, str]]
    OperationName: NotRequired[str]
    DependencyConfig: NotRequired[DependencyConfigUnionTypeDef]
    IncludeLinkedAccounts: NotRequired[bool]
    SloOwnerAwsAccountId: NotRequired[str]
    MetricSourceTypes: NotRequired[Sequence[MetricSourceTypeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceLevelObjectivesInputTypeDef(TypedDict):
    KeyAttributes: NotRequired[Mapping[str, str]]
    OperationName: NotRequired[str]
    DependencyConfig: NotRequired[DependencyConfigUnionTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    IncludeLinkedAccounts: NotRequired[bool]
    SloOwnerAwsAccountId: NotRequired[str]
    MetricSourceTypes: NotRequired[Sequence[MetricSourceTypeType]]

class MetricStatOutputTypeDef(TypedDict):
    Metric: MetricOutputTypeDef
    Period: int
    Stat: str
    Unit: NotRequired[StandardUnitType]

class ServiceDependencyTypeDef(TypedDict):
    OperationName: str
    DependencyKeyAttributes: dict[str, str]
    DependencyOperationName: str
    MetricReferences: list[MetricReferenceTypeDef]

class ServiceDependentTypeDef(TypedDict):
    DependentKeyAttributes: dict[str, str]
    MetricReferences: list[MetricReferenceTypeDef]
    OperationName: NotRequired[str]
    DependentOperationName: NotRequired[str]

class ServiceOperationTypeDef(TypedDict):
    Name: str
    MetricReferences: list[MetricReferenceTypeDef]

class ServiceSummaryTypeDef(TypedDict):
    KeyAttributes: dict[str, str]
    MetricReferences: list[MetricReferenceTypeDef]
    AttributeMaps: NotRequired[list[dict[str, str]]]
    ServiceGroups: NotRequired[list[ServiceGroupTypeDef]]

class ServiceTypeDef(TypedDict):
    KeyAttributes: dict[str, str]
    MetricReferences: list[MetricReferenceTypeDef]
    AttributeMaps: NotRequired[list[dict[str, str]]]
    ServiceGroups: NotRequired[list[ServiceGroupTypeDef]]
    LogGroupReferences: NotRequired[list[dict[str, str]]]

MetricUnionTypeDef = Union[MetricTypeDef, MetricOutputTypeDef]

class ListServiceLevelObjectiveExclusionWindowsOutputTypeDef(TypedDict):
    ExclusionWindows: list[ExclusionWindowOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

ExclusionWindowUnionTypeDef = Union[ExclusionWindowTypeDef, ExclusionWindowOutputTypeDef]

class PutGroupingConfigurationOutputTypeDef(TypedDict):
    GroupingConfiguration: GroupingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutGroupingConfigurationInputTypeDef(TypedDict):
    GroupingAttributeDefinitions: Sequence[GroupingAttributeDefinitionUnionTypeDef]

class GoalOutputTypeDef(TypedDict):
    Interval: NotRequired[IntervalOutputTypeDef]
    AttainmentGoal: NotRequired[float]
    WarningThreshold: NotRequired[float]

AuditTargetTypeDef = TypedDict(
    "AuditTargetTypeDef",
    {
        "Type": str,
        "Data": AuditTargetEntityTypeDef,
    },
)

class GoalTypeDef(TypedDict):
    Interval: NotRequired[IntervalTypeDef]
    AttainmentGoal: NotRequired[float]
    WarningThreshold: NotRequired[float]

class MetricDataQueryOutputTypeDef(TypedDict):
    Id: str
    MetricStat: NotRequired[MetricStatOutputTypeDef]
    Expression: NotRequired[str]
    Label: NotRequired[str]
    ReturnData: NotRequired[bool]
    Period: NotRequired[int]
    AccountId: NotRequired[str]

class ListServiceDependenciesOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ServiceDependencies: list[ServiceDependencyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListServiceDependentsOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ServiceDependents: list[ServiceDependentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListServiceOperationsOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ServiceOperations: list[ServiceOperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListServicesOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    ServiceSummaries: list[ServiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetServiceOutputTypeDef(TypedDict):
    Service: ServiceTypeDef
    StartTime: datetime
    EndTime: datetime
    LogGroupReferences: list[dict[str, str]]
    ResponseMetadata: ResponseMetadataTypeDef

class MetricStatTypeDef(TypedDict):
    Metric: MetricUnionTypeDef
    Period: int
    Stat: str
    Unit: NotRequired[StandardUnitType]

class BatchUpdateExclusionWindowsInputTypeDef(TypedDict):
    SloIds: Sequence[str]
    AddExclusionWindows: NotRequired[Sequence[ExclusionWindowUnionTypeDef]]
    RemoveExclusionWindows: NotRequired[Sequence[ExclusionWindowUnionTypeDef]]

class ListAuditFindingsInputTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    AuditTargets: Sequence[AuditTargetTypeDef]
    Auditors: NotRequired[Sequence[str]]
    DetailLevel: NotRequired[DetailLevelType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

GoalUnionTypeDef = Union[GoalTypeDef, GoalOutputTypeDef]

class MetricGraphTypeDef(TypedDict):
    MetricDataQueries: NotRequired[list[MetricDataQueryOutputTypeDef]]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]

class MonitoredRequestCountMetricDataQueriesOutputTypeDef(TypedDict):
    GoodCountMetric: NotRequired[list[MetricDataQueryOutputTypeDef]]
    BadCountMetric: NotRequired[list[MetricDataQueryOutputTypeDef]]

class ServiceLevelIndicatorMetricTypeDef(TypedDict):
    MetricDataQueries: list[MetricDataQueryOutputTypeDef]
    KeyAttributes: NotRequired[dict[str, str]]
    OperationName: NotRequired[str]
    MetricType: NotRequired[ServiceLevelIndicatorMetricTypeType]
    DependencyConfig: NotRequired[DependencyConfigOutputTypeDef]

MetricStatUnionTypeDef = Union[MetricStatTypeDef, MetricStatOutputTypeDef]
AuditFindingTypeDef = TypedDict(
    "AuditFindingTypeDef",
    {
        "KeyAttributes": dict[str, str],
        "AuditorResults": NotRequired[list[AuditorResultTypeDef]],
        "Operation": NotRequired[str],
        "MetricGraph": NotRequired[MetricGraphTypeDef],
        "DependencyGraph": NotRequired[DependencyGraphTypeDef],
        "Type": NotRequired[str],
    },
)

class RequestBasedServiceLevelIndicatorMetricTypeDef(TypedDict):
    TotalRequestCountMetric: list[MetricDataQueryOutputTypeDef]
    MonitoredRequestCountMetric: MonitoredRequestCountMetricDataQueriesOutputTypeDef
    KeyAttributes: NotRequired[dict[str, str]]
    OperationName: NotRequired[str]
    MetricType: NotRequired[ServiceLevelIndicatorMetricTypeType]
    DependencyConfig: NotRequired[DependencyConfigOutputTypeDef]

class ServiceLevelIndicatorTypeDef(TypedDict):
    SliMetric: ServiceLevelIndicatorMetricTypeDef
    MetricThreshold: float
    ComparisonOperator: ServiceLevelIndicatorComparisonOperatorType

class MetricDataQueryTypeDef(TypedDict):
    Id: str
    MetricStat: NotRequired[MetricStatUnionTypeDef]
    Expression: NotRequired[str]
    Label: NotRequired[str]
    ReturnData: NotRequired[bool]
    Period: NotRequired[int]
    AccountId: NotRequired[str]

class ListAuditFindingsOutputTypeDef(TypedDict):
    StartTime: datetime
    EndTime: datetime
    AuditFindings: list[AuditFindingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RequestBasedServiceLevelIndicatorTypeDef(TypedDict):
    RequestBasedSliMetric: RequestBasedServiceLevelIndicatorMetricTypeDef
    MetricThreshold: NotRequired[float]
    ComparisonOperator: NotRequired[ServiceLevelIndicatorComparisonOperatorType]

MetricDataQueryUnionTypeDef = Union[MetricDataQueryTypeDef, MetricDataQueryOutputTypeDef]

class ServiceLevelObjectiveBudgetReportTypeDef(TypedDict):
    Arn: str
    Name: str
    BudgetStatus: ServiceLevelObjectiveBudgetStatusType
    EvaluationType: NotRequired[EvaluationTypeType]
    Attainment: NotRequired[float]
    TotalBudgetSeconds: NotRequired[int]
    BudgetSecondsRemaining: NotRequired[int]
    TotalBudgetRequests: NotRequired[int]
    BudgetRequestsRemaining: NotRequired[int]
    Sli: NotRequired[ServiceLevelIndicatorTypeDef]
    RequestBasedSli: NotRequired[RequestBasedServiceLevelIndicatorTypeDef]
    Goal: NotRequired[GoalOutputTypeDef]

class ServiceLevelObjectiveTypeDef(TypedDict):
    Arn: str
    Name: str
    CreatedTime: datetime
    LastUpdatedTime: datetime
    Goal: GoalOutputTypeDef
    Description: NotRequired[str]
    Sli: NotRequired[ServiceLevelIndicatorTypeDef]
    RequestBasedSli: NotRequired[RequestBasedServiceLevelIndicatorTypeDef]
    EvaluationType: NotRequired[EvaluationTypeType]
    BurnRateConfigurations: NotRequired[list[BurnRateConfigurationTypeDef]]
    MetricSourceType: NotRequired[MetricSourceTypeType]

class MonitoredRequestCountMetricDataQueriesTypeDef(TypedDict):
    GoodCountMetric: NotRequired[Sequence[MetricDataQueryUnionTypeDef]]
    BadCountMetric: NotRequired[Sequence[MetricDataQueryTypeDef]]

class ServiceLevelIndicatorMetricConfigTypeDef(TypedDict):
    KeyAttributes: NotRequired[Mapping[str, str]]
    OperationName: NotRequired[str]
    MetricType: NotRequired[ServiceLevelIndicatorMetricTypeType]
    MetricName: NotRequired[str]
    Statistic: NotRequired[str]
    PeriodSeconds: NotRequired[int]
    MetricDataQueries: NotRequired[Sequence[MetricDataQueryUnionTypeDef]]
    DependencyConfig: NotRequired[DependencyConfigUnionTypeDef]

class BatchGetServiceLevelObjectiveBudgetReportOutputTypeDef(TypedDict):
    Timestamp: datetime
    Reports: list[ServiceLevelObjectiveBudgetReportTypeDef]
    Errors: list[ServiceLevelObjectiveBudgetReportErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateServiceLevelObjectiveOutputTypeDef(TypedDict):
    Slo: ServiceLevelObjectiveTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetServiceLevelObjectiveOutputTypeDef(TypedDict):
    Slo: ServiceLevelObjectiveTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceLevelObjectiveOutputTypeDef(TypedDict):
    Slo: ServiceLevelObjectiveTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

MonitoredRequestCountMetricDataQueriesUnionTypeDef = Union[
    MonitoredRequestCountMetricDataQueriesTypeDef,
    MonitoredRequestCountMetricDataQueriesOutputTypeDef,
]

class ServiceLevelIndicatorConfigTypeDef(TypedDict):
    SliMetricConfig: ServiceLevelIndicatorMetricConfigTypeDef
    MetricThreshold: float
    ComparisonOperator: ServiceLevelIndicatorComparisonOperatorType

class RequestBasedServiceLevelIndicatorMetricConfigTypeDef(TypedDict):
    KeyAttributes: NotRequired[Mapping[str, str]]
    OperationName: NotRequired[str]
    MetricType: NotRequired[ServiceLevelIndicatorMetricTypeType]
    TotalRequestCountMetric: NotRequired[Sequence[MetricDataQueryUnionTypeDef]]
    MonitoredRequestCountMetric: NotRequired[MonitoredRequestCountMetricDataQueriesUnionTypeDef]
    DependencyConfig: NotRequired[DependencyConfigUnionTypeDef]

class RequestBasedServiceLevelIndicatorConfigTypeDef(TypedDict):
    RequestBasedSliMetricConfig: RequestBasedServiceLevelIndicatorMetricConfigTypeDef
    MetricThreshold: NotRequired[float]
    ComparisonOperator: NotRequired[ServiceLevelIndicatorComparisonOperatorType]

class CreateServiceLevelObjectiveInputTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    SliConfig: NotRequired[ServiceLevelIndicatorConfigTypeDef]
    RequestBasedSliConfig: NotRequired[RequestBasedServiceLevelIndicatorConfigTypeDef]
    Goal: NotRequired[GoalUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    BurnRateConfigurations: NotRequired[Sequence[BurnRateConfigurationTypeDef]]

class UpdateServiceLevelObjectiveInputTypeDef(TypedDict):
    Id: str
    Description: NotRequired[str]
    SliConfig: NotRequired[ServiceLevelIndicatorConfigTypeDef]
    RequestBasedSliConfig: NotRequired[RequestBasedServiceLevelIndicatorConfigTypeDef]
    Goal: NotRequired[GoalUnionTypeDef]
    BurnRateConfigurations: NotRequired[Sequence[BurnRateConfigurationTypeDef]]
