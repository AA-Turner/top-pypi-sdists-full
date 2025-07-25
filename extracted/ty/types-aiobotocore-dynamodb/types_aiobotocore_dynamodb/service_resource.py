"""
Type annotations for dynamodb service ServiceResource.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dynamodb.service_resource import DynamoDBServiceResource
    import types_aiobotocore_dynamodb.service_resource as dynamodb_resources

    session = get_session()
    async with session.resource("dynamodb") as resource:
        resource: DynamoDBServiceResource

        my_table: dynamodb_resources.Table = resource.Table(...)
```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import NoReturn

from aioboto3.resources.base import AIOBoto3ServiceResource
from aioboto3.resources.collection import AIOResourceCollection

from .client import DynamoDBClient
from .literals import MultiRegionConsistencyType, TableStatusType
from .type_defs import (
    ArchivalSummaryTypeDef,
    AttributeDefinitionTypeDef,
    BatchGetItemInputServiceResourceBatchGetItemTypeDef,
    BatchGetItemOutputServiceResourceTypeDef,
    BatchWriteItemInputServiceResourceBatchWriteItemTypeDef,
    BatchWriteItemOutputServiceResourceTypeDef,
    BillingModeSummaryTypeDef,
    CreateTableInputServiceResourceCreateTableTypeDef,
    DeleteItemInputTableDeleteItemTypeDef,
    DeleteItemOutputTableTypeDef,
    DeleteTableOutputTypeDef,
    GetItemInputTableGetItemTypeDef,
    GetItemOutputTableTypeDef,
    GlobalSecondaryIndexDescriptionTypeDef,
    GlobalTableWitnessDescriptionTypeDef,
    KeySchemaElementTypeDef,
    LocalSecondaryIndexDescriptionTypeDef,
    OnDemandThroughputTypeDef,
    ProvisionedThroughputDescriptionTypeDef,
    PutItemInputTablePutItemTypeDef,
    PutItemOutputTableTypeDef,
    QueryInputTableQueryTypeDef,
    QueryOutputTableTypeDef,
    ReplicaDescriptionTypeDef,
    RestoreSummaryTypeDef,
    ScanInputTableScanTypeDef,
    ScanOutputTableTypeDef,
    SSEDescriptionTypeDef,
    StreamSpecificationTypeDef,
    TableClassSummaryTypeDef,
    TableWarmThroughputDescriptionTypeDef,
    UpdateItemInputTableUpdateItemTypeDef,
    UpdateItemOutputTableTypeDef,
    UpdateTableInputTableUpdateTypeDef,
)

try:
    from aioboto3.dynamodb.table import BatchWriter
except ImportError:
    from builtins import object as BatchWriter  # type: ignore[assignment]
try:
    from boto3.resources.base import ResourceMeta
except ImportError:
    from builtins import object as ResourceMeta  # type: ignore[assignment]
if sys.version_info >= (3, 9):
    from builtins import list as List
    from collections.abc import AsyncIterator, Awaitable, Sequence
else:
    from typing import AsyncIterator, Awaitable, List, Sequence
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DynamoDBServiceResource", "ServiceResourceTablesCollection", "Table")


class ServiceResourceTablesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/tables.html#DynamoDB.ServiceResource.tables)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#serviceresourcetablescollection)
    """

    def all(self) -> ServiceResourceTablesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/tables.html#DynamoDB.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def filter(  # type: ignore[override]
        self, *, ExclusiveStartTableName: str = ..., Limit: int = ...
    ) -> ServiceResourceTablesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/tables.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def limit(self, count: int) -> ServiceResourceTablesCollection:
        """
        Return at most this many Tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/tables.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def page_size(self, count: int) -> ServiceResourceTablesCollection:
        """
        Fetch at most this many Tables per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/tables.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Table]]:
        """
        A generator which yields pages of Tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/tables.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/tables.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def __aiter__(self) -> AsyncIterator[Table]:
        """
        A generator which yields Tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/tables.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#serviceresourcetablescollection)
        """


class Table(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html#DynamoDB.Table)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#table)
    """

    name: str
    attribute_definitions: Awaitable[List[AttributeDefinitionTypeDef]]
    table_name: Awaitable[str]
    key_schema: Awaitable[List[KeySchemaElementTypeDef]]
    table_status: Awaitable[TableStatusType]
    creation_date_time: Awaitable[datetime]
    provisioned_throughput: Awaitable[ProvisionedThroughputDescriptionTypeDef]
    table_size_bytes: Awaitable[int]
    item_count: Awaitable[int]
    table_arn: Awaitable[str]
    table_id: Awaitable[str]
    billing_mode_summary: Awaitable[BillingModeSummaryTypeDef]
    local_secondary_indexes: Awaitable[List[LocalSecondaryIndexDescriptionTypeDef]]
    global_secondary_indexes: Awaitable[List[GlobalSecondaryIndexDescriptionTypeDef]]
    stream_specification: Awaitable[StreamSpecificationTypeDef]
    latest_stream_label: Awaitable[str]
    latest_stream_arn: Awaitable[str]
    global_table_version: Awaitable[str]
    replicas: Awaitable[List[ReplicaDescriptionTypeDef]]
    global_table_witnesses: Awaitable[List[GlobalTableWitnessDescriptionTypeDef]]
    restore_summary: Awaitable[RestoreSummaryTypeDef]
    sse_description: Awaitable[SSEDescriptionTypeDef]
    archival_summary: Awaitable[ArchivalSummaryTypeDef]
    table_class_summary: Awaitable[TableClassSummaryTypeDef]
    deletion_protection_enabled: Awaitable[bool]
    on_demand_throughput: Awaitable[OnDemandThroughputTypeDef]
    warm_throughput: Awaitable[TableWarmThroughputDescriptionTypeDef]
    multi_region_consistency: Awaitable[MultiRegionConsistencyType]
    meta: DynamoDBResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tableget_available_subresources-method)
        """

    async def delete(self) -> DeleteTableOutputTypeDef:
        """
        The <code>DeleteTable</code> operation deletes a table and all of its items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tabledelete-method)
        """

    async def delete_item(
        self, **kwargs: Unpack[DeleteItemInputTableDeleteItemTypeDef]
    ) -> DeleteItemOutputTableTypeDef:
        """
        Deletes a single item in a table by primary key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/delete_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tabledelete_item-method)
        """

    async def get_item(
        self, **kwargs: Unpack[GetItemInputTableGetItemTypeDef]
    ) -> GetItemOutputTableTypeDef:
        """
        The <code>GetItem</code> operation returns a set of attributes for the item
        with the given primary key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tableget_item-method)
        """

    async def put_item(
        self, **kwargs: Unpack[PutItemInputTablePutItemTypeDef]
    ) -> PutItemOutputTableTypeDef:
        """
        Creates a new item, or replaces an old item with a new item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/put_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tableput_item-method)
        """

    async def query(self, **kwargs: Unpack[QueryInputTableQueryTypeDef]) -> QueryOutputTableTypeDef:
        """
        You must provide the name of the partition key attribute and a single value for
        that attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/query.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tablequery-method)
        """

    async def scan(self, **kwargs: Unpack[ScanInputTableScanTypeDef]) -> ScanOutputTableTypeDef:
        """
        The <code>Scan</code> operation returns one or more items and item attributes
        by accessing every item in a table or a secondary index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/scan.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tablescan-method)
        """

    async def update(self, **kwargs: Unpack[UpdateTableInputTableUpdateTypeDef]) -> _Table:
        """
        Modifies the provisioned throughput settings, global secondary indexes, or
        DynamoDB Streams settings for a given table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/update.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tableupdate-method)
        """

    async def update_item(
        self, **kwargs: Unpack[UpdateItemInputTableUpdateItemTypeDef]
    ) -> UpdateItemOutputTableTypeDef:
        """
        Edits an existing item's attributes, or adds a new item to the table if it does
        not already exist.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/update_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tableupdate_item-method)
        """

    async def wait_until_exists(self) -> None:
        """
        Waits until Table is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/wait_until_exists.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tablewait_until_exists-method)
        """

    async def wait_until_not_exists(self) -> None:
        """
        Waits until Table is not_exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/wait_until_not_exists.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tablewait_until_not_exists-method)
        """

    def batch_writer(
        self,
        overwrite_by_pkeys: List[str] | None = ...,
        flush_amount: int = ...,
        on_exit_loop_sleep: int = ...,
    ) -> BatchWriter:
        """
        Create a batch writer object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/batch_writer.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tablebatch_writer-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tableload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#tablereload-method)
        """


_Table = Table


class DynamoDBResourceMeta(ResourceMeta):
    client: DynamoDBClient  # type: ignore[override]


class DynamoDBServiceResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/index.html)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/)
    """

    meta: DynamoDBResourceMeta  # type: ignore[override]
    tables: ServiceResourceTablesCollection

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#dynamodbserviceresourceget_available_subresources-method)
        """

    async def batch_get_item(
        self, **kwargs: Unpack[BatchGetItemInputServiceResourceBatchGetItemTypeDef]
    ) -> BatchGetItemOutputServiceResourceTypeDef:
        """
        The <code>BatchGetItem</code> operation returns the attributes of one or more
        items from one or more tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/batch_get_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#dynamodbserviceresourcebatch_get_item-method)
        """

    async def batch_write_item(
        self, **kwargs: Unpack[BatchWriteItemInputServiceResourceBatchWriteItemTypeDef]
    ) -> BatchWriteItemOutputServiceResourceTypeDef:
        """
        The <code>BatchWriteItem</code> operation puts or deletes multiple items in one
        or more tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/batch_write_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#dynamodbserviceresourcebatch_write_item-method)
        """

    async def create_table(
        self, **kwargs: Unpack[CreateTableInputServiceResourceCreateTableTypeDef]
    ) -> _Table:
        """
        The <code>CreateTable</code> operation adds a new table to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/create_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#dynamodbserviceresourcecreate_table-method)
        """

    async def Table(self, name: str) -> _Table:
        """
        Creates a Table resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/service-resource/Table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/service_resource/#dynamodbserviceresourcetable-method)
        """
