"""
Main interface for apigatewaymanagementapi service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apigatewaymanagementapi import (
        ApiGatewayManagementApiClient,
        Client,
    )

    session = get_session()
    async with session.create_client("apigatewaymanagementapi") as client:
        client: ApiGatewayManagementApiClient
        ...

    ```
"""

from .client import ApiGatewayManagementApiClient

Client = ApiGatewayManagementApiClient


__all__ = ("ApiGatewayManagementApiClient", "Client")
