"""
Type annotations for support service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_support/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_support.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import UploadStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AddAttachmentsToSetRequestTypeDef",
    "AddAttachmentsToSetResponseTypeDef",
    "AddCommunicationToCaseRequestTypeDef",
    "AddCommunicationToCaseResponseTypeDef",
    "AttachmentDetailsTypeDef",
    "AttachmentOutputTypeDef",
    "AttachmentTypeDef",
    "AttachmentUnionTypeDef",
    "BlobTypeDef",
    "CaseDetailsTypeDef",
    "CategoryTypeDef",
    "CommunicationTypeDef",
    "CommunicationTypeOptionsTypeDef",
    "CompleteAttachmentUploadRequestTypeDef",
    "CompleteAttachmentUploadResponseTypeDef",
    "CompletedUploadTypeDef",
    "CreateCaseRequestTypeDef",
    "CreateCaseResponseTypeDef",
    "DateIntervalTypeDef",
    "DescribeAttachmentRequestTypeDef",
    "DescribeAttachmentResponseTypeDef",
    "DescribeAttachmentUploadStatusRequestTypeDef",
    "DescribeAttachmentUploadStatusResponseTypeDef",
    "DescribeCasesRequestPaginateTypeDef",
    "DescribeCasesRequestTypeDef",
    "DescribeCasesResponseTypeDef",
    "DescribeCommunicationsRequestPaginateTypeDef",
    "DescribeCommunicationsRequestTypeDef",
    "DescribeCommunicationsResponseTypeDef",
    "DescribeCreateCaseOptionsRequestTypeDef",
    "DescribeCreateCaseOptionsResponseTypeDef",
    "DescribeServicesRequestTypeDef",
    "DescribeServicesResponseTypeDef",
    "DescribeSeverityLevelsRequestTypeDef",
    "DescribeSeverityLevelsResponseTypeDef",
    "DescribeSupportedLanguagesRequestTypeDef",
    "DescribeSupportedLanguagesResponseTypeDef",
    "DescribeTrustedAdvisorCheckRefreshStatusesRequestTypeDef",
    "DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef",
    "DescribeTrustedAdvisorCheckResultRequestTypeDef",
    "DescribeTrustedAdvisorCheckResultResponseTypeDef",
    "DescribeTrustedAdvisorCheckSummariesRequestTypeDef",
    "DescribeTrustedAdvisorCheckSummariesResponseTypeDef",
    "DescribeTrustedAdvisorChecksRequestTypeDef",
    "DescribeTrustedAdvisorChecksResponseTypeDef",
    "DownloadUrlTypeDef",
    "GetAttachmentDownloadLinkRequestTypeDef",
    "GetAttachmentDownloadLinkResponseTypeDef",
    "GetAttachmentUploadLinksRequestTypeDef",
    "GetAttachmentUploadLinksResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RecentCaseCommunicationsTypeDef",
    "RefreshTrustedAdvisorCheckRequestTypeDef",
    "RefreshTrustedAdvisorCheckResponseTypeDef",
    "ResolveCaseRequestTypeDef",
    "ResolveCaseResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceTypeDef",
    "SeverityLevelTypeDef",
    "SupportedHourTypeDef",
    "SupportedLanguageTypeDef",
    "TrustedAdvisorCategorySpecificSummaryTypeDef",
    "TrustedAdvisorCheckDescriptionTypeDef",
    "TrustedAdvisorCheckRefreshStatusTypeDef",
    "TrustedAdvisorCheckResultTypeDef",
    "TrustedAdvisorCheckSummaryTypeDef",
    "TrustedAdvisorCostOptimizingSummaryTypeDef",
    "TrustedAdvisorResourceDetailTypeDef",
    "TrustedAdvisorResourcesSummaryTypeDef",
    "UploadProgressTypeDef",
    "UploadRangeTypeDef",
    "UploadUrlTypeDef",
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AddCommunicationToCaseRequestTypeDef(TypedDict):
    communicationBody: str
    caseId: NotRequired[str]
    ccEmailAddresses: NotRequired[Sequence[str]]
    attachmentSetId: NotRequired[str]
    uploadIds: NotRequired[Sequence[str]]
    dryRun: NotRequired[bool]


class AttachmentDetailsTypeDef(TypedDict):
    attachmentId: NotRequired[str]
    fileName: NotRequired[str]


class AttachmentOutputTypeDef(TypedDict):
    fileName: NotRequired[str]
    data: NotRequired[bytes]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CategoryTypeDef(TypedDict):
    code: NotRequired[str]
    name: NotRequired[str]


class DateIntervalTypeDef(TypedDict):
    startDateTime: NotRequired[str]
    endDateTime: NotRequired[str]


class SupportedHourTypeDef(TypedDict):
    startTime: NotRequired[str]
    endTime: NotRequired[str]


class CompletedUploadTypeDef(TypedDict):
    partIndex: int
    eTag: str


class CreateCaseRequestTypeDef(TypedDict):
    subject: str
    communicationBody: str
    serviceCode: NotRequired[str]
    severityCode: NotRequired[str]
    categoryCode: NotRequired[str]
    ccEmailAddresses: NotRequired[Sequence[str]]
    language: NotRequired[str]
    issueType: NotRequired[str]
    attachmentSetId: NotRequired[str]
    uploadIds: NotRequired[Sequence[str]]
    dryRun: NotRequired[bool]


class DescribeAttachmentRequestTypeDef(TypedDict):
    attachmentId: str
    dryRun: NotRequired[bool]


class DescribeAttachmentUploadStatusRequestTypeDef(TypedDict):
    uploadId: str
    dryRun: NotRequired[bool]


class UploadProgressTypeDef(TypedDict):
    totalParts: NotRequired[int]
    completedPartsCount: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeCasesRequestTypeDef(TypedDict):
    caseIdList: NotRequired[Sequence[str]]
    displayId: NotRequired[str]
    afterTime: NotRequired[str]
    beforeTime: NotRequired[str]
    includeResolvedCases: NotRequired[bool]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    language: NotRequired[str]
    includeCommunications: NotRequired[bool]
    dryRun: NotRequired[bool]


class DescribeCommunicationsRequestTypeDef(TypedDict):
    caseId: str
    beforeTime: NotRequired[str]
    afterTime: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    dryRun: NotRequired[bool]


class DescribeCreateCaseOptionsRequestTypeDef(TypedDict):
    issueType: str
    serviceCode: str
    language: str
    categoryCode: str
    dryRun: NotRequired[bool]


class DescribeServicesRequestTypeDef(TypedDict):
    serviceCodeList: NotRequired[Sequence[str]]
    language: NotRequired[str]
    dryRun: NotRequired[bool]


class DescribeSeverityLevelsRequestTypeDef(TypedDict):
    language: NotRequired[str]
    dryRun: NotRequired[bool]


class SeverityLevelTypeDef(TypedDict):
    code: NotRequired[str]
    name: NotRequired[str]


class DescribeSupportedLanguagesRequestTypeDef(TypedDict):
    issueType: str
    serviceCode: str
    categoryCode: str
    dryRun: NotRequired[bool]


class SupportedLanguageTypeDef(TypedDict):
    code: NotRequired[str]
    language: NotRequired[str]
    display: NotRequired[str]


class DescribeTrustedAdvisorCheckRefreshStatusesRequestTypeDef(TypedDict):
    checkIds: Sequence[str]


class TrustedAdvisorCheckRefreshStatusTypeDef(TypedDict):
    checkId: str
    status: str
    millisUntilNextRefreshable: int


class DescribeTrustedAdvisorCheckResultRequestTypeDef(TypedDict):
    checkId: str
    language: NotRequired[str]


class DescribeTrustedAdvisorCheckSummariesRequestTypeDef(TypedDict):
    checkIds: Sequence[str]


class DescribeTrustedAdvisorChecksRequestTypeDef(TypedDict):
    language: str


TrustedAdvisorCheckDescriptionTypeDef = TypedDict(
    "TrustedAdvisorCheckDescriptionTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "category": str,
        "metadata": list[str],
    },
)


class DownloadUrlTypeDef(TypedDict):
    url: str
    expiryDate: str


class GetAttachmentDownloadLinkRequestTypeDef(TypedDict):
    attachmentId: str
    dryRun: NotRequired[bool]


class UploadRangeTypeDef(TypedDict):
    startIndex: int
    endIndex: NotRequired[int]


class UploadUrlTypeDef(TypedDict):
    url: str
    partIndex: int
    expiryDate: str


class RefreshTrustedAdvisorCheckRequestTypeDef(TypedDict):
    checkId: str


class ResolveCaseRequestTypeDef(TypedDict):
    caseId: NotRequired[str]
    dryRun: NotRequired[bool]


class TrustedAdvisorCostOptimizingSummaryTypeDef(TypedDict):
    estimatedMonthlySavings: float
    estimatedPercentMonthlySavings: float


class TrustedAdvisorResourceDetailTypeDef(TypedDict):
    status: str
    resourceId: str
    metadata: list[str]
    region: NotRequired[str]
    isSuppressed: NotRequired[bool]


class TrustedAdvisorResourcesSummaryTypeDef(TypedDict):
    resourcesProcessed: int
    resourcesFlagged: int
    resourcesIgnored: int
    resourcesSuppressed: int


class AddAttachmentsToSetResponseTypeDef(TypedDict):
    attachmentSetId: str
    expiryTime: str
    ResponseMetadata: ResponseMetadataTypeDef


class AddCommunicationToCaseResponseTypeDef(TypedDict):
    result: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CompleteAttachmentUploadResponseTypeDef(TypedDict):
    uploadStatus: UploadStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCaseResponseTypeDef(TypedDict):
    caseId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResolveCaseResponseTypeDef(TypedDict):
    initialCaseStatus: str
    finalCaseStatus: str
    ResponseMetadata: ResponseMetadataTypeDef


class CommunicationTypeDef(TypedDict):
    caseId: NotRequired[str]
    body: NotRequired[str]
    submittedBy: NotRequired[str]
    timeCreated: NotRequired[str]
    attachments: NotRequired[list[AttachmentDetailsTypeDef]]
    attachmentSet: NotRequired[list[AttachmentDetailsTypeDef]]


class DescribeAttachmentResponseTypeDef(TypedDict):
    attachment: AttachmentOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AttachmentTypeDef(TypedDict):
    fileName: NotRequired[str]
    data: NotRequired[BlobTypeDef]


class ServiceTypeDef(TypedDict):
    code: NotRequired[str]
    name: NotRequired[str]
    categories: NotRequired[list[CategoryTypeDef]]


CommunicationTypeOptionsTypeDef = TypedDict(
    "CommunicationTypeOptionsTypeDef",
    {
        "type": NotRequired[str],
        "supportedHours": NotRequired[list[SupportedHourTypeDef]],
        "datesWithoutSupport": NotRequired[list[DateIntervalTypeDef]],
    },
)


class CompleteAttachmentUploadRequestTypeDef(TypedDict):
    uploadId: str
    completedUploads: Sequence[CompletedUploadTypeDef]
    dryRun: NotRequired[bool]


class DescribeAttachmentUploadStatusResponseTypeDef(TypedDict):
    uploadStatus: UploadStatusType
    fileName: str
    uploadProgress: UploadProgressTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCasesRequestPaginateTypeDef(TypedDict):
    caseIdList: NotRequired[Sequence[str]]
    displayId: NotRequired[str]
    afterTime: NotRequired[str]
    beforeTime: NotRequired[str]
    includeResolvedCases: NotRequired[bool]
    language: NotRequired[str]
    includeCommunications: NotRequired[bool]
    dryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCommunicationsRequestPaginateTypeDef(TypedDict):
    caseId: str
    beforeTime: NotRequired[str]
    afterTime: NotRequired[str]
    dryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSeverityLevelsResponseTypeDef(TypedDict):
    severityLevels: list[SeverityLevelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSupportedLanguagesResponseTypeDef(TypedDict):
    supportedLanguages: list[SupportedLanguageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef(TypedDict):
    statuses: list[TrustedAdvisorCheckRefreshStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RefreshTrustedAdvisorCheckResponseTypeDef(TypedDict):
    status: TrustedAdvisorCheckRefreshStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrustedAdvisorChecksResponseTypeDef(TypedDict):
    checks: list[TrustedAdvisorCheckDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetAttachmentDownloadLinkResponseTypeDef(TypedDict):
    fileName: str
    downloadUrl: DownloadUrlTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAttachmentUploadLinksRequestTypeDef(TypedDict):
    fileName: str
    fileSizeBytes: NotRequired[int]
    uploadId: NotRequired[str]
    uploadRange: NotRequired[UploadRangeTypeDef]
    dryRun: NotRequired[bool]


class GetAttachmentUploadLinksResponseTypeDef(TypedDict):
    uploadId: str
    partSizeBytes: int
    totalParts: int
    nextIndex: int
    uploadUrls: list[UploadUrlTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TrustedAdvisorCategorySpecificSummaryTypeDef(TypedDict):
    costOptimizing: NotRequired[TrustedAdvisorCostOptimizingSummaryTypeDef]


class DescribeCommunicationsResponseTypeDef(TypedDict):
    communications: list[CommunicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RecentCaseCommunicationsTypeDef(TypedDict):
    communications: NotRequired[list[CommunicationTypeDef]]
    nextToken: NotRequired[str]


AttachmentUnionTypeDef = Union[AttachmentTypeDef, AttachmentOutputTypeDef]


class DescribeServicesResponseTypeDef(TypedDict):
    services: list[ServiceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCreateCaseOptionsResponseTypeDef(TypedDict):
    languageAvailability: str
    communicationTypes: list[CommunicationTypeOptionsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TrustedAdvisorCheckResultTypeDef(TypedDict):
    checkId: str
    timestamp: str
    status: str
    resourcesSummary: TrustedAdvisorResourcesSummaryTypeDef
    categorySpecificSummary: TrustedAdvisorCategorySpecificSummaryTypeDef
    flaggedResources: list[TrustedAdvisorResourceDetailTypeDef]


class TrustedAdvisorCheckSummaryTypeDef(TypedDict):
    checkId: str
    timestamp: str
    status: str
    resourcesSummary: TrustedAdvisorResourcesSummaryTypeDef
    categorySpecificSummary: TrustedAdvisorCategorySpecificSummaryTypeDef
    hasFlaggedResources: NotRequired[bool]


class CaseDetailsTypeDef(TypedDict):
    caseId: NotRequired[str]
    displayId: NotRequired[str]
    subject: NotRequired[str]
    status: NotRequired[str]
    serviceCode: NotRequired[str]
    categoryCode: NotRequired[str]
    severityCode: NotRequired[str]
    submittedBy: NotRequired[str]
    timeCreated: NotRequired[str]
    recentCommunications: NotRequired[RecentCaseCommunicationsTypeDef]
    ccEmailAddresses: NotRequired[list[str]]
    language: NotRequired[str]


class AddAttachmentsToSetRequestTypeDef(TypedDict):
    attachments: Sequence[AttachmentUnionTypeDef]
    attachmentSetId: NotRequired[str]
    dryRun: NotRequired[bool]


class DescribeTrustedAdvisorCheckResultResponseTypeDef(TypedDict):
    result: TrustedAdvisorCheckResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrustedAdvisorCheckSummariesResponseTypeDef(TypedDict):
    summaries: list[TrustedAdvisorCheckSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCasesResponseTypeDef(TypedDict):
    cases: list[CaseDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
