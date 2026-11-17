"""
Type annotations for connecthealth service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connecthealth/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_connecthealth.type_defs import ActivateSubscriptionInputTypeDef

    data: ActivateSubscriptionInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    ChecklistItemStatusType,
    CustomTemplateBaseType,
    DatasetStatusType,
    DomainStatusType,
    EncounterTypeType,
    EncryptionTypeType,
    FeedbackArtifactTypeType,
    JobStatusType,
    ManagedNoteTemplateType,
    MedicalScribeLanguageCodeType,
    MedicalScribeMediaEncodingType,
    MedicalScribeParticipantRoleType,
    MedicalScribeStreamStatusType,
    PatientStatusType,
    PeriodontalReviewReasonType,
    PeriodontalSiteNameType,
    PostStreamArtifactGenerationStatusType,
    PronounsType,
    SexType,
    SubscriptionStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ActivateSubscriptionInputTypeDef",
    "ActivateSubscriptionOutputTypeDef",
    "ArtifactDetailsTypeDef",
    "BlobTypeDef",
    "ChecklistItemTypeDef",
    "ChecklistTypeDef",
    "ClinicalNoteGenerationResultTypeDef",
    "ClinicalNoteGenerationSettingsResponseTypeDef",
    "ClinicalNoteGenerationSettingsTypeDef",
    "CreateDatasetInputTypeDef",
    "CreateDatasetOutputTypeDef",
    "CreateDomainInputTypeDef",
    "CreateDomainOutputTypeDef",
    "CreateSubscriptionInputTypeDef",
    "CreateSubscriptionOutputTypeDef",
    "CreateWebAppConfigurationTypeDef",
    "CustomTemplateResponseTypeDef",
    "CustomTemplateTypeDef",
    "DatasetArtifactsTypeDef",
    "DatasetConfigTypeDef",
    "DatasetSummaryTypeDef",
    "DeactivateSubscriptionInputTypeDef",
    "DeactivateSubscriptionOutputTypeDef",
    "DeleteDatasetInputTypeDef",
    "DeleteDatasetOutputTypeDef",
    "DeleteDomainInputTypeDef",
    "DeleteDomainOutputTypeDef",
    "DomainSummaryTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncounterContextTypeDef",
    "EncryptionContextTypeDef",
    "FHIRServerTypeDef",
    "GetDatasetInputTypeDef",
    "GetDatasetOutputTypeDef",
    "GetDomainInputTypeDef",
    "GetDomainOutputTypeDef",
    "GetMedicalCodingJobRequestTypeDef",
    "GetMedicalCodingJobResponseTypeDef",
    "GetMedicalScribeListeningSessionInputTypeDef",
    "GetMedicalScribeListeningSessionOutputTypeDef",
    "GetPatientInsightsJobRequestTypeDef",
    "GetPatientInsightsJobResponseTypeDef",
    "GetSubscriptionInputTypeDef",
    "GetSubscriptionOutputTypeDef",
    "InputDataConfigOutputTypeDef",
    "InputDataConfigTypeDef",
    "InputDataConfigUnionTypeDef",
    "InsightsContextTypeDef",
    "InsightsOutputTypeDef",
    "InternalServerExceptionTypeDef",
    "ListDatasetsInputPaginateTypeDef",
    "ListDatasetsInputTypeDef",
    "ListDatasetsOutputTypeDef",
    "ListDomainsInputPaginateTypeDef",
    "ListDomainsInputTypeDef",
    "ListDomainsOutputTypeDef",
    "ListSubscriptionsInputPaginateTypeDef",
    "ListSubscriptionsInputTypeDef",
    "ListSubscriptionsOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ManagedTemplateResponseTypeDef",
    "ManagedTemplateTypeDef",
    "MedicalCodeGenerationResultTypeDef",
    "MedicalCodeGenerationSettingsResponseTypeDef",
    "MedicalCodeGenerationSettingsTypeDef",
    "MedicalCodesEncounterContextTypeDef",
    "MedicalCodesPatientContextTypeDef",
    "MedicalCodingContextTypeDef",
    "MedicalCodingDatasetArtifactsTypeDef",
    "MedicalCodingDatasetConfigTypeDef",
    "MedicalCodingOutputDataConfigTypeDef",
    "MedicalCodingOutputTypeDef",
    "MedicalScribeAudioEventTypeDef",
    "MedicalScribeBinaryAudioEventTypeDef",
    "MedicalScribeChannelDefinitionTypeDef",
    "MedicalScribeChecklistEventTypeDef",
    "MedicalScribeConfigurationEventTypeDef",
    "MedicalScribeInputStreamTypeDef",
    "MedicalScribeListeningSessionDetailsTypeDef",
    "MedicalScribeOutputStreamTypeDef",
    "MedicalScribePeriodontalChartEventTypeDef",
    "MedicalScribePostStreamActionSettingsResponseTypeDef",
    "MedicalScribePostStreamActionSettingsTypeDef",
    "MedicalScribePostStreamActionsResultTypeDef",
    "MedicalScribeSessionControlEventTypeDef",
    "MedicalScribeTranscriptEventTypeDef",
    "MedicalScribeTranscriptSegmentTypeDef",
    "NoteTemplateSettingsResponseTypeDef",
    "NoteTemplateSettingsTypeDef",
    "OutputDataConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PatientInsightsEncounterContextTypeDef",
    "PatientInsightsPatientContextTypeDef",
    "PeriodontalReviewTypeDef",
    "PeriodontalSiteTypeDef",
    "PeriodontalToothTypeDef",
    "ResponseMetadataTypeDef",
    "S3SourceTypeDef",
    "StartMedicalCodingJobRequestTypeDef",
    "StartMedicalCodingJobResponseTypeDef",
    "StartMedicalScribeListeningSessionInputTypeDef",
    "StartMedicalScribeListeningSessionOutputTypeDef",
    "StartPatientInsightsJobRequestTypeDef",
    "StartPatientInsightsJobResponseTypeDef",
    "SubmitFeedbackRequestTypeDef",
    "SubscriptionDescriptionTypeDef",
    "TagResourceInputTypeDef",
    "TemplateSectionInstructionTypeDef",
    "UntagResourceInputTypeDef",
    "UserContextTypeDef",
    "ValidationExceptionTypeDef",
    "WebAppConfigurationTypeDef",
)

class ActivateSubscriptionInputTypeDef(TypedDict):
    domainId: str
    subscriptionId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class SubscriptionDescriptionTypeDef(TypedDict):
    domainId: str
    subscriptionId: str
    arn: str
    status: SubscriptionStatusType
    createdAt: datetime
    lastUpdatedAt: datetime
    activatedAt: NotRequired[datetime]
    deactivatedAt: NotRequired[datetime]

class ArtifactDetailsTypeDef(TypedDict):
    outputLocation: NotRequired[str]
    status: NotRequired[PostStreamArtifactGenerationStatusType]
    failureReason: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class ChecklistItemTypeDef(TypedDict):
    itemKey: str
    status: ChecklistItemStatusType

class CreateWebAppConfigurationTypeDef(TypedDict):
    ehrRole: str
    idcInstanceId: str
    idcRegion: str

class EncryptionContextTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    kmsKeyArn: NotRequired[str]

class WebAppConfigurationTypeDef(TypedDict):
    ehrRole: str
    idcApplicationId: str
    idcRegion: str

class CreateSubscriptionInputTypeDef(TypedDict):
    domainId: str

class CustomTemplateResponseTypeDef(TypedDict):
    templateType: NotRequired[CustomTemplateBaseType]

class TemplateSectionInstructionTypeDef(TypedDict):
    sectionHeader: str
    sectionInstruction: str

class MedicalCodingDatasetArtifactsTypeDef(TypedDict):
    evaluationS3Uri: NotRequired[str]

class MedicalCodingDatasetConfigTypeDef(TypedDict):
    s3InputPath: str
    s3OutputPath: str

DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "arn": str,
        "datasetId": str,
        "name": str,
        "type": Literal["MEDICAL_CODING"],
        "status": DatasetStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "statusDetails": NotRequired[str],
    },
)

class DeactivateSubscriptionInputTypeDef(TypedDict):
    domainId: str
    subscriptionId: str

class DeleteDatasetInputTypeDef(TypedDict):
    domainId: str
    datasetId: str

class DeleteDomainInputTypeDef(TypedDict):
    domainId: str

class DomainSummaryTypeDef(TypedDict):
    domainId: str
    arn: str
    name: str
    status: DomainStatusType
    createdAt: datetime

class MedicalCodingContextTypeDef(TypedDict):
    sex: NotRequired[SexType]
    status: NotRequired[PatientStatusType]
    dateOfBirth: NotRequired[str]
    encounterType: NotRequired[EncounterTypeType]
    encounterReason: NotRequired[str]
    afterHours: NotRequired[bool]
    encounterDate: NotRequired[str]

class FHIRServerTypeDef(TypedDict):
    fhirEndpoint: str
    oauthToken: NotRequired[str]

class GetDatasetInputTypeDef(TypedDict):
    domainId: str
    datasetId: str

class GetDomainInputTypeDef(TypedDict):
    domainId: str

class GetMedicalCodingJobRequestTypeDef(TypedDict):
    domainId: str
    jobId: str

class MedicalCodesEncounterContextTypeDef(TypedDict):
    encounterType: NotRequired[EncounterTypeType]
    encounterReason: NotRequired[str]
    afterHours: NotRequired[bool]
    encounterDate: NotRequired[str]
    encounterDurationMinutes: NotRequired[int]

class MedicalCodesPatientContextTypeDef(TypedDict):
    sex: NotRequired[SexType]
    status: NotRequired[PatientStatusType]
    dateOfBirth: NotRequired[str]
    insurance: NotRequired[str]

class MedicalCodingOutputDataConfigTypeDef(TypedDict):
    s3OutputPath: str

class MedicalCodingOutputTypeDef(TypedDict):
    uri: str

class GetMedicalScribeListeningSessionInputTypeDef(TypedDict):
    sessionId: str
    domainId: str
    subscriptionId: str

class GetPatientInsightsJobRequestTypeDef(TypedDict):
    domainId: str
    jobId: str

class InsightsContextTypeDef(TypedDict):
    insightsType: Literal["PRE_VISIT"]

class InsightsOutputTypeDef(TypedDict):
    uri: str

class OutputDataConfigTypeDef(TypedDict):
    s3OutputPath: str

class PatientInsightsEncounterContextTypeDef(TypedDict):
    encounterReason: str

class PatientInsightsPatientContextTypeDef(TypedDict):
    patientId: str
    dateOfBirth: NotRequired[str]
    pronouns: NotRequired[PronounsType]

class UserContextTypeDef(TypedDict):
    role: Literal["CLINICIAN"]
    userId: str
    specialty: NotRequired[Literal["PRIMARY_CARE"]]

class GetSubscriptionInputTypeDef(TypedDict):
    domainId: str
    subscriptionId: str

class S3SourceTypeDef(TypedDict):
    uri: str

class InternalServerExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

ListDatasetsInputTypeDef = TypedDict(
    "ListDatasetsInputTypeDef",
    {
        "domainId": str,
        "type": NotRequired[Literal["MEDICAL_CODING"]],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class ListDomainsInputTypeDef(TypedDict):
    status: NotRequired[DomainStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSubscriptionsInputTypeDef(TypedDict):
    domainId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str

class ManagedTemplateResponseTypeDef(TypedDict):
    templateType: NotRequired[ManagedNoteTemplateType]

class ManagedTemplateTypeDef(TypedDict):
    templateType: ManagedNoteTemplateType

class MedicalCodeGenerationSettingsResponseTypeDef(TypedDict):
    enabled: NotRequired[bool]

class MedicalCodeGenerationSettingsTypeDef(TypedDict):
    enabled: bool

class MedicalScribeChannelDefinitionTypeDef(TypedDict):
    channelId: int
    participantRole: MedicalScribeParticipantRoleType

MedicalScribeSessionControlEventTypeDef = TypedDict(
    "MedicalScribeSessionControlEventTypeDef",
    {
        "type": NotRequired[Literal["END_OF_SESSION"]],
    },
)

class ValidationExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class PeriodontalReviewTypeDef(TypedDict):
    reason: PeriodontalReviewReasonType
    toothNumber: NotRequired[int]
    sites: NotRequired[list[PeriodontalSiteNameType]]

class MedicalScribeTranscriptSegmentTypeDef(TypedDict):
    segmentId: NotRequired[str]
    audioBeginOffset: NotRequired[float]
    audioEndOffset: NotRequired[float]
    isPartial: NotRequired[bool]
    channelId: NotRequired[str]
    content: NotRequired[str]

class PeriodontalSiteTypeDef(TypedDict):
    site: PeriodontalSiteNameType
    probingDepth: NotRequired[int]
    recession: NotRequired[int]
    bleeding: NotRequired[bool]
    suppuration: NotRequired[bool]

class SubmitFeedbackRequestTypeDef(TypedDict):
    domainId: str
    artifactSourceId: str
    artifactType: FeedbackArtifactTypeType
    signedArtifactS3Uri: str
    subscriptionId: NotRequired[str]
    generatedArtifactS3Uri: NotRequired[str]
    comments: NotRequired[str]
    clientToken: NotRequired[str]

class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

CreateDatasetOutputTypeDef = TypedDict(
    "CreateDatasetOutputTypeDef",
    {
        "arn": str,
        "datasetId": str,
        "type": Literal["MEDICAL_CODING"],
        "status": DatasetStatusType,
        "createdAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateSubscriptionOutputTypeDef(TypedDict):
    domainId: str
    subscriptionId: str
    arn: str
    status: SubscriptionStatusType
    createdAt: datetime
    lastUpdatedAt: datetime
    activatedAt: datetime
    deactivatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDatasetOutputTypeDef(TypedDict):
    arn: str
    datasetId: str
    status: DatasetStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDomainOutputTypeDef(TypedDict):
    domainId: str
    arn: str
    status: DomainStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartMedicalCodingJobResponseTypeDef(TypedDict):
    jobArn: str
    jobId: str
    creationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StartPatientInsightsJobResponseTypeDef(TypedDict):
    jobArn: str
    jobId: str
    creationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ActivateSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeactivateSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSubscriptionsOutputTypeDef(TypedDict):
    subscriptions: list[SubscriptionDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ClinicalNoteGenerationResultTypeDef(TypedDict):
    noteResult: NotRequired[ArtifactDetailsTypeDef]
    transcriptResult: NotRequired[ArtifactDetailsTypeDef]
    afterVisitSummaryResult: NotRequired[ArtifactDetailsTypeDef]

class MedicalCodeGenerationResultTypeDef(TypedDict):
    medicalCodesResult: NotRequired[ArtifactDetailsTypeDef]
    jobId: NotRequired[str]

class MedicalScribeAudioEventTypeDef(TypedDict):
    audioChunk: BlobTypeDef

class MedicalScribeBinaryAudioEventTypeDef(TypedDict):
    audioChunk: BlobTypeDef

class ChecklistTypeDef(TypedDict):
    checklistId: str
    items: list[ChecklistItemTypeDef]

class CreateDomainInputTypeDef(TypedDict):
    name: str
    kmsKeyArn: NotRequired[str]
    webAppSetupConfiguration: NotRequired[CreateWebAppConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]

class CreateDomainOutputTypeDef(TypedDict):
    domainId: str
    arn: str
    name: str
    kmsKeyArn: str
    encryptionContext: EncryptionContextTypeDef
    status: DomainStatusType
    webAppUrl: str
    webAppConfiguration: WebAppConfigurationTypeDef
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetDomainOutputTypeDef(TypedDict):
    domainId: str
    arn: str
    name: str
    kmsKeyArn: str
    encryptionContext: EncryptionContextTypeDef
    status: DomainStatusType
    webAppUrl: str
    webAppConfiguration: WebAppConfigurationTypeDef
    createdAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CustomTemplateTypeDef(TypedDict):
    templateType: CustomTemplateBaseType
    templateInstructions: Sequence[TemplateSectionInstructionTypeDef]

class DatasetArtifactsTypeDef(TypedDict):
    medicalCoding: NotRequired[MedicalCodingDatasetArtifactsTypeDef]

class DatasetConfigTypeDef(TypedDict):
    medicalCoding: NotRequired[MedicalCodingDatasetConfigTypeDef]

class ListDatasetsOutputTypeDef(TypedDict):
    items: list[DatasetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDomainsOutputTypeDef(TypedDict):
    domains: list[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class EncounterContextTypeDef(TypedDict):
    unstructuredContext: NotRequired[str]
    medicalCodingContext: NotRequired[MedicalCodingContextTypeDef]

class StartMedicalCodingJobRequestTypeDef(TypedDict):
    domainId: str
    text: str
    outputDataConfig: MedicalCodingOutputDataConfigTypeDef
    patientContext: NotRequired[MedicalCodesPatientContextTypeDef]
    encounterContext: NotRequired[MedicalCodesEncounterContextTypeDef]
    datasetId: NotRequired[str]
    clientToken: NotRequired[str]

class GetMedicalCodingJobResponseTypeDef(TypedDict):
    jobId: str
    jobArn: str
    jobStatus: JobStatusType
    creationTime: datetime
    updatedTime: datetime
    text: str
    patientContext: MedicalCodesPatientContextTypeDef
    encounterContext: MedicalCodesEncounterContextTypeDef
    outputDataConfig: MedicalCodingOutputDataConfigTypeDef
    datasetId: str
    medicalCodingOutput: MedicalCodingOutputTypeDef
    statusDetails: str
    ResponseMetadata: ResponseMetadataTypeDef

class InputDataConfigOutputTypeDef(TypedDict):
    fhirServer: NotRequired[FHIRServerTypeDef]
    s3Sources: NotRequired[list[S3SourceTypeDef]]

class InputDataConfigTypeDef(TypedDict):
    fhirServer: NotRequired[FHIRServerTypeDef]
    s3Sources: NotRequired[Sequence[S3SourceTypeDef]]

ListDatasetsInputPaginateTypeDef = TypedDict(
    "ListDatasetsInputPaginateTypeDef",
    {
        "domainId": str,
        "type": NotRequired[Literal["MEDICAL_CODING"]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListDomainsInputPaginateTypeDef(TypedDict):
    status: NotRequired[DomainStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionsInputPaginateTypeDef(TypedDict):
    domainId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class NoteTemplateSettingsResponseTypeDef(TypedDict):
    managedTemplate: NotRequired[ManagedTemplateResponseTypeDef]
    customTemplate: NotRequired[CustomTemplateResponseTypeDef]

class MedicalScribeTranscriptEventTypeDef(TypedDict):
    transcriptSegment: NotRequired[MedicalScribeTranscriptSegmentTypeDef]

class PeriodontalToothTypeDef(TypedDict):
    toothNumber: int
    missing: bool
    mobility: NotRequired[int]
    furcation: NotRequired[int]
    sites: NotRequired[list[PeriodontalSiteTypeDef]]

class MedicalScribePostStreamActionsResultTypeDef(TypedDict):
    clinicalNoteGenerationResult: NotRequired[ClinicalNoteGenerationResultTypeDef]
    medicalCodeGenerationResult: NotRequired[MedicalCodeGenerationResultTypeDef]

class MedicalScribeChecklistEventTypeDef(TypedDict):
    snapshotVersion: int
    checklists: list[ChecklistTypeDef]

class NoteTemplateSettingsTypeDef(TypedDict):
    managedTemplate: NotRequired[ManagedTemplateTypeDef]
    customTemplate: NotRequired[CustomTemplateTypeDef]

class CreateDatasetInputTypeDef(TypedDict):
    domainId: str
    name: str
    config: DatasetConfigTypeDef
    clientToken: NotRequired[str]

GetDatasetOutputTypeDef = TypedDict(
    "GetDatasetOutputTypeDef",
    {
        "arn": str,
        "datasetId": str,
        "name": str,
        "type": Literal["MEDICAL_CODING"],
        "config": DatasetConfigTypeDef,
        "status": DatasetStatusType,
        "statusDetails": str,
        "artifacts": DatasetArtifactsTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetPatientInsightsJobResponseTypeDef(TypedDict):
    jobId: str
    jobArn: str
    jobStatus: JobStatusType
    creationTime: datetime
    updatedTime: datetime
    insightsOutput: InsightsOutputTypeDef
    statusDetails: str
    patientContext: PatientInsightsPatientContextTypeDef
    insightsContext: InsightsContextTypeDef
    encounterContext: PatientInsightsEncounterContextTypeDef
    userContext: UserContextTypeDef
    inputDataConfig: InputDataConfigOutputTypeDef
    outputDataConfig: OutputDataConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

InputDataConfigUnionTypeDef = Union[InputDataConfigTypeDef, InputDataConfigOutputTypeDef]

class ClinicalNoteGenerationSettingsResponseTypeDef(TypedDict):
    noteTemplateSettings: NotRequired[NoteTemplateSettingsResponseTypeDef]

class MedicalScribePeriodontalChartEventTypeDef(TypedDict):
    snapshotVersion: int
    teeth: list[PeriodontalToothTypeDef]
    reviewItems: NotRequired[list[PeriodontalReviewTypeDef]]

class ClinicalNoteGenerationSettingsTypeDef(TypedDict):
    noteTemplateSettings: NoteTemplateSettingsTypeDef

class StartPatientInsightsJobRequestTypeDef(TypedDict):
    domainId: str
    patientContext: PatientInsightsPatientContextTypeDef
    insightsContext: InsightsContextTypeDef
    encounterContext: PatientInsightsEncounterContextTypeDef
    userContext: UserContextTypeDef
    inputDataConfig: InputDataConfigUnionTypeDef
    outputDataConfig: OutputDataConfigTypeDef
    clientToken: NotRequired[str]

class MedicalScribePostStreamActionSettingsResponseTypeDef(TypedDict):
    outputS3Uri: str
    clinicalNoteGenerationSettings: ClinicalNoteGenerationSettingsResponseTypeDef
    medicalCodeGenerationSettings: NotRequired[MedicalCodeGenerationSettingsResponseTypeDef]

class MedicalScribeOutputStreamTypeDef(TypedDict):
    transcriptEvent: NotRequired[MedicalScribeTranscriptEventTypeDef]
    internalFailureException: NotRequired[InternalServerExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]
    periodontalChartEvent: NotRequired[MedicalScribePeriodontalChartEventTypeDef]
    checklistEvent: NotRequired[MedicalScribeChecklistEventTypeDef]

class MedicalScribePostStreamActionSettingsTypeDef(TypedDict):
    outputS3Uri: str
    clinicalNoteGenerationSettings: ClinicalNoteGenerationSettingsTypeDef
    medicalCodeGenerationSettings: NotRequired[MedicalCodeGenerationSettingsTypeDef]

class MedicalScribeListeningSessionDetailsTypeDef(TypedDict):
    sessionId: NotRequired[str]
    domainId: NotRequired[str]
    subscriptionId: NotRequired[str]
    languageCode: NotRequired[MedicalScribeLanguageCodeType]
    mediaSampleRateHertz: NotRequired[int]
    mediaEncoding: NotRequired[MedicalScribeMediaEncodingType]
    channelDefinitions: NotRequired[list[MedicalScribeChannelDefinitionTypeDef]]
    postStreamActionSettings: NotRequired[MedicalScribePostStreamActionSettingsResponseTypeDef]
    postStreamActionResult: NotRequired[MedicalScribePostStreamActionsResultTypeDef]
    encounterContextProvided: NotRequired[bool]
    medicalCodingContextProvided: NotRequired[bool]
    streamStatus: NotRequired[MedicalScribeStreamStatusType]
    streamCreationTime: NotRequired[datetime]
    streamEndTime: NotRequired[datetime]

class StartMedicalScribeListeningSessionOutputTypeDef(TypedDict):
    sessionId: str
    domainId: str
    subscriptionId: str
    requestId: str
    languageCode: MedicalScribeLanguageCodeType
    mediaSampleRateHertz: int
    mediaEncoding: MedicalScribeMediaEncodingType
    responseStream: EventStream[MedicalScribeOutputStreamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class MedicalScribeConfigurationEventTypeDef(TypedDict):
    postStreamActionSettings: MedicalScribePostStreamActionSettingsTypeDef
    channelDefinitions: NotRequired[Sequence[MedicalScribeChannelDefinitionTypeDef]]
    encounterContext: NotRequired[EncounterContextTypeDef]

class GetMedicalScribeListeningSessionOutputTypeDef(TypedDict):
    medicalScribeListeningSessionDetails: MedicalScribeListeningSessionDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class MedicalScribeInputStreamTypeDef(TypedDict):
    audioEvent: NotRequired[MedicalScribeAudioEventTypeDef]
    binaryAudioEvent: NotRequired[MedicalScribeBinaryAudioEventTypeDef]
    sessionControlEvent: NotRequired[MedicalScribeSessionControlEventTypeDef]
    configurationEvent: NotRequired[MedicalScribeConfigurationEventTypeDef]

class StartMedicalScribeListeningSessionInputTypeDef(TypedDict):
    sessionId: str
    domainId: str
    subscriptionId: str
    languageCode: MedicalScribeLanguageCodeType
    mediaSampleRateHertz: int
    mediaEncoding: MedicalScribeMediaEncodingType
    inputStream: NotRequired[EventStream[MedicalScribeInputStreamTypeDef]]
