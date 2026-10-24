"""
Type annotations for lambda-core service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_core/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lambda_core.client import LambdaCoreClient
    from types_aiobotocore_lambda_core.paginator import (
        ListNetworkConnectorVersionsPaginator,
        ListNetworkConnectorsPaginator,
    )

    session = get_session()
    with session.create_client("lambda-core") as client:
        client: LambdaCoreClient

        list_network_connector_versions_paginator: ListNetworkConnectorVersionsPaginator = client.get_paginator("list_network_connector_versions")
        list_network_connectors_paginator: ListNetworkConnectorsPaginator = client.get_paginator("list_network_connectors")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListNetworkConnectorsRequestPaginateTypeDef,
    ListNetworkConnectorsResponseTypeDef,
    ListNetworkConnectorVersionsRequestPaginateTypeDef,
    ListNetworkConnectorVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListNetworkConnectorVersionsPaginator", "ListNetworkConnectorsPaginator")

if TYPE_CHECKING:
    _ListNetworkConnectorVersionsPaginatorBase = AioPaginator[
        ListNetworkConnectorVersionsResponseTypeDef
    ]
else:
    _ListNetworkConnectorVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkConnectorVersionsPaginator(_ListNetworkConnectorVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectorVersions.html#LambdaCore.Paginator.ListNetworkConnectorVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_core/paginators/#listnetworkconnectorversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkConnectorVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkConnectorVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectorVersions.html#LambdaCore.Paginator.ListNetworkConnectorVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_core/paginators/#listnetworkconnectorversionspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkConnectorsPaginatorBase = AioPaginator[ListNetworkConnectorsResponseTypeDef]
else:
    _ListNetworkConnectorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkConnectorsPaginator(_ListNetworkConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectors.html#LambdaCore.Paginator.ListNetworkConnectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_core/paginators/#listnetworkconnectorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkConnectorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectors.html#LambdaCore.Paginator.ListNetworkConnectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_core/paginators/#listnetworkconnectorspaginator)
        """
