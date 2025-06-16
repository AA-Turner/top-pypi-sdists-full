"""
Type annotations for vpc-lattice service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_vpc_lattice.client import VPCLatticeClient
    from types_aiobotocore_vpc_lattice.paginator import (
        ListAccessLogSubscriptionsPaginator,
        ListListenersPaginator,
        ListResourceConfigurationsPaginator,
        ListResourceEndpointAssociationsPaginator,
        ListResourceGatewaysPaginator,
        ListRulesPaginator,
        ListServiceNetworkResourceAssociationsPaginator,
        ListServiceNetworkServiceAssociationsPaginator,
        ListServiceNetworkVpcAssociationsPaginator,
        ListServiceNetworkVpcEndpointAssociationsPaginator,
        ListServiceNetworksPaginator,
        ListServicesPaginator,
        ListTargetGroupsPaginator,
        ListTargetsPaginator,
    )

    session = get_session()
    with session.create_client("vpc-lattice") as client:
        client: VPCLatticeClient

        list_access_log_subscriptions_paginator: ListAccessLogSubscriptionsPaginator = client.get_paginator("list_access_log_subscriptions")
        list_listeners_paginator: ListListenersPaginator = client.get_paginator("list_listeners")
        list_resource_configurations_paginator: ListResourceConfigurationsPaginator = client.get_paginator("list_resource_configurations")
        list_resource_endpoint_associations_paginator: ListResourceEndpointAssociationsPaginator = client.get_paginator("list_resource_endpoint_associations")
        list_resource_gateways_paginator: ListResourceGatewaysPaginator = client.get_paginator("list_resource_gateways")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_service_network_resource_associations_paginator: ListServiceNetworkResourceAssociationsPaginator = client.get_paginator("list_service_network_resource_associations")
        list_service_network_service_associations_paginator: ListServiceNetworkServiceAssociationsPaginator = client.get_paginator("list_service_network_service_associations")
        list_service_network_vpc_associations_paginator: ListServiceNetworkVpcAssociationsPaginator = client.get_paginator("list_service_network_vpc_associations")
        list_service_network_vpc_endpoint_associations_paginator: ListServiceNetworkVpcEndpointAssociationsPaginator = client.get_paginator("list_service_network_vpc_endpoint_associations")
        list_service_networks_paginator: ListServiceNetworksPaginator = client.get_paginator("list_service_networks")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
        list_target_groups_paginator: ListTargetGroupsPaginator = client.get_paginator("list_target_groups")
        list_targets_paginator: ListTargetsPaginator = client.get_paginator("list_targets")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAccessLogSubscriptionsRequestPaginateTypeDef,
    ListAccessLogSubscriptionsResponseTypeDef,
    ListListenersRequestPaginateTypeDef,
    ListListenersResponseTypeDef,
    ListResourceConfigurationsRequestPaginateTypeDef,
    ListResourceConfigurationsResponseTypeDef,
    ListResourceEndpointAssociationsRequestPaginateTypeDef,
    ListResourceEndpointAssociationsResponseTypeDef,
    ListResourceGatewaysRequestPaginateTypeDef,
    ListResourceGatewaysResponseTypeDef,
    ListRulesRequestPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListServiceNetworkResourceAssociationsRequestPaginateTypeDef,
    ListServiceNetworkResourceAssociationsResponseTypeDef,
    ListServiceNetworkServiceAssociationsRequestPaginateTypeDef,
    ListServiceNetworkServiceAssociationsResponseTypeDef,
    ListServiceNetworksRequestPaginateTypeDef,
    ListServiceNetworksResponseTypeDef,
    ListServiceNetworkVpcAssociationsRequestPaginateTypeDef,
    ListServiceNetworkVpcAssociationsResponseTypeDef,
    ListServiceNetworkVpcEndpointAssociationsRequestPaginateTypeDef,
    ListServiceNetworkVpcEndpointAssociationsResponseTypeDef,
    ListServicesRequestPaginateTypeDef,
    ListServicesResponseTypeDef,
    ListTargetGroupsRequestPaginateTypeDef,
    ListTargetGroupsResponseTypeDef,
    ListTargetsRequestPaginateTypeDef,
    ListTargetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAccessLogSubscriptionsPaginator",
    "ListListenersPaginator",
    "ListResourceConfigurationsPaginator",
    "ListResourceEndpointAssociationsPaginator",
    "ListResourceGatewaysPaginator",
    "ListRulesPaginator",
    "ListServiceNetworkResourceAssociationsPaginator",
    "ListServiceNetworkServiceAssociationsPaginator",
    "ListServiceNetworkVpcAssociationsPaginator",
    "ListServiceNetworkVpcEndpointAssociationsPaginator",
    "ListServiceNetworksPaginator",
    "ListServicesPaginator",
    "ListTargetGroupsPaginator",
    "ListTargetsPaginator",
)

if TYPE_CHECKING:
    _ListAccessLogSubscriptionsPaginatorBase = AioPaginator[
        ListAccessLogSubscriptionsResponseTypeDef
    ]
else:
    _ListAccessLogSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccessLogSubscriptionsPaginator(_ListAccessLogSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListAccessLogSubscriptions.html#VPCLattice.Paginator.ListAccessLogSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listaccesslogsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessLogSubscriptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccessLogSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListAccessLogSubscriptions.html#VPCLattice.Paginator.ListAccessLogSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listaccesslogsubscriptionspaginator)
        """

if TYPE_CHECKING:
    _ListListenersPaginatorBase = AioPaginator[ListListenersResponseTypeDef]
