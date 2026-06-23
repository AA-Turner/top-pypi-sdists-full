"""
Type annotations for lambda-core service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_lambda_core.client import LambdaCoreClient
    from mypy_boto3_lambda_core.paginator import (
        ListNetworkConnectorsPaginator,
    )

    session = Session()
    client: LambdaCoreClient = session.client("lambda-core")

    list_network_connectors_paginator: ListNetworkConnectorsPaginator = client.get_paginator("list_network_connectors")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListNetworkConnectorsRequestPaginateTypeDef,
    ListNetworkConnectorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListNetworkConnectorsPaginator",)


if TYPE_CHECKING:
    _ListNetworkConnectorsPaginatorBase = Paginator[ListNetworkConnectorsResponseTypeDef]
else:
    _ListNetworkConnectorsPaginatorBase = Paginator  # type: ignore[assignment]


class ListNetworkConnectorsPaginator(_ListNetworkConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectors.html#LambdaCore.Paginator.ListNetworkConnectors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listnetworkconnectorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkConnectorsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectors.html#LambdaCore.Paginator.ListNetworkConnectors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listnetworkconnectorspaginator)
        """
