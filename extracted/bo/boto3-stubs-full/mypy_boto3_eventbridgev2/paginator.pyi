"""
Type annotations for eventbridgev2 service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_eventbridgev2.client import EventBridgeV2Client
    from mypy_boto3_eventbridgev2.paginator import (
        ListEventBusesPaginator,
        ListEventSourcesPaginator,
        ListResourcePoliciesPaginator,
        ListSubscribersPaginator,
    )

    session = Session()
    client: EventBridgeV2Client = session.client("eventbridgev2")

    list_event_buses_paginator: ListEventBusesPaginator = client.get_paginator("list_event_buses")
    list_event_sources_paginator: ListEventSourcesPaginator = client.get_paginator("list_event_sources")
    list_resource_policies_paginator: ListResourcePoliciesPaginator = client.get_paginator("list_resource_policies")
    list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListEventBusesPaginatorBase = Paginator[ListEventBusesResponseTypeDef]
else:
    _ListEventBusesPaginatorBase = Paginator  # type: ignore[assignment]

class ListEventBusesPaginator(_ListEventBusesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListEventBuses.html#EventBridgeV2.Paginator.ListEventBuses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/paginators/#listeventbusespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventBusesRequestPaginateTypeDef]
    ) -> PageIterator[ListEventBusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListEventBuses.html#EventBridgeV2.Paginator.ListEventBuses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/paginators/#listeventbusespaginator)
        """

if TYPE_CHECKING:
    _ListEventSourcesPaginatorBase = Paginator[ListEventSourcesResponseTypeDef]
else:
    _ListEventSourcesPaginatorBase = Paginator  # type: ignore[assignment]

class ListEventSourcesPaginator(_ListEventSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListEventSources.html#EventBridgeV2.Paginator.ListEventSources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/paginators/#listeventsourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventSourcesRequestPaginateTypeDef]
    ) -> PageIterator[ListEventSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListEventSources.html#EventBridgeV2.Paginator.ListEventSources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/paginators/#listeventsourcespaginator)
        """

if TYPE_CHECKING:
    _ListResourcePoliciesPaginatorBase = Paginator[ListResourcePoliciesResponseTypeDef]
else:
    _ListResourcePoliciesPaginatorBase = Paginator  # type: ignore[assignment]

class ListResourcePoliciesPaginator(_ListResourcePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListResourcePolicies.html#EventBridgeV2.Paginator.ListResourcePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/paginators/#listresourcepoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcePoliciesRequestPaginateTypeDef]
    ) -> PageIterator[ListResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListResourcePolicies.html#EventBridgeV2.Paginator.ListResourcePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/paginators/#listresourcepoliciespaginator)
        """

if TYPE_CHECKING:
    _ListSubscribersPaginatorBase = Paginator[ListSubscribersResponseTypeDef]
else:
    _ListSubscribersPaginatorBase = Paginator  # type: ignore[assignment]

class ListSubscribersPaginator(_ListSubscribersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListSubscribers.html#EventBridgeV2.Paginator.ListSubscribers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/paginators/#listsubscriberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscribersRequestPaginateTypeDef]
    ) -> PageIterator[ListSubscribersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/paginator/ListSubscribers.html#EventBridgeV2.Paginator.ListSubscribers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/paginators/#listsubscriberspaginator)
        """
