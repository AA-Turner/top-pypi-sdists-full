"""
Main interface for freetier service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_freetier/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_freetier import (
        Client,
        FreeTierClient,
        GetFreeTierUsagePaginator,
    )

    session = get_session()
    async with session.create_client("freetier") as client:
        client: FreeTierClient
        ...


    get_free_tier_usage_paginator: GetFreeTierUsagePaginator = client.get_paginator("get_free_tier_usage")
    ```
"""

from .client import FreeTierClient
from .paginator import GetFreeTierUsagePaginator

Client = FreeTierClient

__all__ = ("Client", "FreeTierClient", "GetFreeTierUsagePaginator")
