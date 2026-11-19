"""
Type annotations for abuse-signal service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_abuse_signal/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_abuse_signal.type_defs import ReportDataTypeDef

    data: ReportDataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from .literals import ReasonCodeType, ReportSubmissionStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CreateAbuseReportRequestTypeDef",
    "CreateAbuseReportResponseTypeDef",
    "GetAbuseReportStatusRequestTypeDef",
    "GetAbuseReportStatusRequestWaitTypeDef",
    "GetAbuseReportStatusResponseTypeDef",
    "ListAbuseReportStatusesRequestPaginateTypeDef",
    "ListAbuseReportStatusesRequestTypeDef",
    "ListAbuseReportStatusesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ReportDataTypeDef",
    "ReportStatusListItemTypeDef",
    "ResponseMetadataTypeDef",
    "WaiterConfigTypeDef",
)

class ReportDataTypeDef(TypedDict):
    xarf: NotRequired[Mapping[str, Any]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetAbuseReportStatusRequestTypeDef(TypedDict):
    reportId: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAbuseReportStatusesRequestTypeDef(TypedDict):
    correlationId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ReportStatusListItemTypeDef(TypedDict):
    reportId: str
    status: ReportSubmissionStatusType
    description: str
    correlationId: NotRequired[str]
    reasonCode: NotRequired[ReasonCodeType]

class CreateAbuseReportRequestTypeDef(TypedDict):
    report: ReportDataTypeDef
    correlationId: NotRequired[str]
    clientToken: NotRequired[str]

class CreateAbuseReportResponseTypeDef(TypedDict):
    reportId: str
    correlationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAbuseReportStatusResponseTypeDef(TypedDict):
    reportId: str
    correlationId: str
    status: ReportSubmissionStatusType
    description: str
    reasonCode: ReasonCodeType
    submittedAt: datetime
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetAbuseReportStatusRequestWaitTypeDef(TypedDict):
    reportId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class ListAbuseReportStatusesRequestPaginateTypeDef(TypedDict):
    correlationId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAbuseReportStatusesResponseTypeDef(TypedDict):
    reports: list[ReportStatusListItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
