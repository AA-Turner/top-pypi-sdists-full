"""
Type annotations for s3vectors service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3vectors/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3vectors.client import S3VectorsClient
    from types_aiobotocore_s3vectors.paginator import (
        ListIndexesPaginator,
        ListVectorBucketsPaginator,
        ListVectorsPaginator,
    )

    session = get_session()
    with session.create_client("s3vectors") as client:
        client: S3VectorsClient

        list_indexes_paginator: ListIndexesPaginator = client.get_paginator("list_indexes")
        list_vector_buckets_paginator: ListVectorBucketsPaginator = client.get_paginator("list_vector_buckets")
        list_vectors_paginator: ListVectorsPaginator = client.get_paginator("list_vectors")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListIndexesInputPaginateTypeDef,
    ListIndexesOutputTypeDef,
    ListVectorBucketsInputPaginateTypeDef,
    ListVectorBucketsOutputTypeDef,
    ListVectorsInputPaginateTypeDef,
    ListVectorsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListIndexesPaginator", "ListVectorBucketsPaginator", "ListVectorsPaginator")


if TYPE_CHECKING:
    _ListIndexesPaginatorBase = AioPaginator[ListIndexesOutputTypeDef]
else:
    _ListIndexesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIndexesPaginator(_ListIndexesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/paginator/ListIndexes.html#S3Vectors.Paginator.ListIndexes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3vectors/paginators/#listindexespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIndexesInputPaginateTypeDef]
    ) -> AioPageIterator[ListIndexesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/paginator/ListIndexes.html#S3Vectors.Paginator.ListIndexes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3vectors/paginators/#listindexespaginator)
        """


if TYPE_CHECKING:
    _ListVectorBucketsPaginatorBase = AioPaginator[ListVectorBucketsOutputTypeDef]
else:
    _ListVectorBucketsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListVectorBucketsPaginator(_ListVectorBucketsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/paginator/ListVectorBuckets.html#S3Vectors.Paginator.ListVectorBuckets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3vectors/paginators/#listvectorbucketspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVectorBucketsInputPaginateTypeDef]
    ) -> AioPageIterator[ListVectorBucketsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/paginator/ListVectorBuckets.html#S3Vectors.Paginator.ListVectorBuckets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3vectors/paginators/#listvectorbucketspaginator)
        """


if TYPE_CHECKING:
    _ListVectorsPaginatorBase = AioPaginator[ListVectorsOutputTypeDef]
else:
    _ListVectorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListVectorsPaginator(_ListVectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/paginator/ListVectors.html#S3Vectors.Paginator.ListVectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3vectors/paginators/#listvectorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVectorsInputPaginateTypeDef]
    ) -> AioPageIterator[ListVectorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/paginator/ListVectors.html#S3Vectors.Paginator.ListVectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3vectors/paginators/#listvectorspaginator)
        """
