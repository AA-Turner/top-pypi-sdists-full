"""
Type annotations for healthlake service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_healthlake.type_defs import AgentInputMessageTypeDef

    data: AgentInputMessageTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AgentInputMessageTypeType,
    AgentOutputMessageTypeType,
    AnalyticsStatusType,
    AuthorizationStrategyType,
    CmkTypeType,
    DatastoreStatusType,
    ErrorCategoryType,
    JobStatusType,
    NlpStatusType,
    SourceFormatType,
    TransformationJobStatusType,
    ValidationLevelType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AgentInputMessageTypeDef",
    "AgentOutputMessageTypeDef",
    "AnalyticsConfigurationTypeDef",
    "CreateDataTransformationProfileRequestTypeDef",
    "CreateDataTransformationProfileResponseTypeDef",
    "CreateDataTransformationProfileSourceTypeDef",
    "CreateFHIRDatastoreRequestTypeDef",
    "CreateFHIRDatastoreResponseTypeDef",
    "DataTransformationProfileSummaryTypeDef",
    "DataTransformationProfileVersionSummaryTypeDef",
    "DataTransformationS3ConfigurationTypeDef",
    "DatastoreFilterTypeDef",
    "DatastorePropertiesTypeDef",
    "DeleteDataTransformationProfileRequestTypeDef",
    "DeleteDataTransformationProfileResponseTypeDef",
    "DeleteFHIRDatastoreRequestTypeDef",
    "DeleteFHIRDatastoreResponseTypeDef",
    "DescribeDataTransformationJobRequestTypeDef",
    "DescribeDataTransformationJobRequestWaitTypeDef",
    "DescribeDataTransformationJobResponseTypeDef",
    "DescribeFHIRDatastoreRequestTypeDef",
    "DescribeFHIRDatastoreRequestWaitExtraTypeDef",
    "DescribeFHIRDatastoreRequestWaitTypeDef",
    "DescribeFHIRDatastoreResponseTypeDef",
    "DescribeFHIRExportJobRequestTypeDef",
    "DescribeFHIRExportJobRequestWaitTypeDef",
    "DescribeFHIRExportJobResponseTypeDef",
    "DescribeFHIRImportJobRequestTypeDef",
    "DescribeFHIRImportJobRequestWaitTypeDef",
    "DescribeFHIRImportJobResponseTypeDef",
    "ErrorCauseTypeDef",
    "ExistingVersionedProfileSourceTypeDef",
    "ExportJobPropertiesTypeDef",
    "GetDataTransformationProfileRequestTypeDef",
    "GetDataTransformationProfileResponseTypeDef",
    "IdentityProviderConfigurationTypeDef",
    "ImportJobPropertiesTypeDef",
    "InputDataConfigTypeDef",
    "JobProgressReportTypeDef",
    "KmsEncryptionConfigTypeDef",
    "ListDataTransformationJobsRequestPaginateTypeDef",
    "ListDataTransformationJobsRequestTypeDef",
    "ListDataTransformationJobsResponseTypeDef",
    "ListDataTransformationProfileVersionsRequestPaginateTypeDef",
    "ListDataTransformationProfileVersionsRequestTypeDef",
    "ListDataTransformationProfileVersionsResponseTypeDef",
    "ListDataTransformationProfilesRequestPaginateTypeDef",
    "ListDataTransformationProfilesRequestTypeDef",
    "ListDataTransformationProfilesResponseTypeDef",
    "ListFHIRDatastoresRequestTypeDef",
    "ListFHIRDatastoresResponseTypeDef",
    "ListFHIRExportJobsRequestTypeDef",
    "ListFHIRExportJobsResponseTypeDef",
    "ListFHIRImportJobsRequestTypeDef",
    "ListFHIRImportJobsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NlpConfigurationTypeDef",
    "OutputDataConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PreloadDataConfigTypeDef",
    "ProfileConfigurationOutputTypeDef",
    "ProfileConfigurationTypeDef",
    "ProfileConfigurationUnionTypeDef",
    "ProfileMappingSourceTypeDef",
    "PublishDataTransformationProfileRequestTypeDef",
    "PublishDataTransformationProfileResponseTypeDef",
    "ResponseMetadataTypeDef",
    "S3ConfigurationTypeDef",
    "SampleDataSourceTypeDef",
    "SseConfigurationTypeDef",
    "StartDataTransformationJobRequestTypeDef",
    "StartDataTransformationJobResponseTypeDef",
    "StartFHIRExportJobRequestTypeDef",
    "StartFHIRExportJobResponseTypeDef",
    "StartFHIRImportJobRequestTypeDef",
    "StartFHIRImportJobResponseTypeDef",
    "StarterProfileSourceTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "TransformationInputDataConfigTypeDef",
    "TransformationJobProgressReportTypeDef",
    "TransformationJobPropertiesTypeDef",
    "TransformationJobSummaryTypeDef",
    "TransformationOutputDataConfigTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateDataTransformationProfileRequestTypeDef",
    "UpdateDataTransformationProfileResponseTypeDef",
    "UpdateFHIRDatastoreRequestTypeDef",
    "UpdateFHIRDatastoreResponseTypeDef",
    "UpdateProfileWithAgentRequestTypeDef",
    "UpdateProfileWithAgentResponseTypeDef",
    "WaiterConfigTypeDef",
)

AgentInputMessageTypeDef = TypedDict(
    "AgentInputMessageTypeDef",
    {
        "Body": str,
        "Type": AgentInputMessageTypeType,
    },
)
AgentOutputMessageTypeDef = TypedDict(
    "AgentOutputMessageTypeDef",
    {
        "Body": str,
        "Type": AgentOutputMessageTypeType,
        "OptionsList": NotRequired[list[str]],
    },
)


class AnalyticsConfigurationTypeDef(TypedDict):
    Status: NotRequired[AnalyticsStatusType]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ExistingVersionedProfileSourceTypeDef(TypedDict):
    ProfileId: str
    Version: int


class ProfileMappingSourceTypeDef(TypedDict):
    ProfileMapping: Mapping[str, str]


class SampleDataSourceTypeDef(TypedDict):
    S3Uri: str


class StarterProfileSourceTypeDef(TypedDict):
    StarterProfileName: str


class IdentityProviderConfigurationTypeDef(TypedDict):
    AuthorizationStrategy: AuthorizationStrategyType
    FineGrainedAuthorizationEnabled: NotRequired[bool]
    Metadata: NotRequired[str]
    IdpLambdaArn: NotRequired[str]


class NlpConfigurationTypeDef(TypedDict):
    Status: NotRequired[NlpStatusType]


class PreloadDataConfigTypeDef(TypedDict):
    PreloadDataType: Literal["SYNTHEA"]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class DataTransformationProfileSummaryTypeDef(TypedDict):
    ProfileId: str
    Version: int
    SourceFormat: SourceFormatType
    TargetFormat: Literal["FHIR_R4"]
    ProfileName: NotRequired[str]
    ProfileDescription: NotRequired[str]
    LastUpdatedAt: NotRequired[datetime]


class DataTransformationProfileVersionSummaryTypeDef(TypedDict):
    ProfileId: str
    Version: int
    SourceFormat: SourceFormatType
    TargetFormat: Literal["FHIR_R4"]
    ProfileName: NotRequired[str]
    ChangeDescription: NotRequired[str]
    LastUpdatedAt: NotRequired[datetime]


class DataTransformationS3ConfigurationTypeDef(TypedDict):
    S3Uri: str
    KmsKeyId: str


TimestampTypeDef = Union[datetime, str]


class ErrorCauseTypeDef(TypedDict):
    ErrorMessage: NotRequired[str]
    ErrorCategory: NotRequired[ErrorCategoryType]


class ProfileConfigurationOutputTypeDef(TypedDict):
    DefaultProfiles: NotRequired[list[str]]


class DeleteDataTransformationProfileRequestTypeDef(TypedDict):
    ProfileId: str


class DeleteFHIRDatastoreRequestTypeDef(TypedDict):
    DatastoreId: str


class DescribeDataTransformationJobRequestTypeDef(TypedDict):
    JobId: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeFHIRDatastoreRequestTypeDef(TypedDict):
    DatastoreId: str


class DescribeFHIRExportJobRequestTypeDef(TypedDict):
    DatastoreId: str
    JobId: str


class DescribeFHIRImportJobRequestTypeDef(TypedDict):
    DatastoreId: str
    JobId: str


class GetDataTransformationProfileRequestTypeDef(TypedDict):
    ProfileId: str
    ProfileVersion: NotRequired[int]


class InputDataConfigTypeDef(TypedDict):
    S3Uri: NotRequired[str]


class JobProgressReportTypeDef(TypedDict):
    TotalNumberOfScannedFiles: NotRequired[int]
    TotalSizeOfScannedFilesInMB: NotRequired[float]
    TotalNumberOfImportedFiles: NotRequired[int]
    TotalNumberOfResourcesScanned: NotRequired[int]
    TotalNumberOfResourcesImported: NotRequired[int]
    TotalNumberOfResourcesWithCustomerError: NotRequired[int]
    TotalNumberOfFilesReadWithCustomerError: NotRequired[int]
    TotalNumberOfScannedNonFhirFiles: NotRequired[int]
    TotalSizeOfScannedNonFhirFilesInMB: NotRequired[float]
    TotalNumberOfImportedNonFhirFiles: NotRequired[int]
    TotalNumberOfNonFhirResourcesScanned: NotRequired[int]
    TotalNumberOfNonFhirResourcesImported: NotRequired[int]
    TotalNumberOfNonFhirResourcesWithCustomerError: NotRequired[int]
    TotalNumberOfNonFhirFilesReadWithCustomerError: NotRequired[int]
    Throughput: NotRequired[float]
    TotalFilesConverted: NotRequired[int]
    TotalResourcesGenerated: NotRequired[int]


class KmsEncryptionConfigTypeDef(TypedDict):
    CmkType: CmkTypeType
    KmsKeyId: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class TransformationJobSummaryTypeDef(TypedDict):
    JobId: str
    JobStatus: TransformationJobStatusType
    SubmitTime: datetime
    JobName: NotRequired[str]
    EndTime: NotRequired[datetime]
    SourceFormat: NotRequired[SourceFormatType]


class ListDataTransformationProfileVersionsRequestTypeDef(TypedDict):
    ProfileId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListDataTransformationProfilesRequestTypeDef(TypedDict):
    SourceFormat: SourceFormatType
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceARN: str


class S3ConfigurationTypeDef(TypedDict):
    S3Uri: str
    KmsKeyId: str


class ProfileConfigurationTypeDef(TypedDict):
    DefaultProfiles: NotRequired[Sequence[str]]


class PublishDataTransformationProfileRequestTypeDef(TypedDict):
    ProfileId: str
    SourceFormat: SourceFormatType
    FromExistingVersion: NotRequired[int]
    ChangeDescription: NotRequired[str]


class TransformationInputDataConfigTypeDef(TypedDict):
    S3Uri: str
    SourceFormat: NotRequired[SourceFormatType]


class TransformationJobProgressReportTypeDef(TypedDict):
    TotalFilesScanned: int
    TotalFilesConverted: int
    TotalFilesFailed: int
    TotalResourcesGenerated: int


class UntagResourceRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateDataTransformationProfileRequestTypeDef(TypedDict):
    ProfileId: str
    ProfileMapping: Mapping[str, str]
    ChangeDescription: NotRequired[str]


class UpdateProfileWithAgentRequestTypeDef(TypedDict):
    ProfileId: str
    SourceFormat: SourceFormatType
    InputMessage: AgentInputMessageTypeDef
    ConversationId: NotRequired[str]


class CreateDataTransformationProfileResponseTypeDef(TypedDict):
    ProfileId: str
    Version: int
    SourceFormat: SourceFormatType
    TargetFormat: Literal["FHIR_R4"]
    ProfileName: str
    LastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFHIRDatastoreResponseTypeDef(TypedDict):
    DatastoreId: str
    DatastoreArn: str
    DatastoreStatus: DatastoreStatusType
    DatastoreEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataTransformationProfileResponseTypeDef(TypedDict):
    ProfileId: str
    ProfileName: str
    DeletionTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFHIRDatastoreResponseTypeDef(TypedDict):
    DatastoreId: str
    DatastoreArn: str
    DatastoreStatus: DatastoreStatusType
    DatastoreEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDataTransformationProfileResponseTypeDef(TypedDict):
    ProfileId: str
    Version: int
    SourceFormat: SourceFormatType
    TargetFormat: Literal["FHIR_R4"]
    ProfileMapping: dict[str, str]
    ProfileName: str
    ProfileDescription: str
    ChangeDescription: str
    LastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class PublishDataTransformationProfileResponseTypeDef(TypedDict):
    ProfileId: str
    Version: int
    SourceFormat: SourceFormatType
    TargetFormat: Literal["FHIR_R4"]
    ProfileName: str
    LastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class StartDataTransformationJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: TransformationJobStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class StartFHIRExportJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    DatastoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartFHIRImportJobResponseTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    DatastoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataTransformationProfileResponseTypeDef(TypedDict):
    ProfileId: str
    SourceFormat: SourceFormatType
    TargetFormat: Literal["FHIR_R4"]
    ProfileName: str
    LastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProfileWithAgentResponseTypeDef(TypedDict):
    AgentResponse: AgentOutputMessageTypeDef
    ConversationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataTransformationProfileSourceTypeDef(TypedDict):
    StarterProfile: NotRequired[StarterProfileSourceTypeDef]
    ExistingVersionedProfileId: NotRequired[ExistingVersionedProfileSourceTypeDef]
    ProfileMapping: NotRequired[ProfileMappingSourceTypeDef]
    SampleData: NotRequired[SampleDataSourceTypeDef]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class ListDataTransformationProfilesResponseTypeDef(TypedDict):
    Items: list[DataTransformationProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDataTransformationProfileVersionsResponseTypeDef(TypedDict):
    Items: list[DataTransformationProfileVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TransformationOutputDataConfigTypeDef(TypedDict):
    S3Configuration: DataTransformationS3ConfigurationTypeDef


class DatastoreFilterTypeDef(TypedDict):
    DatastoreName: NotRequired[str]
    DatastoreStatus: NotRequired[DatastoreStatusType]
    CreatedBefore: NotRequired[TimestampTypeDef]
    CreatedAfter: NotRequired[TimestampTypeDef]


class ListDataTransformationJobsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    JobStatus: NotRequired[TransformationJobStatusType]
    JobName: NotRequired[str]
    SubmittedAfter: NotRequired[TimestampTypeDef]
    SubmittedBefore: NotRequired[TimestampTypeDef]


class ListFHIRExportJobsRequestTypeDef(TypedDict):
    DatastoreId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmittedBefore: NotRequired[TimestampTypeDef]
    SubmittedAfter: NotRequired[TimestampTypeDef]


class ListFHIRImportJobsRequestTypeDef(TypedDict):
    DatastoreId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    JobName: NotRequired[str]
    JobStatus: NotRequired[JobStatusType]
    SubmittedBefore: NotRequired[TimestampTypeDef]
    SubmittedAfter: NotRequired[TimestampTypeDef]


class DescribeDataTransformationJobRequestWaitTypeDef(TypedDict):
    JobId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeFHIRDatastoreRequestWaitExtraTypeDef(TypedDict):
    DatastoreId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeFHIRDatastoreRequestWaitTypeDef(TypedDict):
    DatastoreId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeFHIRExportJobRequestWaitTypeDef(TypedDict):
    DatastoreId: str
    JobId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeFHIRImportJobRequestWaitTypeDef(TypedDict):
    DatastoreId: str
    JobId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class SseConfigurationTypeDef(TypedDict):
    KmsEncryptionConfig: KmsEncryptionConfigTypeDef


class ListDataTransformationJobsRequestPaginateTypeDef(TypedDict):
    JobStatus: NotRequired[TransformationJobStatusType]
    JobName: NotRequired[str]
    SubmittedAfter: NotRequired[TimestampTypeDef]
    SubmittedBefore: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataTransformationProfileVersionsRequestPaginateTypeDef(TypedDict):
    ProfileId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataTransformationProfilesRequestPaginateTypeDef(TypedDict):
    SourceFormat: SourceFormatType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataTransformationJobsResponseTypeDef(TypedDict):
    Items: list[TransformationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class OutputDataConfigTypeDef(TypedDict):
    S3Configuration: NotRequired[S3ConfigurationTypeDef]


ProfileConfigurationUnionTypeDef = Union[
    ProfileConfigurationTypeDef, ProfileConfigurationOutputTypeDef
]


class CreateDataTransformationProfileRequestTypeDef(TypedDict):
    SourceFormat: SourceFormatType
    Source: CreateDataTransformationProfileSourceTypeDef
    ProfileName: str
    KmsKeyId: NotRequired[str]
    ProfileDescription: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]


class StartDataTransformationJobRequestTypeDef(TypedDict):
    InputDataConfig: TransformationInputDataConfigTypeDef
    OutputDataConfig: TransformationOutputDataConfigTypeDef
    DataAccessRoleArn: str
    ClientToken: str
    ProfileId: str
    JobName: NotRequired[str]
    DriftDetectionEnabled: NotRequired[bool]
    ProvenanceEnabled: NotRequired[bool]


class TransformationJobPropertiesTypeDef(TypedDict):
    JobId: str
    JobStatus: TransformationJobStatusType
    InputDataConfig: TransformationInputDataConfigTypeDef
    OutputDataConfig: TransformationOutputDataConfigTypeDef
    DataAccessRoleArn: str
    SubmitTime: datetime
    JobName: NotRequired[str]
    ProfileId: NotRequired[str]
    ProfileName: NotRequired[str]
    ProfileVersion: NotRequired[int]
    EndTime: NotRequired[datetime]
    DriftDetectionEnabled: NotRequired[bool]
    ProvenanceEnabled: NotRequired[bool]
    Message: NotRequired[str]
    JobProgressReport: NotRequired[TransformationJobProgressReportTypeDef]


class ListFHIRDatastoresRequestTypeDef(TypedDict):
    Filter: NotRequired[DatastoreFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DatastorePropertiesTypeDef(TypedDict):
    DatastoreId: str
    DatastoreArn: str
    DatastoreStatus: DatastoreStatusType
    DatastoreTypeVersion: Literal["R4"]
    DatastoreEndpoint: str
    DatastoreName: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    SseConfiguration: NotRequired[SseConfigurationTypeDef]
    PreloadDataConfig: NotRequired[PreloadDataConfigTypeDef]
    IdentityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]
    ErrorCause: NotRequired[ErrorCauseTypeDef]
    NlpConfiguration: NotRequired[NlpConfigurationTypeDef]
    AnalyticsConfiguration: NotRequired[AnalyticsConfigurationTypeDef]
    ProfileConfiguration: NotRequired[ProfileConfigurationOutputTypeDef]


class ExportJobPropertiesTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    SubmitTime: datetime
    DatastoreId: str
    OutputDataConfig: OutputDataConfigTypeDef
    JobName: NotRequired[str]
    EndTime: NotRequired[datetime]
    DataAccessRoleArn: NotRequired[str]
    Message: NotRequired[str]


class ImportJobPropertiesTypeDef(TypedDict):
    JobId: str
    JobStatus: JobStatusType
    SubmitTime: datetime
    DatastoreId: str
    InputDataConfig: InputDataConfigTypeDef
    JobName: NotRequired[str]
    EndTime: NotRequired[datetime]
    JobOutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    JobProgressReport: NotRequired[JobProgressReportTypeDef]
    DataAccessRoleArn: NotRequired[str]
    Message: NotRequired[str]
    ValidationLevel: NotRequired[ValidationLevelType]


class StartFHIRExportJobRequestTypeDef(TypedDict):
    OutputDataConfig: OutputDataConfigTypeDef
    DatastoreId: str
    DataAccessRoleArn: str
    JobName: NotRequired[str]
    ClientToken: NotRequired[str]


class StartFHIRImportJobRequestTypeDef(TypedDict):
    InputDataConfig: InputDataConfigTypeDef
    JobOutputDataConfig: OutputDataConfigTypeDef
    DatastoreId: str
    DataAccessRoleArn: str
    JobName: NotRequired[str]
    ClientToken: NotRequired[str]
    ValidationLevel: NotRequired[ValidationLevelType]
    ProfileId: NotRequired[str]
    InputFormat: NotRequired[str]
    DriftDetectionEnabled: NotRequired[bool]
    ProvenanceEnabled: NotRequired[bool]


class CreateFHIRDatastoreRequestTypeDef(TypedDict):
    DatastoreTypeVersion: Literal["R4"]
    DatastoreName: NotRequired[str]
    SseConfiguration: NotRequired[SseConfigurationTypeDef]
    PreloadDataConfig: NotRequired[PreloadDataConfigTypeDef]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    IdentityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]
    AnalyticsConfiguration: NotRequired[AnalyticsConfigurationTypeDef]
    NlpConfiguration: NotRequired[NlpConfigurationTypeDef]
    ProfileConfiguration: NotRequired[ProfileConfigurationUnionTypeDef]


class UpdateFHIRDatastoreRequestTypeDef(TypedDict):
    DatastoreId: str
    DatastoreName: NotRequired[str]
    AnalyticsConfiguration: NotRequired[AnalyticsConfigurationTypeDef]
    NlpConfiguration: NotRequired[NlpConfigurationTypeDef]
    ProfileConfiguration: NotRequired[ProfileConfigurationUnionTypeDef]
    IdentityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]


class DescribeDataTransformationJobResponseTypeDef(TypedDict):
    TransformationJobProperties: TransformationJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFHIRDatastoreResponseTypeDef(TypedDict):
    DatastoreProperties: DatastorePropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListFHIRDatastoresResponseTypeDef(TypedDict):
    DatastorePropertiesList: list[DatastorePropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateFHIRDatastoreResponseTypeDef(TypedDict):
    DatastoreProperties: DatastorePropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFHIRExportJobResponseTypeDef(TypedDict):
    ExportJobProperties: ExportJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListFHIRExportJobsResponseTypeDef(TypedDict):
    ExportJobPropertiesList: list[ExportJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeFHIRImportJobResponseTypeDef(TypedDict):
    ImportJobProperties: ImportJobPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListFHIRImportJobsResponseTypeDef(TypedDict):
    ImportJobPropertiesList: list[ImportJobPropertiesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
