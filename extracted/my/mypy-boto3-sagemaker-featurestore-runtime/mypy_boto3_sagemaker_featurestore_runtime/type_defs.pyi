"""
Type annotations for sagemaker-featurestore-runtime service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_featurestore_runtime/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_sagemaker_featurestore_runtime.type_defs import BatchGetRecordErrorTypeDef

    data: BatchGetRecordErrorTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import Union

from .literals import (
    DeletionModeType,
    ExpirationTimeResponseType,
    TargetStoreType,
    TtlDurationUnitType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BatchGetRecordErrorTypeDef",
    "BatchGetRecordIdentifierOutputTypeDef",
    "BatchGetRecordIdentifierTypeDef",
    "BatchGetRecordIdentifierUnionTypeDef",
    "BatchGetRecordRequestTypeDef",
    "BatchGetRecordResponseTypeDef",
    "BatchGetRecordResultDetailTypeDef",
    "BatchWriteRecordEntryOutputTypeDef",
    "BatchWriteRecordEntryTypeDef",
    "BatchWriteRecordEntryUnionTypeDef",
    "BatchWriteRecordErrorTypeDef",
    "BatchWriteRecordRequestTypeDef",
    "BatchWriteRecordResponseTypeDef",
    "DeleteRecordRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FeatureValueOutputTypeDef",
    "FeatureValueTypeDef",
    "FeatureValueUnionTypeDef",
    "GetRecordRequestTypeDef",
    "GetRecordResponseTypeDef",
    "ListRecordsRequestPaginateTypeDef",
    "ListRecordsRequestTypeDef",
    "ListRecordsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutRecordRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TtlDurationTypeDef",
    "UpdateRecordRequestTypeDef",
)

class BatchGetRecordErrorTypeDef(TypedDict):
    FeatureGroupName: str
    RecordIdentifierValueAsString: str
    ErrorCode: str
    ErrorMessage: str

class BatchGetRecordIdentifierOutputTypeDef(TypedDict):
    FeatureGroupName: str
    RecordIdentifiersValueAsString: list[str]
    FeatureNames: NotRequired[list[str]]

class BatchGetRecordIdentifierTypeDef(TypedDict):
    FeatureGroupName: str
    RecordIdentifiersValueAsString: Sequence[str]
    FeatureNames: NotRequired[Sequence[str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class FeatureValueOutputTypeDef(TypedDict):
    FeatureName: str
    ValueAsString: NotRequired[str]
    ValueAsStringList: NotRequired[list[str]]

class TtlDurationTypeDef(TypedDict):
    Unit: TtlDurationUnitType
    Value: int

class DeleteRecordRequestTypeDef(TypedDict):
    FeatureGroupName: str
    RecordIdentifierValueAsString: str
    EventTime: str
    TargetStores: NotRequired[Sequence[TargetStoreType]]
    DeletionMode: NotRequired[DeletionModeType]

class FeatureValueTypeDef(TypedDict):
    FeatureName: str
    ValueAsString: NotRequired[str]
    ValueAsStringList: NotRequired[Sequence[str]]

class GetRecordRequestTypeDef(TypedDict):
    FeatureGroupName: str
    RecordIdentifierValueAsString: str
    FeatureNames: NotRequired[Sequence[str]]
    ExpirationTimeResponse: NotRequired[ExpirationTimeResponseType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListRecordsRequestTypeDef(TypedDict):
    FeatureGroupName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    IncludeSoftDeletedRecords: NotRequired[bool]

BatchGetRecordIdentifierUnionTypeDef = Union[
    BatchGetRecordIdentifierTypeDef, BatchGetRecordIdentifierOutputTypeDef
]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListRecordsResponseTypeDef(TypedDict):
    RecordIdentifiers: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BatchGetRecordResultDetailTypeDef(TypedDict):
    FeatureGroupName: str
    RecordIdentifierValueAsString: str
    Record: list[FeatureValueOutputTypeDef]
    ExpiresAt: NotRequired[str]

class GetRecordResponseTypeDef(TypedDict):
    Record: list[FeatureValueOutputTypeDef]
    ExpiresAt: str
    ResponseMetadata: ResponseMetadataTypeDef

class BatchWriteRecordEntryOutputTypeDef(TypedDict):
    FeatureGroupName: str
    Record: list[FeatureValueOutputTypeDef]
    TargetStores: NotRequired[list[TargetStoreType]]
    TtlDuration: NotRequired[TtlDurationTypeDef]

FeatureValueUnionTypeDef = Union[FeatureValueTypeDef, FeatureValueOutputTypeDef]

class ListRecordsRequestPaginateTypeDef(TypedDict):
    FeatureGroupName: str
    IncludeSoftDeletedRecords: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class BatchGetRecordRequestTypeDef(TypedDict):
    Identifiers: Sequence[BatchGetRecordIdentifierUnionTypeDef]
    ExpirationTimeResponse: NotRequired[ExpirationTimeResponseType]

class BatchGetRecordResponseTypeDef(TypedDict):
    Records: list[BatchGetRecordResultDetailTypeDef]
    Errors: list[BatchGetRecordErrorTypeDef]
    UnprocessedIdentifiers: list[BatchGetRecordIdentifierOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchWriteRecordErrorTypeDef(TypedDict):
    Entry: BatchWriteRecordEntryOutputTypeDef
    ErrorCode: str
    ErrorMessage: str

class BatchWriteRecordEntryTypeDef(TypedDict):
    FeatureGroupName: str
    Record: Sequence[FeatureValueUnionTypeDef]
    TargetStores: NotRequired[Sequence[TargetStoreType]]
    TtlDuration: NotRequired[TtlDurationTypeDef]

class PutRecordRequestTypeDef(TypedDict):
    FeatureGroupName: str
    Record: Sequence[FeatureValueUnionTypeDef]
    TargetStores: NotRequired[Sequence[TargetStoreType]]
    TtlDuration: NotRequired[TtlDurationTypeDef]

class UpdateRecordRequestTypeDef(TypedDict):
    FeatureGroupName: str
    RecordIdentifierValueAsString: str
    Features: Sequence[FeatureValueUnionTypeDef]
    TargetStores: NotRequired[Sequence[TargetStoreType]]
    TtlDuration: NotRequired[TtlDurationTypeDef]

class BatchWriteRecordResponseTypeDef(TypedDict):
    Errors: list[BatchWriteRecordErrorTypeDef]
    UnprocessedEntries: list[BatchWriteRecordEntryOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

BatchWriteRecordEntryUnionTypeDef = Union[
    BatchWriteRecordEntryTypeDef, BatchWriteRecordEntryOutputTypeDef
]

class BatchWriteRecordRequestTypeDef(TypedDict):
    Entries: Sequence[BatchWriteRecordEntryUnionTypeDef]
    TtlDuration: NotRequired[TtlDurationTypeDef]
