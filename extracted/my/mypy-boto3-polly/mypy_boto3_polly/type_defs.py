"""
Type annotations for polly service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_polly.type_defs import AudioEventTypeDef

    data: AudioEventTypeDef = ...
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
    AudioFormatType,
    CustomVoiceLanguageCodeType,
    EngineType,
    GenderType,
    LanguageCodeType,
    OutputFormatType,
    QuotaCodeType,
    SpeechMarkTypeType,
    TaskStatusType,
    TextTypeType,
    ValidationExceptionReasonType,
    VoiceIdType,
    VoiceOriginType,
    VoiceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AudioEventTypeDef",
    "BlobTypeDef",
    "CreateVoiceInputTypeDef",
    "CreateVoiceOutputTypeDef",
    "CustomerManagedEncryptionOutputTypeDef",
    "CustomerManagedEncryptionTypeDef",
    "CustomerManagedEncryptionUnionTypeDef",
    "DeleteLexiconInputTypeDef",
    "DeleteVoiceInputTypeDef",
    "DescribeVoicesInputPaginateTypeDef",
    "DescribeVoicesInputTypeDef",
    "DescribeVoicesOutputTypeDef",
    "FlushStreamConfigurationTypeDef",
    "GetLexiconInputTypeDef",
    "GetLexiconOutputTypeDef",
    "GetSpeechSynthesisTaskInputTypeDef",
    "GetSpeechSynthesisTaskOutputTypeDef",
    "GetVoiceInputTypeDef",
    "GetVoiceInputWaitTypeDef",
    "GetVoiceOutputTypeDef",
    "LexiconAttributesTypeDef",
    "LexiconDescriptionTypeDef",
    "LexiconTypeDef",
    "ListLexiconsInputPaginateTypeDef",
    "ListLexiconsInputTypeDef",
    "ListLexiconsOutputTypeDef",
    "ListSpeechSynthesisTasksInputPaginateTypeDef",
    "ListSpeechSynthesisTasksInputTypeDef",
    "ListSpeechSynthesisTasksOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PutLexiconInputTypeDef",
    "RecordingDataOutputTypeDef",
    "RecordingDataTypeDef",
    "RecordingOutputTypeDef",
    "RecordingTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceFailureExceptionTypeDef",
    "ServiceQuotaExceededExceptionTypeDef",
    "StartSpeechSynthesisStreamActionStreamTypeDef",
    "StartSpeechSynthesisStreamEventStreamTypeDef",
    "StartSpeechSynthesisStreamInputTypeDef",
    "StartSpeechSynthesisStreamOutputTypeDef",
    "StartSpeechSynthesisTaskInputTypeDef",
    "StartSpeechSynthesisTaskOutputTypeDef",
    "StreamClosedEventTypeDef",
    "SynthesisTaskTypeDef",
    "SynthesizeSpeechInputTypeDef",
    "SynthesizeSpeechOutputTypeDef",
    "TagResourceInputTypeDef",
    "TextEventTypeDef",
    "ThrottlingExceptionTypeDef",
    "ThrottlingReasonTypeDef",
    "UntagResourceInputTypeDef",
    "ValidationExceptionFieldTypeDef",
    "ValidationExceptionTypeDef",
    "VoiceCreationDataOutputTypeDef",
    "VoiceCreationDataTypeDef",
    "VoiceCreationDataUnionTypeDef",
    "VoiceTypeDef",
    "WaiterConfigTypeDef",
)


class AudioEventTypeDef(TypedDict):
    AudioChunk: NotRequired[bytes]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CustomerManagedEncryptionOutputTypeDef(TypedDict):
    KmsKeyArn: str
    EncryptionContext: NotRequired[dict[str, str]]


class CustomerManagedEncryptionTypeDef(TypedDict):
    KmsKeyArn: str
    EncryptionContext: NotRequired[Mapping[str, str]]


class DeleteLexiconInputTypeDef(TypedDict):
    Name: str


class DeleteVoiceInputTypeDef(TypedDict):
    VoiceId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeVoicesInputTypeDef(TypedDict):
    Engine: NotRequired[EngineType]
    LanguageCode: NotRequired[LanguageCodeType]
    IncludeAdditionalLanguageCodes: NotRequired[bool]
    NextToken: NotRequired[str]


class FlushStreamConfigurationTypeDef(TypedDict):
    Force: NotRequired[bool]


class GetLexiconInputTypeDef(TypedDict):
    Name: str


class LexiconAttributesTypeDef(TypedDict):
    Alphabet: NotRequired[str]
    LanguageCode: NotRequired[LanguageCodeType]
    LastModified: NotRequired[datetime]
    LexiconArn: NotRequired[str]
    LexemesCount: NotRequired[int]
    Size: NotRequired[int]


class LexiconTypeDef(TypedDict):
    Content: NotRequired[str]
    Name: NotRequired[str]


class GetSpeechSynthesisTaskInputTypeDef(TypedDict):
    TaskId: str


class SynthesisTaskTypeDef(TypedDict):
    Engine: NotRequired[EngineType]
    TaskId: NotRequired[str]
    TaskStatus: NotRequired[TaskStatusType]
    TaskStatusReason: NotRequired[str]
    OutputUri: NotRequired[str]
    CreationTime: NotRequired[datetime]
    RequestCharacters: NotRequired[int]
    SnsTopicArn: NotRequired[str]
    LexiconNames: NotRequired[list[str]]
    OutputFormat: NotRequired[OutputFormatType]
    SampleRate: NotRequired[str]
    SpeechMarkTypes: NotRequired[list[SpeechMarkTypeType]]
    TextType: NotRequired[TextTypeType]
    VoiceId: NotRequired[VoiceIdType]
    LanguageCode: NotRequired[LanguageCodeType]


class GetVoiceInputTypeDef(TypedDict):
    VoiceId: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class ListLexiconsInputTypeDef(TypedDict):
    NextToken: NotRequired[str]


class ListSpeechSynthesisTasksInputTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Status: NotRequired[TaskStatusType]


class ListTagsForResourceInputTypeDef(TypedDict):
    ResourceArn: str


class PutLexiconInputTypeDef(TypedDict):
    Name: str
    Content: str
    Tags: NotRequired[Mapping[str, str]]


class RecordingDataOutputTypeDef(TypedDict):
    S3Url: NotRequired[str]
    Bytes: NotRequired[bytes]


class ServiceFailureExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ServiceQuotaExceededExceptionTypeDef(TypedDict):
    message: str
    quotaCode: QuotaCodeType
    serviceCode: Literal["polly"]


class StreamClosedEventTypeDef(TypedDict):
    RequestCharacters: NotRequired[int]


StartSpeechSynthesisTaskInputTypeDef = TypedDict(
    "StartSpeechSynthesisTaskInputTypeDef",
    {
        "OutputFormat": OutputFormatType,
        "OutputS3BucketName": str,
        "Text": str,
        "VoiceId": VoiceIdType,
        "Engine": NotRequired[EngineType],
        "LanguageCode": NotRequired[LanguageCodeType],
        "LexiconNames": NotRequired[Sequence[str]],
        "OutputS3KeyPrefix": NotRequired[str],
        "SampleRate": NotRequired[str],
        "SnsTopicArn": NotRequired[str],
        "SpeechMarkTypes": NotRequired[Sequence[SpeechMarkTypeType]],
        "TextType": NotRequired[TextTypeType],
    },
)
SynthesizeSpeechInputTypeDef = TypedDict(
    "SynthesizeSpeechInputTypeDef",
    {
        "OutputFormat": OutputFormatType,
        "Text": str,
        "VoiceId": VoiceIdType,
        "Engine": NotRequired[EngineType],
        "LanguageCode": NotRequired[LanguageCodeType],
        "LexiconNames": NotRequired[Sequence[str]],
        "SampleRate": NotRequired[str],
        "SpeechMarkTypes": NotRequired[Sequence[SpeechMarkTypeType]],
        "TextType": NotRequired[TextTypeType],
    },
)


class TagResourceInputTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class ThrottlingReasonTypeDef(TypedDict):
    reason: NotRequired[str]
    resource: NotRequired[str]


class UntagResourceInputTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class ValidationExceptionFieldTypeDef(TypedDict):
    name: str
    message: str


class RecordingDataTypeDef(TypedDict):
    S3Url: NotRequired[str]
    Bytes: NotRequired[BlobTypeDef]


class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class SynthesizeSpeechOutputTypeDef(TypedDict):
    AudioStream: StreamingBody
    ContentType: str
    RequestCharacters: int
    ResponseMetadata: ResponseMetadataTypeDef


CustomerManagedEncryptionUnionTypeDef = Union[
    CustomerManagedEncryptionTypeDef, CustomerManagedEncryptionOutputTypeDef
]


class DescribeVoicesInputPaginateTypeDef(TypedDict):
    Engine: NotRequired[EngineType]
    LanguageCode: NotRequired[LanguageCodeType]
    IncludeAdditionalLanguageCodes: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLexiconsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSpeechSynthesisTasksInputPaginateTypeDef(TypedDict):
    Status: NotRequired[TaskStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


TextEventTypeDef = TypedDict(
    "TextEventTypeDef",
    {
        "Text": str,
        "TextType": NotRequired[TextTypeType],
        "FlushStreamConfiguration": NotRequired[FlushStreamConfigurationTypeDef],
    },
)


class LexiconDescriptionTypeDef(TypedDict):
    Name: NotRequired[str]
    Attributes: NotRequired[LexiconAttributesTypeDef]


class GetLexiconOutputTypeDef(TypedDict):
    Lexicon: LexiconTypeDef
    LexiconAttributes: LexiconAttributesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSpeechSynthesisTaskOutputTypeDef(TypedDict):
    SynthesisTask: SynthesisTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListSpeechSynthesisTasksOutputTypeDef(TypedDict):
    SynthesisTasks: list[SynthesisTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartSpeechSynthesisTaskOutputTypeDef(TypedDict):
    SynthesisTask: SynthesisTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetVoiceInputWaitTypeDef(TypedDict):
    VoiceId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class RecordingOutputTypeDef(TypedDict):
    Format: AudioFormatType
    Data: RecordingDataOutputTypeDef


class ThrottlingExceptionTypeDef(TypedDict):
    message: NotRequired[str]
    throttlingReasons: NotRequired[list[ThrottlingReasonTypeDef]]


class ValidationExceptionTypeDef(TypedDict):
    message: str
    reason: ValidationExceptionReasonType
    fields: NotRequired[list[ValidationExceptionFieldTypeDef]]


class RecordingTypeDef(TypedDict):
    Format: AudioFormatType
    Data: RecordingDataTypeDef


class StartSpeechSynthesisStreamActionStreamTypeDef(TypedDict):
    TextEvent: NotRequired[TextEventTypeDef]
    CloseStreamEvent: NotRequired[Mapping[str, Any]]


class ListLexiconsOutputTypeDef(TypedDict):
    Lexicons: list[LexiconDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class VoiceCreationDataOutputTypeDef(TypedDict):
    Recordings: list[RecordingOutputTypeDef]


class StartSpeechSynthesisStreamEventStreamTypeDef(TypedDict):
    AudioEvent: NotRequired[AudioEventTypeDef]
    StreamClosedEvent: NotRequired[StreamClosedEventTypeDef]
    ValidationException: NotRequired[ValidationExceptionTypeDef]
    ServiceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    ServiceFailureException: NotRequired[ServiceFailureExceptionTypeDef]
    ThrottlingException: NotRequired[ThrottlingExceptionTypeDef]


class VoiceCreationDataTypeDef(TypedDict):
    Recordings: Sequence[RecordingTypeDef]


class StartSpeechSynthesisStreamInputTypeDef(TypedDict):
    Engine: EngineType
    OutputFormat: OutputFormatType
    VoiceId: VoiceIdType
    LanguageCode: NotRequired[LanguageCodeType]
    LexiconNames: NotRequired[Sequence[str]]
    SampleRate: NotRequired[str]
    ActionStream: NotRequired[EventStream[StartSpeechSynthesisStreamActionStreamTypeDef]]


class VoiceTypeDef(TypedDict):
    Arn: NotRequired[str]
    Gender: NotRequired[GenderType]
    Id: NotRequired[VoiceIdType]
    LanguageCode: NotRequired[LanguageCodeType]
    LanguageName: NotRequired[str]
    Name: NotRequired[str]
    Origin: NotRequired[VoiceOriginType]
    Status: NotRequired[VoiceStatusType]
    StatusReason: NotRequired[str]
    AdditionalLanguageCodes: NotRequired[list[LanguageCodeType]]
    SupportedEngines: NotRequired[list[EngineType]]
    VoiceCreationData: NotRequired[VoiceCreationDataOutputTypeDef]
    CustomerManagedEncryption: NotRequired[CustomerManagedEncryptionOutputTypeDef]
    CreationTime: NotRequired[datetime]


class StartSpeechSynthesisStreamOutputTypeDef(TypedDict):
    EventStream: EventStream[StartSpeechSynthesisStreamEventStreamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


VoiceCreationDataUnionTypeDef = Union[VoiceCreationDataTypeDef, VoiceCreationDataOutputTypeDef]


class CreateVoiceOutputTypeDef(TypedDict):
    Voice: VoiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVoicesOutputTypeDef(TypedDict):
    Voices: list[VoiceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetVoiceOutputTypeDef(TypedDict):
    Voice: VoiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVoiceInputTypeDef(TypedDict):
    Name: str
    LanguageCode: CustomVoiceLanguageCodeType
    TermsAccepted: bool
    VoiceCreationData: VoiceCreationDataUnionTypeDef
    CustomerManagedEncryption: NotRequired[CustomerManagedEncryptionUnionTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]
