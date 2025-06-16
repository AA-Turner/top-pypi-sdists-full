"""
Main interface for sqs service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sqs import (
        Client,
        ListDeadLetterSourceQueuesPaginator,
        ListQueuesPaginator,
        SQSClient,
        SQSServiceResource,
        ServiceResource,
    )

    session = get_session()
    async with session.create_client("sqs") as client:
        client: SQSClient
        ...


    list_dead_letter_source_queues_paginator: ListDeadLetterSourceQueuesPaginator = client.get_paginator("list_dead_letter_source_queues")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```
"""

from .client import SQSClient
from .paginator import ListDeadLetterSourceQueuesPaginator, ListQueuesPaginator

try:
    from .service_resource import SQSServiceResource
except ImportError:
    from builtins import object as SQSServiceResource  # type: ignore[assignment]


Client = SQSClient


ServiceResource = SQSServiceResource


__all__ = (
    "Client",
    "ListDeadLetterSourceQueuesPaginator",
    "ListQueuesPaginator",
    "SQSClient",
    "SQSServiceResource",
    "ServiceResource",
)
