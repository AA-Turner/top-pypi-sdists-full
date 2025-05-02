"""
Main interface for marketplace-deployment service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_deployment/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_deployment import (
        Client,
        MarketplaceDeploymentServiceClient,
    )

    session = get_session()
    async with session.create_client("marketplace-deployment") as client:
        client: MarketplaceDeploymentServiceClient
        ...

    ```
"""

from .client import MarketplaceDeploymentServiceClient

Client = MarketplaceDeploymentServiceClient

__all__ = ("Client", "MarketplaceDeploymentServiceClient")
