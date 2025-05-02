"""
Main interface for sdb service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sdb import (
        Client,
        ListDomainsPaginator,
        SelectPaginator,
        SimpleDBClient,
    )

    session = get_session()
    async with session.create_client("sdb") as client:
        client: SimpleDBClient
        ...


    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    select_paginator: SelectPaginator = client.get_paginator("select")
    ```
"""

from .client import SimpleDBClient
from .paginator import ListDomainsPaginator, SelectPaginator

Client = SimpleDBClient


__all__ = ("Client", "ListDomainsPaginator", "SelectPaginator", "SimpleDBClient")
