"""
Main interface for meteringmarketplace service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_meteringmarketplace import (
        Client,
        MarketplaceMeteringClient,
    )

    session = get_session()
    async with session.create_client("meteringmarketplace") as client:
        client: MarketplaceMeteringClient
        ...

    ```
"""

from .client import MarketplaceMeteringClient

Client = MarketplaceMeteringClient


__all__ = ("Client", "MarketplaceMeteringClient")
