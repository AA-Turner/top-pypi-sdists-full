"""
Type annotations for appmesh service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appmesh.client import AppMeshClient

    session = get_session()
    async with session.create_client("appmesh") as client:
        client: AppMeshClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListGatewayRoutesPaginator,
    ListMeshesPaginator,
    ListRoutesPaginator,
    ListTagsForResourcePaginator,
    ListVirtualGatewaysPaginator,
    ListVirtualNodesPaginator,
    ListVirtualRoutersPaginator,
    ListVirtualServicesPaginator,
)
from .type_defs import (
    CreateGatewayRouteInputTypeDef,
    CreateGatewayRouteOutputTypeDef,
    CreateMeshInputTypeDef,
    CreateMeshOutputTypeDef,
    CreateRouteInputTypeDef,
    CreateRouteOutputTypeDef,
    CreateVirtualGatewayInputTypeDef,
    CreateVirtualGatewayOutputTypeDef,
    CreateVirtualNodeInputTypeDef,
    CreateVirtualNodeOutputTypeDef,
    CreateVirtualRouterInputTypeDef,
    CreateVirtualRouterOutputTypeDef,
    CreateVirtualServiceInputTypeDef,
    CreateVirtualServiceOutputTypeDef,
    DeleteGatewayRouteInputTypeDef,
    DeleteGatewayRouteOutputTypeDef,
    DeleteMeshInputTypeDef,
    DeleteMeshOutputTypeDef,
    DeleteRouteInputTypeDef,
    DeleteRouteOutputTypeDef,
    DeleteVirtualGatewayInputTypeDef,
    DeleteVirtualGatewayOutputTypeDef,
    DeleteVirtualNodeInputTypeDef,
    DeleteVirtualNodeOutputTypeDef,
    DeleteVirtualRouterInputTypeDef,
    DeleteVirtualRouterOutputTypeDef,
    DeleteVirtualServiceInputTypeDef,
    DeleteVirtualServiceOutputTypeDef,
    DescribeGatewayRouteInputTypeDef,
    DescribeGatewayRouteOutputTypeDef,
    DescribeMeshInputTypeDef,
    DescribeMeshOutputTypeDef,
    DescribeRouteInputTypeDef,
    DescribeRouteOutputTypeDef,
    DescribeVirtualGatewayInputTypeDef,
    DescribeVirtualGatewayOutputTypeDef,
    DescribeVirtualNodeInputTypeDef,
    DescribeVirtualNodeOutputTypeDef,
    DescribeVirtualRouterInputTypeDef,
    DescribeVirtualRouterOutputTypeDef,
    DescribeVirtualServiceInputTypeDef,
    DescribeVirtualServiceOutputTypeDef,
    ListGatewayRoutesInputTypeDef,
    ListGatewayRoutesOutputTypeDef,
    ListMeshesInputTypeDef,
    ListMeshesOutputTypeDef,
    ListRoutesInputTypeDef,
    ListRoutesOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualGatewaysInputTypeDef,
    ListVirtualGatewaysOutputTypeDef,
    ListVirtualNodesInputTypeDef,
    ListVirtualNodesOutputTypeDef,
    ListVirtualRoutersInputTypeDef,
    ListVirtualRoutersOutputTypeDef,
    ListVirtualServicesInputTypeDef,
    ListVirtualServicesOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateGatewayRouteInputTypeDef,
    UpdateGatewayRouteOutputTypeDef,
    UpdateMeshInputTypeDef,
    UpdateMeshOutputTypeDef,
    UpdateRouteInputTypeDef,
    UpdateRouteOutputTypeDef,
    UpdateVirtualGatewayInputTypeDef,
    UpdateVirtualGatewayOutputTypeDef,
    UpdateVirtualNodeInputTypeDef,
    UpdateVirtualNodeOutputTypeDef,
    UpdateVirtualRouterInputTypeDef,
    UpdateVirtualRouterOutputTypeDef,
    UpdateVirtualServiceInputTypeDef,
    UpdateVirtualServiceOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("AppMeshClient",)

class Exceptions(BaseClientExceptions):
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class AppMeshClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppMeshClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#generate_presigned_url)
        """

    async def create_gateway_route(
        self, **kwargs: Unpack[CreateGatewayRouteInputTypeDef]
    ) -> CreateGatewayRouteOutputTypeDef:
        """
        Creates a gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_gateway_route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#create_gateway_route)
        """

    async def create_mesh(
        self, **kwargs: Unpack[CreateMeshInputTypeDef]
    ) -> CreateMeshOutputTypeDef:
        """
        Creates a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_mesh.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#create_mesh)
        """

    async def create_route(
        self, **kwargs: Unpack[CreateRouteInputTypeDef]
    ) -> CreateRouteOutputTypeDef:
        """
        Creates a route that is associated with a virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#create_route)
        """

    async def create_virtual_gateway(
        self, **kwargs: Unpack[CreateVirtualGatewayInputTypeDef]
    ) -> CreateVirtualGatewayOutputTypeDef:
        """
        Creates a virtual gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_virtual_gateway.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#create_virtual_gateway)
        """

    async def create_virtual_node(
        self, **kwargs: Unpack[CreateVirtualNodeInputTypeDef]
    ) -> CreateVirtualNodeOutputTypeDef:
        """
        Creates a virtual node within a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_virtual_node.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#create_virtual_node)
        """

    async def create_virtual_router(
        self, **kwargs: Unpack[CreateVirtualRouterInputTypeDef]
    ) -> CreateVirtualRouterOutputTypeDef:
        """
        Creates a virtual router within a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_virtual_router.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#create_virtual_router)
        """

    async def create_virtual_service(
        self, **kwargs: Unpack[CreateVirtualServiceInputTypeDef]
    ) -> CreateVirtualServiceOutputTypeDef:
        """
        Creates a virtual service within a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/create_virtual_service.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#create_virtual_service)
        """

    async def delete_gateway_route(
        self, **kwargs: Unpack[DeleteGatewayRouteInputTypeDef]
    ) -> DeleteGatewayRouteOutputTypeDef:
        """
        Deletes an existing gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_gateway_route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#delete_gateway_route)
        """

    async def delete_mesh(
        self, **kwargs: Unpack[DeleteMeshInputTypeDef]
    ) -> DeleteMeshOutputTypeDef:
        """
        Deletes an existing service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_mesh.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#delete_mesh)
        """

    async def delete_route(
        self, **kwargs: Unpack[DeleteRouteInputTypeDef]
    ) -> DeleteRouteOutputTypeDef:
        """
        Deletes an existing route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#delete_route)
        """

    async def delete_virtual_gateway(
        self, **kwargs: Unpack[DeleteVirtualGatewayInputTypeDef]
    ) -> DeleteVirtualGatewayOutputTypeDef:
        """
        Deletes an existing virtual gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_virtual_gateway.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#delete_virtual_gateway)
        """

    async def delete_virtual_node(
        self, **kwargs: Unpack[DeleteVirtualNodeInputTypeDef]
    ) -> DeleteVirtualNodeOutputTypeDef:
        """
        Deletes an existing virtual node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_virtual_node.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#delete_virtual_node)
        """

    async def delete_virtual_router(
        self, **kwargs: Unpack[DeleteVirtualRouterInputTypeDef]
    ) -> DeleteVirtualRouterOutputTypeDef:
        """
        Deletes an existing virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_virtual_router.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#delete_virtual_router)
        """

    async def delete_virtual_service(
        self, **kwargs: Unpack[DeleteVirtualServiceInputTypeDef]
    ) -> DeleteVirtualServiceOutputTypeDef:
        """
        Deletes an existing virtual service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/delete_virtual_service.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#delete_virtual_service)
        """

    async def describe_gateway_route(
        self, **kwargs: Unpack[DescribeGatewayRouteInputTypeDef]
    ) -> DescribeGatewayRouteOutputTypeDef:
        """
        Describes an existing gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_gateway_route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#describe_gateway_route)
        """

    async def describe_mesh(
        self, **kwargs: Unpack[DescribeMeshInputTypeDef]
    ) -> DescribeMeshOutputTypeDef:
        """
        Describes an existing service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_mesh.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#describe_mesh)
        """

    async def describe_route(
        self, **kwargs: Unpack[DescribeRouteInputTypeDef]
    ) -> DescribeRouteOutputTypeDef:
        """
        Describes an existing route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#describe_route)
        """

    async def describe_virtual_gateway(
        self, **kwargs: Unpack[DescribeVirtualGatewayInputTypeDef]
    ) -> DescribeVirtualGatewayOutputTypeDef:
        """
        Describes an existing virtual gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_virtual_gateway.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#describe_virtual_gateway)
        """

    async def describe_virtual_node(
        self, **kwargs: Unpack[DescribeVirtualNodeInputTypeDef]
    ) -> DescribeVirtualNodeOutputTypeDef:
        """
        Describes an existing virtual node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_virtual_node.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#describe_virtual_node)
        """

    async def describe_virtual_router(
        self, **kwargs: Unpack[DescribeVirtualRouterInputTypeDef]
    ) -> DescribeVirtualRouterOutputTypeDef:
        """
        Describes an existing virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_virtual_router.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#describe_virtual_router)
        """

    async def describe_virtual_service(
        self, **kwargs: Unpack[DescribeVirtualServiceInputTypeDef]
    ) -> DescribeVirtualServiceOutputTypeDef:
        """
        Describes an existing virtual service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/describe_virtual_service.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#describe_virtual_service)
        """

    async def list_gateway_routes(
        self, **kwargs: Unpack[ListGatewayRoutesInputTypeDef]
    ) -> ListGatewayRoutesOutputTypeDef:
        """
        Returns a list of existing gateway routes that are associated to a virtual
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_gateway_routes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#list_gateway_routes)
        """

    async def list_meshes(
        self, **kwargs: Unpack[ListMeshesInputTypeDef]
    ) -> ListMeshesOutputTypeDef:
        """
        Returns a list of existing service meshes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_meshes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#list_meshes)
        """

    async def list_routes(
        self, **kwargs: Unpack[ListRoutesInputTypeDef]
    ) -> ListRoutesOutputTypeDef:
        """
        Returns a list of existing routes in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_routes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#list_routes)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List the tags for an App Mesh resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#list_tags_for_resource)
        """

    async def list_virtual_gateways(
        self, **kwargs: Unpack[ListVirtualGatewaysInputTypeDef]
    ) -> ListVirtualGatewaysOutputTypeDef:
        """
        Returns a list of existing virtual gateways in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_virtual_gateways.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#list_virtual_gateways)
        """

    async def list_virtual_nodes(
        self, **kwargs: Unpack[ListVirtualNodesInputTypeDef]
    ) -> ListVirtualNodesOutputTypeDef:
        """
        Returns a list of existing virtual nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_virtual_nodes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#list_virtual_nodes)
        """

    async def list_virtual_routers(
        self, **kwargs: Unpack[ListVirtualRoutersInputTypeDef]
    ) -> ListVirtualRoutersOutputTypeDef:
        """
        Returns a list of existing virtual routers in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_virtual_routers.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#list_virtual_routers)
        """

    async def list_virtual_services(
        self, **kwargs: Unpack[ListVirtualServicesInputTypeDef]
    ) -> ListVirtualServicesOutputTypeDef:
        """
        Returns a list of existing virtual services in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/list_virtual_services.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#list_virtual_services)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#untag_resource)
        """

    async def update_gateway_route(
        self, **kwargs: Unpack[UpdateGatewayRouteInputTypeDef]
    ) -> UpdateGatewayRouteOutputTypeDef:
        """
        Updates an existing gateway route that is associated to a specified virtual
        gateway in a service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_gateway_route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#update_gateway_route)
        """

    async def update_mesh(
        self, **kwargs: Unpack[UpdateMeshInputTypeDef]
    ) -> UpdateMeshOutputTypeDef:
        """
        Updates an existing service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_mesh.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#update_mesh)
        """

    async def update_route(
        self, **kwargs: Unpack[UpdateRouteInputTypeDef]
    ) -> UpdateRouteOutputTypeDef:
        """
        Updates an existing route for a specified service mesh and virtual router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_route.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#update_route)
        """

    async def update_virtual_gateway(
        self, **kwargs: Unpack[UpdateVirtualGatewayInputTypeDef]
    ) -> UpdateVirtualGatewayOutputTypeDef:
        """
        Updates an existing virtual gateway in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_virtual_gateway.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#update_virtual_gateway)
        """

    async def update_virtual_node(
        self, **kwargs: Unpack[UpdateVirtualNodeInputTypeDef]
    ) -> UpdateVirtualNodeOutputTypeDef:
        """
        Updates an existing virtual node in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_virtual_node.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#update_virtual_node)
        """

    async def update_virtual_router(
        self, **kwargs: Unpack[UpdateVirtualRouterInputTypeDef]
    ) -> UpdateVirtualRouterOutputTypeDef:
        """
        Updates an existing virtual router in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_virtual_router.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#update_virtual_router)
        """

    async def update_virtual_service(
        self, **kwargs: Unpack[UpdateVirtualServiceInputTypeDef]
    ) -> UpdateVirtualServiceOutputTypeDef:
        """
        Updates an existing virtual service in a specified service mesh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/update_virtual_service.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#update_virtual_service)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_gateway_routes"]
    ) -> ListGatewayRoutesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_meshes"]
    ) -> ListMeshesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_routes"]
    ) -> ListRoutesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_virtual_gateways"]
    ) -> ListVirtualGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_virtual_nodes"]
    ) -> ListVirtualNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_virtual_routers"]
    ) -> ListVirtualRoutersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_virtual_services"]
    ) -> ListVirtualServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appmesh/client/)
        """
