"""
Type annotations for osis service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_osis.client import OpenSearchIngestionClient
    from types_aiobotocore_osis.paginator import (
        ListPipelineEndpointConnectionsPaginator,
        ListPipelineEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("osis") as client:
        client: OpenSearchIngestionClient

        list_pipeline_endpoint_connections_paginator: ListPipelineEndpointConnectionsPaginator = client.get_paginator("list_pipeline_endpoint_connections")
        list_pipeline_endpoints_paginator: ListPipelineEndpointsPaginator = client.get_paginator("list_pipeline_endpoints")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListPipelineEndpointConnectionsRequestPaginateTypeDef,
    ListPipelineEndpointConnectionsResponseTypeDef,
    ListPipelineEndpointsRequestPaginateTypeDef,
    ListPipelineEndpointsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListPipelineEndpointConnectionsPaginator", "ListPipelineEndpointsPaginator")


if TYPE_CHECKING:
    _ListPipelineEndpointConnectionsPaginatorBase = AioPaginator[
        ListPipelineEndpointConnectionsResponseTypeDef
    ]
else:
    _ListPipelineEndpointConnectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPipelineEndpointConnectionsPaginator(_ListPipelineEndpointConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/paginator/ListPipelineEndpointConnections.html#OpenSearchIngestion.Paginator.ListPipelineEndpointConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/paginators/#listpipelineendpointconnectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineEndpointConnectionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipelineEndpointConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/paginator/ListPipelineEndpointConnections.html#OpenSearchIngestion.Paginator.ListPipelineEndpointConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/paginators/#listpipelineendpointconnectionspaginator)
        """


if TYPE_CHECKING:
    _ListPipelineEndpointsPaginatorBase = AioPaginator[ListPipelineEndpointsResponseTypeDef]
else:
    _ListPipelineEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPipelineEndpointsPaginator(_ListPipelineEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/paginator/ListPipelineEndpoints.html#OpenSearchIngestion.Paginator.ListPipelineEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/paginators/#listpipelineendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipelineEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/paginator/ListPipelineEndpoints.html#OpenSearchIngestion.Paginator.ListPipelineEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/paginators/#listpipelineendpointspaginator)
        """
