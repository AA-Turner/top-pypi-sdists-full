"""
Main interface for dynamodbstreams service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodbstreams/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_dynamodbstreams import (
        Client,
        DynamoDBStreamsClient,
    )

    session = get_session()
    async with session.create_client("dynamodbstreams") as client:
        client: DynamoDBStreamsClient
        ...

    ```
"""

from .client import DynamoDBStreamsClient

Client = DynamoDBStreamsClient


__all__ = ("Client", "DynamoDBStreamsClient")
