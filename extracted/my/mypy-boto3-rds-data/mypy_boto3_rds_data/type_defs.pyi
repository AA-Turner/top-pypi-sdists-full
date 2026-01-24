"""
Type annotations for rds-data service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_rds_data.type_defs import ArrayValueOutputTypeDef

    data: ArrayValueOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import DecimalReturnTypeType, LongReturnTypeType, RecordsFormatTypeType, TypeHintType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ArrayValueOutputTypeDef",
    "ArrayValueTypeDef",
    "ArrayValueUnionTypeDef",
    "BatchExecuteStatementRequestTypeDef",
    "BatchExecuteStatementResponseTypeDef",
    "BeginTransactionRequestTypeDef",
    "BeginTransactionResponseTypeDef",
    "BlobTypeDef",
    "ColumnMetadataTypeDef",
    "CommitTransactionRequestTypeDef",
    "CommitTransactionResponseTypeDef",
    "ExecuteSqlRequestTypeDef",
    "ExecuteSqlResponseTypeDef",
    "ExecuteStatementRequestTypeDef",
    "ExecuteStatementResponseTypeDef",
    "FieldOutputTypeDef",
    "FieldTypeDef",
    "FieldUnionTypeDef",
    "RecordTypeDef",
    "ResponseMetadataTypeDef",
    "ResultFrameTypeDef",
    "ResultSetMetadataTypeDef",
    "ResultSetOptionsTypeDef",
    "RollbackTransactionRequestTypeDef",
    "RollbackTransactionResponseTypeDef",
    "SqlParameterTypeDef",
    "SqlStatementResultTypeDef",
    "StructValueTypeDef",
    "UpdateResultTypeDef",
    "ValueTypeDef",
)

class ArrayValueOutputTypeDef(TypedDict):
    booleanValues: NotRequired[list[bool]]
    longValues: NotRequired[list[int]]
    doubleValues: NotRequired[list[float]]
    stringValues: NotRequired[list[str]]
    arrayValues: NotRequired[list[dict[str, Any]]]

class ArrayValueTypeDef(TypedDict):
    booleanValues: NotRequired[Sequence[bool]]
    longValues: NotRequired[Sequence[int]]
    doubleValues: NotRequired[Sequence[float]]
    stringValues: NotRequired[Sequence[str]]
    arrayValues: NotRequired[Sequence[Mapping[str, Any]]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BeginTransactionRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    database: NotRequired[str]
    schema: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ColumnMetadataTypeDef = TypedDict(
    "ColumnMetadataTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[int],
        "typeName": NotRequired[str],
        "label": NotRequired[str],
        "schemaName": NotRequired[str],
        "tableName": NotRequired[str],
        "isAutoIncrement": NotRequired[bool],
        "isSigned": NotRequired[bool],
        "isCurrency": NotRequired[bool],
        "isCaseSensitive": NotRequired[bool],
        "nullable": NotRequired[int],
        "precision": NotRequired[int],
        "scale": NotRequired[int],
        "arrayBaseColumnType": NotRequired[int],
    },
)

class CommitTransactionRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    transactionId: str

class ExecuteSqlRequestTypeDef(TypedDict):
    dbClusterOrInstanceArn: str
    awsSecretStoreArn: str
    sqlStatements: str
    database: NotRequired[str]
    schema: NotRequired[str]

class ResultSetOptionsTypeDef(TypedDict):
    decimalReturnType: NotRequired[DecimalReturnTypeType]
    longReturnType: NotRequired[LongReturnTypeType]

class RollbackTransactionRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    transactionId: str

class StructValueTypeDef(TypedDict):
    attributes: NotRequired[list[dict[str, Any]]]

class FieldOutputTypeDef(TypedDict):
    isNull: NotRequired[bool]
    booleanValue: NotRequired[bool]
    longValue: NotRequired[int]
    doubleValue: NotRequired[float]
    stringValue: NotRequired[str]
    blobValue: NotRequired[bytes]
    arrayValue: NotRequired[ArrayValueOutputTypeDef]

ArrayValueUnionTypeDef = Union[ArrayValueTypeDef, ArrayValueOutputTypeDef]

class BeginTransactionResponseTypeDef(TypedDict):
    transactionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CommitTransactionResponseTypeDef(TypedDict):
    transactionStatus: str
    ResponseMetadata: ResponseMetadataTypeDef

class RollbackTransactionResponseTypeDef(TypedDict):
    transactionStatus: str
    ResponseMetadata: ResponseMetadataTypeDef

class ResultSetMetadataTypeDef(TypedDict):
    columnCount: NotRequired[int]
    columnMetadata: NotRequired[list[ColumnMetadataTypeDef]]

class ValueTypeDef(TypedDict):
    isNull: NotRequired[bool]
    bitValue: NotRequired[bool]
    bigIntValue: NotRequired[int]
    intValue: NotRequired[int]
    doubleValue: NotRequired[float]
    realValue: NotRequired[float]
    stringValue: NotRequired[str]
    blobValue: NotRequired[bytes]
    arrayValues: NotRequired[list[dict[str, Any]]]
    structValue: NotRequired[StructValueTypeDef]

class ExecuteStatementResponseTypeDef(TypedDict):
    records: list[list[FieldOutputTypeDef]]
    columnMetadata: list[ColumnMetadataTypeDef]
    numberOfRecordsUpdated: int
    generatedFields: list[FieldOutputTypeDef]
    formattedRecords: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateResultTypeDef(TypedDict):
    generatedFields: NotRequired[list[FieldOutputTypeDef]]

class FieldTypeDef(TypedDict):
    isNull: NotRequired[bool]
    booleanValue: NotRequired[bool]
    longValue: NotRequired[int]
    doubleValue: NotRequired[float]
    stringValue: NotRequired[str]
    blobValue: NotRequired[BlobTypeDef]
    arrayValue: NotRequired[ArrayValueUnionTypeDef]

class RecordTypeDef(TypedDict):
    values: NotRequired[list[ValueTypeDef]]

class BatchExecuteStatementResponseTypeDef(TypedDict):
    updateResults: list[UpdateResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

FieldUnionTypeDef = Union[FieldTypeDef, FieldOutputTypeDef]

class ResultFrameTypeDef(TypedDict):
    resultSetMetadata: NotRequired[ResultSetMetadataTypeDef]
    records: NotRequired[list[RecordTypeDef]]

class SqlParameterTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[FieldUnionTypeDef]
    typeHint: NotRequired[TypeHintType]

class SqlStatementResultTypeDef(TypedDict):
    resultFrame: NotRequired[ResultFrameTypeDef]
    numberOfRecordsUpdated: NotRequired[int]

class BatchExecuteStatementRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    sql: str
    database: NotRequired[str]
    schema: NotRequired[str]
    parameterSets: NotRequired[Sequence[Sequence[SqlParameterTypeDef]]]
    transactionId: NotRequired[str]

class ExecuteStatementRequestTypeDef(TypedDict):
    resourceArn: str
    secretArn: str
    sql: str
    database: NotRequired[str]
    schema: NotRequired[str]
    parameters: NotRequired[Sequence[SqlParameterTypeDef]]
    transactionId: NotRequired[str]
    includeResultMetadata: NotRequired[bool]
    continueAfterTimeout: NotRequired[bool]
    resultSetOptions: NotRequired[ResultSetOptionsTypeDef]
    formatRecordsAs: NotRequired[RecordsFormatTypeType]

class ExecuteSqlResponseTypeDef(TypedDict):
    sqlStatementResults: list[SqlStatementResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
