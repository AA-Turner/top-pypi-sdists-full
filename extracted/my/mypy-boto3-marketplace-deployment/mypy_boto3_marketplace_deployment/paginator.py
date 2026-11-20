"""
Type annotations for marketplace-deployment service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_deployment/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_marketplace_deployment.client import MarketplaceDeploymentServiceClient
    from mypy_boto3_marketplace_deployment.paginator import (
        ListDeploymentConfigurationJobsPaginator,
    )

    session = Session()
    client: MarketplaceDeploymentServiceClient = session.client("marketplace-deployment")

    list_deployment_configuration_jobs_paginator: ListDeploymentConfigurationJobsPaginator = client.get_paginator("list_deployment_configuration_jobs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDeploymentConfigurationJobsRequestPaginateTypeDef,
    ListDeploymentConfigurationJobsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListDeploymentConfigurationJobsPaginator",)


if TYPE_CHECKING:
    _ListDeploymentConfigurationJobsPaginatorBase = Paginator[
        ListDeploymentConfigurationJobsResponseTypeDef
    ]
else:
    _ListDeploymentConfigurationJobsPaginatorBase = Paginator  # type: ignore[assignment]


class ListDeploymentConfigurationJobsPaginator(_ListDeploymentConfigurationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/paginator/ListDeploymentConfigurationJobs.html#MarketplaceDeploymentService.Paginator.ListDeploymentConfigurationJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_deployment/paginators/#listdeploymentconfigurationjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentConfigurationJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListDeploymentConfigurationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-deployment/paginator/ListDeploymentConfigurationJobs.html#MarketplaceDeploymentService.Paginator.ListDeploymentConfigurationJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_deployment/paginators/#listdeploymentconfigurationjobspaginator)
        """
