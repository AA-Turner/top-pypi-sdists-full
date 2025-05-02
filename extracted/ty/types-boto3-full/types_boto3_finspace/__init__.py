"""
Main interface for finspace service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_finspace/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_finspace import (
        Client,
        FinspaceClient,
        ListKxEnvironmentsPaginator,
    )

    session = Session()
    client: FinspaceClient = session.client("finspace")

    list_kx_environments_paginator: ListKxEnvironmentsPaginator = client.get_paginator("list_kx_environments")
    ```
"""

from .client import FinspaceClient
from .paginator import ListKxEnvironmentsPaginator

Client = FinspaceClient


__all__ = ("Client", "FinspaceClient", "ListKxEnvironmentsPaginator")
