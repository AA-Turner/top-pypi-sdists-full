"""
Main interface for kendra-ranking service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra_ranking/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kendra_ranking import (
        Client,
        KendraRankingClient,
    )

    session = get_session()
    async with session.create_client("kendra-ranking") as client:
        client: KendraRankingClient
        ...

    ```
"""

from .client import KendraRankingClient

Client = KendraRankingClient


__all__ = ("Client", "KendraRankingClient")
