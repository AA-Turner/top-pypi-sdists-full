"""
Type annotations for bcm-data-exports service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_data_exports/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_bcm_data_exports.type_defs import ColumnTypeDef

    data: ColumnTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    CompressionOptionType,
    ExecutionStatusCodeType,
    ExecutionStatusReasonType,
    ExportStatusCodeType,
    FormatOptionType,
    OverwriteOptionType,
    S3OutputTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ColumnTypeDef",
    "CreateExportRequestTypeDef",
    "CreateExportResponseTypeDef",
    "DataQueryOutputTypeDef",
    "DataQueryTypeDef",
    "DeleteExportRequestTypeDef",
    "DeleteExportResponseTypeDef",
    "DestinationConfigurationsTypeDef",
    "ExecutionReferenceTypeDef",
    "ExecutionStatusTypeDef",
    "ExportOutputTypeDef",
    "ExportReferenceTypeDef",
    "ExportStatusTypeDef",
    "ExportTypeDef",
    "ExportUnionTypeDef",
    "GetExecutionRequestTypeDef",
    "GetExecutionResponseTypeDef",
    "GetExportRequestTypeDef",
    "GetExportResponseTypeDef",
    "GetTableRequestTypeDef",
    "GetTableResponseTypeDef",
    "ListExecutionsRequestPaginateTypeDef",
    "ListExecutionsRequestTypeDef",
    "ListExecutionsResponseTypeDef",
    "ListExportsRequestPaginateTypeDef",
    "ListExportsRequestTypeDef",
    "ListExportsResponseTypeDef",
    "ListTablesRequestPaginateTypeDef",
    "ListTablesRequestTypeDef",
    "ListTablesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RefreshCadenceTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationTypeDef",
    "S3OutputConfigurationsTypeDef",
    "TablePropertyDescriptionTypeDef",
    "TableTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateExportRequestTypeDef",
    "UpdateExportResponseTypeDef",
)

ColumnTypeDef = TypedDict(
    "ColumnTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[str],
        "Description": NotRequired[str],
    },
)


class ResourceTagTypeDef(TypedDict):
    Key: str
    Value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DataQueryOutputTypeDef(TypedDict):
    QueryStatement: str
    TableConfigurations: NotRequired[dict[str, dict[str, str]]]


class DataQueryTypeDef(TypedDict):
    QueryStatement: str
    TableConfigurations: NotRequired[Mapping[str, Mapping[str, str]]]


class DeleteExportRequestTypeDef(TypedDict):
    ExportArn: str


class ExecutionStatusTypeDef(TypedDict):
    StatusCode: NotRequired[ExecutionStatusCodeType]
    StatusReason: NotRequired[ExecutionStatusReasonType]
    CreatedAt: NotRequired[datetime]
    CompletedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]


class RefreshCadenceTypeDef(TypedDict):
    Frequency: Literal["SYNCHRONOUS"]


class ExportStatusTypeDef(TypedDict):
    StatusCode: NotRequired[ExportStatusCodeType]
    StatusReason: NotRequired[ExecutionStatusReasonType]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    LastRefreshedAt: NotRequired[datetime]


class GetExecutionRequestTypeDef(TypedDict):
    ExportArn: str
    ExecutionId: str


class GetExportRequestTypeDef(TypedDict):
    ExportArn: str


class GetTableRequestTypeDef(TypedDict):
    TableName: str
    TableProperties: NotRequired[Mapping[str, str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListExecutionsRequestTypeDef(TypedDict):
    ExportArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListExportsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTablesRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class S3OutputConfigurationsTypeDef(TypedDict):
    OutputType: S3OutputTypeType
    Format: FormatOptionType
    Compression: CompressionOptionType
    Overwrite: OverwriteOptionType


class TablePropertyDescriptionTypeDef(TypedDict):
    Name: NotRequired[str]
    ValidValues: NotRequired[list[str]]
    DefaultValue: NotRequired[str]
    Description: NotRequired[str]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTagKeys: Sequence[str]


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTags: Sequence[ResourceTagTypeDef]


class CreateExportResponseTypeDef(TypedDict):
    ExportArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteExportResponseTypeDef(TypedDict):
    ExportArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTableResponseTypeDef(TypedDict):
    TableName: str
    Description: str
    TableProperties: dict[str, str]
    Schema: list[ColumnTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceTags: list[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateExportResponseTypeDef(TypedDict):
    ExportArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ExecutionReferenceTypeDef(TypedDict):
    ExecutionId: str
    ExecutionStatus: ExecutionStatusTypeDef


class ExportReferenceTypeDef(TypedDict):
    ExportArn: str
    ExportName: str
    ExportStatus: ExportStatusTypeDef


class ListExecutionsRequestPaginateTypeDef(TypedDict):
    ExportArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExportsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTablesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class S3DestinationTypeDef(TypedDict):
    S3Bucket: str
    S3Prefix: str
    S3Region: str
    S3OutputConfigurations: S3OutputConfigurationsTypeDef
    S3BucketOwner: NotRequired[str]


class TableTypeDef(TypedDict):
    TableName: NotRequired[str]
    Description: NotRequired[str]
    TableProperties: NotRequired[list[TablePropertyDescriptionTypeDef]]


class ListExecutionsResponseTypeDef(TypedDict):
    Executions: list[ExecutionReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListExportsResponseTypeDef(TypedDict):
    Exports: list[ExportReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DestinationConfigurationsTypeDef(TypedDict):
    S3Destination: S3DestinationTypeDef


class ListTablesResponseTypeDef(TypedDict):
    Tables: list[TableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ExportOutputTypeDef(TypedDict):
    Name: str
    DataQuery: DataQueryOutputTypeDef
    DestinationConfigurations: DestinationConfigurationsTypeDef
    RefreshCadence: RefreshCadenceTypeDef
    ExportArn: NotRequired[str]
    Description: NotRequired[str]


class ExportTypeDef(TypedDict):
    Name: str
    DataQuery: DataQueryTypeDef
    DestinationConfigurations: DestinationConfigurationsTypeDef
    RefreshCadence: RefreshCadenceTypeDef
    ExportArn: NotRequired[str]
    Description: NotRequired[str]


class GetExecutionResponseTypeDef(TypedDict):
    ExecutionId: str
    Export: ExportOutputTypeDef
    ExecutionStatus: ExecutionStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetExportResponseTypeDef(TypedDict):
    Export: ExportOutputTypeDef
    ExportStatus: ExportStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ExportUnionTypeDef = Union[ExportTypeDef, ExportOutputTypeDef]


class CreateExportRequestTypeDef(TypedDict):
    Export: ExportUnionTypeDef
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]


class UpdateExportRequestTypeDef(TypedDict):
    ExportArn: str
    Export: ExportUnionTypeDef
