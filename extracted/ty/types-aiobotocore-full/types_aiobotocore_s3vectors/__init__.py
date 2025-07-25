"""
Main interface for s3vectors service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3vectors/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3vectors import (
        Client,
        ListIndexesPaginator,
        ListVectorBucketsPaginator,
        ListVectorsPaginator,
        S3VectorsClient,
    )

    session = get_session()
    async with session.create_client("s3vectors") as client:
        client: S3VectorsClient
        ...


    list_indexes_paginator: ListIndexesPaginator = client.get_paginator("list_indexes")
    list_vector_buckets_paginator: ListVectorBucketsPaginator = client.get_paginator("list_vector_buckets")
    list_vectors_paginator: ListVectorsPaginator = client.get_paginator("list_vectors")
    ```
"""

from .client import S3VectorsClient
from .paginator import ListIndexesPaginator, ListVectorBucketsPaginator, ListVectorsPaginator

Client = S3VectorsClient


__all__ = (
    "Client",
    "ListIndexesPaginator",
    "ListVectorBucketsPaginator",
    "ListVectorsPaginator",
    "S3VectorsClient",
)
