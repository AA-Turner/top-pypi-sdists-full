"""
Type annotations for timestream-write service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_timestream_write.client import TimestreamWriteClient

    session = get_session()
    async with session.create_client("timestream-write") as client:
        client: TimestreamWriteClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CreateBatchLoadTaskRequestTypeDef,
    CreateBatchLoadTaskResponseTypeDef,
    CreateDatabaseRequestTypeDef,
    CreateDatabaseResponseTypeDef,
    CreateTableRequestTypeDef,
    CreateTableResponseTypeDef,
    DeleteDatabaseRequestTypeDef,
    DeleteTableRequestTypeDef,
    DescribeBatchLoadTaskRequestTypeDef,
    DescribeBatchLoadTaskResponseTypeDef,
    DescribeDatabaseRequestTypeDef,
    DescribeDatabaseResponseTypeDef,
    DescribeEndpointsResponseTypeDef,
    DescribeTableRequestTypeDef,
    DescribeTableResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ListBatchLoadTasksRequestTypeDef,
    ListBatchLoadTasksResponseTypeDef,
    ListDatabasesRequestTypeDef,
    ListDatabasesResponseTypeDef,
    ListTablesRequestTypeDef,
    ListTablesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ResumeBatchLoadTaskRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDatabaseRequestTypeDef,
    UpdateDatabaseResponseTypeDef,
    UpdateTableRequestTypeDef,
    UpdateTableResponseTypeDef,
    WriteRecordsRequestTypeDef,
    WriteRecordsResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("TimestreamWriteClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidEndpointException: Type[BotocoreClientError]
    RejectedRecordsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class TimestreamWriteClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write.html#TimestreamWrite.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TimestreamWriteClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write.html#TimestreamWrite.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#generate_presigned_url)
        """

    async def create_batch_load_task(
        self, **kwargs: Unpack[CreateBatchLoadTaskRequestTypeDef]
    ) -> CreateBatchLoadTaskResponseTypeDef:
        """
        Creates a new Timestream batch load task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/create_batch_load_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#create_batch_load_task)
        """

    async def create_database(
        self, **kwargs: Unpack[CreateDatabaseRequestTypeDef]
    ) -> CreateDatabaseResponseTypeDef:
        """
        Creates a new Timestream database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/create_database.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#create_database)
        """

    async def create_table(
        self, **kwargs: Unpack[CreateTableRequestTypeDef]
    ) -> CreateTableResponseTypeDef:
        """
        Adds a new table to an existing database in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/create_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#create_table)
        """

    async def delete_database(
        self, **kwargs: Unpack[DeleteDatabaseRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a given Timestream database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/delete_database.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#delete_database)
        """

    async def delete_table(
        self, **kwargs: Unpack[DeleteTableRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a given Timestream table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/delete_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#delete_table)
        """

    async def describe_batch_load_task(
        self, **kwargs: Unpack[DescribeBatchLoadTaskRequestTypeDef]
    ) -> DescribeBatchLoadTaskResponseTypeDef:
        """
        Returns information about the batch load task, including configurations,
        mappings, progress, and other details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/describe_batch_load_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#describe_batch_load_task)
        """

    async def describe_database(
        self, **kwargs: Unpack[DescribeDatabaseRequestTypeDef]
    ) -> DescribeDatabaseResponseTypeDef:
        """
        Returns information about the database, including the database name, time that
        the database was created, and the total number of tables found within the
        database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/describe_database.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#describe_database)
        """

    async def describe_endpoints(self) -> DescribeEndpointsResponseTypeDef:
        """
        Returns a list of available endpoints to make Timestream API calls against.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/describe_endpoints.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#describe_endpoints)
        """

    async def describe_table(
        self, **kwargs: Unpack[DescribeTableRequestTypeDef]
    ) -> DescribeTableResponseTypeDef:
        """
        Returns information about the table, including the table name, database name,
        retention duration of the memory store and the magnetic store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/describe_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#describe_table)
        """

    async def list_batch_load_tasks(
        self, **kwargs: Unpack[ListBatchLoadTasksRequestTypeDef]
    ) -> ListBatchLoadTasksResponseTypeDef:
        """
        Provides a list of batch load tasks, along with the name, status, when the task
        is resumable until, and other details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/list_batch_load_tasks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#list_batch_load_tasks)
        """

    async def list_databases(
        self, **kwargs: Unpack[ListDatabasesRequestTypeDef]
    ) -> ListDatabasesResponseTypeDef:
        """
        Returns a list of your Timestream databases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/list_databases.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#list_databases)
        """

    async def list_tables(
        self, **kwargs: Unpack[ListTablesRequestTypeDef]
    ) -> ListTablesResponseTypeDef:
        """
        Provides a list of tables, along with the name, status, and retention
        properties of each table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/list_tables.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#list_tables)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags on a Timestream resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#list_tags_for_resource)
        """

    async def resume_batch_load_task(
        self, **kwargs: Unpack[ResumeBatchLoadTaskRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/resume_batch_load_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#resume_batch_load_task)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates a set of tags with a Timestream resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the association of tags from a Timestream resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#untag_resource)
        """

    async def update_database(
        self, **kwargs: Unpack[UpdateDatabaseRequestTypeDef]
    ) -> UpdateDatabaseResponseTypeDef:
        """
        Modifies the KMS key for an existing database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/update_database.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#update_database)
        """

    async def update_table(
        self, **kwargs: Unpack[UpdateTableRequestTypeDef]
    ) -> UpdateTableResponseTypeDef:
        """
        Modifies the retention duration of the memory store and magnetic store for your
        Timestream table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/update_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#update_table)
        """

    async def write_records(
        self, **kwargs: Unpack[WriteRecordsRequestTypeDef]
    ) -> WriteRecordsResponseTypeDef:
        """
        Enables you to write your time-series data into Timestream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write/client/write_records.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/#write_records)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write.html#TimestreamWrite.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-write.html#TimestreamWrite.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_write/client/)
        """
