"""
Main interface for s3tables service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3tables import (
        Client,
        ListNamespacesPaginator,
        ListTableBucketsPaginator,
        ListTablesPaginator,
        S3TablesClient,
    )

    session = get_session()
    async with session.create_client("s3tables") as client:
        client: S3TablesClient
        ...


    list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
    list_table_buckets_paginator: ListTableBucketsPaginator = client.get_paginator("list_table_buckets")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```
"""

from .client import S3TablesClient
from .paginator import ListNamespacesPaginator, ListTableBucketsPaginator, ListTablesPaginator

Client = S3TablesClient

__all__ = (
    "Client",
    "ListNamespacesPaginator",
    "ListTableBucketsPaginator",
    "ListTablesPaginator",
    "S3TablesClient",
)
