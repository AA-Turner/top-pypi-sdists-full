"""
Type annotations for notifications service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_notifications.client import UserNotificationsClient

    session = get_session()
    async with session.create_client("notifications") as client:
        client: UserNotificationsClient
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
from .type_defs import (
    AssociateChannelRequestTypeDef,
    AssociateManagedNotificationAccountContactRequestTypeDef,
    AssociateManagedNotificationAdditionalChannelRequestTypeDef,
    CreateEventRuleRequestTypeDef,
    CreateEventRuleResponseTypeDef,
    CreateNotificationConfigurationRequestTypeDef,
    CreateNotificationConfigurationResponseTypeDef,
    DeleteEventRuleRequestTypeDef,
    DeleteNotificationConfigurationRequestTypeDef,
    DeregisterNotificationHubRequestTypeDef,
    DeregisterNotificationHubResponseTypeDef,
    DisassociateChannelRequestTypeDef,
    DisassociateManagedNotificationAccountContactRequestTypeDef,
    DisassociateManagedNotificationAdditionalChannelRequestTypeDef,
    GetEventRuleRequestTypeDef,
    GetEventRuleResponseTypeDef,
    GetManagedNotificationChildEventRequestTypeDef,
    GetManagedNotificationChildEventResponseTypeDef,
    GetManagedNotificationConfigurationRequestTypeDef,
    GetManagedNotificationConfigurationResponseTypeDef,
    GetManagedNotificationEventRequestTypeDef,
    GetManagedNotificationEventResponseTypeDef,
    GetNotificationConfigurationRequestTypeDef,
    GetNotificationConfigurationResponseTypeDef,
    GetNotificationEventRequestTypeDef,
    GetNotificationEventResponseTypeDef,
    GetNotificationsAccessForOrganizationResponseTypeDef,
    ListChannelsRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListEventRulesRequestTypeDef,
    ListEventRulesResponseTypeDef,
    ListManagedNotificationChannelAssociationsRequestTypeDef,
    ListManagedNotificationChannelAssociationsResponseTypeDef,
    ListManagedNotificationChildEventsRequestTypeDef,
    ListManagedNotificationChildEventsResponseTypeDef,
    ListManagedNotificationConfigurationsRequestTypeDef,
    ListManagedNotificationConfigurationsResponseTypeDef,
    ListManagedNotificationEventsRequestTypeDef,
    ListManagedNotificationEventsResponseTypeDef,
    ListNotificationConfigurationsRequestTypeDef,
    ListNotificationConfigurationsResponseTypeDef,
    ListNotificationEventsRequestTypeDef,
    ListNotificationEventsResponseTypeDef,
    ListNotificationHubsRequestTypeDef,
    ListNotificationHubsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterNotificationHubRequestTypeDef,
    RegisterNotificationHubResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateEventRuleRequestTypeDef,
    UpdateEventRuleResponseTypeDef,
    UpdateNotificationConfigurationRequestTypeDef,
    UpdateNotificationConfigurationResponseTypeDef,
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


__all__ = ("UserNotificationsClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class UserNotificationsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        UserNotificationsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#generate_presigned_url)
        """

    async def associate_channel(
        self, **kwargs: Unpack[AssociateChannelRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a delivery <a
        href="https://docs.aws.amazon.com/notifications/latest/userguide/managing-delivery-channels.html">Channel</a>
        with a particular <code>NotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/associate_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#associate_channel)
        """

    async def associate_managed_notification_account_contact(
        self, **kwargs: Unpack[AssociateManagedNotificationAccountContactRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates an Account Contact with a particular
        <code>ManagedNotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/associate_managed_notification_account_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#associate_managed_notification_account_contact)
        """

    async def associate_managed_notification_additional_channel(
        self, **kwargs: Unpack[AssociateManagedNotificationAdditionalChannelRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates an additional Channel with a particular
        <code>ManagedNotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/associate_managed_notification_additional_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#associate_managed_notification_additional_channel)
        """

    async def create_event_rule(
        self, **kwargs: Unpack[CreateEventRuleRequestTypeDef]
    ) -> CreateEventRuleResponseTypeDef:
        """
        Creates an <a
        href="https://docs.aws.amazon.com/notifications/latest/userguide/glossary.html">
        <code>EventRule</code> </a> that is associated with a specified
        <code>NotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/create_event_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#create_event_rule)
        """

    async def create_notification_configuration(
        self, **kwargs: Unpack[CreateNotificationConfigurationRequestTypeDef]
    ) -> CreateNotificationConfigurationResponseTypeDef:
        """
        Creates a new <code>NotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/create_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#create_notification_configuration)
        """

    async def delete_event_rule(
        self, **kwargs: Unpack[DeleteEventRuleRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an <code>EventRule</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/delete_event_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#delete_event_rule)
        """

    async def delete_notification_configuration(
        self, **kwargs: Unpack[DeleteNotificationConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a <code>NotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/delete_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#delete_notification_configuration)
        """

    async def deregister_notification_hub(
        self, **kwargs: Unpack[DeregisterNotificationHubRequestTypeDef]
    ) -> DeregisterNotificationHubResponseTypeDef:
        """
        Deregisters a <code>NotificationConfiguration</code> in the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/deregister_notification_hub.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#deregister_notification_hub)
        """

    async def disable_notifications_access_for_organization(self) -> Dict[str, Any]:
        """
        Disables service trust between User Notifications and Amazon Web Services
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/disable_notifications_access_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#disable_notifications_access_for_organization)
        """

    async def disassociate_channel(
        self, **kwargs: Unpack[DisassociateChannelRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a Channel from a specified <code>NotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/disassociate_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#disassociate_channel)
        """

    async def disassociate_managed_notification_account_contact(
        self, **kwargs: Unpack[DisassociateManagedNotificationAccountContactRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates an Account Contact with a particular
        <code>ManagedNotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/disassociate_managed_notification_account_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#disassociate_managed_notification_account_contact)
        """

    async def disassociate_managed_notification_additional_channel(
        self, **kwargs: Unpack[DisassociateManagedNotificationAdditionalChannelRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates an additional Channel from a particular
        <code>ManagedNotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/disassociate_managed_notification_additional_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#disassociate_managed_notification_additional_channel)
        """

    async def enable_notifications_access_for_organization(self) -> Dict[str, Any]:
        """
        Enables service trust between User Notifications and Amazon Web Services
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/enable_notifications_access_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#enable_notifications_access_for_organization)
        """

    async def get_event_rule(
        self, **kwargs: Unpack[GetEventRuleRequestTypeDef]
    ) -> GetEventRuleResponseTypeDef:
        """
        Returns a specified <code>EventRule</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_event_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_event_rule)
        """

    async def get_managed_notification_child_event(
        self, **kwargs: Unpack[GetManagedNotificationChildEventRequestTypeDef]
    ) -> GetManagedNotificationChildEventResponseTypeDef:
        """
        Returns the child event of a specific given
        <code>ManagedNotificationEvent</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_managed_notification_child_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_managed_notification_child_event)
        """

    async def get_managed_notification_configuration(
        self, **kwargs: Unpack[GetManagedNotificationConfigurationRequestTypeDef]
    ) -> GetManagedNotificationConfigurationResponseTypeDef:
        """
        Returns a specified <code>ManagedNotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_managed_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_managed_notification_configuration)
        """

    async def get_managed_notification_event(
        self, **kwargs: Unpack[GetManagedNotificationEventRequestTypeDef]
    ) -> GetManagedNotificationEventResponseTypeDef:
        """
        Returns a specified <code>ManagedNotificationEvent</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_managed_notification_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_managed_notification_event)
        """

    async def get_notification_configuration(
        self, **kwargs: Unpack[GetNotificationConfigurationRequestTypeDef]
    ) -> GetNotificationConfigurationResponseTypeDef:
        """
        Returns a specified <code>NotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_notification_configuration)
        """

    async def get_notification_event(
        self, **kwargs: Unpack[GetNotificationEventRequestTypeDef]
    ) -> GetNotificationEventResponseTypeDef:
        """
        Returns a specified <code>NotificationEvent</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_notification_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_notification_event)
        """

    async def get_notifications_access_for_organization(
        self,
    ) -> GetNotificationsAccessForOrganizationResponseTypeDef:
        """
        Returns the AccessStatus of Service Trust Enablement for User Notifications and
        Amazon Web Services Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_notifications_access_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_notifications_access_for_organization)
        """

    async def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Returns a list of Channels for a <code>NotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_channels.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_channels)
        """

    async def list_event_rules(
        self, **kwargs: Unpack[ListEventRulesRequestTypeDef]
    ) -> ListEventRulesResponseTypeDef:
        """
        Returns a list of <code>EventRules</code> according to specified filters, in
        reverse chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_event_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_event_rules)
        """

    async def list_managed_notification_channel_associations(
        self, **kwargs: Unpack[ListManagedNotificationChannelAssociationsRequestTypeDef]
    ) -> ListManagedNotificationChannelAssociationsResponseTypeDef:
        """
        Returns a list of Account contacts and Channels associated with a
        <code>ManagedNotificationConfiguration</code>, in paginated format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_managed_notification_channel_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_managed_notification_channel_associations)
        """

    async def list_managed_notification_child_events(
        self, **kwargs: Unpack[ListManagedNotificationChildEventsRequestTypeDef]
    ) -> ListManagedNotificationChildEventsResponseTypeDef:
        """
        Returns a list of <code>ManagedNotificationChildEvents</code> for a specified
        aggregate <code>ManagedNotificationEvent</code>, ordered by creation time in
        reverse chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_managed_notification_child_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_managed_notification_child_events)
        """

    async def list_managed_notification_configurations(
        self, **kwargs: Unpack[ListManagedNotificationConfigurationsRequestTypeDef]
    ) -> ListManagedNotificationConfigurationsResponseTypeDef:
        """
        Returns a list of Managed Notification Configurations according to specified
        filters, ordered by creation time in reverse chronological order (newest
        first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_managed_notification_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_managed_notification_configurations)
        """

    async def list_managed_notification_events(
        self, **kwargs: Unpack[ListManagedNotificationEventsRequestTypeDef]
    ) -> ListManagedNotificationEventsResponseTypeDef:
        """
        Returns a list of Managed Notification Events according to specified filters,
        ordered by creation time in reverse chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_managed_notification_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_managed_notification_events)
        """

    async def list_notification_configurations(
        self, **kwargs: Unpack[ListNotificationConfigurationsRequestTypeDef]
    ) -> ListNotificationConfigurationsResponseTypeDef:
        """
        Returns a list of abbreviated <code>NotificationConfigurations</code> according
        to specified filters, in reverse chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_notification_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_notification_configurations)
        """

    async def list_notification_events(
        self, **kwargs: Unpack[ListNotificationEventsRequestTypeDef]
    ) -> ListNotificationEventsResponseTypeDef:
        """
        Returns a list of <code>NotificationEvents</code> according to specified
        filters, in reverse chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_notification_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_notification_events)
        """

    async def list_notification_hubs(
        self, **kwargs: Unpack[ListNotificationHubsRequestTypeDef]
    ) -> ListNotificationHubsResponseTypeDef:
        """
        Returns a list of <code>NotificationHubs</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_notification_hubs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_notification_hubs)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_tags_for_resource)
        """

    async def register_notification_hub(
        self, **kwargs: Unpack[RegisterNotificationHubRequestTypeDef]
    ) -> RegisterNotificationHubResponseTypeDef:
        """
        Registers a <code>NotificationConfiguration</code> in the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/register_notification_hub.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#register_notification_hub)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags the resource with a tag key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Untags a resource with a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#untag_resource)
        """

    async def update_event_rule(
        self, **kwargs: Unpack[UpdateEventRuleRequestTypeDef]
    ) -> UpdateEventRuleResponseTypeDef:
        """
        Updates an existing <code>EventRule</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/update_event_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#update_event_rule)
        """

    async def update_notification_configuration(
        self, **kwargs: Unpack[UpdateNotificationConfigurationRequestTypeDef]
    ) -> UpdateNotificationConfigurationResponseTypeDef:
        """
        Updates a <code>NotificationConfiguration</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/update_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#update_notification_configuration)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_channels"]
    ) -> ListChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_event_rules"]
    ) -> ListEventRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_notification_channel_associations"]
    ) -> ListManagedNotificationChannelAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_notification_child_events"]
    ) -> ListManagedNotificationChildEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_notification_configurations"]
    ) -> ListManagedNotificationConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_notification_events"]
    ) -> ListManagedNotificationEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_notification_configurations"]
    ) -> ListNotificationConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_notification_events"]
    ) -> ListNotificationEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_notification_hubs"]
    ) -> ListNotificationHubsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/)
        """
