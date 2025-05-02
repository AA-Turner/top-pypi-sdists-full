"""
Main interface for account service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_account/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_account import (
        AccountClient,
        Client,
        ListRegionsPaginator,
    )

    session = Session()
    client: AccountClient = session.client("account")

    list_regions_paginator: ListRegionsPaginator = client.get_paginator("list_regions")
    ```
"""

from .client import AccountClient
from .paginator import ListRegionsPaginator

Client = AccountClient


__all__ = ("AccountClient", "Client", "ListRegionsPaginator")
