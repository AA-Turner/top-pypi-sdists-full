"""
Main interface for dynamodb service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dynamodb/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_dynamodb import (
        Client,
        ContributorInsightsEnabledWaiter,
        DynamoDBClient,
        DynamoDBServiceResource,
        ExportCompletedWaiter,
        ImportCompletedWaiter,
        KinesisStreamingDestinationActiveWaiter,
        ListBackupsPaginator,
        ListTablesPaginator,
        ListTagsOfResourcePaginator,
        QueryPaginator,
        ScanPaginator,
        ServiceResource,
        TableExistsWaiter,
        TableNotExistsWaiter,
    )

    session = Session()
    client: DynamoDBClient = session.client("dynamodb")

    resource: DynamoDBServiceResource = session.resource("dynamodb")

    contributor_insights_enabled_waiter: ContributorInsightsEnabledWaiter = client.get_waiter("contributor_insights_enabled")
    export_completed_waiter: ExportCompletedWaiter = client.get_waiter("export_completed")
    import_completed_waiter: ImportCompletedWaiter = client.get_waiter("import_completed")
    kinesis_streaming_destination_active_waiter: KinesisStreamingDestinationActiveWaiter = client.get_waiter("kinesis_streaming_destination_active")
    table_exists_waiter: TableExistsWaiter = client.get_waiter("table_exists")
    table_not_exists_waiter: TableNotExistsWaiter = client.get_waiter("table_not_exists")

    list_backups_paginator: ListBackupsPaginator = client.get_paginator("list_backups")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    list_tags_of_resource_paginator: ListTagsOfResourcePaginator = client.get_paginator("list_tags_of_resource")
    query_paginator: QueryPaginator = client.get_paginator("query")
    scan_paginator: ScanPaginator = client.get_paginator("scan")
    ```
"""

from .client import DynamoDBClient
from .paginator import (
    ListBackupsPaginator,
    ListTablesPaginator,
    ListTagsOfResourcePaginator,
    QueryPaginator,
    ScanPaginator,
)
from .waiter import (
    ContributorInsightsEnabledWaiter,
    ExportCompletedWaiter,
    ImportCompletedWaiter,
    KinesisStreamingDestinationActiveWaiter,
    TableExistsWaiter,
    TableNotExistsWaiter,
)

try:
    from .service_resource import DynamoDBServiceResource
except ImportError:
    from builtins import object as DynamoDBServiceResource  # type: ignore[assignment]


Client = DynamoDBClient


ServiceResource = DynamoDBServiceResource


__all__ = (
    "Client",
    "ContributorInsightsEnabledWaiter",
    "DynamoDBClient",
    "DynamoDBServiceResource",
    "ExportCompletedWaiter",
    "ImportCompletedWaiter",
    "KinesisStreamingDestinationActiveWaiter",
    "ListBackupsPaginator",
    "ListTablesPaginator",
    "ListTagsOfResourcePaginator",
    "QueryPaginator",
    "ScanPaginator",
    "ServiceResource",
    "TableExistsWaiter",
    "TableNotExistsWaiter",
)
