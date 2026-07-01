"""
Type annotations for bcm-dashboards service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_dashboards/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_bcm_dashboards.type_defs import GroupDefinitionTypeDef

    data: GroupDefinitionTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    DateTimeTypeType,
    DimensionType,
    GranularityType,
    GroupDefinitionTypeType,
    HealthStatusCodeType,
    MatchOptionType,
    MetricNameType,
    ScheduleStateType,
    StatusReasonType,
    VisualTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "CostAndUsageQueryOutputTypeDef",
    "CostAndUsageQueryTypeDef",
    "CostAndUsageQueryUnionTypeDef",
    "CostCategoryValuesOutputTypeDef",
    "CostCategoryValuesTypeDef",
    "CostCategoryValuesUnionTypeDef",
    "CreateDashboardRequestTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateScheduledReportRequestTypeDef",
    "CreateScheduledReportResponseTypeDef",
    "DashboardReferenceTypeDef",
    "DateTimeRangeTypeDef",
    "DateTimeValueTypeDef",
    "DeleteDashboardRequestTypeDef",
    "DeleteDashboardResponseTypeDef",
    "DeleteScheduledReportRequestTypeDef",
    "DeleteScheduledReportResponseTypeDef",
    "DimensionValuesOutputTypeDef",
    "DimensionValuesTypeDef",
    "DimensionValuesUnionTypeDef",
    "DisplayConfigOutputTypeDef",
    "DisplayConfigTypeDef",
    "DisplayConfigUnionTypeDef",
    "ExecuteScheduledReportRequestTypeDef",
    "ExecuteScheduledReportResponseTypeDef",
    "ExpressionOutputTypeDef",
    "ExpressionTypeDef",
    "ExpressionUnionTypeDef",
    "GetDashboardRequestTypeDef",
    "GetDashboardResponseTypeDef",
    "GetResourcePolicyRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetScheduledReportRequestTypeDef",
    "GetScheduledReportResponseTypeDef",
    "GraphDisplayConfigTypeDef",
    "GroupDefinitionTypeDef",
    "HealthStatusTypeDef",
    "ListDashboardsRequestPaginateTypeDef",
    "ListDashboardsRequestTypeDef",
    "ListDashboardsResponseTypeDef",
    "ListScheduledReportsRequestPaginateTypeDef",
    "ListScheduledReportsRequestTypeDef",
    "ListScheduledReportsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "QueryParametersOutputTypeDef",
    "QueryParametersTypeDef",
    "QueryParametersUnionTypeDef",
    "ReservationCoverageQueryOutputTypeDef",
    "ReservationCoverageQueryTypeDef",
    "ReservationCoverageQueryUnionTypeDef",
    "ReservationUtilizationQueryOutputTypeDef",
    "ReservationUtilizationQueryTypeDef",
    "ReservationUtilizationQueryUnionTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "SavingsPlansCoverageQueryOutputTypeDef",
    "SavingsPlansCoverageQueryTypeDef",
    "SavingsPlansCoverageQueryUnionTypeDef",
    "SavingsPlansUtilizationQueryOutputTypeDef",
    "SavingsPlansUtilizationQueryTypeDef",
    "SavingsPlansUtilizationQueryUnionTypeDef",
    "ScheduleConfigOutputTypeDef",
    "ScheduleConfigTypeDef",
    "ScheduleConfigUnionTypeDef",
    "SchedulePeriodOutputTypeDef",
    "SchedulePeriodTypeDef",
    "SchedulePeriodUnionTypeDef",
    "ScheduledReportInputTypeDef",
    "ScheduledReportSummaryTypeDef",
    "ScheduledReportTypeDef",
    "TagResourceRequestTypeDef",
    "TagValuesOutputTypeDef",
    "TagValuesTypeDef",
    "TagValuesUnionTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateDashboardRequestTypeDef",
    "UpdateDashboardResponseTypeDef",
    "UpdateScheduledReportRequestTypeDef",
    "UpdateScheduledReportResponseTypeDef",
    "WidgetConfigOutputTypeDef",
    "WidgetConfigTypeDef",
    "WidgetConfigUnionTypeDef",
    "WidgetOutputTypeDef",
    "WidgetTypeDef",
    "WidgetUnionTypeDef",
)

GroupDefinitionTypeDef = TypedDict(
    "GroupDefinitionTypeDef",
    {
        "key": str,
        "type": NotRequired[GroupDefinitionTypeType],
    },
)

class CostCategoryValuesOutputTypeDef(TypedDict):
    key: NotRequired[str]
    values: NotRequired[list[str]]
    matchOptions: NotRequired[list[MatchOptionType]]

class CostCategoryValuesTypeDef(TypedDict):
    key: NotRequired[str]
    values: NotRequired[Sequence[str]]
    matchOptions: NotRequired[Sequence[MatchOptionType]]

class ResourceTagTypeDef(TypedDict):
    key: str
    value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

DashboardReferenceTypeDef = TypedDict(
    "DashboardReferenceTypeDef",
    {
        "arn": str,
        "name": str,
        "type": Literal["CUSTOM"],
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
DateTimeValueTypeDef = TypedDict(
    "DateTimeValueTypeDef",
    {
        "type": DateTimeTypeType,
        "value": str,
    },
)

class DeleteDashboardRequestTypeDef(TypedDict):
    arn: str

class DeleteScheduledReportRequestTypeDef(TypedDict):
    arn: str

class DimensionValuesOutputTypeDef(TypedDict):
    key: DimensionType
    values: list[str]
    matchOptions: NotRequired[list[MatchOptionType]]

class DimensionValuesTypeDef(TypedDict):
    key: DimensionType
    values: Sequence[str]
    matchOptions: NotRequired[Sequence[MatchOptionType]]

class GraphDisplayConfigTypeDef(TypedDict):
    visualType: VisualTypeType

class ExecuteScheduledReportRequestTypeDef(TypedDict):
    arn: str
    clientToken: NotRequired[str]
    dryRun: NotRequired[bool]

class HealthStatusTypeDef(TypedDict):
    statusCode: HealthStatusCodeType
    lastRefreshedAt: NotRequired[datetime]
    statusReasons: NotRequired[list[StatusReasonType]]

class TagValuesOutputTypeDef(TypedDict):
    key: NotRequired[str]
    values: NotRequired[list[str]]
    matchOptions: NotRequired[list[MatchOptionType]]

class GetDashboardRequestTypeDef(TypedDict):
    arn: str

class GetResourcePolicyRequestTypeDef(TypedDict):
    resourceArn: str

class GetScheduledReportRequestTypeDef(TypedDict):
    arn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDashboardsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListScheduledReportsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class SchedulePeriodOutputTypeDef(TypedDict):
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]

TimestampTypeDef = Union[datetime, str]

class TagValuesTypeDef(TypedDict):
    key: NotRequired[str]
    values: NotRequired[Sequence[str]]
    matchOptions: NotRequired[Sequence[MatchOptionType]]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    resourceTagKeys: Sequence[str]

CostCategoryValuesUnionTypeDef = Union[CostCategoryValuesTypeDef, CostCategoryValuesOutputTypeDef]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    resourceTags: Sequence[ResourceTagTypeDef]

class CreateDashboardResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateScheduledReportResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDashboardResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteScheduledReportResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyResponseTypeDef(TypedDict):
    resourceArn: str
    policyDocument: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    resourceTags: list[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDashboardResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateScheduledReportResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListDashboardsResponseTypeDef(TypedDict):
    dashboards: list[DashboardReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DateTimeRangeTypeDef(TypedDict):
    startTime: DateTimeValueTypeDef
    endTime: DateTimeValueTypeDef

DimensionValuesUnionTypeDef = Union[DimensionValuesTypeDef, DimensionValuesOutputTypeDef]

class DisplayConfigOutputTypeDef(TypedDict):
    graph: NotRequired[dict[str, GraphDisplayConfigTypeDef]]
    table: NotRequired[dict[str, Any]]

class DisplayConfigTypeDef(TypedDict):
    graph: NotRequired[Mapping[str, GraphDisplayConfigTypeDef]]
    table: NotRequired[Mapping[str, Any]]

class ExecuteScheduledReportResponseTypeDef(TypedDict):
    healthStatus: HealthStatusTypeDef
    executionTriggered: bool
    ResponseMetadata: ResponseMetadataTypeDef

class ScheduledReportSummaryTypeDef(TypedDict):
    arn: str
    name: str
    dashboardArn: str
    scheduleExpression: str
    state: ScheduleStateType
    healthStatus: HealthStatusTypeDef
    scheduleExpressionTimeZone: NotRequired[str]
    widgetIds: NotRequired[list[str]]

ExpressionOutputTypeDef = TypedDict(
    "ExpressionOutputTypeDef",
    {
        "or": NotRequired[list[dict[str, Any]]],
        "and": NotRequired[list[dict[str, Any]]],
        "not": NotRequired[dict[str, Any]],
        "dimensions": NotRequired[DimensionValuesOutputTypeDef],
        "tags": NotRequired[TagValuesOutputTypeDef],
        "costCategories": NotRequired[CostCategoryValuesOutputTypeDef],
    },
)

class ListDashboardsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListScheduledReportsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ScheduleConfigOutputTypeDef(TypedDict):
    scheduleExpression: NotRequired[str]
    scheduleExpressionTimeZone: NotRequired[str]
    schedulePeriod: NotRequired[SchedulePeriodOutputTypeDef]
    state: NotRequired[ScheduleStateType]

class SchedulePeriodTypeDef(TypedDict):
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]

TagValuesUnionTypeDef = Union[TagValuesTypeDef, TagValuesOutputTypeDef]
DisplayConfigUnionTypeDef = Union[DisplayConfigTypeDef, DisplayConfigOutputTypeDef]

class ListScheduledReportsResponseTypeDef(TypedDict):
    scheduledReports: list[ScheduledReportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

CostAndUsageQueryOutputTypeDef = TypedDict(
    "CostAndUsageQueryOutputTypeDef",
    {
        "metrics": list[MetricNameType],
        "timeRange": DateTimeRangeTypeDef,
        "granularity": GranularityType,
        "groupBy": NotRequired[list[GroupDefinitionTypeDef]],
        "filter": NotRequired[ExpressionOutputTypeDef],
    },
)
ReservationCoverageQueryOutputTypeDef = TypedDict(
    "ReservationCoverageQueryOutputTypeDef",
    {
        "timeRange": DateTimeRangeTypeDef,
        "groupBy": NotRequired[list[GroupDefinitionTypeDef]],
        "granularity": NotRequired[GranularityType],
        "filter": NotRequired[ExpressionOutputTypeDef],
        "metrics": NotRequired[list[MetricNameType]],
    },
)
ReservationUtilizationQueryOutputTypeDef = TypedDict(
    "ReservationUtilizationQueryOutputTypeDef",
    {
        "timeRange": DateTimeRangeTypeDef,
        "groupBy": NotRequired[list[GroupDefinitionTypeDef]],
        "granularity": NotRequired[GranularityType],
        "filter": NotRequired[ExpressionOutputTypeDef],
    },
)
SavingsPlansCoverageQueryOutputTypeDef = TypedDict(
    "SavingsPlansCoverageQueryOutputTypeDef",
    {
        "timeRange": DateTimeRangeTypeDef,
        "metrics": NotRequired[list[MetricNameType]],
        "granularity": NotRequired[GranularityType],
        "groupBy": NotRequired[list[GroupDefinitionTypeDef]],
        "filter": NotRequired[ExpressionOutputTypeDef],
    },
)
SavingsPlansUtilizationQueryOutputTypeDef = TypedDict(
    "SavingsPlansUtilizationQueryOutputTypeDef",
    {
        "timeRange": DateTimeRangeTypeDef,
        "granularity": NotRequired[GranularityType],
        "filter": NotRequired[ExpressionOutputTypeDef],
    },
)

class ScheduledReportTypeDef(TypedDict):
    name: str
    dashboardArn: str
    scheduledReportExecutionRoleArn: str
    scheduleConfig: ScheduleConfigOutputTypeDef
    arn: NotRequired[str]
    description: NotRequired[str]
    widgetIds: NotRequired[list[str]]
    widgetDateRangeOverride: NotRequired[DateTimeRangeTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    lastExecutionAt: NotRequired[datetime]
    healthStatus: NotRequired[HealthStatusTypeDef]

SchedulePeriodUnionTypeDef = Union[SchedulePeriodTypeDef, SchedulePeriodOutputTypeDef]
ExpressionTypeDef = TypedDict(
    "ExpressionTypeDef",
    {
        "or": NotRequired[Sequence[Mapping[str, Any]]],
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "not": NotRequired[Mapping[str, Any]],
        "dimensions": NotRequired[DimensionValuesUnionTypeDef],
        "tags": NotRequired[TagValuesUnionTypeDef],
        "costCategories": NotRequired[CostCategoryValuesUnionTypeDef],
    },
)

class QueryParametersOutputTypeDef(TypedDict):
    costAndUsage: NotRequired[CostAndUsageQueryOutputTypeDef]
    savingsPlansCoverage: NotRequired[SavingsPlansCoverageQueryOutputTypeDef]
    savingsPlansUtilization: NotRequired[SavingsPlansUtilizationQueryOutputTypeDef]
    reservationCoverage: NotRequired[ReservationCoverageQueryOutputTypeDef]
    reservationUtilization: NotRequired[ReservationUtilizationQueryOutputTypeDef]

class GetScheduledReportResponseTypeDef(TypedDict):
    scheduledReport: ScheduledReportTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ScheduleConfigTypeDef(TypedDict):
    scheduleExpression: NotRequired[str]
    scheduleExpressionTimeZone: NotRequired[str]
    schedulePeriod: NotRequired[SchedulePeriodUnionTypeDef]
    state: NotRequired[ScheduleStateType]

ExpressionUnionTypeDef = Union[ExpressionTypeDef, ExpressionOutputTypeDef]

class WidgetConfigOutputTypeDef(TypedDict):
    queryParameters: QueryParametersOutputTypeDef
    displayConfig: DisplayConfigOutputTypeDef

ScheduleConfigUnionTypeDef = Union[ScheduleConfigTypeDef, ScheduleConfigOutputTypeDef]
CostAndUsageQueryTypeDef = TypedDict(
    "CostAndUsageQueryTypeDef",
    {
        "metrics": Sequence[MetricNameType],
        "timeRange": DateTimeRangeTypeDef,
        "granularity": GranularityType,
        "groupBy": NotRequired[Sequence[GroupDefinitionTypeDef]],
        "filter": NotRequired[ExpressionUnionTypeDef],
    },
)
ReservationCoverageQueryTypeDef = TypedDict(
    "ReservationCoverageQueryTypeDef",
    {
        "timeRange": DateTimeRangeTypeDef,
        "groupBy": NotRequired[Sequence[GroupDefinitionTypeDef]],
        "granularity": NotRequired[GranularityType],
        "filter": NotRequired[ExpressionUnionTypeDef],
        "metrics": NotRequired[Sequence[MetricNameType]],
    },
)
ReservationUtilizationQueryTypeDef = TypedDict(
    "ReservationUtilizationQueryTypeDef",
    {
        "timeRange": DateTimeRangeTypeDef,
        "groupBy": NotRequired[Sequence[GroupDefinitionTypeDef]],
        "granularity": NotRequired[GranularityType],
        "filter": NotRequired[ExpressionUnionTypeDef],
    },
)
SavingsPlansCoverageQueryTypeDef = TypedDict(
    "SavingsPlansCoverageQueryTypeDef",
    {
        "timeRange": DateTimeRangeTypeDef,
        "metrics": NotRequired[Sequence[MetricNameType]],
        "granularity": NotRequired[GranularityType],
        "groupBy": NotRequired[Sequence[GroupDefinitionTypeDef]],
        "filter": NotRequired[ExpressionUnionTypeDef],
    },
)
SavingsPlansUtilizationQueryTypeDef = TypedDict(
    "SavingsPlansUtilizationQueryTypeDef",
    {
        "timeRange": DateTimeRangeTypeDef,
        "granularity": NotRequired[GranularityType],
        "filter": NotRequired[ExpressionUnionTypeDef],
    },
)
WidgetOutputTypeDef = TypedDict(
    "WidgetOutputTypeDef",
    {
        "title": str,
        "configs": list[WidgetConfigOutputTypeDef],
        "id": NotRequired[str],
        "description": NotRequired[str],
        "width": NotRequired[int],
        "height": NotRequired[int],
        "horizontalOffset": NotRequired[int],
    },
)

class ScheduledReportInputTypeDef(TypedDict):
    name: str
    dashboardArn: str
    scheduledReportExecutionRoleArn: str
    scheduleConfig: ScheduleConfigUnionTypeDef
    description: NotRequired[str]
    widgetIds: NotRequired[Sequence[str]]
    widgetDateRangeOverride: NotRequired[DateTimeRangeTypeDef]

class UpdateScheduledReportRequestTypeDef(TypedDict):
    arn: str
    name: NotRequired[str]
    description: NotRequired[str]
    dashboardArn: NotRequired[str]
    scheduledReportExecutionRoleArn: NotRequired[str]
    scheduleConfig: NotRequired[ScheduleConfigUnionTypeDef]
    widgetIds: NotRequired[Sequence[str]]
    widgetDateRangeOverride: NotRequired[DateTimeRangeTypeDef]
    clearWidgetIds: NotRequired[bool]
    clearWidgetDateRangeOverride: NotRequired[bool]

CostAndUsageQueryUnionTypeDef = Union[CostAndUsageQueryTypeDef, CostAndUsageQueryOutputTypeDef]
ReservationCoverageQueryUnionTypeDef = Union[
    ReservationCoverageQueryTypeDef, ReservationCoverageQueryOutputTypeDef
]
ReservationUtilizationQueryUnionTypeDef = Union[
    ReservationUtilizationQueryTypeDef, ReservationUtilizationQueryOutputTypeDef
]
SavingsPlansCoverageQueryUnionTypeDef = Union[
    SavingsPlansCoverageQueryTypeDef, SavingsPlansCoverageQueryOutputTypeDef
]
SavingsPlansUtilizationQueryUnionTypeDef = Union[
    SavingsPlansUtilizationQueryTypeDef, SavingsPlansUtilizationQueryOutputTypeDef
]
GetDashboardResponseTypeDef = TypedDict(
    "GetDashboardResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "description": str,
        "type": Literal["CUSTOM"],
        "widgets": list[WidgetOutputTypeDef],
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateScheduledReportRequestTypeDef(TypedDict):
    scheduledReport: ScheduledReportInputTypeDef
    resourceTags: NotRequired[Sequence[ResourceTagTypeDef]]
    clientToken: NotRequired[str]

class QueryParametersTypeDef(TypedDict):
    costAndUsage: NotRequired[CostAndUsageQueryUnionTypeDef]
    savingsPlansCoverage: NotRequired[SavingsPlansCoverageQueryUnionTypeDef]
    savingsPlansUtilization: NotRequired[SavingsPlansUtilizationQueryUnionTypeDef]
    reservationCoverage: NotRequired[ReservationCoverageQueryUnionTypeDef]
    reservationUtilization: NotRequired[ReservationUtilizationQueryUnionTypeDef]

QueryParametersUnionTypeDef = Union[QueryParametersTypeDef, QueryParametersOutputTypeDef]

class WidgetConfigTypeDef(TypedDict):
    queryParameters: QueryParametersUnionTypeDef
    displayConfig: DisplayConfigUnionTypeDef

WidgetConfigUnionTypeDef = Union[WidgetConfigTypeDef, WidgetConfigOutputTypeDef]
WidgetTypeDef = TypedDict(
    "WidgetTypeDef",
    {
        "title": str,
        "configs": Sequence[WidgetConfigUnionTypeDef],
        "id": NotRequired[str],
        "description": NotRequired[str],
        "width": NotRequired[int],
        "height": NotRequired[int],
        "horizontalOffset": NotRequired[int],
    },
)
WidgetUnionTypeDef = Union[WidgetTypeDef, WidgetOutputTypeDef]

class CreateDashboardRequestTypeDef(TypedDict):
    name: str
    widgets: Sequence[WidgetUnionTypeDef]
    description: NotRequired[str]
    resourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class UpdateDashboardRequestTypeDef(TypedDict):
    arn: str
    name: str
    description: NotRequired[str]
    widgets: NotRequired[Sequence[WidgetUnionTypeDef]]
