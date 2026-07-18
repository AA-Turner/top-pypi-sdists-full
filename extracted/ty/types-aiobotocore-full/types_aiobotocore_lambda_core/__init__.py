"""
Main interface for lambda-core service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_core/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lambda_core import (
        Client,
        LambdaCoreClient,
        ListNetworkConnectorsPaginator,
    )

    session = get_session()
    async with session.create_client("lambda-core") as client:
        client: LambdaCoreClient
        ...


    list_network_connectors_paginator: ListNetworkConnectorsPaginator = client.get_paginator("list_network_connectors")
    ```
"""

from .client import LambdaCoreClient
from .paginator import ListNetworkConnectorsPaginator

Client = LambdaCoreClient


__all__ = ("Client", "LambdaCoreClient", "ListNetworkConnectorsPaginator")
