"""
Type annotations for networkmanager service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_networkmanager.client import NetworkManagerClient
    from types_aiobotocore_networkmanager.paginator import (
        DescribeGlobalNetworksPaginator,
        GetConnectPeerAssociationsPaginator,
        GetConnectionsPaginator,
        GetCoreNetworkChangeEventsPaginator,
        GetCoreNetworkChangeSetPaginator,
        GetCustomerGatewayAssociationsPaginator,
        GetDevicesPaginator,
        GetLinkAssociationsPaginator,
        GetLinksPaginator,
        GetNetworkResourceCountsPaginator,
        GetNetworkResourceRelationshipsPaginator,
        GetNetworkResourcesPaginator,
        GetNetworkTelemetryPaginator,
        GetSitesPaginator,
        GetTransitGatewayConnectPeerAssociationsPaginator,
        GetTransitGatewayRegistrationsPaginator,
        ListAttachmentsPaginator,
        ListConnectPeersPaginator,
        ListCoreNetworkPolicyVersionsPaginator,
        ListCoreNetworksPaginator,
        ListPeeringsPaginator,
    )

    session = get_session()
    with session.create_client("networkmanager") as client:
        client: NetworkManagerClient

        describe_global_networks_paginator: DescribeGlobalNetworksPaginator = client.get_paginator("describe_global_networks")
        get_connect_peer_associations_paginator: GetConnectPeerAssociationsPaginator = client.get_paginator("get_connect_peer_associations")
        get_connections_paginator: GetConnectionsPaginator = client.get_paginator("get_connections")
        get_core_network_change_events_paginator: GetCoreNetworkChangeEventsPaginator = client.get_paginator("get_core_network_change_events")
        get_core_network_change_set_paginator: GetCoreNetworkChangeSetPaginator = client.get_paginator("get_core_network_change_set")
        get_customer_gateway_associations_paginator: GetCustomerGatewayAssociationsPaginator = client.get_paginator("get_customer_gateway_associations")
        get_devices_paginator: GetDevicesPaginator = client.get_paginator("get_devices")
        get_link_associations_paginator: GetLinkAssociationsPaginator = client.get_paginator("get_link_associations")
        get_links_paginator: GetLinksPaginator = client.get_paginator("get_links")
        get_network_resource_counts_paginator: GetNetworkResourceCountsPaginator = client.get_paginator("get_network_resource_counts")
        get_network_resource_relationships_paginator: GetNetworkResourceRelationshipsPaginator = client.get_paginator("get_network_resource_relationships")
        get_network_resources_paginator: GetNetworkResourcesPaginator = client.get_paginator("get_network_resources")
        get_network_telemetry_paginator: GetNetworkTelemetryPaginator = client.get_paginator("get_network_telemetry")
        get_sites_paginator: GetSitesPaginator = client.get_paginator("get_sites")
        get_transit_gateway_connect_peer_associations_paginator: GetTransitGatewayConnectPeerAssociationsPaginator = client.get_paginator("get_transit_gateway_connect_peer_associations")
        get_transit_gateway_registrations_paginator: GetTransitGatewayRegistrationsPaginator = client.get_paginator("get_transit_gateway_registrations")
        list_attachments_paginator: ListAttachmentsPaginator = client.get_paginator("list_attachments")
        list_connect_peers_paginator: ListConnectPeersPaginator = client.get_paginator("list_connect_peers")
        list_core_network_policy_versions_paginator: ListCoreNetworkPolicyVersionsPaginator = client.get_paginator("list_core_network_policy_versions")
        list_core_networks_paginator: ListCoreNetworksPaginator = client.get_paginator("list_core_networks")
        list_peerings_paginator: ListPeeringsPaginator = client.get_paginator("list_peerings")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeGlobalNetworksRequestPaginateTypeDef,
    DescribeGlobalNetworksResponseTypeDef,
    GetConnectionsRequestPaginateTypeDef,
    GetConnectionsResponseTypeDef,
    GetConnectPeerAssociationsRequestPaginateTypeDef,
    GetConnectPeerAssociationsResponseTypeDef,
    GetCoreNetworkChangeEventsRequestPaginateTypeDef,
    GetCoreNetworkChangeEventsResponseTypeDef,
    GetCoreNetworkChangeSetRequestPaginateTypeDef,
    GetCoreNetworkChangeSetResponseTypeDef,
    GetCustomerGatewayAssociationsRequestPaginateTypeDef,
    GetCustomerGatewayAssociationsResponseTypeDef,
    GetDevicesRequestPaginateTypeDef,
    GetDevicesResponseTypeDef,
    GetLinkAssociationsRequestPaginateTypeDef,
    GetLinkAssociationsResponseTypeDef,
    GetLinksRequestPaginateTypeDef,
    GetLinksResponseTypeDef,
    GetNetworkResourceCountsRequestPaginateTypeDef,
    GetNetworkResourceCountsResponseTypeDef,
    GetNetworkResourceRelationshipsRequestPaginateTypeDef,
    GetNetworkResourceRelationshipsResponseTypeDef,
    GetNetworkResourcesRequestPaginateTypeDef,
    GetNetworkResourcesResponseTypeDef,
    GetNetworkTelemetryRequestPaginateTypeDef,
    GetNetworkTelemetryResponseTypeDef,
    GetSitesRequestPaginateTypeDef,
    GetSitesResponseTypeDef,
    GetTransitGatewayConnectPeerAssociationsRequestPaginateTypeDef,
    GetTransitGatewayConnectPeerAssociationsResponseTypeDef,
    GetTransitGatewayRegistrationsRequestPaginateTypeDef,
    GetTransitGatewayRegistrationsResponseTypeDef,
    ListAttachmentsRequestPaginateTypeDef,
    ListAttachmentsResponseTypeDef,
    ListConnectPeersRequestPaginateTypeDef,
    ListConnectPeersResponseTypeDef,
    ListCoreNetworkPolicyVersionsRequestPaginateTypeDef,
    ListCoreNetworkPolicyVersionsResponseTypeDef,
    ListCoreNetworksRequestPaginateTypeDef,
    ListCoreNetworksResponseTypeDef,
    ListPeeringsRequestPaginateTypeDef,
    ListPeeringsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeGlobalNetworksPaginator",
    "GetConnectPeerAssociationsPaginator",
    "GetConnectionsPaginator",
    "GetCoreNetworkChangeEventsPaginator",
    "GetCoreNetworkChangeSetPaginator",
    "GetCustomerGatewayAssociationsPaginator",
    "GetDevicesPaginator",
    "GetLinkAssociationsPaginator",
    "GetLinksPaginator",
    "GetNetworkResourceCountsPaginator",
    "GetNetworkResourceRelationshipsPaginator",
    "GetNetworkResourcesPaginator",
    "GetNetworkTelemetryPaginator",
    "GetSitesPaginator",
    "GetTransitGatewayConnectPeerAssociationsPaginator",
    "GetTransitGatewayRegistrationsPaginator",
    "ListAttachmentsPaginator",
    "ListConnectPeersPaginator",
    "ListCoreNetworkPolicyVersionsPaginator",
    "ListCoreNetworksPaginator",
    "ListPeeringsPaginator",
)


if TYPE_CHECKING:
    _DescribeGlobalNetworksPaginatorBase = AioPaginator[DescribeGlobalNetworksResponseTypeDef]
else:
    _DescribeGlobalNetworksPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeGlobalNetworksPaginator(_DescribeGlobalNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/DescribeGlobalNetworks.html#NetworkManager.Paginator.DescribeGlobalNetworks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#describeglobalnetworkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGlobalNetworksRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeGlobalNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/DescribeGlobalNetworks.html#NetworkManager.Paginator.DescribeGlobalNetworks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#describeglobalnetworkspaginator)
        """


