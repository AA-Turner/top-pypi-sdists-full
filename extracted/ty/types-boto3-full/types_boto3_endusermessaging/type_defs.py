"""
Type annotations for endusermessaging service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_endusermessaging.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    BrandProfileAttributeTypeType,
    CodeTypeType,
    JobResourceTypeType,
    JobStatusType,
    NotifyChannelType,
    OnAttributeConflictType,
    StatusType,
    VerificationStatusType,
    VoiceMessageBodyTextTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "BlobTypeDef",
    "BrandProfileAttributeInputTypeDef",
    "BrandProfileAttributeOutputTypeDef",
    "BrandProfileAttributeSummaryTypeDef",
    "BrandProfileInfoTypeDef",
    "ChannelParametersOutputTypeDef",
    "ChannelParametersTypeDef",
    "ChannelParametersUnionTypeDef",
    "CodeConfigurationParametersTypeDef",
    "CreateBrandProfileAttributesInputTypeDef",
    "CreateBrandProfileAttributesOutputTypeDef",
    "CreateBrandProfileFromRegistrationInputTypeDef",
    "CreateBrandProfileFromRegistrationOutputTypeDef",
    "CreateBrandProfileInputTypeDef",
    "CreateBrandProfileOutputTypeDef",
    "CreateNotifyCodeConfigurationInputTypeDef",
    "CreateNotifyCodeConfigurationOutputTypeDef",
    "CreateRegistrationsFromBrandProfileInputTypeDef",
    "CreateRegistrationsFromBrandProfileOutputTypeDef",
    "DeleteBrandProfileAttributeInputTypeDef",
    "DeleteBrandProfileAttributeOutputTypeDef",
    "DeleteBrandProfileInputTypeDef",
    "DeleteBrandProfileOutputTypeDef",
    "DeleteNotifyCodeConfigurationInputTypeDef",
    "GetBrandProfileAttributeInputTypeDef",
    "GetBrandProfileAttributeOutputTypeDef",
    "GetBrandProfileInputTypeDef",
    "GetBrandProfileInputWaitTypeDef",
    "GetBrandProfileOutputTypeDef",
    "GetJobInputTypeDef",
    "GetJobInputWaitTypeDef",
    "GetNotifyCodeConfigurationInputTypeDef",
    "GetNotifyCodeConfigurationOutputTypeDef",
    "JobResourceTypeDef",
    "JobResultTypeDef",
    "JobSummaryTypeDef",
    "JobTypeDef",
    "ListBrandProfileAttributesInputPaginateTypeDef",
    "ListBrandProfileAttributesInputTypeDef",
    "ListBrandProfileAttributesOutputTypeDef",
    "ListBrandProfilesInputPaginateTypeDef",
    "ListBrandProfilesInputTypeDef",
    "ListBrandProfilesOutputTypeDef",
    "ListJobsInputPaginateTypeDef",
    "ListJobsInputTypeDef",
    "ListJobsOutputTypeDef",
    "ListNotifyCodeConfigurationsInputPaginateTypeDef",
    "ListNotifyCodeConfigurationsInputTypeDef",
    "ListNotifyCodeConfigurationsOutputTypeDef",
    "ListRegistrationsFromBrandProfileInputPaginateTypeDef",
    "ListRegistrationsFromBrandProfileInputTypeDef",
    "ListRegistrationsFromBrandProfileOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "NotifyCodeConfigurationTypeDef",
    "NotifyParametersTypeDef",
    "PaginatorConfigTypeDef",
    "RegistrationAssociationSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "SendNotifyCodeVerificationInputTypeDef",
    "SendNotifyCodeVerificationOutputTypeDef",
    "TagResourceInputTypeDef",
    "TagTypeDef",
    "TextParametersOutputTypeDef",
    "TextParametersTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateBrandProfileAttributeInputTypeDef",
    "UpdateBrandProfileAttributeOutputTypeDef",
    "UpdateBrandProfileFromRegistrationInputTypeDef",
    "UpdateBrandProfileFromRegistrationOutputTypeDef",
    "UpdateBrandProfileInputTypeDef",
    "UpdateBrandProfileOutputTypeDef",
    "UpdateChannelParametersTypeDef",
    "UpdateCodeConfigurationParametersTypeDef",
    "UpdateNotifyCodeConfigurationInputTypeDef",
    "UpdateNotifyCodeConfigurationOutputTypeDef",
    "UpdateNotifyParametersTypeDef",
    "UpdateRegistrationsFromBrandProfileInputTypeDef",
    "UpdateRegistrationsFromBrandProfileOutputTypeDef",
    "UpdateTextParametersTypeDef",
    "UpdateVoiceParametersTypeDef",
    "UpdateWhatsAppParametersTypeDef",
    "ValidateNotifyCodeVerificationInputTypeDef",
    "ValidateNotifyCodeVerificationOutputTypeDef",
    "VoiceParametersTypeDef",
    "WaiterConfigTypeDef",
    "WhatsAppParametersTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class BrandProfileAttributeOutputTypeDef(TypedDict):
    attributeName: str
    attributeType: BrandProfileAttributeTypeType
    mediaDownloadUrl: NotRequired[str]


class BrandProfileAttributeSummaryTypeDef(TypedDict):
    attributeName: str
    attributeType: BrandProfileAttributeTypeType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    category: NotRequired[str]


class BrandProfileInfoTypeDef(TypedDict):
    brandProfileId: str
    brandProfileArn: str
    brandProfileName: str
    status: StatusType
    deletionProtectionEnabled: bool
    createdAt: datetime
    updatedAt: datetime


class NotifyParametersTypeDef(TypedDict):
    notifyTemplateId: NotRequired[str]
    voiceId: NotRequired[str]


class TextParametersOutputTypeDef(TypedDict):
    inlineTemplateBody: NotRequired[str]
    destinationCountryParameters: NotRequired[dict[str, str]]


class VoiceParametersTypeDef(TypedDict):
    inlineTemplateBody: NotRequired[str]
    languageCode: NotRequired[str]
    voiceId: NotRequired[str]
    voiceMessageBodyTextType: NotRequired[VoiceMessageBodyTextTypeType]


class WhatsAppParametersTypeDef(TypedDict):
    whatsAppTemplateName: NotRequired[str]
    languageCode: NotRequired[str]


class TextParametersTypeDef(TypedDict):
    inlineTemplateBody: NotRequired[str]
    destinationCountryParameters: NotRequired[Mapping[str, str]]


class CodeConfigurationParametersTypeDef(TypedDict):
    codeType: NotRequired[CodeTypeType]
    codeLength: NotRequired[int]
    validityPeriodMinutes: NotRequired[int]
    maxAttempts: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class TagTypeDef(TypedDict):
    key: str
    value: str


class JobResultTypeDef(TypedDict):
    jobId: str
    resourceIdentifier: str


class CreateRegistrationsFromBrandProfileInputTypeDef(TypedDict):
    brandProfileId: str
    registrationTypes: Sequence[str]
    smartMatch: NotRequired[bool]
    clientToken: NotRequired[str]


class DeleteBrandProfileAttributeInputTypeDef(TypedDict):
    brandProfileId: str
    attributeName: str


class DeleteBrandProfileInputTypeDef(TypedDict):
    brandProfileId: str


class DeleteNotifyCodeConfigurationInputTypeDef(TypedDict):
    notifyCodeConfigurationId: str


class GetBrandProfileAttributeInputTypeDef(TypedDict):
    brandProfileId: str
    attributeName: str


class GetBrandProfileInputTypeDef(TypedDict):
    brandProfileId: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class GetJobInputTypeDef(TypedDict):
    jobId: str


class GetNotifyCodeConfigurationInputTypeDef(TypedDict):
    notifyCodeConfigurationId: str


class JobResourceTypeDef(TypedDict):
    resourceType: JobResourceTypeType
    resourceId: str
    resourceArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListBrandProfileAttributesInputTypeDef(TypedDict):
    brandProfileId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBrandProfilesInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListJobsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[JobStatusType]
    brandProfileId: NotRequired[str]
    operationType: NotRequired[str]


class ListNotifyCodeConfigurationsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListRegistrationsFromBrandProfileInputTypeDef(TypedDict):
    brandProfileId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class RegistrationAssociationSummaryTypeDef(TypedDict):
    registrationId: str
    registrationType: str
    createdAt: datetime
    smartMatchUsed: bool


class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str


class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateBrandProfileFromRegistrationInputTypeDef(TypedDict):
    brandProfileId: str
    registrationId: str
    smartMatch: NotRequired[bool]
    onAttributeConflict: NotRequired[OnAttributeConflictType]
    clientToken: NotRequired[str]


class UpdateBrandProfileInputTypeDef(TypedDict):
    brandProfileId: str
    brandProfileName: NotRequired[str]
    deletionProtectionEnabled: NotRequired[bool]


class UpdateNotifyParametersTypeDef(TypedDict):
    notifyTemplateId: NotRequired[str]
    voiceId: NotRequired[str]


class UpdateTextParametersTypeDef(TypedDict):
    inlineTemplateBody: NotRequired[str]
    destinationCountryParameters: NotRequired[Mapping[str, str]]


class UpdateVoiceParametersTypeDef(TypedDict):
    inlineTemplateBody: NotRequired[str]
    languageCode: NotRequired[str]
    voiceId: NotRequired[str]
    voiceMessageBodyTextType: NotRequired[VoiceMessageBodyTextTypeType]


class UpdateWhatsAppParametersTypeDef(TypedDict):
    whatsAppTemplateName: NotRequired[str]
    languageCode: NotRequired[str]


class UpdateCodeConfigurationParametersTypeDef(TypedDict):
    codeType: NotRequired[CodeTypeType]
    codeLength: NotRequired[int]
    validityPeriodMinutes: NotRequired[int]
    maxAttempts: NotRequired[int]


class UpdateRegistrationsFromBrandProfileInputTypeDef(TypedDict):
    brandProfileId: str
    registrationIds: Sequence[str]
    smartMatch: NotRequired[bool]
    onAttributeConflict: NotRequired[OnAttributeConflictType]
    clientToken: NotRequired[str]


class ValidateNotifyCodeVerificationInputTypeDef(TypedDict):
    destinationIdentity: str
    code: str
    referenceId: NotRequired[str]


class BrandProfileAttributeInputTypeDef(TypedDict):
    attributeName: str
    attributeType: BrandProfileAttributeTypeType
    attributeValue: NotRequired[str]
    attachmentBody: NotRequired[BlobTypeDef]
    description: NotRequired[str]
    category: NotRequired[str]


class UpdateBrandProfileAttributeInputTypeDef(TypedDict):
    brandProfileId: str
    attributeName: str
    attributeValue: NotRequired[str]
    attachmentBody: NotRequired[BlobTypeDef]
    description: NotRequired[str]
    category: NotRequired[str]


class ChannelParametersOutputTypeDef(TypedDict):
    text: NotRequired[TextParametersOutputTypeDef]
    voice: NotRequired[VoiceParametersTypeDef]
    notify: NotRequired[NotifyParametersTypeDef]
    whatsApp: NotRequired[WhatsAppParametersTypeDef]


class ChannelParametersTypeDef(TypedDict):
    text: NotRequired[TextParametersTypeDef]
    voice: NotRequired[VoiceParametersTypeDef]
    notify: NotRequired[NotifyParametersTypeDef]
    whatsApp: NotRequired[WhatsAppParametersTypeDef]


class CreateBrandProfileAttributesOutputTypeDef(TypedDict):
    attributes: list[BrandProfileAttributeOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBrandProfileOutputTypeDef(TypedDict):
    brandProfileId: str
    brandProfileArn: str
    brandProfileName: str
    status: StatusType
    deletionProtectionEnabled: bool
    createdAt: datetime
    updatedAt: datetime
    attributesCreated: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBrandProfileAttributeOutputTypeDef(TypedDict):
    brandProfileId: str
    attributeName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBrandProfileOutputTypeDef(TypedDict):
    brandProfileId: str
    brandProfileArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetBrandProfileAttributeOutputTypeDef(TypedDict):
    attributeName: str
    attributeType: BrandProfileAttributeTypeType
    attributeValue: str
    description: str
    category: str
    mediaContentType: str
    mediaSizeBytes: int
    mediaDownloadUrl: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetBrandProfileOutputTypeDef(TypedDict):
    brandProfileId: str
    brandProfileArn: str
    brandProfileName: str
    status: StatusType
    deletionProtectionEnabled: bool
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListBrandProfileAttributesOutputTypeDef(TypedDict):
    brandProfileAttributes: list[BrandProfileAttributeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBrandProfilesOutputTypeDef(TypedDict):
    brandProfiles: list[BrandProfileInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SendNotifyCodeVerificationOutputTypeDef(TypedDict):
    verificationId: str
    messageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrandProfileAttributeOutputTypeDef(TypedDict):
    attributeName: str
    attributeType: BrandProfileAttributeTypeType
    attributeValue: str
    description: str
    category: str
    mediaContentType: str
    mediaSizeBytes: int
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrandProfileOutputTypeDef(TypedDict):
    brandProfileId: str
    brandProfileArn: str
    brandProfileName: str
    status: StatusType
    deletionProtectionEnabled: bool
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ValidateNotifyCodeVerificationOutputTypeDef(TypedDict):
    status: VerificationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBrandProfileFromRegistrationInputTypeDef(TypedDict):
    registrationId: str
    brandProfileName: str
    smartMatch: NotRequired[bool]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientToken: NotRequired[str]


class CreateBrandProfileInputTypeDef(TypedDict):
    brandProfileName: str
    clientToken: NotRequired[str]
    deletionProtectionEnabled: NotRequired[bool]
    tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class CreateBrandProfileFromRegistrationOutputTypeDef(TypedDict):
    results: list[JobResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRegistrationsFromBrandProfileOutputTypeDef(TypedDict):
    results: list[JobResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrandProfileFromRegistrationOutputTypeDef(TypedDict):
    results: list[JobResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRegistrationsFromBrandProfileOutputTypeDef(TypedDict):
    results: list[JobResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetBrandProfileInputWaitTypeDef(TypedDict):
    brandProfileId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetJobInputWaitTypeDef(TypedDict):
    jobId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class JobSummaryTypeDef(TypedDict):
    jobId: str
    status: JobStatusType
    operationType: str
    createdAt: datetime
    updatedAt: datetime
    brandProfileId: NotRequired[str]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]
    resources: NotRequired[list[JobResourceTypeDef]]


class JobTypeDef(TypedDict):
    jobId: str
    status: JobStatusType
    operationType: str
    createdAt: datetime
    updatedAt: datetime
    brandProfileId: str
    errorCode: str
    errorMessage: str
    resources: list[JobResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListBrandProfileAttributesInputPaginateTypeDef(TypedDict):
    brandProfileId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBrandProfilesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJobsInputPaginateTypeDef(TypedDict):
    status: NotRequired[JobStatusType]
    brandProfileId: NotRequired[str]
    operationType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNotifyCodeConfigurationsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRegistrationsFromBrandProfileInputPaginateTypeDef(TypedDict):
    brandProfileId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRegistrationsFromBrandProfileOutputTypeDef(TypedDict):
    registrationAssociations: list[RegistrationAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateChannelParametersTypeDef(TypedDict):
    text: NotRequired[UpdateTextParametersTypeDef]
    voice: NotRequired[UpdateVoiceParametersTypeDef]
    notify: NotRequired[UpdateNotifyParametersTypeDef]
    whatsApp: NotRequired[UpdateWhatsAppParametersTypeDef]


class CreateBrandProfileAttributesInputTypeDef(TypedDict):
    brandProfileId: str
    attributes: Sequence[BrandProfileAttributeInputTypeDef]
    clientToken: NotRequired[str]


class NotifyCodeConfigurationTypeDef(TypedDict):
    notifyCodeConfigurationId: str
    notifyCodeConfigurationArn: str
    notifyCodeConfigurationName: str
    deletionProtectionEnabled: bool
    createdAt: datetime
    updatedAt: datetime
    codeConfigurationParameters: NotRequired[CodeConfigurationParametersTypeDef]
    channelParameters: NotRequired[ChannelParametersOutputTypeDef]


ChannelParametersUnionTypeDef = Union[ChannelParametersTypeDef, ChannelParametersOutputTypeDef]


class ListJobsOutputTypeDef(TypedDict):
    jobs: list[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateNotifyCodeConfigurationInputTypeDef(TypedDict):
    notifyCodeConfigurationId: str
    notifyCodeConfigurationName: NotRequired[str]
    codeConfigurationParameters: NotRequired[UpdateCodeConfigurationParametersTypeDef]
    channelParameters: NotRequired[UpdateChannelParametersTypeDef]
    deletionProtectionEnabled: NotRequired[bool]


class CreateNotifyCodeConfigurationOutputTypeDef(TypedDict):
    notifyCodeConfiguration: NotifyCodeConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetNotifyCodeConfigurationOutputTypeDef(TypedDict):
    notifyCodeConfiguration: NotifyCodeConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListNotifyCodeConfigurationsOutputTypeDef(TypedDict):
    notifyCodeConfigurations: list[NotifyCodeConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateNotifyCodeConfigurationOutputTypeDef(TypedDict):
    notifyCodeConfiguration: NotifyCodeConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNotifyCodeConfigurationInputTypeDef(TypedDict):
    notifyCodeConfigurationName: str
    codeConfigurationParameters: NotRequired[CodeConfigurationParametersTypeDef]
    channelParameters: NotRequired[ChannelParametersUnionTypeDef]
    deletionProtectionEnabled: NotRequired[bool]
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class SendNotifyCodeVerificationInputTypeDef(TypedDict):
    channel: NotifyChannelType
    destinationIdentity: str
    originationIdentity: str
    notifyCodeConfiguration: NotRequired[str]
    overrideChannelParameters: NotRequired[ChannelParametersUnionTypeDef]
    overrideCodeConfigurationParameters: NotRequired[CodeConfigurationParametersTypeDef]
    configurationSetName: NotRequired[str]
    context: NotRequired[Mapping[str, str]]
    referenceId: NotRequired[str]
