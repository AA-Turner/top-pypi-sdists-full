"""
Type annotations for backupstorage service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_backupstorage.client import BackupStorageClient

    session = get_session()
    async with session.create_client("backupstorage") as client:
        client: BackupStorageClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    BlobTypeDef,
    EmptyResponseMetadataTypeDef,
    GetChunkOutputTypeDef,
    GetObjectMetadataOutputTypeDef,
    ListChunksOutputTypeDef,
    ListObjectsOutputTypeDef,
    NotifyObjectCompleteOutputTypeDef,
    PutChunkOutputTypeDef,
    PutObjectOutputTypeDef,
    StartObjectOutputTypeDef,
    TimestampTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("BackupStorageClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DataAlreadyExistsException: Type[BotocoreClientError]
    IllegalArgumentException: Type[BotocoreClientError]
    KMSInvalidKeyUsageException: Type[BotocoreClientError]
    NotReadableInputStreamException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    RetryableException: Type[BotocoreClientError]
    ServiceInternalException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class BackupStorageClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BackupStorageClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#close)
        """

    async def delete_object(
        self, *, BackupJobId: str, ObjectName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete Object from the incremental base Backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.delete_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#delete_object)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#generate_presigned_url)
        """

    async def get_chunk(self, *, StorageJobId: str, ChunkToken: str) -> GetChunkOutputTypeDef:
        """
        Gets the specified object's chunk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.get_chunk)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#get_chunk)
        """

    async def get_object_metadata(
        self, *, StorageJobId: str, ObjectToken: str
    ) -> GetObjectMetadataOutputTypeDef:
        """
        Get metadata associated with an Object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.get_object_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#get_object_metadata)
        """

    async def list_chunks(
        self, *, StorageJobId: str, ObjectToken: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListChunksOutputTypeDef:
        """
        List chunks in a given Object See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/backupstorage-2018-04-10/ListChunks).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.list_chunks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#list_chunks)
        """

    async def list_objects(
        self,
        *,
        StorageJobId: str,
        StartingObjectName: str = ...,
        StartingObjectPrefix: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        CreatedBefore: TimestampTypeDef = ...,
        CreatedAfter: TimestampTypeDef = ...,
    ) -> ListObjectsOutputTypeDef:
        """
        List all Objects in a given Backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.list_objects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#list_objects)
        """

    async def notify_object_complete(
        self,
        *,
        BackupJobId: str,
        UploadId: str,
        ObjectChecksum: str,
        ObjectChecksumAlgorithm: Literal["SUMMARY"],
        MetadataString: str = ...,
        MetadataBlob: BlobTypeDef = ...,
        MetadataBlobLength: int = ...,
        MetadataBlobChecksum: str = ...,
        MetadataBlobChecksumAlgorithm: Literal["SHA256"] = ...,
    ) -> NotifyObjectCompleteOutputTypeDef:
        """
        Complete upload See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/backupstorage-2018-04-10/NotifyObjectComplete).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.notify_object_complete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#notify_object_complete)
        """

    async def put_chunk(
        self,
        *,
        BackupJobId: str,
        UploadId: str,
        ChunkIndex: int,
        Data: BlobTypeDef,
        Length: int,
        Checksum: str,
        ChecksumAlgorithm: Literal["SHA256"],
    ) -> PutChunkOutputTypeDef:
        """
        Upload chunk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.put_chunk)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#put_chunk)
        """

    async def put_object(
        self,
        *,
        BackupJobId: str,
        ObjectName: str,
        MetadataString: str = ...,
        InlineChunk: BlobTypeDef = ...,
        InlineChunkLength: int = ...,
        InlineChunkChecksum: str = ...,
        InlineChunkChecksumAlgorithm: str = ...,
        ObjectChecksum: str = ...,
        ObjectChecksumAlgorithm: Literal["SUMMARY"] = ...,
        ThrowOnDuplicate: bool = ...,
    ) -> PutObjectOutputTypeDef:
        """
        Upload object that can store object metadata String and data blob in single API
        call using inline chunk
        field.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.put_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#put_object)
        """

    async def start_object(
        self, *, BackupJobId: str, ObjectName: str, ThrowOnDuplicate: bool = ...
    ) -> StartObjectOutputTypeDef:
        """
        Start upload containing one or many chunks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client.start_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/#start_object)
        """

    async def __aenter__(self) -> "BackupStorageClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupstorage.html#BackupStorage.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/client/)
        """