if TYPE_CHECKING:
    _GetConnectPeerAssociationsPaginatorBase = AioPaginator[
        GetConnectPeerAssociationsResponseTypeDef
    ]
else:
    _GetConnectPeerAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetConnectPeerAssociationsPaginator(_GetConnectPeerAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnectPeerAssociations.html#NetworkManager.Paginator.GetConnectPeerAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getconnectpeerassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetConnectPeerAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetConnectPeerAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnectPeerAssociations.html#NetworkManager.Paginator.GetConnectPeerAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getconnectpeerassociationspaginator)
        """


if TYPE_CHECKING:
    _GetConnectionsPaginatorBase = AioPaginator[GetConnectionsResponseTypeDef]
else:
    _GetConnectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetConnectionsPaginator(_GetConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnections.html#NetworkManager.Paginator.GetConnections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getconnectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetConnectionsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetConnections.html#NetworkManager.Paginator.GetConnections.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getconnectionspaginator)
        """


if TYPE_CHECKING:
    _GetCoreNetworkChangeEventsPaginatorBase = AioPaginator[
        GetCoreNetworkChangeEventsResponseTypeDef
    ]
else:
    _GetCoreNetworkChangeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetCoreNetworkChangeEventsPaginator(_GetCoreNetworkChangeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeEvents.html#NetworkManager.Paginator.GetCoreNetworkChangeEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcorenetworkchangeeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCoreNetworkChangeEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCoreNetworkChangeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeEvents.html#NetworkManager.Paginator.GetCoreNetworkChangeEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcorenetworkchangeeventspaginator)
        """


if TYPE_CHECKING:
    _GetCoreNetworkChangeSetPaginatorBase = AioPaginator[GetCoreNetworkChangeSetResponseTypeDef]
else:
    _GetCoreNetworkChangeSetPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetCoreNetworkChangeSetPaginator(_GetCoreNetworkChangeSetPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeSet.html#NetworkManager.Paginator.GetCoreNetworkChangeSet)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcorenetworkchangesetpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCoreNetworkChangeSetRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCoreNetworkChangeSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCoreNetworkChangeSet.html#NetworkManager.Paginator.GetCoreNetworkChangeSet.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcorenetworkchangesetpaginator)
        """


if TYPE_CHECKING:
    _GetCustomerGatewayAssociationsPaginatorBase = AioPaginator[
        GetCustomerGatewayAssociationsResponseTypeDef
    ]
else:
    _GetCustomerGatewayAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetCustomerGatewayAssociationsPaginator(_GetCustomerGatewayAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCustomerGatewayAssociations.html#NetworkManager.Paginator.GetCustomerGatewayAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcustomergatewayassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCustomerGatewayAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCustomerGatewayAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetCustomerGatewayAssociations.html#NetworkManager.Paginator.GetCustomerGatewayAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getcustomergatewayassociationspaginator)
        """


if TYPE_CHECKING:
    _GetDevicesPaginatorBase = AioPaginator[GetDevicesResponseTypeDef]
else:
    _GetDevicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetDevicesPaginator(_GetDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetDevices.html#NetworkManager.Paginator.GetDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getdevicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDevicesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetDevices.html#NetworkManager.Paginator.GetDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getdevicespaginator)
        """


if TYPE_CHECKING:
    _GetLinkAssociationsPaginatorBase = AioPaginator[GetLinkAssociationsResponseTypeDef]
else:
    _GetLinkAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetLinkAssociationsPaginator(_GetLinkAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinkAssociations.html#NetworkManager.Paginator.GetLinkAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getlinkassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetLinkAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinkAssociations.html#NetworkManager.Paginator.GetLinkAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getlinkassociationspaginator)
        """


if TYPE_CHECKING:
    _GetLinksPaginatorBase = AioPaginator[GetLinksResponseTypeDef]
else:
    _GetLinksPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetLinksPaginator(_GetLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinks.html#NetworkManager.Paginator.GetLinks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getlinkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinksRequestPaginateTypeDef]
    ) -> AioPageIterator[GetLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetLinks.html#NetworkManager.Paginator.GetLinks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getlinkspaginator)
        """


if TYPE_CHECKING:
    _GetNetworkResourceCountsPaginatorBase = AioPaginator[GetNetworkResourceCountsResponseTypeDef]
else:
    _GetNetworkResourceCountsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetNetworkResourceCountsPaginator(_GetNetworkResourceCountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceCounts.html#NetworkManager.Paginator.GetNetworkResourceCounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcecountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetNetworkResourceCountsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetNetworkResourceCountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceCounts.html#NetworkManager.Paginator.GetNetworkResourceCounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcecountspaginator)
        """


if TYPE_CHECKING:
    _GetNetworkResourceRelationshipsPaginatorBase = AioPaginator[
        GetNetworkResourceRelationshipsResponseTypeDef
    ]
else:
    _GetNetworkResourceRelationshipsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetNetworkResourceRelationshipsPaginator(_GetNetworkResourceRelationshipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceRelationships.html#NetworkManager.Paginator.GetNetworkResourceRelationships)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcerelationshipspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetNetworkResourceRelationshipsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetNetworkResourceRelationshipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResourceRelationships.html#NetworkManager.Paginator.GetNetworkResourceRelationships.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcerelationshipspaginator)
        """


if TYPE_CHECKING:
    _GetNetworkResourcesPaginatorBase = AioPaginator[GetNetworkResourcesResponseTypeDef]
else:
    _GetNetworkResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetNetworkResourcesPaginator(_GetNetworkResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResources.html#NetworkManager.Paginator.GetNetworkResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetNetworkResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetNetworkResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkResources.html#NetworkManager.Paginator.GetNetworkResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworkresourcespaginator)
        """


if TYPE_CHECKING:
    _GetNetworkTelemetryPaginatorBase = AioPaginator[GetNetworkTelemetryResponseTypeDef]
else:
    _GetNetworkTelemetryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetNetworkTelemetryPaginator(_GetNetworkTelemetryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkTelemetry.html#NetworkManager.Paginator.GetNetworkTelemetry)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworktelemetrypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetNetworkTelemetryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetNetworkTelemetryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetNetworkTelemetry.html#NetworkManager.Paginator.GetNetworkTelemetry.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getnetworktelemetrypaginator)
        """


if TYPE_CHECKING:
    _GetSitesPaginatorBase = AioPaginator[GetSitesResponseTypeDef]
else:
    _GetSitesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetSitesPaginator(_GetSitesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetSites.html#NetworkManager.Paginator.GetSites)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getsitespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetSitesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetSitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetSites.html#NetworkManager.Paginator.GetSites.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#getsitespaginator)
        """


if TYPE_CHECKING:
    _GetTransitGatewayConnectPeerAssociationsPaginatorBase = AioPaginator[
        GetTransitGatewayConnectPeerAssociationsResponseTypeDef
    ]
else:
    _GetTransitGatewayConnectPeerAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetTransitGatewayConnectPeerAssociationsPaginator(
    _GetTransitGatewayConnectPeerAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayConnectPeerAssociations.html#NetworkManager.Paginator.GetTransitGatewayConnectPeerAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#gettransitgatewayconnectpeerassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetTransitGatewayConnectPeerAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetTransitGatewayConnectPeerAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayConnectPeerAssociations.html#NetworkManager.Paginator.GetTransitGatewayConnectPeerAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#gettransitgatewayconnectpeerassociationspaginator)
        """


if TYPE_CHECKING:
    _GetTransitGatewayRegistrationsPaginatorBase = AioPaginator[
        GetTransitGatewayRegistrationsResponseTypeDef
    ]
else:
    _GetTransitGatewayRegistrationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetTransitGatewayRegistrationsPaginator(_GetTransitGatewayRegistrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayRegistrations.html#NetworkManager.Paginator.GetTransitGatewayRegistrations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#gettransitgatewayregistrationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetTransitGatewayRegistrationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetTransitGatewayRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/GetTransitGatewayRegistrations.html#NetworkManager.Paginator.GetTransitGatewayRegistrations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#gettransitgatewayregistrationspaginator)
        """


if TYPE_CHECKING:
    _ListAttachmentsPaginatorBase = AioPaginator[ListAttachmentsResponseTypeDef]
else:
    _ListAttachmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAttachmentsPaginator(_ListAttachmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListAttachments.html#NetworkManager.Paginator.ListAttachments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listattachmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListAttachments.html#NetworkManager.Paginator.ListAttachments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listattachmentspaginator)
        """


if TYPE_CHECKING:
    _ListConnectPeersPaginatorBase = AioPaginator[ListConnectPeersResponseTypeDef]
else:
    _ListConnectPeersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConnectPeersPaginator(_ListConnectPeersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListConnectPeers.html#NetworkManager.Paginator.ListConnectPeers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listconnectpeerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectPeersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectPeersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListConnectPeers.html#NetworkManager.Paginator.ListConnectPeers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listconnectpeerspaginator)
        """


if TYPE_CHECKING:
    _ListCoreNetworkPolicyVersionsPaginatorBase = AioPaginator[
        ListCoreNetworkPolicyVersionsResponseTypeDef
    ]
else:
    _ListCoreNetworkPolicyVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCoreNetworkPolicyVersionsPaginator(_ListCoreNetworkPolicyVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworkPolicyVersions.html#NetworkManager.Paginator.ListCoreNetworkPolicyVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listcorenetworkpolicyversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCoreNetworkPolicyVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCoreNetworkPolicyVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworkPolicyVersions.html#NetworkManager.Paginator.ListCoreNetworkPolicyVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listcorenetworkpolicyversionspaginator)
        """


if TYPE_CHECKING:
    _ListCoreNetworksPaginatorBase = AioPaginator[ListCoreNetworksResponseTypeDef]
else:
    _ListCoreNetworksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCoreNetworksPaginator(_ListCoreNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworks.html#NetworkManager.Paginator.ListCoreNetworks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listcorenetworkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCoreNetworksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCoreNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListCoreNetworks.html#NetworkManager.Paginator.ListCoreNetworks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listcorenetworkspaginator)
        """


if TYPE_CHECKING:
    _ListPeeringsPaginatorBase = AioPaginator[ListPeeringsResponseTypeDef]
else:
    _ListPeeringsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPeeringsPaginator(_ListPeeringsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListPeerings.html#NetworkManager.Paginator.ListPeerings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listpeeringspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPeeringsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPeeringsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager/paginator/ListPeerings.html#NetworkManager.Paginator.ListPeerings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmanager/paginators/#listpeeringspaginator)
        """
