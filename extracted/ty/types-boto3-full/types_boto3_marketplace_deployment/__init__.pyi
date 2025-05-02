"""
Main interface for marketplace-deployment service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_marketplace_deployment import (
        Client,
        MarketplaceDeploymentServiceClient,
    )

    session = Session()
    client: MarketplaceDeploymentServiceClient = session.client("marketplace-deployment")
    ```
"""

from .client import MarketplaceDeploymentServiceClient

Client = MarketplaceDeploymentServiceClient

__all__ = ("Client", "MarketplaceDeploymentServiceClient")
