"""
Type annotations for globalaccelerator service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_globalaccelerator.client import GlobalAcceleratorClient
    from types_aiobotocore_globalaccelerator.paginator import (
        ListAcceleratorsPaginator,
        ListByoipCidrsPaginator,
        ListCrossAccountAttachmentsPaginator,
        ListCrossAccountResourcesPaginator,
        ListCustomRoutingAcceleratorsPaginator,
        ListCustomRoutingEndpointGroupsPaginator,
        ListCustomRoutingListenersPaginator,
        ListCustomRoutingPortMappingsByDestinationPaginator,
        ListCustomRoutingPortMappingsPaginator,
        ListEndpointGroupsPaginator,
        ListListenersPaginator,
    )

    session = get_session()
    with session.create_client("globalaccelerator") as client:
        client: GlobalAcceleratorClient

        list_accelerators_paginator: ListAcceleratorsPaginator = client.get_paginator("list_accelerators")
        list_byoip_cidrs_paginator: ListByoipCidrsPaginator = client.get_paginator("list_byoip_cidrs")
        list_cross_account_attachments_paginator: ListCrossAccountAttachmentsPaginator = client.get_paginator("list_cross_account_attachments")
        list_cross_account_resources_paginator: ListCrossAccountResourcesPaginator = client.get_paginator("list_cross_account_resources")
        list_custom_routing_accelerators_paginator: ListCustomRoutingAcceleratorsPaginator = client.get_paginator("list_custom_routing_accelerators")
        list_custom_routing_endpoint_groups_paginator: ListCustomRoutingEndpointGroupsPaginator = client.get_paginator("list_custom_routing_endpoint_groups")
        list_custom_routing_listeners_paginator: ListCustomRoutingListenersPaginator = client.get_paginator("list_custom_routing_listeners")
        list_custom_routing_port_mappings_by_destination_paginator: ListCustomRoutingPortMappingsByDestinationPaginator = client.get_paginator("list_custom_routing_port_mappings_by_destination")
        list_custom_routing_port_mappings_paginator: ListCustomRoutingPortMappingsPaginator = client.get_paginator("list_custom_routing_port_mappings")
        list_endpoint_groups_paginator: ListEndpointGroupsPaginator = client.get_paginator("list_endpoint_groups")
        list_listeners_paginator: ListListenersPaginator = client.get_paginator("list_listeners")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAcceleratorsRequestPaginateTypeDef,
    ListAcceleratorsResponseTypeDef,
    ListByoipCidrsRequestPaginateTypeDef,
    ListByoipCidrsResponseTypeDef,
    ListCrossAccountAttachmentsRequestPaginateTypeDef,
    ListCrossAccountAttachmentsResponseTypeDef,
    ListCrossAccountResourcesRequestPaginateTypeDef,
    ListCrossAccountResourcesResponseTypeDef,
    ListCustomRoutingAcceleratorsRequestPaginateTypeDef,
    ListCustomRoutingAcceleratorsResponseTypeDef,
    ListCustomRoutingEndpointGroupsRequestPaginateTypeDef,
    ListCustomRoutingEndpointGroupsResponseTypeDef,
    ListCustomRoutingListenersRequestPaginateTypeDef,
    ListCustomRoutingListenersResponseTypeDef,
    ListCustomRoutingPortMappingsByDestinationRequestPaginateTypeDef,
    ListCustomRoutingPortMappingsByDestinationResponseTypeDef,
    ListCustomRoutingPortMappingsRequestPaginateTypeDef,
    ListCustomRoutingPortMappingsResponseTypeDef,
    ListEndpointGroupsRequestPaginateTypeDef,
    ListEndpointGroupsResponseTypeDef,
    ListListenersRequestPaginateTypeDef,
    ListListenersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAcceleratorsPaginator",
    "ListByoipCidrsPaginator",
    "ListCrossAccountAttachmentsPaginator",
    "ListCrossAccountResourcesPaginator",
    "ListCustomRoutingAcceleratorsPaginator",
    "ListCustomRoutingEndpointGroupsPaginator",
    "ListCustomRoutingListenersPaginator",
    "ListCustomRoutingPortMappingsByDestinationPaginator",
    "ListCustomRoutingPortMappingsPaginator",
    "ListEndpointGroupsPaginator",
    "ListListenersPaginator",
)


if TYPE_CHECKING:
    _ListAcceleratorsPaginatorBase = AioPaginator[ListAcceleratorsResponseTypeDef]
else:
    _ListAcceleratorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAcceleratorsPaginator(_ListAcceleratorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListAccelerators.html#GlobalAccelerator.Paginator.ListAccelerators)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listacceleratorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcceleratorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListAccelerators.html#GlobalAccelerator.Paginator.ListAccelerators.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listacceleratorspaginator)
        """


if TYPE_CHECKING:
    _ListByoipCidrsPaginatorBase = AioPaginator[ListByoipCidrsResponseTypeDef]
