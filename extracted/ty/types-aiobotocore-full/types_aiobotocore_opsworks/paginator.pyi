"""
Type annotations for opsworks service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_opsworks.client import OpsWorksClient
    from types_aiobotocore_opsworks.paginator import (
        DescribeEcsClustersPaginator,
    )

    session = get_session()
    with session.create_client("opsworks") as client:
        client: OpsWorksClient

        describe_ecs_clusters_paginator: DescribeEcsClustersPaginator = client.get_paginator("describe_ecs_clusters")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import DescribeEcsClustersRequestPaginateTypeDef, DescribeEcsClustersResultTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeEcsClustersPaginator",)

if TYPE_CHECKING:
    _DescribeEcsClustersPaginatorBase = AioPaginator[DescribeEcsClustersResultTypeDef]
else:
    _DescribeEcsClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEcsClustersPaginator(_DescribeEcsClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/paginator/DescribeEcsClusters.html#OpsWorks.Paginator.DescribeEcsClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/paginators/#describeecsclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEcsClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEcsClustersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/paginator/DescribeEcsClusters.html#OpsWorks.Paginator.DescribeEcsClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/paginators/#describeecsclusterspaginator)
        """
