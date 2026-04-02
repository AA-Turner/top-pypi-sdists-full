"""
Type annotations for textract service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_textract/type_defs/)

Copyright 2025 Vlad Emelianov

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
    FeatureTypeType,
    JobStatusType,
    RelationshipTypeType,
    SelectionStatusType,
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
    "BoundingBoxTypeDef",
    "CreateAdapterRequestTypeDef",
    "CreateAdapterResponseTypeDef",
    "CreateAdapterVersionRequestTypeDef",
    "CreateAdapterVersionResponseTypeDef",
    "DeleteAdapterRequestTypeDef",
    "DeleteAdapterVersionRequestTypeDef",
    "DetectDocumentTextRequestTypeDef",
    "DetectDocumentTextResponseTypeDef",
    "DetectedSignatureTypeDef",
    "DocumentGroupTypeDef",
    "DocumentLocationTypeDef",
    "DocumentMetadataTypeDef",
    "DocumentTypeDef",
    "EvaluationMetricTypeDef",
    "ExpenseCurrencyTypeDef",
    "ExpenseDetectionTypeDef",
    "ExpenseDocumentTypeDef",
    "ExpenseFieldTypeDef",
    "ExpenseGroupPropertyTypeDef",
    "ExpenseTypeTypeDef",
    "ExtractionTypeDef",
    "GeometryTypeDef",
    "GetAdapterRequestTypeDef",
    "GetAdapterResponseTypeDef",
    "GetAdapterVersionRequestTypeDef",
    "GetAdapterVersionResponseTypeDef",
    "GetDocumentAnalysisRequestTypeDef",
    "GetDocumentAnalysisResponseTypeDef",
    "GetDocumentTextDetectionRequestTypeDef",
    "GetDocumentTextDetectionResponseTypeDef",
    "GetExpenseAnalysisRequestTypeDef",
    "GetExpenseAnalysisResponseTypeDef",
    "GetLendingAnalysisRequestTypeDef",
    "GetLendingAnalysisResponseTypeDef",
    "GetLendingAnalysisSummaryRequestTypeDef",
    "GetLendingAnalysisSummaryResponseTypeDef",
    "HumanLoopActivationOutputTypeDef",
    "HumanLoopConfigTypeDef",
    "HumanLoopDataAttributesTypeDef",
    "IdentityDocumentFieldTypeDef",
    "IdentityDocumentTypeDef",
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
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NormalizedValueTypeDef",
    "NotificationChannelTypeDef",
    "OutputConfigTypeDef",
    "PageClassificationTypeDef",
    "PaginatorConfigTypeDef",
    "PointTypeDef",
    "PredictionTypeDef",
    "QueriesConfigTypeDef",
    "QueryOutputTypeDef",
    "QueryTypeDef",
    "QueryUnionTypeDef",
    "RelationshipTypeDef",
    "ResponseMetadataTypeDef",
    "S3ObjectTypeDef",
    "SignatureDetectionTypeDef",
    "SplitDocumentTypeDef",
    "StartDocumentAnalysisRequestTypeDef",
    "StartDocumentAnalysisResponseTypeDef",
    "StartDocumentTextDetectionRequestTypeDef",
    "StartDocumentTextDetectionResponseTypeDef",
    "StartExpenseAnalysisRequestTypeDef",
    "StartExpenseAnalysisResponseTypeDef",
    "StartLendingAnalysisRequestTypeDef",
    "StartLendingAnalysisResponseTypeDef",
    "TagResourceRequestTypeDef",
    "TimestampTypeDef",
    "UndetectedSignatureTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAdapterRequestTypeDef",
    "UpdateAdapterResponseTypeDef",
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

class DeleteAdapterRequestTypeDef(TypedDict):
    AdapterId: str

class DeleteAdapterVersionRequestTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str

class DetectedSignatureTypeDef(TypedDict):
    Page: NotRequired[int]

class SplitDocumentTypeDef(TypedDict):
    Index: NotRequired[int]
    Pages: NotRequired[list[int]]

class UndetectedSignatureTypeDef(TypedDict):
    Page: NotRequired[int]

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

class PointTypeDef(TypedDict):
    X: NotRequired[float]
    Y: NotRequired[float]

class GetAdapterRequestTypeDef(TypedDict):
    AdapterId: str

class GetAdapterVersionRequestTypeDef(TypedDict):
    AdapterId: str
    AdapterVersion: str

class GetDocumentAnalysisRequestTypeDef(TypedDict):
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class WarningTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    Pages: NotRequired[list[int]]

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

class HumanLoopDataAttributesTypeDef(TypedDict):
    ContentClassifiers: NotRequired[Sequence[ContentClassifierType]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceARN: str

class NotificationChannelTypeDef(TypedDict):
    SNSTopicArn: str
    RoleArn: str

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

class GetAdapterResponseTypeDef(TypedDict):
    AdapterId: str
    AdapterName: str
    CreationTime: datetime
    Description: str
    FeatureTypes: list[FeatureTypeType]
    AutoUpdate: AutoUpdateType
    Tags: dict[str, str]
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

DocumentGroupTypeDef = TypedDict(
    "DocumentGroupTypeDef",
    {
        "Type": NotRequired[str],
        "SplitDocuments": NotRequired[list[SplitDocumentTypeDef]],
        "DetectedSignatures": NotRequired[list[DetectedSignatureTypeDef]],
        "UndetectedSignatures": NotRequired[list[UndetectedSignatureTypeDef]],
    },
)

class GeometryTypeDef(TypedDict):
    BoundingBox: NotRequired[BoundingBoxTypeDef]
    Polygon: NotRequired[list[PointTypeDef]]
    RotationAngle: NotRequired[float]

class HumanLoopConfigTypeDef(TypedDict):
    HumanLoopName: str
    FlowDefinitionArn: str
    DataAttributes: NotRequired[HumanLoopDataAttributesTypeDef]

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

class LendingSummaryTypeDef(TypedDict):
    DocumentGroups: NotRequired[list[DocumentGroupTypeDef]]
    UndetectedDocumentTypes: NotRequired[list[str]]

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
