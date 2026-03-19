"""
Type annotations for connecthealth service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_connecthealth.type_defs import ActivateSubscriptionInputTypeDef

    data: ActivateSubscriptionInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from aiobotocore.eventstream import AioEventStream
from aiobotocore.response import StreamingBody

from .literals import (
    CustomTemplateBaseType,
    DomainStatusType,
    EncryptionTypeType,
    JobStatusType,
    ManagedNoteTemplateType,
    MedicalScribeMediaEncodingType,
    MedicalScribeParticipantRoleType,
    MedicalScribeStreamStatusType,
    PostStreamArtifactGenerationStatusType,
    PronounsType,
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
    "ClinicalNoteGenerationResultTypeDef",
    "ClinicalNoteGenerationSettingsResponseTypeDef",
    "ClinicalNoteGenerationSettingsTypeDef",
    "CreateDomainInputTypeDef",
    "CreateDomainOutputTypeDef",
    "CreateSubscriptionInputTypeDef",
    "CreateSubscriptionOutputTypeDef",
    "CreateWebAppConfigurationTypeDef",
    "CustomTemplateResponseTypeDef",
    "CustomTemplateTypeDef",
    "DeactivateSubscriptionInputTypeDef",
    "DeactivateSubscriptionOutputTypeDef",
    "DeleteDomainInputTypeDef",
    "DeleteDomainOutputTypeDef",
    "DomainSummaryTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncounterContextTypeDef",
    "EncryptionContextTypeDef",
    "FHIRServerTypeDef",
    "GetDomainInputTypeDef",
    "GetDomainOutputTypeDef",
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
    "MedicalScribeAudioEventTypeDef",
    "MedicalScribeChannelDefinitionTypeDef",
    "MedicalScribeConfigurationEventTypeDef",
    "MedicalScribeInputStreamTypeDef",
    "MedicalScribeListeningSessionDetailsTypeDef",
    "MedicalScribeOutputStreamTypeDef",
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
    "ResponseMetadataTypeDef",
    "S3SourceTypeDef",
    "StartMedicalScribeListeningSessionInputTypeDef",
    "StartMedicalScribeListeningSessionOutputTypeDef",
    "StartPatientInsightsJobRequestTypeDef",
    "StartPatientInsightsJobResponseTypeDef",
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

class DeactivateSubscriptionInputTypeDef(TypedDict):
    domainId: str
    subscriptionId: str

class DeleteDomainInputTypeDef(TypedDict):
    domainId: str

class DomainSummaryTypeDef(TypedDict):
    domainId: str
    arn: str
    name: str
    status: DomainStatusType
    createdAt: datetime

class EncounterContextTypeDef(TypedDict):
    unstructuredContext: NotRequired[str]

class FHIRServerTypeDef(TypedDict):
    fhirEndpoint: str
    oauthToken: NotRequired[str]

class GetDomainInputTypeDef(TypedDict):
    domainId: str

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

class MedicalScribeTranscriptSegmentTypeDef(TypedDict):
    segmentId: NotRequired[str]
    audioBeginOffset: NotRequired[float]
    audioEndOffset: NotRequired[float]
    isPartial: NotRequired[bool]
    channelId: NotRequired[str]
    content: NotRequired[str]

class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

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

class MedicalScribeAudioEventTypeDef(TypedDict):
    audioChunk: BlobTypeDef

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

class ListDomainsOutputTypeDef(TypedDict):
    domains: list[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class InputDataConfigOutputTypeDef(TypedDict):
    fhirServer: NotRequired[FHIRServerTypeDef]
    s3Sources: NotRequired[list[S3SourceTypeDef]]

class InputDataConfigTypeDef(TypedDict):
    fhirServer: NotRequired[FHIRServerTypeDef]
    s3Sources: NotRequired[Sequence[S3SourceTypeDef]]

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

class MedicalScribePostStreamActionsResultTypeDef(TypedDict):
    clinicalNoteGenerationResult: NotRequired[ClinicalNoteGenerationResultTypeDef]

class NoteTemplateSettingsTypeDef(TypedDict):
    managedTemplate: NotRequired[ManagedTemplateTypeDef]
    customTemplate: NotRequired[CustomTemplateTypeDef]

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

class MedicalScribeOutputStreamTypeDef(TypedDict):
    transcriptEvent: NotRequired[MedicalScribeTranscriptEventTypeDef]
    internalFailureException: NotRequired[InternalServerExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]

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

class StartMedicalScribeListeningSessionOutputTypeDef(TypedDict):
    sessionId: str
    domainId: str
    subscriptionId: str
    requestId: str
    languageCode: Literal["en-US"]
    mediaSampleRateHertz: int
    mediaEncoding: MedicalScribeMediaEncodingType
    responseStream: AioEventStream[MedicalScribeOutputStreamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class MedicalScribePostStreamActionSettingsTypeDef(TypedDict):
    outputS3Uri: str
    clinicalNoteGenerationSettings: ClinicalNoteGenerationSettingsTypeDef

class MedicalScribeListeningSessionDetailsTypeDef(TypedDict):
    sessionId: NotRequired[str]
    domainId: NotRequired[str]
    subscriptionId: NotRequired[str]
    languageCode: NotRequired[Literal["en-US"]]
    mediaSampleRateHertz: NotRequired[int]
    mediaEncoding: NotRequired[MedicalScribeMediaEncodingType]
    channelDefinitions: NotRequired[list[MedicalScribeChannelDefinitionTypeDef]]
    postStreamActionSettings: NotRequired[MedicalScribePostStreamActionSettingsResponseTypeDef]
    postStreamActionResult: NotRequired[MedicalScribePostStreamActionsResultTypeDef]
    encounterContextProvided: NotRequired[bool]
    streamStatus: NotRequired[MedicalScribeStreamStatusType]
    streamCreationTime: NotRequired[datetime]
    streamEndTime: NotRequired[datetime]

class MedicalScribeConfigurationEventTypeDef(TypedDict):
    postStreamActionSettings: MedicalScribePostStreamActionSettingsTypeDef
    channelDefinitions: NotRequired[Sequence[MedicalScribeChannelDefinitionTypeDef]]
    encounterContext: NotRequired[EncounterContextTypeDef]

class GetMedicalScribeListeningSessionOutputTypeDef(TypedDict):
    medicalScribeListeningSessionDetails: MedicalScribeListeningSessionDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class MedicalScribeInputStreamTypeDef(TypedDict):
    audioEvent: NotRequired[MedicalScribeAudioEventTypeDef]
    sessionControlEvent: NotRequired[MedicalScribeSessionControlEventTypeDef]
    configurationEvent: NotRequired[MedicalScribeConfigurationEventTypeDef]

class StartMedicalScribeListeningSessionInputTypeDef(TypedDict):
    sessionId: str
    domainId: str
    subscriptionId: str
    languageCode: Literal["en-US"]
    mediaSampleRateHertz: int
    mediaEncoding: MedicalScribeMediaEncodingType
    inputStream: NotRequired[AioEventStream[MedicalScribeInputStreamTypeDef]]
