"""
Type annotations for dynamodb service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dynamodb.client import DynamoDBClient
    from types_aiobotocore_dynamodb.paginator import (
        ListBackupsPaginator,
        ListTablesPaginator,
        ListTagsOfResourcePaginator,
        QueryPaginator,
        ScanPaginator,
    )

    session = get_session()
    with session.create_client("dynamodb") as client:
        client: DynamoDBClient

        list_backups_paginator: ListBackupsPaginator = client.get_paginator("list_backups")
        list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
        list_tags_of_resource_paginator: ListTagsOfResourcePaginator = client.get_paginator("list_tags_of_resource")
        query_paginator: QueryPaginator = client.get_paginator("query")
        scan_paginator: ScanPaginator = client.get_paginator("scan")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListBackupsInputPaginateTypeDef,
    ListBackupsOutputTypeDef,
    ListTablesInputPaginateTypeDef,
    ListTablesOutputTypeDef,
    ListTagsOfResourceInputPaginateTypeDef,
    ListTagsOfResourceOutputTypeDef,
    QueryInputPaginateTypeDef,
    QueryOutputTypeDef,
    ScanInputPaginateTypeDef,
    ScanOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListBackupsPaginator",
    "ListTablesPaginator",
    "ListTagsOfResourcePaginator",
    "QueryPaginator",
    "ScanPaginator",
)


if TYPE_CHECKING:
    _ListBackupsPaginatorBase = AioPaginator[ListBackupsOutputTypeDef]
else:
    _ListBackupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBackupsPaginator(_ListBackupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/ListBackups.html#DynamoDB.Paginator.ListBackups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#listbackupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBackupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBackupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/ListBackups.html#DynamoDB.Paginator.ListBackups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#listbackupspaginator)
        """


if TYPE_CHECKING:
    _ListTablesPaginatorBase = AioPaginator[ListTablesOutputTypeDef]
else:
    _ListTablesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTablesPaginator(_ListTablesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/ListTables.html#DynamoDB.Paginator.ListTables)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#listtablespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTablesInputPaginateTypeDef]
    ) -> AioPageIterator[ListTablesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/ListTables.html#DynamoDB.Paginator.ListTables.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#listtablespaginator)
        """


if TYPE_CHECKING:
    _ListTagsOfResourcePaginatorBase = AioPaginator[ListTagsOfResourceOutputTypeDef]
else:
    _ListTagsOfResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsOfResourcePaginator(_ListTagsOfResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/ListTagsOfResource.html#DynamoDB.Paginator.ListTagsOfResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#listtagsofresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsOfResourceInputPaginateTypeDef]
    ) -> AioPageIterator[ListTagsOfResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/ListTagsOfResource.html#DynamoDB.Paginator.ListTagsOfResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#listtagsofresourcepaginator)
        """


if TYPE_CHECKING:
    _QueryPaginatorBase = AioPaginator[QueryOutputTypeDef]
else:
    _QueryPaginatorBase = AioPaginator  # type: ignore[assignment]


class QueryPaginator(_QueryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/Query.html#DynamoDB.Paginator.Query)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#querypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[QueryInputPaginateTypeDef]
    ) -> AioPageIterator[QueryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/Query.html#DynamoDB.Paginator.Query.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#querypaginator)
        """


if TYPE_CHECKING:
    _ScanPaginatorBase = AioPaginator[ScanOutputTypeDef]
else:
    _ScanPaginatorBase = AioPaginator  # type: ignore[assignment]


class ScanPaginator(_ScanPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/Scan.html#DynamoDB.Paginator.Scan)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#scanpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ScanInputPaginateTypeDef]
    ) -> AioPageIterator[ScanOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/paginator/Scan.html#DynamoDB.Paginator.Scan.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/paginators/#scanpaginator)
        """
