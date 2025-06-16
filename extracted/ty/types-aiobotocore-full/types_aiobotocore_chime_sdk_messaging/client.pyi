"""
Type annotations for chime-sdk-messaging service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_messaging.client import ChimeSDKMessagingClient

    session = get_session()
    async with session.create_client("chime-sdk-messaging") as client:
        client: ChimeSDKMessagingClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    AssociateChannelFlowRequestTypeDef,
    BatchCreateChannelMembershipRequestTypeDef,
    BatchCreateChannelMembershipResponseTypeDef,
    ChannelFlowCallbackRequestTypeDef,
    ChannelFlowCallbackResponseTypeDef,
    CreateChannelBanRequestTypeDef,
    CreateChannelBanResponseTypeDef,
    CreateChannelFlowRequestTypeDef,
    CreateChannelFlowResponseTypeDef,
    CreateChannelMembershipRequestTypeDef,
    CreateChannelMembershipResponseTypeDef,
    CreateChannelModeratorRequestTypeDef,
    CreateChannelModeratorResponseTypeDef,
    CreateChannelRequestTypeDef,
    CreateChannelResponseTypeDef,
    DeleteChannelBanRequestTypeDef,
    DeleteChannelFlowRequestTypeDef,
    DeleteChannelMembershipRequestTypeDef,
    DeleteChannelMessageRequestTypeDef,
    DeleteChannelModeratorRequestTypeDef,
    DeleteChannelRequestTypeDef,
    DeleteMessagingStreamingConfigurationsRequestTypeDef,
    DescribeChannelBanRequestTypeDef,
    DescribeChannelBanResponseTypeDef,
    DescribeChannelFlowRequestTypeDef,
    DescribeChannelFlowResponseTypeDef,
    DescribeChannelMembershipForAppInstanceUserRequestTypeDef,
    DescribeChannelMembershipForAppInstanceUserResponseTypeDef,
    DescribeChannelMembershipRequestTypeDef,
    DescribeChannelMembershipResponseTypeDef,
    DescribeChannelModeratedByAppInstanceUserRequestTypeDef,
    DescribeChannelModeratedByAppInstanceUserResponseTypeDef,
    DescribeChannelModeratorRequestTypeDef,
    DescribeChannelModeratorResponseTypeDef,
    DescribeChannelRequestTypeDef,
    DescribeChannelResponseTypeDef,
    DisassociateChannelFlowRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetChannelMembershipPreferencesRequestTypeDef,
    GetChannelMembershipPreferencesResponseTypeDef,
    GetChannelMessageRequestTypeDef,
    GetChannelMessageResponseTypeDef,
    GetChannelMessageStatusRequestTypeDef,
    GetChannelMessageStatusResponseTypeDef,
    GetMessagingSessionEndpointResponseTypeDef,
    GetMessagingStreamingConfigurationsRequestTypeDef,
    GetMessagingStreamingConfigurationsResponseTypeDef,
    ListChannelBansRequestTypeDef,
    ListChannelBansResponseTypeDef,
    ListChannelFlowsRequestTypeDef,
    ListChannelFlowsResponseTypeDef,
    ListChannelMembershipsForAppInstanceUserRequestTypeDef,
    ListChannelMembershipsForAppInstanceUserResponseTypeDef,
    ListChannelMembershipsRequestTypeDef,
    ListChannelMembershipsResponseTypeDef,
    ListChannelMessagesRequestTypeDef,
    ListChannelMessagesResponseTypeDef,
    ListChannelModeratorsRequestTypeDef,
    ListChannelModeratorsResponseTypeDef,
    ListChannelsAssociatedWithChannelFlowRequestTypeDef,
    ListChannelsAssociatedWithChannelFlowResponseTypeDef,
    ListChannelsModeratedByAppInstanceUserRequestTypeDef,
    ListChannelsModeratedByAppInstanceUserResponseTypeDef,
    ListChannelsRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListSubChannelsRequestTypeDef,
    ListSubChannelsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutChannelExpirationSettingsRequestTypeDef,
    PutChannelExpirationSettingsResponseTypeDef,
    PutChannelMembershipPreferencesRequestTypeDef,
    PutChannelMembershipPreferencesResponseTypeDef,
    PutMessagingStreamingConfigurationsRequestTypeDef,
    PutMessagingStreamingConfigurationsResponseTypeDef,
    RedactChannelMessageRequestTypeDef,
    RedactChannelMessageResponseTypeDef,
    SearchChannelsRequestTypeDef,
    SearchChannelsResponseTypeDef,
    SendChannelMessageRequestTypeDef,
    SendChannelMessageResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateChannelFlowRequestTypeDef,
    UpdateChannelFlowResponseTypeDef,
    UpdateChannelMessageRequestTypeDef,
    UpdateChannelMessageResponseTypeDef,
    UpdateChannelReadMarkerRequestTypeDef,
    UpdateChannelReadMarkerResponseTypeDef,
    UpdateChannelRequestTypeDef,
    UpdateChannelResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("ChimeSDKMessagingClient",)

class Exceptions(BaseClientExceptions):
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]

class ChimeSDKMessagingClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging.html#ChimeSDKMessaging.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKMessagingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging.html#ChimeSDKMessaging.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#generate_presigned_url)
        """

    async def associate_channel_flow(
        self, **kwargs: Unpack[AssociateChannelFlowRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a channel flow with a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/associate_channel_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#associate_channel_flow)
        """

    async def batch_create_channel_membership(
        self, **kwargs: Unpack[BatchCreateChannelMembershipRequestTypeDef]
    ) -> BatchCreateChannelMembershipResponseTypeDef:
        """
        Adds a specified number of users and bots to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/batch_create_channel_membership.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#batch_create_channel_membership)
        """

    async def channel_flow_callback(
        self, **kwargs: Unpack[ChannelFlowCallbackRequestTypeDef]
    ) -> ChannelFlowCallbackResponseTypeDef:
        """
        Calls back Amazon Chime SDK messaging with a processing response message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/channel_flow_callback.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#channel_flow_callback)
        """

    async def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a channel to which you can add users and send messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#create_channel)
        """

    async def create_channel_ban(
        self, **kwargs: Unpack[CreateChannelBanRequestTypeDef]
    ) -> CreateChannelBanResponseTypeDef:
        """
        Permanently bans a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel_ban.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#create_channel_ban)
        """

    async def create_channel_flow(
        self, **kwargs: Unpack[CreateChannelFlowRequestTypeDef]
    ) -> CreateChannelFlowResponseTypeDef:
        """
        Creates a channel flow, a container for processors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#create_channel_flow)
        """

    async def create_channel_membership(
        self, **kwargs: Unpack[CreateChannelMembershipRequestTypeDef]
    ) -> CreateChannelMembershipResponseTypeDef:
        """
        Adds a member to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel_membership.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#create_channel_membership)
        """

    async def create_channel_moderator(
        self, **kwargs: Unpack[CreateChannelModeratorRequestTypeDef]
    ) -> CreateChannelModeratorResponseTypeDef:
        """
        Creates a new <code>ChannelModerator</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/create_channel_moderator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#create_channel_moderator)
        """

    async def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Immediately makes a channel and its memberships inaccessible and marks them for
        deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#delete_channel)
        """

    async def delete_channel_ban(
        self, **kwargs: Unpack[DeleteChannelBanRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a member from a channel's ban list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_ban.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#delete_channel_ban)
        """

    async def delete_channel_flow(
        self, **kwargs: Unpack[DeleteChannelFlowRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel flow, an irreversible process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#delete_channel_flow)
        """

    async def delete_channel_membership(
        self, **kwargs: Unpack[DeleteChannelMembershipRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_membership.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#delete_channel_membership)
        """

    async def delete_channel_message(
        self, **kwargs: Unpack[DeleteChannelMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#delete_channel_message)
        """

    async def delete_channel_moderator(
        self, **kwargs: Unpack[DeleteChannelModeratorRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a channel moderator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_channel_moderator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#delete_channel_moderator)
        """

    async def delete_messaging_streaming_configurations(
        self, **kwargs: Unpack[DeleteMessagingStreamingConfigurationsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the streaming configurations for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/delete_messaging_streaming_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#delete_messaging_streaming_configurations)
        """

    async def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Returns the full details of a channel in an Amazon Chime
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#describe_channel)
        """

    async def describe_channel_ban(
        self, **kwargs: Unpack[DescribeChannelBanRequestTypeDef]
    ) -> DescribeChannelBanResponseTypeDef:
        """
        Returns the full details of a channel ban.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_ban.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#describe_channel_ban)
        """

    async def describe_channel_flow(
        self, **kwargs: Unpack[DescribeChannelFlowRequestTypeDef]
    ) -> DescribeChannelFlowResponseTypeDef:
        """
        Returns the full details of a channel flow in an Amazon Chime
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#describe_channel_flow)
        """

    async def describe_channel_membership(
        self, **kwargs: Unpack[DescribeChannelMembershipRequestTypeDef]
    ) -> DescribeChannelMembershipResponseTypeDef:
        """
        Returns the full details of a user's channel membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_membership.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#describe_channel_membership)
        """

    async def describe_channel_membership_for_app_instance_user(
        self, **kwargs: Unpack[DescribeChannelMembershipForAppInstanceUserRequestTypeDef]
    ) -> DescribeChannelMembershipForAppInstanceUserResponseTypeDef:
        """
        Returns the details of a channel based on the membership of the specified
        <code>AppInstanceUser</code> or <code>AppInstanceBot</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_membership_for_app_instance_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#describe_channel_membership_for_app_instance_user)
        """

    async def describe_channel_moderated_by_app_instance_user(
        self, **kwargs: Unpack[DescribeChannelModeratedByAppInstanceUserRequestTypeDef]
    ) -> DescribeChannelModeratedByAppInstanceUserResponseTypeDef:
        """
        Returns the full details of a channel moderated by the specified
        <code>AppInstanceUser</code> or <code>AppInstanceBot</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_moderated_by_app_instance_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#describe_channel_moderated_by_app_instance_user)
        """

    async def describe_channel_moderator(
        self, **kwargs: Unpack[DescribeChannelModeratorRequestTypeDef]
    ) -> DescribeChannelModeratorResponseTypeDef:
        """
        Returns the full details of a single ChannelModerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/describe_channel_moderator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#describe_channel_moderator)
        """

    async def disassociate_channel_flow(
        self, **kwargs: Unpack[DisassociateChannelFlowRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a channel flow from all its channels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/disassociate_channel_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#disassociate_channel_flow)
        """

    async def get_channel_membership_preferences(
        self, **kwargs: Unpack[GetChannelMembershipPreferencesRequestTypeDef]
    ) -> GetChannelMembershipPreferencesResponseTypeDef:
        """
        Gets the membership preferences of an <code>AppInstanceUser</code> or
        <code>AppInstanceBot</code> for the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_channel_membership_preferences.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#get_channel_membership_preferences)
        """

    async def get_channel_message(
        self, **kwargs: Unpack[GetChannelMessageRequestTypeDef]
    ) -> GetChannelMessageResponseTypeDef:
        """
        Gets the full details of a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_channel_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#get_channel_message)
        """

    async def get_channel_message_status(
        self, **kwargs: Unpack[GetChannelMessageStatusRequestTypeDef]
    ) -> GetChannelMessageStatusResponseTypeDef:
        """
        Gets message status for a specified <code>messageId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_channel_message_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#get_channel_message_status)
        """

    async def get_messaging_session_endpoint(self) -> GetMessagingSessionEndpointResponseTypeDef:
        """
        The details of the endpoint for the messaging session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_messaging_session_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#get_messaging_session_endpoint)
        """

    async def get_messaging_streaming_configurations(
        self, **kwargs: Unpack[GetMessagingStreamingConfigurationsRequestTypeDef]
    ) -> GetMessagingStreamingConfigurationsResponseTypeDef:
        """
        Retrieves the data streaming configuration for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/get_messaging_streaming_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#get_messaging_streaming_configurations)
        """

    async def list_channel_bans(
        self, **kwargs: Unpack[ListChannelBansRequestTypeDef]
    ) -> ListChannelBansResponseTypeDef:
        """
        Lists all the users and bots banned from a particular channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_bans.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_channel_bans)
        """

    async def list_channel_flows(
        self, **kwargs: Unpack[ListChannelFlowsRequestTypeDef]
    ) -> ListChannelFlowsResponseTypeDef:
        """
        Returns a paginated lists of all the channel flows created under a single Chime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_flows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_channel_flows)
        """

    async def list_channel_memberships(
        self, **kwargs: Unpack[ListChannelMembershipsRequestTypeDef]
    ) -> ListChannelMembershipsResponseTypeDef:
        """
        Lists all channel memberships in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_memberships.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_channel_memberships)
        """

    async def list_channel_memberships_for_app_instance_user(
        self, **kwargs: Unpack[ListChannelMembershipsForAppInstanceUserRequestTypeDef]
    ) -> ListChannelMembershipsForAppInstanceUserResponseTypeDef:
        """
        Lists all channels that an <code>AppInstanceUser</code> or
        <code>AppInstanceBot</code> is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_memberships_for_app_instance_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_channel_memberships_for_app_instance_user)
        """

    async def list_channel_messages(
        self, **kwargs: Unpack[ListChannelMessagesRequestTypeDef]
    ) -> ListChannelMessagesResponseTypeDef:
        """
        List all the messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_messages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_channel_messages)
        """

    async def list_channel_moderators(
        self, **kwargs: Unpack[ListChannelModeratorsRequestTypeDef]
    ) -> ListChannelModeratorsResponseTypeDef:
        """
        Lists all the moderators for a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channel_moderators.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_channel_moderators)
        """

    async def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Lists all Channels created under a single Chime App as a paginated list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channels.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_channels)
        """

    async def list_channels_associated_with_channel_flow(
        self, **kwargs: Unpack[ListChannelsAssociatedWithChannelFlowRequestTypeDef]
    ) -> ListChannelsAssociatedWithChannelFlowResponseTypeDef:
        """
        Lists all channels associated with a specified channel flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channels_associated_with_channel_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_channels_associated_with_channel_flow)
        """

    async def list_channels_moderated_by_app_instance_user(
        self, **kwargs: Unpack[ListChannelsModeratedByAppInstanceUserRequestTypeDef]
    ) -> ListChannelsModeratedByAppInstanceUserResponseTypeDef:
        """
        A list of the channels moderated by an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_channels_moderated_by_app_instance_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_channels_moderated_by_app_instance_user)
        """

    async def list_sub_channels(
        self, **kwargs: Unpack[ListSubChannelsRequestTypeDef]
    ) -> ListSubChannelsResponseTypeDef:
        """
        Lists all the SubChannels in an elastic channel when given a channel ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_sub_channels.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_sub_channels)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK messaging resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#list_tags_for_resource)
        """

    async def put_channel_expiration_settings(
        self, **kwargs: Unpack[PutChannelExpirationSettingsRequestTypeDef]
    ) -> PutChannelExpirationSettingsResponseTypeDef:
        """
        Sets the number of days before the channel is automatically deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/put_channel_expiration_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#put_channel_expiration_settings)
        """

    async def put_channel_membership_preferences(
        self, **kwargs: Unpack[PutChannelMembershipPreferencesRequestTypeDef]
    ) -> PutChannelMembershipPreferencesResponseTypeDef:
        """
        Sets the membership preferences of an <code>AppInstanceUser</code> or
        <code>AppInstanceBot</code> for the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/put_channel_membership_preferences.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#put_channel_membership_preferences)
        """

    async def put_messaging_streaming_configurations(
        self, **kwargs: Unpack[PutMessagingStreamingConfigurationsRequestTypeDef]
    ) -> PutMessagingStreamingConfigurationsResponseTypeDef:
        """
        Sets the data streaming configuration for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/put_messaging_streaming_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#put_messaging_streaming_configurations)
        """

    async def redact_channel_message(
        self, **kwargs: Unpack[RedactChannelMessageRequestTypeDef]
    ) -> RedactChannelMessageResponseTypeDef:
        """
        Redacts message content, but not metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/redact_channel_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#redact_channel_message)
        """

    async def search_channels(
        self, **kwargs: Unpack[SearchChannelsRequestTypeDef]
    ) -> SearchChannelsResponseTypeDef:
        """
        Allows the <code>ChimeBearer</code> to search channels by channel members.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/search_channels.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#search_channels)
        """

    async def send_channel_message(
        self, **kwargs: Unpack[SendChannelMessageRequestTypeDef]
    ) -> SendChannelMessageResponseTypeDef:
        """
        Sends a message to a particular channel that the member is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/send_channel_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#send_channel_message)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies the specified tags to the specified Amazon Chime SDK messaging resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the specified Amazon Chime SDK messaging
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#untag_resource)
        """

    async def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Update a channel's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/update_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#update_channel)
        """

    async def update_channel_flow(
        self, **kwargs: Unpack[UpdateChannelFlowRequestTypeDef]
    ) -> UpdateChannelFlowResponseTypeDef:
        """
        Updates channel flow attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/update_channel_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#update_channel_flow)
        """

    async def update_channel_message(
        self, **kwargs: Unpack[UpdateChannelMessageRequestTypeDef]
    ) -> UpdateChannelMessageResponseTypeDef:
        """
        Updates the content of a message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/update_channel_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#update_channel_message)
        """

    async def update_channel_read_marker(
        self, **kwargs: Unpack[UpdateChannelReadMarkerRequestTypeDef]
    ) -> UpdateChannelReadMarkerResponseTypeDef:
        """
        The details of the time when a user last read messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging/client/update_channel_read_marker.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/#update_channel_read_marker)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging.html#ChimeSDKMessaging.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-messaging.html#ChimeSDKMessaging.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_messaging/client/)
        """