else:
    _ListListenersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListListenersPaginator(_ListListenersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListListeners.html#VPCLattice.Paginator.ListListeners)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listlistenerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListListenersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListListeners.html#VPCLattice.Paginator.ListListeners.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listlistenerspaginator)
        """

if TYPE_CHECKING:
    _ListResourceConfigurationsPaginatorBase = AioPaginator[
        ListResourceConfigurationsResponseTypeDef
    ]
else:
    _ListResourceConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceConfigurationsPaginator(_ListResourceConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceConfigurations.html#VPCLattice.Paginator.ListResourceConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listresourceconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceConfigurations.html#VPCLattice.Paginator.ListResourceConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listresourceconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListResourceEndpointAssociationsPaginatorBase = AioPaginator[
        ListResourceEndpointAssociationsResponseTypeDef
    ]
else:
    _ListResourceEndpointAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceEndpointAssociationsPaginator(_ListResourceEndpointAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceEndpointAssociations.html#VPCLattice.Paginator.ListResourceEndpointAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listresourceendpointassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceEndpointAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceEndpointAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceEndpointAssociations.html#VPCLattice.Paginator.ListResourceEndpointAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listresourceendpointassociationspaginator)
        """

if TYPE_CHECKING:
    _ListResourceGatewaysPaginatorBase = AioPaginator[ListResourceGatewaysResponseTypeDef]
else:
    _ListResourceGatewaysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceGatewaysPaginator(_ListResourceGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceGateways.html#VPCLattice.Paginator.ListResourceGateways)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listresourcegatewayspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceGatewaysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceGatewaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListResourceGateways.html#VPCLattice.Paginator.ListResourceGateways.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listresourcegatewayspaginator)
        """

if TYPE_CHECKING:
    _ListRulesPaginatorBase = AioPaginator[ListRulesResponseTypeDef]
else:
    _ListRulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRulesPaginator(_ListRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListRules.html#VPCLattice.Paginator.ListRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listrulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListRules.html#VPCLattice.Paginator.ListRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listrulespaginator)
        """

if TYPE_CHECKING:
    _ListServiceNetworkResourceAssociationsPaginatorBase = AioPaginator[
        ListServiceNetworkResourceAssociationsResponseTypeDef
    ]
else:
    _ListServiceNetworkResourceAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceNetworkResourceAssociationsPaginator(
    _ListServiceNetworkResourceAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkResourceAssociations.html#VPCLattice.Paginator.ListServiceNetworkResourceAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkresourceassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceNetworkResourceAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceNetworkResourceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkResourceAssociations.html#VPCLattice.Paginator.ListServiceNetworkResourceAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkresourceassociationspaginator)
        """

if TYPE_CHECKING:
    _ListServiceNetworkServiceAssociationsPaginatorBase = AioPaginator[
        ListServiceNetworkServiceAssociationsResponseTypeDef
    ]
else:
    _ListServiceNetworkServiceAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceNetworkServiceAssociationsPaginator(
    _ListServiceNetworkServiceAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkServiceAssociations.html#VPCLattice.Paginator.ListServiceNetworkServiceAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkserviceassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceNetworkServiceAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceNetworkServiceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkServiceAssociations.html#VPCLattice.Paginator.ListServiceNetworkServiceAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkserviceassociationspaginator)
        """

if TYPE_CHECKING:
    _ListServiceNetworkVpcAssociationsPaginatorBase = AioPaginator[
        ListServiceNetworkVpcAssociationsResponseTypeDef
    ]
else:
    _ListServiceNetworkVpcAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceNetworkVpcAssociationsPaginator(_ListServiceNetworkVpcAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkvpcassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceNetworkVpcAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceNetworkVpcAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkvpcassociationspaginator)
        """

if TYPE_CHECKING:
    _ListServiceNetworkVpcEndpointAssociationsPaginatorBase = AioPaginator[
        ListServiceNetworkVpcEndpointAssociationsResponseTypeDef
    ]
else:
    _ListServiceNetworkVpcEndpointAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceNetworkVpcEndpointAssociationsPaginator(
    _ListServiceNetworkVpcEndpointAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcEndpointAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcEndpointAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkvpcendpointassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceNetworkVpcEndpointAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceNetworkVpcEndpointAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworkVpcEndpointAssociations.html#VPCLattice.Paginator.ListServiceNetworkVpcEndpointAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkvpcendpointassociationspaginator)
        """

if TYPE_CHECKING:
    _ListServiceNetworksPaginatorBase = AioPaginator[ListServiceNetworksResponseTypeDef]
else:
    _ListServiceNetworksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceNetworksPaginator(_ListServiceNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworks.html#VPCLattice.Paginator.ListServiceNetworks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceNetworksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServiceNetworks.html#VPCLattice.Paginator.ListServiceNetworks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicenetworkspaginator)
        """

if TYPE_CHECKING:
    _ListServicesPaginatorBase = AioPaginator[ListServicesResponseTypeDef]
else:
    _ListServicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServices.html#VPCLattice.Paginator.ListServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListServices.html#VPCLattice.Paginator.ListServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listservicespaginator)
        """

if TYPE_CHECKING:
    _ListTargetGroupsPaginatorBase = AioPaginator[ListTargetGroupsResponseTypeDef]
else:
    _ListTargetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTargetGroupsPaginator(_ListTargetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargetGroups.html#VPCLattice.Paginator.ListTargetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listtargetgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargetGroups.html#VPCLattice.Paginator.ListTargetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listtargetgroupspaginator)
        """

if TYPE_CHECKING:
    _ListTargetsPaginatorBase = AioPaginator[ListTargetsResponseTypeDef]
else:
    _ListTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTargetsPaginator(_ListTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargets.html#VPCLattice.Paginator.ListTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listtargetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/paginator/ListTargets.html#VPCLattice.Paginator.ListTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_vpc_lattice/paginators/#listtargetspaginator)
        """