else:
    _ListByoipCidrsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListByoipCidrsPaginator(_ListByoipCidrsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListByoipCidrs.html#GlobalAccelerator.Paginator.ListByoipCidrs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listbyoipcidrspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListByoipCidrsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListByoipCidrsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListByoipCidrs.html#GlobalAccelerator.Paginator.ListByoipCidrs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listbyoipcidrspaginator)
        """


if TYPE_CHECKING:
    _ListCrossAccountAttachmentsPaginatorBase = AioPaginator[
        ListCrossAccountAttachmentsResponseTypeDef
    ]
else:
    _ListCrossAccountAttachmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCrossAccountAttachmentsPaginator(_ListCrossAccountAttachmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCrossAccountAttachments.html#GlobalAccelerator.Paginator.ListCrossAccountAttachments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcrossaccountattachmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCrossAccountAttachmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCrossAccountAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCrossAccountAttachments.html#GlobalAccelerator.Paginator.ListCrossAccountAttachments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcrossaccountattachmentspaginator)
        """


if TYPE_CHECKING:
    _ListCrossAccountResourcesPaginatorBase = AioPaginator[ListCrossAccountResourcesResponseTypeDef]
else:
    _ListCrossAccountResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCrossAccountResourcesPaginator(_ListCrossAccountResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCrossAccountResources.html#GlobalAccelerator.Paginator.ListCrossAccountResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcrossaccountresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCrossAccountResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCrossAccountResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCrossAccountResources.html#GlobalAccelerator.Paginator.ListCrossAccountResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcrossaccountresourcespaginator)
        """


if TYPE_CHECKING:
    _ListCustomRoutingAcceleratorsPaginatorBase = AioPaginator[
        ListCustomRoutingAcceleratorsResponseTypeDef
    ]
else:
    _ListCustomRoutingAcceleratorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomRoutingAcceleratorsPaginator(_ListCustomRoutingAcceleratorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingAccelerators.html#GlobalAccelerator.Paginator.ListCustomRoutingAccelerators)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutingacceleratorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomRoutingAcceleratorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomRoutingAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingAccelerators.html#GlobalAccelerator.Paginator.ListCustomRoutingAccelerators.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutingacceleratorspaginator)
        """


if TYPE_CHECKING:
    _ListCustomRoutingEndpointGroupsPaginatorBase = AioPaginator[
        ListCustomRoutingEndpointGroupsResponseTypeDef
    ]
else:
    _ListCustomRoutingEndpointGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomRoutingEndpointGroupsPaginator(_ListCustomRoutingEndpointGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingEndpointGroups.html#GlobalAccelerator.Paginator.ListCustomRoutingEndpointGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutingendpointgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomRoutingEndpointGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomRoutingEndpointGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingEndpointGroups.html#GlobalAccelerator.Paginator.ListCustomRoutingEndpointGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutingendpointgroupspaginator)
        """


if TYPE_CHECKING:
    _ListCustomRoutingListenersPaginatorBase = AioPaginator[
        ListCustomRoutingListenersResponseTypeDef
    ]
else:
    _ListCustomRoutingListenersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomRoutingListenersPaginator(_ListCustomRoutingListenersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingListeners.html#GlobalAccelerator.Paginator.ListCustomRoutingListeners)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutinglistenerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomRoutingListenersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomRoutingListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingListeners.html#GlobalAccelerator.Paginator.ListCustomRoutingListeners.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutinglistenerspaginator)
        """


if TYPE_CHECKING:
    _ListCustomRoutingPortMappingsByDestinationPaginatorBase = AioPaginator[
        ListCustomRoutingPortMappingsByDestinationResponseTypeDef
    ]
else:
    _ListCustomRoutingPortMappingsByDestinationPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomRoutingPortMappingsByDestinationPaginator(
    _ListCustomRoutingPortMappingsByDestinationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingPortMappingsByDestination.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappingsByDestination)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutingportmappingsbydestinationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomRoutingPortMappingsByDestinationRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomRoutingPortMappingsByDestinationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingPortMappingsByDestination.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappingsByDestination.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutingportmappingsbydestinationpaginator)
        """


if TYPE_CHECKING:
    _ListCustomRoutingPortMappingsPaginatorBase = AioPaginator[
        ListCustomRoutingPortMappingsResponseTypeDef
    ]
else:
    _ListCustomRoutingPortMappingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomRoutingPortMappingsPaginator(_ListCustomRoutingPortMappingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingPortMappings.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutingportmappingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomRoutingPortMappingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomRoutingPortMappingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListCustomRoutingPortMappings.html#GlobalAccelerator.Paginator.ListCustomRoutingPortMappings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listcustomroutingportmappingspaginator)
        """


if TYPE_CHECKING:
    _ListEndpointGroupsPaginatorBase = AioPaginator[ListEndpointGroupsResponseTypeDef]
else:
    _ListEndpointGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEndpointGroupsPaginator(_ListEndpointGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListEndpointGroups.html#GlobalAccelerator.Paginator.ListEndpointGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listendpointgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEndpointGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEndpointGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListEndpointGroups.html#GlobalAccelerator.Paginator.ListEndpointGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listendpointgroupspaginator)
        """


if TYPE_CHECKING:
    _ListListenersPaginatorBase = AioPaginator[ListListenersResponseTypeDef]
else:
    _ListListenersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListListenersPaginator(_ListListenersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListListeners.html#GlobalAccelerator.Paginator.ListListeners)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listlistenerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListListenersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/paginator/ListListeners.html#GlobalAccelerator.Paginator.ListListeners.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/paginators/#listlistenerspaginator)
        """
