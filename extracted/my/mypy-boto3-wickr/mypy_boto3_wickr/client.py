"""
Type annotations for wickr service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_wickr.client import WickrAdminAPIClient

    session = Session()
    client: WickrAdminAPIClient = session.client("wickr")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListBlockedGuestUsersPaginator,
    ListBotsPaginator,
    ListDevicesForUserPaginator,
    ListGuestUsersPaginator,
    ListNetworksPaginator,
    ListSecurityGroupsPaginator,
    ListSecurityGroupUsersPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    BatchCreateUserRequestTypeDef,
    BatchCreateUserResponseTypeDef,
    BatchDeleteUserRequestTypeDef,
    BatchDeleteUserResponseTypeDef,
    BatchLookupUserUnameRequestTypeDef,
    BatchLookupUserUnameResponseTypeDef,
    BatchReinviteUserRequestTypeDef,
    BatchReinviteUserResponseTypeDef,
    BatchResetDevicesForUserRequestTypeDef,
    BatchResetDevicesForUserResponseTypeDef,
    BatchToggleUserSuspendStatusRequestTypeDef,
    BatchToggleUserSuspendStatusResponseTypeDef,
    CreateBotRequestTypeDef,
    CreateBotResponseTypeDef,
    CreateDataRetentionBotChallengeRequestTypeDef,
    CreateDataRetentionBotChallengeResponseTypeDef,
    CreateDataRetentionBotRequestTypeDef,
    CreateDataRetentionBotResponseTypeDef,
    CreateNetworkRequestTypeDef,
    CreateNetworkResponseTypeDef,
    CreateSecurityGroupRequestTypeDef,
    CreateSecurityGroupResponseTypeDef,
    DeleteBotRequestTypeDef,
    DeleteBotResponseTypeDef,
    DeleteDataRetentionBotRequestTypeDef,
    DeleteDataRetentionBotResponseTypeDef,
    DeleteNetworkRequestTypeDef,
    DeleteNetworkResponseTypeDef,
    DeleteSecurityGroupRequestTypeDef,
    DeleteSecurityGroupResponseTypeDef,
    GetBotRequestTypeDef,
    GetBotResponseTypeDef,
    GetBotsCountRequestTypeDef,
    GetBotsCountResponseTypeDef,
    GetDataRetentionBotRequestTypeDef,
    GetDataRetentionBotResponseTypeDef,
    GetGuestUserHistoryCountRequestTypeDef,
    GetGuestUserHistoryCountResponseTypeDef,
    GetNetworkRequestTypeDef,
    GetNetworkResponseTypeDef,
    GetNetworkSettingsRequestTypeDef,
    GetNetworkSettingsResponseTypeDef,
    GetOidcInfoRequestTypeDef,
    GetOidcInfoResponseTypeDef,
    GetSecurityGroupRequestTypeDef,
    GetSecurityGroupResponseTypeDef,
    GetUserRequestTypeDef,
    GetUserResponseTypeDef,
    GetUsersCountRequestTypeDef,
    GetUsersCountResponseTypeDef,
    ListBlockedGuestUsersRequestTypeDef,
    ListBlockedGuestUsersResponseTypeDef,
    ListBotsRequestTypeDef,
    ListBotsResponseTypeDef,
    ListDevicesForUserRequestTypeDef,
    ListDevicesForUserResponseTypeDef,
    ListGuestUsersRequestTypeDef,
    ListGuestUsersResponseTypeDef,
    ListNetworksRequestTypeDef,
    ListNetworksResponseTypeDef,
    ListSecurityGroupsRequestTypeDef,
    ListSecurityGroupsResponseTypeDef,
    ListSecurityGroupUsersRequestTypeDef,
    ListSecurityGroupUsersResponseTypeDef,
    ListUsersRequestTypeDef,
    ListUsersResponseTypeDef,
    RegisterOidcConfigRequestTypeDef,
    RegisterOidcConfigResponseTypeDef,
    RegisterOidcConfigTestRequestTypeDef,
    RegisterOidcConfigTestResponseTypeDef,
    UpdateBotRequestTypeDef,
    UpdateBotResponseTypeDef,
    UpdateDataRetentionRequestTypeDef,
    UpdateDataRetentionResponseTypeDef,
    UpdateGuestUserRequestTypeDef,
    UpdateGuestUserResponseTypeDef,
    UpdateNetworkRequestTypeDef,
    UpdateNetworkResponseTypeDef,
    UpdateNetworkSettingsRequestTypeDef,
    UpdateNetworkSettingsResponseTypeDef,
    UpdateSecurityGroupRequestTypeDef,
    UpdateSecurityGroupResponseTypeDef,
    UpdateUserRequestTypeDef,
    UpdateUserResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("WickrAdminAPIClient",)


class Exceptions(BaseClientExceptions):
    BadRequestError: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ForbiddenError: type[BotocoreClientError]
    InternalServerError: type[BotocoreClientError]
    RateLimitError: type[BotocoreClientError]
    ResourceNotFoundError: type[BotocoreClientError]
    UnauthorizedError: type[BotocoreClientError]
    ValidationError: type[BotocoreClientError]


class WickrAdminAPIClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr.html#WickrAdminAPI.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WickrAdminAPIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr.html#WickrAdminAPI.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#generate_presigned_url)
        """

    def batch_create_user(
        self, **kwargs: Unpack[BatchCreateUserRequestTypeDef]
    ) -> BatchCreateUserResponseTypeDef:
        """
        Creates multiple users in a specified Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/batch_create_user.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#batch_create_user)
        """

    def batch_delete_user(
        self, **kwargs: Unpack[BatchDeleteUserRequestTypeDef]
    ) -> BatchDeleteUserResponseTypeDef:
        """
        Deletes multiple users from a specified Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/batch_delete_user.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#batch_delete_user)
        """

    def batch_lookup_user_uname(
        self, **kwargs: Unpack[BatchLookupUserUnameRequestTypeDef]
    ) -> BatchLookupUserUnameResponseTypeDef:
        """
        Looks up multiple user usernames from their unique username hashes (unames).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/batch_lookup_user_uname.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#batch_lookup_user_uname)
        """

    def batch_reinvite_user(
        self, **kwargs: Unpack[BatchReinviteUserRequestTypeDef]
    ) -> BatchReinviteUserResponseTypeDef:
        """
        Resends invitation codes to multiple users who have pending invitations in a
        Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/batch_reinvite_user.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#batch_reinvite_user)
        """

    def batch_reset_devices_for_user(
        self, **kwargs: Unpack[BatchResetDevicesForUserRequestTypeDef]
    ) -> BatchResetDevicesForUserResponseTypeDef:
        """
        Resets multiple devices for a specific user in a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/batch_reset_devices_for_user.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#batch_reset_devices_for_user)
        """

    def batch_toggle_user_suspend_status(
        self, **kwargs: Unpack[BatchToggleUserSuspendStatusRequestTypeDef]
    ) -> BatchToggleUserSuspendStatusResponseTypeDef:
        """
        Suspends or unsuspends multiple users in a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/batch_toggle_user_suspend_status.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#batch_toggle_user_suspend_status)
        """

    def create_bot(self, **kwargs: Unpack[CreateBotRequestTypeDef]) -> CreateBotResponseTypeDef:
        """
        Creates a new bot in a specified Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/create_bot.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#create_bot)
        """

    def create_data_retention_bot(
        self, **kwargs: Unpack[CreateDataRetentionBotRequestTypeDef]
    ) -> CreateDataRetentionBotResponseTypeDef:
        """
        Creates a data retention bot in a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/create_data_retention_bot.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#create_data_retention_bot)
        """

    def create_data_retention_bot_challenge(
        self, **kwargs: Unpack[CreateDataRetentionBotChallengeRequestTypeDef]
    ) -> CreateDataRetentionBotChallengeResponseTypeDef:
        """
        Creates a new challenge password for the data retention bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/create_data_retention_bot_challenge.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#create_data_retention_bot_challenge)
        """

    def create_network(
        self, **kwargs: Unpack[CreateNetworkRequestTypeDef]
    ) -> CreateNetworkResponseTypeDef:
        """
        Creates a new Wickr network with specified access level and configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/create_network.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#create_network)
        """

    def create_security_group(
        self, **kwargs: Unpack[CreateSecurityGroupRequestTypeDef]
    ) -> CreateSecurityGroupResponseTypeDef:
        """
        Creates a new security group in a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/create_security_group.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#create_security_group)
        """

    def delete_bot(self, **kwargs: Unpack[DeleteBotRequestTypeDef]) -> DeleteBotResponseTypeDef:
        """
        Deletes a bot from a specified Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/delete_bot.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#delete_bot)
        """

    def delete_data_retention_bot(
        self, **kwargs: Unpack[DeleteDataRetentionBotRequestTypeDef]
    ) -> DeleteDataRetentionBotResponseTypeDef:
        """
        Deletes the data retention bot from a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/delete_data_retention_bot.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#delete_data_retention_bot)
        """

    def delete_network(
        self, **kwargs: Unpack[DeleteNetworkRequestTypeDef]
    ) -> DeleteNetworkResponseTypeDef:
        """
        Deletes a Wickr network and all its associated resources, including users,
        bots, security groups, and settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/delete_network.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#delete_network)
        """

    def delete_security_group(
        self, **kwargs: Unpack[DeleteSecurityGroupRequestTypeDef]
    ) -> DeleteSecurityGroupResponseTypeDef:
        """
        Deletes a security group from a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/delete_security_group.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#delete_security_group)
        """

    def get_bot(self, **kwargs: Unpack[GetBotRequestTypeDef]) -> GetBotResponseTypeDef:
        """
        Retrieves detailed information about a specific bot in a Wickr network,
        including its status, group membership, and authentication details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_bot.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_bot)
        """

    def get_bots_count(
        self, **kwargs: Unpack[GetBotsCountRequestTypeDef]
    ) -> GetBotsCountResponseTypeDef:
        """
        Retrieves the count of bots in a Wickr network, categorized by their status
        (pending, active, and total).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_bots_count.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_bots_count)
        """

    def get_data_retention_bot(
        self, **kwargs: Unpack[GetDataRetentionBotRequestTypeDef]
    ) -> GetDataRetentionBotResponseTypeDef:
        """
        Retrieves information about the data retention bot in a Wickr network,
        including its status and whether the data retention service is enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_data_retention_bot.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_data_retention_bot)
        """

    def get_guest_user_history_count(
        self, **kwargs: Unpack[GetGuestUserHistoryCountRequestTypeDef]
    ) -> GetGuestUserHistoryCountResponseTypeDef:
        """
        Retrieves historical guest user count data for a Wickr network, showing the
        number of guest users per billing period over the past 90 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_guest_user_history_count.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_guest_user_history_count)
        """

    def get_network(self, **kwargs: Unpack[GetNetworkRequestTypeDef]) -> GetNetworkResponseTypeDef:
        """
        Retrieves detailed information about a specific Wickr network, including its
        configuration, access level, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_network.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_network)
        """

    def get_network_settings(
        self, **kwargs: Unpack[GetNetworkSettingsRequestTypeDef]
    ) -> GetNetworkSettingsResponseTypeDef:
        """
        Retrieves all network-level settings for a Wickr network, including client
        metrics, data retention, and other configuration options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_network_settings.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_network_settings)
        """

    def get_oidc_info(
        self, **kwargs: Unpack[GetOidcInfoRequestTypeDef]
    ) -> GetOidcInfoResponseTypeDef:
        """
        Retrieves the OpenID Connect (OIDC) configuration for a Wickr network,
        including SSO settings and optional token information if access token
        parameters are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_oidc_info.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_oidc_info)
        """

    def get_security_group(
        self, **kwargs: Unpack[GetSecurityGroupRequestTypeDef]
    ) -> GetSecurityGroupResponseTypeDef:
        """
        Retrieves detailed information about a specific security group in a Wickr
        network, including its settings, member counts, and configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_security_group.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_security_group)
        """

    def get_user(self, **kwargs: Unpack[GetUserRequestTypeDef]) -> GetUserResponseTypeDef:
        """
        Retrieves detailed information about a specific user in a Wickr network,
        including their profile, status, and activity history.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_user.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_user)
        """

    def get_users_count(
        self, **kwargs: Unpack[GetUsersCountRequestTypeDef]
    ) -> GetUsersCountResponseTypeDef:
        """
        Retrieves the count of users in a Wickr network, categorized by their status
        (pending, active, rejected) and showing how many users can still be added.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_users_count.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_users_count)
        """

    def list_blocked_guest_users(
        self, **kwargs: Unpack[ListBlockedGuestUsersRequestTypeDef]
    ) -> ListBlockedGuestUsersResponseTypeDef:
        """
        Retrieves a paginated list of guest users who have been blocked from a Wickr
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/list_blocked_guest_users.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#list_blocked_guest_users)
        """

    def list_bots(self, **kwargs: Unpack[ListBotsRequestTypeDef]) -> ListBotsResponseTypeDef:
        """
        Retrieves a paginated list of bots in a specified Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/list_bots.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#list_bots)
        """

    def list_devices_for_user(
        self, **kwargs: Unpack[ListDevicesForUserRequestTypeDef]
    ) -> ListDevicesForUserResponseTypeDef:
        """
        Retrieves a paginated list of devices associated with a specific user in a
        Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/list_devices_for_user.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#list_devices_for_user)
        """

    def list_guest_users(
        self, **kwargs: Unpack[ListGuestUsersRequestTypeDef]
    ) -> ListGuestUsersResponseTypeDef:
        """
        Retrieves a paginated list of guest users who have communicated with your Wickr
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/list_guest_users.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#list_guest_users)
        """

    def list_networks(
        self, **kwargs: Unpack[ListNetworksRequestTypeDef]
    ) -> ListNetworksResponseTypeDef:
        """
        Retrieves a paginated list of all Wickr networks associated with your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/list_networks.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#list_networks)
        """

    def list_security_group_users(
        self, **kwargs: Unpack[ListSecurityGroupUsersRequestTypeDef]
    ) -> ListSecurityGroupUsersResponseTypeDef:
        """
        Retrieves a paginated list of users who belong to a specific security group in
        a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/list_security_group_users.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#list_security_group_users)
        """

    def list_security_groups(
        self, **kwargs: Unpack[ListSecurityGroupsRequestTypeDef]
    ) -> ListSecurityGroupsResponseTypeDef:
        """
        Retrieves a paginated list of security groups in a specified Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/list_security_groups.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#list_security_groups)
        """

    def list_users(self, **kwargs: Unpack[ListUsersRequestTypeDef]) -> ListUsersResponseTypeDef:
        """
        Retrieves a paginated list of users in a specified Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/list_users.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#list_users)
        """

    def register_oidc_config(
        self, **kwargs: Unpack[RegisterOidcConfigRequestTypeDef]
    ) -> RegisterOidcConfigResponseTypeDef:
        """
        Registers and saves an OpenID Connect (OIDC) configuration for a Wickr network,
        enabling Single Sign-On (SSO) authentication through an identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/register_oidc_config.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#register_oidc_config)
        """

    def register_oidc_config_test(
        self, **kwargs: Unpack[RegisterOidcConfigTestRequestTypeDef]
    ) -> RegisterOidcConfigTestResponseTypeDef:
        """
        Tests an OpenID Connect (OIDC) configuration for a Wickr network by validating
        the connection to the identity provider and retrieving its supported
        capabilities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/register_oidc_config_test.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#register_oidc_config_test)
        """

    def update_bot(self, **kwargs: Unpack[UpdateBotRequestTypeDef]) -> UpdateBotResponseTypeDef:
        """
        Updates the properties of an existing bot in a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/update_bot.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#update_bot)
        """

    def update_data_retention(
        self, **kwargs: Unpack[UpdateDataRetentionRequestTypeDef]
    ) -> UpdateDataRetentionResponseTypeDef:
        """
        Updates the data retention bot settings, allowing you to enable or disable the
        data retention service, or acknowledge the public key message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/update_data_retention.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#update_data_retention)
        """

    def update_guest_user(
        self, **kwargs: Unpack[UpdateGuestUserRequestTypeDef]
    ) -> UpdateGuestUserResponseTypeDef:
        """
        Updates the block status of a guest user in a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/update_guest_user.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#update_guest_user)
        """

    def update_network(
        self, **kwargs: Unpack[UpdateNetworkRequestTypeDef]
    ) -> UpdateNetworkResponseTypeDef:
        """
        Updates the properties of an existing Wickr network, such as its name or
        encryption key configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/update_network.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#update_network)
        """

    def update_network_settings(
        self, **kwargs: Unpack[UpdateNetworkSettingsRequestTypeDef]
    ) -> UpdateNetworkSettingsResponseTypeDef:
        """
        Updates network-level settings for a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/update_network_settings.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#update_network_settings)
        """

    def update_security_group(
        self, **kwargs: Unpack[UpdateSecurityGroupRequestTypeDef]
    ) -> UpdateSecurityGroupResponseTypeDef:
        """
        Updates the properties of an existing security group in a Wickr network, such
        as its name or settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/update_security_group.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#update_security_group)
        """

    def update_user(self, **kwargs: Unpack[UpdateUserRequestTypeDef]) -> UpdateUserResponseTypeDef:
        """
        Updates the properties of an existing user in a Wickr network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/update_user.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#update_user)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_blocked_guest_users"]
    ) -> ListBlockedGuestUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_bots"]
    ) -> ListBotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_devices_for_user"]
    ) -> ListDevicesForUserPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_guest_users"]
    ) -> ListGuestUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_networks"]
    ) -> ListNetworksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_security_group_users"]
    ) -> ListSecurityGroupUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_security_groups"]
    ) -> ListSecurityGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_users"]
    ) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wickr/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/client/#get_paginator)
        """
