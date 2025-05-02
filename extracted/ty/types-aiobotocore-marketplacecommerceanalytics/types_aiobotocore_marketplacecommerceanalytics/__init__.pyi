"""
Main interface for marketplacecommerceanalytics service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplacecommerceanalytics/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplacecommerceanalytics import (
        Client,
        MarketplaceCommerceAnalyticsClient,
    )

    session = get_session()
    async with session.create_client("marketplacecommerceanalytics") as client:
        client: MarketplaceCommerceAnalyticsClient
        ...

    ```
"""

from .client import MarketplaceCommerceAnalyticsClient

Client = MarketplaceCommerceAnalyticsClient

__all__ = ("Client", "MarketplaceCommerceAnalyticsClient")
