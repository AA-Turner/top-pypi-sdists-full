"""
Type annotations for location service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_location.type_defs import AndroidAppTypeDef

    data: AndroidAppTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    BatchItemErrorCodeType,
    DimensionUnitType,
    DistanceUnitType,
    ForecastedGeofenceEventTypeType,
    IntendedUseType,
    OptimizationModeType,
    PositionFilteringType,
    PricingPlanType,
    RouteMatrixErrorCodeType,
    SpeedUnitType,
    StatusType,
    TravelModeType,
    VehicleWeightUnitType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AndroidAppTypeDef",
    "ApiKeyFilterTypeDef",
    "ApiKeyRestrictionsOutputTypeDef",
    "ApiKeyRestrictionsTypeDef",
    "ApiKeyRestrictionsUnionTypeDef",
    "AppleAppTypeDef",
    "AssociateTrackerConsumerRequestTypeDef",
    "BatchDeleteDevicePositionHistoryErrorTypeDef",
    "BatchDeleteDevicePositionHistoryRequestTypeDef",
    "BatchDeleteDevicePositionHistoryResponseTypeDef",
    "BatchDeleteGeofenceErrorTypeDef",
    "BatchDeleteGeofenceRequestTypeDef",
    "BatchDeleteGeofenceResponseTypeDef",
    "BatchEvaluateGeofencesErrorTypeDef",
    "BatchEvaluateGeofencesRequestTypeDef",
    "BatchEvaluateGeofencesResponseTypeDef",
    "BatchGetDevicePositionErrorTypeDef",
    "BatchGetDevicePositionRequestTypeDef",
    "BatchGetDevicePositionResponseTypeDef",
    "BatchItemErrorTypeDef",
    "BatchPutGeofenceErrorTypeDef",
    "BatchPutGeofenceRequestEntryTypeDef",
    "BatchPutGeofenceRequestTypeDef",
    "BatchPutGeofenceResponseTypeDef",
    "BatchPutGeofenceSuccessTypeDef",
    "BatchUpdateDevicePositionErrorTypeDef",
    "BatchUpdateDevicePositionRequestTypeDef",
    "BatchUpdateDevicePositionResponseTypeDef",
    "BlobTypeDef",
    "CalculateRouteCarModeOptionsTypeDef",
    "CalculateRouteMatrixRequestTypeDef",
    "CalculateRouteMatrixResponseTypeDef",
    "CalculateRouteMatrixSummaryTypeDef",
    "CalculateRouteRequestTypeDef",
    "CalculateRouteResponseTypeDef",
    "CalculateRouteSummaryTypeDef",
    "CalculateRouteTruckModeOptionsTypeDef",
    "CellSignalsTypeDef",
    "CircleOutputTypeDef",
    "CircleTypeDef",
    "CircleUnionTypeDef",
    "CreateGeofenceCollectionRequestTypeDef",
    "CreateGeofenceCollectionResponseTypeDef",
    "CreateKeyRequestTypeDef",
    "CreateKeyResponseTypeDef",
    "CreateMapRequestTypeDef",
    "CreateMapResponseTypeDef",
    "CreatePlaceIndexRequestTypeDef",
    "CreatePlaceIndexResponseTypeDef",
    "CreateRouteCalculatorRequestTypeDef",
    "CreateRouteCalculatorResponseTypeDef",
    "CreateTrackerRequestTypeDef",
    "CreateTrackerResponseTypeDef",
    "DataSourceConfigurationTypeDef",
    "DeleteGeofenceCollectionRequestTypeDef",
    "DeleteKeyRequestTypeDef",
    "DeleteMapRequestTypeDef",
    "DeletePlaceIndexRequestTypeDef",
    "DeleteRouteCalculatorRequestTypeDef",
    "DeleteTrackerRequestTypeDef",
    "DescribeGeofenceCollectionRequestTypeDef",
    "DescribeGeofenceCollectionResponseTypeDef",
    "DescribeKeyRequestTypeDef",
    "DescribeKeyResponseTypeDef",
    "DescribeMapRequestTypeDef",
    "DescribeMapResponseTypeDef",
    "DescribePlaceIndexRequestTypeDef",
    "DescribePlaceIndexResponseTypeDef",
    "DescribeRouteCalculatorRequestTypeDef",
    "DescribeRouteCalculatorResponseTypeDef",
    "DescribeTrackerRequestTypeDef",
    "DescribeTrackerResponseTypeDef",
    "DevicePositionTypeDef",
    "DevicePositionUpdateTypeDef",
    "DeviceStateTypeDef",
    "DisassociateTrackerConsumerRequestTypeDef",
    "ForecastGeofenceEventsDeviceStateTypeDef",
    "ForecastGeofenceEventsRequestPaginateTypeDef",
    "ForecastGeofenceEventsRequestTypeDef",
    "ForecastGeofenceEventsResponseTypeDef",
    "ForecastedEventTypeDef",
    "GeofenceGeometryOutputTypeDef",
    "GeofenceGeometryTypeDef",
    "GeofenceGeometryUnionTypeDef",
    "GetDevicePositionHistoryRequestPaginateTypeDef",
    "GetDevicePositionHistoryRequestTypeDef",
    "GetDevicePositionHistoryResponseTypeDef",
    "GetDevicePositionRequestTypeDef",
    "GetDevicePositionResponseTypeDef",
    "GetGeofenceRequestTypeDef",
    "GetGeofenceResponseTypeDef",
    "GetMapGlyphsRequestTypeDef",
    "GetMapGlyphsResponseTypeDef",
    "GetMapSpritesRequestTypeDef",
    "GetMapSpritesResponseTypeDef",
    "GetMapStyleDescriptorRequestTypeDef",
    "GetMapStyleDescriptorResponseTypeDef",
    "GetMapTileRequestTypeDef",
    "GetMapTileResponseTypeDef",
    "GetPlaceRequestTypeDef",
    "GetPlaceResponseTypeDef",
    "InferredStateTypeDef",
    "LegGeometryTypeDef",
    "LegTypeDef",
    "ListDevicePositionsRequestPaginateTypeDef",
    "ListDevicePositionsRequestTypeDef",
    "ListDevicePositionsResponseEntryTypeDef",
    "ListDevicePositionsResponseTypeDef",
    "ListGeofenceCollectionsRequestPaginateTypeDef",
    "ListGeofenceCollectionsRequestTypeDef",
    "ListGeofenceCollectionsResponseEntryTypeDef",
    "ListGeofenceCollectionsResponseTypeDef",
    "ListGeofenceResponseEntryTypeDef",
    "ListGeofencesRequestPaginateTypeDef",
    "ListGeofencesRequestTypeDef",
    "ListGeofencesResponseTypeDef",
    "ListKeysRequestPaginateTypeDef",
    "ListKeysRequestTypeDef",
    "ListKeysResponseEntryTypeDef",
    "ListKeysResponseTypeDef",
    "ListMapsRequestPaginateTypeDef",
    "ListMapsRequestTypeDef",
    "ListMapsResponseEntryTypeDef",
    "ListMapsResponseTypeDef",
    "ListPlaceIndexesRequestPaginateTypeDef",
    "ListPlaceIndexesRequestTypeDef",
    "ListPlaceIndexesResponseEntryTypeDef",
    "ListPlaceIndexesResponseTypeDef",
    "ListRouteCalculatorsRequestPaginateTypeDef",
    "ListRouteCalculatorsRequestTypeDef",
    "ListRouteCalculatorsResponseEntryTypeDef",
    "ListRouteCalculatorsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTrackerConsumersRequestPaginateTypeDef",
    "ListTrackerConsumersRequestTypeDef",
    "ListTrackerConsumersResponseTypeDef",
    "ListTrackersRequestPaginateTypeDef",
    "ListTrackersRequestTypeDef",
    "ListTrackersResponseEntryTypeDef",
    "ListTrackersResponseTypeDef",
    "LteCellDetailsTypeDef",
    "LteLocalIdTypeDef",
    "LteNetworkMeasurementsTypeDef",
    "MapConfigurationOutputTypeDef",
    "MapConfigurationTypeDef",
    "MapConfigurationUnionTypeDef",
    "MapConfigurationUpdateTypeDef",
    "PaginatorConfigTypeDef",
    "PlaceGeometryTypeDef",
    "PlaceTypeDef",
    "PositionalAccuracyTypeDef",
    "PutGeofenceRequestTypeDef",
    "PutGeofenceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RouteMatrixEntryErrorTypeDef",
    "RouteMatrixEntryTypeDef",
    "SearchForPositionResultTypeDef",
    "SearchForSuggestionsResultTypeDef",
    "SearchForTextResultTypeDef",
    "SearchPlaceIndexForPositionRequestTypeDef",
    "SearchPlaceIndexForPositionResponseTypeDef",
    "SearchPlaceIndexForPositionSummaryTypeDef",
    "SearchPlaceIndexForSuggestionsRequestTypeDef",
    "SearchPlaceIndexForSuggestionsResponseTypeDef",
    "SearchPlaceIndexForSuggestionsSummaryTypeDef",
    "SearchPlaceIndexForTextRequestTypeDef",
    "SearchPlaceIndexForTextResponseTypeDef",
    "SearchPlaceIndexForTextSummaryTypeDef",
    "StepTypeDef",
    "TagResourceRequestTypeDef",
    "TimeZoneTypeDef",
    "TimestampTypeDef",
    "TrackingFilterGeometryTypeDef",
    "TruckDimensionsTypeDef",
    "TruckWeightTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateGeofenceCollectionRequestTypeDef",
    "UpdateGeofenceCollectionResponseTypeDef",
    "UpdateKeyRequestTypeDef",
    "UpdateKeyResponseTypeDef",
    "UpdateMapRequestTypeDef",
    "UpdateMapResponseTypeDef",
    "UpdatePlaceIndexRequestTypeDef",
    "UpdatePlaceIndexResponseTypeDef",
    "UpdateRouteCalculatorRequestTypeDef",
    "UpdateRouteCalculatorResponseTypeDef",
    "UpdateTrackerRequestTypeDef",
    "UpdateTrackerResponseTypeDef",
    "VerifyDevicePositionRequestTypeDef",
    "VerifyDevicePositionResponseTypeDef",
    "WiFiAccessPointTypeDef",
)

class AndroidAppTypeDef(TypedDict):
    Package: str
    CertificateFingerprint: str

class ApiKeyFilterTypeDef(TypedDict):
    KeyStatus: NotRequired[StatusType]

class AppleAppTypeDef(TypedDict):
    BundleId: str

class AssociateTrackerConsumerRequestTypeDef(TypedDict):
    TrackerName: str
    ConsumerArn: str

class BatchItemErrorTypeDef(TypedDict):
    Code: NotRequired[BatchItemErrorCodeType]
    Message: NotRequired[str]

class BatchDeleteDevicePositionHistoryRequestTypeDef(TypedDict):
    TrackerName: str
    DeviceIds: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchDeleteGeofenceRequestTypeDef(TypedDict):
    CollectionName: str
    GeofenceIds: Sequence[str]

class BatchGetDevicePositionRequestTypeDef(TypedDict):
    TrackerName: str
    DeviceIds: Sequence[str]

class BatchPutGeofenceSuccessTypeDef(TypedDict):
    GeofenceId: str
    CreateTime: datetime
    UpdateTime: datetime

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CalculateRouteCarModeOptionsTypeDef(TypedDict):
    AvoidFerries: NotRequired[bool]
    AvoidTolls: NotRequired[bool]

TimestampTypeDef = Union[datetime, str]

class CalculateRouteMatrixSummaryTypeDef(TypedDict):
    DataSource: str
    RouteCount: int
    ErrorCount: int
    DistanceUnit: DistanceUnitType

class CalculateRouteSummaryTypeDef(TypedDict):
    RouteBBox: list[float]
    DataSource: str
    Distance: float
    DurationSeconds: float
    DistanceUnit: DistanceUnitType

class TruckDimensionsTypeDef(TypedDict):
    Length: NotRequired[float]
    Height: NotRequired[float]
    Width: NotRequired[float]
    Unit: NotRequired[DimensionUnitType]

class TruckWeightTypeDef(TypedDict):
    Total: NotRequired[float]
    Unit: NotRequired[VehicleWeightUnitType]

class CircleOutputTypeDef(TypedDict):
    Center: list[float]
    Radius: float

class CircleTypeDef(TypedDict):
    Center: Sequence[float]
    Radius: float

class CreateGeofenceCollectionRequestTypeDef(TypedDict):
    CollectionName: str
    PricingPlan: NotRequired[PricingPlanType]
    PricingPlanDataSource: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    KmsKeyId: NotRequired[str]

class DataSourceConfigurationTypeDef(TypedDict):
    IntendedUse: NotRequired[IntendedUseType]

class CreateRouteCalculatorRequestTypeDef(TypedDict):
    CalculatorName: str
    DataSource: str
    PricingPlan: NotRequired[PricingPlanType]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class CreateTrackerRequestTypeDef(TypedDict):
    TrackerName: str
    PricingPlan: NotRequired[PricingPlanType]
    KmsKeyId: NotRequired[str]
    PricingPlanDataSource: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    PositionFiltering: NotRequired[PositionFilteringType]
    EventBridgeEnabled: NotRequired[bool]
    KmsKeyEnableGeospatialQueries: NotRequired[bool]

class DeleteGeofenceCollectionRequestTypeDef(TypedDict):
    CollectionName: str

class DeleteKeyRequestTypeDef(TypedDict):
    KeyName: str
    ForceDelete: NotRequired[bool]

class DeleteMapRequestTypeDef(TypedDict):
    MapName: str

class DeletePlaceIndexRequestTypeDef(TypedDict):
    IndexName: str

class DeleteRouteCalculatorRequestTypeDef(TypedDict):
    CalculatorName: str

class DeleteTrackerRequestTypeDef(TypedDict):
    TrackerName: str

class DescribeGeofenceCollectionRequestTypeDef(TypedDict):
    CollectionName: str

class DescribeKeyRequestTypeDef(TypedDict):
    KeyName: str

class DescribeMapRequestTypeDef(TypedDict):
    MapName: str

class MapConfigurationOutputTypeDef(TypedDict):
    Style: str
    PoliticalView: NotRequired[str]
    CustomLayers: NotRequired[list[str]]

class DescribePlaceIndexRequestTypeDef(TypedDict):
    IndexName: str

class DescribeRouteCalculatorRequestTypeDef(TypedDict):
    CalculatorName: str

class DescribeTrackerRequestTypeDef(TypedDict):
    TrackerName: str

class PositionalAccuracyTypeDef(TypedDict):
    Horizontal: float

class WiFiAccessPointTypeDef(TypedDict):
    MacAddress: str
    Rss: int

class DisassociateTrackerConsumerRequestTypeDef(TypedDict):
    TrackerName: str
    ConsumerArn: str

class ForecastGeofenceEventsDeviceStateTypeDef(TypedDict):
    Position: Sequence[float]
    Speed: NotRequired[float]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ForecastedEventTypeDef(TypedDict):
    EventId: str
    GeofenceId: str
    IsDeviceInGeofence: bool
    NearestDistance: float
    EventType: ForecastedGeofenceEventTypeType
    ForecastedBreachTime: NotRequired[datetime]
    GeofenceProperties: NotRequired[dict[str, str]]

class GetDevicePositionRequestTypeDef(TypedDict):
    TrackerName: str
    DeviceId: str

class GetGeofenceRequestTypeDef(TypedDict):
    CollectionName: str
    GeofenceId: str

class GetMapGlyphsRequestTypeDef(TypedDict):
    MapName: str
    FontStack: str
    FontUnicodeRange: str
    Key: NotRequired[str]

class GetMapSpritesRequestTypeDef(TypedDict):
    MapName: str
    FileName: str
    Key: NotRequired[str]

class GetMapStyleDescriptorRequestTypeDef(TypedDict):
    MapName: str
    Key: NotRequired[str]

class GetMapTileRequestTypeDef(TypedDict):
    MapName: str
    Z: str
    X: str
    Y: str
    Key: NotRequired[str]

class GetPlaceRequestTypeDef(TypedDict):
    IndexName: str
    PlaceId: str
    Language: NotRequired[str]
    Key: NotRequired[str]

class LegGeometryTypeDef(TypedDict):
    LineString: NotRequired[list[list[float]]]

class StepTypeDef(TypedDict):
    StartPosition: list[float]
    EndPosition: list[float]
    Distance: float
    DurationSeconds: float
    GeometryOffset: NotRequired[int]

class TrackingFilterGeometryTypeDef(TypedDict):
    Polygon: NotRequired[Sequence[Sequence[Sequence[float]]]]

class ListGeofenceCollectionsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListGeofenceCollectionsResponseEntryTypeDef(TypedDict):
    CollectionName: str
    Description: str
    CreateTime: datetime
    UpdateTime: datetime
    PricingPlan: NotRequired[PricingPlanType]
    PricingPlanDataSource: NotRequired[str]

class ListGeofencesRequestTypeDef(TypedDict):
    CollectionName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListMapsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListMapsResponseEntryTypeDef(TypedDict):
    MapName: str
    Description: str
    DataSource: str
    CreateTime: datetime
    UpdateTime: datetime
    PricingPlan: NotRequired[PricingPlanType]

class ListPlaceIndexesRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListPlaceIndexesResponseEntryTypeDef(TypedDict):
    IndexName: str
    Description: str
    DataSource: str
    CreateTime: datetime
    UpdateTime: datetime
    PricingPlan: NotRequired[PricingPlanType]

class ListRouteCalculatorsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRouteCalculatorsResponseEntryTypeDef(TypedDict):
    CalculatorName: str
    Description: str
    DataSource: str
    CreateTime: datetime
    UpdateTime: datetime
    PricingPlan: NotRequired[PricingPlanType]

class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str

class ListTrackerConsumersRequestTypeDef(TypedDict):
    TrackerName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTrackersRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTrackersResponseEntryTypeDef(TypedDict):
    TrackerName: str
    Description: str
    CreateTime: datetime
    UpdateTime: datetime
    PricingPlan: NotRequired[PricingPlanType]
    PricingPlanDataSource: NotRequired[str]

class LteLocalIdTypeDef(TypedDict):
    Earfcn: int
    Pci: int

class LteNetworkMeasurementsTypeDef(TypedDict):
    Earfcn: int
    CellId: int
    Pci: int
    Rsrp: NotRequired[int]
    Rsrq: NotRequired[float]

class MapConfigurationTypeDef(TypedDict):
    Style: str
    PoliticalView: NotRequired[str]
    CustomLayers: NotRequired[Sequence[str]]

class MapConfigurationUpdateTypeDef(TypedDict):
    PoliticalView: NotRequired[str]
    CustomLayers: NotRequired[Sequence[str]]

class PlaceGeometryTypeDef(TypedDict):
    Point: NotRequired[list[float]]

class TimeZoneTypeDef(TypedDict):
    Name: str
    Offset: NotRequired[int]

class RouteMatrixEntryErrorTypeDef(TypedDict):
    Code: RouteMatrixErrorCodeType
    Message: NotRequired[str]

SearchForSuggestionsResultTypeDef = TypedDict(
    "SearchForSuggestionsResultTypeDef",
    {
        "Text": str,
        "PlaceId": NotRequired[str],
        "Categories": NotRequired[list[str]],
        "SupplementalCategories": NotRequired[list[str]],
    },
)

class SearchPlaceIndexForPositionRequestTypeDef(TypedDict):
    IndexName: str
    Position: Sequence[float]
    MaxResults: NotRequired[int]
    Language: NotRequired[str]
    Key: NotRequired[str]

class SearchPlaceIndexForPositionSummaryTypeDef(TypedDict):
    Position: list[float]
    DataSource: str
    MaxResults: NotRequired[int]
    Language: NotRequired[str]

SearchPlaceIndexForSuggestionsRequestTypeDef = TypedDict(
    "SearchPlaceIndexForSuggestionsRequestTypeDef",
    {
        "IndexName": str,
        "Text": str,
        "BiasPosition": NotRequired[Sequence[float]],
        "FilterBBox": NotRequired[Sequence[float]],
        "FilterCountries": NotRequired[Sequence[str]],
        "MaxResults": NotRequired[int],
        "Language": NotRequired[str],
        "FilterCategories": NotRequired[Sequence[str]],
        "Key": NotRequired[str],
    },
)
SearchPlaceIndexForSuggestionsSummaryTypeDef = TypedDict(
    "SearchPlaceIndexForSuggestionsSummaryTypeDef",
    {
        "Text": str,
        "DataSource": str,
        "BiasPosition": NotRequired[list[float]],
        "FilterBBox": NotRequired[list[float]],
        "FilterCountries": NotRequired[list[str]],
        "MaxResults": NotRequired[int],
        "Language": NotRequired[str],
        "FilterCategories": NotRequired[list[str]],
    },
)
SearchPlaceIndexForTextRequestTypeDef = TypedDict(
    "SearchPlaceIndexForTextRequestTypeDef",
    {
        "IndexName": str,
        "Text": str,
        "BiasPosition": NotRequired[Sequence[float]],
        "FilterBBox": NotRequired[Sequence[float]],
        "FilterCountries": NotRequired[Sequence[str]],
        "MaxResults": NotRequired[int],
        "Language": NotRequired[str],
        "FilterCategories": NotRequired[Sequence[str]],
        "Key": NotRequired[str],
    },
)
SearchPlaceIndexForTextSummaryTypeDef = TypedDict(
    "SearchPlaceIndexForTextSummaryTypeDef",
    {
        "Text": str,
        "DataSource": str,
        "BiasPosition": NotRequired[list[float]],
        "FilterBBox": NotRequired[list[float]],
        "FilterCountries": NotRequired[list[str]],
        "MaxResults": NotRequired[int],
        "ResultBBox": NotRequired[list[float]],
        "Language": NotRequired[str],
        "FilterCategories": NotRequired[list[str]],
    },
)

class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateGeofenceCollectionRequestTypeDef(TypedDict):
    CollectionName: str
    PricingPlan: NotRequired[PricingPlanType]
    PricingPlanDataSource: NotRequired[str]
    Description: NotRequired[str]

class UpdateRouteCalculatorRequestTypeDef(TypedDict):
    CalculatorName: str
    PricingPlan: NotRequired[PricingPlanType]
    Description: NotRequired[str]

class UpdateTrackerRequestTypeDef(TypedDict):
    TrackerName: str
    PricingPlan: NotRequired[PricingPlanType]
    PricingPlanDataSource: NotRequired[str]
    Description: NotRequired[str]
    PositionFiltering: NotRequired[PositionFilteringType]
    EventBridgeEnabled: NotRequired[bool]
    KmsKeyEnableGeospatialQueries: NotRequired[bool]

class ListKeysRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filter: NotRequired[ApiKeyFilterTypeDef]

class ApiKeyRestrictionsOutputTypeDef(TypedDict):
    AllowActions: list[str]
    AllowResources: list[str]
    AllowReferers: NotRequired[list[str]]
    AllowAndroidApps: NotRequired[list[AndroidAppTypeDef]]
    AllowAppleApps: NotRequired[list[AppleAppTypeDef]]

class ApiKeyRestrictionsTypeDef(TypedDict):
    AllowActions: Sequence[str]
    AllowResources: Sequence[str]
    AllowReferers: NotRequired[Sequence[str]]
    AllowAndroidApps: NotRequired[Sequence[AndroidAppTypeDef]]
    AllowAppleApps: NotRequired[Sequence[AppleAppTypeDef]]

class BatchDeleteDevicePositionHistoryErrorTypeDef(TypedDict):
    DeviceId: str
    Error: BatchItemErrorTypeDef

class BatchDeleteGeofenceErrorTypeDef(TypedDict):
    GeofenceId: str
    Error: BatchItemErrorTypeDef

class BatchEvaluateGeofencesErrorTypeDef(TypedDict):
    DeviceId: str
    SampleTime: datetime
    Error: BatchItemErrorTypeDef

class BatchGetDevicePositionErrorTypeDef(TypedDict):
    DeviceId: str
    Error: BatchItemErrorTypeDef

class BatchPutGeofenceErrorTypeDef(TypedDict):
    GeofenceId: str
    Error: BatchItemErrorTypeDef

class BatchUpdateDevicePositionErrorTypeDef(TypedDict):
    DeviceId: str
    SampleTime: datetime
    Error: BatchItemErrorTypeDef

class CreateGeofenceCollectionResponseTypeDef(TypedDict):
    CollectionName: str
    CollectionArn: str
    CreateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateKeyResponseTypeDef(TypedDict):
    Key: str
    KeyArn: str
    KeyName: str
    CreateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMapResponseTypeDef(TypedDict):
    MapName: str
    MapArn: str
    CreateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePlaceIndexResponseTypeDef(TypedDict):
    IndexName: str
    IndexArn: str
    CreateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRouteCalculatorResponseTypeDef(TypedDict):
    CalculatorName: str
    CalculatorArn: str
    CreateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTrackerResponseTypeDef(TypedDict):
    TrackerName: str
    TrackerArn: str
    CreateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeGeofenceCollectionResponseTypeDef(TypedDict):
    CollectionName: str
    CollectionArn: str
    Description: str
    PricingPlan: PricingPlanType
    PricingPlanDataSource: str
    KmsKeyId: str
    Tags: dict[str, str]
    CreateTime: datetime
    UpdateTime: datetime
    GeofenceCount: int
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRouteCalculatorResponseTypeDef(TypedDict):
    CalculatorName: str
    CalculatorArn: str
    PricingPlan: PricingPlanType
    Description: str
    CreateTime: datetime
    UpdateTime: datetime
    DataSource: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTrackerResponseTypeDef(TypedDict):
    TrackerName: str
    TrackerArn: str
    Description: str
    PricingPlan: PricingPlanType
    PricingPlanDataSource: str
    Tags: dict[str, str]
    CreateTime: datetime
    UpdateTime: datetime
    KmsKeyId: str
    PositionFiltering: PositionFilteringType
    EventBridgeEnabled: bool
    KmsKeyEnableGeospatialQueries: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GetMapGlyphsResponseTypeDef(TypedDict):
    Blob: StreamingBody
    ContentType: str
    CacheControl: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetMapSpritesResponseTypeDef(TypedDict):
    Blob: StreamingBody
    ContentType: str
    CacheControl: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetMapStyleDescriptorResponseTypeDef(TypedDict):
    Blob: StreamingBody
    ContentType: str
    CacheControl: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetMapTileResponseTypeDef(TypedDict):
    Blob: StreamingBody
    ContentType: str
    CacheControl: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTrackerConsumersResponseTypeDef(TypedDict):
    ConsumerArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutGeofenceResponseTypeDef(TypedDict):
    GeofenceId: str
    CreateTime: datetime
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGeofenceCollectionResponseTypeDef(TypedDict):
    CollectionName: str
    CollectionArn: str
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKeyResponseTypeDef(TypedDict):
    KeyArn: str
    KeyName: str
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMapResponseTypeDef(TypedDict):
    MapName: str
    MapArn: str
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePlaceIndexResponseTypeDef(TypedDict):
    IndexName: str
    IndexArn: str
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRouteCalculatorResponseTypeDef(TypedDict):
    CalculatorName: str
    CalculatorArn: str
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTrackerResponseTypeDef(TypedDict):
    TrackerName: str
    TrackerArn: str
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetDevicePositionHistoryRequestTypeDef(TypedDict):
    TrackerName: str
    DeviceId: str
    NextToken: NotRequired[str]
    StartTimeInclusive: NotRequired[TimestampTypeDef]
    EndTimeExclusive: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]

class CalculateRouteTruckModeOptionsTypeDef(TypedDict):
    AvoidFerries: NotRequired[bool]
    AvoidTolls: NotRequired[bool]
    Dimensions: NotRequired[TruckDimensionsTypeDef]
    Weight: NotRequired[TruckWeightTypeDef]

class GeofenceGeometryOutputTypeDef(TypedDict):
    Polygon: NotRequired[list[list[list[float]]]]
    Circle: NotRequired[CircleOutputTypeDef]
    Geobuf: NotRequired[bytes]
    MultiPolygon: NotRequired[list[list[list[list[float]]]]]

CircleUnionTypeDef = Union[CircleTypeDef, CircleOutputTypeDef]

class CreatePlaceIndexRequestTypeDef(TypedDict):
    IndexName: str
    DataSource: str
    PricingPlan: NotRequired[PricingPlanType]
    Description: NotRequired[str]
    DataSourceConfiguration: NotRequired[DataSourceConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]

class DescribePlaceIndexResponseTypeDef(TypedDict):
    IndexName: str
    IndexArn: str
    PricingPlan: PricingPlanType
    Description: str
    CreateTime: datetime
    UpdateTime: datetime
    DataSource: str
    DataSourceConfiguration: DataSourceConfigurationTypeDef
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePlaceIndexRequestTypeDef(TypedDict):
    IndexName: str
    PricingPlan: NotRequired[PricingPlanType]
    Description: NotRequired[str]
    DataSourceConfiguration: NotRequired[DataSourceConfigurationTypeDef]

class DescribeMapResponseTypeDef(TypedDict):
    MapName: str
    MapArn: str
    PricingPlan: PricingPlanType
    DataSource: str
    Configuration: MapConfigurationOutputTypeDef
    Description: str
    Tags: dict[str, str]
    CreateTime: datetime
    UpdateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DevicePositionTypeDef(TypedDict):
    SampleTime: datetime
    ReceivedTime: datetime
    Position: list[float]
    DeviceId: NotRequired[str]
    Accuracy: NotRequired[PositionalAccuracyTypeDef]
    PositionProperties: NotRequired[dict[str, str]]

class DevicePositionUpdateTypeDef(TypedDict):
    DeviceId: str
    SampleTime: TimestampTypeDef
    Position: Sequence[float]
    Accuracy: NotRequired[PositionalAccuracyTypeDef]
    PositionProperties: NotRequired[Mapping[str, str]]

class GetDevicePositionResponseTypeDef(TypedDict):
    DeviceId: str
    SampleTime: datetime
    ReceivedTime: datetime
    Position: list[float]
    Accuracy: PositionalAccuracyTypeDef
    PositionProperties: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class InferredStateTypeDef(TypedDict):
    ProxyDetected: bool
    Position: NotRequired[list[float]]
    Accuracy: NotRequired[PositionalAccuracyTypeDef]
    DeviationDistance: NotRequired[float]

class ListDevicePositionsResponseEntryTypeDef(TypedDict):
    DeviceId: str
    SampleTime: datetime
    Position: list[float]
    Accuracy: NotRequired[PositionalAccuracyTypeDef]
    PositionProperties: NotRequired[dict[str, str]]

class ForecastGeofenceEventsRequestTypeDef(TypedDict):
    CollectionName: str
    DeviceState: ForecastGeofenceEventsDeviceStateTypeDef
    TimeHorizonMinutes: NotRequired[float]
    DistanceUnit: NotRequired[DistanceUnitType]
    SpeedUnit: NotRequired[SpeedUnitType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ForecastGeofenceEventsRequestPaginateTypeDef(TypedDict):
    CollectionName: str
    DeviceState: ForecastGeofenceEventsDeviceStateTypeDef
    TimeHorizonMinutes: NotRequired[float]
    DistanceUnit: NotRequired[DistanceUnitType]
    SpeedUnit: NotRequired[SpeedUnitType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetDevicePositionHistoryRequestPaginateTypeDef(TypedDict):
    TrackerName: str
    DeviceId: str
    StartTimeInclusive: NotRequired[TimestampTypeDef]
    EndTimeExclusive: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGeofenceCollectionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGeofencesRequestPaginateTypeDef(TypedDict):
    CollectionName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListKeysRequestPaginateTypeDef(TypedDict):
    Filter: NotRequired[ApiKeyFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMapsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPlaceIndexesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRouteCalculatorsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrackerConsumersRequestPaginateTypeDef(TypedDict):
    TrackerName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrackersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ForecastGeofenceEventsResponseTypeDef(TypedDict):
    ForecastedEvents: list[ForecastedEventTypeDef]
    DistanceUnit: DistanceUnitType
    SpeedUnit: SpeedUnitType
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class LegTypeDef(TypedDict):
    StartPosition: list[float]
    EndPosition: list[float]
    Distance: float
    DurationSeconds: float
    Steps: list[StepTypeDef]
    Geometry: NotRequired[LegGeometryTypeDef]

class ListDevicePositionsRequestPaginateTypeDef(TypedDict):
    TrackerName: str
    FilterGeometry: NotRequired[TrackingFilterGeometryTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDevicePositionsRequestTypeDef(TypedDict):
    TrackerName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    FilterGeometry: NotRequired[TrackingFilterGeometryTypeDef]

class ListGeofenceCollectionsResponseTypeDef(TypedDict):
    Entries: list[ListGeofenceCollectionsResponseEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListMapsResponseTypeDef(TypedDict):
    Entries: list[ListMapsResponseEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPlaceIndexesResponseTypeDef(TypedDict):
    Entries: list[ListPlaceIndexesResponseEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRouteCalculatorsResponseTypeDef(TypedDict):
    Entries: list[ListRouteCalculatorsResponseEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTrackersResponseTypeDef(TypedDict):
    Entries: list[ListTrackersResponseEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class LteCellDetailsTypeDef(TypedDict):
    CellId: int
    Mcc: int
    Mnc: int
    LocalId: NotRequired[LteLocalIdTypeDef]
    NetworkMeasurements: NotRequired[Sequence[LteNetworkMeasurementsTypeDef]]
    TimingAdvance: NotRequired[int]
    NrCapable: NotRequired[bool]
    Rsrp: NotRequired[int]
    Rsrq: NotRequired[float]
    Tac: NotRequired[int]

MapConfigurationUnionTypeDef = Union[MapConfigurationTypeDef, MapConfigurationOutputTypeDef]

class UpdateMapRequestTypeDef(TypedDict):
    MapName: str
    PricingPlan: NotRequired[PricingPlanType]
    Description: NotRequired[str]
    ConfigurationUpdate: NotRequired[MapConfigurationUpdateTypeDef]

class PlaceTypeDef(TypedDict):
    Geometry: PlaceGeometryTypeDef
    Label: NotRequired[str]
    AddressNumber: NotRequired[str]
    Street: NotRequired[str]
    Neighborhood: NotRequired[str]
    Municipality: NotRequired[str]
    SubRegion: NotRequired[str]
    Region: NotRequired[str]
    Country: NotRequired[str]
    PostalCode: NotRequired[str]
    Interpolated: NotRequired[bool]
    TimeZone: NotRequired[TimeZoneTypeDef]
    UnitType: NotRequired[str]
    UnitNumber: NotRequired[str]
    Categories: NotRequired[list[str]]
    SupplementalCategories: NotRequired[list[str]]
    SubMunicipality: NotRequired[str]

class RouteMatrixEntryTypeDef(TypedDict):
    Distance: NotRequired[float]
    DurationSeconds: NotRequired[float]
    Error: NotRequired[RouteMatrixEntryErrorTypeDef]

class SearchPlaceIndexForSuggestionsResponseTypeDef(TypedDict):
    Summary: SearchPlaceIndexForSuggestionsSummaryTypeDef
    Results: list[SearchForSuggestionsResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeKeyResponseTypeDef(TypedDict):
    Key: str
    KeyArn: str
    KeyName: str
    Restrictions: ApiKeyRestrictionsOutputTypeDef
    CreateTime: datetime
    ExpireTime: datetime
    UpdateTime: datetime
    Description: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListKeysResponseEntryTypeDef(TypedDict):
    KeyName: str
    ExpireTime: datetime
    Restrictions: ApiKeyRestrictionsOutputTypeDef
    CreateTime: datetime
    UpdateTime: datetime
    Description: NotRequired[str]

ApiKeyRestrictionsUnionTypeDef = Union[ApiKeyRestrictionsTypeDef, ApiKeyRestrictionsOutputTypeDef]

class BatchDeleteDevicePositionHistoryResponseTypeDef(TypedDict):
    Errors: list[BatchDeleteDevicePositionHistoryErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteGeofenceResponseTypeDef(TypedDict):
    Errors: list[BatchDeleteGeofenceErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchEvaluateGeofencesResponseTypeDef(TypedDict):
    Errors: list[BatchEvaluateGeofencesErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchPutGeofenceResponseTypeDef(TypedDict):
    Successes: list[BatchPutGeofenceSuccessTypeDef]
    Errors: list[BatchPutGeofenceErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdateDevicePositionResponseTypeDef(TypedDict):
    Errors: list[BatchUpdateDevicePositionErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CalculateRouteMatrixRequestTypeDef(TypedDict):
    CalculatorName: str
    DeparturePositions: Sequence[Sequence[float]]
    DestinationPositions: Sequence[Sequence[float]]
    TravelMode: NotRequired[TravelModeType]
    DepartureTime: NotRequired[TimestampTypeDef]
    DepartNow: NotRequired[bool]
    DistanceUnit: NotRequired[DistanceUnitType]
    CarModeOptions: NotRequired[CalculateRouteCarModeOptionsTypeDef]
    TruckModeOptions: NotRequired[CalculateRouteTruckModeOptionsTypeDef]
    Key: NotRequired[str]

class CalculateRouteRequestTypeDef(TypedDict):
    CalculatorName: str
    DeparturePosition: Sequence[float]
    DestinationPosition: Sequence[float]
    WaypointPositions: NotRequired[Sequence[Sequence[float]]]
    TravelMode: NotRequired[TravelModeType]
    DepartureTime: NotRequired[TimestampTypeDef]
    DepartNow: NotRequired[bool]
    DistanceUnit: NotRequired[DistanceUnitType]
    IncludeLegGeometry: NotRequired[bool]
    CarModeOptions: NotRequired[CalculateRouteCarModeOptionsTypeDef]
    TruckModeOptions: NotRequired[CalculateRouteTruckModeOptionsTypeDef]
    ArrivalTime: NotRequired[TimestampTypeDef]
    OptimizeFor: NotRequired[OptimizationModeType]
    Key: NotRequired[str]

class GetGeofenceResponseTypeDef(TypedDict):
    GeofenceId: str
    Geometry: GeofenceGeometryOutputTypeDef
    Status: str
    CreateTime: datetime
    UpdateTime: datetime
    GeofenceProperties: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListGeofenceResponseEntryTypeDef(TypedDict):
    GeofenceId: str
    Geometry: GeofenceGeometryOutputTypeDef
    Status: str
    CreateTime: datetime
    UpdateTime: datetime
    GeofenceProperties: NotRequired[dict[str, str]]

class GeofenceGeometryTypeDef(TypedDict):
    Polygon: NotRequired[Sequence[Sequence[Sequence[float]]]]
    Circle: NotRequired[CircleUnionTypeDef]
    Geobuf: NotRequired[BlobTypeDef]
    MultiPolygon: NotRequired[Sequence[Sequence[Sequence[Sequence[float]]]]]

class BatchGetDevicePositionResponseTypeDef(TypedDict):
    Errors: list[BatchGetDevicePositionErrorTypeDef]
    DevicePositions: list[DevicePositionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDevicePositionHistoryResponseTypeDef(TypedDict):
    DevicePositions: list[DevicePositionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BatchEvaluateGeofencesRequestTypeDef(TypedDict):
    CollectionName: str
    DevicePositionUpdates: Sequence[DevicePositionUpdateTypeDef]

class BatchUpdateDevicePositionRequestTypeDef(TypedDict):
    TrackerName: str
    Updates: Sequence[DevicePositionUpdateTypeDef]

class VerifyDevicePositionResponseTypeDef(TypedDict):
    InferredState: InferredStateTypeDef
    DeviceId: str
    SampleTime: datetime
    ReceivedTime: datetime
    DistanceUnit: DistanceUnitType
    ResponseMetadata: ResponseMetadataTypeDef

class ListDevicePositionsResponseTypeDef(TypedDict):
    Entries: list[ListDevicePositionsResponseEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CalculateRouteResponseTypeDef(TypedDict):
    Legs: list[LegTypeDef]
    Summary: CalculateRouteSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CellSignalsTypeDef(TypedDict):
    LteCellDetails: Sequence[LteCellDetailsTypeDef]

class CreateMapRequestTypeDef(TypedDict):
    MapName: str
    Configuration: MapConfigurationUnionTypeDef
    PricingPlan: NotRequired[PricingPlanType]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class GetPlaceResponseTypeDef(TypedDict):
    Place: PlaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SearchForPositionResultTypeDef(TypedDict):
    Place: PlaceTypeDef
    Distance: float
    PlaceId: NotRequired[str]

class SearchForTextResultTypeDef(TypedDict):
    Place: PlaceTypeDef
    Distance: NotRequired[float]
    Relevance: NotRequired[float]
    PlaceId: NotRequired[str]

class CalculateRouteMatrixResponseTypeDef(TypedDict):
    RouteMatrix: list[list[RouteMatrixEntryTypeDef]]
    SnappedDeparturePositions: list[list[float]]
    SnappedDestinationPositions: list[list[float]]
    Summary: CalculateRouteMatrixSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListKeysResponseTypeDef(TypedDict):
    Entries: list[ListKeysResponseEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateKeyRequestTypeDef(TypedDict):
    KeyName: str
    Restrictions: ApiKeyRestrictionsUnionTypeDef
    Description: NotRequired[str]
    ExpireTime: NotRequired[TimestampTypeDef]
    NoExpiry: NotRequired[bool]
    Tags: NotRequired[Mapping[str, str]]

class UpdateKeyRequestTypeDef(TypedDict):
    KeyName: str
    Description: NotRequired[str]
    ExpireTime: NotRequired[TimestampTypeDef]
    NoExpiry: NotRequired[bool]
    ForceUpdate: NotRequired[bool]
    Restrictions: NotRequired[ApiKeyRestrictionsUnionTypeDef]

class ListGeofencesResponseTypeDef(TypedDict):
    Entries: list[ListGeofenceResponseEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

GeofenceGeometryUnionTypeDef = Union[GeofenceGeometryTypeDef, GeofenceGeometryOutputTypeDef]

class DeviceStateTypeDef(TypedDict):
    DeviceId: str
    SampleTime: TimestampTypeDef
    Position: Sequence[float]
    Accuracy: NotRequired[PositionalAccuracyTypeDef]
    Ipv4Address: NotRequired[str]
    WiFiAccessPoints: NotRequired[Sequence[WiFiAccessPointTypeDef]]
    CellSignals: NotRequired[CellSignalsTypeDef]

class SearchPlaceIndexForPositionResponseTypeDef(TypedDict):
    Summary: SearchPlaceIndexForPositionSummaryTypeDef
    Results: list[SearchForPositionResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SearchPlaceIndexForTextResponseTypeDef(TypedDict):
    Summary: SearchPlaceIndexForTextSummaryTypeDef
    Results: list[SearchForTextResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchPutGeofenceRequestEntryTypeDef(TypedDict):
    GeofenceId: str
    Geometry: GeofenceGeometryUnionTypeDef
    GeofenceProperties: NotRequired[Mapping[str, str]]

class PutGeofenceRequestTypeDef(TypedDict):
    CollectionName: str
    GeofenceId: str
    Geometry: GeofenceGeometryUnionTypeDef
    GeofenceProperties: NotRequired[Mapping[str, str]]

class VerifyDevicePositionRequestTypeDef(TypedDict):
    TrackerName: str
    DeviceState: DeviceStateTypeDef
    DistanceUnit: NotRequired[DistanceUnitType]

class BatchPutGeofenceRequestTypeDef(TypedDict):
    CollectionName: str
    Entries: Sequence[BatchPutGeofenceRequestEntryTypeDef]
