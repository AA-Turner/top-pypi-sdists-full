"""
Type annotations for artifact service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_artifact.type_defs import AccountSettingsTypeDef

    data: AccountSettingsTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from aiobotocore.response import StreamingBody

from .literals import (
    AcceptanceTypeType,
    AgreementTypeType,
    CustomerAgreementStateType,
    FeedbackRatingType,
    FeedbackReasonCodeType,
    InputSourceType,
    InquiryStatusMessageType,
    InquiryStatusType,
    InquirySupportModeType,
    NotificationSubscriptionStatusType,
    PublishedStateType,
    QueryStatusMessageType,
    QueryStatusType,
    ReviewTypeType,
    UploadStateType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AccountSettingsTypeDef",
    "BlobTypeDef",
    "CitationTypeDef",
    "CreateComplianceInquiryRequestTypeDef",
    "CreateComplianceInquiryResponseTypeDef",
    "CustomerAgreementSummaryTypeDef",
    "ExportComplianceInquiryRequestTypeDef",
    "ExportComplianceInquiryResponseTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "GetComplianceInquiryMetadataRequestTypeDef",
    "GetComplianceInquiryMetadataResponseTypeDef",
    "GetReportMetadataRequestTypeDef",
    "GetReportMetadataResponseTypeDef",
    "GetReportRequestTypeDef",
    "GetReportResponseTypeDef",
    "GetTermForReportRequestTypeDef",
    "GetTermForReportResponseTypeDef",
    "InquiryContentTypeDef",
    "InquiryDetailTypeDef",
    "InquiryFileContentTypeDef",
    "InquirySummaryTypeDef",
    "ListComplianceInquiriesRequestPaginateTypeDef",
    "ListComplianceInquiriesRequestTypeDef",
    "ListComplianceInquiriesResponseTypeDef",
    "ListComplianceInquiryQueriesRequestPaginateTypeDef",
    "ListComplianceInquiryQueriesRequestTypeDef",
    "ListComplianceInquiryQueriesResponseTypeDef",
    "ListCustomerAgreementsRequestPaginateTypeDef",
    "ListCustomerAgreementsRequestTypeDef",
    "ListCustomerAgreementsResponseTypeDef",
    "ListReportVersionsRequestPaginateTypeDef",
    "ListReportVersionsRequestTypeDef",
    "ListReportVersionsResponseTypeDef",
    "ListReportsRequestPaginateTypeDef",
    "ListReportsRequestTypeDef",
    "ListReportsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutAccountSettingsRequestTypeDef",
    "PutAccountSettingsResponseTypeDef",
    "PutComplianceInquiryFeedbackRequestTypeDef",
    "PutComplianceInquiryFeedbackResponseTypeDef",
    "QuerySummaryTypeDef",
    "ReportDetailTypeDef",
    "ReportSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseVersionTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
)

class AccountSettingsTypeDef(TypedDict):
    notificationSubscriptionStatus: NotRequired[NotificationSubscriptionStatusType]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CitationTypeDef(TypedDict):
    sourceLabel: NotRequired[str]
    sourceContent: NotRequired[str]
    sourceLink: NotRequired[str]

InquirySummaryTypeDef = TypedDict(
    "InquirySummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "id": str,
        "status": InquiryStatusType,
        "statusMessage": InquiryStatusMessageType,
        "inputSource": InputSourceType,
        "createdAt": datetime,
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

CustomerAgreementSummaryTypeDef = TypedDict(
    "CustomerAgreementSummaryTypeDef",
    {
        "name": NotRequired[str],
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "agreementArn": NotRequired[str],
        "awsAccountId": NotRequired[str],
        "organizationArn": NotRequired[str],
        "effectiveStart": NotRequired[datetime],
        "effectiveEnd": NotRequired[datetime],
        "state": NotRequired[CustomerAgreementStateType],
        "description": NotRequired[str],
        "acceptanceTerms": NotRequired[list[str]],
        "terminateTerms": NotRequired[list[str]],
        "type": NotRequired[AgreementTypeType],
    },
)

class ExportComplianceInquiryRequestTypeDef(TypedDict):
    complianceInquiryId: str
    queryIdentifiers: NotRequired[Sequence[int]]
    includeCitations: NotRequired[bool]

class GetComplianceInquiryMetadataRequestTypeDef(TypedDict):
    complianceInquiryId: str

InquiryDetailTypeDef = TypedDict(
    "InquiryDetailTypeDef",
    {
        "arn": str,
        "name": str,
        "id": str,
        "status": InquiryStatusType,
        "statusMessage": InquiryStatusMessageType,
        "inputSource": InputSourceType,
        "createdAt": datetime,
        "updatedAt": NotRequired[datetime],
        "supportMode": NotRequired[InquirySupportModeType],
    },
)

class GetReportMetadataRequestTypeDef(TypedDict):
    reportId: str
    reportVersion: NotRequired[int]

ReportDetailTypeDef = TypedDict(
    "ReportDetailTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "periodStart": NotRequired[datetime],
        "periodEnd": NotRequired[datetime],
        "createdAt": NotRequired[datetime],
        "lastModifiedAt": NotRequired[datetime],
        "deletedAt": NotRequired[datetime],
        "state": NotRequired[PublishedStateType],
        "arn": NotRequired[str],
        "series": NotRequired[str],
        "category": NotRequired[str],
        "companyName": NotRequired[str],
        "productName": NotRequired[str],
        "termArn": NotRequired[str],
        "version": NotRequired[int],
        "acceptanceType": NotRequired[AcceptanceTypeType],
        "sequenceNumber": NotRequired[int],
        "uploadState": NotRequired[UploadStateType],
        "statusMessage": NotRequired[str],
    },
)

class GetReportRequestTypeDef(TypedDict):
    reportId: str
    termToken: str
    reportVersion: NotRequired[int]

class GetTermForReportRequestTypeDef(TypedDict):
    reportId: str
    reportVersion: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListComplianceInquiriesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListComplianceInquiryQueriesRequestTypeDef(TypedDict):
    complianceInquiryId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCustomerAgreementsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListReportVersionsRequestTypeDef(TypedDict):
    reportId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ReportSummaryTypeDef = TypedDict(
    "ReportSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "state": NotRequired[PublishedStateType],
        "arn": NotRequired[str],
        "version": NotRequired[int],
        "uploadState": NotRequired[UploadStateType],
        "description": NotRequired[str],
        "periodStart": NotRequired[datetime],
        "periodEnd": NotRequired[datetime],
        "series": NotRequired[str],
        "category": NotRequired[str],
        "companyName": NotRequired[str],
        "productName": NotRequired[str],
        "statusMessage": NotRequired[str],
        "acceptanceType": NotRequired[AcceptanceTypeType],
    },
)

class ListReportsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class PutAccountSettingsRequestTypeDef(TypedDict):
    notificationSubscriptionStatus: NotRequired[NotificationSubscriptionStatusType]

class PutComplianceInquiryFeedbackRequestTypeDef(TypedDict):
    complianceInquiryId: str
    rating: FeedbackRatingType
    queryIdentifier: NotRequired[int]
    responseRevisionId: NotRequired[int]
    reasonCodes: NotRequired[Sequence[FeedbackReasonCodeType]]
    comment: NotRequired[str]
    clientToken: NotRequired[str]

class ResponseVersionTypeDef(TypedDict):
    responseText: str
    timestamp: datetime

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class InquiryFileContentTypeDef(TypedDict):
    content: BlobTypeDef
    fileSections: NotRequired[Sequence[str]]

class CreateComplianceInquiryResponseTypeDef(TypedDict):
    complianceInquirySummary: InquirySummaryTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ExportComplianceInquiryResponseTypeDef(TypedDict):
    documentPresignedUrl: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetAccountSettingsResponseTypeDef(TypedDict):
    accountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetReportResponseTypeDef(TypedDict):
    documentPresignedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetTermForReportResponseTypeDef(TypedDict):
    documentPresignedUrl: str
    termToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListComplianceInquiriesResponseTypeDef(TypedDict):
    complianceInquiries: list[InquirySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutAccountSettingsResponseTypeDef(TypedDict):
    accountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutComplianceInquiryFeedbackResponseTypeDef(TypedDict):
    submittedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListCustomerAgreementsResponseTypeDef(TypedDict):
    customerAgreements: list[CustomerAgreementSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetComplianceInquiryMetadataResponseTypeDef(TypedDict):
    complianceInquiryDetail: InquiryDetailTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetReportMetadataResponseTypeDef(TypedDict):
    reportDetails: ReportDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListComplianceInquiriesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComplianceInquiryQueriesRequestPaginateTypeDef(TypedDict):
    complianceInquiryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomerAgreementsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReportVersionsRequestPaginateTypeDef(TypedDict):
    reportId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReportsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReportVersionsResponseTypeDef(TypedDict):
    reports: list[ReportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListReportsResponseTypeDef(TypedDict):
    reports: list[ReportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class QuerySummaryTypeDef(TypedDict):
    queryIdentifier: int
    query: str
    status: QueryStatusType
    statusMessage: QueryStatusMessageType
    createdAt: datetime
    response: NotRequired[str]
    reviewType: NotRequired[ReviewTypeType]
    citations: NotRequired[list[CitationTypeDef]]
    updatedResponseVersions: NotRequired[list[ResponseVersionTypeDef]]

class InquiryContentTypeDef(TypedDict):
    query: NotRequired[str]
    fileContent: NotRequired[InquiryFileContentTypeDef]

class ListComplianceInquiryQueriesResponseTypeDef(TypedDict):
    queries: list[QuerySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateComplianceInquiryRequestTypeDef(TypedDict):
    name: str
    inquiryContent: InquiryContentTypeDef
    clientToken: NotRequired[str]
    supportMode: NotRequired[InquirySupportModeType]
    tags: NotRequired[Mapping[str, str]]
