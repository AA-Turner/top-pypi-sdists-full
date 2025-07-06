"""
Type annotations for privatenetworks service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_privatenetworks.client import Private5GClient

    session = get_session()
    async with session.create_client("privatenetworks") as client:
        client: Private5GClient
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
    ListDeviceIdentifiersPaginator,
    ListNetworkResourcesPaginator,
    ListNetworkSitesPaginator,
    ListNetworksPaginator,
    ListOrdersPaginator,
)
from .type_defs import (
    AcknowledgeOrderReceiptRequestTypeDef,
    AcknowledgeOrderReceiptResponseTypeDef,
    ActivateDeviceIdentifierRequestTypeDef,
    ActivateDeviceIdentifierResponseTypeDef,
    ActivateNetworkSiteRequestTypeDef,
    ActivateNetworkSiteResponseTypeDef,
    ConfigureAccessPointRequestTypeDef,
    ConfigureAccessPointResponseTypeDef,
    CreateNetworkRequestTypeDef,
    CreateNetworkResponseTypeDef,
    CreateNetworkSiteRequestTypeDef,
    CreateNetworkSiteResponseTypeDef,
    DeactivateDeviceIdentifierRequestTypeDef,
    DeactivateDeviceIdentifierResponseTypeDef,
    DeleteNetworkRequestTypeDef,
    DeleteNetworkResponseTypeDef,
    DeleteNetworkSiteRequestTypeDef,
    DeleteNetworkSiteResponseTypeDef,
    GetDeviceIdentifierRequestTypeDef,
    GetDeviceIdentifierResponseTypeDef,
    GetNetworkRequestTypeDef,
    GetNetworkResourceRequestTypeDef,
    GetNetworkResourceResponseTypeDef,
    GetNetworkResponseTypeDef,
    GetNetworkSiteRequestTypeDef,
    GetNetworkSiteResponseTypeDef,
    GetOrderRequestTypeDef,
    GetOrderResponseTypeDef,
    ListDeviceIdentifiersRequestTypeDef,
    ListDeviceIdentifiersResponseTypeDef,
    ListNetworkResourcesRequestTypeDef,
    ListNetworkResourcesResponseTypeDef,
    ListNetworkSitesRequestTypeDef,
    ListNetworkSitesResponseTypeDef,
    ListNetworksRequestTypeDef,
    ListNetworksResponseTypeDef,
    ListOrdersRequestTypeDef,
    ListOrdersResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PingResponseTypeDef,
    StartNetworkResourceUpdateRequestTypeDef,
    StartNetworkResourceUpdateResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateNetworkSitePlanRequestTypeDef,
    UpdateNetworkSiteRequestTypeDef,
    UpdateNetworkSiteResponseTypeDef,
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


__all__ = ("Private5GClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Private5GClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Private5GClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#generate_presigned_url)
        """

    async def acknowledge_order_receipt(
        self, **kwargs: Unpack[AcknowledgeOrderReceiptRequestTypeDef]
    ) -> AcknowledgeOrderReceiptResponseTypeDef:
        """
        Acknowledges that the specified network order was received.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/acknowledge_order_receipt.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#acknowledge_order_receipt)
        """

    async def activate_device_identifier(
        self, **kwargs: Unpack[ActivateDeviceIdentifierRequestTypeDef]
    ) -> ActivateDeviceIdentifierResponseTypeDef:
        """
        Activates the specified device identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/activate_device_identifier.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#activate_device_identifier)
        """

    async def activate_network_site(
        self, **kwargs: Unpack[ActivateNetworkSiteRequestTypeDef]
    ) -> ActivateNetworkSiteResponseTypeDef:
        """
        Activates the specified network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/activate_network_site.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#activate_network_site)
        """

    async def configure_access_point(
        self, **kwargs: Unpack[ConfigureAccessPointRequestTypeDef]
    ) -> ConfigureAccessPointResponseTypeDef:
        """
        Configures the specified network resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/configure_access_point.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#configure_access_point)
        """

    async def create_network(
        self, **kwargs: Unpack[CreateNetworkRequestTypeDef]
    ) -> CreateNetworkResponseTypeDef:
        """
        Creates a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/create_network.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#create_network)
        """

    async def create_network_site(
        self, **kwargs: Unpack[CreateNetworkSiteRequestTypeDef]
    ) -> CreateNetworkSiteResponseTypeDef:
        """
        Creates a network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/create_network_site.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#create_network_site)
        """

    async def deactivate_device_identifier(
        self, **kwargs: Unpack[DeactivateDeviceIdentifierRequestTypeDef]
    ) -> DeactivateDeviceIdentifierResponseTypeDef:
        """
        Deactivates the specified device identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/deactivate_device_identifier.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#deactivate_device_identifier)
        """

    async def delete_network(
        self, **kwargs: Unpack[DeleteNetworkRequestTypeDef]
    ) -> DeleteNetworkResponseTypeDef:
        """
        Deletes the specified network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/delete_network.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#delete_network)
        """

    async def delete_network_site(
        self, **kwargs: Unpack[DeleteNetworkSiteRequestTypeDef]
    ) -> DeleteNetworkSiteResponseTypeDef:
        """
        Deletes the specified network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/delete_network_site.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#delete_network_site)
        """

    async def get_device_identifier(
        self, **kwargs: Unpack[GetDeviceIdentifierRequestTypeDef]
    ) -> GetDeviceIdentifierResponseTypeDef:
        """
        Gets the specified device identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_device_identifier.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_device_identifier)
        """

    async def get_network(
        self, **kwargs: Unpack[GetNetworkRequestTypeDef]
    ) -> GetNetworkResponseTypeDef:
        """
        Gets the specified network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_network.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_network)
        """

    async def get_network_resource(
        self, **kwargs: Unpack[GetNetworkResourceRequestTypeDef]
    ) -> GetNetworkResourceResponseTypeDef:
        """
        Gets the specified network resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_network_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_network_resource)
        """

    async def get_network_site(
        self, **kwargs: Unpack[GetNetworkSiteRequestTypeDef]
    ) -> GetNetworkSiteResponseTypeDef:
        """
        Gets the specified network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_network_site.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_network_site)
        """

    async def get_order(self, **kwargs: Unpack[GetOrderRequestTypeDef]) -> GetOrderResponseTypeDef:
        """
        Gets the specified order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_order.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_order)
        """

    async def list_device_identifiers(
        self, **kwargs: Unpack[ListDeviceIdentifiersRequestTypeDef]
    ) -> ListDeviceIdentifiersResponseTypeDef:
        """
        Lists device identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_device_identifiers.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#list_device_identifiers)
        """

    async def list_network_resources(
        self, **kwargs: Unpack[ListNetworkResourcesRequestTypeDef]
    ) -> ListNetworkResourcesResponseTypeDef:
        """
        Lists network resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_network_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#list_network_resources)
        """

    async def list_network_sites(
        self, **kwargs: Unpack[ListNetworkSitesRequestTypeDef]
    ) -> ListNetworkSitesResponseTypeDef:
        """
        Lists network sites.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_network_sites.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#list_network_sites)
        """

    async def list_networks(
        self, **kwargs: Unpack[ListNetworksRequestTypeDef]
    ) -> ListNetworksResponseTypeDef:
        """
        Lists networks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_networks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#list_networks)
        """

    async def list_orders(
        self, **kwargs: Unpack[ListOrdersRequestTypeDef]
    ) -> ListOrdersResponseTypeDef:
        """
        Lists orders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_orders.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#list_orders)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#list_tags_for_resource)
        """

    async def ping(self) -> PingResponseTypeDef:
        """
        Checks the health of the service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/ping.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#ping)
        """

    async def start_network_resource_update(
        self, **kwargs: Unpack[StartNetworkResourceUpdateRequestTypeDef]
    ) -> StartNetworkResourceUpdateResponseTypeDef:
        """
        Use this action to do the following tasks:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/start_network_resource_update.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#start_network_resource_update)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#untag_resource)
        """

    async def update_network_site(
        self, **kwargs: Unpack[UpdateNetworkSiteRequestTypeDef]
    ) -> UpdateNetworkSiteResponseTypeDef:
        """
        Updates the specified network site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/update_network_site.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#update_network_site)
        """

    async def update_network_site_plan(
        self, **kwargs: Unpack[UpdateNetworkSitePlanRequestTypeDef]
    ) -> UpdateNetworkSiteResponseTypeDef:
        """
        Updates the specified network site plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/update_network_site_plan.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#update_network_site_plan)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_device_identifiers"]
    ) -> ListDeviceIdentifiersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_network_resources"]
    ) -> ListNetworkResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_network_sites"]
    ) -> ListNetworkSitesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_networks"]
    ) -> ListNetworksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_orders"]
    ) -> ListOrdersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/client/)
        """
