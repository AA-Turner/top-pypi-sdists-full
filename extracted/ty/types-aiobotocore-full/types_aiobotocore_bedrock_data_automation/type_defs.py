"""
Type annotations for bedrock-data-automation service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_bedrock_data_automation.type_defs import AudioLanguageConfigurationOutputTypeDef

    data: AudioLanguageConfigurationOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AudioExtractionCategoryTypeType,
    AudioGenerativeOutputLanguageType,
    AudioStandardGenerativeFieldTypeType,
    BlueprintOptimizationJobStatusType,
    BlueprintStageFilterType,
    BlueprintStageType,
    DataAutomationLibraryStatusType,
    DataAutomationProjectStageFilterType,
    DataAutomationProjectStageType,
    DataAutomationProjectStatusType,
    DataAutomationProjectTypeType,
    DesiredModalityType,
    DocumentExtractionGranularityTypeType,
    DocumentOutputTextFormatTypeType,
    ImageExtractionCategoryTypeType,
    ImageStandardGenerativeFieldTypeType,
    LanguageType,
    LibraryIngestionJobOperationTypeType,
    LibraryIngestionJobStatusType,
    PIIEntityTypeType,
    PIIRedactionMaskModeType,
    ResourceOwnerType,
    SensitiveDataDetectionModeType,
    SensitiveDataDetectionScopeTypeType,
    StateType,
    TypeType,
    VideoExtractionCategoryTypeType,
    VideoStandardGenerativeFieldTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AudioExtractionCategoryOutputTypeDef",
    "AudioExtractionCategoryTypeConfigurationTypeDef",
    "AudioExtractionCategoryTypeDef",
    "AudioLanguageConfigurationOutputTypeDef",
    "AudioLanguageConfigurationTypeDef",
    "AudioOverrideConfigurationOutputTypeDef",
    "AudioOverrideConfigurationTypeDef",
    "AudioStandardExtractionOutputTypeDef",
    "AudioStandardExtractionTypeDef",
    "AudioStandardGenerativeFieldOutputTypeDef",
    "AudioStandardGenerativeFieldTypeDef",
    "AudioStandardOutputConfigurationOutputTypeDef",
    "AudioStandardOutputConfigurationTypeDef",
    "BlueprintFilterTypeDef",
    "BlueprintItemTypeDef",
    "BlueprintOptimizationObjectTypeDef",
    "BlueprintOptimizationOutputConfigurationTypeDef",
    "BlueprintOptimizationSampleTypeDef",
    "BlueprintSummaryTypeDef",
    "BlueprintTypeDef",
    "ChannelLabelingConfigurationTypeDef",
    "CopyBlueprintStageRequestTypeDef",
    "CreateBlueprintRequestTypeDef",
    "CreateBlueprintResponseTypeDef",
    "CreateBlueprintVersionRequestTypeDef",
    "CreateBlueprintVersionResponseTypeDef",
    "CreateDataAutomationLibraryRequestTypeDef",
    "CreateDataAutomationLibraryResponseTypeDef",
    "CreateDataAutomationProjectRequestTypeDef",
    "CreateDataAutomationProjectResponseTypeDef",
    "CustomOutputConfigurationOutputTypeDef",
    "CustomOutputConfigurationTypeDef",
    "CustomOutputConfigurationUnionTypeDef",
    "DataAutomationLibraryConfigurationOutputTypeDef",
    "DataAutomationLibraryConfigurationTypeDef",
    "DataAutomationLibraryConfigurationUnionTypeDef",
    "DataAutomationLibraryEntitySummaryTypeDef",
    "DataAutomationLibraryFilterTypeDef",
    "DataAutomationLibraryIngestionJobSummaryTypeDef",
    "DataAutomationLibraryIngestionJobTypeDef",
    "DataAutomationLibraryItemTypeDef",
    "DataAutomationLibrarySummaryTypeDef",
    "DataAutomationLibraryTypeDef",
    "DataAutomationProjectFilterTypeDef",
    "DataAutomationProjectSummaryTypeDef",
    "DataAutomationProjectTypeDef",
    "DeleteBlueprintRequestTypeDef",
    "DeleteDataAutomationLibraryRequestTypeDef",
    "DeleteDataAutomationLibraryResponseTypeDef",
    "DeleteDataAutomationProjectRequestTypeDef",
    "DeleteDataAutomationProjectResponseTypeDef",
    "DeleteEntitiesInfoTypeDef",
    "DocumentBoundingBoxTypeDef",
    "DocumentCustomOutputConfigurationOutputTypeDef",
    "DocumentCustomOutputConfigurationTypeDef",
    "DocumentExtractionGranularityOutputTypeDef",
    "DocumentExtractionGranularityTypeDef",
    "DocumentOutputAdditionalFileFormatTypeDef",
    "DocumentOutputFormatOutputTypeDef",
    "DocumentOutputFormatTypeDef",
    "DocumentOutputTextFormatOutputTypeDef",
    "DocumentOutputTextFormatTypeDef",
    "DocumentOverrideConfigurationOutputTypeDef",
    "DocumentOverrideConfigurationTypeDef",
    "DocumentStandardExtractionOutputTypeDef",
    "DocumentStandardExtractionTypeDef",
    "DocumentStandardGenerativeFieldTypeDef",
    "DocumentStandardOutputConfigurationOutputTypeDef",
    "DocumentStandardOutputConfigurationTypeDef",
    "EncryptionConfigurationTypeDef",
    "EntityDetailsTypeDef",
    "EntityTypeInfoTypeDef",
    "EventBridgeConfigurationTypeDef",
    "GetBlueprintOptimizationStatusRequestTypeDef",
    "GetBlueprintOptimizationStatusResponseTypeDef",
    "GetBlueprintRequestTypeDef",
    "GetBlueprintResponseTypeDef",
    "GetDataAutomationLibraryEntityRequestTypeDef",
    "GetDataAutomationLibraryEntityResponseTypeDef",
    "GetDataAutomationLibraryIngestionJobRequestTypeDef",
    "GetDataAutomationLibraryIngestionJobResponseTypeDef",
    "GetDataAutomationLibraryRequestTypeDef",
    "GetDataAutomationLibraryResponseTypeDef",
    "GetDataAutomationProjectRequestTypeDef",
    "GetDataAutomationProjectResponseTypeDef",
    "ImageBoundingBoxTypeDef",
    "ImageExtractionCategoryOutputTypeDef",
    "ImageExtractionCategoryTypeDef",
    "ImageOverrideConfigurationOutputTypeDef",
    "ImageOverrideConfigurationTypeDef",
    "ImageStandardExtractionOutputTypeDef",
    "ImageStandardExtractionTypeDef",
    "ImageStandardGenerativeFieldOutputTypeDef",
    "ImageStandardGenerativeFieldTypeDef",
    "ImageStandardOutputConfigurationOutputTypeDef",
    "ImageStandardOutputConfigurationTypeDef",
    "InlinePayloadTypeDef",
    "InputConfigurationTypeDef",
    "InvokeBlueprintOptimizationAsyncRequestTypeDef",
    "InvokeBlueprintOptimizationAsyncResponseTypeDef",
    "InvokeDataAutomationLibraryIngestionJobRequestTypeDef",
    "InvokeDataAutomationLibraryIngestionJobResponseTypeDef",
    "ListBlueprintsRequestPaginateTypeDef",
    "ListBlueprintsRequestTypeDef",
    "ListBlueprintsResponseTypeDef",
    "ListDataAutomationLibrariesRequestPaginateTypeDef",
    "ListDataAutomationLibrariesRequestTypeDef",
    "ListDataAutomationLibrariesResponseTypeDef",
    "ListDataAutomationLibraryEntitiesRequestPaginateTypeDef",
    "ListDataAutomationLibraryEntitiesRequestTypeDef",
    "ListDataAutomationLibraryEntitiesResponseTypeDef",
    "ListDataAutomationLibraryIngestionJobsRequestPaginateTypeDef",
    "ListDataAutomationLibraryIngestionJobsRequestTypeDef",
    "ListDataAutomationLibraryIngestionJobsResponseTypeDef",
    "ListDataAutomationProjectsRequestPaginateTypeDef",
    "ListDataAutomationProjectsRequestTypeDef",
    "ListDataAutomationProjectsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ModalityProcessingConfigurationTypeDef",
    "ModalityRoutingConfigurationTypeDef",
    "NotificationConfigurationTypeDef",
    "OutputConfigurationTypeDef",
    "OverrideConfigurationOutputTypeDef",
    "OverrideConfigurationTypeDef",
    "OverrideConfigurationUnionTypeDef",
    "PIIEntitiesConfigurationOutputTypeDef",
    "PIIEntitiesConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PhraseTypeDef",
    "ResponseMetadataTypeDef",
    "S3ObjectTypeDef",
    "SensitiveDataConfigurationOutputTypeDef",
    "SensitiveDataConfigurationTypeDef",
    "SpeakerLabelingConfigurationTypeDef",
    "SplitterConfigurationTypeDef",
    "StandardOutputConfigurationOutputTypeDef",
    "StandardOutputConfigurationTypeDef",
    "StandardOutputConfigurationUnionTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TranscriptConfigurationTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateBlueprintRequestTypeDef",
    "UpdateBlueprintResponseTypeDef",
    "UpdateDataAutomationLibraryRequestTypeDef",
    "UpdateDataAutomationLibraryResponseTypeDef",
    "UpdateDataAutomationProjectRequestTypeDef",
    "UpdateDataAutomationProjectResponseTypeDef",
    "UpsertEntityInfoTypeDef",
    "VideoBoundingBoxTypeDef",
    "VideoExtractionCategoryOutputTypeDef",
    "VideoExtractionCategoryTypeDef",
    "VideoOverrideConfigurationOutputTypeDef",
    "VideoOverrideConfigurationTypeDef",
    "VideoStandardExtractionOutputTypeDef",
    "VideoStandardExtractionTypeDef",
    "VideoStandardGenerativeFieldOutputTypeDef",
    "VideoStandardGenerativeFieldTypeDef",
    "VideoStandardOutputConfigurationOutputTypeDef",
    "VideoStandardOutputConfigurationTypeDef",
    "VocabularyEntityInfoTypeDef",
    "VocabularyEntitySummaryTypeDef",
    "VocabularyEntityTypeDef",
)


class AudioLanguageConfigurationOutputTypeDef(TypedDict):
    inputLanguages: NotRequired[list[LanguageType]]
    generativeOutputLanguage: NotRequired[AudioGenerativeOutputLanguageType]
    identifyMultipleLanguages: NotRequired[bool]


class AudioLanguageConfigurationTypeDef(TypedDict):
    inputLanguages: NotRequired[Sequence[LanguageType]]
    generativeOutputLanguage: NotRequired[AudioGenerativeOutputLanguageType]
    identifyMultipleLanguages: NotRequired[bool]


class ModalityProcessingConfigurationTypeDef(TypedDict):
    state: NotRequired[StateType]


AudioStandardGenerativeFieldOutputTypeDef = TypedDict(
    "AudioStandardGenerativeFieldOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[list[AudioStandardGenerativeFieldTypeType]],
    },
)
AudioStandardGenerativeFieldTypeDef = TypedDict(
    "AudioStandardGenerativeFieldTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[AudioStandardGenerativeFieldTypeType]],
    },
)


class BlueprintFilterTypeDef(TypedDict):
    blueprintArn: str
    blueprintVersion: NotRequired[str]
    blueprintStage: NotRequired[BlueprintStageType]


class BlueprintItemTypeDef(TypedDict):
    blueprintArn: str
    blueprintVersion: NotRequired[str]
    blueprintStage: NotRequired[BlueprintStageType]


class BlueprintOptimizationObjectTypeDef(TypedDict):
    blueprintArn: str
    stage: NotRequired[BlueprintStageType]


class S3ObjectTypeDef(TypedDict):
    s3Uri: str
    version: NotRequired[str]


class BlueprintSummaryTypeDef(TypedDict):
    blueprintArn: str
    creationTime: datetime
    blueprintVersion: NotRequired[str]
    blueprintStage: NotRequired[BlueprintStageType]
    blueprintName: NotRequired[str]
    lastModifiedTime: NotRequired[datetime]


class ChannelLabelingConfigurationTypeDef(TypedDict):
    state: StateType


class CopyBlueprintStageRequestTypeDef(TypedDict):
    blueprintArn: str
    sourceStage: BlueprintStageType
    targetStage: BlueprintStageType
    clientToken: NotRequired[str]


class EncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: str
    kmsEncryptionContext: NotRequired[Mapping[str, str]]


class TagTypeDef(TypedDict):
    key: str
    value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateBlueprintVersionRequestTypeDef(TypedDict):
    blueprintArn: str
    clientToken: NotRequired[str]


class DataAutomationLibraryItemTypeDef(TypedDict):
    libraryArn: str


class VocabularyEntitySummaryTypeDef(TypedDict):
    entityId: NotRequired[str]
    description: NotRequired[str]
    language: NotRequired[LanguageType]
    numOfPhrases: NotRequired[int]
    lastModifiedTime: NotRequired[datetime]


class DataAutomationLibraryFilterTypeDef(TypedDict):
    libraryArn: str


class DataAutomationLibraryIngestionJobSummaryTypeDef(TypedDict):
    jobArn: str
    jobStatus: LibraryIngestionJobStatusType
    entityType: Literal["VOCABULARY"]
    operationType: LibraryIngestionJobOperationTypeType
    creationTime: datetime
    completionTime: NotRequired[datetime]


class OutputConfigurationTypeDef(TypedDict):
    s3Uri: str


class DataAutomationLibrarySummaryTypeDef(TypedDict):
    libraryArn: str
    creationTime: datetime
    libraryName: NotRequired[str]


class EntityTypeInfoTypeDef(TypedDict):
    entityType: Literal["VOCABULARY"]
    entityMetadata: NotRequired[str]


class DataAutomationProjectFilterTypeDef(TypedDict):
    projectArn: str
    projectStage: NotRequired[DataAutomationProjectStageType]


class DataAutomationProjectSummaryTypeDef(TypedDict):
    projectArn: str
    creationTime: datetime
    projectStage: NotRequired[DataAutomationProjectStageType]
    projectType: NotRequired[DataAutomationProjectTypeType]
    projectName: NotRequired[str]


class DeleteBlueprintRequestTypeDef(TypedDict):
    blueprintArn: str
    blueprintVersion: NotRequired[str]


class DeleteDataAutomationLibraryRequestTypeDef(TypedDict):
    libraryArn: str


class DeleteDataAutomationProjectRequestTypeDef(TypedDict):
    projectArn: str


class DeleteEntitiesInfoTypeDef(TypedDict):
    entityIds: Sequence[str]


class DocumentBoundingBoxTypeDef(TypedDict):
    state: StateType


DocumentExtractionGranularityOutputTypeDef = TypedDict(
    "DocumentExtractionGranularityOutputTypeDef",
    {
        "types": NotRequired[list[DocumentExtractionGranularityTypeType]],
    },
)
DocumentExtractionGranularityTypeDef = TypedDict(
    "DocumentExtractionGranularityTypeDef",
    {
        "types": NotRequired[Sequence[DocumentExtractionGranularityTypeType]],
    },
)


class DocumentOutputAdditionalFileFormatTypeDef(TypedDict):
    state: StateType


DocumentOutputTextFormatOutputTypeDef = TypedDict(
    "DocumentOutputTextFormatOutputTypeDef",
    {
        "types": NotRequired[list[DocumentOutputTextFormatTypeType]],
    },
)
DocumentOutputTextFormatTypeDef = TypedDict(
    "DocumentOutputTextFormatTypeDef",
    {
        "types": NotRequired[Sequence[DocumentOutputTextFormatTypeType]],
    },
)


class SplitterConfigurationTypeDef(TypedDict):
    state: NotRequired[StateType]


class DocumentStandardGenerativeFieldTypeDef(TypedDict):
    state: StateType


class EventBridgeConfigurationTypeDef(TypedDict):
    eventBridgeEnabled: bool


class GetBlueprintOptimizationStatusRequestTypeDef(TypedDict):
    invocationArn: str


class GetBlueprintRequestTypeDef(TypedDict):
    blueprintArn: str
    blueprintVersion: NotRequired[str]
    blueprintStage: NotRequired[BlueprintStageType]


class GetDataAutomationLibraryEntityRequestTypeDef(TypedDict):
    libraryArn: str
    entityType: Literal["VOCABULARY"]
    entityId: str


class GetDataAutomationLibraryIngestionJobRequestTypeDef(TypedDict):
    libraryArn: str
    jobArn: str


class GetDataAutomationLibraryRequestTypeDef(TypedDict):
    libraryArn: str


class GetDataAutomationProjectRequestTypeDef(TypedDict):
    projectArn: str
    projectStage: NotRequired[DataAutomationProjectStageType]


class ImageBoundingBoxTypeDef(TypedDict):
    state: StateType


ImageExtractionCategoryOutputTypeDef = TypedDict(
    "ImageExtractionCategoryOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[list[ImageExtractionCategoryTypeType]],
    },
)
ImageExtractionCategoryTypeDef = TypedDict(
    "ImageExtractionCategoryTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[ImageExtractionCategoryTypeType]],
    },
)
ImageStandardGenerativeFieldOutputTypeDef = TypedDict(
    "ImageStandardGenerativeFieldOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[list[ImageStandardGenerativeFieldTypeType]],
    },
)
ImageStandardGenerativeFieldTypeDef = TypedDict(
    "ImageStandardGenerativeFieldTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[ImageStandardGenerativeFieldTypeType]],
    },
)


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListDataAutomationLibraryEntitiesRequestTypeDef(TypedDict):
    libraryArn: str
    entityType: Literal["VOCABULARY"]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListDataAutomationLibraryIngestionJobsRequestTypeDef(TypedDict):
    libraryArn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceARN: str


class ModalityRoutingConfigurationTypeDef(TypedDict):
    jpeg: NotRequired[DesiredModalityType]
    png: NotRequired[DesiredModalityType]
    mp4: NotRequired[DesiredModalityType]
    mov: NotRequired[DesiredModalityType]


class PIIEntitiesConfigurationOutputTypeDef(TypedDict):
    piiEntityTypes: NotRequired[list[PIIEntityTypeType]]
    redactionMaskMode: NotRequired[PIIRedactionMaskModeType]


class PIIEntitiesConfigurationTypeDef(TypedDict):
    piiEntityTypes: NotRequired[Sequence[PIIEntityTypeType]]
    redactionMaskMode: NotRequired[PIIRedactionMaskModeType]


class PhraseTypeDef(TypedDict):
    text: str
    displayAsText: NotRequired[str]


class SpeakerLabelingConfigurationTypeDef(TypedDict):
    state: StateType


class UntagResourceRequestTypeDef(TypedDict):
    resourceARN: str
    tagKeys: Sequence[str]


class UpdateDataAutomationLibraryRequestTypeDef(TypedDict):
    libraryArn: str
    libraryDescription: NotRequired[str]
    clientToken: NotRequired[str]


class VideoBoundingBoxTypeDef(TypedDict):
    state: StateType


VideoExtractionCategoryOutputTypeDef = TypedDict(
    "VideoExtractionCategoryOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[list[VideoExtractionCategoryTypeType]],
    },
)
VideoExtractionCategoryTypeDef = TypedDict(
    "VideoExtractionCategoryTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[VideoExtractionCategoryTypeType]],
    },
)
VideoStandardGenerativeFieldOutputTypeDef = TypedDict(
    "VideoStandardGenerativeFieldOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[list[VideoStandardGenerativeFieldTypeType]],
    },
)
VideoStandardGenerativeFieldTypeDef = TypedDict(
    "VideoStandardGenerativeFieldTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[VideoStandardGenerativeFieldTypeType]],
    },
)


class DocumentCustomOutputConfigurationOutputTypeDef(TypedDict):
    fallbackBlueprints: NotRequired[list[BlueprintItemTypeDef]]


class DocumentCustomOutputConfigurationTypeDef(TypedDict):
    fallbackBlueprints: NotRequired[Sequence[BlueprintItemTypeDef]]


class BlueprintOptimizationOutputConfigurationTypeDef(TypedDict):
    s3Object: S3ObjectTypeDef


class BlueprintOptimizationSampleTypeDef(TypedDict):
    assetS3Object: S3ObjectTypeDef
    groundTruthS3Object: S3ObjectTypeDef


class UpdateBlueprintRequestTypeDef(TypedDict):
    blueprintArn: str
    schema: str
    blueprintStage: NotRequired[BlueprintStageType]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]


CreateBlueprintRequestTypeDef = TypedDict(
    "CreateBlueprintRequestTypeDef",
    {
        "blueprintName": str,
        "type": TypeType,
        "schema": str,
        "blueprintStage": NotRequired[BlueprintStageType],
        "clientToken": NotRequired[str],
        "encryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class CreateDataAutomationLibraryRequestTypeDef(TypedDict):
    libraryName: str
    libraryDescription: NotRequired[str]
    clientToken: NotRequired[str]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestTypeDef(TypedDict):
    resourceARN: str
    tags: Sequence[TagTypeDef]


class CreateDataAutomationLibraryResponseTypeDef(TypedDict):
    libraryArn: str
    status: DataAutomationLibraryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataAutomationProjectResponseTypeDef(TypedDict):
    projectArn: str
    projectStage: DataAutomationProjectStageType
    status: DataAutomationProjectStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataAutomationLibraryResponseTypeDef(TypedDict):
    libraryArn: str
    status: DataAutomationLibraryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataAutomationProjectResponseTypeDef(TypedDict):
    projectArn: str
    status: DataAutomationProjectStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class InvokeBlueprintOptimizationAsyncResponseTypeDef(TypedDict):
    invocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class InvokeDataAutomationLibraryIngestionJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListBlueprintsResponseTypeDef(TypedDict):
    blueprints: list[BlueprintSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataAutomationLibraryResponseTypeDef(TypedDict):
    libraryArn: str
    status: DataAutomationLibraryStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataAutomationProjectResponseTypeDef(TypedDict):
    projectArn: str
    projectStage: DataAutomationProjectStageType
    status: DataAutomationProjectStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DataAutomationLibraryConfigurationOutputTypeDef(TypedDict):
    libraries: NotRequired[list[DataAutomationLibraryItemTypeDef]]


class DataAutomationLibraryConfigurationTypeDef(TypedDict):
    libraries: NotRequired[Sequence[DataAutomationLibraryItemTypeDef]]


class DataAutomationLibraryEntitySummaryTypeDef(TypedDict):
    vocabulary: NotRequired[VocabularyEntitySummaryTypeDef]


class ListDataAutomationProjectsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    projectStageFilter: NotRequired[DataAutomationProjectStageFilterType]
    blueprintFilter: NotRequired[BlueprintFilterTypeDef]
    resourceOwner: NotRequired[ResourceOwnerType]
    libraryFilter: NotRequired[DataAutomationLibraryFilterTypeDef]


class ListDataAutomationLibraryIngestionJobsResponseTypeDef(TypedDict):
    jobs: list[DataAutomationLibraryIngestionJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataAutomationLibraryIngestionJobTypeDef(TypedDict):
    jobArn: str
    creationTime: datetime
    entityType: Literal["VOCABULARY"]
    operationType: LibraryIngestionJobOperationTypeType
    jobStatus: LibraryIngestionJobStatusType
    outputConfiguration: OutputConfigurationTypeDef
    completionTime: NotRequired[datetime]
    errorMessage: NotRequired[str]
    errorType: NotRequired[str]


class ListDataAutomationLibrariesResponseTypeDef(TypedDict):
    libraries: list[DataAutomationLibrarySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataAutomationLibraryTypeDef(TypedDict):
    libraryArn: str
    creationTime: datetime
    libraryName: str
    status: DataAutomationLibraryStatusType
    libraryDescription: NotRequired[str]
    entityTypes: NotRequired[list[EntityTypeInfoTypeDef]]
    kmsKeyId: NotRequired[str]
    kmsEncryptionContext: NotRequired[dict[str, str]]


class ListBlueprintsRequestTypeDef(TypedDict):
    blueprintArn: NotRequired[str]
    resourceOwner: NotRequired[ResourceOwnerType]
    blueprintStageFilter: NotRequired[BlueprintStageFilterType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    projectFilter: NotRequired[DataAutomationProjectFilterTypeDef]


class ListDataAutomationLibrariesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    projectFilter: NotRequired[DataAutomationProjectFilterTypeDef]


class ListDataAutomationProjectsResponseTypeDef(TypedDict):
    projects: list[DataAutomationProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DocumentStandardExtractionOutputTypeDef(TypedDict):
    granularity: DocumentExtractionGranularityOutputTypeDef
    boundingBox: DocumentBoundingBoxTypeDef


class DocumentStandardExtractionTypeDef(TypedDict):
    granularity: DocumentExtractionGranularityTypeDef
    boundingBox: DocumentBoundingBoxTypeDef


class DocumentOutputFormatOutputTypeDef(TypedDict):
    textFormat: DocumentOutputTextFormatOutputTypeDef
    additionalFileFormat: DocumentOutputAdditionalFileFormatTypeDef


class DocumentOutputFormatTypeDef(TypedDict):
    textFormat: DocumentOutputTextFormatTypeDef
    additionalFileFormat: DocumentOutputAdditionalFileFormatTypeDef


class NotificationConfigurationTypeDef(TypedDict):
    eventBridgeConfiguration: EventBridgeConfigurationTypeDef


class ImageStandardExtractionOutputTypeDef(TypedDict):
    category: ImageExtractionCategoryOutputTypeDef
    boundingBox: ImageBoundingBoxTypeDef


class ImageStandardExtractionTypeDef(TypedDict):
    category: ImageExtractionCategoryTypeDef
    boundingBox: ImageBoundingBoxTypeDef


class ListBlueprintsRequestPaginateTypeDef(TypedDict):
    blueprintArn: NotRequired[str]
    resourceOwner: NotRequired[ResourceOwnerType]
    blueprintStageFilter: NotRequired[BlueprintStageFilterType]
    projectFilter: NotRequired[DataAutomationProjectFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataAutomationLibrariesRequestPaginateTypeDef(TypedDict):
    projectFilter: NotRequired[DataAutomationProjectFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataAutomationLibraryEntitiesRequestPaginateTypeDef(TypedDict):
    libraryArn: str
    entityType: Literal["VOCABULARY"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataAutomationLibraryIngestionJobsRequestPaginateTypeDef(TypedDict):
    libraryArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataAutomationProjectsRequestPaginateTypeDef(TypedDict):
    projectStageFilter: NotRequired[DataAutomationProjectStageFilterType]
    blueprintFilter: NotRequired[BlueprintFilterTypeDef]
    resourceOwner: NotRequired[ResourceOwnerType]
    libraryFilter: NotRequired[DataAutomationLibraryFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SensitiveDataConfigurationOutputTypeDef(TypedDict):
    detectionMode: SensitiveDataDetectionModeType
    detectionScope: NotRequired[list[SensitiveDataDetectionScopeTypeType]]
    piiEntitiesConfiguration: NotRequired[PIIEntitiesConfigurationOutputTypeDef]


class SensitiveDataConfigurationTypeDef(TypedDict):
    detectionMode: SensitiveDataDetectionModeType
    detectionScope: NotRequired[Sequence[SensitiveDataDetectionScopeTypeType]]
    piiEntitiesConfiguration: NotRequired[PIIEntitiesConfigurationTypeDef]


class VocabularyEntityInfoTypeDef(TypedDict):
    language: LanguageType
    phrases: Sequence[PhraseTypeDef]
    entityId: NotRequired[str]
    description: NotRequired[str]


class VocabularyEntityTypeDef(TypedDict):
    entityId: NotRequired[str]
    description: NotRequired[str]
    language: NotRequired[LanguageType]
    phrases: NotRequired[list[PhraseTypeDef]]
    lastModifiedTime: NotRequired[datetime]


class TranscriptConfigurationTypeDef(TypedDict):
    speakerLabeling: NotRequired[SpeakerLabelingConfigurationTypeDef]
    channelLabeling: NotRequired[ChannelLabelingConfigurationTypeDef]


class VideoStandardExtractionOutputTypeDef(TypedDict):
    category: VideoExtractionCategoryOutputTypeDef
    boundingBox: VideoBoundingBoxTypeDef


class VideoStandardExtractionTypeDef(TypedDict):
    category: VideoExtractionCategoryTypeDef
    boundingBox: VideoBoundingBoxTypeDef


class CustomOutputConfigurationOutputTypeDef(TypedDict):
    blueprints: NotRequired[list[BlueprintItemTypeDef]]
    document: NotRequired[DocumentCustomOutputConfigurationOutputTypeDef]


class CustomOutputConfigurationTypeDef(TypedDict):
    blueprints: NotRequired[Sequence[BlueprintItemTypeDef]]
    document: NotRequired[DocumentCustomOutputConfigurationTypeDef]


class GetBlueprintOptimizationStatusResponseTypeDef(TypedDict):
    status: BlueprintOptimizationJobStatusType
    errorType: str
    errorMessage: str
    outputConfiguration: BlueprintOptimizationOutputConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


BlueprintTypeDef = TypedDict(
    "BlueprintTypeDef",
    {
        "blueprintArn": str,
        "schema": str,
        "type": TypeType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "blueprintName": str,
        "blueprintVersion": NotRequired[str],
        "blueprintStage": NotRequired[BlueprintStageType],
        "kmsKeyId": NotRequired[str],
        "kmsEncryptionContext": NotRequired[dict[str, str]],
        "optimizationSamples": NotRequired[list[BlueprintOptimizationSampleTypeDef]],
        "optimizationTime": NotRequired[datetime],
    },
)


class InvokeBlueprintOptimizationAsyncRequestTypeDef(TypedDict):
    blueprint: BlueprintOptimizationObjectTypeDef
    samples: Sequence[BlueprintOptimizationSampleTypeDef]
    outputConfiguration: BlueprintOptimizationOutputConfigurationTypeDef
    dataAutomationProfileArn: str
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


DataAutomationLibraryConfigurationUnionTypeDef = Union[
    DataAutomationLibraryConfigurationTypeDef, DataAutomationLibraryConfigurationOutputTypeDef
]


class ListDataAutomationLibraryEntitiesResponseTypeDef(TypedDict):
    entities: list[DataAutomationLibraryEntitySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetDataAutomationLibraryIngestionJobResponseTypeDef(TypedDict):
    job: DataAutomationLibraryIngestionJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDataAutomationLibraryResponseTypeDef(TypedDict):
    library: DataAutomationLibraryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DocumentStandardOutputConfigurationOutputTypeDef(TypedDict):
    extraction: NotRequired[DocumentStandardExtractionOutputTypeDef]
    generativeField: NotRequired[DocumentStandardGenerativeFieldTypeDef]
    outputFormat: NotRequired[DocumentOutputFormatOutputTypeDef]


class DocumentStandardOutputConfigurationTypeDef(TypedDict):
    extraction: NotRequired[DocumentStandardExtractionTypeDef]
    generativeField: NotRequired[DocumentStandardGenerativeFieldTypeDef]
    outputFormat: NotRequired[DocumentOutputFormatTypeDef]


class ImageStandardOutputConfigurationOutputTypeDef(TypedDict):
    extraction: NotRequired[ImageStandardExtractionOutputTypeDef]
    generativeField: NotRequired[ImageStandardGenerativeFieldOutputTypeDef]


class ImageStandardOutputConfigurationTypeDef(TypedDict):
    extraction: NotRequired[ImageStandardExtractionTypeDef]
    generativeField: NotRequired[ImageStandardGenerativeFieldTypeDef]


class AudioOverrideConfigurationOutputTypeDef(TypedDict):
    modalityProcessing: NotRequired[ModalityProcessingConfigurationTypeDef]
    languageConfiguration: NotRequired[AudioLanguageConfigurationOutputTypeDef]
    sensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationOutputTypeDef]


class DocumentOverrideConfigurationOutputTypeDef(TypedDict):
    splitter: NotRequired[SplitterConfigurationTypeDef]
    modalityProcessing: NotRequired[ModalityProcessingConfigurationTypeDef]
    sensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationOutputTypeDef]


class ImageOverrideConfigurationOutputTypeDef(TypedDict):
    modalityProcessing: NotRequired[ModalityProcessingConfigurationTypeDef]
    sensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationOutputTypeDef]


class VideoOverrideConfigurationOutputTypeDef(TypedDict):
    modalityProcessing: NotRequired[ModalityProcessingConfigurationTypeDef]
    sensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationOutputTypeDef]


class AudioOverrideConfigurationTypeDef(TypedDict):
    modalityProcessing: NotRequired[ModalityProcessingConfigurationTypeDef]
    languageConfiguration: NotRequired[AudioLanguageConfigurationTypeDef]
    sensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationTypeDef]


class DocumentOverrideConfigurationTypeDef(TypedDict):
    splitter: NotRequired[SplitterConfigurationTypeDef]
    modalityProcessing: NotRequired[ModalityProcessingConfigurationTypeDef]
    sensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationTypeDef]


class ImageOverrideConfigurationTypeDef(TypedDict):
    modalityProcessing: NotRequired[ModalityProcessingConfigurationTypeDef]
    sensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationTypeDef]


class VideoOverrideConfigurationTypeDef(TypedDict):
    modalityProcessing: NotRequired[ModalityProcessingConfigurationTypeDef]
    sensitiveDataConfiguration: NotRequired[SensitiveDataConfigurationTypeDef]


class UpsertEntityInfoTypeDef(TypedDict):
    vocabulary: NotRequired[VocabularyEntityInfoTypeDef]


class EntityDetailsTypeDef(TypedDict):
    vocabulary: NotRequired[VocabularyEntityTypeDef]


class AudioExtractionCategoryTypeConfigurationTypeDef(TypedDict):
    transcript: NotRequired[TranscriptConfigurationTypeDef]


class VideoStandardOutputConfigurationOutputTypeDef(TypedDict):
    extraction: NotRequired[VideoStandardExtractionOutputTypeDef]
    generativeField: NotRequired[VideoStandardGenerativeFieldOutputTypeDef]


class VideoStandardOutputConfigurationTypeDef(TypedDict):
    extraction: NotRequired[VideoStandardExtractionTypeDef]
    generativeField: NotRequired[VideoStandardGenerativeFieldTypeDef]


CustomOutputConfigurationUnionTypeDef = Union[
    CustomOutputConfigurationTypeDef, CustomOutputConfigurationOutputTypeDef
]


class CreateBlueprintResponseTypeDef(TypedDict):
    blueprint: BlueprintTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBlueprintVersionResponseTypeDef(TypedDict):
    blueprint: BlueprintTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetBlueprintResponseTypeDef(TypedDict):
    blueprint: BlueprintTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBlueprintResponseTypeDef(TypedDict):
    blueprint: BlueprintTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class OverrideConfigurationOutputTypeDef(TypedDict):
    document: NotRequired[DocumentOverrideConfigurationOutputTypeDef]
    image: NotRequired[ImageOverrideConfigurationOutputTypeDef]
    video: NotRequired[VideoOverrideConfigurationOutputTypeDef]
    audio: NotRequired[AudioOverrideConfigurationOutputTypeDef]
    modalityRouting: NotRequired[ModalityRoutingConfigurationTypeDef]


class OverrideConfigurationTypeDef(TypedDict):
    document: NotRequired[DocumentOverrideConfigurationTypeDef]
    image: NotRequired[ImageOverrideConfigurationTypeDef]
    video: NotRequired[VideoOverrideConfigurationTypeDef]
    audio: NotRequired[AudioOverrideConfigurationTypeDef]
    modalityRouting: NotRequired[ModalityRoutingConfigurationTypeDef]


class InlinePayloadTypeDef(TypedDict):
    upsertEntitiesInfo: NotRequired[Sequence[UpsertEntityInfoTypeDef]]
    deleteEntitiesInfo: NotRequired[DeleteEntitiesInfoTypeDef]


class GetDataAutomationLibraryEntityResponseTypeDef(TypedDict):
    entity: EntityDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


AudioExtractionCategoryOutputTypeDef = TypedDict(
    "AudioExtractionCategoryOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[list[AudioExtractionCategoryTypeType]],
        "typeConfiguration": NotRequired[AudioExtractionCategoryTypeConfigurationTypeDef],
    },
)
AudioExtractionCategoryTypeDef = TypedDict(
    "AudioExtractionCategoryTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[AudioExtractionCategoryTypeType]],
        "typeConfiguration": NotRequired[AudioExtractionCategoryTypeConfigurationTypeDef],
    },
)
OverrideConfigurationUnionTypeDef = Union[
    OverrideConfigurationTypeDef, OverrideConfigurationOutputTypeDef
]


class InputConfigurationTypeDef(TypedDict):
    s3Object: NotRequired[S3ObjectTypeDef]
    inlinePayload: NotRequired[InlinePayloadTypeDef]


class AudioStandardExtractionOutputTypeDef(TypedDict):
    category: AudioExtractionCategoryOutputTypeDef


class AudioStandardExtractionTypeDef(TypedDict):
    category: AudioExtractionCategoryTypeDef


class InvokeDataAutomationLibraryIngestionJobRequestTypeDef(TypedDict):
    libraryArn: str
    inputConfiguration: InputConfigurationTypeDef
    entityType: Literal["VOCABULARY"]
    operationType: LibraryIngestionJobOperationTypeType
    outputConfiguration: OutputConfigurationTypeDef
    clientToken: NotRequired[str]
    notificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class AudioStandardOutputConfigurationOutputTypeDef(TypedDict):
    extraction: NotRequired[AudioStandardExtractionOutputTypeDef]
    generativeField: NotRequired[AudioStandardGenerativeFieldOutputTypeDef]


class AudioStandardOutputConfigurationTypeDef(TypedDict):
    extraction: NotRequired[AudioStandardExtractionTypeDef]
    generativeField: NotRequired[AudioStandardGenerativeFieldTypeDef]


class StandardOutputConfigurationOutputTypeDef(TypedDict):
    document: NotRequired[DocumentStandardOutputConfigurationOutputTypeDef]
    image: NotRequired[ImageStandardOutputConfigurationOutputTypeDef]
    video: NotRequired[VideoStandardOutputConfigurationOutputTypeDef]
    audio: NotRequired[AudioStandardOutputConfigurationOutputTypeDef]


class StandardOutputConfigurationTypeDef(TypedDict):
    document: NotRequired[DocumentStandardOutputConfigurationTypeDef]
    image: NotRequired[ImageStandardOutputConfigurationTypeDef]
    video: NotRequired[VideoStandardOutputConfigurationTypeDef]
    audio: NotRequired[AudioStandardOutputConfigurationTypeDef]


class DataAutomationProjectTypeDef(TypedDict):
    projectArn: str
    creationTime: datetime
    lastModifiedTime: datetime
    projectName: str
    status: DataAutomationProjectStatusType
    projectStage: NotRequired[DataAutomationProjectStageType]
    projectType: NotRequired[DataAutomationProjectTypeType]
    projectDescription: NotRequired[str]
    standardOutputConfiguration: NotRequired[StandardOutputConfigurationOutputTypeDef]
    customOutputConfiguration: NotRequired[CustomOutputConfigurationOutputTypeDef]
    overrideConfiguration: NotRequired[OverrideConfigurationOutputTypeDef]
    dataAutomationLibraryConfiguration: NotRequired[DataAutomationLibraryConfigurationOutputTypeDef]
    kmsKeyId: NotRequired[str]
    kmsEncryptionContext: NotRequired[dict[str, str]]


StandardOutputConfigurationUnionTypeDef = Union[
    StandardOutputConfigurationTypeDef, StandardOutputConfigurationOutputTypeDef
]


class GetDataAutomationProjectResponseTypeDef(TypedDict):
    project: DataAutomationProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataAutomationProjectRequestTypeDef(TypedDict):
    projectName: str
    standardOutputConfiguration: StandardOutputConfigurationUnionTypeDef
    projectDescription: NotRequired[str]
    projectStage: NotRequired[DataAutomationProjectStageType]
    projectType: NotRequired[DataAutomationProjectTypeType]
    customOutputConfiguration: NotRequired[CustomOutputConfigurationUnionTypeDef]
    overrideConfiguration: NotRequired[OverrideConfigurationUnionTypeDef]
    dataAutomationLibraryConfiguration: NotRequired[DataAutomationLibraryConfigurationUnionTypeDef]
    clientToken: NotRequired[str]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateDataAutomationProjectRequestTypeDef(TypedDict):
    projectArn: str
    standardOutputConfiguration: StandardOutputConfigurationUnionTypeDef
    projectStage: NotRequired[DataAutomationProjectStageType]
    projectDescription: NotRequired[str]
    customOutputConfiguration: NotRequired[CustomOutputConfigurationUnionTypeDef]
    overrideConfiguration: NotRequired[OverrideConfigurationUnionTypeDef]
    dataAutomationLibraryConfiguration: NotRequired[DataAutomationLibraryConfigurationUnionTypeDef]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
