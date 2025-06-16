"""
Main interface for marketplace-reporting service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_reporting/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_reporting import (
        Client,
        MarketplaceReportingServiceClient,
    )

    session = get_session()
    async with session.create_client("marketplace-reporting") as client:
        client: MarketplaceReportingServiceClient
        ...

    ```
"""

from .client import MarketplaceReportingServiceClient

Client = MarketplaceReportingServiceClient


__all__ = ("Client", "MarketplaceReportingServiceClient")
