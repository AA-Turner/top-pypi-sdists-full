"""
Main interface for marketplace-deployment service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_deployment/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_marketplace_deployment import (
        Client,
        ListDeploymentConfigurationJobsPaginator,
        MarketplaceDeploymentServiceClient,
    )

    session = Session()
    client: MarketplaceDeploymentServiceClient = session.client("marketplace-deployment")

    list_deployment_configuration_jobs_paginator: ListDeploymentConfigurationJobsPaginator = client.get_paginator("list_deployment_configuration_jobs")
    ```
"""

from .client import MarketplaceDeploymentServiceClient
from .paginator import ListDeploymentConfigurationJobsPaginator

Client = MarketplaceDeploymentServiceClient


__all__ = (
    "Client",
    "ListDeploymentConfigurationJobsPaginator",
    "MarketplaceDeploymentServiceClient",
)
