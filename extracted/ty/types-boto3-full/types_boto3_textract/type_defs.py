"""
Type annotations for textract service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_textract/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_textract.type_defs import AdapterOverviewTypeDef

    data: AdapterOverviewTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    AdapterVersionStatusType,
    AutoUpdateType,
    BlockTypeType,
    ContentClassifierType,
    EntityTypeType,
    ExtractionGranularityTypeType,
    FeatureTypeType,
    JobStatusType,
    OutputTextFormatTypeType,
    PIIEntityTypeType,
    PIIRedactionMaskModeType,
    ProjectStatusType,
    RelationshipTypeType,
    ResourceOwnerType,
    SelectionStatusType,
    SensitiveDataDetectionModeType,
    StateType,
    TextTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AdapterOverviewTypeDef",
    "AdapterTypeDef",
    "AdapterVersionDatasetConfigTypeDef",
    "AdapterVersionEvaluationMetricTypeDef",
    "AdapterVersionOverviewTypeDef",
    "AdaptersConfigTypeDef",
    "AnalyzeDocumentRequestTypeDef",
    "AnalyzeDocumentResponseTypeDef",
    "AnalyzeExpenseRequestTypeDef",
    "AnalyzeExpenseResponseTypeDef",
    "AnalyzeIDDetectionsTypeDef",
    "AnalyzeIDRequestTypeDef",
    "AnalyzeIDResponseTypeDef",
    "BlobTypeDef",
    "BlockTypeDef",
    "BlueprintFilterTypeDef",
    "BlueprintItemTypeDef",
    "BlueprintSummaryTypeDef",
    "BoundingBoxConfigurationTypeDef",
    "BoundingBoxTypeDef",
    "CreateAdapterRequestTypeDef",
    "CreateAdapterResponseTypeDef",
    "CreateAdapterVersionRequestTypeDef",
    "CreateAdapterVersionResponseTypeDef",
    "CreateBlueprintRequestTypeDef",
    "CreateBlueprintResponseTypeDef",
    "CreateBlueprintVersionRequestTypeDef",
    "CreateBlueprintVersionResponseTypeDef",
    "CreateProjectRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "CustomConfigurationOutputTypeDef",
    "CustomConfigurationTypeDef",
    "CustomConfigurationUnionTypeDef",
    "DeleteAdapterRequestTypeDef",
    "DeleteAdapterVersionRequestTypeDef",
    "DeleteBlueprintRequestTypeDef",
    "DeleteProjectRequestTypeDef",
    "DetectDocumentTextRequestTypeDef",
    "DetectDocumentTextResponseTypeDef",
    "DetectedSignatureTypeDef",
    "DocumentGroupTypeDef",
    "DocumentLocationTypeDef",
    "DocumentMetadataTypeDef",
    "DocumentTypeDef",
    "EncryptionConfigurationOutputTypeDef",
    "EncryptionConfigurationTypeDef",
    "EncryptionConfigurationUnionTypeDef",
    "EvaluationMetricTypeDef",
    "EventBridgeConfigurationTypeDef",
    "ExpenseCurrencyTypeDef",
    "ExpenseDetectionTypeDef",
    "ExpenseDocumentTypeDef",
    "ExpenseFieldTypeDef",
    "ExpenseGroupPropertyTypeDef",
    "ExpenseTypeTypeDef",
    "ExtractionConfigurationOutputTypeDef",
    "ExtractionConfigurationTypeDef",
    "ExtractionConfigurationUnionTypeDef",
    "ExtractionGranularityOutputTypeDef",
    "ExtractionGranularityTypeDef",
    "ExtractionTypeDef",
    "FigureCaptionConfigurationTypeDef",
    "GenerativeConfigurationTypeDef",
    "GeometryTypeDef",
    "GetAdapterRequestTypeDef",
    "GetAdapterResponseTypeDef",
    "GetAdapterVersionRequestTypeDef",
    "GetAdapterVersionResponseTypeDef",
    "GetBlueprintRequestTypeDef",
    "GetBlueprintResponseTypeDef",
    "GetDocumentAnalysisRequestTypeDef",
    "GetDocumentAnalysisResponseTypeDef",
    "GetDocumentInsightsRequestTypeDef",
    "GetDocumentInsightsResponseTypeDef",
    "GetDocumentTextDetectionRequestTypeDef",
    "GetDocumentTextDetectionResponseTypeDef",
    "GetExpenseAnalysisRequestTypeDef",
    "GetExpenseAnalysisResponseTypeDef",
    "GetLendingAnalysisRequestTypeDef",
    "GetLendingAnalysisResponseTypeDef",
    "GetLendingAnalysisSummaryRequestTypeDef",
    "GetLendingAnalysisSummaryResponseTypeDef",
    "GetProjectRequestTypeDef",
    "GetProjectResponseTypeDef",
    "HumanLoopActivationOutputTypeDef",
    "HumanLoopConfigTypeDef",
    "HumanLoopDataAttributesTypeDef",
    "IdentityDocumentFieldTypeDef",
    "IdentityDocumentTypeDef",
    "InputConfigurationTypeDef",
    "LendingDetectionTypeDef",
    "LendingDocumentTypeDef",
    "LendingFieldTypeDef",
    "LendingResultTypeDef",
    "LendingSummaryTypeDef",
    "LineItemFieldsTypeDef",
    "LineItemGroupTypeDef",
    "ListAdapterVersionsRequestPaginateTypeDef",
    "ListAdapterVersionsRequestTypeDef",
    "ListAdapterVersionsResponseTypeDef",
    "ListAdaptersRequestPaginateTypeDef",
    "ListAdaptersRequestTypeDef",
    "ListAdaptersResponseTypeDef",
    "ListBlueprintsRequestPaginateTypeDef",
    "ListBlueprintsRequestTypeDef",
    "ListBlueprintsResponseTypeDef",
    "ListProjectsRequestPaginateTypeDef",
    "ListProjectsRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NormalizedValueTypeDef",
    "NotificationChannelTypeDef",
    "NotificationConfigurationTypeDef",
    "OutputAdditionalFileFormatTypeDef",
    "OutputConfigTypeDef",
    "OutputConfigurationTypeDef",
    "OutputFormatOutputTypeDef",
    "OutputFormatTypeDef",
    "OutputTextFormatOutputTypeDef",
    "OutputTextFormatTypeDef",
    "PIIEntitiesConfigurationOutputTypeDef",
    "PIIEntitiesConfigurationTypeDef",
    "PageClassificationTypeDef",
    "PaginatorConfigTypeDef",
    "PointTypeDef",
    "PredictionTypeDef",
    "ProjectFilterTypeDef",
    "ProjectSummaryTypeDef",
    "QueriesConfigTypeDef",
    "QueryOutputTypeDef",
    "QueryTypeDef",
    "QueryUnionTypeDef",
    "RelationshipTypeDef",
    "ResponseMetadataTypeDef",
    "S3ObjectTypeDef",
    "SensitiveDataConfigurationOutputTypeDef",
    "SensitiveDataConfigurationTypeDef",
    "SensitiveDataConfigurationUnionTypeDef",
    "SignatureDetectionTypeDef",
    "SplitDocumentTypeDef",
    "SplitterConfigurationTypeDef",
    "StartDocumentAnalysisRequestTypeDef",
    "StartDocumentAnalysisResponseTypeDef",
    "StartDocumentInsightsRequestTypeDef",
    "StartDocumentInsightsResponseTypeDef",
    "StartDocumentTextDetectionRequestTypeDef",
    "StartDocumentTextDetectionResponseTypeDef",
    "StartExpenseAnalysisRequestTypeDef",
    "StartExpenseAnalysisResponseTypeDef",
    "StartLendingAnalysisRequestTypeDef",
    "StartLendingAnalysisResponseTypeDef",
    "SummarizationConfigurationTypeDef",
    "TagResourceRequestTypeDef",
    "TimestampTypeDef",
    "UndetectedSignatureTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAdapterRequestTypeDef",
    "UpdateAdapterResponseTypeDef",
    "UpdateBlueprintRequestTypeDef",
    "UpdateBlueprintResponseTypeDef",
    "UpdateProjectRequestTypeDef",
    "UpdateProjectResponseTypeDef",
    "WarningTypeDef",
)


class AdapterOverviewTypeDef(TypedDict):
    AdapterId: NotRequired[str]
    AdapterName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    FeatureTypes: NotRequired[list[FeatureTypeType]]


class AdapterTypeDef(TypedDict):
    AdapterId: str
    Version: str
    Pages: NotRequired[Sequence[str]]


class S3ObjectTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[str]


class EvaluationMetricTypeDef(TypedDict):
    F1Score: NotRequired[float]
    Precision: NotRequired[float]
    Recall: NotRequired[float]


class AdapterVersionOverviewTypeDef(TypedDict):
    AdapterId: NotRequired[str]
    AdapterVersion: NotRequired[str]
    CreationTime: NotRequired[datetime]
    FeatureTypes: NotRequired[list[FeatureTypeType]]
    Status: NotRequired[AdapterVersionStatusType]
    StatusMessage: NotRequired[str]


class DocumentMetadataTypeDef(TypedDict):
    Pages: NotRequired[int]


class HumanLoopActivationOutputTypeDef(TypedDict):
    HumanLoopArn: NotRequired[str]
    HumanLoopActivationReasons: NotRequired[list[str]]
    HumanLoopActivationConditionsEvaluationResults: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class NormalizedValueTypeDef(TypedDict):
    Value: NotRequired[str]
    ValueType: NotRequired[Literal["DATE"]]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
QueryOutputTypeDef = TypedDict(
    "QueryOutputTypeDef",
    {
        "Text": str,
        "Alias": NotRequired[str],
        "Pages": NotRequired[list[str]],
    },
)
RelationshipTypeDef = TypedDict(
    "RelationshipTypeDef",
    {
        "Type": NotRequired[RelationshipTypeType],
        "Ids": NotRequired[list[str]],
    },
)


class BlueprintFilterTypeDef(TypedDict):
    BlueprintArn: str
    BlueprintVersion: NotRequired[str]


class BlueprintItemTypeDef(TypedDict):
    BlueprintArn: str
    BlueprintVersion: NotRequired[str]


class BlueprintSummaryTypeDef(TypedDict):
    BlueprintArn: str
    CreationTime: datetime
    BlueprintName: NotRequired[str]
    BlueprintVersion: NotRequired[str]
    ResourceOwner: NotRequired[ResourceOwnerType]
    LastModifiedTime: NotRequired[datetime]


class BoundingBoxConfigurationTypeDef(TypedDict):
    State: StateType


class BoundingBoxTypeDef(TypedDict):
    Width: NotRequired[float]
    Height: NotRequired[float]
    Left: NotRequired[float]
    Top: NotRequired[float]


class CreateAdapterRequestTypeDef(TypedDict):
    AdapterName: str
    FeatureTypes: Sequence[FeatureTypeType]
    ClientRequestToken: NotRequired[str]
    Description: NotRequired[str]
    AutoUpdate: NotRequired[AutoUpdateType]
    Tags: NotRequired[Mapping[str, str]]


class OutputConfigTypeDef(TypedDict):
    S3Bucket: str
    S3Prefix: NotRequired[str]


class CreateBlueprintVersionRequestTypeDef(TypedDict):
    BlueprintArn: str
    ClientRequestToken: NotRequired[str]


class SplitterConfigurationTypeDef(TypedDict):
    State: StateType


class DeleteAdapterRequestTypeDef(TypedDict):
    AdapterId: str


class DeleteAdapterVersionRequestTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str


class DeleteBlueprintRequestTypeDef(TypedDict):
    BlueprintArn: str
    BlueprintVersion: NotRequired[str]


class DeleteProjectRequestTypeDef(TypedDict):
    ProjectArn: str


class DetectedSignatureTypeDef(TypedDict):
    Page: NotRequired[int]


class SplitDocumentTypeDef(TypedDict):
    Index: NotRequired[int]
    Pages: NotRequired[list[int]]


class UndetectedSignatureTypeDef(TypedDict):
    Page: NotRequired[int]


class EncryptionConfigurationOutputTypeDef(TypedDict):
    KmsKeyId: str
    KmsEncryptionContext: NotRequired[dict[str, str]]


class EncryptionConfigurationTypeDef(TypedDict):
    KmsKeyId: str
    KmsEncryptionContext: NotRequired[Mapping[str, str]]


class EventBridgeConfigurationTypeDef(TypedDict):
    State: StateType


class ExpenseCurrencyTypeDef(TypedDict):
    Code: NotRequired[str]
    Confidence: NotRequired[float]


class ExpenseGroupPropertyTypeDef(TypedDict):
    Types: NotRequired[list[str]]
    Id: NotRequired[str]


ExpenseTypeTypeDef = TypedDict(
    "ExpenseTypeTypeDef",
    {
        "Text": NotRequired[str],
        "Confidence": NotRequired[float],
    },
)


class ExtractionGranularityOutputTypeDef(TypedDict):
    Types: NotRequired[list[ExtractionGranularityTypeType]]


class ExtractionGranularityTypeDef(TypedDict):
    Types: NotRequired[Sequence[ExtractionGranularityTypeType]]


class FigureCaptionConfigurationTypeDef(TypedDict):
    State: StateType


class SummarizationConfigurationTypeDef(TypedDict):
    State: StateType


class PointTypeDef(TypedDict):
    X: NotRequired[float]
    Y: NotRequired[float]


class GetAdapterRequestTypeDef(TypedDict):
    AdapterId: str


class GetAdapterVersionRequestTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str


class GetBlueprintRequestTypeDef(TypedDict):
    BlueprintArn: str
    BlueprintVersion: NotRequired[str]


class GetDocumentAnalysisRequestTypeDef(TypedDict):
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class WarningTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    Pages: NotRequired[list[int]]


class GetDocumentInsightsRequestTypeDef(TypedDict):
    JobArn: str


class OutputConfigurationTypeDef(TypedDict):
    S3Uri: str


class GetDocumentTextDetectionRequestTypeDef(TypedDict):
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetExpenseAnalysisRequestTypeDef(TypedDict):
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetLendingAnalysisRequestTypeDef(TypedDict):
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetLendingAnalysisSummaryRequestTypeDef(TypedDict):
    JobId: str


class GetProjectRequestTypeDef(TypedDict):
    ProjectArn: str


class HumanLoopDataAttributesTypeDef(TypedDict):
    ContentClassifiers: NotRequired[Sequence[ContentClassifierType]]


class InputConfigurationTypeDef(TypedDict):
    S3Uri: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ProjectFilterTypeDef(TypedDict):
    ProjectArn: str


class ProjectSummaryTypeDef(TypedDict):
    ProjectArn: str
    CreationTime: datetime
    ProjectName: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceARN: str


class NotificationChannelTypeDef(TypedDict):
    SNSTopicArn: str
    RoleArn: str


class OutputAdditionalFileFormatTypeDef(TypedDict):
    State: StateType


class OutputTextFormatOutputTypeDef(TypedDict):
    Types: NotRequired[list[OutputTextFormatTypeType]]


class OutputTextFormatTypeDef(TypedDict):
    Types: NotRequired[Sequence[OutputTextFormatTypeType]]


class PIIEntitiesConfigurationOutputTypeDef(TypedDict):
    PiiEntityTypes: list[PIIEntityTypeType]
    RedactionMaskMode: PIIRedactionMaskModeType


class PIIEntitiesConfigurationTypeDef(TypedDict):
    PiiEntityTypes: Sequence[PIIEntityTypeType]
    RedactionMaskMode: PIIRedactionMaskModeType


class PredictionTypeDef(TypedDict):
    Value: NotRequired[str]
    Confidence: NotRequired[float]


QueryTypeDef = TypedDict(
    "QueryTypeDef",
    {
        "Text": str,
        "Alias": NotRequired[str],
        "Pages": NotRequired[Sequence[str]],
    },
)


class TagResourceRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateAdapterRequestTypeDef(TypedDict):
    AdapterId: str
    Description: NotRequired[str]
    AdapterName: NotRequired[str]
    AutoUpdate: NotRequired[AutoUpdateType]


class AdaptersConfigTypeDef(TypedDict):
    Adapters: Sequence[AdapterTypeDef]


class AdapterVersionDatasetConfigTypeDef(TypedDict):
    ManifestS3Object: NotRequired[S3ObjectTypeDef]


class DocumentLocationTypeDef(TypedDict):
    S3Object: NotRequired[S3ObjectTypeDef]


class AdapterVersionEvaluationMetricTypeDef(TypedDict):
    Baseline: NotRequired[EvaluationMetricTypeDef]
    AdapterVersion: NotRequired[EvaluationMetricTypeDef]
    FeatureType: NotRequired[FeatureTypeType]


class CreateAdapterResponseTypeDef(TypedDict):
    AdapterId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAdapterVersionResponseTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBlueprintResponseTypeDef(TypedDict):
    BlueprintArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBlueprintVersionResponseTypeDef(TypedDict):
    BlueprintArn: str
    BlueprintVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProjectResponseTypeDef(TypedDict):
    ProjectArn: str
    Status: ProjectStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetAdapterResponseTypeDef(TypedDict):
    AdapterId: str
    AdapterName: str
    CreationTime: datetime
    Description: str
    FeatureTypes: list[FeatureTypeType]
    AutoUpdate: AutoUpdateType
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetBlueprintResponseTypeDef(TypedDict):
    BlueprintArn: str
    BlueprintName: str
    BlueprintVersion: str
    Schema: str
    KmsKeyId: str
    KmsEncryptionContext: dict[str, str]
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListAdapterVersionsResponseTypeDef(TypedDict):
    AdapterVersions: list[AdapterVersionOverviewTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAdaptersResponseTypeDef(TypedDict):
    Adapters: list[AdapterOverviewTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartDocumentAnalysisResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartDocumentInsightsResponseTypeDef(TypedDict):
    JobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartDocumentTextDetectionResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartExpenseAnalysisResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartLendingAnalysisResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAdapterResponseTypeDef(TypedDict):
    AdapterId: str
    AdapterName: str
    CreationTime: datetime
    Description: str
    FeatureTypes: list[FeatureTypeType]
    AutoUpdate: AutoUpdateType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBlueprintResponseTypeDef(TypedDict):
    BlueprintArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProjectResponseTypeDef(TypedDict):
    ProjectArn: str
    Status: ProjectStatusType
    ResponseMetadata: ResponseMetadataTypeDef


AnalyzeIDDetectionsTypeDef = TypedDict(
    "AnalyzeIDDetectionsTypeDef",
    {
        "Text": str,
        "NormalizedValue": NotRequired[NormalizedValueTypeDef],
        "Confidence": NotRequired[float],
    },
)


class DocumentTypeDef(TypedDict):
    Bytes: NotRequired[BlobTypeDef]
    S3Object: NotRequired[S3ObjectTypeDef]


class ListProjectsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    BlueprintFilter: NotRequired[BlueprintFilterTypeDef]


class CustomConfigurationOutputTypeDef(TypedDict):
    Blueprints: list[BlueprintItemTypeDef]
    FallbackBlueprints: NotRequired[list[BlueprintItemTypeDef]]


class CustomConfigurationTypeDef(TypedDict):
    Blueprints: Sequence[BlueprintItemTypeDef]
    FallbackBlueprints: NotRequired[Sequence[BlueprintItemTypeDef]]


class ListBlueprintsResponseTypeDef(TypedDict):
    Blueprints: list[BlueprintSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


DocumentGroupTypeDef = TypedDict(
    "DocumentGroupTypeDef",
    {
        "Type": NotRequired[str],
        "SplitDocuments": NotRequired[list[SplitDocumentTypeDef]],
        "DetectedSignatures": NotRequired[list[DetectedSignatureTypeDef]],
        "UndetectedSignatures": NotRequired[list[UndetectedSignatureTypeDef]],
    },
)
EncryptionConfigurationUnionTypeDef = Union[
    EncryptionConfigurationTypeDef, EncryptionConfigurationOutputTypeDef
]


class NotificationConfigurationTypeDef(TypedDict):
    EventBridgeConfiguration: EventBridgeConfigurationTypeDef


class GenerativeConfigurationTypeDef(TypedDict):
    Summarization: NotRequired[SummarizationConfigurationTypeDef]
    FigureCaption: NotRequired[FigureCaptionConfigurationTypeDef]


class GeometryTypeDef(TypedDict):
    BoundingBox: NotRequired[BoundingBoxTypeDef]
    Polygon: NotRequired[list[PointTypeDef]]
    RotationAngle: NotRequired[float]


class GetDocumentInsightsResponseTypeDef(TypedDict):
    Status: JobStatusType
    OutputConfiguration: OutputConfigurationTypeDef
    ErrorType: str
    ErrorMessage: str
    ResponseMetadata: ResponseMetadataTypeDef


class HumanLoopConfigTypeDef(TypedDict):
    HumanLoopName: str
    FlowDefinitionArn: str
    DataAttributes: NotRequired[HumanLoopDataAttributesTypeDef]


class ListProjectsRequestPaginateTypeDef(TypedDict):
    BlueprintFilter: NotRequired[BlueprintFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAdapterVersionsRequestPaginateTypeDef(TypedDict):
    AdapterId: NotRequired[str]
    AfterCreationTime: NotRequired[TimestampTypeDef]
    BeforeCreationTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAdapterVersionsRequestTypeDef(TypedDict):
    AdapterId: NotRequired[str]
    AfterCreationTime: NotRequired[TimestampTypeDef]
    BeforeCreationTime: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAdaptersRequestPaginateTypeDef(TypedDict):
    AfterCreationTime: NotRequired[TimestampTypeDef]
    BeforeCreationTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAdaptersRequestTypeDef(TypedDict):
    AfterCreationTime: NotRequired[TimestampTypeDef]
    BeforeCreationTime: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListBlueprintsRequestPaginateTypeDef(TypedDict):
    BlueprintArn: NotRequired[str]
    ProjectFilter: NotRequired[ProjectFilterTypeDef]
    ResourceOwner: NotRequired[ResourceOwnerType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBlueprintsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    BlueprintArn: NotRequired[str]
    ProjectFilter: NotRequired[ProjectFilterTypeDef]
    ResourceOwner: NotRequired[ResourceOwnerType]


class ListProjectsResponseTypeDef(TypedDict):
    Projects: list[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class OutputFormatOutputTypeDef(TypedDict):
    AdditionalFileFormat: OutputAdditionalFileFormatTypeDef
    TextFormat: OutputTextFormatOutputTypeDef


class OutputFormatTypeDef(TypedDict):
    AdditionalFileFormat: OutputAdditionalFileFormatTypeDef
    TextFormat: OutputTextFormatTypeDef


class SensitiveDataConfigurationOutputTypeDef(TypedDict):
    DetectionMode: SensitiveDataDetectionModeType
    PiiEntitiesConfiguration: NotRequired[PIIEntitiesConfigurationOutputTypeDef]


class SensitiveDataConfigurationTypeDef(TypedDict):
    DetectionMode: SensitiveDataDetectionModeType
    PiiEntitiesConfiguration: NotRequired[PIIEntitiesConfigurationTypeDef]


class PageClassificationTypeDef(TypedDict):
    PageType: list[PredictionTypeDef]
    PageNumber: list[PredictionTypeDef]


QueryUnionTypeDef = Union[QueryTypeDef, QueryOutputTypeDef]


class CreateAdapterVersionRequestTypeDef(TypedDict):
    AdapterId: str
    DatasetConfig: AdapterVersionDatasetConfigTypeDef
    OutputConfig: OutputConfigTypeDef
    ClientRequestToken: NotRequired[str]
    KMSKeyId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class StartDocumentTextDetectionRequestTypeDef(TypedDict):
    DocumentLocation: DocumentLocationTypeDef
    ClientRequestToken: NotRequired[str]
    JobTag: NotRequired[str]
    NotificationChannel: NotRequired[NotificationChannelTypeDef]
    OutputConfig: NotRequired[OutputConfigTypeDef]
    KMSKeyId: NotRequired[str]


class StartExpenseAnalysisRequestTypeDef(TypedDict):
    DocumentLocation: DocumentLocationTypeDef
    ClientRequestToken: NotRequired[str]
    JobTag: NotRequired[str]
    NotificationChannel: NotRequired[NotificationChannelTypeDef]
    OutputConfig: NotRequired[OutputConfigTypeDef]
    KMSKeyId: NotRequired[str]


class StartLendingAnalysisRequestTypeDef(TypedDict):
    DocumentLocation: DocumentLocationTypeDef
    ClientRequestToken: NotRequired[str]
    JobTag: NotRequired[str]
    NotificationChannel: NotRequired[NotificationChannelTypeDef]
    OutputConfig: NotRequired[OutputConfigTypeDef]
    KMSKeyId: NotRequired[str]


class GetAdapterVersionResponseTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str
    CreationTime: datetime
    FeatureTypes: list[FeatureTypeType]
    Status: AdapterVersionStatusType
    StatusMessage: str
    DatasetConfig: AdapterVersionDatasetConfigTypeDef
    KMSKeyId: str
    OutputConfig: OutputConfigTypeDef
    EvaluationMetrics: list[AdapterVersionEvaluationMetricTypeDef]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


IdentityDocumentFieldTypeDef = TypedDict(
    "IdentityDocumentFieldTypeDef",
    {
        "Type": NotRequired[AnalyzeIDDetectionsTypeDef],
        "ValueDetection": NotRequired[AnalyzeIDDetectionsTypeDef],
    },
)


class AnalyzeExpenseRequestTypeDef(TypedDict):
    Document: DocumentTypeDef


class AnalyzeIDRequestTypeDef(TypedDict):
    DocumentPages: Sequence[DocumentTypeDef]


class DetectDocumentTextRequestTypeDef(TypedDict):
    Document: DocumentTypeDef


CustomConfigurationUnionTypeDef = Union[
    CustomConfigurationTypeDef, CustomConfigurationOutputTypeDef
]


class LendingSummaryTypeDef(TypedDict):
    DocumentGroups: NotRequired[list[DocumentGroupTypeDef]]
    UndetectedDocumentTypes: NotRequired[list[str]]


class CreateBlueprintRequestTypeDef(TypedDict):
    BlueprintName: str
    Schema: str
    ClientRequestToken: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationUnionTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class UpdateBlueprintRequestTypeDef(TypedDict):
    BlueprintArn: str
    Schema: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationUnionTypeDef]


class StartDocumentInsightsRequestTypeDef(TypedDict):
    InputConfiguration: InputConfigurationTypeDef
    OutputConfiguration: OutputConfigurationTypeDef
    ProjectArn: NotRequired[str]
    Blueprints: NotRequired[Sequence[BlueprintItemTypeDef]]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationUnionTypeDef]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]


BlockTypeDef = TypedDict(
    "BlockTypeDef",
    {
        "BlockType": NotRequired[BlockTypeType],
        "Confidence": NotRequired[float],
        "Text": NotRequired[str],
        "TextType": NotRequired[TextTypeType],
        "RowIndex": NotRequired[int],
        "ColumnIndex": NotRequired[int],
        "RowSpan": NotRequired[int],
        "ColumnSpan": NotRequired[int],
        "Geometry": NotRequired[GeometryTypeDef],
        "Id": NotRequired[str],
        "Relationships": NotRequired[list[RelationshipTypeDef]],
        "EntityTypes": NotRequired[list[EntityTypeType]],
        "SelectionStatus": NotRequired[SelectionStatusType],
        "Page": NotRequired[int],
        "Query": NotRequired[QueryOutputTypeDef],
    },
)
ExpenseDetectionTypeDef = TypedDict(
    "ExpenseDetectionTypeDef",
    {
        "Text": NotRequired[str],
        "Geometry": NotRequired[GeometryTypeDef],
        "Confidence": NotRequired[float],
    },
)
LendingDetectionTypeDef = TypedDict(
    "LendingDetectionTypeDef",
    {
        "Text": NotRequired[str],
        "SelectionStatus": NotRequired[SelectionStatusType],
        "Geometry": NotRequired[GeometryTypeDef],
        "Confidence": NotRequired[float],
    },
)


class SignatureDetectionTypeDef(TypedDict):
    Confidence: NotRequired[float]
    Geometry: NotRequired[GeometryTypeDef]


class ExtractionConfigurationOutputTypeDef(TypedDict):
    BoundingBox: BoundingBoxConfigurationTypeDef
    Granularity: ExtractionGranularityOutputTypeDef
    OutputFormat: OutputFormatOutputTypeDef


class ExtractionConfigurationTypeDef(TypedDict):
    BoundingBox: BoundingBoxConfigurationTypeDef
    Granularity: ExtractionGranularityTypeDef
    OutputFormat: OutputFormatTypeDef


SensitiveDataConfigurationUnionTypeDef = Union[
    SensitiveDataConfigurationTypeDef, SensitiveDataConfigurationOutputTypeDef
]


class QueriesConfigTypeDef(TypedDict):
    Queries: Sequence[QueryUnionTypeDef]


class GetLendingAnalysisSummaryResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    Summary: LendingSummaryTypeDef
    Warnings: list[WarningTypeDef]
    StatusMessage: str
    AnalyzeLendingModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class AnalyzeDocumentResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    Blocks: list[BlockTypeDef]
    HumanLoopActivationOutput: HumanLoopActivationOutputTypeDef
    AnalyzeDocumentModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class DetectDocumentTextResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    Blocks: list[BlockTypeDef]
    DetectDocumentTextModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDocumentAnalysisResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    Blocks: list[BlockTypeDef]
    Warnings: list[WarningTypeDef]
    StatusMessage: str
    AnalyzeDocumentModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetDocumentTextDetectionResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    Blocks: list[BlockTypeDef]
    Warnings: list[WarningTypeDef]
    StatusMessage: str
    DetectDocumentTextModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class IdentityDocumentTypeDef(TypedDict):
    DocumentIndex: NotRequired[int]
    IdentityDocumentFields: NotRequired[list[IdentityDocumentFieldTypeDef]]
    Blocks: NotRequired[list[BlockTypeDef]]


ExpenseFieldTypeDef = TypedDict(
    "ExpenseFieldTypeDef",
    {
        "Type": NotRequired[ExpenseTypeTypeDef],
        "LabelDetection": NotRequired[ExpenseDetectionTypeDef],
        "ValueDetection": NotRequired[ExpenseDetectionTypeDef],
        "PageNumber": NotRequired[int],
        "Currency": NotRequired[ExpenseCurrencyTypeDef],
        "GroupProperties": NotRequired[list[ExpenseGroupPropertyTypeDef]],
    },
)
LendingFieldTypeDef = TypedDict(
    "LendingFieldTypeDef",
    {
        "Type": NotRequired[str],
        "KeyDetection": NotRequired[LendingDetectionTypeDef],
        "ValueDetections": NotRequired[list[LendingDetectionTypeDef]],
    },
)


class GetProjectResponseTypeDef(TypedDict):
    ProjectArn: str
    ProjectName: str
    ProjectDescription: str
    Status: ProjectStatusType
    ExtractionConfiguration: ExtractionConfigurationOutputTypeDef
    GenerativeConfiguration: GenerativeConfigurationTypeDef
    CustomConfiguration: CustomConfigurationOutputTypeDef
    SplitterConfiguration: SplitterConfigurationTypeDef
    SensitiveDataConfiguration: SensitiveDataConfigurationOutputTypeDef
    EncryptionConfiguration: EncryptionConfigurationOutputTypeDef
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


ExtractionConfigurationUnionTypeDef = Union[
    ExtractionConfigurationTypeDef, ExtractionConfigurationOutputTypeDef
]


class AnalyzeDocumentRequestTypeDef(TypedDict):
    Document: DocumentTypeDef
    FeatureTypes: Sequence[FeatureTypeType]
    HumanLoopConfig: NotRequired[HumanLoopConfigTypeDef]
    QueriesConfig: NotRequired[QueriesConfigTypeDef]
    AdaptersConfig: NotRequired[AdaptersConfigTypeDef]


class StartDocumentAnalysisRequestTypeDef(TypedDict):
    DocumentLocation: DocumentLocationTypeDef
    FeatureTypes: Sequence[FeatureTypeType]
    ClientRequestToken: NotRequired[str]
    JobTag: NotRequired[str]
    NotificationChannel: NotRequired[NotificationChannelTypeDef]
    OutputConfig: NotRequired[OutputConfigTypeDef]
    KMSKeyId: NotRequired[str]
    QueriesConfig: NotRequired[QueriesConfigTypeDef]
    AdaptersConfig: NotRequired[AdaptersConfigTypeDef]


class AnalyzeIDResponseTypeDef(TypedDict):
    IdentityDocuments: list[IdentityDocumentTypeDef]
    DocumentMetadata: DocumentMetadataTypeDef
    AnalyzeIDModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class LineItemFieldsTypeDef(TypedDict):
    LineItemExpenseFields: NotRequired[list[ExpenseFieldTypeDef]]


class LendingDocumentTypeDef(TypedDict):
    LendingFields: NotRequired[list[LendingFieldTypeDef]]
    SignatureDetections: NotRequired[list[SignatureDetectionTypeDef]]


class CreateProjectRequestTypeDef(TypedDict):
    ProjectName: str
    ExtractionConfiguration: ExtractionConfigurationUnionTypeDef
    ClientRequestToken: NotRequired[str]
    ProjectDescription: NotRequired[str]
    GenerativeConfiguration: NotRequired[GenerativeConfigurationTypeDef]
    CustomConfiguration: NotRequired[CustomConfigurationUnionTypeDef]
    SplitterConfiguration: NotRequired[SplitterConfigurationTypeDef]
    SensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationUnionTypeDef]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationUnionTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class UpdateProjectRequestTypeDef(TypedDict):
    ProjectArn: str
    ProjectDescription: NotRequired[str]
    ExtractionConfiguration: NotRequired[ExtractionConfigurationUnionTypeDef]
    GenerativeConfiguration: NotRequired[GenerativeConfigurationTypeDef]
    CustomConfiguration: NotRequired[CustomConfigurationUnionTypeDef]
    SplitterConfiguration: NotRequired[SplitterConfigurationTypeDef]
    SensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationUnionTypeDef]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationUnionTypeDef]


class LineItemGroupTypeDef(TypedDict):
    LineItemGroupIndex: NotRequired[int]
    LineItems: NotRequired[list[LineItemFieldsTypeDef]]


class ExpenseDocumentTypeDef(TypedDict):
    ExpenseIndex: NotRequired[int]
    SummaryFields: NotRequired[list[ExpenseFieldTypeDef]]
    LineItemGroups: NotRequired[list[LineItemGroupTypeDef]]
    Blocks: NotRequired[list[BlockTypeDef]]


class AnalyzeExpenseResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    ExpenseDocuments: list[ExpenseDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExtractionTypeDef(TypedDict):
    LendingDocument: NotRequired[LendingDocumentTypeDef]
    ExpenseDocument: NotRequired[ExpenseDocumentTypeDef]
    IdentityDocument: NotRequired[IdentityDocumentTypeDef]


class GetExpenseAnalysisResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    ExpenseDocuments: list[ExpenseDocumentTypeDef]
    Warnings: list[WarningTypeDef]
    StatusMessage: str
    AnalyzeExpenseModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LendingResultTypeDef(TypedDict):
    Page: NotRequired[int]
    PageClassification: NotRequired[PageClassificationTypeDef]
    Extractions: NotRequired[list[ExtractionTypeDef]]


class GetLendingAnalysisResponseTypeDef(TypedDict):
    DocumentMetadata: DocumentMetadataTypeDef
    JobStatus: JobStatusType
    Results: list[LendingResultTypeDef]
    Warnings: list[WarningTypeDef]
    StatusMessage: str
    AnalyzeLendingModelVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
