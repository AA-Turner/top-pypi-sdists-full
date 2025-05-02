"""
Type annotations for kinesis service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesis.client import KinesisClient
    from types_aiobotocore_kinesis.paginator import (
        DescribeStreamPaginator,
        ListShardsPaginator,
        ListStreamConsumersPaginator,
        ListStreamsPaginator,
    )

    session = get_session()
    with session.create_client("kinesis") as client:
        client: KinesisClient

        describe_stream_paginator: DescribeStreamPaginator = client.get_paginator("describe_stream")
        list_shards_paginator: ListShardsPaginator = client.get_paginator("list_shards")
        list_stream_consumers_paginator: ListStreamConsumersPaginator = client.get_paginator("list_stream_consumers")
        list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeStreamInputPaginateTypeDef,
    DescribeStreamOutputTypeDef,
    ListShardsInputPaginateTypeDef,
    ListShardsOutputTypeDef,
    ListStreamConsumersInputPaginateTypeDef,
    ListStreamConsumersOutputTypeDef,
    ListStreamsInputPaginateTypeDef,
    ListStreamsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeStreamPaginator",
    "ListShardsPaginator",
    "ListStreamConsumersPaginator",
    "ListStreamsPaginator",
)


if TYPE_CHECKING:
    _DescribeStreamPaginatorBase = AioPaginator[DescribeStreamOutputTypeDef]
else:
    _DescribeStreamPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeStreamPaginator(_DescribeStreamPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/DescribeStream.html#Kinesis.Paginator.DescribeStream)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#describestreampaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStreamInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeStreamOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/DescribeStream.html#Kinesis.Paginator.DescribeStream.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#describestreampaginator)
        """


if TYPE_CHECKING:
    _ListShardsPaginatorBase = AioPaginator[ListShardsOutputTypeDef]
else:
    _ListShardsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListShardsPaginator(_ListShardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListShards.html#Kinesis.Paginator.ListShards)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#listshardspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListShardsInputPaginateTypeDef]
    ) -> AioPageIterator[ListShardsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListShards.html#Kinesis.Paginator.ListShards.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#listshardspaginator)
        """


if TYPE_CHECKING:
    _ListStreamConsumersPaginatorBase = AioPaginator[ListStreamConsumersOutputTypeDef]
else:
    _ListStreamConsumersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStreamConsumersPaginator(_ListStreamConsumersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListStreamConsumers.html#Kinesis.Paginator.ListStreamConsumers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#liststreamconsumerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamConsumersInputPaginateTypeDef]
    ) -> AioPageIterator[ListStreamConsumersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListStreamConsumers.html#Kinesis.Paginator.ListStreamConsumers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#liststreamconsumerspaginator)
        """


if TYPE_CHECKING:
    _ListStreamsPaginatorBase = AioPaginator[ListStreamsOutputTypeDef]
else:
    _ListStreamsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStreamsPaginator(_ListStreamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListStreams.html#Kinesis.Paginator.ListStreams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#liststreamspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStreamsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListStreams.html#Kinesis.Paginator.ListStreams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#liststreamspaginator)
        """
