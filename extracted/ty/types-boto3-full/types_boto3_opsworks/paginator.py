"""
Type annotations for opsworks service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_opsworks.client import OpsWorksClient
    from types_boto3_opsworks.paginator import (
        DescribeEcsClustersPaginator,
    )

    session = Session()
    client: OpsWorksClient = session.client("opsworks")

    describe_ecs_clusters_paginator: DescribeEcsClustersPaginator = client.get_paginator("describe_ecs_clusters")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import DescribeEcsClustersRequestPaginateTypeDef, DescribeEcsClustersResultTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeEcsClustersPaginator",)


if TYPE_CHECKING:
    _DescribeEcsClustersPaginatorBase = Paginator[DescribeEcsClustersResultTypeDef]
else:
    _DescribeEcsClustersPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeEcsClustersPaginator(_DescribeEcsClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/paginator/DescribeEcsClusters.html#OpsWorks.Paginator.DescribeEcsClusters)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/paginators/#describeecsclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEcsClustersRequestPaginateTypeDef]
    ) -> PageIterator[DescribeEcsClustersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/paginator/DescribeEcsClusters.html#OpsWorks.Paginator.DescribeEcsClusters.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/paginators/#describeecsclusterspaginator)
        """
