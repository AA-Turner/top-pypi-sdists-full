"""
Main interface for rbin service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rbin/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rbin import (
        Client,
        ListRulesPaginator,
        RecycleBinClient,
    )

    session = get_session()
    async with session.create_client("rbin") as client:
        client: RecycleBinClient
        ...


    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```
"""

from .client import RecycleBinClient
from .paginator import ListRulesPaginator

Client = RecycleBinClient

__all__ = ("Client", "ListRulesPaginator", "RecycleBinClient")
