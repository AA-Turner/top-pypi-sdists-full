"""
Type annotations for cur service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_cur.type_defs import DeleteReportDefinitionRequestTypeDef

    data: DeleteReportDefinitionRequestTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import Union

from .literals import (
    AdditionalArtifactType,
    AWSRegionType,
    CompressionFormatType,
    LastStatusType,
    ReportFormatType,
    ReportVersioningType,
    SchemaElementType,
    TimeUnitType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "DeleteReportDefinitionRequestTypeDef",
    "DeleteReportDefinitionResponseTypeDef",
    "DescribeReportDefinitionsRequestPaginateTypeDef",
    "DescribeReportDefinitionsRequestTypeDef",
    "DescribeReportDefinitionsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ModifyReportDefinitionRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PutReportDefinitionRequestTypeDef",
    "ReportDefinitionOutputTypeDef",
    "ReportDefinitionTypeDef",
    "ReportDefinitionUnionTypeDef",
    "ReportStatusTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestTypeDef",
)

class DeleteReportDefinitionRequestTypeDef(TypedDict):
    ReportName: str

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

class DescribeReportDefinitionsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    ReportName: str

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ReportStatusTypeDef(TypedDict):
    lastDelivery: NotRequired[str]
    lastStatus: NotRequired[LastStatusType]

class UntagResourceRequestTypeDef(TypedDict):
    ReportName: str
    TagKeys: Sequence[str]

class DeleteReportDefinitionResponseTypeDef(TypedDict):
    ResponseMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeReportDefinitionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestTypeDef(TypedDict):
    ReportName: str
    Tags: Sequence[TagTypeDef]

class ReportDefinitionOutputTypeDef(TypedDict):
    ReportName: str
    TimeUnit: TimeUnitType
    Format: ReportFormatType
    Compression: CompressionFormatType
    AdditionalSchemaElements: list[SchemaElementType]
    S3Bucket: str
    S3Prefix: str
    S3Region: AWSRegionType
    AdditionalArtifacts: NotRequired[list[AdditionalArtifactType]]
    RefreshClosedReports: NotRequired[bool]
    ReportVersioning: NotRequired[ReportVersioningType]
    BillingViewArn: NotRequired[str]
    ReportStatus: NotRequired[ReportStatusTypeDef]

class ReportDefinitionTypeDef(TypedDict):
    ReportName: str
    TimeUnit: TimeUnitType
    Format: ReportFormatType
    Compression: CompressionFormatType
    AdditionalSchemaElements: Sequence[SchemaElementType]
    S3Bucket: str
    S3Prefix: str
    S3Region: AWSRegionType
    AdditionalArtifacts: NotRequired[Sequence[AdditionalArtifactType]]
    RefreshClosedReports: NotRequired[bool]
    ReportVersioning: NotRequired[ReportVersioningType]
    BillingViewArn: NotRequired[str]
    ReportStatus: NotRequired[ReportStatusTypeDef]

class DescribeReportDefinitionsResponseTypeDef(TypedDict):
    ReportDefinitions: list[ReportDefinitionOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

ReportDefinitionUnionTypeDef = Union[ReportDefinitionTypeDef, ReportDefinitionOutputTypeDef]

class ModifyReportDefinitionRequestTypeDef(TypedDict):
    ReportName: str
    ReportDefinition: ReportDefinitionUnionTypeDef

class PutReportDefinitionRequestTypeDef(TypedDict):
    ReportDefinition: ReportDefinitionUnionTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]
