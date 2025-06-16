"""
Type annotations for s3tables service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3tables.client import S3TablesClient
    from types_aiobotocore_s3tables.paginator import (
        ListNamespacesPaginator,
        ListTableBucketsPaginator,
        ListTablesPaginator,
    )

    session = get_session()
    with session.create_client("s3tables") as client:
        client: S3TablesClient

        list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
        list_table_buckets_paginator: ListTableBucketsPaginator = client.get_paginator("list_table_buckets")
        list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListNamespacesRequestPaginateTypeDef,
    ListNamespacesResponseTypeDef,
    ListTableBucketsRequestPaginateTypeDef,
    ListTableBucketsResponseTypeDef,
    ListTablesRequestPaginateTypeDef,
    ListTablesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListNamespacesPaginator", "ListTableBucketsPaginator", "ListTablesPaginator")

if TYPE_CHECKING:
    _ListNamespacesPaginatorBase = AioPaginator[ListNamespacesResponseTypeDef]
else:
    _ListNamespacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNamespacesPaginator(_ListNamespacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListNamespaces.html#S3Tables.Paginator.ListNamespaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listnamespacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNamespacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListNamespaces.html#S3Tables.Paginator.ListNamespaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listnamespacespaginator)
        """

if TYPE_CHECKING:
    _ListTableBucketsPaginatorBase = AioPaginator[ListTableBucketsResponseTypeDef]
else:
    _ListTableBucketsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTableBucketsPaginator(_ListTableBucketsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTableBuckets.html#S3Tables.Paginator.ListTableBuckets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listtablebucketspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTableBucketsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTableBucketsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTableBuckets.html#S3Tables.Paginator.ListTableBuckets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listtablebucketspaginator)
        """

if TYPE_CHECKING:
    _ListTablesPaginatorBase = AioPaginator[ListTablesResponseTypeDef]
else:
    _ListTablesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTablesPaginator(_ListTablesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTables.html#S3Tables.Paginator.ListTables)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listtablespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTablesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTablesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTables.html#S3Tables.Paginator.ListTables.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listtablespaginator)
        """
