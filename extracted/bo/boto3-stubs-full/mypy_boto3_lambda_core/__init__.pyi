"""
Main interface for lambda-core service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lambda_core import (
        Client,
        LambdaCoreClient,
        ListNetworkConnectorsPaginator,
    )

    session = Session()
    client: LambdaCoreClient = session.client("lambda-core")

    list_network_connectors_paginator: ListNetworkConnectorsPaginator = client.get_paginator("list_network_connectors")
    ```
"""

from .client import LambdaCoreClient
from .paginator import ListNetworkConnectorsPaginator

Client = LambdaCoreClient

__all__ = ("Client", "LambdaCoreClient", "ListNetworkConnectorsPaginator")
