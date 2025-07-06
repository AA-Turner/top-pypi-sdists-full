"""
Main interface for mq service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mq import (
        Client,
        ListBrokersPaginator,
        MQClient,
    )

    session = get_session()
    async with session.create_client("mq") as client:
        client: MQClient
        ...


    list_brokers_paginator: ListBrokersPaginator = client.get_paginator("list_brokers")
    ```
"""

from .client import MQClient
from .paginator import ListBrokersPaginator

Client = MQClient

__all__ = ("Client", "ListBrokersPaginator", "MQClient")
