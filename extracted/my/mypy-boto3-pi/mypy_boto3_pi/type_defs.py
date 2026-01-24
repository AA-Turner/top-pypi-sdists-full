"""
Type annotations for pi service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_pi.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    AnalysisStatusType,
    ContextTypeType,
    DetailStatusType,
    FeatureStatusType,
    FineGrainedActionType,
    PeriodAlignmentType,
    ServiceTypeType,
    SeverityType,
    TextFormatType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AnalysisReportSummaryTypeDef",
    "AnalysisReportTypeDef",
    "CreatePerformanceAnalysisReportRequestTypeDef",
    "CreatePerformanceAnalysisReportResponseTypeDef",
    "DataPointTypeDef",
    "DataTypeDef",
    "DeletePerformanceAnalysisReportRequestTypeDef",
    "DescribeDimensionKeysRequestTypeDef",
    "DescribeDimensionKeysResponseTypeDef",
    "DimensionDetailTypeDef",
    "DimensionGroupDetailTypeDef",
    "DimensionGroupTypeDef",
    "DimensionKeyDescriptionTypeDef",
    "DimensionKeyDetailTypeDef",
    "FeatureMetadataTypeDef",
    "GetDimensionKeyDetailsRequestTypeDef",
    "GetDimensionKeyDetailsResponseTypeDef",
    "GetPerformanceAnalysisReportRequestTypeDef",
    "GetPerformanceAnalysisReportResponseTypeDef",
    "GetResourceMetadataRequestTypeDef",
    "GetResourceMetadataResponseTypeDef",
    "GetResourceMetricsRequestTypeDef",
    "GetResourceMetricsResponseTypeDef",
    "InsightTypeDef",
    "ListAvailableResourceDimensionsRequestTypeDef",
    "ListAvailableResourceDimensionsResponseTypeDef",
    "ListAvailableResourceMetricsRequestTypeDef",
    "ListAvailableResourceMetricsResponseTypeDef",
    "ListPerformanceAnalysisReportsRequestTypeDef",
    "ListPerformanceAnalysisReportsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricDimensionGroupsTypeDef",
    "MetricKeyDataPointsTypeDef",
    "MetricQueryTypeDef",
    "PerformanceInsightsMetricTypeDef",
    "RecommendationTypeDef",
    "ResponseMetadataTypeDef",
    "ResponsePartitionKeyTypeDef",
    "ResponseResourceMetricKeyTypeDef",
    "ResponseResourceMetricTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
)


class TagTypeDef(TypedDict):
    Key: str
    Value: str


TimestampTypeDef = Union[datetime, str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DataPointTypeDef(TypedDict):
    Timestamp: datetime
    Value: float


class PerformanceInsightsMetricTypeDef(TypedDict):
    Metric: NotRequired[str]
    DisplayName: NotRequired[str]
    Dimensions: NotRequired[dict[str, str]]
    Filter: NotRequired[dict[str, str]]
    Value: NotRequired[float]


class DeletePerformanceAnalysisReportRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str
    AnalysisReportId: str


class DimensionGroupTypeDef(TypedDict):
    Group: str
    Dimensions: NotRequired[Sequence[str]]
    Limit: NotRequired[int]


class DimensionKeyDescriptionTypeDef(TypedDict):
    Dimensions: NotRequired[dict[str, str]]
    Total: NotRequired[float]
    AdditionalMetrics: NotRequired[dict[str, float]]
    Partitions: NotRequired[list[float]]


class ResponsePartitionKeyTypeDef(TypedDict):
    Dimensions: dict[str, str]


class DimensionDetailTypeDef(TypedDict):
    Identifier: NotRequired[str]


class DimensionKeyDetailTypeDef(TypedDict):
    Value: NotRequired[str]
    Dimension: NotRequired[str]
    Status: NotRequired[DetailStatusType]


class FeatureMetadataTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]


class GetDimensionKeyDetailsRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str
    Group: str
    GroupIdentifier: str
    RequestedDimensions: NotRequired[Sequence[str]]


class GetPerformanceAnalysisReportRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str
    AnalysisReportId: str
    TextFormat: NotRequired[TextFormatType]
    AcceptLanguage: NotRequired[Literal["EN_US"]]


class GetResourceMetadataRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str


class RecommendationTypeDef(TypedDict):
    RecommendationId: NotRequired[str]
    RecommendationDescription: NotRequired[str]


class ListAvailableResourceDimensionsRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str
    Metrics: Sequence[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AuthorizedActions: NotRequired[Sequence[FineGrainedActionType]]


class ListAvailableResourceMetricsRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str
    MetricTypes: Sequence[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ResponseResourceMetricTypeDef(TypedDict):
    Metric: NotRequired[str]
    Description: NotRequired[str]
    Unit: NotRequired[str]


class ListPerformanceAnalysisReportsRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ListTags: NotRequired[bool]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    ResourceARN: str


class ResponseResourceMetricKeyTypeDef(TypedDict):
    Metric: str
    Dimensions: NotRequired[dict[str, str]]


class UntagResourceRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    ResourceARN: str
    TagKeys: Sequence[str]


class AnalysisReportSummaryTypeDef(TypedDict):
    AnalysisReportId: NotRequired[str]
    CreateTime: NotRequired[datetime]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Status: NotRequired[AnalysisStatusType]
    Tags: NotRequired[list[TagTypeDef]]


class TagResourceRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreatePerformanceAnalysisReportRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreatePerformanceAnalysisReportResponseTypeDef(TypedDict):
    AnalysisReportId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DataTypeDef(TypedDict):
    PerformanceInsightsMetric: NotRequired[PerformanceInsightsMetricTypeDef]


class DescribeDimensionKeysRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    Metric: str
    GroupBy: DimensionGroupTypeDef
    PeriodInSeconds: NotRequired[int]
    AdditionalMetrics: NotRequired[Sequence[str]]
    PartitionBy: NotRequired[DimensionGroupTypeDef]
    Filter: NotRequired[Mapping[str, str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MetricQueryTypeDef(TypedDict):
    Metric: str
    GroupBy: NotRequired[DimensionGroupTypeDef]
    Filter: NotRequired[Mapping[str, str]]


class DescribeDimensionKeysResponseTypeDef(TypedDict):
    AlignedStartTime: datetime
    AlignedEndTime: datetime
    PartitionKeys: list[ResponsePartitionKeyTypeDef]
    Keys: list[DimensionKeyDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DimensionGroupDetailTypeDef(TypedDict):
    Group: NotRequired[str]
    Dimensions: NotRequired[list[DimensionDetailTypeDef]]


class GetDimensionKeyDetailsResponseTypeDef(TypedDict):
    Dimensions: list[DimensionKeyDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourceMetadataResponseTypeDef(TypedDict):
    Identifier: str
    Features: dict[str, FeatureMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAvailableResourceMetricsResponseTypeDef(TypedDict):
    Metrics: list[ResponseResourceMetricTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MetricKeyDataPointsTypeDef(TypedDict):
    Key: NotRequired[ResponseResourceMetricKeyTypeDef]
    DataPoints: NotRequired[list[DataPointTypeDef]]


class ListPerformanceAnalysisReportsResponseTypeDef(TypedDict):
    AnalysisReports: list[AnalysisReportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InsightTypeDef(TypedDict):
    InsightId: str
    InsightType: NotRequired[str]
    Context: NotRequired[ContextTypeType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Severity: NotRequired[SeverityType]
    SupportingInsights: NotRequired[list[dict[str, Any]]]
    Description: NotRequired[str]
    Recommendations: NotRequired[list[RecommendationTypeDef]]
    InsightData: NotRequired[list[DataTypeDef]]
    BaselineData: NotRequired[list[DataTypeDef]]


class GetResourceMetricsRequestTypeDef(TypedDict):
    ServiceType: ServiceTypeType
    Identifier: str
    MetricQueries: Sequence[MetricQueryTypeDef]
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    PeriodInSeconds: NotRequired[int]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    PeriodAlignment: NotRequired[PeriodAlignmentType]


class MetricDimensionGroupsTypeDef(TypedDict):
    Metric: NotRequired[str]
    Groups: NotRequired[list[DimensionGroupDetailTypeDef]]


class GetResourceMetricsResponseTypeDef(TypedDict):
    AlignedStartTime: datetime
    AlignedEndTime: datetime
    Identifier: str
    MetricList: list[MetricKeyDataPointsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AnalysisReportTypeDef(TypedDict):
    AnalysisReportId: str
    Identifier: NotRequired[str]
    ServiceType: NotRequired[ServiceTypeType]
    CreateTime: NotRequired[datetime]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Status: NotRequired[AnalysisStatusType]
    Insights: NotRequired[list[InsightTypeDef]]


class ListAvailableResourceDimensionsResponseTypeDef(TypedDict):
    MetricDimensions: list[MetricDimensionGroupsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetPerformanceAnalysisReportResponseTypeDef(TypedDict):
    AnalysisReport: AnalysisReportTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
