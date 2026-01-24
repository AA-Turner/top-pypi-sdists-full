"""
Type annotations for mediaconnect service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediaconnect.client import MediaConnectClient
    from types_aiobotocore_mediaconnect.paginator import (
        ListBridgesPaginator,
        ListEntitlementsPaginator,
        ListFlowsPaginator,
        ListGatewayInstancesPaginator,
        ListGatewaysPaginator,
        ListOfferingsPaginator,
        ListReservationsPaginator,
        ListRouterInputsPaginator,
        ListRouterNetworkInterfacesPaginator,
        ListRouterOutputsPaginator,
    )

    session = get_session()
    with session.create_client("mediaconnect") as client:
        client: MediaConnectClient

        list_bridges_paginator: ListBridgesPaginator = client.get_paginator("list_bridges")
        list_entitlements_paginator: ListEntitlementsPaginator = client.get_paginator("list_entitlements")
        list_flows_paginator: ListFlowsPaginator = client.get_paginator("list_flows")
        list_gateway_instances_paginator: ListGatewayInstancesPaginator = client.get_paginator("list_gateway_instances")
        list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
        list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
        list_reservations_paginator: ListReservationsPaginator = client.get_paginator("list_reservations")
        list_router_inputs_paginator: ListRouterInputsPaginator = client.get_paginator("list_router_inputs")
        list_router_network_interfaces_paginator: ListRouterNetworkInterfacesPaginator = client.get_paginator("list_router_network_interfaces")
        list_router_outputs_paginator: ListRouterOutputsPaginator = client.get_paginator("list_router_outputs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListBridgesRequestPaginateTypeDef,
    ListBridgesResponseTypeDef,
    ListEntitlementsRequestPaginateTypeDef,
    ListEntitlementsResponseTypeDef,
    ListFlowsRequestPaginateTypeDef,
    ListFlowsResponseTypeDef,
    ListGatewayInstancesRequestPaginateTypeDef,
    ListGatewayInstancesResponseTypeDef,
    ListGatewaysRequestPaginateTypeDef,
    ListGatewaysResponseTypeDef,
    ListOfferingsRequestPaginateTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsRequestPaginateTypeDef,
    ListReservationsResponseTypeDef,
    ListRouterInputsRequestPaginateTypeDef,
    ListRouterInputsResponseTypeDef,
    ListRouterNetworkInterfacesRequestPaginateTypeDef,
    ListRouterNetworkInterfacesResponseTypeDef,
    ListRouterOutputsRequestPaginateTypeDef,
    ListRouterOutputsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBridgesPaginator",
    "ListEntitlementsPaginator",
    "ListFlowsPaginator",
    "ListGatewayInstancesPaginator",
    "ListGatewaysPaginator",
    "ListOfferingsPaginator",
    "ListReservationsPaginator",
    "ListRouterInputsPaginator",
    "ListRouterNetworkInterfacesPaginator",
    "ListRouterOutputsPaginator",
)

if TYPE_CHECKING:
    _ListBridgesPaginatorBase = AioPaginator[ListBridgesResponseTypeDef]
else:
    _ListBridgesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBridgesPaginator(_ListBridgesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListBridges.html#MediaConnect.Paginator.ListBridges)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listbridgespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBridgesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBridgesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListBridges.html#MediaConnect.Paginator.ListBridges.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listbridgespaginator)
        """

if TYPE_CHECKING:
    _ListEntitlementsPaginatorBase = AioPaginator[ListEntitlementsResponseTypeDef]
else:
    _ListEntitlementsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEntitlementsPaginator(_ListEntitlementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListEntitlements.html#MediaConnect.Paginator.ListEntitlements)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listentitlementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEntitlementsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEntitlementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListEntitlements.html#MediaConnect.Paginator.ListEntitlements.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listentitlementspaginator)
        """

if TYPE_CHECKING:
    _ListFlowsPaginatorBase = AioPaginator[ListFlowsResponseTypeDef]
else:
    _ListFlowsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFlowsPaginator(_ListFlowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListFlows.html#MediaConnect.Paginator.ListFlows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListFlows.html#MediaConnect.Paginator.ListFlows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listflowspaginator)
        """

if TYPE_CHECKING:
    _ListGatewayInstancesPaginatorBase = AioPaginator[ListGatewayInstancesResponseTypeDef]
else:
    _ListGatewayInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGatewayInstancesPaginator(_ListGatewayInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListGatewayInstances.html#MediaConnect.Paginator.ListGatewayInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listgatewayinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGatewayInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGatewayInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListGatewayInstances.html#MediaConnect.Paginator.ListGatewayInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listgatewayinstancespaginator)
        """

if TYPE_CHECKING:
    _ListGatewaysPaginatorBase = AioPaginator[ListGatewaysResponseTypeDef]
else:
    _ListGatewaysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGatewaysPaginator(_ListGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListGateways.html#MediaConnect.Paginator.ListGateways)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listgatewayspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGatewaysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGatewaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListGateways.html#MediaConnect.Paginator.ListGateways.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listgatewayspaginator)
        """

if TYPE_CHECKING:
    _ListOfferingsPaginatorBase = AioPaginator[ListOfferingsResponseTypeDef]
else:
    _ListOfferingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOfferingsPaginator(_ListOfferingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListOfferings.html#MediaConnect.Paginator.ListOfferings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listofferingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOfferingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListOfferings.html#MediaConnect.Paginator.ListOfferings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listofferingspaginator)
        """

if TYPE_CHECKING:
    _ListReservationsPaginatorBase = AioPaginator[ListReservationsResponseTypeDef]
else:
    _ListReservationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReservationsPaginator(_ListReservationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListReservations.html#MediaConnect.Paginator.ListReservations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listreservationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReservationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReservationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListReservations.html#MediaConnect.Paginator.ListReservations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listreservationspaginator)
        """

if TYPE_CHECKING:
    _ListRouterInputsPaginatorBase = AioPaginator[ListRouterInputsResponseTypeDef]
else:
    _ListRouterInputsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRouterInputsPaginator(_ListRouterInputsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListRouterInputs.html#MediaConnect.Paginator.ListRouterInputs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listrouterinputspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRouterInputsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRouterInputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListRouterInputs.html#MediaConnect.Paginator.ListRouterInputs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listrouterinputspaginator)
        """

if TYPE_CHECKING:
    _ListRouterNetworkInterfacesPaginatorBase = AioPaginator[
        ListRouterNetworkInterfacesResponseTypeDef
    ]
else:
    _ListRouterNetworkInterfacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRouterNetworkInterfacesPaginator(_ListRouterNetworkInterfacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListRouterNetworkInterfaces.html#MediaConnect.Paginator.ListRouterNetworkInterfaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listrouternetworkinterfacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRouterNetworkInterfacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRouterNetworkInterfacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListRouterNetworkInterfaces.html#MediaConnect.Paginator.ListRouterNetworkInterfaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listrouternetworkinterfacespaginator)
        """

if TYPE_CHECKING:
    _ListRouterOutputsPaginatorBase = AioPaginator[ListRouterOutputsResponseTypeDef]
else:
    _ListRouterOutputsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRouterOutputsPaginator(_ListRouterOutputsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListRouterOutputs.html#MediaConnect.Paginator.ListRouterOutputs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listrouteroutputspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRouterOutputsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRouterOutputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect/paginator/ListRouterOutputs.html#MediaConnect.Paginator.ListRouterOutputs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listrouteroutputspaginator)
        """
