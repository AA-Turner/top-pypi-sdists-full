"""
Main interface for ce service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ce import (
        Client,
        CostExplorerClient,
    )

    session = get_session()
    async with session.create_client("ce") as client:
        client: CostExplorerClient
        ...

    ```
"""

from .client import CostExplorerClient

Client = CostExplorerClient


__all__ = ("Client", "CostExplorerClient")
