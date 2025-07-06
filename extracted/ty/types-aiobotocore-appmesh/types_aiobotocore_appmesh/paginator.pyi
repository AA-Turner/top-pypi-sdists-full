"""
Type annotations for appmesh service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appmesh.client import AppMeshClient
    from types_aiobotocore_appmesh.paginator import (
        ListGatewayRoutesPaginator,
        ListMeshesPaginator,
        ListRoutesPaginator,
        ListTagsForResourcePaginator,
        ListVirtualGatewaysPaginator,
        ListVirtualNodesPaginator,
        ListVirtualRoutersPaginator,
        ListVirtualServicesPaginator,
    )

    session = get_session()
    with session.create_client("appmesh") as client:
        client: AppMeshClient

        list_gateway_routes_paginator: ListGatewayRoutesPaginator = client.get_paginator("list_gateway_routes")
        list_meshes_paginator: ListMeshesPaginator = client.get_paginator("list_meshes")
        list_routes_paginator: ListRoutesPaginator = client.get_paginator("list_routes")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_virtual_gateways_paginator: ListVirtualGatewaysPaginator = client.get_paginator("list_virtual_gateways")
        list_virtual_nodes_paginator: ListVirtualNodesPaginator = client.get_paginator("list_virtual_nodes")
        list_virtual_routers_paginator: ListVirtualRoutersPaginator = client.get_paginator("list_virtual_routers")
        list_virtual_services_paginator: ListVirtualServicesPaginator = client.get_paginator("list_virtual_services")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListGatewayRoutesInputPaginateTypeDef,
    ListGatewayRoutesOutputTypeDef,
    ListMeshesInputPaginateTypeDef,
    ListMeshesOutputTypeDef,
    ListRoutesInputPaginateTypeDef,
    ListRoutesOutputTypeDef,
    ListTagsForResourceInputPaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualGatewaysInputPaginateTypeDef,
    ListVirtualGatewaysOutputTypeDef,
    ListVirtualNodesInputPaginateTypeDef,
    ListVirtualNodesOutputTypeDef,
    ListVirtualRoutersInputPaginateTypeDef,
    ListVirtualRoutersOutputTypeDef,
    ListVirtualServicesInputPaginateTypeDef,
    ListVirtualServicesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListGatewayRoutesPaginator",
    "ListMeshesPaginator",
    "ListRoutesPaginator",
    "ListTagsForResourcePaginator",
    "ListVirtualGatewaysPaginator",
    "ListVirtualNodesPaginator",
    "ListVirtualRoutersPaginator",
    "ListVirtualServicesPaginator",
)

if TYPE_CHECKING:
    _ListGatewayRoutesPaginatorBase = AioPaginator[ListGatewayRoutesOutputTypeDef]
else:
    _ListGatewayRoutesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGatewayRoutesPaginator(_ListGatewayRoutesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListGatewayRoutes.html#AppMesh.Paginator.ListGatewayRoutes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listgatewayroutespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGatewayRoutesInputPaginateTypeDef]
    ) -> AioPageIterator[ListGatewayRoutesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListGatewayRoutes.html#AppMesh.Paginator.ListGatewayRoutes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listgatewayroutespaginator)
        """

if TYPE_CHECKING:
    _ListMeshesPaginatorBase = AioPaginator[ListMeshesOutputTypeDef]
else:
    _ListMeshesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMeshesPaginator(_ListMeshesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListMeshes.html#AppMesh.Paginator.ListMeshes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listmeshespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMeshesInputPaginateTypeDef]
    ) -> AioPageIterator[ListMeshesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListMeshes.html#AppMesh.Paginator.ListMeshes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listmeshespaginator)
        """

if TYPE_CHECKING:
    _ListRoutesPaginatorBase = AioPaginator[ListRoutesOutputTypeDef]
else:
    _ListRoutesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRoutesPaginator(_ListRoutesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListRoutes.html#AppMesh.Paginator.ListRoutes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listroutespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoutesInputPaginateTypeDef]
    ) -> AioPageIterator[ListRoutesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListRoutes.html#AppMesh.Paginator.ListRoutes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listroutespaginator)
        """

if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceOutputTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListTagsForResource.html#AppMesh.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listtagsforresourcepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceInputPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListTagsForResource.html#AppMesh.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listtagsforresourcepaginator)
        """

if TYPE_CHECKING:
    _ListVirtualGatewaysPaginatorBase = AioPaginator[ListVirtualGatewaysOutputTypeDef]
else:
    _ListVirtualGatewaysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVirtualGatewaysPaginator(_ListVirtualGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualGateways.html#AppMesh.Paginator.ListVirtualGateways)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listvirtualgatewayspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVirtualGatewaysInputPaginateTypeDef]
    ) -> AioPageIterator[ListVirtualGatewaysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualGateways.html#AppMesh.Paginator.ListVirtualGateways.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listvirtualgatewayspaginator)
        """

if TYPE_CHECKING:
    _ListVirtualNodesPaginatorBase = AioPaginator[ListVirtualNodesOutputTypeDef]
else:
    _ListVirtualNodesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVirtualNodesPaginator(_ListVirtualNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualNodes.html#AppMesh.Paginator.ListVirtualNodes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listvirtualnodespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVirtualNodesInputPaginateTypeDef]
    ) -> AioPageIterator[ListVirtualNodesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualNodes.html#AppMesh.Paginator.ListVirtualNodes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listvirtualnodespaginator)
        """

if TYPE_CHECKING:
    _ListVirtualRoutersPaginatorBase = AioPaginator[ListVirtualRoutersOutputTypeDef]
else:
    _ListVirtualRoutersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVirtualRoutersPaginator(_ListVirtualRoutersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualRouters.html#AppMesh.Paginator.ListVirtualRouters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listvirtualrouterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVirtualRoutersInputPaginateTypeDef]
    ) -> AioPageIterator[ListVirtualRoutersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualRouters.html#AppMesh.Paginator.ListVirtualRouters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listvirtualrouterspaginator)
        """

if TYPE_CHECKING:
    _ListVirtualServicesPaginatorBase = AioPaginator[ListVirtualServicesOutputTypeDef]
else:
    _ListVirtualServicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVirtualServicesPaginator(_ListVirtualServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualServices.html#AppMesh.Paginator.ListVirtualServices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listvirtualservicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVirtualServicesInputPaginateTypeDef]
    ) -> AioPageIterator[ListVirtualServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/paginator/ListVirtualServices.html#AppMesh.Paginator.ListVirtualServices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/paginators/#listvirtualservicespaginator)
        """
