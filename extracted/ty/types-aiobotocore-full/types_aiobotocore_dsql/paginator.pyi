"""
Type annotations for dsql service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dsql.client import AuroraDSQLClient
    from types_aiobotocore_dsql.paginator import (
        ListClustersPaginator,
    )

    session = get_session()
    with session.create_client("dsql") as client:
        client: AuroraDSQLClient

        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListClustersInputPaginateTypeDef, ListClustersOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListClustersPaginator",)

if TYPE_CHECKING:
    _ListClustersPaginatorBase = AioPaginator[ListClustersOutputTypeDef]
else:
    _ListClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/paginator/ListClusters.html#AuroraDSQL.Paginator.ListClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/paginators/#listclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersInputPaginateTypeDef]
    ) -> AioPageIterator[ListClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/paginator/ListClusters.html#AuroraDSQL.Paginator.ListClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/paginators/#listclusterspaginator)
        """
