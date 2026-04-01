"""
Type annotations for sustainability service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_sustainability.type_defs import DimensionEntryTypeDef

    data: DimensionEntryTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import DimensionType, EmissionsTypeType, TimeGranularityType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "DimensionEntryTypeDef",
    "EmissionsTypeDef",
    "EstimatedCarbonEmissionsTypeDef",
    "FilterExpressionTypeDef",
    "GetEstimatedCarbonEmissionsDimensionValuesRequestPaginateTypeDef",
    "GetEstimatedCarbonEmissionsDimensionValuesRequestTypeDef",
    "GetEstimatedCarbonEmissionsDimensionValuesResponseTypeDef",
    "GetEstimatedCarbonEmissionsRequestPaginateTypeDef",
    "GetEstimatedCarbonEmissionsRequestTypeDef",
    "GetEstimatedCarbonEmissionsResponseTypeDef",
    "GranularityConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TimePeriodOutputTypeDef",
    "TimePeriodTypeDef",
    "TimePeriodUnionTypeDef",
    "TimestampTypeDef",
)

class DimensionEntryTypeDef(TypedDict):
    Dimension: DimensionType
    Value: str

class EmissionsTypeDef(TypedDict):
    Value: float
    Unit: Literal["MTCO2e"]

class TimePeriodOutputTypeDef(TypedDict):
    Start: datetime
    End: datetime

class FilterExpressionTypeDef(TypedDict):
    Dimensions: NotRequired[Mapping[DimensionType, Sequence[str]]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GranularityConfigurationTypeDef(TypedDict):
    FiscalYearStartMonth: NotRequired[int]

TimestampTypeDef = Union[datetime, str]

class EstimatedCarbonEmissionsTypeDef(TypedDict):
    TimePeriod: TimePeriodOutputTypeDef
    DimensionsValues: dict[DimensionType, str]
    ModelVersion: str
    EmissionsValues: dict[EmissionsTypeType, EmissionsTypeDef]

class GetEstimatedCarbonEmissionsDimensionValuesResponseTypeDef(TypedDict):
    Results: list[DimensionEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TimePeriodTypeDef(TypedDict):
    Start: TimestampTypeDef
    End: TimestampTypeDef

class GetEstimatedCarbonEmissionsResponseTypeDef(TypedDict):
    Results: list[EstimatedCarbonEmissionsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

TimePeriodUnionTypeDef = Union[TimePeriodTypeDef, TimePeriodOutputTypeDef]

class GetEstimatedCarbonEmissionsDimensionValuesRequestPaginateTypeDef(TypedDict):
    TimePeriod: TimePeriodUnionTypeDef
    Dimensions: Sequence[DimensionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetEstimatedCarbonEmissionsDimensionValuesRequestTypeDef(TypedDict):
    TimePeriod: TimePeriodUnionTypeDef
    Dimensions: Sequence[DimensionType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class GetEstimatedCarbonEmissionsRequestPaginateTypeDef(TypedDict):
    TimePeriod: TimePeriodUnionTypeDef
    GroupBy: NotRequired[Sequence[DimensionType]]
    FilterBy: NotRequired[FilterExpressionTypeDef]
    EmissionsTypes: NotRequired[Sequence[EmissionsTypeType]]
    Granularity: NotRequired[TimeGranularityType]
    GranularityConfiguration: NotRequired[GranularityConfigurationTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetEstimatedCarbonEmissionsRequestTypeDef(TypedDict):
    TimePeriod: TimePeriodUnionTypeDef
    GroupBy: NotRequired[Sequence[DimensionType]]
    FilterBy: NotRequired[FilterExpressionTypeDef]
    EmissionsTypes: NotRequired[Sequence[EmissionsTypeType]]
    Granularity: NotRequired[TimeGranularityType]
    GranularityConfiguration: NotRequired[GranularityConfigurationTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
