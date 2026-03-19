"""
Type annotations for simpledbv2 service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_simpledbv2/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_simpledbv2.type_defs import ExportSummaryTypeDef

    data: ExportSummaryTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime

from .literals import ExportStatusType, S3SseAlgorithmType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ExportSummaryTypeDef",
    "GetExportRequestTypeDef",
    "GetExportRequestWaitTypeDef",
    "GetExportResponseTypeDef",
    "ListExportsRequestPaginateTypeDef",
    "ListExportsRequestTypeDef",
    "ListExportsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "StartDomainExportRequestTypeDef",
    "StartDomainExportResponseTypeDef",
    "WaiterConfigTypeDef",
)


class ExportSummaryTypeDef(TypedDict):
    exportArn: str
    exportStatus: ExportStatusType
    requestedAt: datetime
    domainName: str


class GetExportRequestTypeDef(TypedDict):
    exportArn: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListExportsRequestTypeDef(TypedDict):
    domainName: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class StartDomainExportRequestTypeDef(TypedDict):
    domainName: str
    s3Bucket: str
    clientToken: NotRequired[str]
    s3KeyPrefix: NotRequired[str]
    s3SseAlgorithm: NotRequired[S3SseAlgorithmType]
    s3SseKmsKeyId: NotRequired[str]
    s3BucketOwner: NotRequired[str]


class GetExportRequestWaitTypeDef(TypedDict):
    exportArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetExportResponseTypeDef(TypedDict):
    exportArn: str
    clientToken: str
    exportStatus: ExportStatusType
    domainName: str
    requestedAt: datetime
    s3Bucket: str
    s3KeyPrefix: str
    s3SseAlgorithm: S3SseAlgorithmType
    s3SseKmsKeyId: str
    s3BucketOwner: str
    failureCode: str
    failureMessage: str
    exportManifest: str
    itemsCount: int
    exportDataCutoffTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListExportsResponseTypeDef(TypedDict):
    exportSummaries: list[ExportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartDomainExportResponseTypeDef(TypedDict):
    clientToken: str
    exportArn: str
    requestedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListExportsRequestPaginateTypeDef(TypedDict):
    domainName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]
