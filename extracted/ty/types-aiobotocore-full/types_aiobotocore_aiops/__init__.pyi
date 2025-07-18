"""
Main interface for aiops service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_aiops import (
        AIOpsClient,
        Client,
        ListInvestigationGroupsPaginator,
    )

    session = get_session()
    async with session.create_client("aiops") as client:
        client: AIOpsClient
        ...


    list_investigation_groups_paginator: ListInvestigationGroupsPaginator = client.get_paginator("list_investigation_groups")
    ```
"""

from .client import AIOpsClient
from .paginator import ListInvestigationGroupsPaginator

Client = AIOpsClient

__all__ = ("AIOpsClient", "Client", "ListInvestigationGroupsPaginator")
