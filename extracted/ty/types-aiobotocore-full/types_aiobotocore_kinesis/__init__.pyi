"""
Main interface for kinesis service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis import (
        ChannelActiveWaiter,
        Client,
        DescribeStreamPaginator,
        KinesisClient,
        ListChannelsPaginator,
        ListShardsPaginator,
        ListStreamConsumersPaginator,
        ListStreamsPaginator,
        StreamExistsWaiter,
        StreamNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("kinesis") as client:
        client: KinesisClient
        ...


    channel_active_waiter: ChannelActiveWaiter = client.get_waiter("channel_active")
    stream_exists_waiter: StreamExistsWaiter = client.get_waiter("stream_exists")
    stream_not_exists_waiter: StreamNotExistsWaiter = client.get_waiter("stream_not_exists")

    describe_stream_paginator: DescribeStreamPaginator = client.get_paginator("describe_stream")
    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_shards_paginator: ListShardsPaginator = client.get_paginator("list_shards")
    list_stream_consumers_paginator: ListStreamConsumersPaginator = client.get_paginator("list_stream_consumers")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""

from .client import KinesisClient
from .paginator import (
    DescribeStreamPaginator,
    ListChannelsPaginator,
    ListShardsPaginator,
    ListStreamConsumersPaginator,
    ListStreamsPaginator,
)
from .waiter import ChannelActiveWaiter, StreamExistsWaiter, StreamNotExistsWaiter

Client = KinesisClient

__all__ = (
    "ChannelActiveWaiter",
    "Client",
    "DescribeStreamPaginator",
    "KinesisClient",
    "ListChannelsPaginator",
    "ListShardsPaginator",
    "ListStreamConsumersPaginator",
    "ListStreamsPaginator",
    "StreamExistsWaiter",
    "StreamNotExistsWaiter",
)
