"""
Type annotations for connect-contact-lens service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect_contact_lens/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_connect_contact_lens.type_defs import TagConditionTypeDef

    data: TagConditionTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence

from .literals import (
    ExtractedInformationFailureCodeType,
    PostContactSummaryFailureCodeType,
    PostContactSummaryStatusType,
    SentimentValueType,
    TagComparisonTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CategoriesAttributeAndConditionTypeDef",
    "CategoriesAttributeFilterTypeDef",
    "CategoriesTypeDef",
    "CategoryDetailsTypeDef",
    "CharacterOffsetsTypeDef",
    "ExtractedInformationTypeDef",
    "ExtractedInformationValueTypeDef",
    "IssueDetectedTypeDef",
    "ListRealtimeContactAnalysisSegmentsRequestTypeDef",
    "ListRealtimeContactAnalysisSegmentsResponseTypeDef",
    "PointOfInterestTypeDef",
    "PostContactSummaryTypeDef",
    "RealTimeContactAnalysisSegmentsFilterTypeDef",
    "RealtimeContactAnalysisSegmentTypeDef",
    "ResponseMetadataTypeDef",
    "TagConditionTypeDef",
    "TranscriptTypeDef",
)


class TagConditionTypeDef(TypedDict):
    TagKey: NotRequired[str]
    TagValue: NotRequired[str]
    ComparisonType: NotRequired[TagComparisonTypeType]


class PointOfInterestTypeDef(TypedDict):
    BeginOffsetMillis: int
    EndOffsetMillis: int


class CharacterOffsetsTypeDef(TypedDict):
    BeginOffsetChar: int
    EndOffsetChar: int


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class PostContactSummaryTypeDef(TypedDict):
    Status: PostContactSummaryStatusType
    Content: NotRequired[str]
    FailureCode: NotRequired[PostContactSummaryFailureCodeType]


class CategoriesAttributeAndConditionTypeDef(TypedDict):
    TagConditions: NotRequired[Sequence[TagConditionTypeDef]]


class CategoryDetailsTypeDef(TypedDict):
    PointsOfInterest: list[PointOfInterestTypeDef]
    RuleId: NotRequired[str]


class ExtractedInformationValueTypeDef(TypedDict):
    Content: str
    PointsOfInterest: list[PointOfInterestTypeDef]


class IssueDetectedTypeDef(TypedDict):
    CharacterOffsets: CharacterOffsetsTypeDef


class CategoriesAttributeFilterTypeDef(TypedDict):
    OrConditions: NotRequired[Sequence[CategoriesAttributeAndConditionTypeDef]]
    AndCondition: NotRequired[CategoriesAttributeAndConditionTypeDef]
    TagCondition: NotRequired[TagConditionTypeDef]


class CategoriesTypeDef(TypedDict):
    MatchedCategories: list[str]
    MatchedDetails: dict[str, CategoryDetailsTypeDef]


class ExtractedInformationTypeDef(TypedDict):
    ExtractionDefinitionId: str
    ExtractionDefinitionName: str
    ExtractionDefinitionDisplayLabel: NotRequired[str]
    ExtractedValues: NotRequired[list[ExtractedInformationValueTypeDef]]
    FailureCode: NotRequired[ExtractedInformationFailureCodeType]


class TranscriptTypeDef(TypedDict):
    Id: str
    ParticipantId: str
    ParticipantRole: str
    Content: str
    BeginOffsetMillis: int
    EndOffsetMillis: int
    Sentiment: NotRequired[SentimentValueType]
    IssuesDetected: NotRequired[list[IssueDetectedTypeDef]]


class RealTimeContactAnalysisSegmentsFilterTypeDef(TypedDict):
    CategoriesAttributeFilter: NotRequired[CategoriesAttributeFilterTypeDef]


class RealtimeContactAnalysisSegmentTypeDef(TypedDict):
    Transcript: NotRequired[TranscriptTypeDef]
    Categories: NotRequired[CategoriesTypeDef]
    PostContactSummary: NotRequired[PostContactSummaryTypeDef]
    ExtractedInformation: NotRequired[ExtractedInformationTypeDef]


class ListRealtimeContactAnalysisSegmentsRequestTypeDef(TypedDict):
    InstanceId: str
    ContactId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ListFilter: NotRequired[RealTimeContactAnalysisSegmentsFilterTypeDef]


class ListRealtimeContactAnalysisSegmentsResponseTypeDef(TypedDict):
    Segments: list[RealtimeContactAnalysisSegmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
