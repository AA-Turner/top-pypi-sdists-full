"""
Type annotations for notifications service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_notifications.client import UserNotificationsClient
    from types_aiobotocore_notifications.paginator import (
        ListChannelsPaginator,
        ListEventRulesPaginator,
        ListManagedNotificationChannelAssociationsPaginator,
        ListManagedNotificationChildEventsPaginator,
        ListManagedNotificationConfigurationsPaginator,
        ListManagedNotificationEventsPaginator,
        ListNotificationConfigurationsPaginator,
        ListNotificationEventsPaginator,
        ListNotificationHubsPaginator,
    )

    session = get_session()
    with session.create_client("notifications") as client:
        client: UserNotificationsClient

        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_event_rules_paginator: ListEventRulesPaginator = client.get_paginator("list_event_rules")
        list_managed_notification_channel_associations_paginator: ListManagedNotificationChannelAssociationsPaginator = client.get_paginator("list_managed_notification_channel_associations")
        list_managed_notification_child_events_paginator: ListManagedNotificationChildEventsPaginator = client.get_paginator("list_managed_notification_child_events")
        list_managed_notification_configurations_paginator: ListManagedNotificationConfigurationsPaginator = client.get_paginator("list_managed_notification_configurations")
        list_managed_notification_events_paginator: ListManagedNotificationEventsPaginator = client.get_paginator("list_managed_notification_events")
        list_notification_configurations_paginator: ListNotificationConfigurationsPaginator = client.get_paginator("list_notification_configurations")
        list_notification_events_paginator: ListNotificationEventsPaginator = client.get_paginator("list_notification_events")
        list_notification_hubs_paginator: ListNotificationHubsPaginator = client.get_paginator("list_notification_hubs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChannelsRequestPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListEventRulesRequestPaginateTypeDef,
    ListEventRulesResponseTypeDef,
    ListManagedNotificationChannelAssociationsRequestPaginateTypeDef,
    ListManagedNotificationChannelAssociationsResponseTypeDef,
    ListManagedNotificationChildEventsRequestPaginateTypeDef,
    ListManagedNotificationChildEventsResponseTypeDef,
    ListManagedNotificationConfigurationsRequestPaginateTypeDef,
    ListManagedNotificationConfigurationsResponseTypeDef,
    ListManagedNotificationEventsRequestPaginateTypeDef,
    ListManagedNotificationEventsResponseTypeDef,
    ListNotificationConfigurationsRequestPaginateTypeDef,
    ListNotificationConfigurationsResponseTypeDef,
    ListNotificationEventsRequestPaginateTypeDef,
    ListNotificationEventsResponseTypeDef,
    ListNotificationHubsRequestPaginateTypeDef,
    ListNotificationHubsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChannelsPaginator",
    "ListEventRulesPaginator",
    "ListManagedNotificationChannelAssociationsPaginator",
    "ListManagedNotificationChildEventsPaginator",
    "ListManagedNotificationConfigurationsPaginator",
    "ListManagedNotificationEventsPaginator",
    "ListNotificationConfigurationsPaginator",
    "ListNotificationEventsPaginator",
    "ListNotificationHubsPaginator",
)


if TYPE_CHECKING:
    _ListChannelsPaginatorBase = AioPaginator[ListChannelsResponseTypeDef]
else:
    _ListChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChannelsPaginator(_ListChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListChannels.html#UserNotifications.Paginator.ListChannels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listchannelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListChannels.html#UserNotifications.Paginator.ListChannels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listchannelspaginator)
        """


if TYPE_CHECKING:
    _ListEventRulesPaginatorBase = AioPaginator[ListEventRulesResponseTypeDef]
else:
    _ListEventRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventRulesPaginator(_ListEventRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListEventRules.html#UserNotifications.Paginator.ListEventRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listeventrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListEventRules.html#UserNotifications.Paginator.ListEventRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listeventrulespaginator)
        """


if TYPE_CHECKING:
    _ListManagedNotificationChannelAssociationsPaginatorBase = AioPaginator[
        ListManagedNotificationChannelAssociationsResponseTypeDef
    ]
else:
    _ListManagedNotificationChannelAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListManagedNotificationChannelAssociationsPaginator(
    _ListManagedNotificationChannelAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListManagedNotificationChannelAssociations.html#UserNotifications.Paginator.ListManagedNotificationChannelAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listmanagednotificationchannelassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedNotificationChannelAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedNotificationChannelAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListManagedNotificationChannelAssociations.html#UserNotifications.Paginator.ListManagedNotificationChannelAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listmanagednotificationchannelassociationspaginator)
        """


if TYPE_CHECKING:
    _ListManagedNotificationChildEventsPaginatorBase = AioPaginator[
        ListManagedNotificationChildEventsResponseTypeDef
    ]
else:
    _ListManagedNotificationChildEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListManagedNotificationChildEventsPaginator(_ListManagedNotificationChildEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListManagedNotificationChildEvents.html#UserNotifications.Paginator.ListManagedNotificationChildEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listmanagednotificationchildeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedNotificationChildEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedNotificationChildEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListManagedNotificationChildEvents.html#UserNotifications.Paginator.ListManagedNotificationChildEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listmanagednotificationchildeventspaginator)
        """


if TYPE_CHECKING:
    _ListManagedNotificationConfigurationsPaginatorBase = AioPaginator[
        ListManagedNotificationConfigurationsResponseTypeDef
    ]
else:
    _ListManagedNotificationConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListManagedNotificationConfigurationsPaginator(
    _ListManagedNotificationConfigurationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListManagedNotificationConfigurations.html#UserNotifications.Paginator.ListManagedNotificationConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listmanagednotificationconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedNotificationConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedNotificationConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListManagedNotificationConfigurations.html#UserNotifications.Paginator.ListManagedNotificationConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listmanagednotificationconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListManagedNotificationEventsPaginatorBase = AioPaginator[
        ListManagedNotificationEventsResponseTypeDef
    ]
else:
    _ListManagedNotificationEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListManagedNotificationEventsPaginator(_ListManagedNotificationEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListManagedNotificationEvents.html#UserNotifications.Paginator.ListManagedNotificationEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listmanagednotificationeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedNotificationEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedNotificationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListManagedNotificationEvents.html#UserNotifications.Paginator.ListManagedNotificationEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listmanagednotificationeventspaginator)
        """


if TYPE_CHECKING:
    _ListNotificationConfigurationsPaginatorBase = AioPaginator[
        ListNotificationConfigurationsResponseTypeDef
    ]
else:
    _ListNotificationConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNotificationConfigurationsPaginator(_ListNotificationConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationConfigurations.html#UserNotifications.Paginator.ListNotificationConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationConfigurations.html#UserNotifications.Paginator.ListNotificationConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListNotificationEventsPaginatorBase = AioPaginator[ListNotificationEventsResponseTypeDef]
else:
    _ListNotificationEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNotificationEventsPaginator(_ListNotificationEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationEvents.html#UserNotifications.Paginator.ListNotificationEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationEvents.html#UserNotifications.Paginator.ListNotificationEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationeventspaginator)
        """


if TYPE_CHECKING:
    _ListNotificationHubsPaginatorBase = AioPaginator[ListNotificationHubsResponseTypeDef]
else:
    _ListNotificationHubsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNotificationHubsPaginator(_ListNotificationHubsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationHubs.html#UserNotifications.Paginator.ListNotificationHubs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationhubspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationHubsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationHubsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationHubs.html#UserNotifications.Paginator.ListNotificationHubs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationhubspaginator)
        """
