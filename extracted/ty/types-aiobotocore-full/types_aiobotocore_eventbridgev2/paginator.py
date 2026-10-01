"""
Type annotations for eventbridgev2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_eventbridgev2.client import EventBridgeV2Client
    from types_aiobotocore_eventbridgev2.paginator import (
        ListEventBusesPaginator,
        ListEventSourcesPaginator,
        ListResourcePoliciesPaginator,
        ListSubscribersPaginator,
    )

    session = get_session()
    with session.create_client("eventbridgev2") as client:
        client: EventBridgeV2Client

        list_event_buses_paginator: ListEventBusesPaginator = client.get_paginator("list_event_buses")
        list_event_sources_paginator: ListEventSourcesPaginator = client.get_paginator("list_event_sources")
        list_resource_policies_paginator: ListResourcePoliciesPaginator = client.get_paginator("list_resource_policies")
        list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListEventBusesRequestPaginateTypeDef,
    ListEventBusesResponseTypeDef,
    ListEventSourcesRequestPaginateTypeDef,
    ListEventSourcesResponseTypeDef,
    ListResourcePoliciesRequestPaginateTypeDef,
    ListResourcePoliciesResponseTypeDef,
    ListSubscribersRequestPaginateTypeDef,
    ListSubscribersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListEventBusesPaginator",
    "ListEventSourcesPaginator",
    "ListResourcePoliciesPaginator",
    "ListSubscribersPaginator",
)


if TYPE_CHECKING:
    _ListEventBusesPaginatorBase = AioPaginator[ListEventBusesResponseTypeDef]
else:
    _ListEventBusesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventBusesPaginator(_ListEventBusesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListEventBuses.html#EventBridgeV2.Paginator.ListEventBuses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/paginators/#listeventbusespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventBusesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventBusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListEventBuses.html#EventBridgeV2.Paginator.ListEventBuses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/paginators/#listeventbusespaginator)
        """


if TYPE_CHECKING:
    _ListEventSourcesPaginatorBase = AioPaginator[ListEventSourcesResponseTypeDef]
else:
    _ListEventSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventSourcesPaginator(_ListEventSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListEventSources.html#EventBridgeV2.Paginator.ListEventSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/paginators/#listeventsourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListEventSources.html#EventBridgeV2.Paginator.ListEventSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/paginators/#listeventsourcespaginator)
        """


if TYPE_CHECKING:
    _ListResourcePoliciesPaginatorBase = AioPaginator[ListResourcePoliciesResponseTypeDef]
else:
    _ListResourcePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourcePoliciesPaginator(_ListResourcePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListResourcePolicies.html#EventBridgeV2.Paginator.ListResourcePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/paginators/#listresourcepoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListResourcePolicies.html#EventBridgeV2.Paginator.ListResourcePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/paginators/#listresourcepoliciespaginator)
        """


if TYPE_CHECKING:
    _ListSubscribersPaginatorBase = AioPaginator[ListSubscribersResponseTypeDef]
else:
    _ListSubscribersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSubscribersPaginator(_ListSubscribersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListSubscribers.html#EventBridgeV2.Paginator.ListSubscribers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/paginators/#listsubscriberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscribersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSubscribersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListSubscribers.html#EventBridgeV2.Paginator.ListSubscribers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/paginators/#listsubscriberspaginator)
        """
