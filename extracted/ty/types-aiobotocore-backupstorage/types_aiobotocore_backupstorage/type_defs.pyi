"""
Type annotations for backupstorage service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/type_defs/)

Usage::

    ```python
    from types_aiobotocore_backupstorage.type_defs import BackupObjectTypeDef

    data: BackupObjectTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Union

from aiobotocore.response import StreamingBody

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BackupObjectTypeDef",
    "BlobTypeDef",
    "ChunkTypeDef",
    "DeleteObjectInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GetChunkInputRequestTypeDef",
    "GetObjectMetadataInputRequestTypeDef",
    "ListChunksInputRequestTypeDef",
    "TimestampTypeDef",
    "StartObjectInputRequestTypeDef",
    "NotifyObjectCompleteInputRequestTypeDef",
    "PutChunkInputRequestTypeDef",
    "PutObjectInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetChunkOutputTypeDef",
    "GetObjectMetadataOutputTypeDef",
    "ListChunksOutputTypeDef",
    "ListObjectsOutputTypeDef",
    "NotifyObjectCompleteOutputTypeDef",
    "PutChunkOutputTypeDef",
    "PutObjectOutputTypeDef",
    "StartObjectOutputTypeDef",
    "ListObjectsInputRequestTypeDef",
)

BackupObjectTypeDef = TypedDict(
    "BackupObjectTypeDef",
    {
        "Name": str,
        "ObjectChecksum": str,
        "ObjectChecksumAlgorithm": Literal["SUMMARY"],
        "ObjectToken": str,
        "ChunksCount": NotRequired[int],
        "MetadataString": NotRequired[str],
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ChunkTypeDef = TypedDict(
    "ChunkTypeDef",
    {
        "Index": int,
        "Length": int,
        "Checksum": str,
        "ChecksumAlgorithm": Literal["SHA256"],
        "ChunkToken": str,
    },
)
DeleteObjectInputRequestTypeDef = TypedDict(
    "DeleteObjectInputRequestTypeDef",
    {
        "BackupJobId": str,
        "ObjectName": str,
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
GetChunkInputRequestTypeDef = TypedDict(
    "GetChunkInputRequestTypeDef",
    {
        "StorageJobId": str,
        "ChunkToken": str,
    },
)
GetObjectMetadataInputRequestTypeDef = TypedDict(
    "GetObjectMetadataInputRequestTypeDef",
    {
        "StorageJobId": str,
        "ObjectToken": str,
    },
)
ListChunksInputRequestTypeDef = TypedDict(
    "ListChunksInputRequestTypeDef",
    {
        "StorageJobId": str,
        "ObjectToken": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
TimestampTypeDef = Union[datetime, str]
StartObjectInputRequestTypeDef = TypedDict(
    "StartObjectInputRequestTypeDef",
    {
        "BackupJobId": str,
        "ObjectName": str,
        "ThrowOnDuplicate": NotRequired[bool],
    },
)
NotifyObjectCompleteInputRequestTypeDef = TypedDict(
    "NotifyObjectCompleteInputRequestTypeDef",
    {
        "BackupJobId": str,
        "UploadId": str,
        "ObjectChecksum": str,
        "ObjectChecksumAlgorithm": Literal["SUMMARY"],
        "MetadataString": NotRequired[str],
        "MetadataBlob": NotRequired[BlobTypeDef],
        "MetadataBlobLength": NotRequired[int],
        "MetadataBlobChecksum": NotRequired[str],
        "MetadataBlobChecksumAlgorithm": NotRequired[Literal["SHA256"]],
    },
)
PutChunkInputRequestTypeDef = TypedDict(
    "PutChunkInputRequestTypeDef",
    {
        "BackupJobId": str,
        "UploadId": str,
        "ChunkIndex": int,
        "Data": BlobTypeDef,
        "Length": int,
        "Checksum": str,
        "ChecksumAlgorithm": Literal["SHA256"],
    },
)
PutObjectInputRequestTypeDef = TypedDict(
    "PutObjectInputRequestTypeDef",
    {
        "BackupJobId": str,
        "ObjectName": str,
        "MetadataString": NotRequired[str],
        "InlineChunk": NotRequired[BlobTypeDef],
        "InlineChunkLength": NotRequired[int],
        "InlineChunkChecksum": NotRequired[str],
        "InlineChunkChecksumAlgorithm": NotRequired[str],
        "ObjectChecksum": NotRequired[str],
        "ObjectChecksumAlgorithm": NotRequired[Literal["SUMMARY"]],
        "ThrowOnDuplicate": NotRequired[bool],
    },
)
EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetChunkOutputTypeDef = TypedDict(
    "GetChunkOutputTypeDef",
    {
        "Data": StreamingBody,
        "Length": int,
        "Checksum": str,
        "ChecksumAlgorithm": Literal["SHA256"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetObjectMetadataOutputTypeDef = TypedDict(
    "GetObjectMetadataOutputTypeDef",
    {
        "MetadataString": str,
        "MetadataBlob": StreamingBody,
        "MetadataBlobLength": int,
        "MetadataBlobChecksum": str,
        "MetadataBlobChecksumAlgorithm": Literal["SHA256"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListChunksOutputTypeDef = TypedDict(
    "ListChunksOutputTypeDef",
    {
        "ChunkList": List[ChunkTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListObjectsOutputTypeDef = TypedDict(
    "ListObjectsOutputTypeDef",
    {
        "ObjectList": List[BackupObjectTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
NotifyObjectCompleteOutputTypeDef = TypedDict(
    "NotifyObjectCompleteOutputTypeDef",
    {
        "ObjectChecksum": str,
        "ObjectChecksumAlgorithm": Literal["SUMMARY"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutChunkOutputTypeDef = TypedDict(
    "PutChunkOutputTypeDef",
    {
        "ChunkChecksum": str,
        "ChunkChecksumAlgorithm": Literal["SHA256"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutObjectOutputTypeDef = TypedDict(
    "PutObjectOutputTypeDef",
    {
        "InlineChunkChecksum": str,
        "InlineChunkChecksumAlgorithm": Literal["SHA256"],
        "ObjectChecksum": str,
        "ObjectChecksumAlgorithm": Literal["SUMMARY"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartObjectOutputTypeDef = TypedDict(
    "StartObjectOutputTypeDef",
    {
        "UploadId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListObjectsInputRequestTypeDef = TypedDict(
    "ListObjectsInputRequestTypeDef",
    {
        "StorageJobId": str,
        "StartingObjectName": NotRequired[str],
        "StartingObjectPrefix": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "CreatedBefore": NotRequired[TimestampTypeDef],
        "CreatedAfter": NotRequired[TimestampTypeDef],
    },
)
